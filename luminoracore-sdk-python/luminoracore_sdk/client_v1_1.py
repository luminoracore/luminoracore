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
        user_id: str = "demo",
        personality_name: str = "default",
        provider_config: Optional[Dict[str, Any]] = None,
        session_config: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new session for conversation memory with proper user management
        
        Args:
            user_id: User ID (persistent across sessions) - defaults to "demo"
            personality_name: Name of the personality to use
            provider_config: LLM provider configuration
            session_config: Session configuration (ttl, max_idle, etc.)
            
        Returns:
            Session ID
        """
        import uuid
        from datetime import datetime, timedelta
        
        # Default session configuration
        config = session_config or {}
        ttl = config.get("ttl", 3600)  # 1 hour default
        max_idle = config.get("max_idle", 1800)  # 30 minutes default
        
        # Generate unique session ID
        session_id = f"session_{uuid.uuid4().hex[:12]}_{int(datetime.now().timestamp())}"
        
        # Calculate expiration times
        created_at = datetime.now()
        expires_at = created_at + timedelta(seconds=ttl)
        last_activity = created_at
        
        # Initialize session data in storage
        if self.storage_v11:
            # Ensure user exists (create if not exists)
            await self.ensure_user_exists(user_id, personality_name)
            
            # Create session entry
            await self.storage_v11.save_session(
                session_id=session_id,
                user_id=user_id,
                personality_name=personality_name,
                created_at=created_at.isoformat(),
                expires_at=expires_at.isoformat(),
                last_activity=last_activity.isoformat(),
                status="active",
                provider_config=provider_config
            )
            
            # Create initial session metadata
            await self.storage_v11.save_fact(
                user_id=user_id,
                category="session_metadata",
                key=f"session_{session_id}",
                value={
                    "session_id": session_id,
                    "personality_name": personality_name,
                    "created_at": created_at.isoformat(),
                    "expires_at": expires_at.isoformat(),
                    "provider_config": provider_config
                }
            )
        
        logger.info(f"Created v1.1 session: {session_id} for user: {user_id} with personality: {personality_name}")
        return session_id
    
    async def ensure_user_exists(
        self,
        user_id: str,
        personality_name: str = "default"
    ) -> bool:
        """
        Ensure user exists in storage, create if not exists
        
        Args:
            user_id: User ID to check/create
            personality_name: Personality name for affinity
            
        Returns:
            True if user exists or was created
        """
        if not self.storage_v11:
            return True
            
        # Check if user exists by looking for affinity data
        affinity = await self.storage_v11.get_affinity(user_id, personality_name)
        
        if affinity is None:
            # User doesn't exist, create it
            logger.info(f"User {user_id} doesn't exist, creating it")
            await self.storage_v11.save_affinity(
                user_id=user_id,
                personality_name=personality_name,
                affinity_points=0,
                current_level="stranger",
                total_interactions=0,
                positive_interactions=0,
                created_at=datetime.now().isoformat(),
                last_interaction=datetime.now().isoformat()
            )
            
            # Create initial user metadata
            await self.storage_v11.save_fact(
                user_id=user_id,
                category="user_metadata",
                key="created_at",
                value=datetime.now().isoformat()
            )
            
            await self.storage_v11.save_fact(
                user_id=user_id,
                category="user_metadata",
                key="default_personality",
                value=personality_name
            )
        
        return True
    
    async def ensure_session_exists(
        self,
        session_id: str,
        user_id: str = "demo",
        personality_name: str = "default",
        provider_config: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Ensure session exists, create if it doesn't
        
        Args:
            session_id: Session ID to check/create
            user_id: User ID (persistent across sessions)
            personality_name: Name of the personality to use
            provider_config: LLM provider configuration
            
        Returns:
            Session ID (same as input or newly created)
        """
        if not self.storage_v11:
            return session_id
            
        # Check if session exists
        session_exists = await self.storage_v11.get_session(session_id)
        
        if session_exists is None:
            # Session doesn't exist, create it
            logger.info(f"Session {session_id} doesn't exist, creating it for user {user_id}")
            
            # Ensure user exists first
            await self.ensure_user_exists(user_id, personality_name)
            
            # Create session entry
            from datetime import datetime, timedelta
            created_at = datetime.now()
            expires_at = created_at + timedelta(seconds=3600)  # 1 hour default
            
            await self.storage_v11.save_session(
                session_id=session_id,
                user_id=user_id,
                personality_name=personality_name,
                created_at=created_at.isoformat(),
                expires_at=expires_at.isoformat(),
                last_activity=created_at.isoformat(),
                status="active",
                provider_config=provider_config
            )
            
            # Create initial session metadata
            await self.storage_v11.save_fact(
                user_id=user_id,
                category="session_metadata",
                key=f"session_{session_id}",
                value={
                    "session_id": session_id,
                    "personality_name": personality_name,
                    "created_at": created_at.isoformat(),
                    "expires_at": expires_at.isoformat(),
                    "provider_config": provider_config
                }
            )
        
        return session_id
    
    # CRITICAL METHOD: Send message with full conversation context
    async def send_message_with_memory(
        self,
        session_id: str,
        user_message: str,
        user_id: Optional[str] = None,
        personality_name: str = "default",
        provider_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        CRITICAL METHOD: Send message with full conversation context and memory
        
        Args:
            session_id: Session ID for the conversation
            user_message: User's message
            user_id: User ID (persistent across sessions) - defaults to "demo"
            personality_name: Name of the personality to use
            provider_config: LLM provider configuration
        
        Returns:
            Response with full context and memory integration
        
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
        
        # CRITICAL FIX: Use session_id as user_id if not provided
        # This ensures memory contextual works correctly
        if user_id is None:
            user_id = session_id
            logger.info(f"Using session_id as user_id: {user_id}")
        
        # Ensure session exists before processing
        session_id = await self.ensure_session_exists(
            session_id=session_id,
            user_id=user_id,
            personality_name=personality_name,
            provider_config=provider_config
        )
        
        return await self.conversation_manager.send_message_with_full_context(
            session_id=session_id,
            user_message=user_message,
            user_id=user_id,  # Pass user_id to conversation manager
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
        
        # Use the storage's delete_fact method
        return await self.storage_v11.delete_fact(user_id, category, key)
    
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
            new_level = self._calculate_affinity_level(new_points)
            await self.storage_v11.save_affinity(
                user_id=user_id,
                personality_name=personality_name,
                affinity_points=new_points,
                current_level=new_level
            )
        else:
            # Update existing
            new_points = affinity["affinity_points"] + points_delta
            new_points = max(0, min(100, new_points))
            new_level = self._calculate_affinity_level(new_points)
            
            await self.storage_v11.save_affinity(
                user_id=user_id,
                personality_name=personality_name,
                affinity_points=new_points,
                current_level=new_level
            )
        
        # Return updated affinity
        return await self.storage_v11.get_affinity(user_id, personality_name)
    
    def _calculate_affinity_level(self, points: int) -> str:
        """Calculate affinity level based on points"""
        if points >= 50:
            return "friend"
        elif points >= 25:
            return "acquaintance"
        else:
            return "stranger"
    
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
        message: Optional[str] = None,
        context: Optional[List[str]] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze sentiment of user message or entire session
        
        Args:
            user_id: User ID
            message: Optional message to analyze. If None and session_id provided, analyzes entire session
            context: Previous messages for context (only used if message is provided)
            session_id: Optional session ID. If provided and message is None, analyzes entire session conversations
            
        Returns:
            Sentiment analysis results with:
            - sentiment: "positive" | "neutral" | "negative"
            - sentiment_score: float (0.0 - 1.0)
            - confidence: float (0.0 - 1.0)
            - emotions_detected: List[str]
            - sentiment_trend: str
            - analysis_timestamp: str
            - message_count: int
            - detailed_analysis: dict
        """
        if not self.sentiment_analyzer:
            logger.warning("Sentiment analyzer not configured")
            return {"sentiment": "neutral", "confidence": 0.5, "error": "Sentiment analyzer not configured"}
        
        try:
            # MODE 1: Analyze entire session (if session_id provided and message is None/empty)
            if session_id and not message:
                logger.info(f"Analyzing entire session: {session_id}")
                
                # Use the original session_id to find conversations
                # Conversations are stored with: get_facts(user_id=session_id, category="conversation_history")
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
            
            # MODE 2: Analyze specific message
            elif message:
                logger.info(f"Analyzing specific message for user: {user_id}")
                
                # Create temporary session_id for single message analysis
                temp_session_id = f"{user_id}_message_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                # Convert message and context to conversation format for analysis
                conversation_data = [{
                    "content": message,
                    "type": "user",
                    "timestamp": datetime.now().isoformat()
                }]
                
                if context:
                    for ctx_msg in context[-3:]:  # Last 3 context messages
                        conversation_data.insert(0, {
                            "content": ctx_msg,
                            "type": "context",
                            "timestamp": datetime.now().isoformat()
                        })
                
                # Perform analysis using the conversation data directly
                # Use a helper method that can analyze conversation data directly
                basic_analysis = self.sentiment_analyzer._perform_basic_analysis(conversation_data)
                advanced_analysis = await self.sentiment_analyzer._perform_advanced_analysis(conversation_data)
                emotion_analysis = self.sentiment_analyzer._perform_emotion_analysis(conversation_data)
                
                # Combine analyses
                combined_result = self.sentiment_analyzer._combine_analyses(
                    basic_analysis, advanced_analysis, emotion_analysis, {}
                )
                
                return {
                    "sentiment": combined_result["overall_sentiment"],
                    "confidence": combined_result["confidence"],
                    "sentiment_score": combined_result["sentiment_score"],
                    "emotions_detected": combined_result["emotions_detected"],
                    "sentiment_trend": "stable",  # No trend for single message
                    "analysis_timestamp": datetime.now().isoformat(),
                    "message_count": len(conversation_data),
                    "detailed_analysis": combined_result["detailed_analysis"]
                }
            
            else:
                return {"sentiment": "neutral", "confidence": 0.0, "error": "Either message or session_id must be provided"}
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}", exc_info=True)
            return {"sentiment": "neutral", "confidence": 0.0, "error": str(e)}
    
    # EXPORT METHODS
    async def export_conversation(
        self,
        session_id: str,
        format: str = "json",
        include_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        Export conversation data
        
        Args:
            session_id: Session ID to export
            format: Export format ("json", "csv", "markdown", "pdf")
            include_metadata: Include session metadata
            
        Returns:
            Exported conversation data
        """
        try:
            # Get session information
            session_data = await self.storage_v11.get_session(session_id) if self.storage_v11 else None
            
            # Get conversation history
            conversation_history = await self._get_conversation_history(session_id)
            
            # Get user facts if session exists (excluir conversation_history)
            # ✅ FIX: No incluir conversation_history en facts del usuario para export
            user_facts = []
            if session_data:
                user_id = session_data.get("user_id", "unknown")
                all_user_facts = await self.get_facts(user_id)
                # Filtrar conversation_history de user_facts (los turns no son facts del usuario)
                user_facts = [f for f in all_user_facts if f.get('category') != 'conversation_history']
            
            export_data = {
                "session_id": session_id,
                "conversation_history": conversation_history,
                "export_timestamp": datetime.now().isoformat(),
                "format": format
            }
            
            if include_metadata and session_data:
                export_data["metadata"] = session_data
            
            if user_facts:
                export_data["user_facts"] = user_facts
            
            return {
                "success": True,
                "data": export_data,
                "format": format
            }
            
        except Exception as e:
            logger.error(f"Error exporting conversation: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def export_user_conversations(
        self,
        user_id: str,
        format: str = "json",
        date_range: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Export all conversations for a user
        
        Args:
            user_id: User ID to export
            format: Export format
            date_range: Optional date range filter
            
        Returns:
            All user conversations
        """
        try:
            # Get all user facts (excluir conversation_history)
            # ✅ FIX: No incluir conversation_history en facts del usuario
            all_user_facts = await self.get_facts(user_id)
            user_facts = [f for f in all_user_facts if f.get('category') != 'conversation_history']
            
            # Get user affinity data
            affinity_data = {}
            personalities = ["default", "alicia", "dr_luna", "assistant"]  # Common personalities
            for personality in personalities:
                affinity = await self.get_affinity(user_id, personality)
                if affinity:
                    affinity_data[personality] = affinity
            
            # Get sentiment history
            sentiment_history = await self.get_sentiment_history(user_id, limit=100)
            
            export_data = {
                "user_id": user_id,
                "export_timestamp": datetime.now().isoformat(),
                "format": format,
                "user_facts": user_facts,
                "affinity_data": affinity_data,
                "sentiment_history": sentiment_history
            }
            
            if date_range:
                export_data["date_range"] = date_range
            
            return {
                "success": True,
                "data": export_data,
                "format": format
            }
            
        except Exception as e:
            logger.error(f"Error exporting user conversations: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def export_complete_user_data(
        self,
        user_id: str,
        include_facts: bool = True,
        include_episodes: bool = True,
        include_sentiment_history: bool = True,
        include_personality_evolution: bool = True
    ) -> Dict[str, Any]:
        """
        Export complete user data
        
        Args:
            user_id: User ID to export
            include_facts: Include user facts
            include_episodes: Include episodes
            include_sentiment_history: Include sentiment history
            include_personality_evolution: Include personality evolution
            
        Returns:
            Complete user data
        """
        try:
            export_data = {
                "user_id": user_id,
                "export_timestamp": datetime.now().isoformat(),
                "export_type": "complete_user_data"
            }
            
            if include_facts:
                export_data["facts"] = await self.get_facts(user_id)
            
            if include_episodes:
                export_data["episodes"] = await self.get_episodes(user_id)
            
            if include_sentiment_history:
                export_data["sentiment_history"] = await self.get_sentiment_history(user_id, limit=100)
            
            if include_personality_evolution:
                # Get evolution for common personalities
                personalities = ["default", "alicia", "dr_luna", "assistant"]
                evolution_data = {}
                for personality in personalities:
                    try:
                        evolution = await self.get_evolution_history(user_id, personality)
                        if evolution:
                            evolution_data[personality] = evolution
                    except:
                        pass
                export_data["personality_evolution"] = evolution_data
            
            # Get affinity data
            affinity_data = {}
            for personality in ["default", "alicia", "dr_luna", "assistant"]:
                affinity = await self.get_affinity(user_id, personality)
                if affinity:
                    affinity_data[personality] = affinity
            export_data["affinity_data"] = affinity_data
            
            return {
                "success": True,
                "data": export_data
            }
            
        except Exception as e:
            logger.error(f"Error exporting complete user data: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
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
    
    # ✅ REMOVED: _analyze_sentiment_keywords() method with hardcoded English keywords
    # Now using LLM-based analysis exclusively (multilingual, no hardcodes)

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
            # ✅ FIX: Use .chat() with ChatMessage (not .generate())
            from .types.provider import ChatMessage
            
            # Check if llm_provider exists
            if not hasattr(self.base_client, 'llm_provider') or not self.base_client.llm_provider:
                logger.warning("LLM provider not available for sentiment analysis")
                return {"analysis_method": "llm_not_available"}
            
            messages = [
                ChatMessage(role="user", content=prompt)
            ]
            
            response = await self.base_client.llm_provider.chat(
                messages=messages,
                temperature=0.1,
                max_tokens=200
            )
            
            # Parse LLM response (simplified - would need full parsing in production)
            content = response.content if hasattr(response, 'content') else str(response)
            return {
                "sentiment": "positive",  # Would parse from content
                "confidence": 0.8,
                "emotional_tone": "engaged",
                "user_satisfaction": "high",
                "suggested_response_tone": "encouraging",
                "analysis_method": "llm_based",
                "raw_response": content[:200]  # For debugging
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
    
    # SENTIMENT ANALYSIS METHODS
    
    async def save_mood(
        self,
        user_id: str,
        personality_name: str,
        mood: str,
        intensity: float,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Save user mood data"""
        try:
            mood_data = {
                "user_id": user_id,
                "personality_name": personality_name,
                "mood": mood,
                "intensity": intensity,
                "context": context,
                "created_at": datetime.now().isoformat()
            }
            
            await self.storage_v11.save_mood(
                user_id=user_id,
                mood_data=mood_data
            )
            
            return {
                "success": True,
                "mood_saved": True,
                "mood": mood,
                "intensity": intensity
            }
            
        except Exception as e:
            logger.error(f"Error saving mood: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_mood_history(
        self,
        user_id: str,
        personality_name: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get user mood history"""
        try:
            moods = await self.storage_v11.get_moods(
                user_id=user_id,
                personality_name=personality_name,
                max_results=limit
            )
            return moods
            
        except Exception as e:
            logger.error(f"Error getting mood history: {e}")
            return []
    
    
    async def get_sentiment_history(
        self,
        user_id: str,
        personality_name: str = "default",
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get sentiment analysis history"""
        try:
            # Get sentiment history from storage directly
            if self.storage_v11:
                # Try to get sentiment data from facts
                sentiment_facts = await self.storage_v11.get_facts(user_id, category="sentiment_history")
                if sentiment_facts:
                    return sentiment_facts[:limit] if limit else sentiment_facts
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting sentiment history: {e}")
            return []
    
    async def get_sentiment_trends(
        self,
        user_id: str,
        personality_name: str = "default",
        days: int = 7
    ) -> Dict[str, Any]:
        """Get sentiment trends over time"""
        try:
            # Get sentiment history
            sentiment_history = await self.get_sentiment_history(user_id, personality_name, limit=50)
            
            # Simple trend analysis
            if not sentiment_history:
                return {
                    "success": True,
                    "trends": {
                        "overall_trend": "neutral",
                        "average_sentiment": 0.0,
                        "sentiment_count": 0,
                        "positive_percentage": 0.0,
                        "negative_percentage": 0.0,
                        "neutral_percentage": 100.0
                    }
                }
            
            # Calculate trends
            sentiments = [entry.get('sentiment', 'neutral') for entry in sentiment_history]
            sentiment_scores = [entry.get('score', 0.0) for entry in sentiment_history]
            
            positive_count = sentiments.count('positive')
            negative_count = sentiments.count('negative')
            neutral_count = sentiments.count('neutral')
            total_count = len(sentiments)
            
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
            
            # Determine overall trend
            if avg_sentiment > 0.1:
                overall_trend = "positive"
            elif avg_sentiment < -0.1:
                overall_trend = "negative"
            else:
                overall_trend = "neutral"
            
            return {
                "success": True,
                "trends": {
                    "overall_trend": overall_trend,
                    "average_sentiment": avg_sentiment,
                    "sentiment_count": total_count,
                    "positive_percentage": (positive_count / total_count) * 100,
                    "negative_percentage": (negative_count / total_count) * 100,
                    "neutral_percentage": (neutral_count / total_count) * 100
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting sentiment trends: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # SNAPSHOT MANAGEMENT METHODS
    
    async def create_snapshot(
        self,
        session_id: str,
        snapshot_name: Optional[str] = None
    ) -> str:
        """Create a snapshot of the current session state"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            snapshot_id = f"{session_id}_{timestamp}"
            
            if snapshot_name:
                snapshot_id = f"{snapshot_name}_{timestamp}"
            
            # Export current state
            snapshot_data = await self.export_snapshot(session_id)
            
            # Save snapshot metadata
            snapshot_metadata = {
                "snapshot_id": snapshot_id,
                "session_id": session_id,
                "created_at": datetime.now().isoformat(),
                "snapshot_name": snapshot_name or f"snapshot_{timestamp}",
                "data_size": len(str(snapshot_data))
            }
            
            await self.storage_v11.save_snapshot(
                user_id=session_id,
                snapshot_id=snapshot_id,
                snapshot_data=snapshot_data,
                metadata=snapshot_metadata
            )
            
            return snapshot_id
            
        except Exception as e:
            logger.error(f"Error creating snapshot: {e}")
            raise e
    
    async def list_snapshots(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """List all snapshots for a session"""
        try:
            snapshots = await self.storage_v11.get_snapshots(
                user_id=session_id,
                max_results=limit
            )
            return snapshots
            
        except Exception as e:
            logger.error(f"Error listing snapshots: {e}")
            return []
    
    async def delete_snapshot(
        self,
        session_id: str,
        snapshot_id: str
    ) -> Dict[str, Any]:
        """Delete a specific snapshot"""
        try:
            await self.storage_v11.delete_snapshot(
                user_id=session_id,
                snapshot_id=snapshot_id
            )
            
            return {
                "success": True,
                "snapshot_deleted": snapshot_id
            }
            
        except Exception as e:
            logger.error(f"Error deleting snapshot: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_snapshot_info(
        self,
        session_id: str,
        snapshot_id: str
    ) -> Dict[str, Any]:
        """Get information about a specific snapshot"""
        try:
            snapshot_info = await self.storage_v11.get_snapshot_info(
                user_id=session_id,
                snapshot_id=snapshot_id
            )
            
            return {
                "success": True,
                "snapshot_info": snapshot_info
            }
            
        except Exception as e:
            logger.error(f"Error getting snapshot info: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # CONVERSATION HISTORY METHODS
    
    async def get_conversation_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get conversation history for a session"""
        try:
            # Get conversation episodes
            episodes = await self.get_episodes(session_id)
            
            # Filter for conversation episodes
            conversation_episodes = [
                episode for episode in episodes 
                if episode.get("episode_type") == "conversation"
            ]
            
            if limit:
                conversation_episodes = conversation_episodes[-limit:]
            
            return conversation_episodes
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return []
    
    async def export_conversation(
        self,
        session_id: str,
        format: str = "json"
    ) -> Dict[str, Any]:
        """Export conversation in specified format"""
        try:
            conversation_history = await self.get_conversation_history(session_id)
            facts = await self.get_facts(session_id)
            affinity = await self.get_affinity(session_id, "default")
            
            export_data = {
                "session_id": session_id,
                "export_timestamp": datetime.now().isoformat(),
                "conversation_history": conversation_history,
                "facts": facts,
                "affinity": affinity,
                "format": format
            }
            
            return {
                "success": True,
                "export_data": export_data
            }
            
        except Exception as e:
            logger.error(f"Error exporting conversation: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def export_session(self, session_id: str) -> str:
        """Export session data as JSON string"""
        try:
            if not self.storage_v11:
                return json.dumps({"error": "Storage v1.1 not configured"})
            
            # Get session data
            session_data = await self.storage_v11.get_session(session_id)
            if not session_data:
                return json.dumps({"error": "Session not found"})
            
            # Get conversation history
            conversation_history = await self.conversation_manager._get_conversation_history(session_id)
            
            # Get user facts (excluir conversation_history)
            # ✅ FIX: No incluir conversation_history en facts del usuario
            user_id = session_data.get('user_id', session_id)
            all_user_facts = await self.get_facts(user_id)
            user_facts = [f for f in all_user_facts if f.get('category') != 'conversation_history']
            
            # Get affinity
            personality_name = session_data.get('personality_name', 'default')
            affinity = await self.get_affinity(user_id, personality_name)
            
            # Build export data
            export_data = {
                "session_id": session_id,
                "session_data": session_data,
                "conversation_history": [
                    {
                        "user_message": turn.user_message,
                        "assistant_response": turn.assistant_response,
                        "personality_name": turn.personality_name,
                        "timestamp": turn.timestamp.isoformat(),
                        "facts_learned": turn.facts_learned
                    } for turn in conversation_history
                ],
                "user_facts": user_facts,
                "affinity": affinity,
                "export_timestamp": datetime.now().isoformat()
            }
            
            return json.dumps(export_data, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error exporting session: {e}")
            return json.dumps({"error": str(e)})
    
    async def export_user_data(self, user_id: str) -> str:
        """Export complete user data as JSON string"""
        try:
            if not self.storage_v11:
                return json.dumps({"error": "Storage v1.1 not configured"})
            
            # Get all user data (excluir conversation_history)
            # ✅ FIX: No incluir conversation_history en facts del usuario
            all_user_facts = await self.get_facts(user_id)
            user_facts = [f for f in all_user_facts if f.get('category') != 'conversation_history']
            affinity_data = await self.get_affinity(user_id, "default")
            sentiment_history = await self.get_sentiment_history(user_id)
            mood_history = await self.get_mood_history(user_id, "default")
            
            # Build export data
            export_data = {
                "user_id": user_id,
                "user_facts": user_facts,
                "affinity_data": affinity_data,
                "sentiment_history": sentiment_history,
                "mood_history": mood_history,
                "export_timestamp": datetime.now().isoformat()
            }
            
            return json.dumps(export_data, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error exporting user data: {e}")
            return json.dumps({"error": str(e)})
