from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import os
from dotenv import load_dotenv
from web3 import Web3
import ipfshttpclient
import json
from .api import reports

# Load environment variables
load_dotenv()

app = FastAPI(title="GreenStamp API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Web3 and IPFS
w3 = Web3(Web3.HTTPProvider(os.getenv("POLYGON_RPC_URL")))
ipfs_client = ipfshttpclient.connect("/ip4/127.0.0.1/tcp/5001")

# Load contract ABI and address
with open("contracts/abi/GreenStamp.json") as f:
    contract_abi = json.load(f)

contract_address = os.getenv("CONTRACT_ADDRESS")
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Include routers
app.include_router(reports.router, prefix="/reports", tags=["reports"])

@app.get("/")
async def root():
    return {"message": "Welcome to GreenStamp API"}

@app.post("/upload")
async def upload_report(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        file_path = f"temp/{file.filename}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # TODO: Implement AI analysis
        # For now, return mock data
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "esg_score": 85,
            "summary": "Mock ESG report summary",
            "greenwashing_risk": "Low"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reports")
async def get_reports():
    # TODO: Implement report listing
    return {"reports": []}

@app.get("/reports/{report_id}")
async def get_report(report_id: str):
    # TODO: Implement report retrieval
    return {"report_id": report_id, "details": {}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 