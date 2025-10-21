"""
Storage v1.1 Extensions for LuminoraCore SDK

Adds v1.1 table support to existing storage backends.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class StorageV11Extension(ABC):
    """
    Abstract extension for v1.1 storage methods
    
    Storage implementations can inherit from both SessionStorage and this
    to provide v1.1 functionality.
    """
    
    # AFFINITY METHODS
    @abstractmethod
    async def save_affinity(
        self,
        user_id: str,
        personality_name: str,
        affinity_points: int,
        current_level: str,
        **kwargs
    ) -> bool:
        """Save or update user affinity"""
        pass
    
    @abstractmethod
    async def get_affinity(
        self,
        user_id: str,
        personality_name: str
    ) -> Optional[Dict[str, Any]]:
        """Get user affinity data"""
        pass
    
    # FACT METHODS
    @abstractmethod
    async def save_fact(
        self,
        user_id: str,
        category: str,
        key: str,
        value: Any,
        **kwargs
    ) -> bool:
        """Save a user fact"""
        pass
    
    @abstractmethod
    async def get_facts(
        self,
        user_id: str,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get user facts, optionally filtered by category"""
        pass
    
    # EPISODE METHODS
    @abstractmethod
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
        """Save an episode"""
        pass
    
    @abstractmethod
    async def get_episodes(
        self,
        user_id: str,
        min_importance: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Get episodes, optionally filtered by importance"""
        pass
    
    # MOOD METHODS
    @abstractmethod
    async def save_mood(
        self,
        session_id: str,
        user_id: str,
        current_mood: str,
        mood_intensity: float = 1.0
    ) -> bool:
        """Save current mood state"""
        pass
    
    @abstractmethod
    async def get_mood(
        self,
        session_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get current mood state"""
        pass
    
    # SESSION MANAGEMENT METHODS
    @abstractmethod
    async def save_session(
        self,
        session_id: str,
        user_id: str,
        personality_name: str,
        created_at: str,
        expires_at: str,
        last_activity: str,
        status: str,
        provider_config: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Save session information"""
        pass
    
    @abstractmethod
    async def get_session(
        self,
        session_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get session information"""
        pass
    
    @abstractmethod
    async def update_session_activity(
        self,
        session_id: str,
        last_activity: str
    ) -> bool:
        """Update session last activity"""
        pass
    
    @abstractmethod
    async def get_expired_sessions(self) -> List[str]:
        """Get list of expired session IDs"""
        pass
    
    @abstractmethod
    async def delete_session(
        self,
        session_id: str
    ) -> bool:
        """Delete session"""
        pass


class InMemoryStorageV11(StorageV11Extension):
    """In-memory implementation of v1.1 storage"""
    
    def __init__(self):
        """Initialize in-memory v1.1 storage"""
        self._affinity: Dict[str, Dict[str, Any]] = {}
        self._facts: Dict[str, List[Dict[str, Any]]] = {}
        self._episodes: Dict[str, List[Dict[str, Any]]] = {}
        self._moods: Dict[str, Dict[str, Any]] = {}
        self._snapshots: Dict[str, Dict[str, Any]] = {}
        self._sessions: Dict[str, Dict[str, Any]] = {}
    
    async def save_affinity(
        self,
        user_id: str,
        personality_name: str,
        affinity_points: int,
        current_level: str,
        **kwargs
    ) -> bool:
        """Save affinity in memory"""
        key = f"{user_id}:{personality_name}"
        self._affinity[key] = {
            "user_id": user_id,
            "personality_name": personality_name,
            "affinity_points": affinity_points,
            "current_level": current_level,
            "updated_at": datetime.now().isoformat(),
            **kwargs
        }
        return True
    
    async def get_affinity(
        self,
        user_id: str,
        personality_name: str
    ) -> Optional[Dict[str, Any]]:
        """Get affinity from memory"""
        key = f"{user_id}:{personality_name}"
        return self._affinity.get(key)
    
    async def save_fact(
        self,
        user_id: str,
        category: str,
        key: str,
        value: Any,
        **kwargs
    ) -> bool:
        """Save fact in memory"""
        if user_id not in self._facts:
            self._facts[user_id] = []
        
        # Update if exists, otherwise append
        fact_dict = {
            "user_id": user_id,
            "category": category,
            "key": key,
            "value": value,
            "updated_at": datetime.now().isoformat(),
            **kwargs
        }
        
        # Replace existing fact with same key
        self._facts[user_id] = [
            f for f in self._facts[user_id]
            if not (f["category"] == category and f["key"] == key)
        ]
        self._facts[user_id].append(fact_dict)
        
        return True
    
    async def get_facts(
        self,
        user_id: str,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get facts from memory"""
        facts = self._facts.get(user_id, [])
        
        if category:
            return [f for f in facts if f["category"] == category]
        
        return facts
    
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
        """Save episode in memory"""
        if user_id not in self._episodes:
            self._episodes[user_id] = []
        
        episode_dict = {
            "user_id": user_id,
            "episode_type": episode_type,
            "title": title,
            "summary": summary,
            "importance": importance,
            "sentiment": sentiment,
            "timestamp": kwargs.get("timestamp", datetime.now().isoformat()),
            **kwargs
        }
        
        self._episodes[user_id].append(episode_dict)
        return True
    
    async def get_episodes(
        self,
        user_id: str,
        min_importance: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Get episodes from memory"""
        episodes = self._episodes.get(user_id, [])
        
        if min_importance is not None:
            return [e for e in episodes if e["importance"] >= min_importance]
        
        return episodes
    
    async def save_mood(
        self,
        session_id: str,
        user_id: str,
        current_mood: str,
        mood_intensity: float = 1.0
    ) -> bool:
        """Save mood in memory"""
        self._moods[session_id] = {
            "session_id": session_id,
            "user_id": user_id,
            "current_mood": current_mood,
            "mood_intensity": mood_intensity,
            "updated_at": datetime.now().isoformat()
        }
        return True
    
    async def get_mood(
        self,
        session_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get mood from memory"""
        return self._moods.get(session_id)
    
    # MOOD MANAGEMENT METHODS
    
    async def save_mood(
        self,
        user_id: str,
        mood_data: Dict[str, Any]
    ) -> bool:
        """Save mood data"""
        try:
            mood_key = f"{user_id}_mood_{mood_data.get('created_at', 'default')}"
            self._moods[mood_key] = mood_data
            return True
        except Exception as e:
            logger.error(f"Error saving mood: {e}")
            return False
    
    async def get_moods(
        self,
        user_id: str,
        personality_name: Optional[str] = None,
        max_results: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get mood history for user"""
        try:
            moods = []
            for key, mood_data in self._moods.items():
                if key.startswith(f"{user_id}_mood_"):
                    if personality_name is None or mood_data.get('personality_name') == personality_name:
                        moods.append(mood_data)
            
            # Sort by created_at
            moods.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            
            if max_results:
                moods = moods[:max_results]
            
            return moods
        except Exception as e:
            logger.error(f"Error getting moods: {e}")
            return []
    
    async def get_mood_history(
        self,
        user_id: str,
        personality_name: Optional[str] = None,
        days: int = 7,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get mood history for user (alias for get_moods)"""
        return await self.get_moods(user_id, personality_name, limit)
    
    # SNAPSHOT MANAGEMENT METHODS
    
    async def save_snapshot(
        self,
        user_id: str,
        snapshot_id: str,
        snapshot_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Save snapshot data"""
        try:
            snapshot_key = f"{user_id}_snapshot_{snapshot_id}"
            snapshot_record = {
                "snapshot_id": snapshot_id,
                "user_id": user_id,
                "snapshot_data": snapshot_data,
                "metadata": metadata or {},
                "created_at": datetime.now().isoformat()
            }
            self._snapshots[snapshot_key] = snapshot_record
            return True
        except Exception as e:
            logger.error(f"Error saving snapshot: {e}")
            return False
    
    async def get_snapshots(
        self,
        user_id: str,
        max_results: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get all snapshots for user"""
        try:
            snapshots = []
            for key, snapshot_record in self._snapshots.items():
                if key.startswith(f"{user_id}_snapshot_"):
                    snapshots.append(snapshot_record)
            
            # Sort by created_at
            snapshots.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            
            if max_results:
                snapshots = snapshots[:max_results]
            
            return snapshots
        except Exception as e:
            logger.error(f"Error getting snapshots: {e}")
            return []
    
    async def get_snapshot_info(
        self,
        user_id: str,
        snapshot_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get snapshot information"""
        try:
            snapshot_key = f"{user_id}_snapshot_{snapshot_id}"
            return self._snapshots.get(snapshot_key)
        except Exception as e:
            logger.error(f"Error getting snapshot info: {e}")
            return None
    
    async def delete_snapshot(
        self,
        user_id: str,
        snapshot_id: str
    ) -> bool:
        """Delete snapshot"""
        try:
            snapshot_key = f"{user_id}_snapshot_{snapshot_id}"
            if snapshot_key in self._snapshots:
                del self._snapshots[snapshot_key]
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting snapshot: {e}")
            return False
    
    # SESSION MANAGEMENT METHODS
    async def save_session(
        self,
        session_id: str,
        user_id: str,
        personality_name: str,
        created_at: str,
        expires_at: str,
        last_activity: str,
        status: str,
        provider_config: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Save session information"""
        try:
            self._sessions[session_id] = {
                "session_id": session_id,
                "user_id": user_id,
                "personality_name": personality_name,
                "created_at": created_at,
                "expires_at": expires_at,
                "last_activity": last_activity,
                "status": status,
                "provider_config": provider_config
            }
            return True
        except Exception as e:
            logger.error(f"Error saving session: {e}")
            return False
    
    async def get_session(
        self,
        session_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get session information"""
        try:
            return self._sessions.get(session_id)
        except Exception as e:
            logger.error(f"Error getting session: {e}")
            return None
    
    async def update_session_activity(
        self,
        session_id: str,
        last_activity: str
    ) -> bool:
        """Update session last activity"""
        try:
            if session_id in self._sessions:
                self._sessions[session_id]["last_activity"] = last_activity
                return True
            return False
        except Exception as e:
            logger.error(f"Error updating session activity: {e}")
            return False
    
    async def get_expired_sessions(self) -> List[str]:
        """Get list of expired session IDs"""
        try:
            from datetime import datetime
            expired_sessions = []
            current_time = datetime.now()
            
            for session_id, session_data in self._sessions.items():
                expires_at_str = session_data.get("expires_at")
                if expires_at_str:
                    expires_at = datetime.fromisoformat(expires_at_str)
                    if current_time > expires_at:
                        expired_sessions.append(session_id)
            
            return expired_sessions
        except Exception as e:
            logger.error(f"Error getting expired sessions: {e}")
            return []
    
    async def delete_session(
        self,
        session_id: str
    ) -> bool:
        """Delete session"""
        try:
            if session_id in self._sessions:
                del self._sessions[session_id]
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting session: {e}")
            return False

