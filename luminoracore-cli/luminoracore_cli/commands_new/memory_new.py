"""
New Memory Commands
CLI commands that use core directly
"""

import asyncio
from typing import Dict, List, Optional, Any
import click
from datetime import datetime

# Import from core directly
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'luminoracore'))

from luminoracore import PersonalityEngine, MemorySystem, EvolutionEngine, InMemoryStorage
from luminoracore.interfaces import StorageInterface


class MemoryCommandNew:
    """New memory command that uses core directly"""
    
    def __init__(self, storage_config: Optional[Dict] = None):
        """Initialize memory command with core components"""
        # Initialize core components
        self.personality_engine = PersonalityEngine()
        self.evolution_engine = EvolutionEngine()
        
        # Set up storage
        if storage_config:
            self.storage = self._create_storage_from_config(storage_config)
        else:
            self.storage = InMemoryStorage()
        
        # Initialize memory system
        self.memory_system = MemorySystem(self.storage)
        
        # Set evolution engine in personality engine
        self.personality_engine.evolution_engine = self.evolution_engine
    
    def _create_storage_from_config(self, config: Dict) -> StorageInterface:
        """Create storage from configuration"""
        storage_type = config.get('storage_type', 'memory')
        
        if storage_type == 'memory':
            return InMemoryStorage()
        else:
            # For now, default to in-memory
            # In the future, this would create other storage types
            return InMemoryStorage()
    
    async def list_facts(self, user_id: str, category: Optional[str] = None) -> List[Dict]:
        """List facts for a user"""
        return await self.storage.get_facts(user_id, category)
    
    async def list_episodes(self, user_id: str, min_importance: Optional[float] = None, 
                           limit: Optional[int] = None) -> List[Dict]:
        """List episodes for a user"""
        return await self.storage.get_episodes(user_id, min_importance, limit)
    
    async def list_affinities(self, user_id: str) -> List[Dict]:
        """List affinities for a user"""
        return await self.storage.get_all_affinities(user_id)
    
    async def search_facts(self, user_id: str, query: str, limit: Optional[int] = None) -> List[Dict]:
        """Search facts for a user"""
        return await self.storage.search_facts(user_id, query, limit)
    
    async def search_episodes(self, user_id: str, query: str, limit: Optional[int] = None) -> List[Dict]:
        """Search episodes for a user"""
        return await self.storage.search_episodes(user_id, query, limit)
    
    async def get_user_context(self, user_id: str) -> Dict:
        """Get comprehensive user context"""
        return await self.memory_system.get_user_context(user_id)
    
    async def get_user_stats(self, user_id: str) -> Dict:
        """Get user statistics"""
        return await self.storage.get_user_stats(user_id)
    
    async def get_memory_stats(self, user_id: str) -> Dict:
        """Get memory statistics"""
        return await self.memory_system.get_memory_stats(user_id)
    
    async def cleanup_old_data(self, days_old: int = 365) -> int:
        """Clean up old data"""
        return await self.storage.cleanup_old_data(days_old)
    
    async def health_check(self) -> Dict:
        """Check system health"""
        return await self.storage.health_check()


@click.group()
def memory_new():
    """New memory management commands using core"""
    pass


@memory_new.command()
@click.option('--user-id', required=True, help='User ID')
@click.option('--category', help='Filter by category')
def list_facts(user_id: str, category: Optional[str]):
    """List facts for a user"""
    async def _list_facts():
        command = MemoryCommandNew()
        facts = await command.list_facts(user_id, category)
        
        if not facts:
            click.echo("No facts found")
            return
        
        click.echo(f"Found {len(facts)} facts:")
        for fact in facts:
            click.echo(f"  {fact['category']}.{fact['key']}: {fact['value']} (confidence: {fact['confidence']})")
    
    asyncio.run(_list_facts())


@memory_new.command()
@click.option('--user-id', required=True, help='User ID')
@click.option('--min-importance', type=float, help='Minimum importance')
@click.option('--limit', type=int, help='Limit results')
def list_episodes(user_id: str, min_importance: Optional[float], limit: Optional[int]):
    """List episodes for a user"""
    async def _list_episodes():
        command = MemoryCommandNew()
        episodes = await command.list_episodes(user_id, min_importance, limit)
        
        if not episodes:
            click.echo("No episodes found")
            return
        
        click.echo(f"Found {len(episodes)} episodes:")
        for episode in episodes:
            click.echo(f"  {episode['title']}: {episode['summary']} (importance: {episode['importance']})")
    
    asyncio.run(_list_episodes())


@memory_new.command()
@click.option('--user-id', required=True, help='User ID')
def list_affinities(user_id: str):
    """List affinities for a user"""
    async def _list_affinities():
        command = MemoryCommandNew()
        affinities = await command.list_affinities(user_id)
        
        if not affinities:
            click.echo("No affinities found")
            return
        
        click.echo(f"Found {len(affinities)} affinities:")
        for affinity in affinities:
            click.echo(f"  {affinity['personality_name']}: {affinity['level']} ({affinity['points']} points)")
    
    asyncio.run(_list_affinities())


@memory_new.command()
@click.option('--user-id', required=True, help='User ID')
@click.option('--query', required=True, help='Search query')
@click.option('--limit', type=int, help='Limit results')
def search_facts(user_id: str, query: str, limit: Optional[int]):
    """Search facts for a user"""
    async def _search_facts():
        command = MemoryCommandNew()
        facts = await command.search_facts(user_id, query, limit)
        
        if not facts:
            click.echo("No facts found")
            return
        
        click.echo(f"Found {len(facts)} facts:")
        for fact in facts:
            click.echo(f"  {fact['category']}.{fact['key']}: {fact['value']}")
    
    asyncio.run(_search_facts())


@memory_new.command()
@click.option('--user-id', required=True, help='User ID')
@click.option('--query', required=True, help='Search query')
@click.option('--limit', type=int, help='Limit results')
def search_episodes(user_id: str, query: str, limit: Optional[int]):
    """Search episodes for a user"""
    async def _search_episodes():
        command = MemoryCommandNew()
        episodes = await command.search_episodes(user_id, query, limit)
        
        if not episodes:
            click.echo("No episodes found")
            return
        
        click.echo(f"Found {len(episodes)} episodes:")
        for episode in episodes:
            click.echo(f"  {episode['title']}: {episode['summary']}")
    
    asyncio.run(_search_episodes())


@memory_new.command()
@click.option('--user-id', required=True, help='User ID')
def get_context(user_id: str):
    """Get comprehensive user context"""
    async def _get_context():
        command = MemoryCommandNew()
        context = await command.get_user_context(user_id)
        
        click.echo(f"User Context for {user_id}:")
        click.echo(f"  Facts: {len(context.get('facts', []))}")
        click.echo(f"  Episodes: {len(context.get('episodes', []))}")
        click.echo(f"  Affinities: {len(context.get('affinities', []))}")
        click.echo(f"  Stats: {context.get('stats', {})}")
    
    asyncio.run(_get_context())


@memory_new.command()
@click.option('--user-id', required=True, help='User ID')
def get_stats(user_id: str):
    """Get user statistics"""
    async def _get_stats():
        command = MemoryCommandNew()
        stats = await command.get_user_stats(user_id)
        
        click.echo(f"User Statistics for {user_id}:")
        click.echo(f"  Fact Count: {stats.get('fact_count', 0)}")
        click.echo(f"  Episode Count: {stats.get('episode_count', 0)}")
        click.echo(f"  Affinity Count: {stats.get('affinity_count', 0)}")
        click.echo(f"  Total Points: {stats.get('total_points', 0)}")
    
    asyncio.run(_get_stats())


@memory_new.command()
@click.option('--days-old', type=int, default=365, help='Days old threshold')
def cleanup(days_old: int):
    """Clean up old data"""
    async def _cleanup():
        command = MemoryCommandNew()
        cleaned_count = await command.cleanup_old_data(days_old)
        
        click.echo(f"Cleaned up {cleaned_count} old records")
    
    asyncio.run(_cleanup())


@memory_new.command()
def health():
    """Check system health"""
    async def _health():
        command = MemoryCommandNew()
        health_info = await command.health_check()
        
        click.echo(f"System Health: {health_info.get('status', 'unknown')}")
        click.echo(f"Total Users: {health_info.get('total_users', 0)}")
        click.echo(f"Total Facts: {health_info.get('total_facts', 0)}")
        click.echo(f"Total Episodes: {health_info.get('total_episodes', 0)}")
        click.echo(f"Total Affinities: {health_info.get('total_affinities', 0)}")
    
    asyncio.run(_health())
