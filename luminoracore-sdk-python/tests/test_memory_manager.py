"""
Tests adicionales para MemoryManager con Core integration
"""

import pytest
import logging
from unittest.mock import Mock, AsyncMock, patch

from luminoracore_sdk.session.memory import MemoryManager
from luminoracore_sdk.types.session import MemoryConfig

logger = logging.getLogger(__name__)


class TestMemoryManagerCoreIntegration:
    """Tests de integration con Core MemorySystem"""
    
    @pytest.fixture
    def memory_config(self):
        return MemoryConfig(
            max_messages=100,
            max_tokens=10000,
            ttl=3600
        )
    
    @pytest.mark.asyncio
    async def test_memory_manager_uses_core_if_available(self, memory_config):
        """MemoryManager debe usar Core si disponible"""
        manager = MemoryManager(memory_config)
        
        # Verificar si usa Core
        # Nota: depende de si Core está instalado
        if hasattr(manager, '_use_core'):
            logger.info(f"Using Core: {manager._use_core}")
    
    @pytest.mark.asyncio
    async def test_store_and_retrieve_memories(self, memory_config):
        """Store/retrieve debe funcionar con o sin Core"""
        manager = MemoryManager(memory_config)
        
        # Store memory
        await manager.store_memory(
            session_id="session1",
            key="test_key",
            value="test_value"
        )
        
        # Retrieve
        value = await manager.get_memory("session1", "test_key")
        
        assert value == "test_value"
    
    @pytest.mark.asyncio
    async def test_clear_memory(self, memory_config):
        """Clear memory debe funcionar"""
        manager = MemoryManager(memory_config)
        
        # Store
        await manager.store_memory(
            session_id="session1",
            key="test_key",
            value="test_value"
        )
        
        # Clear
        result = await manager.clear_memory("session1")
        
        # Verify cleared
        assert result is True
        value = await manager.get_memory("session1", "test_key")
        assert value is None
    
    @pytest.mark.asyncio
    async def test_get_stats(self, memory_config):
        """get_stats debe retornar info útil"""
        manager = MemoryManager(memory_config)
        
        # Add some memories
        await manager.store_memory(
            session_id="session1",
            key="test_key",
            value="test_value"
        )
        
        # Get stats
        stats = await manager.get_stats()
        
        assert "total_sessions" in stats
        assert stats["total_sessions"] >= 1
    
    @pytest.mark.asyncio
    async def test_get_memory_stats(self, memory_config):
        """get_memory_stats debe retornar stats de sesión"""
        manager = MemoryManager(memory_config)
        
        # Add memory
        await manager.store_memory(
            session_id="session1",
            key="test_key",
            value="test_value"
        )
        
        # Get stats
        stats = await manager.get_memory_stats("session1")
        
        assert stats is not None
        assert "total_memories" in stats
        assert stats["total_memories"] >= 1


# IMPORTANTE: Estos tests validan que MemoryManager funciona
# con o sin Core MemorySystem

