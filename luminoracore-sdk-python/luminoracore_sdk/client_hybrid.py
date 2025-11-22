"""
Hybrid LuminoraCore SDK Client
Uses core for new functionality while maintaining backward compatibility
"""

import asyncio
from typing import Dict, List, Optional, Any, AsyncGenerator, Union
import logging
from datetime import datetime

# Import from core directly
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'luminoracore'))

from luminoracore import PersonalityEngine, MemorySystem, EvolutionEngine, InMemoryStorage
from luminoracore.interfaces import StorageInterface

# Keep existing imports for backward compatibility
from .types.session import SessionConfig, StorageConfig, MemoryConfig
from .types.provider import ProviderConfig, ChatMessage, ChatResponse
from .types.personality import PersonalityData, PersonalityBlend
from .providers.factory import ProviderFactory
from .providers.base import BaseProvider
from .session.manager import SessionManager
from .session.conversation import ConversationManager
from .session.memory import MemoryManager
from .session.storage import create_storage
from .personality.manager import PersonalityManager
from .personality.blender import PersonalityBlender
from .utils.exceptions import LuminoraCoreSDKError, SessionError, ProviderError
import os
import pathlib
from .utils.helpers import generate_session_id

logger = logging.getLogger(__name__)


class LuminoraCoreClientHybrid:
    """Hybrid client that uses core for new functionality while maintaining compatibility"""
    
    def __init__(
        self,
        storage_config: Optional[StorageConfig] = None,
        memory_config: Optional[MemoryConfig] = None,
        personalities_dir: Optional[str] = None
    ):
        """
        Initialize the hybrid LuminoraCore client.
        
        Args:
            storage_config: Storage configuration
            memory_config: Memory configuration
            personalities_dir: Directory containing personality files
        """
        # Initialize core components
        self.personality_engine = PersonalityEngine()
        self.evolution_engine = EvolutionEngine()
        
        # Set up storage (use core storage if available, fallback to existing)
        if storage_config:
            self.storage = self._create_core_storage(storage_config)
        else:
            self.storage = InMemoryStorage()
        
        # Initialize memory system
        self.memory_system = MemorySystem(self.storage)
        
        # Set evolution engine in personality engine
        self.personality_engine.evolution_engine = self.evolution_engine
        
        # Keep existing components for backward compatibility
        self.storage_config = storage_config
        self.memory_config = memory_config or MemoryConfig()
        
        # Set default personalities directory
        if personalities_dir is None:
            personalities_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'luminoracore', 'personalities')
        
        self.personalities_dir = personalities_dir
        
        # Initialize existing components
        self.session_manager = SessionManager(storage_config)
        self.conversation_manager = ConversationManager()
        self.memory_manager = MemoryManager(memory_config)
        self.personality_manager = PersonalityManager(personalities_dir)
        self.personality_blender = PersonalityBlender()
        
        # Initialize provider factory
        self.provider_factory = ProviderFactory()
        
        logger.info("LuminoraCore hybrid client initialized")
    
    def _create_core_storage(self, storage_config: StorageConfig) -> StorageInterface:
        """Create core storage from existing storage config"""
        # For now, create in-memory storage
        # In the future, this would map to appropriate core storage implementations
        return InMemoryStorage()
    
    # Core-based methods (new functionality)
    async def save_fact(self, user_id: str, category: str, key: str, value: Any, confidence: float = 0.8) -> bool:
        """Save a fact for a user using core storage"""
        return await self.storage.save_fact(user_id, category, key, value, confidence)
    
    async def get_facts(self, user_id: str, category: Optional[str] = None) -> List[Dict]:
        """Get facts for a user using core storage"""
        return await self.storage.get_facts(user_id, category)
    
    async def save_episode(self, user_id: str, episode_type: str, title: str, summary: str, 
                          importance: float = 0.5, sentiment: str = "neutral", 
                          metadata: Optional[Dict] = None) -> bool:
        """Save an episode for a user using core storage"""
        return await self.storage.save_episode(user_id, episode_type, title, summary, 
                                             importance, sentiment, metadata)
    
    async def get_episodes(self, user_id: str, min_importance: Optional[float] = None, 
                          limit: Optional[int] = None) -> List[Dict]:
        """Get episodes for a user using core storage"""
        return await self.storage.get_episodes(user_id, min_importance, limit)
    
    async def update_affinity(self, user_id: str, personality_name: str, points_delta: int, 
                             interaction_type: str = "neutral") -> Dict:
        """Update affinity between user and personality using core storage"""
        return await self.storage.update_affinity(user_id, personality_name, points_delta, 
                                                interaction_type)
    
    async def get_affinity(self, user_id: str, personality_name: str) -> Optional[Dict]:
        """Get affinity between user and personality using core storage"""
        return await self.storage.get_affinity(user_id, personality_name)
    
    async def get_all_affinities(self, user_id: str) -> List[Dict]:
        """Get all affinities for a user using core storage"""
        return await self.storage.get_all_affinities(user_id)
    
    async def search_facts(self, user_id: str, query: str, limit: Optional[int] = None) -> List[Dict]:
        """Search facts using core storage"""
        return await self.storage.search_facts(user_id, query, limit)
    
    async def search_episodes(self, user_id: str, query: str, limit: Optional[int] = None) -> List[Dict]:
        """Search episodes using core storage"""
        return await self.storage.search_episodes(user_id, query, limit)
    
    async def get_user_context(self, user_id: str) -> Dict:
        """Get comprehensive user context using core memory system"""
        return await self.memory_system.get_user_context(user_id)
    
    async def get_relevant_memories(self, user_id: str, context: str, 
                                   memory_types: List[str] = None) -> List[Dict]:
        """Get relevant memories for context using core memory system"""
        return await self.memory_system.get_relevant_memories(user_id, context, memory_types)
    
    async def evolve_personality(self, personality_name: str, user_id: str, 
                                interaction_data: Dict) -> Dict:
        """Evolve personality based on interaction using core evolution engine"""
        return await self.personality_engine.evolve_personality(personality_name, user_id, 
                                                               interaction_data)
    
    # Backward compatibility methods (existing functionality)
    async def initialize(self) -> bool:
        """Initialize the client (backward compatibility)"""
        try:
            await self.session_manager.initialize()
            await self.memory_manager.initialize()
            await self.personality_manager.initialize()
            return True
        except Exception as e:
            logger.error(f"Failed to initialize client: {e}")
            return False
    
    async def cleanup(self) -> bool:
        """Cleanup the client (backward compatibility)"""
        try:
            await self.session_manager.cleanup()
            await self.memory_manager.cleanup()
            return True
        except Exception as e:
            logger.error(f"Failed to cleanup client: {e}")
            return False
    
    async def load_personality(self, name: str, data: Optional[Dict] = None) -> bool:
        """Load a personality (backward compatibility)"""
        if data:
            return await self.personality_engine.load_personality(name, data)
        else:
            return await self.personality_manager.load_personality(name)
    
    async def get_personality(self, name: str) -> Optional[Dict]:
        """Get personality by name (backward compatibility)"""
        # Try core first, then fallback to existing
        personality = await self.personality_engine.get_personality(name)
        if personality:
            return personality
        return await self.personality_manager.get_personality(name)
    
    async def blend_personalities(self, personalities: List[str], weights: List[float]) -> Dict:
        """Blend personalities (backward compatibility)"""
        return await self.personality_engine.blend_personalities(personalities, weights)
    
    async def create_session(self, session_id: Optional[str] = None, 
                           personality_name: Optional[str] = None) -> str:
        """Create a session (backward compatibility)"""
        return await self.session_manager.create_session(session_id, personality_name)
    
    async def send_message(self, session_id: str, message: str, 
                          personality_name: Optional[str] = None) -> ChatResponse:
        """Send a message (backward compatibility)"""
        return await self.session_manager.send_message(session_id, message, personality_name)
    
    async def get_conversation(self, session_id: str) -> List[ChatMessage]:
        """Get conversation history (backward compatibility)"""
        return await self.session_manager.get_conversation(session_id)
    
    async def store_memory(self, session_id: str, memory_type: str, content: str, 
                          importance: float = 0.5) -> bool:
        """Store memory (backward compatibility)"""
        return await self.memory_manager.store_memory(session_id, memory_type, content, importance)
    
    async def get_memory(self, session_id: str, memory_type: Optional[str] = None) -> List[Dict]:
        """Get memory (backward compatibility)"""
        return await self.memory_manager.get_memory(session_id, memory_type)
    
    # Health and stats methods
    async def health_check(self) -> Dict:
        """Check system health"""
        return await self.storage.health_check()
    
    async def get_user_stats(self, user_id: str) -> Dict:
        """Get statistics for a user"""
        return await self.storage.get_user_stats(user_id)
    
    async def get_memory_stats(self, user_id: str) -> Dict:
        """Get memory statistics for a user"""
        return await self.memory_system.get_memory_stats(user_id)
    
    async def cleanup_old_data(self, days_old: int = 365) -> int:
        """Clean up old data"""
        return await self.storage.cleanup_old_data(days_old)
