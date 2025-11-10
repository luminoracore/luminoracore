"""Session manager for LuminoraCore SDK."""

import asyncio
from typing import Dict, List, Optional, Any, AsyncGenerator
import logging
from datetime import datetime

from ..types.session import SessionConfig, SessionType, Message, Conversation
from ..types.provider import ChatMessage, ChatResponse
from ..providers.factory import ProviderFactory
from ..providers.base import BaseProvider
from ..utils.exceptions import SessionError
from ..utils.helpers import generate_session_id

logger = logging.getLogger(__name__)


class SessionManager:
    """Manages AI personality sessions and conversations."""
    
    def __init__(self, storage: Optional[Any] = None):
        """
        Initialize the session manager.
        
        Args:
            storage: Optional storage backend for session persistence
        """
        self.storage = storage
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._providers: Dict[str, BaseProvider] = {}
        self._lock = asyncio.Lock()
    
    async def create_session(
        self,
        personality: Dict[str, Any],
        provider_config: Dict[str, Any],
        session_config: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new session.
        
        Args:
            personality: Personality configuration
            provider_config: Provider configuration
            session_config: Optional session configuration
            
        Returns:
            Session ID
        """
        session_id = generate_session_id()
        
        # Create provider
        provider = ProviderFactory.create_provider_from_dict(provider_config)
        self._providers[session_id] = provider
        
        # Create session configuration
        config = SessionConfig(
            session_id=session_id,
            personality=personality,
            provider_config=provider_config,
            session_type=SessionType.CHAT,
            max_history=session_config.get("max_history", 100) if session_config else 100,
            timeout=session_config.get("timeout", 300) if session_config else 300,
        )
        
        # Initialize session
        session_data = {
            "config": config,
            "conversation": Conversation(
                session_id=session_id,
                messages=[],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
            "personality": personality,
            "provider": provider,
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
        }
        
        async with self._lock:
            self._sessions[session_id] = session_data
        
        # Save to storage if available
        if self.storage:
            await self.storage.save_session(session_id, session_data)
        
        logger.info(f"Created session: {session_id}")
        return session_id
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session data.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session data or None if not found
        """
        # Check memory first
        if session_id in self._sessions:
            return self._sessions[session_id]
        
        # Load from storage if available
        if self.storage:
            session_data = await self.storage.load_session(session_id)
            if session_data:
                self._sessions[session_id] = session_data
                return session_data
        
        return None
    
    async def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            True if session was deleted
        """
        async with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
            
            if session_id in self._providers:
                del self._providers[session_id]
        
        # Delete from storage if available
        if self.storage:
            await self.storage.delete_session(session_id)
        
        logger.info(f"Deleted session: {session_id}")
        return True
    
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
        """
        session_data = await self.get_session(session_id)
        if not session_data:
            raise SessionError(f"Session not found: {session_id}")
        
        provider = session_data["provider"]
        conversation = session_data["conversation"]
        personality = session_data["personality"]
        
        # Add user message to conversation
        user_message = Message(
            role="user",
            content=message,
            timestamp=datetime.utcnow(),
            metadata={}
        )
        conversation.messages.append(user_message)
        
        # Prepare messages for provider
        chat_messages = self._prepare_messages(conversation, personality)
        
        try:
            # Send to provider
            response = await provider.chat_with_retry(
                messages=chat_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            # Add assistant response to conversation
            assistant_message = Message(
                role="assistant",
                content=response.content,
                timestamp=datetime.utcnow(),
                metadata=response.provider_metadata or {}
            )
            conversation.messages.append(assistant_message)
            
            # Update session
            session_data["last_activity"] = datetime.utcnow()
            conversation.updated_at = datetime.utcnow()
            
            # Save to storage if available
            if self.storage:
                await self.storage.save_session(session_id, session_data)
            
            return response
            
        except Exception as e:
            logger.error(f"Error sending message to session {session_id}: {e}")
            raise SessionError(f"Failed to send message: {e}")
    
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
        """
        session_data = await self.get_session(session_id)
        if not session_data:
            raise SessionError(f"Session not found: {session_id}")
        
        provider = session_data["provider"]
        conversation = session_data["conversation"]
        personality = session_data["personality"]
        
        # Add user message to conversation
        user_message = Message(
            role="user",
            content=message,
            timestamp=datetime.utcnow(),
            metadata={}
        )
        conversation.messages.append(user_message)
        
        # Prepare messages for provider
        chat_messages = self._prepare_messages(conversation, personality)
        
        try:
            # Stream from provider
            full_response = ""
            async for chunk in provider.stream_chat_with_retry(
                messages=chat_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            ):
                full_response += chunk.content
                yield chunk
            
            # Add complete assistant response to conversation
            assistant_message = Message(
                role="assistant",
                content=full_response,
                timestamp=datetime.utcnow(),
                metadata=chunk.provider_metadata or {}
            )
            conversation.messages.append(assistant_message)
            
            # Update session
            session_data["last_activity"] = datetime.utcnow()
            conversation.updated_at = datetime.utcnow()
            
            # Save to storage if available
            if self.storage:
                await self.storage.save_session(session_id, session_data)
            
        except Exception as e:
            logger.error(f"Error streaming message to session {session_id}: {e}")
            raise SessionError(f"Failed to stream message: {e}")
    
    async def get_conversation(self, session_id: str) -> Optional[Conversation]:
        """
        Get conversation for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            Conversation or None if session not found
        """
        session_data = await self.get_session(session_id)
        if not session_data:
            return None
        
        return session_data["conversation"]
    
    async def clear_conversation(self, session_id: str) -> bool:
        """
        Clear conversation history for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            True if conversation was cleared
        """
        session_data = await self.get_session(session_id)
        if not session_data:
            return False
        
        conversation = session_data["conversation"]
        conversation.messages.clear()
        conversation.updated_at = datetime.utcnow()
        
        # Save to storage if available
        if self.storage:
            await self.storage.save_session(session_id, session_data)
        
        logger.info(f"Cleared conversation for session: {session_id}")
        return True
    
    async def update_personality(self, session_id: str, personality: Dict[str, Any]) -> bool:
        """
        Update personality for a session.
        
        Args:
            session_id: Session ID
            personality: New personality configuration
            
        Returns:
            True if personality was updated
        """
        session_data = await self.get_session(session_id)
        if not session_data:
            return False
        
        session_data["personality"] = personality
        session_data["last_activity"] = datetime.utcnow()
        
        # Save to storage if available
        if self.storage:
            await self.storage.save_session(session_id, session_data)
        
        logger.info(f"Updated personality for session: {session_id}")
        return True
    
    async def list_sessions(self) -> List[str]:
        """
        List all active sessions.
        
        Returns:
            List of session IDs
        """
        return list(self._sessions.keys())
    
    async def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session information.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session information or None if not found
        """
        session_data = await self.get_session(session_id)
        if not session_data:
            return None
        
        return {
            "session_id": session_id,
            "personality": session_data["personality"]["name"],
            "provider": session_data["provider"].name,
            "model": session_data["provider"].model,
            "created_at": session_data["created_at"],
            "last_activity": session_data["last_activity"],
            "message_count": len(session_data["conversation"].messages),
        }
    
    def _prepare_messages(
        self,
        conversation: Conversation,
        personality: Dict[str, Any]
    ) -> List[ChatMessage]:
        """
        Prepare messages for provider.
        
        Args:
            conversation: Conversation object
            personality: Personality configuration
            
        Returns:
            List of chat messages
        """
        messages = []
        
        # Add system message if personality has one
        if "system_prompt" in personality:
            messages.append(ChatMessage(
                role="system",
                content=personality["system_prompt"]
            ))
        
        # Add conversation messages
        for message in conversation.messages:
            messages.append(ChatMessage(
                role=message.role,
                content=message.content
            ))
        
        return messages
