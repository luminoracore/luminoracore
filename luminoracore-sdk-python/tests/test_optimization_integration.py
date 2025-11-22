"""
Tests de integración para optimization del Core en SDK

Valida que SDK usa correctamente el optimizer del Core.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch

from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types.session import StorageConfig, MemoryConfig, StorageType


# Check si optimization está disponible
try:
    from luminoracore.optimization import OptimizationConfig, Optimizer
    HAS_OPTIMIZATION = True
except ImportError:
    HAS_OPTIMIZATION = False
    pytest.skip("luminoracore.optimization not available", allow_module_level=True)


class TestOptimizationIntegration:
    """Test suite para integration con Core optimizer"""
    
    @pytest.mark.asyncio
    async def test_client_with_optimization_config(self):
        """Client debe aceptar optimization_config"""
        opt_config = OptimizationConfig(
            key_abbreviation=True,
            compact_format=True,
            cache_enabled=True
        )
        
        client = LuminoraCoreClient(
            storage_config=StorageConfig(storage_type=StorageType.MEMORY),
            optimization_config=opt_config
        )
        await client.initialize()
        
        # Verificar optimizer está configurado
        assert client.optimizer is not None
        assert isinstance(client.optimizer, Optimizer)
        
        await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_client_without_optimization(self):
        """Client debe funcionar sin optimization (backward compat)"""
        client = LuminoraCoreClient(
            storage_config=StorageConfig(storage_type=StorageType.MEMORY)
        )
        await client.initialize()
        
        # Sin optimization config, optimizer debe ser None
        assert client.optimizer is None
        
        await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_storage_wrapped_with_optimizer(self):
        """Storage debe estar wrapped cuando optimization habilitado"""
        from luminoracore_sdk.session.storage import OptimizedStorageWrapper
        
        opt_config = OptimizationConfig(
            key_abbreviation=True,
            cache_enabled=True
        )
        
        client = LuminoraCoreClient(
            storage_config=StorageConfig(storage_type=StorageType.MEMORY),
            optimization_config=opt_config
        )
        await client.initialize()
        
        # Storage debe ser OptimizedStorageWrapper
        assert isinstance(client.storage, OptimizedStorageWrapper)
        
        await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_get_optimization_stats(self):
        """Client debe retornar optimization stats"""
        opt_config = OptimizationConfig(
            key_abbreviation=True,
            cache_enabled=True
        )
        
        client = LuminoraCoreClient(
            storage_config=StorageConfig(storage_type=StorageType.MEMORY),
            optimization_config=opt_config
        )
        await client.initialize()
        
        # Get stats
        stats = await client.get_optimization_stats()
        
        assert stats is not None
        assert stats["enabled"] is True
        assert "config" in stats
        assert stats["config"]["key_abbreviation"] is True
        
        await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_optimization_stats_when_disabled(self):
        """Stats debe retornar None cuando optimization disabled"""
        client = LuminoraCoreClient(
            storage_config=StorageConfig(storage_type=StorageType.MEMORY)
        )
        await client.initialize()
        
        stats = await client.get_optimization_stats()
        assert stats is None
        
        await client.cleanup()


class TestOptimizedStorageWrapper:
    """Tests para OptimizedStorageWrapper"""
    
    @pytest.fixture
    def mock_storage(self):
        """Mock storage"""
        from luminoracore_sdk.session.storage import InMemoryStorage
        from luminoracore_sdk.types.session import StorageConfig, StorageType
        
        storage = InMemoryStorage(StorageConfig(storage_type=StorageType.MEMORY))
        return storage
    
    @pytest.fixture
    def mock_optimizer(self):
        """Mock optimizer"""
        optimizer = Mock()
        optimizer.config = Mock()
        optimizer.config.key_abbreviation = True
        optimizer.config.compact_format = True
        optimizer.config.minify_json = True
        optimizer.config.cache_enabled = True
        optimizer.compress = Mock(side_effect=lambda x: {"compressed": x})
        optimizer.expand = Mock(side_effect=lambda x: x.get("compressed", x) if isinstance(x, dict) and "compressed" in x else x)
        return optimizer
    
    @pytest.mark.asyncio
    async def test_wrapper_compresses_on_save(self, mock_storage, mock_optimizer):
        """Wrapper debe comprimir al guardar"""
        from luminoracore_sdk.session.storage import OptimizedStorageWrapper
        
        wrapper = OptimizedStorageWrapper(mock_storage, mock_optimizer)
        
        session_data = {"key": "value", "test": "data"}
        result = await wrapper.save_session("test_session", session_data)
        
        # Verificar que compress fue llamado
        mock_optimizer.compress.assert_called_once()
        
        # Verificar que save fue exitoso
        assert result is True
    
    @pytest.mark.asyncio
    async def test_wrapper_expands_on_load(self, mock_storage, mock_optimizer):
        """Wrapper debe expandir al leer"""
        from luminoracore_sdk.session.storage import OptimizedStorageWrapper
        
        # Primero guardar con compresión
        wrapper = OptimizedStorageWrapper(mock_storage, mock_optimizer)
        session_data = {"key": "value", "test": "data"}
        await wrapper.save_session("test_session", session_data)
        
        # Resetear mock para verificar expand
        mock_optimizer.expand.reset_mock()
        
        # Cargar sesión
        result = await wrapper.load_session("test_session")
        
        # Verificar que expand fue llamado
        mock_optimizer.expand.assert_called()
        
        # Verificar que resultado no es None
        assert result is not None


# IMPORTANTE: Estos tests validan integration con Core

