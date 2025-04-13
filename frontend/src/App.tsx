import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Web3ReactProvider } from '@web3-react/core';
import { ethers } from 'ethers';
import { Web3ContextProvider } from './context/Web3Context';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Upload from './pages/Upload';
import ReportDetails from './pages/ReportDetails';
import TestConnection from './pages/TestConnection';

const queryClient = new QueryClient();

function getLibrary(provider: any) {
  return new ethers.providers.Web3Provider(provider);
}

const App: React.FC = () => {
  return (
    <Web3ReactProvider getLibrary={getLibrary}>
      <QueryClientProvider client={queryClient}>
        <Web3ContextProvider>
          <Router>
            <div className="min-h-screen bg-gray-50">
              <Navbar />
              <main className="container mx-auto px-4 py-8">
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/upload" element={<Upload />} />
                  <Route path="/reports/:id" element={<ReportDetails />} />
                  <Route path="/test" element={<TestConnection />} />
                </Routes>
              </main>
            </div>
          </Router>
        </Web3ContextProvider>
      </QueryClientProvider>
    </Web3ReactProvider>
  );
};

export default App;
