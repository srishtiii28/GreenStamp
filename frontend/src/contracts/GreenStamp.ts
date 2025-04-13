export const GreenStamp = {
  address: process.env.VITE_CONTRACT_ADDRESS,
  abi: [
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "reportId",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "ipfsHash",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "reportHash",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "esgScore",
          "type": "uint256"
        }
      ],
      "name": "uploadReport",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "reportId",
          "type": "string"
        }
      ],
      "name": "getReport",
      "outputs": [
        {
          "components": [
            {
              "internalType": "string",
              "name": "ipfsHash",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "reportHash",
              "type": "string"
            },
            {
              "internalType": "uint256",
              "name": "esgScore",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "timestamp",
              "type": "uint256"
            }
          ],
          "internalType": "struct GreenStamp.Report",
          "name": "",
          "type": "tuple"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
  ]
};

export interface Report {
  ipfsHash: string;
  reportHash: string;
  esgScore: number;
  timestamp: number;
} 