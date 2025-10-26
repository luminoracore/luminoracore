"""
Fact Extraction System for LuminoraCore v1.1

Automatically extracts factual information from user conversations.
"""

from dataclasses import dataclass
from typing import List, Optional, Any
from datetime import datetime
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


class FactCategory(Enum):
    """Categories of facts"""
    PERSONAL_INFO = "personal_info"
    PREFERENCES = "preferences"
    RELATIONSHIPS = "relationships"
    HOBBIES = "hobbies"
    GOALS = "goals"
    HEALTH = "health"
    WORK = "work"
    EVENTS = "events"
    OTHER = "other"


@dataclass
class Fact:
    """Represents a fact learned about a user"""
    user_id: str
    category: str
    key: str
    value: Any
    confidence: float = 1.0
    source_message_id: Optional[str] = None
    first_mentioned: Optional[datetime] = None
    context: Optional[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        """Set defaults"""
        if self.first_mentioned is None:
            self.first_mentioned = datetime.now()
        if self.tags is None:
            self.tags = []
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"Confidence must be 0-1, got {self.confidence}")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "user_id": self.user_id,
            "category": self.category,
            "key": self.key,
            "value": self.value,
            "confidence": self.confidence,
            "source_message_id": self.source_message_id,
            "first_mentioned": self.first_mentioned.isoformat() if self.first_mentioned else None,
            "context": self.context,
            "tags": self.tags
        }


class FactExtractor:
    """
    Extracts facts from user messages using LLM
    
    Usage:
        from luminoracore_sdk.providers import DeepSeekProvider
        
        provider = DeepSeekProvider(api_key=key)
        extractor = FactExtractor(llm_provider=provider)
        
        facts = await extractor.extract_from_message(
            user_id="user123",
            message="I'm Diego, I'm 28 and work in IT",
            message_id="msg_123"
        )
    """
    
    def __init__(self, llm_provider=None, confidence_threshold: float = 0.7):
        """
        Initialize fact extractor
        
        Args:
            llm_provider: LLM provider from SDK (optional, can be set later)
            confidence_threshold: Minimum confidence to accept facts
        """
        self.llm_provider = llm_provider
        self.confidence_threshold = confidence_threshold
    
    def build_extraction_prompt(self, message: str, context: Optional[List[str]] = None) -> str:
        """
        Build prompt for fact extraction
        
        Args:
            message: User message
            context: Optional previous messages for context
            
        Returns:
            Prompt string
        """
        prompt = f"""Extract factual information about the user from the following message.

User message: "{message}"

Respond with JSON:
{{
    "facts": [
        {{
            "category": "personal_info | preferences | relationships | hobbies | goals | health | work | events | other",
            "key": "descriptive_fact_name",
            "value": "extracted_value",
            "confidence": 0.0-1.0,
            "tags": ["tag1", "tag2"]
        }}
    ]
}}

Rules:
- Only extract EXPLICIT facts, don't infer
- High confidence (>0.9) only if direct statement
- Key should be descriptive (e.g. "favorite_anime", "pet_name", "age")
- If no facts, return empty array
- Be concise

Examples:

Input: "I'm Diego, I'm 28 and work in IT"
Output:
{{
    "facts": [
        {{"category": "personal_info", "key": "name", "value": "Diego", "confidence": 0.99, "tags": ["name"]}},
        {{"category": "personal_info", "key": "age", "value": 28, "confidence": 0.99, "tags": ["age"]}},
        {{"category": "work", "key": "profession", "value": "IT", "confidence": 0.95, "tags": ["work", "career"]}}
    ]
}}"""
        
        if context:
            prompt += f"\n\nPrevious context:\n" + "\n".join(context)
        
        return prompt
    
    def parse_llm_response(self, response: str) -> List[dict]:
        """
        Parse LLM response into fact dictionaries
        
        Args:
            response: LLM response (JSON string)
            
        Returns:
            List of fact dictionaries
        """
        try:
            # Try to parse as JSON
            data = json.loads(response)
            facts_data = data.get("facts", [])
            return facts_data
        except json.JSONDecodeError:
            # If not valid JSON, try to extract JSON from markdown code block
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
                data = json.loads(json_str)
                return data.get("facts", [])
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
                data = json.loads(json_str)
                return data.get("facts", [])
            else:
                logger.warning(f"Failed to parse LLM response as JSON: {response[:100]}")
                return []
    
    def filter_by_confidence(self, facts_data: List[dict]) -> List[dict]:
        """Filter facts by confidence threshold"""
        return [
            f for f in facts_data
            if f.get("confidence", 0.0) >= self.confidence_threshold
        ]
    
    def create_fact_objects(
        self,
        user_id: str,
        facts_data: List[dict],
        source_message_id: Optional[str] = None
    ) -> List[Fact]:
        """
        Create Fact objects from parsed data
        
        Args:
            user_id: User ID
            facts_data: List of fact dictionaries from LLM
            source_message_id: ID of source message
            
        Returns:
            List of Fact objects
        """
        facts = []
        for fact_data in facts_data:
            try:
                fact = Fact(
                    user_id=user_id,
                    category=fact_data["category"],
                    key=fact_data["key"],
                    value=fact_data["value"],
                    confidence=fact_data.get("confidence", 1.0),
                    source_message_id=source_message_id,
                    tags=fact_data.get("tags", [])
                )
                facts.append(fact)
            except (KeyError, ValueError) as e:
                logger.warning(f"Skipping invalid fact: {e}")
                continue
        
        return facts
    
    async def extract_from_message(
        self,
        user_id: str,
        message: str,
        message_id: Optional[str] = None,
        context: Optional[List[str]] = None
    ) -> List[Fact]:
        """
        Extract facts from a message (main method)
        
        Args:
            user_id: User ID
            message: User message text
            message_id: Message ID (optional)
            context: Previous messages for context (optional)
            
        Returns:
            List of extracted Fact objects
        """
        if not self.llm_provider:
            logger.warning("No LLM provider configured, cannot extract facts")
            return []
        
        # Build prompt
        prompt = self.build_extraction_prompt(message, context)
        
        # Call LLM (async)
        try:
            # Note: This uses SDK provider interface
            response = await self.llm_provider.generate(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500
            )
            
            # Parse response
            facts_data = self.parse_llm_response(response)
            
            # Filter by confidence
            filtered = self.filter_by_confidence(facts_data)
            
            # Create Fact objects
            facts = self.create_fact_objects(user_id, filtered, message_id)
            
            logger.info(f"Extracted {len(facts)} facts from message")
            return facts
            
        except Exception as e:
            logger.error(f"Error extracting facts: {e}")
            return []
    
    def extract_sync(
        self,
        user_id: str,
        message: str,
        message_id: Optional[str] = None
    ) -> List[Fact]:
        """
        Synchronous fact extraction (for testing without LLM)
        
        Simple pattern matching for common facts.
        """
        facts = []
        
        # Simple pattern matching
        message_lower = message.lower()
        
        # Name detection (simple)
        if "i'm " in message_lower or "my name is" in message_lower:
            # Extract name (very basic)
            parts = message.split()
            for i, word in enumerate(parts):
                if word.lower() in ["i'm", "im", "name"]:
                    if i + 1 < len(parts):
                        name = parts[i + 1].strip(",.")
                        facts.append(Fact(
                            user_id=user_id,
                            category="personal_info",
                            key="name",
                            value=name,
                            confidence=0.8,
                            source_message_id=message_id
                        ))
                        break
        
        return facts

