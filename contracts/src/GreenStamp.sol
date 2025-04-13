// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GreenStamp {
    struct Report {
        string ipfsHash;
        string reportHash;
        uint256 timestamp;
        uint256 esgScore;
        address uploader;
        bool verified;
    }

    mapping(string => Report) public reports;
    mapping(address => string[]) public userReports;
    
    event ReportUploaded(string indexed reportId, address indexed uploader, uint256 timestamp);
    event ReportVerified(string indexed reportId, bool verified);

    function uploadReport(
        string memory reportId,
        string memory ipfsHash,
        string memory reportHash,
        uint256 esgScore
    ) public {
        require(bytes(reports[reportId].reportHash).length == 0, "Report already exists");
        
        reports[reportId] = Report({
            ipfsHash: ipfsHash,
            reportHash: reportHash,
            timestamp: block.timestamp,
            esgScore: esgScore,
            uploader: msg.sender,
            verified: false
        });
        
        userReports[msg.sender].push(reportId);
        emit ReportUploaded(reportId, msg.sender, block.timestamp);
    }

    function verifyReport(string memory reportId, bool verified) public {
        require(reports[reportId].uploader == msg.sender, "Not authorized");
        reports[reportId].verified = verified;
        emit ReportVerified(reportId, verified);
    }

    function getReport(string memory reportId) public view returns (
        string memory ipfsHash,
        string memory reportHash,
        uint256 timestamp,
        uint256 esgScore,
        address uploader,
        bool verified
    ) {
        Report memory report = reports[reportId];
        return (
            report.ipfsHash,
            report.reportHash,
            report.timestamp,
            report.esgScore,
            report.uploader,
            report.verified
        );
    }

    function getUserReports(address user) public view returns (string[] memory) {
        return userReports[user];
    }
} 