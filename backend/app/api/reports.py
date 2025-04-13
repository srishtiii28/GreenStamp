from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
import uuid
from ..models.report import Report, ReportCreate, create_report, get_report, get_reports
from ..services.ai_service import AIService
from ..services.blockchain_service import BlockchainService

router = APIRouter()
ai_service = AIService()
blockchain_service = BlockchainService()

@router.post("/upload", response_model=Report)
async def upload_report(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        file_path = f"temp/{uuid.uuid4()}.pdf"
        os.makedirs("temp", exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process report with AI
        analysis = ai_service.process_report(file_path)
        
        # Upload to IPFS
        ipfs_hash = blockchain_service.upload_to_ipfs(file_path)
        
        # Calculate file hash
        report_hash = blockchain_service.calculate_file_hash(file_path)
        
        # Create report ID
        report_id = f"report_{uuid.uuid4()}"
        
        # Upload to blockchain
        blockchain_service.upload_report(
            report_id=report_id,
            ipfs_hash=ipfs_hash,
            report_hash=report_hash,
            esg_score=analysis["esg_score"]
        )
        
        # Create report in database
        report = ReportCreate(
            report_id=report_id,
            ipfs_hash=ipfs_hash,
            report_hash=report_hash,
            esg_score=analysis["esg_score"],
            summary=analysis["summary"],
            greenwashing_risk=analysis["greenwashing_risk"],
            missing_disclosures=analysis["missing_disclosures"]
        )
        
        db_report = create_report(report)
        
        # Clean up
        os.remove(file_path)
        
        return db_report
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Report])
async def list_reports():
    return get_reports()

@router.get("/{report_id}", response_model=Report)
async def get_report_by_id(report_id: int):
    report = get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report 