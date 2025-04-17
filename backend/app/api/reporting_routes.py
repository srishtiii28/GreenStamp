from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from ..services.ai_service import ESGAIService
import logging

router = APIRouter()
ai_service = ESGAIService()
logger = logging.getLogger(__name__)

class ReportGenerationRequest(BaseModel):
    metrics: Dict
    topics: Dict
    compliance_results: Dict
    risks: Dict
    industry_sector: Optional[str] = None
    time_period: Optional[str] = None

class ReportAnalysisRequest(BaseModel):
    text: str
    report_type: str
    industry_sector: Optional[str] = None

@router.post("/generate")
async def generate_report(request: ReportGenerationRequest) -> Dict:
    """
    Generate an ESG report based on analyzed data
    """
    try:
        report_sections = {
            "executive_summary": "",
            "environmental_performance": [],
            "social_impact": [],
            "governance_practices": [],
            "risk_assessment": [],
            "recommendations": []
        }

        # Process environmental metrics
        env_metrics = request.metrics.get("environmental", {})
        for metric_name, values in env_metrics.items():
            if values:  # Only add if there are values
                report_sections["environmental_performance"].append({
                    "metric": metric_name.replace("_", " ").title(),
                    "values": values
                })

        # Process social metrics
        social_metrics = request.metrics.get("social", {})
        for metric_name, values in social_metrics.items():
            if values:
                report_sections["social_impact"].append({
                    "metric": metric_name.replace("_", " ").title(),
                    "values": values
                })

        # Process governance metrics
        gov_metrics = request.metrics.get("governance", {})
        for metric_name, values in gov_metrics.items():
            if values:
                report_sections["governance_practices"].append({
                    "metric": metric_name.replace("_", " ").title(),
                    "values": values
                })

        # Add risk assessment
        for risk_type, risks in request.risks.items():
            if risks:
                report_sections["risk_assessment"].extend([
                    {
                        "type": risk_type.replace("_", " ").title(),
                        "risk": risk["risk"],
                        "probability": risk["probability"]
                    }
                    for risk in risks
                ])

        # Generate recommendations based on compliance results
        if request.compliance_results.get("missing_requirements"):
            report_sections["recommendations"].extend([
                f"Address compliance gap in: {req}"
                for req in request.compliance_results["missing_requirements"]
            ])

        # Generate executive summary
        env_score = len(report_sections["environmental_performance"])
        social_score = len(report_sections["social_impact"])
        gov_score = len(report_sections["governance_practices"])
        total_metrics = env_score + social_score + gov_score

        report_sections["executive_summary"] = (
            f"ESG Performance Overview\n"
            f"Total Metrics Tracked: {total_metrics}\n"
            f"Environmental Metrics: {env_score}\n"
            f"Social Metrics: {social_score}\n"
            f"Governance Metrics: {gov_score}\n"
            f"Risk Factors Identified: {len(report_sections['risk_assessment'])}\n"
            f"Recommendations: {len(report_sections['recommendations'])}"
        )

        return report_sections
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
async def analyze_report(request: ReportAnalysisRequest) -> Dict:
    """
    Analyze an existing ESG report
    """
    try:
        # Use AI service to analyze the report
        analysis = await ai_service.analyze_document(request.text)
        
        # Add report-specific analysis
        report_analysis = {
            "report_type": request.report_type,
            "industry_sector": request.industry_sector,
            "completeness_score": 0.0,
            "quality_score": 0.0,
            "missing_elements": [],
            **analysis
        }

        # Calculate completeness score based on required elements
        required_elements = [
            "environmental_metrics",
            "social_metrics",
            "governance_metrics",
            "risk_assessment",
            "compliance_statement"
        ]

        present_elements = sum(1 for elem in required_elements if elem in request.text.lower())
        report_analysis["completeness_score"] = (present_elements / len(required_elements)) * 100

        # Calculate quality score based on various factors
        quality_factors = {
            "has_quantitative_metrics": bool(analysis["metrics"]["environmental"]["carbon_emissions"]),
            "has_risk_assessment": bool(analysis["risks"]["environmental_risks"]),
            "has_compliance_info": bool(analysis["compliance"]["standards_met"]),
            "has_detailed_topics": bool(analysis["topics"]["environmental"] or 
                                     analysis["topics"]["social"] or 
                                     analysis["topics"]["governance"])
        }
        report_analysis["quality_score"] = (sum(quality_factors.values()) / len(quality_factors)) * 100

        # Identify missing elements
        report_analysis["missing_elements"] = [
            elem.replace("_", " ").title()
            for elem in required_elements
            if elem not in request.text.lower()
        ]

        return report_analysis
    except Exception as e:
        logger.error(f"Error analyzing report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates")
async def get_report_templates() -> Dict:
    """
    Get available report templates
    """
    try:
        return {
            "templates": [
                {
                    "id": "standard_esg",
                    "name": "Standard ESG Report",
                    "description": "Comprehensive ESG report covering all major aspects",
                    "sections": [
                        "Executive Summary",
                        "Environmental Performance",
                        "Social Impact",
                        "Governance Practices",
                        "Risk Assessment",
                        "Recommendations"
                    ]
                },
                {
                    "id": "environmental_focus",
                    "name": "Environmental Impact Report",
                    "description": "Detailed analysis of environmental performance",
                    "sections": [
                        "Executive Summary",
                        "Carbon Emissions",
                        "Energy Usage",
                        "Water Management",
                        "Waste Management",
                        "Environmental Risks",
                        "Recommendations"
                    ]
                },
                {
                    "id": "governance_focus",
                    "name": "Governance Report",
                    "description": "Focus on corporate governance and compliance",
                    "sections": [
                        "Executive Summary",
                        "Board Structure",
                        "Risk Management",
                        "Compliance Overview",
                        "Ethics and Policies",
                        "Recommendations"
                    ]
                }
            ]
        }
    except Exception as e:
        logger.error(f"Error getting templates: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 