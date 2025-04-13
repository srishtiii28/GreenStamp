import React from 'react';
import { useParams } from 'react-router-dom';

const ReportDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold mb-4">Report Details</h1>
        <div className="bg-white shadow rounded-lg p-6">
          <p>Report ID: {id}</p>
        </div>
      </div>
    </div>
  );
};

export default ReportDetails; 