import { createContext, useContext, useState, useEffect } from 'react';
import { useWeb3React } from '@web3-react/core';
import { InjectedConnector } from '@web3-react/injected-connector';
import { ethers } from 'ethers';
import { GreenStamp } from '../contracts/GreenStamp';

export const injected = new InjectedConnector({
  supportedChainIds: [80001], // Polygon Mumbai
});

interface Web3ContextType {
  connect: () => Promise<void>;
  disconnect: () => void;
  isConnected: boolean;
  account: string | null;
  contract: ethers.Contract | null;
  uploadReport: (reportId: string, ipfsHash: string, reportHash: string, esgScore: number) => Promise<void>;
  getReport: (reportId: string) => Promise<any>;
}

const Web3Context = createContext<Web3ContextType | null>(null);

export const Web3ContextProvider = ({ children }: { children: React.ReactNode }) => {
  const { activate, deactivate, account, library, active } = useWeb3React();
  const [contract, setContract] = useState<ethers.Contract | null>(null);

  useEffect(() => {
    if (library && active) {
      const contractAddress = process.env.VITE_CONTRACT_ADDRESS;
      const contract = new ethers.Contract(
        contractAddress!,
        GreenStamp.abi,
        library.getSigner()
      );
      setContract(contract);
    }
  }, [library, active]);

  const connect = async () => {
    try {
      await activate(injected);
    } catch (error) {
      console.error('Failed to connect:', error);
    }
  };

  const disconnect = () => {
    deactivate();
  };

  const uploadReport = async (
    reportId: string,
    ipfsHash: string,
    reportHash: string,
    esgScore: number
  ) => {
    if (!contract) throw new Error('Contract not initialized');
    const tx = await contract.uploadReport(reportId, ipfsHash, reportHash, esgScore);
    await tx.wait();
  };

  const getReport = async (reportId: string) => {
    if (!contract) throw new Error('Contract not initialized');
    return await contract.getReport(reportId);
  };

  return (
    <Web3Context.Provider
      value={{
        connect,
        disconnect,
        isConnected: active,
        account: account || null,
        contract,
        uploadReport,
        getReport,
      }}
    >
      {children}
    </Web3Context.Provider>
  );
};

export const useWeb3 = () => {
  const context = useContext(Web3Context);
  if (!context) {
    throw new Error('useWeb3 must be used within a Web3ContextProvider');
  }
  return context;
}; 