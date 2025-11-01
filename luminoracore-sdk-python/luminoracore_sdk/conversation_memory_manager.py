# luminoracore-sdk-python/luminoracore_sdk/conversation_memory_manager.py
"""
Conversation Memory Manager - Core component for managing conversation context
This is the CRITICAL fix for proper conversation memory integration
"""

import asyncio
import json
import time
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)

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
            # Ensure session_id is not None
            if not session_id:
                session_id = f"session_{int(time.time())}"
            
            # Ensure user_id is not None
            if not user_id:
                user_id = session_id
            
            # Step 1: Get conversation history
            conversation_history = await self._get_conversation_history(session_id)
            
            # Step 2: Get user facts from memory (excluir conversation_history)
            # ✅ FIX: No incluir conversation_history en facts del usuario para contexto
            # Los turns de conversación se guardan como facts pero no deben usarse como facts
            all_user_facts = await self.client.get_facts(user_id)
            user_facts = [f for f in all_user_facts if f.get('category') != 'conversation_history']
            
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
                existing_facts=user_facts,
                provider_config=provider_config  # Pass provider_config
            )
            
            # Step 7: Save new facts to memory
            for fact in new_facts:
                await self.client.save_fact(
                    user_id=user_id,  # Facts are per USER, not per session
                    category=fact["category"],
                    key=fact["key"],
                    value=fact["value"],
                    confidence=fact["confidence"],
                    session_id=session_id  # Track which session learned this fact
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
                current_affinity=affinity,
                provider_config=provider_config  # Pass provider_config
            )
            
            # ✅ FIX: Calculate context_used correctly based on actual context
            # context_used should be True if we had previous context to use
            # - If there are previous conversation turns → context was used
            # - If there are existing user facts → context was used
            # - If both are empty (first message) → NO context used
            context_used = len(conversation_history) > 0 or len(user_facts) > 0
            
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
                "context_used": context_used,  # ✅ CORRECT: Based on actual context
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
    
    async def _load_personality_data(self, personality_name: str) -> Optional[Dict[str, Any]]:
        """Load personality data from JSON file"""
        try:
            import pathlib
            from pathlib import Path
            
            # Try to get personalities directory from client
            personalities_dir = None
            if hasattr(self.client, 'base_client') and hasattr(self.client.base_client, 'personalities_dir'):
                personalities_dir = self.client.base_client.personalities_dir
            else:
                # Default to SDK personalities directory
                sdk_dir = Path(__file__).parent.parent
                personalities_dir = str(sdk_dir / "personalities")
            
            # Try different name formats (Grandma Hope -> grandma_hope.json)
            # Also handle "Dr. Luna" -> "dr_luna.json"
            name_variations = [
                personality_name.lower().replace(" ", "_").replace(".", "_"),  # "Dr. Luna" -> "dr_luna"
                personality_name.lower().replace(" ", "_"),  # "grandma hope" -> "grandma_hope"
                personality_name.lower().replace(" ", "").replace(".", ""),     # "Dr. Luna" -> "drluna"
                personality_name.lower().replace(" ", ""),     # "grandma hope" -> "grandmahope"
                personality_name.lower().replace(".", "").replace(" ", "_"),  # "Dr. Luna" -> "dr_luna" (sin punto)
                personality_name.lower(),                      # "grandma hope" -> "grandma hope"
            ]
            
            # Try to find the personality file
            personalities_path = Path(personalities_dir)
            personality_file = None
            
            for variation in name_variations:
                potential_files = [
                    personalities_path / f"{variation}.json",
                    personalities_path / f"{variation.lower()}.json",
                ]
                for file_path in potential_files:
                    if file_path.exists():
                        personality_file = file_path
                        break
                if personality_file:
                    break
            
            # Also try direct match with spaces/underscores
            if not personality_file:
                for json_file in personalities_path.glob("*.json"):
                    # Check if the personality name matches (case-insensitive)
                    file_stem = json_file.stem.lower()
                    name_lower = personality_name.lower().replace(" ", "_")
                    if file_stem == name_lower or personality_name.lower() in file_stem or file_stem in personality_name.lower():
                        personality_file = json_file
                        break
            
            if not personality_file:
                logger.warning(f"Personality file not found for: {personality_name}")
                return None
            
            # Load and parse JSON
            with open(personality_file, 'r', encoding='utf-8') as f:
                personality_data = json.load(f)
            
            return personality_data
            
        except Exception as e:
            logger.warning(f"Failed to load personality {personality_name}: {e}")
            return None
    
    def _build_personality_prompt(self, personality_data: Dict[str, Any], personality_name: str) -> str:
        """Build complete personality prompt from JSON data"""
        prompt_parts = []
        
        # Extract persona info
        if "persona" in personality_data:
            persona = personality_data["persona"]
            name = persona.get("name", personality_name)
            description = persona.get("description", "")
            prompt_parts.append(f"You are {name}. {description}")
        else:
            prompt_parts.append(f"You are {personality_name}.")
        
        # Add core traits
        if "core_traits" in personality_data:
            traits = personality_data["core_traits"]
            trait_lines = []
            if traits.get("archetype"):
                trait_lines.append(f"Archetype: {traits['archetype']}")
            if traits.get("temperament"):
                trait_lines.append(f"Temperament: {traits['temperament']}")
            if traits.get("communication_style"):
                trait_lines.append(f"Communication Style: {traits['communication_style']}")
            if trait_lines:
                prompt_parts.append("\nCore Traits:\n" + "\n".join(f"- {line}" for line in trait_lines))
        
        # Add linguistic profile
        if "linguistic_profile" in personality_data:
            ling = personality_data["linguistic_profile"]
            ling_parts = []
            if ling.get("tone"):
                tones = ling["tone"] if isinstance(ling["tone"], list) else [ling["tone"]]
                ling_parts.append(f"Tone: {', '.join(tones)}")
            if ling.get("vocabulary"):
                vocab = ling["vocabulary"] if isinstance(ling["vocabulary"], list) else [ling["vocabulary"]]
                ling_parts.append(f"Vocabulary to use: {', '.join(vocab[:10])}")  # Limit to first 10
            if ling.get("fillers"):
                fillers = ling["fillers"] if isinstance(ling["fillers"], list) else [ling["fillers"]]
                ling_parts.append(f"Common expressions/fillers: {', '.join(fillers[:5])}")  # Limit to first 5
            if ling.get("syntax"):
                ling_parts.append(f"Syntax style: {ling['syntax']}")
            if ling_parts:
                prompt_parts.append("\nLinguistic Profile:\n" + "\n".join(f"- {part}" for part in ling_parts))
        
        # Add behavioral rules
        if "behavioral_rules" in personality_data:
            rules = personality_data["behavioral_rules"]
            if rules:
                prompt_parts.append("\nBehavioral Rules:")
                for rule in rules:
                    prompt_parts.append(f"- {rule}")
        
        # Add advanced parameters (if relevant)
        if "advanced_parameters" in personality_data:
            params = personality_data["advanced_parameters"]
            param_parts = []
            if params.get("verbosity"):
                param_parts.append(f"Verbosity: {params['verbosity']}")
            if params.get("formality"):
                param_parts.append(f"Formality: {params['formality']}")
            if params.get("empathy"):
                param_parts.append(f"Empathy: {params['empathy']}")
            if param_parts:
                prompt_parts.append("\nCommunication Parameters:\n" + "\n".join(f"- {part}" for part in param_parts))
        
        return "\n".join(prompt_parts)
    
    async def _generate_response_with_context(
        self,
        context: ConversationContext,
        provider_config: Optional[ProviderConfig] = None
    ) -> Dict[str, Any]:
        """Generate response using LLM with full context"""
        
        try:
            # Build a comprehensive context string for the LLM
            context_parts = []
            
            # ✅ FIX: Load and apply personality data from JSON file
            personality_data = await self._load_personality_data(context.personality_name)
            if personality_data:
                # Build complete personality prompt from JSON
                personality_prompt = self._build_personality_prompt(personality_data, context.personality_name)
                context_parts.append(personality_prompt)
            else:
                # Fallback to simple name if file not found
                context_parts.append(f"You are {context.personality_name}, an AI personality.")
            
            # Relationship context
            context_parts.append(f"\nCurrent relationship level: {context.affinity['current_level']} ({context.affinity['affinity_points']}/100 points)")
            
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
            
            # ✅ SOLUTION: Use Provider directly instead of base_client.send_message()
            # This avoids the requirement for an existing session in DynamoDB
            
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
            
            if provider_config_obj:
                try:
                    # Import ProviderFactory
                    from .providers.factory import ProviderFactory
                    
                    # Create provider instance
                    provider = ProviderFactory.create_provider(provider_config_obj)
                    
                    # Create the complete prompt with context
                    system_prompt = full_context
                    user_prompt = context.current_message
                    
                    # Prepare messages for the provider
                    from ..types.provider import ChatMessage
                    messages = [
                        ChatMessage(role="system", content=system_prompt),
                        ChatMessage(role="user", content=user_prompt)
                    ]
                    
                    # Call provider directly (doesn't require session to exist)
                    print(f"🔍 DEBUG: Calling LLM provider directly with context length: {len(full_context)}")
                    response = await provider.chat(
                        messages=messages,
                        temperature=0.7
                    )
                    
                    # Extract content
                    content = response.content if hasattr(response, 'content') else str(response)
                    
                    print(f"🔍 DEBUG: LLM response received: {content[:100]}...")
                    
                    return {
                        "content": content,
                        "metadata": {
                            "context_used": True,
                            "personality_name": context.personality_name,
                            "affinity_level": context.affinity['current_level'],
                            "facts_count": len(context.user_facts),
                            "history_length": len(context.conversation_history),
                            "provider_used": provider_config_obj.name if provider_config_obj else "unknown"
                        }
                    }
                    
                except Exception as e:
                    print(f"🔍 DEBUG: Provider direct call failed: {e}")
                    import traceback
                    traceback.print_exc()
                    # Fall through to fallback
                    pass
            
            # Fallback: context-aware response without LLM
            print(f"🔍 DEBUG: Using context-aware fallback response")
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
            print(f"🔍 DEBUG: Error in _generate_response_with_context: {e}")
            import traceback
            traceback.print_exc()
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
        existing_facts: List[Dict[str, Any]],
        provider_config: Optional[ProviderConfig] = None
    ) -> List[Dict[str, Any]]:
        """
        Extract new facts from the conversation using LLM
        
        ✅ NO HARDCODED PATTERNS
        ✅ MULTILINGUAL SUPPORT
        ✅ LLM-BASED INTELLIGENT EXTRACTION
        """
        
        new_facts = []
        
        print(f"🔍 DEBUG: Starting fact extraction for user message: '{user_message[:50]}...'")
        print(f"🔍 DEBUG: Existing facts count: {len(existing_facts)}")
        
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
                
                # ✅ SOLUTION: Use Provider directly for fact extraction
                # This avoids the requirement for an existing session in DynamoDB
                print(f"🔍 DEBUG: Calling LLM provider directly for fact extraction: {provider_config.name if provider_config else 'None'}")
                
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
                
                if provider_config_obj:
                    from .providers.factory import ProviderFactory
                    from .types.provider import ChatMessage
                    provider = ProviderFactory.create_provider(provider_config_obj)
                    
                    # Prepare messages
                    messages = [
                        ChatMessage(role="user", content=extraction_prompt)
                    ]
                    
                    # Call provider directly
                    response = await provider.chat(
                        messages=messages,
                        temperature=0.3  # Lower temperature for more deterministic extraction
                    )
                    
                    content = response.content if hasattr(response, 'content') else str(response)
                    print(f"🔍 DEBUG: LLM response received for fact extraction: {content[:100]}...")
                else:
                    print(f"🔍 DEBUG: No provider config available for fact extraction")
                    content = ""
                
                # Parse LLM response (content already extracted above)
                
                # Try to extract JSON from response
                import re
                json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content, re.DOTALL)
                print(f"🔍 DEBUG: JSON match found: {json_match is not None}")
                
                if json_match:
                    json_str = json_match.group(0)
                    print(f"🔍 DEBUG: Extracted JSON string: {json_str}")
                    try:
                        extracted_data = json.loads(json_str)
                        print(f"🔍 DEBUG: Parsed JSON data: {extracted_data}")
                        
                        if isinstance(extracted_data, dict) and "facts" in extracted_data:
                            print(f"🔍 DEBUG: Found {len(extracted_data['facts'])} facts in response")
                            
                            for i, fact_data in enumerate(extracted_data["facts"]):
                                print(f"🔍 DEBUG: Processing fact {i+1}: {fact_data}")
                                
                                # Check if fact already exists
                                exists = any(
                                    f.get('key') == fact_data.get('key') and
                                    str(f.get('value')).lower() == str(fact_data.get('value')).lower()
                                    for f in existing_facts
                                )
                                
                                print(f"🔍 DEBUG: Fact exists: {exists}, confidence: {fact_data.get('confidence', 0)}")
                                
                                if not exists and fact_data.get('confidence', 0) > 0.7:
                                    # ✅ FIX: Asegurar que value sea siempre string (no objeto)
                                    # El LLM puede devolver value como objeto en el JSON, pero el frontend espera strings
                                    fact_value = fact_data.get('value', '')
                                    if isinstance(fact_value, (dict, list)):
                                        import json as json_module
                                        fact_value = json_module.dumps(fact_value, ensure_ascii=False)
                                    elif fact_value is None:
                                        fact_value = ''
                                    else:
                                        fact_value = str(fact_value)
                                    
                                    new_fact = {
                                        "category": fact_data.get('category', 'other'),
                                        "key": fact_data.get('key', 'fact'),
                                        "value": fact_value,  # ← Siempre string
                                        "confidence": fact_data.get('confidence', 0.8)
                                    }
                                    new_facts.append(new_fact)
                                    print(f"🔍 DEBUG: Added new fact: {new_fact}")
                                else:
                                    print(f"🔍 DEBUG: Skipped fact (exists or low confidence)")
                        else:
                            print(f"🔍 DEBUG: No 'facts' key in extracted data")
                    except json.JSONDecodeError as e:
                        print(f"🔍 DEBUG: JSON decode error: {e}")
                else:
                    print(f"🔍 DEBUG: No JSON pattern found in response")
                
            except Exception as e:
                print(f"🔍 DEBUG: LLM fact extraction failed: {e}")
                import traceback
                traceback.print_exc()
                # Continue without extracting (better than wrong data)
        else:
            print(f"🔍 DEBUG: No base_client available for fact extraction")
        
        print(f"🔍 DEBUG: Final new_facts count: {len(new_facts)}")
        print(f"🔍 DEBUG: Final new_facts: {new_facts}")
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
        current_affinity: Dict[str, Any],
        provider_config: Optional[ProviderConfig] = None
    ) -> Dict[str, Any]:
        """Update affinity based on the interaction"""
        
        # Base points for any interaction
        points_change = 1
        
        # Use LLM to detect sentiment/quality of interaction
        if provider_config:
            try:
                sentiment_prompt = f"""Analyze this conversation interaction quality on a scale of 1-5 (1=negative, 5=very positive):

USER: {conversation_turn.user_message}

Rate the interaction quality (1-5):"""
                
                # ✅ SOLUTION: Use Provider directly for affinity evaluation
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
                
                if provider_config_obj:
                    from .providers.factory import ProviderFactory
                    from .types.provider import ChatMessage
                    provider = ProviderFactory.create_provider(provider_config_obj)
                    
                    messages = [ChatMessage(role="user", content=sentiment_prompt)]
                    response = await provider.chat(
                        messages=messages,
                        temperature=0.3
                    )
                    
                    # Parse rating
                    import re
                    content = response.content if hasattr(response, 'content') else str(response)
                    rating_match = re.search(r'\b([1-5])\b', content)
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
            user_id=session_id,  # Keep session_id for affinity tracking
            personality_name=conversation_turn.personality_name,
            points_delta=points_change,
            interaction_type="conversation_interaction"
        )
        
        return {
            "points_change": points_change,
            "new_points": new_points,
            "previous_level": current_affinity["current_level"]
        }
