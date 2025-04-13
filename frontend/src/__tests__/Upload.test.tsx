import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { Web3ReactProvider } from '@web3-react/core';
import { ethers } from 'ethers';
import Upload from '../pages/Upload';
import { Web3ContextProvider } from '../context/Web3Context';

// Mock the Web3 context
jest.mock('../context/Web3Context', () => ({
  useWeb3: () => ({
    isConnected: true,
    uploadReport: jest.fn(),
  }),
  Web3ContextProvider: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

// Mock axios
jest.mock('axios', () => ({
  post: jest.fn(() => Promise.resolve({
    data: {
      esg_score: 85,
      summary: 'Test summary',
      greenwashing_risk: 'Low',
    },
  })),
}));

function getLibrary(provider: any) {
  return new ethers.providers.Web3Provider(provider);
}

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <Web3ReactProvider getLibrary={getLibrary}>
      <Web3ContextProvider>
        <BrowserRouter>
          {component}
        </BrowserRouter>
      </Web3ContextProvider>
    </Web3ReactProvider>
  );
};

describe('Upload Component', () => {
  it('renders upload form when wallet is connected', () => {
    renderWithProviders(<Upload />);
    expect(screen.getByText('Upload ESG Report')).toBeInTheDocument();
    expect(screen.getByText('Select PDF Report')).toBeInTheDocument();
  });

  it('handles file upload', async () => {
    renderWithProviders(<Upload />);
    
    const file = new File(['dummy content'], 'test.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText(/select pdf report/i);
    
    fireEvent.change(input, { target: { files: [file] } });
    
    const uploadButton = screen.getByText('Upload Report');
    fireEvent.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText('ESG Score:')).toBeInTheDocument();
      expect(screen.getByText('85')).toBeInTheDocument();
      expect(screen.getByText('Low')).toBeInTheDocument();
    });
  });

  it('shows wallet connection message when not connected', () => {
    // Override the mock to return not connected
    jest.mock('../context/Web3Context', () => ({
      useWeb3: () => ({
        isConnected: false,
      }),
    }));
    
    renderWithProviders(<Upload />);
    expect(screen.getByText('Please connect your wallet to upload reports')).toBeInTheDocument();
  });
}); 