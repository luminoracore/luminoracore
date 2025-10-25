"""Main LuminoraCore client for AI personality management."""

import asyncio
from typing import Dict, List, Optional, Any, AsyncGenerator, Union
import logging
from datetime import datetime

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


class LuminoraCoreClient:
    """Main client for LuminoraCore SDK."""
    
    def __init__(
        self,
        storage_config: Optional[StorageConfig] = None,
        memory_config: Optional[MemoryConfig] = None,
        personalities_dir: Optional[str] = None
    ):
        """
        Initialize the LuminoraCore client.
        
        Args:
            storage_config: Storage configuration
            memory_config: Memory configuration
            personalities_dir: Directory containing personality files
        """
        # Initialize components
        self.storage_config = storage_config
        self.memory_config = memory_config or MemoryConfig()
        
        # Set default personalities directory to SDK's personalities folder
        if personalities_dir is None:
            # Get the path to the SDK's personalities directory
            sdk_dir = pathlib.Path(__file__).parent
            self.personalities_dir = str(sdk_dir / "personalities")
        else:
            self.personalities_dir = personalities_dir
        
        # Create storage backend
        if storage_config:
            self.storage = create_storage(storage_config)
        else:
            self.storage = None
        
        # Initialize managers
        self.session_manager = SessionManager(storage=self.storage)
        self.conversation_manager = ConversationManager()
        self.memory_manager = MemoryManager(memory_config)
        self.personality_manager = PersonalityManager(personalities_dir)
        self.personality_blender = PersonalityBlender()
        
        # Initialize provider registry
        self._providers: Dict[str, BaseProvider] = {}
        self._lock = asyncio.Lock()
    
    async def initialize(self) -> None:
        """Initialize the client and load personalities."""
        try:
            # Load personalities from directory
            await self.personality_manager.load_personalities_from_directory()
            logger.info("LuminoraCore client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize LuminoraCore client: {e}")
            raise LuminoraCoreSDKError(f"Initialization failed: {e}")
    
    async def create_session(
        self,
        personality_name: str,
        provider_config: ProviderConfig,
        session_config: Optional[SessionConfig] = None
    ) -> str:
        """
        Create a new AI personality session.
        
        Args:
            personality_name: Name of the personality to use
            provider_config: Provider configuration
            session_config: Optional session configuration
            
        Returns:
            Session ID
            
        Raises:
            LuminoraCoreSDKError: If session creation fails
        """
        try:
            # Get personality
            personality = await self.personality_manager.get_personality(personality_name)
            if not personality:
                raise LuminoraCoreSDKError(f"Personality not found: {personality_name}")
            
            # Create session
            session_id = await self.session_manager.create_session(
                personality=personality.__dict__,
                provider_config=provider_config.__dict__,
                session_config=session_config.__dict__ if session_config else None
            )
            
            logger.info(f"Created session {session_id} with personality {personality_name}")
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to create session: {e}")
            raise LuminoraCoreSDKError(f"Session creation failed: {e}")
    
    async def send_message(
        self,
        session_id: str,
        message: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatResponse:
        """
        Send a message to a session.
        
        Args:
            session_id: Session ID
            message: User message
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters
            
        Returns:
            Chat response
            
        Raises:
            LuminoraCoreSDKError: If message sending fails
        """
        try:
            response = await self.session_manager.send_message(
                session_id=session_id,
                message=message,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            logger.debug(f"Sent message to session {session_id}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to send message to session {session_id}: {e}")
            raise LuminoraCoreSDKError(f"Message sending failed: {e}")
    
    async def stream_message(
        self,
        session_id: str,
        message: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[ChatResponse, None]:
        """
        Stream a message to a session.
        
        Args:
            session_id: Session ID
            message: User message
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters
            
        Yields:
            Chat response chunks
            
        Raises:
            LuminoraCoreSDKError: If message streaming fails
        """
        try:
            async for chunk in self.session_manager.stream_message(
                session_id=session_id,
                message=message,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            ):
                yield chunk
                
        except Exception as e:
            logger.error(f"Failed to stream message to session {session_id}: {e}")
            raise LuminoraCoreSDKError(f"Message streaming failed: {e}")
    
    async def get_conversation(self, session_id: str) -> Optional[List[ChatMessage]]:
        """
        Get conversation history for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            List of chat messages or None if session not found
        """
        try:
            conversation = await self.session_manager.get_conversation(session_id)
            if not conversation:
                return None
            
            # Convert to chat messages
            messages = []
            for msg in conversation.messages:
                messages.append(ChatMessage(
                    role=msg.role,
                    content=msg.content
                ))
            
            return messages
            
        except Exception as e:
            logger.error(f"Failed to get conversation for session {session_id}: {e}")
            return None
    
    async def clear_conversation(self, session_id: str) -> bool:
        """
        Clear conversation history for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            True if conversation was cleared
        """
        try:
            return await self.session_manager.clear_conversation(session_id)
        except Exception as e:
            logger.error(f"Failed to clear conversation for session {session_id}: {e}")
            return False
    
    async def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            True if session was deleted
        """
        try:
            return await self.session_manager.delete_session(session_id)
        except Exception as e:
            logger.error(f"Failed to delete session {session_id}: {e}")
            return False
    
    async def list_sessions(self) -> List[str]:
        """
        List all active sessions.
        
        Returns:
            List of session IDs
        """
        try:
            return await self.session_manager.list_sessions()
        except Exception as e:
            logger.error(f"Failed to list sessions: {e}")
            return []
    
    async def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session information.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session information or None if not found
        """
        try:
            return await self.session_manager.get_session_info(session_id)
        except Exception as e:
            logger.error(f"Failed to get session info for {session_id}: {e}")
            return None
    
    # Personality Management
    
    async def load_personality(self, name: str, config: Dict[str, Any]) -> bool:
        """
        Load a personality from configuration.
        
        Args:
            name: Personality name
            config: Personality configuration
            
        Returns:
            True if personality was loaded
        """
        try:
            await self.personality_manager.load_personality(name, config)
            return True
        except Exception as e:
            logger.error(f"Failed to load personality {name}: {e}")
            return False
    
    async def get_personality(self, name: str) -> Optional[PersonalityData]:
        """
        Get a personality by name.
        
        Args:
            name: Personality name
            
        Returns:
            Personality data or None if not found
        """
        try:
            return await self.personality_manager.get_personality(name)
        except Exception as e:
            logger.error(f"Failed to get personality {name}: {e}")
            return None
    
    async def list_personalities(self) -> List[str]:
        """
        List all loaded personalities.
        
        Returns:
            List of personality names
        """
        try:
            return await self.personality_manager.list_personalities()
        except Exception as e:
            logger.error(f"Failed to list personalities: {e}")
            return []
    
    async def delete_personality(self, name: str) -> bool:
        """
        Delete a personality.
        
        Args:
            name: Personality name
            
        Returns:
            True if personality was deleted
        """
        try:
            return await self.personality_manager.delete_personality(name)
        except Exception as e:
            logger.error(f"Failed to delete personality {name}: {e}")
            return False
    
    # Personality Blending
    
    async def blend_personalities(
        self,
        personality_names: List[str],
        weights: List[float],
        blend_name: Optional[str] = None
    ) -> Optional[PersonalityData]:
        """
        Blend multiple personalities.
        
        Args:
            personality_names: List of personality names to blend
            weights: List of weights for each personality
            blend_name: Optional name for the blended personality
            
        Returns:
            Blended personality data or None if blending fails
        """
        try:
            # Get personalities
            personalities = []
            for name in personality_names:
                personality = await self.personality_manager.get_personality(name)
                if not personality:
                    raise LuminoraCoreSDKError(f"Personality not found: {name}")
                personalities.append(personality)
            
            # Blend personalities
            blended = await self.personality_blender.blend_personalities(
                personalities=personalities,
                weights=weights,
                blend_name=blend_name
            )
            
            # Load the blended personality
            await self.personality_manager.load_personality(blend_name or blended.name, blended.__dict__)
            
            return blended
            
        except Exception as e:
            logger.error(f"Failed to blend personalities: {e}")
            return None
    
    async def blend_personalities_from_config(
        self,
        blend_config: Dict[str, float],
        blend_name: Optional[str] = None
    ) -> Optional[PersonalityData]:
        """
        Blend personalities from configuration.
        
        Args:
            blend_config: Dictionary mapping personality names to weights
            blend_name: Optional name for the blended personality
            
        Returns:
            Blended personality data or None if blending fails
        """
        try:
            blended = await self.personality_blender.blend_personalities_from_config(
                blend_config=blend_config,
                personality_manager=self.personality_manager
            )
            
            # Load the blended personality
            await self.personality_manager.load_personality(blend_name or blended.name, blended.__dict__)
            
            return blended
            
        except Exception as e:
            logger.error(f"Failed to blend personalities from config: {e}")
            return None
    
    # Memory Management
    
    async def store_memory(
        self,
        session_id: str,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Store a memory item for a session.
        
        Args:
            session_id: Session ID
            key: Memory key
            value: Memory value
            ttl: Time to live in seconds
            
        Returns:
            True if memory was stored
        """
        try:
            return await self.memory_manager.store_memory(session_id, key, value, ttl)
        except Exception as e:
            logger.error(f"Failed to store memory for session {session_id}: {e}")
            return False
    
    async def get_memory(self, session_id: str, key: str) -> Optional[Any]:
        """
        Get a memory item for a session.
        
        Args:
            session_id: Session ID
            key: Memory key
            
        Returns:
            Memory value or None if not found
        """
        try:
            return await self.memory_manager.get_memory(session_id, key)
        except Exception as e:
            logger.error(f"Failed to get memory for session {session_id}: {e}")
            return None
    
    async def delete_memory(self, session_id: str, key: str) -> bool:
        """
        Delete a memory item for a session.
        
        Args:
            session_id: Session ID
            key: Memory key
            
        Returns:
            True if memory was deleted
        """
        try:
            return await self.memory_manager.delete_memory(session_id, key)
        except Exception as e:
            logger.error(f"Failed to delete memory for session {session_id}: {e}")
            return False
    
    async def clear_memory(self, session_id: str) -> bool:
        """
        Clear all memories for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            True if memories were cleared
        """
        try:
            return await self.memory_manager.clear_memory(session_id)
        except Exception as e:
            logger.error(f"Failed to clear memory for session {session_id}: {e}")
            return False
    
    # Utility Methods
    
    async def get_client_info(self) -> Dict[str, Any]:
        """
        Get client information.
        
        Returns:
            Client information dictionary
        """
        try:
            personalities = await self.personality_manager.list_personalities()
            sessions = await self.session_manager.list_sessions()
            
            return {
                "client_version": "1.0.0",
                "storage_type": self.storage_config.storage_type if self.storage_config else "memory",
                "personalities_dir": self.personalities_dir,
                "total_personalities": len(personalities),
                "total_sessions": len(sessions),
                "personality_names": personalities,
                "session_ids": sessions,
            }
            
        except Exception as e:
            logger.error(f"Failed to get client info: {e}")
            return {}
    
    async def cleanup(self) -> None:
        """Clean up resources and close connections."""
        try:
            # Clean up expired memories
            await self.memory_manager.cleanup_expired_memories()
            
            # Clear blend cache
            await self.personality_blender.clear_blend_cache()
            
            logger.info("LuminoraCore client cleanup completed")
            
        except Exception as e:
            logger.error(f"Failed to cleanup LuminoraCore client: {e}")
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.cleanup()
