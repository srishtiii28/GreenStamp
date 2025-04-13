import os
from typing import Dict, Optional
from web3 import Web3
import ipfshttpclient
from web3.middleware import geth_poa_middleware
import json
import hashlib

class BlockchainService:
    def __init__(self):
        # Initialize Web3
        self.w3 = Web3(Web3.HTTPProvider(os.getenv("POLYGON_RPC_URL")))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        # Initialize IPFS client
        self.ipfs = ipfshttpclient.connect("/ip4/127.0.0.1/tcp/5001")
        
        # Load contract
        with open("contracts/abi/GreenStamp.json") as f:
            contract_abi = json.load(f)
        
        self.contract_address = os.getenv("CONTRACT_ADDRESS")
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=contract_abi
        )
        
        # Set default account
        self.w3.eth.default_account = self.w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))
    
    def upload_to_ipfs(self, file_path: str) -> str:
        """Upload a file to IPFS and return the hash."""
        try:
            result = self.ipfs.add(file_path)
            return result['Hash']
        except Exception as e:
            print(f"Error uploading to IPFS: {e}")
            raise
    
    def calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def upload_report(
        self,
        report_id: str,
        ipfs_hash: str,
        report_hash: str,
        esg_score: int
    ) -> Dict:
        """Upload report metadata to the blockchain."""
        try:
            tx = self.contract.functions.uploadReport(
                report_id,
                ipfs_hash,
                report_hash,
                esg_score
            ).build_transaction({
                'from': self.w3.eth.default_account.address,
                'nonce': self.w3.eth.get_transaction_count(self.w3.eth.default_account.address),
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            signed_tx = self.w3.eth.account.sign_transaction(tx, os.getenv("PRIVATE_KEY"))
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                "tx_hash": tx_hash.hex(),
                "status": receipt.status,
                "block_number": receipt.blockNumber
            }
        except Exception as e:
            print(f"Error uploading to blockchain: {e}")
            raise
    
    def get_report(self, report_id: str) -> Optional[Dict]:
        """Retrieve report metadata from the blockchain."""
        try:
            result = self.contract.functions.getReport(report_id).call()
            return {
                "ipfs_hash": result[0],
                "report_hash": result[1],
                "timestamp": result[2],
                "esg_score": result[3],
                "uploader": result[4],
                "verified": result[5]
            }
        except Exception as e:
            print(f"Error retrieving report: {e}")
            return None 