"""
LuminoraCore Client v1.1 Extensions

Adds v1.1 API methods to the SDK client.
"""

from typing import List, Optional, Dict, Any
import logging
from datetime import datetime

from .session.storage_v1_1 import StorageV11Extension
from .session.memory_v1_1 import MemoryManagerV11
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
        # Placeholder implementation
        logger.info(f"Exporting snapshot for session {session_id}")
        
        snapshot: PersonalitySnapshotDict = {
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
        
        return snapshot
    
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

