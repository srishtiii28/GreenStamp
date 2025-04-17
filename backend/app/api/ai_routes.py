from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Dict
from ..services.ai_service import ESGAIService
import logging
import os

router = APIRouter()
ai_service = ESGAIService()
logger = logging.getLogger(__name__)

@router.post("/analyze-text")
async def analyze_esg_text(text: str) -> Dict:
    """
    Analyze ESG-related text and provide insights
    """
    try:
        # Use the comprehensive document analysis method
        results = await ai_service.analyze_document(text)
        return results
    except Exception as e:
        logger.error(f"Error analyzing ESG text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract-metrics")
async def extract_esg_metrics(text: str) -> Dict:
    """
    Extract specific ESG metrics from text
    """
    try:
        metrics = await ai_service.extract_esg_metrics(text)
        return metrics
    except Exception as e:
        logger.error(f"Error extracting ESG metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate-compliance")
async def validate_esg_compliance(text: str, standards: List[str]) -> Dict:
    """
    Validate ESG compliance against specified standards
    """
    try:
        compliance = await ai_service.analyze_compliance(text)
        return compliance
    except Exception as e:
        logger.error(f"Error validating ESG compliance: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-document")
async def analyze_esg_document(file: UploadFile = File(...)) -> Dict:
    """
    Analyze ESG document (PDF, image, or text) and provide comprehensive insights
    """
    try:
        # Create temp directory if it doesn't exist
        os.makedirs("temp", exist_ok=True)
        
        # Save uploaded file temporarily
        file_path = f"temp/{file.filename}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        try:
            # Analyze the document
            results = await ai_service.analyze_document(file_path)
            return results
        finally:
            # Clean up temporary file
            if os.path.exists(file_path):
                os.remove(file_path)
                
    except Exception as e:
        logger.error(f"Error analyzing ESG document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 