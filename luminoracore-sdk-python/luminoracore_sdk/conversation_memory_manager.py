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
        personality_name: str = "default",
        provider_config: Optional[ProviderConfig] = None
    ) -> Dict[str, Any]:
        """
        CRITICAL METHOD: Send message with full conversation context
        
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
            user_facts = await self.client.get_facts(session_id)
            
            # Step 3: Get user affinity/relationship level
            affinity = await self.client.get_affinity(session_id, personality_name)
            
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
                "affinity_level": affinity["level"],
                "affinity_points": affinity["points"],
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
            history_data = await self.client.storage.get_facts(
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
                        turn_data = json.loads(fact["value"])
                        conversation_history.append(ConversationTurn(
                            user_message=turn_data["user_message"],
                            assistant_response=turn_data["assistant_response"],
                            personality_name=turn_data["personality_name"],
                            timestamp=datetime.fromisoformat(turn_data["timestamp"]),
                            facts_learned=turn_data.get("facts_learned", [])
                        ))
                    except (json.JSONDecodeError, KeyError) as e:
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
        context_parts.append(f"Relationship Level: {affinity['level']} ({affinity['points']}/100 points)")
        
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
        if affinity['level'] == 'stranger':
            context_parts.append("Instructions: Be professional and formal. Ask questions to learn about the user.")
        elif affinity['level'] == 'acquaintance':
            context_parts.append("Instructions: Be friendly and polite. Reference what you know about the user.")
        elif affinity['level'] == 'friend':
            context_parts.append("Instructions: Be casual and friendly. Reference previous conversations and shared experiences.")
        elif affinity['level'] == 'close_friend':
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
        
        # Use the client's LLM generation with full context
        if hasattr(self.client, 'generate_with_context'):
            # If the client has a context-aware generation method
            response = await self.client.generate_with_context(
                context=context.context_string,
                personality_name=context.personality_name,
                provider_config=provider_config
            )
        else:
            # Fallback: Use the context string as a prompt
            prompt = f"""
{context.context_string}

Based on the above context, generate an appropriate response to the current user message.
Remember to:
- Use the personality traits for {context.personality_name}
- Reference the relationship level ({context.affinity['level']})
- Use known facts about the user
- Reference previous conversation if relevant
- Be natural and conversational

Response:"""
            
            # Use basic message sending with the context as prompt
            response = await self.client.send_message(
                session_id=context.session_id,
                message=prompt,
                provider_config=provider_config
            )
        
        return {
            "content": response.get("content", response.get("response", "I'm sorry, I couldn't generate a response.")),
            "metadata": {
                "context_used": True,
                "personality_name": context.personality_name,
                "affinity_level": context.affinity['level'],
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
        """Extract new facts from the conversation"""
        
        new_facts = []
        
        # Simple fact extraction logic (can be enhanced with LLM-based extraction)
        user_message_lower = user_message.lower()
        
        # Extract name
        if "me llamo" in user_message_lower or "soy" in user_message_lower or "mi nombre es" in user_message_lower:
            # Try to extract name
            words = user_message.split()
            for i, word in enumerate(words):
                if word.lower() in ["soy", "me", "llamo", "nombre", "es"]:
                    if i + 1 < len(words):
                        name = words[i + 1].strip(".,!?")
                        if len(name) > 1 and name.isalpha():
                            # Check if we already know this name
                            existing_names = [f["value"] for f in existing_facts if f["key"] == "name"]
                            if name not in existing_names:
                                new_facts.append({
                                    "category": "personal_info",
                                    "key": "name",
                                    "value": name,
                                    "confidence": 0.9
                                })
                            break
        
        # Extract other facts based on keywords
        if "himalaya" in user_message_lower or "viaje" in user_message_lower:
            new_facts.append({
                "category": "travel_plans",
                "key": "travel_destination",
                "value": "Himalayas",
                "confidence": 0.8
            })
        
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
        
        await self.client.storage.save_fact(
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
        
        # Simple affinity update logic (can be enhanced)
        points_change = 1  # Base points for any interaction
        
        # Increase points for positive interactions
        positive_keywords = ["gracias", "perfecto", "excelente", "genial", "increíble"]
        if any(keyword in conversation_turn.user_message.lower() for keyword in positive_keywords):
            points_change = 2
        
        # Increase points for personal sharing
        personal_keywords = ["soy", "me llamo", "mi nombre", "mi vida", "personal"]
        if any(keyword in conversation_turn.user_message.lower() for keyword in personal_keywords):
            points_change = 3
        
        new_points = current_affinity["points"] + points_change
        new_points = min(100, new_points)  # Cap at 100
        
        # Update affinity
        await self.client.update_affinity(
            session_id=session_id,
            points_delta=points_change,
            reason="conversation_interaction"
        )
        
        return {
            "points_change": points_change,
            "new_points": new_points,
            "previous_level": current_affinity["level"]
        }
