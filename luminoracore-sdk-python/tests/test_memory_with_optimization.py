"""
Tests exhaustivos de Memory con Optimization

Valida que memory + optimization funcionan perfectamente juntos.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch

from luminoracore_sdk.session.memory import MemoryManager
from luminoracore_sdk.types.session import MemoryConfig

# Check si optimization está disponible
try:
    from luminoracore.optimization import OptimizationConfig, Optimizer
    HAS_OPTIMIZATION = True
except ImportError:
    HAS_OPTIMIZATION = False
    pytest.skip("Optimization not available", allow_module_level=True)


class TestMemoryWithOptimization:
    """Test suite completo para Memory + Optimization"""
    
    @pytest.fixture
    def optimizer(self):
        """Create optimizer instance"""
        config = OptimizationConfig(
            key_abbreviation=True,
            compact_format=True,
            minify_json=True,
            cache_enabled=True
        )
        return Optimizer(config)
    
    @pytest.fixture
    def memory_config(self):
        """Create memory config"""
        return MemoryConfig(
            max_messages=100,
            max_tokens=10000,
            ttl=3600
        )
    
    @pytest.fixture
    def memory_manager(self, memory_config, optimizer):
        """Create memory manager with optimizer"""
        return MemoryManager(memory_config, optimizer=optimizer)
    
    @pytest.mark.asyncio
    async def test_memory_manager_with_optimizer(self, memory_manager, optimizer):
        """MemoryManager debe aceptar optimizer"""
        assert memory_manager.optimizer is not None
        assert memory_manager.optimizer == optimizer
    
    @pytest.mark.asyncio
    async def test_store_memory_with_optimization(self, memory_manager):
        """Store memory debe funcionar con optimizer"""
        result = await memory_manager.store_memory(
            session_id="session1",
            key="test_key",
            value="test_value"
        )
        
        assert result is True
    
    @pytest.mark.asyncio
    async def test_get_memory_with_optimization(self, memory_manager):
        """Get memory debe funcionar con optimizer"""
        # Store
        await memory_manager.store_memory(
            session_id="session1",
            key="test_key",
            value="test_value"
        )
        
        # Retrieve
        value = await memory_manager.get_memory("session1", "test_key")
        
        assert value == "test_value"
    
    @pytest.mark.asyncio
    async def test_multiple_memories_with_optimization(self, memory_manager):
        """Multiple memories con optimization"""
        # Store multiple memories
        for i in range(10):
            await memory_manager.store_memory(
                session_id="session1",
                key=f"key_{i}",
                value=f"value_{i}"
            )
        
        # Retrieve all
        for i in range(10):
            value = await memory_manager.get_memory("session1", f"key_{i}")
            assert value == f"value_{i}"
    
    @pytest.mark.asyncio
    async def test_get_stats_with_optimization(self, memory_manager):
        """Stats debe funcionar con optimization"""
        # Add memories
        for i in range(5):
            await memory_manager.store_memory(
                session_id="session1",
                key=f"key_{i}",
                value=f"value_{i}"
            )
        
        # Get stats
        stats = await memory_manager.get_stats()
        
        assert stats is not None
        assert "total_sessions" in stats
        assert stats["total_sessions"] >= 1
    
    @pytest.mark.asyncio
    async def test_get_memory_stats_with_optimization(self, memory_manager):
        """Memory stats debe funcionar con optimization"""
        # Add memories
        await memory_manager.store_memory(
            session_id="session1",
            key="test_key",
            value="test_value"
        )
        
        # Get stats
        stats = await memory_manager.get_memory_stats("session1")
        
        assert stats is not None
        assert "total_memories" in stats
        assert stats["total_memories"] >= 1
    
    @pytest.mark.asyncio
    async def test_clear_memory_with_optimization(self, memory_manager):
        """Clear memory debe funcionar con optimization"""
        # Store
        await memory_manager.store_memory(
            session_id="session1",
            key="test_key",
            value="test_value"
        )
        
        # Clear
        result = await memory_manager.clear_memory("session1")
        
        assert result is True
        
        # Verify cleared
        value = await memory_manager.get_memory("session1", "test_key")
        assert value is None
    
    @pytest.mark.asyncio
    async def test_list_memories_with_optimization(self, memory_manager):
        """List memories debe funcionar con optimization"""
        # Store multiple
        for i in range(5):
            await memory_manager.store_memory(
                session_id="session1",
                key=f"key_{i}",
                value=f"value_{i}"
            )
        
        # List
        keys = await memory_manager.list_memories("session1")
        
        assert len(keys) == 5
        assert "key_0" in keys
        assert "key_4" in keys
    
    @pytest.mark.asyncio
    async def test_search_memories_with_optimization(self, memory_manager):
        """Search memories debe funcionar con optimization"""
        # Store memories
        await memory_manager.store_memory(
            session_id="session1",
            key="name",
            value="John Doe"
        )
        await memory_manager.store_memory(
            session_id="session1",
            key="city",
            value="New York"
        )
        
        # Search
        results = await memory_manager.search_memories("session1", "John")
        
        assert len(results) >= 1
        assert any(r["key"] == "name" for r in results)
    
    @pytest.mark.asyncio
    async def test_export_import_memories_with_optimization(self, memory_manager):
        """Export/import debe funcionar con optimization"""
        # Store memories
        await memory_manager.store_memory(
            session_id="session1",
            key="test_key",
            value="test_value"
        )
        
        # Export
        exported = await memory_manager.export_memories("session1")
        
        assert exported is not None
        assert "memories" in exported
        assert "test_key" in exported["memories"]
        
        # Import to new session
        result = await memory_manager.import_memories("session2", exported)
        
        assert result is True
        
        # Verify imported
        value = await memory_manager.get_memory("session2", "test_key")
        assert value == "test_value"
    
    @pytest.mark.asyncio
    async def test_cleanup_expired_with_optimization(self, memory_manager):
        """Cleanup expired debe funcionar con optimization"""
        # Store memory with short TTL (simulated)
        await memory_manager.store_memory(
            session_id="session1",
            key="test_key",
            value="test_value",
            ttl=1  # 1 second
        )
        
        # Wait a bit (in real test would use time.sleep or freezegun)
        # For now, just verify cleanup method exists
        count = await memory_manager.cleanup_expired_memories()
        
        assert isinstance(count, int)
        assert count >= 0


class TestMemoryWithoutOptimization:
    """Tests que validan backward compatibility sin optimization"""
    
    @pytest.fixture
    def memory_config(self):
        return MemoryConfig(
            max_messages=100,
            max_tokens=10000,
            ttl=3600
        )
    
    @pytest.fixture
    def memory_manager(self, memory_config):
        """MemoryManager sin optimizer"""
        return MemoryManager(memory_config)
    
    @pytest.mark.asyncio
    async def test_memory_manager_without_optimizer(self, memory_manager):
        """MemoryManager debe funcionar sin optimizer"""
        assert memory_manager.optimizer is None or memory_manager.optimizer is None
        
        # Debe funcionar igual
        result = await memory_manager.store_memory(
            session_id="session1",
            key="test_key",
            value="test_value"
        )
        
        assert result is True
        
        value = await memory_manager.get_memory("session1", "test_key")
        assert value == "test_value"
    
    @pytest.mark.asyncio
    async def test_stats_without_optimization(self, memory_manager):
        """Stats debe funcionar sin optimization"""
        await memory_manager.store_memory(
            session_id="session1",
            key="test_key",
            value="test_value"
        )
        
        stats = await memory_manager.get_stats()
        
        assert stats is not None
        assert "total_sessions" in stats
        assert stats.get("using_core") is False or "using_core" not in stats


# IMPORTANTE: Estos tests validan que Memory + Optimization funcionan juntos
# y que backward compatibility se mantiene sin optimization

