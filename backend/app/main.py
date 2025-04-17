from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GreenStamp ESG Analysis API",
    description="Advanced AI-powered ESG Analysis and Compliance Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include AI service routers
from .api import ai_routes, compliance_routes, reporting_routes

app.include_router(ai_routes.router, prefix="/api/ai", tags=["AI Analysis"])
app.include_router(compliance_routes.router, prefix="/api/compliance", tags=["Compliance"])
app.include_router(reporting_routes.router, prefix="/api/reporting", tags=["ESG Reporting"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to GreenStamp ESG Analysis API",
        "features": [
            "Advanced NLP for ESG Analysis",
            "Automated ESG Reporting",
            "Regulatory Compliance Analysis",
            "ESG Performance Insights"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/analyze-document")
async def analyze_document(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        file_path = f"temp/{file.filename}"
        os.makedirs("temp", exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process the document using AI services
        from .services.ai_service import ESGAIService
        ai_service = ESGAIService()
        
        analysis_result = await ai_service.analyze_document(file_path)
        
        # Clean up
        os.remove(file_path)
        
        return analysis_result
    except Exception as e:
        logger.error(f"Error analyzing document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 