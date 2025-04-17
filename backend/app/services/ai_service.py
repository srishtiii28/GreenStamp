import os
from typing import Dict, List, Tuple, Union
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
from transformers import (
    pipeline,
    AutoModelForSequenceClassification,
    AutoTokenizer,
    AutoModelForQuestionAnswering,
    T5ForConditionalGeneration,
    GPT2LMHeadModel
)
import torch
import json
import logging
import re
from datetime import datetime

class ESGAIService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize NLP pipelines
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="finiteautomata/bertweet-base-sentiment-analysis"
        )
        
        self.esg_classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
        
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn"
        )
        
        self.qa_model = pipeline(
            "question-answering",
            model="deepset/roberta-base-squad2"
        )
        
        # Load regulatory knowledge base
        self.regulatory_kb = self._load_regulatory_kb()

    def _load_regulatory_kb(self) -> Dict:
        """Load regulatory knowledge base"""
        # TODO: Load from actual knowledge base
        return {
            "GRI": {"standards": ["GRI 101", "GRI 102", "GRI 103"]},
            "SASB": {"standards": ["Industry-Specific Standards"]},
            "TCFD": {"categories": ["Governance", "Strategy", "Risk Management", "Metrics"]}
        }

    async def analyze_document(self, file_path: str) -> Dict:
        """Comprehensive document analysis"""
        try:
            # Extract text from document
            text = await self._extract_text(file_path)
            
            # Perform various analyses
            summary = await self.generate_summary(text)
            sentiment = await self.analyze_sentiment(text)
            topics = await self.classify_esg_topics(text)
            metrics = await self.extract_esg_metrics(text)
            compliance = await self.analyze_compliance(text)
            risks = await self.identify_risks(text)
            
            return {
                "summary": summary,
                "sentiment": sentiment,
                "topics": topics,
                "metrics": metrics,
                "compliance": compliance,
                "risks": risks,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error in document analysis: {str(e)}")
            raise

    async def generate_summary(self, text: str) -> str:
        """Generate a concise summary of the text"""
        try:
            summary = self.summarizer(text, max_length=130, min_length=30, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            self.logger.error(f"Error generating summary: {str(e)}")
            raise

    async def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment with detailed scoring"""
        try:
            sentiment_results = self.sentiment_analyzer(text)
            
            # Enhanced sentiment analysis
            sentences = text.split('.')
            detailed_sentiment = {
                "overall": sentiment_results[0],
                "sentence_level": [
                    self.sentiment_analyzer(sent)[0] for sent in sentences if sent.strip()
                ]
            }
            
            return detailed_sentiment
        except Exception as e:
            self.logger.error(f"Error in sentiment analysis: {str(e)}")
            raise

    async def classify_esg_topics(self, text: str) -> Dict:
        """Classify ESG topics with detailed categorization"""
        try:
            esg_categories = [
                "Environmental Impact", "Climate Change", "Resource Usage",
                "Social Responsibility", "Employee Relations", "Community Impact",
                "Corporate Governance", "Business Ethics", "Risk Management"
            ]
            
            results = self.esg_classifier(
                text,
                candidate_labels=esg_categories,
                multi_label=True
            )
            
            # Organize results by ESG pillar
            categorized_results = {
                "environmental": [],
                "social": [],
                "governance": []
            }
            
            for label, score in zip(results["labels"], results["scores"]):
                if score > 0.5:  # Confidence threshold
                    if any(term in label.lower() for term in ["environmental", "climate", "resource"]):
                        categorized_results["environmental"].append({"topic": label, "score": score})
                    elif any(term in label.lower() for term in ["social", "employee", "community"]):
                        categorized_results["social"].append({"topic": label, "score": score})
                    else:
                        categorized_results["governance"].append({"topic": label, "score": score})
            
            return categorized_results
        except Exception as e:
            self.logger.error(f"Error in topic classification: {str(e)}")
            raise

    async def extract_esg_metrics(self, text: str) -> Dict:
        """Extract ESG metrics using NLP"""
        try:
            metrics = {
                "environmental": {
                    "carbon_emissions": [],
                    "energy_usage": [],
                    "water_consumption": [],
                    "waste_management": []
                },
                "social": {
                    "employee_diversity": [],
                    "training_hours": [],
                    "safety_incidents": [],
                    "community_investment": []
                },
                "governance": {
                    "board_diversity": [],
                    "ethics_violations": [],
                    "compliance_rate": []
                }
            }
            
            # Extract metrics using regex and NLP
            # Example pattern for carbon emissions
            carbon_pattern = r"(\d+(?:,\d+)?(?:\.\d+)?)\s*(?:tons?|t)?(?:\s*CO2e?|\s*carbon)"
            carbon_matches = re.finditer(carbon_pattern, text, re.IGNORECASE)
            metrics["environmental"]["carbon_emissions"] = [
                {"value": m.group(1), "unit": "tons CO2e"} for m in carbon_matches
            ]
            
            # Add more metric extraction patterns here
            
            return metrics
        except Exception as e:
            self.logger.error(f"Error extracting metrics: {str(e)}")
            raise

    async def analyze_compliance(self, text: str) -> Dict:
        """Analyze regulatory compliance"""
        try:
            compliance_results = {
                "standards_met": [],
                "potential_violations": [],
                "recommendations": []
            }
            
            # Check compliance against known standards
            for standard, details in self.regulatory_kb.items():
                # Use QA model to check compliance
                for requirement in details["standards"]:
                    question = f"Does the text comply with {standard} {requirement}?"
                    answer = self.qa_model(question=question, context=text)
                    
                    if answer["score"] > 0.8:  # High confidence threshold
                        if "yes" in answer["answer"].lower():
                            compliance_results["standards_met"].append(f"{standard} {requirement}")
                        elif "no" in answer["answer"].lower():
                            compliance_results["potential_violations"].append(f"{standard} {requirement}")
            
            return compliance_results
        except Exception as e:
            self.logger.error(f"Error in compliance analysis: {str(e)}")
            raise

    async def identify_risks(self, text: str) -> Dict:
        """Identify ESG risks and opportunities"""
        try:
            risks = {
                "environmental_risks": [],
                "social_risks": [],
                "governance_risks": [],
                "opportunities": []
            }
            
            # Use zero-shot classification for risk identification
            risk_categories = [
                "climate risk", "regulatory risk", "reputation risk",
                "supply chain risk", "human rights risk", "cybersecurity risk"
            ]
            
            risk_results = self.esg_classifier(
                text,
                candidate_labels=risk_categories,
                multi_label=True
            )
            
            # Categorize risks
            for label, score in zip(risk_results["labels"], risk_results["scores"]):
                if score > 0.6:  # Confidence threshold
                    if "climate" in label or "environmental" in label:
                        risks["environmental_risks"].append({"risk": label, "probability": score})
                    elif "human" in label or "social" in label:
                        risks["social_risks"].append({"risk": label, "probability": score})
                    else:
                        risks["governance_risks"].append({"risk": label, "probability": score})
            
            return risks
        except Exception as e:
            self.logger.error(f"Error in risk identification: {str(e)}")
            raise

    async def _extract_text(self, file_path: str) -> str:
        """Extract text from document"""
        try:
            if file_path.lower().endswith('.pdf'):
                return self._extract_text_from_pdf(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            self.logger.error(f"Error extracting text: {str(e)}")
            raise

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using OCR"""
        images = convert_from_path(pdf_path)
        text = ""
        
        for image in images:
            # Convert to grayscale
            gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
            
            # Apply thresholding
            _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            
            # Extract text
            page_text = pytesseract.image_to_string(binary)
            text += page_text + "\n"
        
        return text

class AIService:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using OCR."""
        images = convert_from_path(pdf_path)
        text = ""
        
        for image in images:
            # Convert to grayscale
            gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
            
            # Apply thresholding
            _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            
            # Extract text
            page_text = pytesseract.image_to_string(binary)
            text += page_text + "\n"
            
        return text
    
    def analyze_esg_report(self, text: str) -> Dict:
        """Analyze ESG report text and return insights."""
        # Generate summary
        summary = self.summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        
        # Analyze sentiment and detect potential greenwashing
        sentences = text.split('.')
        greenwashing_indicators = [
            "sustainable", "green", "eco-friendly", "environmentally friendly",
            "carbon neutral", "net zero", "renewable", "clean energy"
        ]
        
        greenwashing_score = 0
        for sentence in sentences:
            if any(indicator in sentence.lower() for indicator in greenwashing_indicators):
                sentiment = self.classifier(sentence)[0]
                if sentiment['label'] == 'NEGATIVE':
                    greenwashing_score += 1
        
        # Calculate ESG score (mock implementation)
        esg_score = max(0, min(100, 85 - greenwashing_score * 5))
        
        # Check for missing disclosures
        required_disclosures = [
            "carbon emissions",
            "energy consumption",
            "waste management",
            "water usage",
            "employee diversity",
            "community engagement",
            "board composition",
            "executive compensation"
        ]
        
        missing_disclosures = [
            disclosure for disclosure in required_disclosures
            if disclosure not in text.lower()
        ]
        
        return {
            "summary": summary,
            "esg_score": esg_score,
            "greenwashing_risk": "High" if greenwashing_score > 5 else "Medium" if greenwashing_score > 2 else "Low",
            "missing_disclosures": missing_disclosures
        }
    
    def process_report(self, pdf_path: str) -> Dict:
        """Process an ESG report and return analysis results."""
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        
        # Analyze content
        analysis = self.analyze_esg_report(text)
        
        return analysis 