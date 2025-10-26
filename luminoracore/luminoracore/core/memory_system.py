"""
Memory System
Core memory management and retrieval system
"""

import asyncio
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from ..interfaces import MemoryInterface, StorageInterface


class MemorySystem(MemoryInterface):
    """Core memory system for managing user memories"""
    
    def __init__(self, storage: StorageInterface):
        self.storage = storage
        self.fact_extractor = None
        self.episode_manager = None
        self.affinity_tracker = None
    
    async def extract_facts(self, conversation: List[Dict], user_id: str) -> List[Dict]:
        """Extract facts from conversation"""
        if not self.fact_extractor:
            # Simple fact extraction for now
            return await self._simple_fact_extraction(conversation, user_id)
        
        return await self.fact_extractor.extract_facts(conversation, user_id)
    
    async def extract_episodes(self, conversation: List[Dict], user_id: str) -> List[Dict]:
        """Extract episodes from conversation"""
        if not self.episode_manager:
            # Simple episode extraction for now
            return await self._simple_episode_extraction(conversation, user_id)
        
        return await self.episode_manager.extract_episodes(conversation, user_id)
    
    async def get_relevant_memories(self, user_id: str, context: str, 
                                   memory_types: List[str] = None) -> List[Dict]:
        """Get relevant memories for context"""
        memories = []
        
        if memory_types is None:
            memory_types = ['facts', 'episodes', 'affinity']
        
        # Get facts
        if 'facts' in memory_types:
            facts = await self.storage.get_facts(user_id)
            memories.extend(facts)
        
        # Get episodes
        if 'episodes' in memory_types:
            episodes = await self.storage.get_episodes(user_id)
            memories.extend(episodes)
        
        # Get affinity
        if 'affinity' in memory_types:
            affinities = await self.storage.get_all_affinities(user_id)
            memories.extend(affinities)
        
        # Simple relevance scoring (would be more sophisticated in real implementation)
        relevant_memories = await self._score_relevance(memories, context)
        
        return relevant_memories
    
    async def update_affinity(self, user_id: str, personality_name: str, 
                             interaction_quality: str, points_delta: int) -> Dict:
        """Update affinity based on interaction"""
        return await self.storage.update_affinity(
            user_id, personality_name, points_delta, interaction_quality
        )
    
    async def get_user_context(self, user_id: str) -> Dict:
        """Get comprehensive user context"""
        context = {
            'user_id': user_id,
            'facts': await self.storage.get_facts(user_id),
            'episodes': await self.storage.get_episodes(user_id),
            'affinities': await self.storage.get_all_affinities(user_id),
            'stats': await self.storage.get_user_stats(user_id),
            'timestamp': datetime.now().isoformat()
        }
        
        return context
    
    async def search_memories(self, user_id: str, query: str, 
                             memory_types: List[str] = None) -> List[Dict]:
        """Search memories using semantic search"""
        if memory_types is None:
            memory_types = ['facts', 'episodes']
        
        results = []
        
        # Search facts
        if 'facts' in memory_types:
            fact_results = await self.storage.search_facts(user_id, query)
            results.extend(fact_results)
        
        # Search episodes
        if 'episodes' in memory_types:
            episode_results = await self.storage.search_episodes(user_id, query)
            results.extend(episode_results)
        
        return results
    
    async def get_memory_stats(self, user_id: str) -> Dict:
        """Get memory statistics for user"""
        stats = await self.storage.get_user_stats(user_id)
        
        # Add memory-specific stats
        stats['memory_types'] = {
            'facts': len(await self.storage.get_facts(user_id)),
            'episodes': len(await self.storage.get_episodes(user_id)),
            'affinities': len(await self.storage.get_all_affinities(user_id))
        }
        
        return stats
    
    async def cleanup_memories(self, user_id: str, days_old: int = 365) -> int:
        """Clean up old memories"""
        return await self.storage.cleanup_old_data(days_old)
    
    async def _simple_fact_extraction(self, conversation: List[Dict], user_id: str) -> List[Dict]:
        """Simple fact extraction implementation"""
        facts = []
        
        for message in conversation:
            if message.get('role') == 'user':
                content = message.get('content', '')
                
                # Simple fact extraction patterns
                if 'my name is' in content.lower():
                    name = content.lower().split('my name is')[1].strip()
                    facts.append({
                        'category': 'personal_info',
                        'key': 'name',
                        'value': name,
                        'confidence': 0.8,
                        'source': 'conversation',
                        'timestamp': datetime.now().isoformat()
                    })
                
                if 'i am from' in content.lower():
                    location = content.lower().split('i am from')[1].strip()
                    facts.append({
                        'category': 'personal_info',
                        'key': 'location',
                        'value': location,
                        'confidence': 0.8,
                        'source': 'conversation',
                        'timestamp': datetime.now().isoformat()
                    })
        
        return facts
    
    async def _simple_episode_extraction(self, conversation: List[Dict], user_id: str) -> List[Dict]:
        """Simple episode extraction implementation"""
        episodes = []
        
        # Group conversation into episodes
        current_episode = []
        episode_count = 0
        
        for message in conversation:
            current_episode.append(message)
            
            # Simple episode boundary detection
            if len(current_episode) >= 5:  # Arbitrary threshold
                episode_count += 1
                episodes.append({
                    'episode_type': 'conversation',
                    'title': f"Conversation Episode {episode_count}",
                    'summary': f"Conversation with {len(current_episode)} messages",
                    'importance': 0.5,
                    'sentiment': 'neutral',
                    'metadata': {
                        'message_count': len(current_episode),
                        'episode_number': episode_count
                    },
                    'timestamp': datetime.now().isoformat()
                })
                current_episode = []
        
        return episodes
    
    async def _score_relevance(self, memories: List[Dict], context: str) -> List[Dict]:
        """Score memory relevance to context"""
        # Simple relevance scoring
        scored_memories = []
        
        for memory in memories:
            score = 0.0
            
            # Simple keyword matching
            context_lower = context.lower()
            memory_text = str(memory).lower()
            
            # Count keyword matches
            keywords = context_lower.split()
            matches = sum(1 for keyword in keywords if keyword in memory_text)
            score = matches / len(keywords) if keywords else 0.0
            
            scored_memories.append({
                'memory': memory,
                'relevance_score': score
            })
        
        # Sort by relevance score
        scored_memories.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return scored_memories
