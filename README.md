# GreenStamp 

GreenStamp is an AI + Blockchain-powered platform for analyzing ESG (Environmental, Social, and Governance) reports to detect greenwashing, automate ESG compliance scoring, and store tamper-proof report hashes on-chain.

## Features

- **AI-Powered ESG Analysis**
  - OCR + NLP for content extraction and analysis
  - Automated ESG compliance scoring
  - Greenwashing detection using advanced ML models
  - Report summarization and missing disclosure detection

- **Blockchain Integration**
  - Tamper-proof report hash storage on Polygon
  - IPFS-based decentralized document storage
  - Instant verification of report authenticity

- **User Interface**
  - Modern, responsive dashboard
  - File upload portal
  - Interactive ESG score visualization
  - Blockchain verification status display
  - Searchable and sortable report database

## Tech Stack

- **Frontend**: React + Tailwind CSS
- **Backend**: FastAPI (Python)
- **AI/ML**: HuggingFace Transformers, OpenCV, Tesseract
- **Blockchain**: Solidity, Polygon (Mumbai), Ethers.js
- **Storage**: IPFS (via web3.storage)

## Project Structure

```
greenstamp/
├── frontend/           # React frontend application
├── backend/            # FastAPI backend service
├── contracts/          # Solidity smart contracts
├── ai/                 # AI/ML models and pipelines
└── docs/              # Documentation
```

## Getting Started

### Prerequisites

- Node.js (v16+)
- Python (v3.9+)
- MetaMask wallet
- Polygon Mumbai testnet tokens

### Installation

1. Clone the repository
2. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```
3. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
4. Set up environment variables (see `.env.example` files)
5. Start the development servers:
   ```bash
   # Frontend
   cd frontend
   npm run dev
   
   # Backend
   cd backend
   uvicorn main:app --reload
   ```

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.