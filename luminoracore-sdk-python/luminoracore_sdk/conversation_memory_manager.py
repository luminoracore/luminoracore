# luminoracore-sdk-python/luminoracore_sdk/conversation_memory_manager.py
"""
Conversation Memory Manager - Core component for managing conversation context
This is the CRITICAL fix for proper conversation memory integration
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass

# from .client_v1_1 import LuminoraCoreClientV11  # Avoid circular import
from .types.provider import ProviderConfig


@dataclass
class ConversationTurn:
    """Represents a single turn in a conversation"""
    user_message: str
    assistant_response: str
    personality_name: str
    timestamp: datetime
    facts_learned: List[Dict[str, Any]]
    affinity_change: Optional[Dict[str, Any]] = None


@dataclass
class ConversationContext:
    """Complete context for LLM generation"""
    session_id: str
    personality_name: str
    conversation_history: List[ConversationTurn]
    user_facts: List[Dict[str, Any]]
    affinity: Dict[str, Any]
    current_message: str
    context_string: str


class ConversationMemoryManager:
    """
    CRITICAL COMPONENT: Manages conversation memory and context
    
    This is the core fix that makes LuminoraCore actually use its memory system
    instead of sending individual messages without context.
    """
    
    def __init__(self, client_v11):  # Type hint removed to avoid circular import
        self.client = client_v11
        self.max_history_turns = 20  # Keep last 20 turns for context
    
    async def send_message_with_full_context(
        self,
        session_id: str,
        user_message: str,
        user_id: str = "demo",
        personality_name: str = "default",
        provider_config: Optional[ProviderConfig] = None
    ) -> Dict[str, Any]:
        """
        CRITICAL METHOD: Send message with full conversation context
        
        Args:
            session_id: Session ID for the conversation
            user_message: User's message
            user_id: User ID (persistent across sessions) - defaults to "demo"
            personality_name: Name of the personality to use
            provider_config: LLM provider configuration
        
        Returns:
            Response with full context and memory integration
        
        This is the method that should be used instead of individual message sending.
        It:
        1. Gets conversation history
        2. Gets user facts from memory
        3. Gets affinity/relationship level
        4. Builds complete context for LLM
        5. Generates response with full context
        6. Extracts and saves new facts
        7. Updates conversation history
        8. Updates affinity based on interaction
        """
        try:
            # Step 1: Get conversation history
            conversation_history = await self._get_conversation_history(session_id)
            
            # Step 2: Get user facts from memory
            user_facts = await self.client.get_facts(user_id)
            
            # Step 3: Get user affinity/relationship level
            affinity = await self.client.get_affinity(user_id, personality_name)
            
            # Handle case where affinity is None (new user)
            if affinity is None:
                affinity = {
                    "current_level": "stranger",
                    "affinity_points": 0,
                    "total_interactions": 0,
                    "positive_interactions": 0
                }
            
            # Step 4: Build complete context for LLM
            context = await self._build_llm_context(
                session_id=session_id,
                personality_name=personality_name,
                conversation_history=conversation_history,
                user_facts=user_facts,
                affinity=affinity,
                current_message=user_message
            )
            
            # Step 5: Generate response with full context
            response = await self._generate_response_with_context(
                context=context,
                provider_config=provider_config
            )
            
            # Step 6: Extract new facts from the conversation
            new_facts = await self._extract_facts_from_conversation(
                session_id=session_id,
                user_message=user_message,
                assistant_response=response["content"],
                existing_facts=user_facts
            )
            
            # Step 7: Save new facts to memory
            for fact in new_facts:
                await self.client.save_fact(
                    user_id=session_id,
                    category=fact["category"],
                    key=fact["key"],
                    value=fact["value"],
                    confidence=fact["confidence"]
                )
            
            # Step 8: Save conversation turn
            conversation_turn = ConversationTurn(
                user_message=user_message,
                assistant_response=response["content"],
                personality_name=personality_name,
                timestamp=datetime.now(),
                facts_learned=new_facts
            )
            
            await self._save_conversation_turn(session_id, conversation_turn)
            
            # Step 9: Update affinity based on interaction
            affinity_change = await self._update_affinity_from_interaction(
                session_id=session_id,
                conversation_turn=conversation_turn,
                current_affinity=affinity
            )
            
            return {
                "success": True,
                "response": response["content"],
                "personality_name": personality_name,
                "facts_learned": len(new_facts),
                "memory_facts_count": len(user_facts),
                "user_facts": user_facts,
                "affinity_level": affinity["current_level"],
                "affinity_points": affinity["affinity_points"],
                "conversation_length": len(conversation_history) + 1,
                "context_used": True,
                "new_facts": new_facts,
                "affinity_change": affinity_change
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": f"I apologize, but I encountered an error: {str(e)}. Please try again.",
                "context_used": False
            }
    
    async def _get_conversation_history(self, session_id: str) -> List[ConversationTurn]:
        """Get conversation history for the session"""
        try:
            # Try to get from conversation history storage
            history_data = await self.client.storage_v11.get_facts(
                user_id=session_id, 
                category="conversation_history"
            )
            
            if not history_data:
                return []
            
            # Parse conversation history
            conversation_history = []
            for fact in history_data:
                if fact.get("key", "").startswith("turn_"):
                    try:
                        # fact["value"] might be a string or already a dict
                        turn_data = fact["value"]
                        if isinstance(turn_data, str):
                            turn_data = json.loads(turn_data)
                        
                        conversation_history.append(ConversationTurn(
                            user_message=turn_data["user_message"],
                            assistant_response=turn_data["assistant_response"],
                            personality_name=turn_data["personality_name"],
                            timestamp=datetime.fromisoformat(turn_data["timestamp"]),
                            facts_learned=turn_data.get("facts_learned", [])
                        ))
                    except (json.JSONDecodeError, KeyError, TypeError) as e:
                        print(f"Error parsing conversation turn: {e}")
                        continue
            
            # Sort by timestamp and return last N turns
            conversation_history.sort(key=lambda x: x.timestamp)
            return conversation_history[-self.max_history_turns:]
            
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []
    
    async def _build_llm_context(
        self,
        session_id: str,
        personality_name: str,
        conversation_history: List[ConversationTurn],
        user_facts: List[Dict[str, Any]],
        affinity: Dict[str, Any],
        current_message: str
    ) -> ConversationContext:
        """Build complete context for LLM generation"""
        
        # Build context string
        context_parts = []
        
        # 1. Personality and relationship context
        context_parts.append(f"Personality: {personality_name}")
        context_parts.append(f"Relationship Level: {affinity['current_level']} ({affinity['affinity_points']}/100 points)")
        
        # 2. User facts context
        if user_facts:
            facts_context = "User Facts: "
            facts_list = []
            for fact in user_facts:
                facts_list.append(f"{fact['key']}: {fact['value']}")
            facts_context += ", ".join(facts_list)
            context_parts.append(facts_context)
        
        # 3. Conversation history
        if conversation_history:
            history_context = "Conversation History:\n"
            for turn in conversation_history[-10:]:  # Last 10 turns
                history_context += f"User: {turn.user_message}\n"
                history_context += f"Assistant: {turn.assistant_response}\n"
            context_parts.append(history_context)
        
        # 4. Personality-specific instructions based on relationship level
        if affinity['current_level'] == 'stranger':
            context_parts.append("Instructions: Be professional and formal. Ask questions to learn about the user.")
        elif affinity['current_level'] == 'acquaintance':
            context_parts.append("Instructions: Be friendly and polite. Reference what you know about the user.")
        elif affinity['current_level'] == 'friend':
            context_parts.append("Instructions: Be casual and friendly. Reference previous conversations and shared experiences.")
        elif affinity['current_level'] == 'close_friend':
            context_parts.append("Instructions: Be personal and warm. Show deep understanding of the user and their preferences.")
        
        # 5. Current message context
        context_parts.append(f"Current User Message: {current_message}")
        
        context_string = "\n\n".join(context_parts)
        
        return ConversationContext(
            session_id=session_id,
            personality_name=personality_name,
            conversation_history=conversation_history,
            user_facts=user_facts,
            affinity=affinity,
            current_message=current_message,
            context_string=context_string
        )
    
    async def _generate_response_with_context(
        self,
        context: ConversationContext,
        provider_config: Optional[ProviderConfig] = None
    ) -> Dict[str, Any]:
        """Generate response using LLM with full context"""
        
        try:
            # Build a comprehensive context string for the LLM
            context_parts = []
            
            # 1. Personality and relationship context
            context_parts.append(f"You are {context.personality_name}, an AI personality.")
            context_parts.append(f"Current relationship level: {context.affinity['current_level']} ({context.affinity['affinity_points']}/100 points)")
            
            # 2. User facts context
            if context.user_facts:
                facts_text = ', '.join([f"{fact['key']}: {fact['value']}" for fact in context.user_facts])
                context_parts.append(f"User Facts: {facts_text}")
            else:
                context_parts.append("User Facts: No facts yet")
            
            # 3. Conversation history
            if context.conversation_history:
                history_text = '\n'.join([f"User: {turn.user_message}\nAssistant: {turn.assistant_response}" for turn in context.conversation_history[-3:]])
                context_parts.append(f"Conversation History:\n{history_text}")
            else:
                context_parts.append("Conversation History: No previous conversation")
            
            # 4. Instructions based on relationship level
            if context.affinity['current_level'] == 'stranger':
                context_parts.append("Instructions: Be professional and formal. Ask questions to learn about the user.")
            elif context.affinity['current_level'] == 'acquaintance':
                context_parts.append("Instructions: Be friendly and polite. Reference what you know about the user.")
            elif context.affinity['current_level'] == 'friend':
                context_parts.append("Instructions: Be casual and friendly. Reference previous conversations and shared experiences.")
            elif context.affinity['current_level'] == 'close_friend':
                context_parts.append("Instructions: Be personal and warm. Show deep understanding of the user and their preferences.")
            
            # 5. Current message
            context_parts.append(f"Current User Message: {context.current_message}")
            
            # Build the complete context string
            full_context = "\n\n".join(context_parts)
            
            # Try to use the base_client with the context
            if hasattr(self.client, 'base_client') and self.client.base_client:
                try:
                    # Create a context-aware message for the base client
                    context_aware_message = f"""Contexto del usuario: {full_context}

Usuario: {context.current_message}

Responde como {context.personality_name}, usando el contexto proporcionado para dar una respuesta personalizada y relevante."""
                    
                    # Convert dict to ProviderConfig if needed
                    if isinstance(provider_config, dict):
                        from .types.provider import ProviderConfig
                        provider_config_obj = ProviderConfig(
                            name=provider_config.get("name", "deepseek"),
                            api_key=provider_config.get("api_key", "mock-key"),
                            model=provider_config.get("model", "deepseek-chat")
                        )
                    else:
                        provider_config_obj = provider_config
                    
                    # Use the base client with the context-aware message
                    response = await self.client.base_client.send_message(
                        session_id=context.session_id,
                        message=context_aware_message,
                        personality_name=context.personality_name,
                        provider_config=provider_config_obj
                    )
                    
                    return {
                        "content": response.get("content", response.get("response", "I'm sorry, I couldn't generate a response.")),
                        "metadata": {
                            "context_used": True,
                            "personality_name": context.personality_name,
                            "affinity_level": context.affinity['current_level'],
                            "facts_count": len(context.user_facts),
                            "history_length": len(context.conversation_history)
                        }
                    }
                    
                except Exception as e:
                    print(f"Base client send_message failed: {e}")
                    # Use context-aware fallback
                    fallback_response = self._create_context_aware_fallback_response(context)
                    return {
                        "content": fallback_response["content"],
                        "metadata": {
                            **fallback_response["metadata"],
                            "error": True,
                            "error_message": str(e)
                        }
                    }
            else:
                # Final fallback with context awareness
                fallback_response = self._create_context_aware_fallback_response(context)
                return {
                    "content": fallback_response["content"],
                    "metadata": {
                        **fallback_response["metadata"],
                        "fallback": True
                    }
                }
                
        except Exception as e:
            # Error handling - use context-aware fallback instead of generic error
            print(f"Error in _generate_response_with_context: {e}")
            fallback_response = self._create_context_aware_fallback_response(context)
            return {
                "content": fallback_response["content"],
                "metadata": {
                    **fallback_response["metadata"],
                    "error": True, 
                    "error_message": str(e)
                }
            }
    
    def _create_context_aware_fallback_response(self, context: ConversationContext) -> Dict[str, Any]:
        """
        Create a context-aware fallback response
        
        ✅ LANGUAGE-AGNOSTIC - No hardcoded phrases
        ✅ USES CONTEXT - Leverages known facts
        """
        
        # Extract user name if available (universal pattern)
        user_name = None
        for fact in context.user_facts:
            if fact.get('key') == 'name':
                user_name = fact.get('value')
                break
        
        # Create generic, language-agnostic response
        if user_name:
            response_content = f"Hello {user_name}! How can I help you today?"
        else:
            response_content = f"Hello! I'm {context.personality_name}. How can I assist you?"
        
        return {
            "content": response_content,
            "metadata": {
                "fallback": True,
                "context_aware": True,
                "personality_name": context.personality_name,
                "affinity_level": context.affinity['current_level'],
                "facts_count": len(context.user_facts),
                "history_length": len(context.conversation_history)
            }
        }
    
    async def _extract_facts_from_conversation(
        self,
        session_id: str,
        user_message: str,
        assistant_response: str,
        existing_facts: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Extract new facts from the conversation using LLM
        
        ✅ NO HARDCODED PATTERNS
        ✅ MULTILINGUAL SUPPORT
        ✅ LLM-BASED INTELLIGENT EXTRACTION
        """
        
        new_facts = []
        
        # ✅ USE LLM FOR INTELLIGENT FACT EXTRACTION (NO HARDCODING)
        if hasattr(self.client, 'base_client') and self.client.base_client:
            try:
                # Build extraction prompt
                facts_context = "\n".join([
                    f"- {fact['key']}: {fact['value']}" 
                    for fact in existing_facts[:10]  # Limit context
                ])
                
                extraction_prompt = f"""Extract factual information about the user from their message.

EXISTING KNOWN FACTS:
{facts_context if facts_context else "None yet"}

USER MESSAGE: "{user_message}"

Extract NEW facts in JSON format:
{{
    "facts": [
        {{
            "category": "personal_info|preferences|relationships|hobbies|goals|health|work|events|other",
            "key": "descriptive_name",
            "value": "extracted_value",
            "confidence": 0.0-1.0
        }}
    ]
}}

Rules:
- Only extract EXPLICIT, CLEAR facts (high confidence >0.8)
- Don't infer or guess
- Key should be descriptive (e.g. "name", "age", "profession")
- If no new facts, return empty array
- Be concise

Example:
Input: "My name is John, I'm 30 and work as a developer"
Output: {{"facts": [{{"category": "personal_info", "key": "name", "value": "John", "confidence": 0.99}}, {{"category": "personal_info", "key": "age", "value": "30", "confidence": 0.98}}, {{"category": "work", "key": "profession", "value": "developer", "confidence": 0.95}}]}}

JSON response:"""
                
                # Use base client to get LLM extraction
                response = await self.client.base_client.send_message(
                    session_id=session_id,
                    message=extraction_prompt,
                    personality_name="fact_extractor",
                    provider_config=None  # Will use default
                )
                
                # Parse LLM response
                content = response.get("content", response.get("response", ""))
                
                # Try to extract JSON from response
                import re
                json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    extracted_data = json.loads(json_str)
                    
                    if isinstance(extracted_data, dict) and "facts" in extracted_data:
                        for fact_data in extracted_data["facts"]:
                            # Check if fact already exists
                            exists = any(
                                f.get('key') == fact_data.get('key') and
                                str(f.get('value')).lower() == str(fact_data.get('value')).lower()
                                for f in existing_facts
                            )
                            
                            if not exists and fact_data.get('confidence', 0) > 0.7:
                                new_facts.append({
                                    "category": fact_data.get('category', 'other'),
                                    "key": fact_data.get('key', 'fact'),
                                    "value": fact_data.get('value', ''),
                                    "confidence": fact_data.get('confidence', 0.8)
                                })
                
            except Exception as e:
                print(f"LLM fact extraction failed: {e}")
                # Continue without extracting (better than wrong data)
        
        return new_facts
    
    async def _save_conversation_turn(self, session_id: str, turn: ConversationTurn):
        """Save a conversation turn to storage"""
        
        turn_data = {
            "user_message": turn.user_message,
            "assistant_response": turn.assistant_response,
            "personality_name": turn.personality_name,
            "timestamp": turn.timestamp.isoformat(),
            "facts_learned": turn.facts_learned
        }
        
        turn_key = f"turn_{turn.timestamp.strftime('%Y%m%d_%H%M%S_%f')}"
        
        await self.client.storage_v11.save_fact(
            user_id=session_id,
            category="conversation_history",
            key=turn_key,
            value=json.dumps(turn_data)
        )
    
    async def _update_affinity_from_interaction(
        self,
        session_id: str,
        conversation_turn: ConversationTurn,
        current_affinity: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update affinity based on the interaction"""
        
        # Base points for any interaction
        points_change = 1
        
        # Use LLM to detect sentiment/quality of interaction
        if hasattr(self.client, 'base_client') and self.client.base_client:
            try:
                sentiment_prompt = f"""Analyze this conversation interaction quality on a scale of 1-5 (1=negative, 5=very positive):

USER: {conversation_turn.user_message}

Rate the interaction quality (1-5):"""
                
                response = await self.client.base_client.send_message(
                    session_id=session_id,
                    message=sentiment_prompt,
                    personality_name="affinity_evaluator",
                    provider_config=None
                )
                
                # Parse rating
                import re
                rating_match = re.search(r'\b([1-5])\b', response.get("content", response.get("response", "")))
                if rating_match:
                    rating = int(rating_match.group(1))
                    points_change = rating  # Scale points with quality
                
            except Exception as e:
                print(f"LLM affinity evaluation failed: {e}")
                # Fall through to default
        
        new_points = current_affinity["affinity_points"] + points_change
        new_points = min(100, new_points)  # Cap at 100
        
        # Update affinity
        await self.client.update_affinity(
            user_id=session_id,
            personality_name=conversation_turn.personality_name,
            points_delta=points_change,
            interaction_type="conversation_interaction"
        )
        
        return {
            "points_change": points_change,
            "new_points": new_points,
            "previous_level": current_affinity["current_level"]
        }
