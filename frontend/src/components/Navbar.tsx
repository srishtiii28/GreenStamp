import React from 'react';
import { Link } from 'react-router-dom';
import { useWeb3 } from '../context/Web3Context';

const Navbar: React.FC = () => {
  const { connect, disconnect, isConnected, account } = useWeb3();

  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link to="/" className="flex items-center">
              <span className="text-xl font-bold">GreenStamp</span>
            </Link>
          </div>
          <div className="flex items-center">
            {isConnected ? (
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-500">
                  {account?.slice(0, 6)}...{account?.slice(-4)}
                </span>
                <button
                  onClick={disconnect}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
                >
                  Disconnect
                </button>
              </div>
            ) : (
              <button
                onClick={connect}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
              >
                Connect Wallet
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 