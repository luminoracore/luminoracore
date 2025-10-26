"""
Base Storage Implementation
Base implementation of storage interface
"""

import asyncio
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from ..interfaces import StorageInterface


class BaseStorage(StorageInterface):
    """Base storage implementation with common functionality"""
    
    def __init__(self):
        self.data: Dict[str, Any] = {
            'facts': {},
            'episodes': {},
            'affinities': {}
        }
        self.next_id = 1
    
    async def save_fact(self, user_id: str, category: str, key: str, value: Any, confidence: float = 0.8) -> bool:
        """Save a fact for a user"""
        try:
            fact_id = f"{user_id}_{category}_{key}"
            fact_data = {
                'id': fact_id,
                'user_id': user_id,
                'category': category,
                'key': key,
                'value': value,
                'confidence': confidence,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            if user_id not in self.data['facts']:
                self.data['facts'][user_id] = {}
            
            self.data['facts'][user_id][fact_id] = fact_data
            return True
        except Exception as e:
            print(f"Error saving fact: {e}")
            return False
    
    async def get_facts(self, user_id: str, category: Optional[str] = None) -> List[Dict]:
        """Get facts for a user, optionally filtered by category"""
        if user_id not in self.data['facts']:
            return []
        
        facts = list(self.data['facts'][user_id].values())
        
        if category:
            facts = [f for f in facts if f.get('category') == category]
        
        return facts
    
    async def update_fact(self, user_id: str, category: str, key: str, value: Any, confidence: float = 0.8) -> bool:
        """Update an existing fact"""
        fact_id = f"{user_id}_{category}_{key}"
        
        if user_id not in self.data['facts'] or fact_id not in self.data['facts'][user_id]:
            return await self.save_fact(user_id, category, key, value, confidence)
        
        self.data['facts'][user_id][fact_id]['value'] = value
        self.data['facts'][user_id][fact_id]['confidence'] = confidence
        self.data['facts'][user_id][fact_id]['updated_at'] = datetime.now().isoformat()
        
        return True
    
    async def delete_fact(self, user_id: str, category: str, key: str) -> bool:
        """Delete a fact"""
        fact_id = f"{user_id}_{category}_{key}"
        
        if user_id in self.data['facts'] and fact_id in self.data['facts'][user_id]:
            del self.data['facts'][user_id][fact_id]
            return True
        
        return False
    
    async def save_episode(self, user_id: str, episode_type: str, title: str, summary: str, 
                          importance: float = 0.5, sentiment: str = "neutral", 
                          metadata: Optional[Dict] = None) -> bool:
        """Save an episode for a user"""
        try:
            episode_id = f"episode_{self.next_id}"
            self.next_id += 1
            
            episode_data = {
                'id': episode_id,
                'user_id': user_id,
                'episode_type': episode_type,
                'title': title,
                'summary': summary,
                'importance': importance,
                'sentiment': sentiment,
                'metadata': metadata or {},
                'created_at': datetime.now().isoformat()
            }
            
            if user_id not in self.data['episodes']:
                self.data['episodes'][user_id] = []
            
            self.data['episodes'][user_id].append(episode_data)
            return True
        except Exception as e:
            print(f"Error saving episode: {e}")
            return False
    
    async def get_episodes(self, user_id: str, min_importance: Optional[float] = None, 
                          limit: Optional[int] = None) -> List[Dict]:
        """Get episodes for a user, optionally filtered by importance"""
        if user_id not in self.data['episodes']:
            return []
        
        episodes = self.data['episodes'][user_id].copy()
        
        if min_importance is not None:
            episodes = [e for e in episodes if e.get('importance', 0) >= min_importance]
        
        if limit is not None:
            episodes = episodes[:limit]
        
        return episodes
    
    async def update_episode(self, user_id: str, episode_id: str, **kwargs) -> bool:
        """Update an existing episode"""
        if user_id not in self.data['episodes']:
            return False
        
        for episode in self.data['episodes'][user_id]:
            if episode['id'] == episode_id:
                episode.update(kwargs)
                episode['updated_at'] = datetime.now().isoformat()
                return True
        
        return False
    
    async def delete_episode(self, user_id: str, episode_id: str) -> bool:
        """Delete an episode"""
        if user_id not in self.data['episodes']:
            return False
        
        for i, episode in enumerate(self.data['episodes'][user_id]):
            if episode['id'] == episode_id:
                del self.data['episodes'][user_id][i]
                return True
        
        return False
    
    async def update_affinity(self, user_id: str, personality_name: str, points_delta: int, 
                             interaction_type: str = "neutral") -> Dict:
        """Update affinity between user and personality"""
        affinity_key = f"{user_id}_{personality_name}"
        
        if user_id not in self.data['affinities']:
            self.data['affinities'][user_id] = {}
        
        if affinity_key not in self.data['affinities'][user_id]:
            self.data['affinities'][user_id][affinity_key] = {
                'user_id': user_id,
                'personality_name': personality_name,
                'points': 0,
                'level': 'stranger',
                'interaction_count': 0,
                'last_interaction': None,
                'created_at': datetime.now().isoformat()
            }
        
        affinity = self.data['affinities'][user_id][affinity_key]
        affinity['points'] += points_delta
        affinity['interaction_count'] += 1
        affinity['last_interaction'] = datetime.now().isoformat()
        affinity['updated_at'] = datetime.now().isoformat()
        
        # Update level based on points
        if affinity['points'] >= 100:
            affinity['level'] = 'intimate'
        elif affinity['points'] >= 50:
            affinity['level'] = 'close_friend'
        elif affinity['points'] >= 20:
            affinity['level'] = 'friend'
        elif affinity['points'] >= 5:
            affinity['level'] = 'acquaintance'
        else:
            affinity['level'] = 'stranger'
        
        return affinity.copy()
    
    async def get_affinity(self, user_id: str, personality_name: str) -> Optional[Dict]:
        """Get affinity between user and personality"""
        affinity_key = f"{user_id}_{personality_name}"
        
        if user_id in self.data['affinities'] and affinity_key in self.data['affinities'][user_id]:
            return self.data['affinities'][user_id][affinity_key].copy()
        
        return None
    
    async def get_all_affinities(self, user_id: str) -> List[Dict]:
        """Get all affinities for a user"""
        if user_id not in self.data['affinities']:
            return []
        
        return list(self.data['affinities'][user_id].values())
    
    async def search_facts(self, user_id: str, query: str, limit: Optional[int] = None) -> List[Dict]:
        """Search facts using semantic search"""
        facts = await self.get_facts(user_id)
        
        # Simple text search
        query_lower = query.lower()
        matching_facts = []
        
        for fact in facts:
            fact_text = f"{fact.get('key', '')} {fact.get('value', '')} {fact.get('category', '')}"
            if query_lower in fact_text.lower():
                matching_facts.append(fact)
        
        if limit is not None:
            matching_facts = matching_facts[:limit]
        
        return matching_facts
    
    async def search_episodes(self, user_id: str, query: str, limit: Optional[int] = None) -> List[Dict]:
        """Search episodes using semantic search"""
        episodes = await self.get_episodes(user_id)
        
        # Simple text search
        query_lower = query.lower()
        matching_episodes = []
        
        for episode in episodes:
            episode_text = f"{episode.get('title', '')} {episode.get('summary', '')}"
            if query_lower in episode_text.lower():
                matching_episodes.append(episode)
        
        if limit is not None:
            matching_episodes = matching_episodes[:limit]
        
        return matching_episodes
    
    async def get_user_stats(self, user_id: str) -> Dict:
        """Get statistics for a user"""
        facts = await self.get_facts(user_id)
        episodes = await self.get_episodes(user_id)
        affinities = await self.get_all_affinities(user_id)
        
        return {
            'user_id': user_id,
            'fact_count': len(facts),
            'episode_count': len(episodes),
            'affinity_count': len(affinities),
            'total_points': sum(a.get('points', 0) for a in affinities),
            'last_activity': datetime.now().isoformat()
        }
    
    async def cleanup_old_data(self, days_old: int = 365) -> int:
        """Clean up old data"""
        cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
        cleaned_count = 0
        
        # Clean up old episodes
        for user_id in self.data['episodes']:
            episodes = self.data['episodes'][user_id]
            original_count = len(episodes)
            
            self.data['episodes'][user_id] = [
                e for e in episodes 
                if datetime.fromisoformat(e.get('created_at', '1970-01-01')).timestamp() > cutoff_date
            ]
            
            cleaned_count += original_count - len(self.data['episodes'][user_id])
        
        return cleaned_count
    
    async def health_check(self) -> Dict:
        """Check storage health"""
        return {
            'status': 'healthy',
            'total_users': len(self.data['facts']),
            'total_facts': sum(len(facts) for facts in self.data['facts'].values()),
            'total_episodes': sum(len(episodes) for episodes in self.data['episodes'].values()),
            'total_affinities': sum(len(affinities) for affinities in self.data['affinities'].values()),
            'timestamp': datetime.now().isoformat()
        }
