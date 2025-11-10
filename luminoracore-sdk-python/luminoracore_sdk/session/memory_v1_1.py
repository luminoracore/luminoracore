"""
Memory Manager v1.1 Extensions for LuminoraCore SDK

Adds episodic memory and semantic search capabilities.
"""

from typing import List, Optional, Dict, Any
import logging

from ..types.memory import FactDict, EpisodeDict, MemorySearchResult, MemoryQueryOptions

logger = logging.getLogger(__name__)


class MemoryManagerV11:
    """
    Extended memory manager for v1.1 features
    
    Usage:
        manager = MemoryManagerV11(storage=storage_v11)
        
        # Get episodes
        episodes = await manager.get_episodes(user_id="user1", min_importance=7.0)
        
        # Get facts
        facts = await manager.get_facts(user_id="user1", category="personal_info")
        
        # Semantic search (requires vector store)
        results = await manager.semantic_search(
            user_id="user1",
            query="remember when we talked about my dog?",
            top_k=5
        )
    """
    
    def __init__(self, storage_v11=None, vector_store=None):
        """
        Initialize v1.1 memory manager
        
        Args:
            storage_v11: Storage v1.1 extension instance
            vector_store: Vector store for semantic search (optional)
        """
        self.storage = storage_v11
        self.vector_store = vector_store
    
    async def get_facts(
        self,
        user_id: str,
        options: Optional[MemoryQueryOptions] = None
    ) -> List[FactDict]:
        """
        Get user facts with optional filtering
        
        Args:
            user_id: User ID
            options: Query options (category filter, sorting, etc.)
            
        Returns:
            List of facts
        """
        if not self.storage:
            logger.warning("No storage configured")
            return []
        
        category = options.get("category") if options else None
        
        facts = await self.storage.get_facts(user_id, category=category)
        
        # Apply additional filtering if options provided
        if options:
            if not options.get("include_inactive", True):
                facts = [f for f in facts if f.get("is_active", True)]
            
            max_results = options.get("max_results")
            if max_results:
                facts = facts[:max_results]
        
        return facts
    
    async def get_episodes(
        self,
        user_id: str,
        min_importance: Optional[float] = None,
        max_results: Optional[int] = None
    ) -> List[EpisodeDict]:
        """
        Get user episodes
        
        Args:
            user_id: User ID
            min_importance: Minimum importance filter
            max_results: Maximum number of results
            
        Returns:
            List of episodes
        """
        if not self.storage:
            logger.warning("No storage configured")
            return []
        
        episodes = await self.storage.get_episodes(user_id, min_importance=min_importance)
        
        # Sort by importance (descending)
        episodes_sorted = sorted(
            episodes,
            key=lambda e: e.get("importance", 0) * e.get("temporal_decay", 1.0),
            reverse=True
        )
        
        if max_results:
            episodes_sorted = episodes_sorted[:max_results]
        
        return episodes_sorted
    
    async def get_episode_by_id(
        self,
        episode_id: str
    ) -> Optional[EpisodeDict]:
        """
        Get a specific episode by ID
        
        Args:
            episode_id: Episode ID
            
        Returns:
            Episode or None
        """
        # This would need implementation in storage
        # For now, return None
        logger.warning("get_episode_by_id not yet implemented")
        return None
    
    async def semantic_search(
        self,
        user_id: str,
        query: str,
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[MemorySearchResult]:
        """
        Perform semantic search on memories
        
        Args:
            user_id: User ID
            query: Search query
            top_k: Number of results to return
            filters: Optional filters (date range, importance, etc.)
            
        Returns:
            List of search results with similarity scores
        """
        if not self.vector_store:
            logger.warning("Vector store not configured, semantic search unavailable")
            return []
        
        # This would use vector store for actual search
        # For now, return empty list
        logger.info(f"Semantic search: '{query}' (top_k={top_k})")
        return []
    
    async def get_context_for_query(
        self,
        user_id: str,
        query: str,
        max_facts: int = 5,
        max_episodes: int = 3
    ) -> Dict[str, Any]:
        """
        Get relevant context for a query
        
        Combines facts, episodes, and semantic search.
        
        Args:
            user_id: User ID
            query: Query to find context for
            max_facts: Maximum facts to include
            max_episodes: Maximum episodes to include
            
        Returns:
            Dict with facts, episodes, and search results
        """
        # Get recent facts
        facts = await self.get_facts(user_id, options={"max_results": max_facts})
        
        # Get important episodes
        episodes = await self.get_episodes(
            user_id,
            min_importance=5.0,
            max_results=max_episodes
        )
        
        # Semantic search if available
        search_results = []
        if self.vector_store:
            search_results = await self.semantic_search(user_id, query, top_k=5)
        
        return {
            "facts": facts,
            "episodes": episodes,
            "search_results": search_results
        }

