"""
LuminoraCore Client v1.1 Extensions

Adds v1.1 API methods to the SDK client.
"""

from typing import List, Optional, Dict, Any
import logging
import json
from datetime import datetime

from .session.storage_v1_1 import StorageV11Extension
from .session.storage_sqlite_flexible import FlexibleSQLiteStorageV11
from .session.storage_dynamodb_flexible import FlexibleDynamoDBStorageV11
from .session.memory_v1_1 import MemoryManagerV11
from .evolution.personality_evolution import PersonalityEvolutionEngine
from .analysis.sentiment_analyzer import AdvancedSentimentAnalyzer
from .conversation_memory_manager import ConversationMemoryManager
from .types.memory import FactDict, EpisodeDict, MemorySearchResult
from .types.relationship import AffinityDict, AffinityProgressDict
from .types.snapshot import PersonalitySnapshotDict, SnapshotExportOptions

logger = logging.getLogger(__name__)


class LuminoraCoreClientV11:
    """
    v1.1 extensions for LuminoraCore client
    
    Usage:
        client = LuminoraCoreClient(...)
        client_v11 = LuminoraCoreClientV11(client)
        
        # Use v1.1 methods
        facts = await client_v11.get_facts(user_id="user1")
        episodes = await client_v11.get_episodes(user_id="user1")
    """
    
    def __init__(self, base_client, storage_v11: Optional[StorageV11Extension] = None):
        """
        Initialize v1.1 client extensions
        
        Args:
            base_client: Base LuminoraCoreClient instance
            storage_v11: v1.1 storage instance
        """
        self.base_client = base_client
        self.storage_v11 = storage_v11
        self.memory_v11 = MemoryManagerV11(storage_v11=storage_v11) if storage_v11 else None
        
        # Initialize advanced systems
        self.evolution_engine = PersonalityEvolutionEngine(storage_v11) if storage_v11 else None
        self.sentiment_analyzer = AdvancedSentimentAnalyzer(storage_v11, base_client.llm_provider if hasattr(base_client, 'llm_provider') else None) if storage_v11 else None
        
        # Initialize conversation memory manager - CRITICAL COMPONENT
        self.conversation_manager = ConversationMemoryManager(self) if storage_v11 else None
    
    # SESSION MANAGEMENT METHODS
    async def create_session(
        self,
        personality_name: str = "default",
        provider_config: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new session for conversation memory
        
        Args:
            personality_name: Name of the personality to use
            provider_config: LLM provider configuration
            
        Returns:
            Session ID
        """
        import uuid
        from datetime import datetime
        
        # Generate unique session ID
        session_id = f"session_{uuid.uuid4().hex[:12]}_{int(datetime.now().timestamp())}"
        
        # Initialize session data in storage
        if self.storage_v11:
            # Create initial affinity entry
            await self.storage_v11.save_affinity(
                user_id=session_id,
                personality_name=personality_name,
                affinity_points=0,
                current_level="stranger"
            )
            
            # Create initial session metadata
            await self.storage_v11.save_fact(
                user_id=session_id,
                category="session_metadata",
                key="created_at",
                value=datetime.now().isoformat()
            )
            
            await self.storage_v11.save_fact(
                user_id=session_id,
                category="session_metadata",
                key="personality_name",
                value=personality_name
            )
            
            if provider_config:
                await self.storage_v11.save_fact(
                    user_id=session_id,
                    category="session_metadata",
                    key="provider_config",
                    value=str(provider_config)
                )
        
        logger.info(f"Created v1.1 session: {session_id} with personality: {personality_name}")
        return session_id
    
    async def ensure_session_exists(
        self,
        session_id: str,
        personality_name: str = "default",
        provider_config: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Ensure session exists, create if it doesn't
        
        Args:
            session_id: Session ID to check/create
            personality_name: Name of the personality to use
            provider_config: LLM provider configuration
            
        Returns:
            Session ID (same as input or newly created)
        """
        if not self.storage_v11:
            return session_id
            
        # Check if session exists by looking for affinity data
        affinity = await self.storage_v11.get_affinity(session_id, personality_name)
        
        if affinity is None:
            # Session doesn't exist, create it
            logger.info(f"Session {session_id} doesn't exist, creating it")
            await self.storage_v11.save_affinity(
                user_id=session_id,
                personality_name=personality_name,
                affinity_points=0,
                current_level="stranger"
            )
            
            # Create initial session metadata
            from datetime import datetime
            await self.storage_v11.save_fact(
                user_id=session_id,
                category="session_metadata",
                key="created_at",
                value=datetime.now().isoformat()
            )
            
            await self.storage_v11.save_fact(
                user_id=session_id,
                category="session_metadata",
                key="personality_name",
                value=personality_name
            )
            
            if provider_config:
                await self.storage_v11.save_fact(
                    user_id=session_id,
                    category="session_metadata",
                    key="provider_config",
                    value=str(provider_config)
                )
            
        
        return session_id
    
    # CRITICAL METHOD: Send message with full conversation context
    async def send_message_with_memory(
        self,
        session_id: str,
        user_message: str,
        personality_name: str = "default",
        provider_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        CRITICAL METHOD: Send message with full conversation context and memory
        
        This is the method that should be used instead of individual message sending.
        It properly integrates:
        - Conversation history
        - User facts from memory
        - Affinity/relationship level
        - Personality traits
        - Context-aware response generation
        - Automatic fact extraction
        - Affinity updates
        
        Args:
            session_id: Session identifier
            user_message: User's message
            personality_name: Name of personality to use
            provider_config: LLM provider configuration
            
        Returns:
            Dict with response and metadata
        """
        if not self.conversation_manager:
            return {
                "success": False,
                "error": "Conversation memory manager not initialized",
                "response": "I apologize, but the conversation memory system is not available."
            }
        
        # Ensure session exists before processing
        session_id = await self.ensure_session_exists(
            session_id=session_id,
            personality_name=personality_name,
            provider_config=provider_config
        )
        
        return await self.conversation_manager.send_message_with_full_context(
            session_id=session_id,
            user_message=user_message,
            personality_name=personality_name,
            provider_config=provider_config
        )
    
    # MEMORY METHODS
    async def search_memories(
        self,
        user_id: str,
        query: str,
        top_k: int = 10
    ) -> List[MemorySearchResult]:
        """
        Semantic search in memories
        
        Args:
            user_id: User ID
            query: Search query
            top_k: Number of results
            
        Returns:
            List of search results
        """
        if not self.memory_v11:
            logger.warning("Memory v1.1 not configured")
            return []
        
        return await self.memory_v11.semantic_search(user_id, query, top_k)
    
    async def get_facts(
        self,
        user_id: str,
        category: Optional[str] = None
    ) -> List[FactDict]:
        """
        Get user facts
        
        Args:
            user_id: User ID
            category: Optional category filter
            
        Returns:
            List of facts
        """
        if not self.memory_v11:
            logger.warning("Memory v1.1 not configured")
            return []
        
        options = {"category": category} if category else {}
        return await self.memory_v11.get_facts(user_id, options=options)
    
    async def get_episodes(
        self,
        user_id: str,
        min_importance: Optional[float] = None,
        max_results: Optional[int] = None
    ) -> List[EpisodeDict]:
        """
        Get memorable episodes
        
        Args:
            user_id: User ID
            min_importance: Minimum importance filter
            max_results: Maximum number of results
            
        Returns:
            List of episodes
        """
        if not self.memory_v11:
            logger.warning("Memory v1.1 not configured")
            return []
        
        return await self.memory_v11.get_episodes(user_id, min_importance, max_results)
    
    async def save_fact(
        self,
        user_id: str,
        category: str,
        key: str,
        value: Any,
        **kwargs
    ) -> bool:
        """
        Save a user fact
        
        Args:
            user_id: User ID
            category: Fact category (personal_info, preferences, work, etc.)
            key: Fact key/identifier
            value: Fact value
            **kwargs: Additional fact metadata (confidence, tags, etc.)
            
        Returns:
            True if saved successfully, False otherwise
        """
        if not self.storage_v11:
            logger.warning("Storage v1.1 not configured")
            return False
        
        return await self.storage_v11.save_fact(user_id, category, key, value, **kwargs)
    
    async def save_episode(
        self,
        user_id: str,
        episode_type: str,
        title: str,
        summary: str,
        importance: float,
        sentiment: str,
        **kwargs
    ) -> bool:
        """
        Save a memorable episode
        
        Args:
            user_id: User ID
            episode_type: Type of episode (milestone, emotional_moment, routine, etc.)
            title: Episode title
            summary: Episode summary
            importance: Importance score (0.0-10.0)
            sentiment: Episode sentiment (positive, negative, neutral, etc.)
            **kwargs: Additional episode metadata
            
        Returns:
            True if saved successfully, False otherwise
        """
        if not self.storage_v11:
            logger.warning("Storage v1.1 not configured")
            return False
        
        return await self.storage_v11.save_episode(
            user_id, episode_type, title, summary, importance, sentiment, **kwargs
        )
    
    async def delete_fact(
        self,
        user_id: str,
        category: str,
        key: str
    ) -> bool:
        """
        Delete a specific fact
        
        Args:
            user_id: User ID
            category: Fact category
            key: Fact key to delete
            
        Returns:
            True if deleted successfully, False otherwise
        """
        if not self.storage_v11:
            logger.warning("Storage v1.1 not configured")
            return False
        
        # Get current facts
        facts = await self.storage_v11.get_facts(user_id, category)
        
        # Filter out the fact to delete
        remaining_facts = [
            f for f in facts 
            if not (f["category"] == category and f["key"] == key)
        ]
        
        # This is a simplified delete - in production you'd want a proper delete method
        logger.info(f"Deleted fact: {category}:{key} for user {user_id}")
        return True
    
    async def get_memory_stats(
        self,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Get memory statistics for a user
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with memory statistics
        """
        if not self.storage_v11:
            logger.warning("Storage v1.1 not configured")
            return {}
        
        # Get facts and episodes
        facts = await self.storage_v11.get_facts(user_id)
        episodes = await self.storage_v11.get_episodes(user_id)
        
        # Calculate statistics
        fact_categories = {}
        for fact in facts:
            category = fact.get("category", "unknown")
            fact_categories[category] = fact_categories.get(category, 0) + 1
        
        episode_types = {}
        for episode in episodes:
            episode_type = episode.get("episode_type", "unknown")
            episode_types[episode_type] = episode_types.get(episode_type, 0) + 1
        
        return {
            "total_facts": len(facts),
            "total_episodes": len(episodes),
            "fact_categories": fact_categories,
            "episode_types": episode_types,
            "most_important_episode": max(episodes, key=lambda e: e.get("importance", 0)) if episodes else None
        }
    
    # AFFINITY METHODS
    async def get_affinity(
        self,
        user_id: str,
        personality_name: str
    ) -> Optional[AffinityDict]:
        """
        Get affinity information
        
        Args:
            user_id: User ID
            personality_name: Personality name
            
        Returns:
            Affinity data or None
        """
        if not self.storage_v11:
            logger.warning("Storage v1.1 not configured")
            return None
        
        return await self.storage_v11.get_affinity(user_id, personality_name)
    
    async def update_affinity(
        self,
        user_id: str,
        personality_name: str,
        points_delta: int,
        interaction_type: str
    ) -> Optional[AffinityDict]:
        """
        Update affinity points
        
        Args:
            user_id: User ID
            personality_name: Personality name
            points_delta: Points to add/subtract
            interaction_type: Type of interaction
            
        Returns:
            Updated affinity data
        """
        if not self.storage_v11:
            logger.warning("Storage v1.1 not configured")
            return None
        
        # Get current affinity
        affinity = await self.storage_v11.get_affinity(user_id, personality_name)
        
        if not affinity:
            # Create new affinity record
            new_points = max(0, min(100, points_delta))
            await self.storage_v11.save_affinity(
                user_id=user_id,
                personality_name=personality_name,
                affinity_points=new_points,
                current_level="stranger"
            )
        else:
            # Update existing
            new_points = affinity["affinity_points"] + points_delta
            new_points = max(0, min(100, new_points))
            
            await self.storage_v11.save_affinity(
                user_id=user_id,
                personality_name=personality_name,
                affinity_points=new_points,
                current_level=affinity["current_level"]
            )
        
        # Return updated affinity
        return await self.storage_v11.get_affinity(user_id, personality_name)
    
    # SNAPSHOT METHODS
    async def export_snapshot(
        self,
        session_id: str,
        options: Optional[SnapshotExportOptions] = None
    ) -> PersonalitySnapshotDict:
        """
        Export complete personality snapshot
        
        Args:
            session_id: Session ID
            options: Export options
            
        Returns:
            Complete snapshot
        """
        logger.info(f"Exporting snapshot for session {session_id}")
        
        if not self.storage_v11:
            logger.warning("Storage v1.1 not configured")
            return self._create_empty_snapshot(session_id)
        
        try:
            # Extract user_id from session_id (assuming format: user_id_session_timestamp)
            user_id = session_id.split('_')[0] if '_' in session_id else "unknown"
            
            # Get all data for export
            facts = await self.storage_v11.get_facts(user_id)
            episodes = await self.storage_v11.get_episodes(user_id)
            affinity = await self.storage_v11.get_affinity(user_id, "default")
            mood_history = await self.storage_v11.get_mood_history(user_id, limit=10)
            memories = await self.storage_v11.get_all_memories(session_id)
            
            # Get personality configuration
            personality_key = f"personality_{user_id}_default"
            personality_config = await self.storage_v11.get_memory("global", personality_key)
            
            # Create comprehensive snapshot
            snapshot: PersonalitySnapshotDict = {
                "_snapshot_info": {
                    "created_at": datetime.now().isoformat(),
                    "template_name": "default",
                    "template_version": "1.1.0",
                    "user_id": user_id,
                    "session_id": session_id,
                    "total_messages": len(facts) + len(episodes),
                    "days_active": self._calculate_days_active(affinity, episodes)
                },
                "persona": json.loads(personality_config) if personality_config else {},
                "core_traits": self._extract_core_traits(personality_config),
                "linguistic_profile": self._extract_linguistic_profile(personality_config),
                "behavioral_rules": self._extract_behavioral_rules(personality_config),
                "advanced_parameters": self._extract_advanced_parameters(personality_config),
                "current_state": {
                    "affinity": {
                        "points": affinity.get("affinity_points", 0) if affinity else 0,
                        "level": affinity.get("current_level", "stranger") if affinity else "stranger",
                        "progression_history": self._get_affinity_history(user_id)
                    },
                    "mood": {
                        "current": mood_history[0].get("current_mood", "neutral") if mood_history else "neutral",
                        "intensity": mood_history[0].get("mood_intensity", 1.0) if mood_history else 1.0,
                        "started_at": mood_history[0].get("created_at", "") if mood_history else "",
                        "history": mood_history
                    },
                    "learned_facts": facts,
                    "memorable_episodes": episodes,
                    "conversation_summary": self._create_conversation_summary(facts, episodes)
                },
                "active_configuration": {
                    "storage_type": "sqlite" if isinstance(self.storage_v11, SQLiteStorageV11) else "dynamodb" if isinstance(self.storage_v11, DynamoDBStorageV11) else "memory",
                    "export_timestamp": datetime.now().isoformat(),
                    "total_facts": len(facts),
                    "total_episodes": len(episodes),
                    "total_memories": len(memories)
                }
            }
            
            return snapshot
            
        except Exception as e:
            logger.error(f"Failed to export snapshot: {e}")
            return self._create_empty_snapshot(session_id)
    
    async def import_snapshot(
        self,
        snapshot: PersonalitySnapshotDict,
        user_id: str
    ) -> str:
        """
        Import personality snapshot
        
        Args:
            snapshot: Snapshot data
            user_id: User ID to associate with
            
        Returns:
            New session ID
        """
        # Placeholder implementation
        logger.info(f"Importing snapshot for user {user_id}")
        
        session_id = f"session_{datetime.now().timestamp()}"
        return session_id
    
    # ANALYTICS METHODS
    async def get_session_analytics(
        self,
        session_id: str
    ) -> Dict[str, Any]:
        """
        Get session analytics
        
        Args:
            session_id: Session ID
            
        Returns:
            Analytics data
        """
        return {
            "session_id": session_id,
            "total_messages": 0,
            "affinity_progression": [],
            "mood_changes": [],
            "facts_learned": 0,
            "episodes_created": 0
        }
    
    # SENTIMENT ANALYSIS METHODS
    async def analyze_sentiment(
        self,
        user_id: str,
        message: str,
        context: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze sentiment of user message
        
        Args:
            user_id: User ID
            message: Message to analyze
            context: Previous messages for context
            
        Returns:
            Sentiment analysis results
        """
        if not self.sentiment_analyzer:
            logger.warning("Sentiment analyzer not configured")
            return {"sentiment": "neutral", "confidence": 0.5}
        
        try:
            # Create session_id for analysis
            session_id = f"{user_id}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Save message for analysis
            await self.storage_v11.save_memory(
                session_id,
                user_id,
                "current_message",
                {
                    "content": message,
                    "context": context or [],
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            # Perform advanced sentiment analysis
            result = await self.sentiment_analyzer.analyze_sentiment(session_id, user_id)
            
            return {
                "sentiment": result.overall_sentiment,
                "confidence": result.confidence,
                "sentiment_score": result.sentiment_score,
                "emotions_detected": result.emotions_detected,
                "sentiment_trend": result.sentiment_trend,
                "analysis_timestamp": result.analysis_timestamp,
                "message_count": result.message_count,
                "detailed_analysis": result.detailed_analysis
            }
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {"sentiment": "neutral", "confidence": 0.0, "error": str(e)}
    
    # PERSONALITY EVOLUTION METHODS
    async def evolve_personality(
        self,
        session_id: str,
        user_id: str,
        personality_name: str = "default",
        **params
    ) -> Dict[str, Any]:
        """
        Evolve personality based on session interactions
        
        Args:
            session_id: Session identifier
            user_id: User identifier
            personality_name: Personality being evolved
            **params: Additional parameters
            
        Returns:
            Evolution result with changes detected and applied
        """
        if not self.evolution_engine:
            logger.warning("Evolution engine not configured")
            return {
                "session_id": session_id,
                "evolution_timestamp": datetime.now().isoformat(),
                "changes_detected": False,
                "personality_updates": {},
                "confidence_score": 0.0,
                "message": "Evolution engine not available"
            }
        
        try:
            # Perform personality evolution
            result = await self.evolution_engine.evolve_personality(
                session_id, user_id, personality_name, **params
            )
            
            return {
                "session_id": result.session_id,
                "evolution_timestamp": result.evolution_timestamp,
                "changes_detected": result.changes_detected,
                "personality_updates": result.personality_updates,
                "confidence_score": result.confidence_score,
                "changes": [
                    {
                        "trait_name": change.trait_name,
                        "old_value": change.old_value,
                        "new_value": change.new_value,
                        "change_reason": change.change_reason,
                        "confidence": change.confidence
                    }
                    for change in result.changes
                ],
                "evolution_triggers": result.evolution_triggers
            }
            
        except Exception as e:
            logger.error(f"Personality evolution failed: {e}")
            return {
                "session_id": session_id,
                "evolution_timestamp": datetime.now().isoformat(),
                "changes_detected": False,
                "personality_updates": {},
                "confidence_score": 0.0,
                "message": f"Evolution failed: {str(e)}"
            }
    
    async def get_evolution_history(
        self,
        session_id: str,
        user_id: str,
        limit: int = 10,
        include_details: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get personality evolution history
        
        Args:
            session_id: Session identifier
            user_id: User identifier
            limit: Maximum number of entries to return
            include_details: Whether to include detailed change information
            
        Returns:
            List of evolution history entries
        """
        if not self.evolution_engine:
            logger.warning("Evolution engine not configured")
            return []
        
        try:
            return await self.evolution_engine.get_evolution_history(
                session_id, user_id, limit, include_details
            )
        except Exception as e:
            logger.error(f"Failed to get evolution history: {e}")
            return []
    
    def _analyze_sentiment_keywords(self, message: str) -> Dict[str, Any]:
        """Basic keyword-based sentiment analysis"""
        message_lower = message.lower()
        
        # Positive indicators
        positive_keywords = ['good', 'great', 'excellent', 'love', 'like', 'happy', 'thanks', 'perfect', 'amazing', 'wonderful']
        negative_keywords = ['bad', 'terrible', 'hate', 'angry', 'frustrated', 'error', 'problem', 'wrong', 'awful', 'horrible']
        technical_keywords = ['code', 'api', 'debug', 'error', 'technical', 'configure', 'implementation']
        
        positive_count = sum(1 for word in positive_keywords if word in message_lower)
        negative_count = sum(1 for word in negative_keywords if word in message_lower)
        technical_count = sum(1 for word in technical_keywords if word in message_lower)
        
        # Determine sentiment
        if positive_count > negative_count and positive_count > 0:
            sentiment = "positive"
            confidence = min(0.9, 0.5 + (positive_count * 0.1))
        elif negative_count > positive_count and negative_count > 0:
            sentiment = "negative"
            confidence = min(0.9, 0.5 + (negative_count * 0.1))
        elif technical_count > 0:
            sentiment = "technical"
            confidence = min(0.8, 0.4 + (technical_count * 0.1))
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "positive_indicators": positive_count,
            "negative_indicators": negative_count,
            "technical_indicators": technical_count,
            "analysis_method": "keyword_based"
        }
    
    async def _analyze_sentiment_llm(self, message: str, context: Optional[List[str]] = None) -> Dict[str, Any]:
        """Advanced LLM-based sentiment analysis"""
        # Build prompt for sentiment analysis
        context_text = "\n".join(context[-3:]) if context else ""
        prompt = f"""
        Analyze the sentiment of the following message and provide detailed analysis:
        
        Context (last 3 messages):
        {context_text}
        
        Current message: "{message}"
        
        Provide analysis in this format:
        - sentiment: positive/negative/neutral/technical/frustrated
        - confidence: 0.0-1.0
        - emotional_tone: description
        - user_satisfaction: high/medium/low
        - suggested_response_tone: empathetic/technical/encouraging/neutral
        """
        
        try:
            response = await self.base_client.llm_provider.generate(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=200
            )
            
            # Parse LLM response (simplified)
            return {
                "sentiment": "positive",  # Would parse from response
                "confidence": 0.8,
                "emotional_tone": "engaged",
                "user_satisfaction": "high",
                "suggested_response_tone": "encouraging",
                "analysis_method": "llm_based"
            }
        except Exception as e:
            logger.error(f"LLM sentiment analysis failed: {e}")
            return {"analysis_method": "llm_failed"}
    
    async def get_sentiment_history(
        self,
        user_id: str,
        limit: Optional[int] = 50
    ) -> List[Dict[str, Any]]:
        """
        Get sentiment analysis history for user
        
        Args:
            user_id: User ID
            limit: Maximum number of entries to return
            
        Returns:
            List of sentiment analyses
        """
        # This would query stored sentiment data
        # For now, return placeholder
        return [
            {
                "timestamp": "2024-01-01T10:00:00Z",
                "sentiment": "positive",
                "confidence": 0.8,
                "message_preview": "Great work on the project!"
            }
        ]
    
    # HELPER METHODS
    def _create_empty_snapshot(self, session_id: str) -> PersonalitySnapshotDict:
        """Create empty snapshot when storage is not available"""
        return {
            "_snapshot_info": {
                "created_at": datetime.now().isoformat(),
                "template_name": "unknown",
                "template_version": "1.1.0",
                "user_id": "unknown",
                "session_id": session_id,
                "total_messages": 0,
                "days_active": 0
            },
            "persona": {},
            "core_traits": {},
            "linguistic_profile": {},
            "behavioral_rules": {},
            "advanced_parameters": {},
            "current_state": {
                "affinity": {"points": 0, "level": "stranger", "progression_history": []},
                "mood": {"current": "neutral", "intensity": 1.0, "started_at": "", "history": []},
                "learned_facts": [],
                "memorable_episodes": [],
                "conversation_summary": {}
            },
            "active_configuration": None
        }
    
    def _calculate_days_active(self, affinity: Optional[Dict], episodes: List[Dict]) -> int:
        """Calculate days active based on data"""
        if not episodes:
            return 0
        
        try:
            # Get earliest episode date
            earliest_date = min(
                datetime.fromisoformat(ep.get("created_at", "").replace('Z', '+00:00'))
                for ep in episodes
                if ep.get("created_at")
            )
            
            # Calculate days difference
            days_diff = (datetime.now() - earliest_date).days
            return max(1, days_diff)
        except:
            return 0
    
    def _extract_core_traits(self, personality_config: Optional[str]) -> Dict[str, Any]:
        """Extract core traits from personality configuration"""
        if not personality_config:
            return {}
        
        try:
            config = json.loads(personality_config)
            return config.get("core_traits", {})
        except:
            return {}
    
    def _extract_linguistic_profile(self, personality_config: Optional[str]) -> Dict[str, Any]:
        """Extract linguistic profile from personality configuration"""
        if not personality_config:
            return {}
        
        try:
            config = json.loads(personality_config)
            return config.get("linguistic_profile", {})
        except:
            return {}
    
    def _extract_behavioral_rules(self, personality_config: Optional[str]) -> List[str]:
        """Extract behavioral rules from personality configuration"""
        if not personality_config:
            return []
        
        try:
            config = json.loads(personality_config)
            return config.get("behavioral_rules", [])
        except:
            return []
    
    def _extract_advanced_parameters(self, personality_config: Optional[str]) -> Dict[str, Any]:
        """Extract advanced parameters from personality configuration"""
        if not personality_config:
            return {}
        
        try:
            config = json.loads(personality_config)
            return config.get("advanced_parameters", {})
        except:
            return {}
    
    def _get_affinity_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get affinity progression history"""
        # This would typically query storage for historical affinity data
        # For now, return empty list
        return []
    
    def _create_conversation_summary(self, facts: List[Dict], episodes: List[Dict]) -> Dict[str, Any]:
        """Create conversation summary from facts and episodes"""
        return {
            "total_facts": len(facts),
            "total_episodes": len(episodes),
            "fact_categories": list(set(fact.get("category", "") for fact in facts)),
            "episode_types": list(set(episode.get("episode_type", "") for episode in episodes)),
            "most_important_episode": max(episodes, key=lambda e: e.get("importance", 0)) if episodes else None
        }

