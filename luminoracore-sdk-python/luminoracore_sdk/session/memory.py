"""Memory management for LuminoraCore SDK."""

import asyncio
from typing import Dict, List, Optional, Any, Union
import logging
from datetime import datetime, timedelta
import json

from ..types.session import MemoryConfig, Message
from ..utils.exceptions import SessionError
from ..utils.helpers import generate_session_id

logger = logging.getLogger(__name__)


class MemoryManager:
    """Manages conversation memory and context."""
    
    def __init__(self, config: Optional[MemoryConfig] = None):
        """
        Initialize the memory manager.
        
        Args:
            config: Memory configuration
        """
        self.config = config or MemoryConfig()
        self._memories: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()
    
    async def store_memory(
        self,
        session_id: str,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Store a memory item.
        
        Args:
            session_id: Session ID
            key: Memory key
            value: Memory value
            ttl: Time to live in seconds
            
        Returns:
            True if memory was stored
        """
        ttl = ttl or self.config.ttl
        
        memory_item = {
            "value": value,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(seconds=ttl) if ttl else None,
            "access_count": 0,
            "last_accessed": datetime.utcnow(),
        }
        
        async with self._lock:
            if session_id not in self._memories:
                self._memories[session_id] = {}
            
            self._memories[session_id][key] = memory_item
        
        logger.debug(f"Stored memory for session {session_id}: {key}")
        return True
    
    async def get_memory(self, session_id: str, key: str) -> Optional[Any]:
        """
        Get a memory item.
        
        Args:
            session_id: Session ID
            key: Memory key
            
        Returns:
            Memory value or None if not found or expired
        """
        async with self._lock:
            if session_id not in self._memories:
                return None
            
            if key not in self._memories[session_id]:
                return None
            
            memory_item = self._memories[session_id][key]
            
            # Check if expired
            if memory_item["expires_at"] and datetime.utcnow() > memory_item["expires_at"]:
                del self._memories[session_id][key]
                return None
            
            # Update access statistics
            memory_item["access_count"] += 1
            memory_item["last_accessed"] = datetime.utcnow()
            
            return memory_item["value"]
    
    async def delete_memory(self, session_id: str, key: str) -> bool:
        """
        Delete a memory item.
        
        Args:
            session_id: Session ID
            key: Memory key
            
        Returns:
            True if memory was deleted
        """
        async with self._lock:
            if session_id not in self._memories:
                return False
            
            if key in self._memories[session_id]:
                del self._memories[session_id][key]
                logger.debug(f"Deleted memory for session {session_id}: {key}")
                return True
        
        return False
    
    async def clear_memory(self, session_id: str) -> bool:
        """
        Clear all memories for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            True if memories were cleared
        """
        async with self._lock:
            if session_id in self._memories:
                del self._memories[session_id]
                logger.info(f"Cleared all memories for session: {session_id}")
                return True
        
        return False
    
    async def list_memories(self, session_id: str) -> List[str]:
        """
        List all memory keys for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            List of memory keys
        """
        async with self._lock:
            if session_id not in self._memories:
                return []
            
            # Filter out expired memories
            valid_keys = []
            for key, memory_item in self._memories[session_id].items():
                if not memory_item["expires_at"] or datetime.utcnow() <= memory_item["expires_at"]:
                    valid_keys.append(key)
                else:
                    del self._memories[session_id][key]
            
            return valid_keys
    
    async def get_memory_info(self, session_id: str, key: str) -> Optional[Dict[str, Any]]:
        """
        Get memory item information.
        
        Args:
            session_id: Session ID
            key: Memory key
            
        Returns:
            Memory information or None if not found
        """
        async with self._lock:
            if session_id not in self._memories or key not in self._memories[session_id]:
                return None
            
            memory_item = self._memories[session_id][key]
            
            # Check if expired
            if memory_item["expires_at"] and datetime.utcnow() > memory_item["expires_at"]:
                del self._memories[session_id][key]
                return None
            
            return {
                "key": key,
                "created_at": memory_item["created_at"],
                "expires_at": memory_item["expires_at"],
                "access_count": memory_item["access_count"],
                "last_accessed": memory_item["last_accessed"],
                "is_expired": memory_item["expires_at"] and datetime.utcnow() > memory_item["expires_at"],
            }
    
    async def cleanup_expired_memories(self) -> int:
        """
        Clean up expired memories.
        
        Returns:
            Number of expired memories cleaned up
        """
        cleaned_count = 0
        
        async with self._lock:
            for session_id in list(self._memories.keys()):
                for key in list(self._memories[session_id].keys()):
                    memory_item = self._memories[session_id][key]
                    if memory_item["expires_at"] and datetime.utcnow() > memory_item["expires_at"]:
                        del self._memories[session_id][key]
                        cleaned_count += 1
        
        if cleaned_count > 0:
            logger.info(f"Cleaned up {cleaned_count} expired memories")
        
        return cleaned_count
    
    async def get_memory_stats(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get memory statistics for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            Memory statistics or None if session not found
        """
        async with self._lock:
            if session_id not in self._memories:
                return None
            
            memories = self._memories[session_id]
            total_memories = len(memories)
            expired_memories = 0
            total_access_count = 0
            oldest_memory = None
            newest_memory = None
            
            for key, memory_item in memories.items():
                if memory_item["expires_at"] and datetime.utcnow() > memory_item["expires_at"]:
                    expired_memories += 1
                
                total_access_count += memory_item["access_count"]
                
                if oldest_memory is None or memory_item["created_at"] < oldest_memory:
                    oldest_memory = memory_item["created_at"]
                
                if newest_memory is None or memory_item["created_at"] > newest_memory:
                    newest_memory = memory_item["created_at"]
            
            return {
                "total_memories": total_memories,
                "expired_memories": expired_memories,
                "active_memories": total_memories - expired_memories,
                "total_access_count": total_access_count,
                "average_access_count": total_access_count / total_memories if total_memories > 0 else 0,
                "oldest_memory": oldest_memory,
                "newest_memory": newest_memory,
            }
    
    async def search_memories(
        self,
        session_id: str,
        query: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Search memories by content.
        
        Args:
            session_id: Session ID
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching memories
        """
        async with self._lock:
            if session_id not in self._memories:
                return []
            
            query_lower = query.lower()
            matching_memories = []
            
            for key, memory_item in self._memories[session_id].items():
                # Check if expired
                if memory_item["expires_at"] and datetime.utcnow() > memory_item["expires_at"]:
                    continue
                
                # Search in value (convert to string for searching)
                value_str = str(memory_item["value"]).lower()
                if query_lower in value_str:
                    matching_memories.append({
                        "key": key,
                        "value": memory_item["value"],
                        "created_at": memory_item["created_at"],
                        "access_count": memory_item["access_count"],
                        "last_accessed": memory_item["last_accessed"],
                    })
            
            if limit:
                matching_memories = matching_memories[:limit]
            
            return matching_memories
    
    async def export_memories(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Export all memories for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            Exported memories or None if session not found
        """
        async with self._lock:
            if session_id not in self._memories:
                return None
            
            memories = {}
            for key, memory_item in self._memories[session_id].items():
                # Skip expired memories
                if memory_item["expires_at"] and datetime.utcnow() > memory_item["expires_at"]:
                    continue
                
                memories[key] = {
                    "value": memory_item["value"],
                    "created_at": memory_item["created_at"].isoformat(),
                    "expires_at": memory_item["expires_at"].isoformat() if memory_item["expires_at"] else None,
                    "access_count": memory_item["access_count"],
                    "last_accessed": memory_item["last_accessed"].isoformat(),
                }
            
            return {
                "session_id": session_id,
                "exported_at": datetime.utcnow().isoformat(),
                "memories": memories,
            }
    
    async def import_memories(self, session_id: str, memories_data: Dict[str, Any]) -> bool:
        """
        Import memories for a session.
        
        Args:
            session_id: Session ID
            memories_data: Memories data to import
            
        Returns:
            True if memories were imported
        """
        try:
            async with self._lock:
                if session_id not in self._memories:
                    self._memories[session_id] = {}
                
                for key, memory_data in memories_data.get("memories", {}).items():
                    memory_item = {
                        "value": memory_data["value"],
                        "created_at": datetime.fromisoformat(memory_data["created_at"]),
                        "expires_at": datetime.fromisoformat(memory_data["expires_at"]) if memory_data["expires_at"] else None,
                        "access_count": memory_data["access_count"],
                        "last_accessed": datetime.fromisoformat(memory_data["last_accessed"]),
                    }
                    
                    self._memories[session_id][key] = memory_item
            
            logger.info(f"Imported memories for session: {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to import memories for session {session_id}: {e}")
            return False
