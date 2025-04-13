import React from 'react';
import { useWeb3 } from '../context/Web3Context';

const TestConnection: React.FC = () => {
  const { connect, disconnect, isConnected, account } = useWeb3();

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-6 text-center">Wallet Connection Test</h1>
        
        {!isConnected ? (
          <button
            onClick={connect}
            className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors"
          >
            Connect Wallet
          </button>
        ) : (
          <div className="space-y-4">
            <p className="text-center text-gray-700">
              Connected Account: <span className="font-mono">{account}</span>
            </p>
            <button
              onClick={disconnect}
              className="w-full bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700 transition-colors"
            >
              Disconnect Wallet
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default TestConnection; 