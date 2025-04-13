import React from 'react';
import { useState } from 'react';
import { useWeb3 } from '../context/Web3Context';
import axios from 'axios';

const Upload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const { isConnected, uploadReport } = useWeb3();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file || !isConnected) return;

    setUploading(true);
    try {
      // Upload to backend for AI analysis
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post('http://localhost:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // TODO: Upload to IPFS and get hash
      const ipfsHash = 'mock_ipfs_hash';
      const reportHash = 'mock_report_hash';

      // Upload to blockchain
      await uploadReport(
        `report_${Date.now()}`,
        ipfsHash,
        reportHash,
        response.data.esg_score
      );

      setResult(response.data);
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold mb-4">Upload Report</h1>
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-2xl font-bold mb-6">Upload ESG Report</h2>
          
          {!isConnected ? (
            <div className="text-center py-8">
              <p className="text-gray-600 mb-4">Please connect your wallet to upload reports</p>
            </div>
          ) : (
            <>
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Select PDF Report
                </label>
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileChange}
                  className="block w-full text-sm text-gray-500
                    file:mr-4 file:py-2 file:px-4
                    file:rounded-md file:border-0
                    file:text-sm file:font-semibold
                    file:bg-green-50 file:text-green-700
                    hover:file:bg-green-100"
                />
              </div>

              <button
                onClick={handleUpload}
                disabled={!file || uploading}
                className={`w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white
                  ${!file || uploading
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-green-600 hover:bg-green-700'
                  }`}
              >
                {uploading ? 'Uploading...' : 'Upload Report'}
              </button>

              {result && (
                <div className="mt-6 p-4 bg-gray-50 rounded-md">
                  <h3 className="text-lg font-medium mb-2">Analysis Results</h3>
                  <div className="space-y-2">
                    <p><span className="font-medium">ESG Score:</span> {result.esg_score}</p>
                    <p><span className="font-medium">Summary:</span> {result.summary}</p>
                    <p><span className="font-medium">Greenwashing Risk:</span> {result.greenwashing_risk}</p>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Upload; 