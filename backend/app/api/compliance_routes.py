from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from ..services.ai_service import ESGAIService
import logging

router = APIRouter()
ai_service = ESGAIService()
logger = logging.getLogger(__name__)

class ComplianceRequest(BaseModel):
    text: str
    frameworks: List[str]
    industry_sector: Optional[str] = None

@router.post("/validate")
async def validate_compliance(request: ComplianceRequest) -> Dict:
    """
    Validate ESG compliance against specified frameworks
    """
    try:
        compliance_results = await ai_service.analyze_compliance(request.text)
        return compliance_results
    except Exception as e:
        logger.error(f"Error in compliance validation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/frameworks")
async def get_frameworks() -> Dict:
    """
    Get list of supported compliance frameworks
    """
    try:
        return {
            "frameworks": [
                {
                    "id": "GRI",
                    "name": "Global Reporting Initiative",
                    "description": "Comprehensive sustainability reporting standards",
                    "categories": ["Economic", "Environmental", "Social"]
                },
                {
                    "id": "SASB",
                    "name": "Sustainability Accounting Standards Board",
                    "description": "Industry-specific sustainability standards",
                    "categories": ["Financial Materiality", "Industry Metrics"]
                },
                {
                    "id": "TCFD",
                    "name": "Task Force on Climate-related Financial Disclosures",
                    "description": "Climate-related financial risk disclosures",
                    "categories": ["Governance", "Strategy", "Risk Management", "Metrics"]
                }
            ]
        }
    except Exception as e:
        logger.error(f"Error getting frameworks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/requirements/{framework_id}")
async def get_framework_requirements(framework_id: str) -> Dict:
    """
    Get detailed requirements for a specific framework
    """
    try:
        frameworks = {
            "GRI": {
                "name": "Global Reporting Initiative",
                "version": "Standards 2021",
                "requirements": [
                    {
                        "id": "GRI-2",
                        "title": "General Disclosures",
                        "items": [
                            "Organizational details",
                            "Reporting practices",
                            "Activities and workers",
                            "Governance",
                            "Strategy and policies",
                            "Stakeholder engagement"
                        ]
                    },
                    {
                        "id": "GRI-3",
                        "title": "Material Topics",
                        "items": [
                            "Process to determine material topics",
                            "List of material topics",
                            "Management of material topics"
                        ]
                    }
                ]
            },
            "SASB": {
                "name": "SASB Standards",
                "version": "2021",
                "requirements": [
                    {
                        "id": "SASB-ENV",
                        "title": "Environmental Metrics",
                        "items": [
                            "GHG emissions",
                            "Air quality",
                            "Energy management",
                            "Water management",
                            "Waste management"
                        ]
                    },
                    {
                        "id": "SASB-SOC",
                        "title": "Social Capital",
                        "items": [
                            "Human rights",
                            "Customer privacy",
                            "Data security",
                            "Access and affordability",
                            "Product quality and safety"
                        ]
                    }
                ]
            },
            "TCFD": {
                "name": "TCFD Framework",
                "version": "2021",
                "requirements": [
                    {
                        "id": "TCFD-GOV",
                        "title": "Governance",
                        "items": [
                            "Board oversight",
                            "Management role"
                        ]
                    },
                    {
                        "id": "TCFD-STRAT",
                        "title": "Strategy",
                        "items": [
                            "Climate-related risks and opportunities",
                            "Impact on organization",
                            "Resilience of strategy"
                        ]
                    },
                    {
                        "id": "TCFD-RISK",
                        "title": "Risk Management",
                        "items": [
                            "Risk identification process",
                            "Risk management process",
                            "Integration into overall risk management"
                        ]
                    }
                ]
            }
        }
        
        if framework_id not in frameworks:
            raise HTTPException(
                status_code=404,
                detail=f"Framework '{framework_id}' not found"
            )
        
        return frameworks[framework_id]
    except Exception as e:
        logger.error(f"Error getting framework requirements: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/check-requirements")
async def check_requirements(request: ComplianceRequest) -> Dict:
    """
    Check if text meets specific framework requirements
    """
    try:
        # Get framework requirements
        requirements = []
        for framework in request.frameworks:
            try:
                framework_reqs = await get_framework_requirements(framework)
                requirements.extend([
                    item
                    for section in framework_reqs["requirements"]
                    for item in section["items"]
                ])
            except HTTPException:
                continue

        # Check compliance for each requirement
        compliance_results = {
            "met_requirements": [],
            "missing_requirements": [],
            "partial_requirements": [],
            "framework_scores": {}
        }

        # Use AI service to analyze compliance
        analysis = await ai_service.analyze_compliance(request.text)
        
        # Map analysis results to requirements
        for req in requirements:
            if req in analysis["standards_met"]:
                compliance_results["met_requirements"].append(req)
            elif req in analysis["potential_violations"]:
                compliance_results["missing_requirements"].append(req)
            else:
                compliance_results["partial_requirements"].append(req)

        # Calculate framework-specific scores
        for framework in request.frameworks:
            try:
                framework_reqs = await get_framework_requirements(framework)
                total_reqs = sum(len(section["items"]) for section in framework_reqs["requirements"])
                met_reqs = len([
                    req for req in compliance_results["met_requirements"]
                    if any(req in section["items"] for section in framework_reqs["requirements"])
                ])
                compliance_results["framework_scores"][framework] = (met_reqs / total_reqs) * 100
            except HTTPException:
                continue

        return compliance_results
    except Exception as e:
        logger.error(f"Error checking requirements: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 