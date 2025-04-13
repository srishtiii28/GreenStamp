import os
from typing import Dict, List, Tuple
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
from transformers import pipeline
import torch

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