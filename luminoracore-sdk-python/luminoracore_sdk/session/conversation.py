"""Conversation management for LuminoraCore SDK."""

import asyncio
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

from ..types.session import Conversation, Message, MessageRole
from ..utils.exceptions import SessionError
from ..utils.helpers import generate_session_id

logger = logging.getLogger(__name__)


class ConversationManager:
    """Manages conversation history and context."""
    
    def __init__(self, max_history: int = 100):
        """
        Initialize the conversation manager.
        
        Args:
            max_history: Maximum number of messages to keep in history
        """
        self.max_history = max_history
        self._conversations: Dict[str, Conversation] = {}
        self._lock = asyncio.Lock()
    
    async def create_conversation(self, session_id: str) -> Conversation:
        """
        Create a new conversation.
        
        Args:
            session_id: Session ID
            
        Returns:
            New conversation object
        """
        conversation = Conversation(
            session_id=session_id,
            messages=[],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        
        async with self._lock:
            self._conversations[session_id] = conversation
        
        logger.info(f"Created conversation for session: {session_id}")
        return conversation
    
    async def get_conversation(self, session_id: str) -> Optional[Conversation]:
        """
        Get conversation for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            Conversation or None if not found
        """
        async with self._lock:
            return self._conversations.get(session_id)
    
    async def add_message(
        self,
        session_id: str,
        role: MessageRole,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Message:
        """
        Add a message to the conversation.
        
        Args:
            session_id: Session ID
            role: Message role
            content: Message content
            metadata: Optional message metadata
            
        Returns:
            Created message object
        """
        conversation = await self.get_conversation(session_id)
        if not conversation:
            raise SessionError(f"Conversation not found for session: {session_id}")
        
        message = Message(
            role=role,
            content=content,
            timestamp=datetime.utcnow(),
            metadata=metadata or {}
        )
        
        async with self._lock:
            conversation.messages.append(message)
            conversation.updated_at = datetime.utcnow()
            
            # Trim history if necessary
            if len(conversation.messages) > self.max_history:
                conversation.messages = conversation.messages[-self.max_history:]
        
        logger.debug(f"Added message to conversation {session_id}: {role}")
        return message
    
    async def get_messages(
        self,
        session_id: str,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Message]:
        """
        Get messages from conversation.
        
        Args:
            session_id: Session ID
            limit: Maximum number of messages to return
            offset: Number of messages to skip
            
        Returns:
            List of messages
        """
        conversation = await self.get_conversation(session_id)
        if not conversation:
            return []
        
        messages = conversation.messages[offset:]
        if limit:
            messages = messages[:limit]
        
        return messages
    
    async def get_last_message(self, session_id: str) -> Optional[Message]:
        """
        Get the last message from conversation.
        
        Args:
            session_id: Session ID
            
        Returns:
            Last message or None if conversation is empty
        """
        conversation = await self.get_conversation(session_id)
        if not conversation or not conversation.messages:
            return None
        
        return conversation.messages[-1]
    
    async def get_message_count(self, session_id: str) -> int:
        """
        Get the number of messages in conversation.
        
        Args:
            session_id: Session ID
            
        Returns:
            Number of messages
        """
        conversation = await self.get_conversation(session_id)
        if not conversation:
            return 0
        
        return len(conversation.messages)
    
    async def clear_conversation(self, session_id: str) -> bool:
        """
        Clear all messages from conversation.
        
        Args:
            session_id: Session ID
            
        Returns:
            True if conversation was cleared
        """
        conversation = await self.get_conversation(session_id)
        if not conversation:
            return False
        
        async with self._lock:
            conversation.messages.clear()
            conversation.updated_at = datetime.utcnow()
        
        logger.info(f"Cleared conversation for session: {session_id}")
        return True
    
    async def delete_conversation(self, session_id: str) -> bool:
        """
        Delete a conversation.
        
        Args:
            session_id: Session ID
            
        Returns:
            True if conversation was deleted
        """
        async with self._lock:
            if session_id in self._conversations:
                del self._conversations[session_id]
                logger.info(f"Deleted conversation for session: {session_id}")
                return True
        
        return False
    
    async def get_conversation_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get conversation summary.
        
        Args:
            session_id: Session ID
            
        Returns:
            Conversation summary or None if not found
        """
        conversation = await self.get_conversation(session_id)
        if not conversation:
            return None
        
        user_messages = [msg for msg in conversation.messages if msg.role == "user"]
        assistant_messages = [msg for msg in conversation.messages if msg.role == "assistant"]
        
        return {
            "session_id": session_id,
            "total_messages": len(conversation.messages),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "created_at": conversation.created_at,
            "updated_at": conversation.updated_at,
            "first_message": conversation.messages[0] if conversation.messages else None,
            "last_message": conversation.messages[-1] if conversation.messages else None,
        }
    
    async def search_messages(
        self,
        session_id: str,
        query: str,
        limit: Optional[int] = None
    ) -> List[Message]:
        """
        Search messages in conversation.
        
        Args:
            session_id: Session ID
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching messages
        """
        conversation = await self.get_conversation(session_id)
        if not conversation:
            return []
        
        query_lower = query.lower()
        matching_messages = []
        
        for message in conversation.messages:
            if query_lower in message.content.lower():
                matching_messages.append(message)
        
        if limit:
            matching_messages = matching_messages[:limit]
        
        return matching_messages
    
    async def get_messages_by_role(
        self,
        session_id: str,
        role: MessageRole,
        limit: Optional[int] = None
    ) -> List[Message]:
        """
        Get messages by role.
        
        Args:
            session_id: Session ID
            role: Message role to filter by
            limit: Maximum number of results
            
        Returns:
            List of messages with the specified role
        """
        conversation = await self.get_conversation(session_id)
        if not conversation:
            return []
        
        messages = [msg for msg in conversation.messages if msg.role == role]
        
        if limit:
            messages = messages[:limit]
        
        return messages
    
    async def list_conversations(self) -> List[str]:
        """
        List all active conversations.
        
        Returns:
            List of session IDs
        """
        async with self._lock:
            return list(self._conversations.keys())
    
    async def get_conversation_stats(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get conversation statistics.
        
        Args:
            session_id: Session ID
            
        Returns:
            Conversation statistics or None if not found
        """
        conversation = await self.get_conversation(session_id)
        if not conversation:
            return None
        
        stats = {
            "total_messages": len(conversation.messages),
            "user_messages": 0,
            "assistant_messages": 0,
            "system_messages": 0,
            "total_characters": 0,
            "average_message_length": 0,
            "created_at": conversation.created_at,
            "updated_at": conversation.updated_at,
            "duration": (conversation.updated_at - conversation.created_at).total_seconds(),
        }
        
        for message in conversation.messages:
            stats[f"{message.role}_messages"] += 1
            stats["total_characters"] += len(message.content)
        
        if stats["total_messages"] > 0:
            stats["average_message_length"] = stats["total_characters"] / stats["total_messages"]
        
        return stats
