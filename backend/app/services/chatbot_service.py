from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, AutoModelForQuestionAnswering
import torch
from typing import Dict, List
import json
import logging
from datetime import datetime

class ComplianceChatbot:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Defer loading models — will load only when needed
        self.tokenizer = None
        self.model = None
        self.qa_pipeline = None

        # Load compliance knowledge base
        self.knowledge_base = self._load_knowledge_base()
        
        # Conversation history per user
        self.conversation_history = {}

    def _load_knowledge_base(self) -> Dict:
        return {
            "regulations": {
                "GRI": {
                    "description": "Global Reporting Initiative Standards",
                    "requirements": [
                        "Economic performance disclosure",
                        "Environmental impact reporting",
                        "Social responsibility metrics"
                    ]
                },
                "SASB": {
                    "description": "Sustainability Accounting Standards Board",
                    "requirements": [
                        "Industry-specific metrics",
                        "Financial materiality",
                        "Sustainability risks"
                    ]
                },
                "TCFD": {
                    "description": "Task Force on Climate-related Financial Disclosures",
                    "requirements": [
                        "Climate risk assessment",
                        "Emissions reporting",
                        "Climate strategy"
                    ]
                }
            },
            "common_questions": {
                "reporting_requirements": [
                    "What are the main ESG reporting requirements?",
                    "How often should we report ESG metrics?",
                    "What framework should we use for ESG reporting?"
                ],
                "compliance_process": [
                    "How to start ESG reporting?",
                    "What documents are needed for compliance?",
                    "How to verify ESG data?"
                ]
            }
        }

    async def get_response(self, user_id: str, message: str) -> Dict:
        try:
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            self.conversation_history[user_id].append({
                "role": "user",
                "message": message,
                "timestamp": datetime.now().isoformat()
            })

            response = await self._process_message(message)

            self.conversation_history[user_id].append({
                "role": "bot",
                "message": response["message"],
                "timestamp": datetime.now().isoformat()
            })

            return response
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            raise

    async def _process_message(self, message: str) -> Dict:
        try:
            if self._is_compliance_question(message):
                return await self._handle_compliance_question(message)
            if self._is_regulation_query(message):
                return await self._handle_regulation_query(message)
            return await self._generate_conversation_response(message)
        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            raise

    def _is_compliance_question(self, message: str) -> bool:
        compliance_keywords = [
            "requirement", "regulation", "compliance", "report",
            "standard", "framework", "guideline", "rule"
        ]
        return any(keyword in message.lower() for keyword in compliance_keywords)

    def _is_regulation_query(self, message: str) -> bool:
        regulation_keywords = ["gri", "sasb", "tcfd", "esg"]
        return any(keyword in message.lower() for keyword in regulation_keywords)

    async def _handle_compliance_question(self, message: str) -> Dict:
        try:
            if self.qa_pipeline is None:
                # Lazy-load the QA pipeline using locally cached model
                self.qa_pipeline = pipeline(
                    "question-answering",
                    model="deepset/roberta-base-squad2",
                    tokenizer="deepset/roberta-base-squad2",
                    local_files_only=True
                )

            best_answer = None
            best_score = 0

            for category, questions in self.knowledge_base["common_questions"].items():
                for question in questions:
                    result = self.qa_pipeline(question=message, context=question)
                    if result["score"] > best_score:
                        best_score = result["score"]
                        best_answer = self.knowledge_base["regulations"].get(category, {}).get("description", "")

            if best_score > 0.7:
                return {
                    "message": best_answer,
                    "type": "compliance",
                    "confidence": best_score
                }

            return await self._generate_conversation_response(message)
        except Exception as e:
            self.logger.error(f"Error handling compliance question: {str(e)}")
            raise

    async def _handle_regulation_query(self, message: str) -> Dict:
        try:
            for reg_name, reg_info in self.knowledge_base["regulations"].items():
                if reg_name.lower() in message.lower():
                    return {
                        "message": f"{reg_name}: {reg_info['description']}\nKey requirements:\n" +
                                 "\n".join(f"- {req}" for req in reg_info["requirements"]),
                        "type": "regulation",
                        "regulation": reg_name
                    }

            return await self._generate_conversation_response(message)
        except Exception as e:
            self.logger.error(f"Error handling regulation query: {str(e)}")
            raise

    async def _generate_conversation_response(self, message: str) -> Dict:
        try:
            # Lazy-load DialoGPT
            if self.tokenizer is None or self.model is None:
                self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
                self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

            inputs = self.tokenizer.encode(message + self.tokenizer.eos_token, return_tensors="pt")
            response_ids = self.model.generate(
                inputs,
                max_length=1000,
                pad_token_id=self.tokenizer.eos_token_id,
                no_repeat_ngram_size=3,
                do_sample=True,
                top_k=100,
                top_p=0.7,
                temperature=0.8
            )
            response = self.tokenizer.decode(response_ids[0], skip_special_tokens=True)

            return {
                "message": response,
                "type": "conversation"
            }
        except Exception as e:
            self.logger.error(f"Error generating conversation response: {str(e)}")
            raise

    def get_conversation_history(self, user_id: str) -> List[Dict]:
        return self.conversation_history.get(user_id, [])
