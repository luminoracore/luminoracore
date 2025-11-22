"""
End-to-End Integration Tests: SDK + Core

Tests completos que validan toda la stack funciona junta.
"""

import pytest
import asyncio

from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types.session import StorageConfig, MemoryConfig, StorageType
from luminoracore_sdk.types.provider import ProviderConfig
from luminoracore_sdk.types.personality import PersonalityData

# Check si Core está disponible
try:
    from luminoracore.optimization import OptimizationConfig, Optimizer
    from luminoracore.tools.blender import PersonaBlend
    HAS_CORE = True
except ImportError:
    HAS_CORE = False
    pytest.skip("Core not available", allow_module_level=True)


class TestSDKCoreE2E:
    """Tests E2E completos que validan SDK usa Core correctamente"""
    
    @pytest.mark.asyncio
    async def test_full_stack_with_optimization(self):
        """
        Test E2E: Client con optimization del Core
        
        CRÍTICO: Este test valida toda la arquitectura
        """
        # 1. Setup client con optimization
        opt_config = OptimizationConfig(
            key_abbreviation=True,
            compact_format=True,
            cache_enabled=True
        )
        
        client = LuminoraCoreClient(
            storage_config=StorageConfig(storage_type=StorageType.MEMORY),
            memory_config=MemoryConfig(max_messages=50),
            optimization_config=opt_config
        )
        
        await client.initialize()
        
        try:
            # 2. Verificar optimizer está activo
            assert client.optimizer is not None
            assert isinstance(client.optimizer, Optimizer)
            
            # 3. Verificar storage está wrapped
            from luminoracore_sdk.session.storage import OptimizedStorageWrapper
            assert isinstance(client.storage, OptimizedStorageWrapper)
            
            # 4. Test memory con optimization
            await client.memory_manager.store_memory(
                session_id="test_session",
                key="test_key",
                value="test_value"
            )
            
            value = await client.memory_manager.get_memory("test_session", "test_key")
            assert value == "test_value"
            
            # 5. Get stats
            stats = await client.get_optimization_stats()
            assert stats is not None
            assert stats["enabled"] is True
            assert "config" in stats
            assert stats["config"]["key_abbreviation"] is True
            
        finally:
            await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_personality_blending_uses_core(self):
        """Blending debe usar Core PersonaBlend via adapter"""
        client = LuminoraCoreClient()
        await client.initialize()
        
        try:
            # Verificar blender usa adapter
            assert hasattr(client.personality_blender, '_adapter')
            
            # Si adapter está disponible, debe ser PersonaBlendAdapter
            if client.personality_blender._adapter is not None:
                from luminoracore_sdk.personality.adapter import PersonaBlendAdapter
                assert isinstance(client.personality_blender._adapter, PersonaBlendAdapter)
            
            # Verificar que blender funciona
            # (sin personalidades reales, solo validar estructura)
            assert client.personality_blender is not None
            
        finally:
            await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_backward_compatibility_e2e(self):
        """
        E2E sin optimization (backward compat)
        
        CRÍTICO: Cliente v1.0 debe seguir funcionando
        """
        # Cliente SIN optimization
        client = LuminoraCoreClient(
            storage_config=StorageConfig(storage_type=StorageType.MEMORY)
        )
        
        await client.initialize()
        
        try:
            # Debe funcionar perfectamente sin optimization
            assert client.optimizer is None
            
            # Test funcionalidad básica
            await client.memory_manager.store_memory(
                session_id="test_session",
                key="test_key",
                value="test_value"
            )
            
            value = await client.memory_manager.get_memory("test_session", "test_key")
            assert value == "test_value"
            
            # Stats debe retornar None sin optimization
            stats = await client.get_optimization_stats()
            assert stats is None
            
        finally:
            await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_optimization_stats_e2e(self):
        """Stats de optimization deben funcionar end-to-end"""
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
        
        try:
            # Usar el cliente para generar actividad
            await client.memory_manager.store_memory(
                session_id="test_session",
                key="key1",
                value="value1"
            )
            
            await client.memory_manager.store_memory(
                session_id="test_session",
                key="key2",
                value="value2"
            )
            
            # Get stats
            stats = await client.get_optimization_stats()
            
            assert stats is not None
            assert stats["enabled"] is True
            assert "config" in stats
            assert "stats" in stats or "cache_stats" in stats
            
        finally:
            await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_storage_compression_e2e(self):
        """Storage debe comprimir/expandir datos correctamente"""
        opt_config = OptimizationConfig(
            key_abbreviation=True,
            compact_format=True,
            minify_json=True
        )
        
        client = LuminoraCoreClient(
            storage_config=StorageConfig(storage_type=StorageType.MEMORY),
            optimization_config=opt_config
        )
        
        await client.initialize()
        
        try:
            # Crear sesión
            session_id = "test_session_e2e"
            session_data = {
                "personality": "test_personality",
                "messages": [
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi there!"}
                ],
                "metadata": {"test": True}
            }
            
            # Guardar sesión (debe comprimir)
            result = await client.storage.save_session(session_id, session_data)
            assert result is True
            
            # Cargar sesión (debe expandir)
            loaded = await client.storage.load_session(session_id)
            
            assert loaded is not None
            assert loaded["personality"] == "test_personality"
            assert len(loaded["messages"]) == 2
            assert loaded["metadata"]["test"] is True
            
        finally:
            await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_memory_manager_with_optimizer_e2e(self):
        """MemoryManager debe usar optimizer cuando disponible"""
        opt_config = OptimizationConfig(
            key_abbreviation=True,
            cache_enabled=True
        )
        
        client = LuminoraCoreClient(
            storage_config=StorageConfig(storage_type=StorageType.MEMORY),
            optimization_config=opt_config
        )
        
        await client.initialize()
        
        try:
            # Verificar optimizer está pasado a memory manager
            assert client.memory_manager.optimizer is not None
            assert client.memory_manager.optimizer == client.optimizer
            
            # Test operaciones de memoria
            await client.memory_manager.store_memory(
                session_id="test_session",
                key="name",
                value="John Doe"
            )
            
            await client.memory_manager.store_memory(
                session_id="test_session",
                key="city",
                value="New York"
            )
            
            # Get stats
            stats = await client.memory_manager.get_stats()
            assert stats is not None
            assert stats["total_sessions"] >= 1
            
        finally:
            await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_full_workflow_with_optimization(self):
        """Workflow completo: Client -> Storage -> Memory -> Optimization"""
        opt_config = OptimizationConfig(
            key_abbreviation=True,
            compact_format=True,
            cache_enabled=True
        )
        
        client = LuminoraCoreClient(
            storage_config=StorageConfig(storage_type=StorageType.MEMORY),
            memory_config=MemoryConfig(max_messages=100),
            optimization_config=opt_config
        )
        
        await client.initialize()
        
        try:
            # 1. Crear sesión
            session_id = "workflow_test"
            
            # 2. Almacenar memoria
            await client.memory_manager.store_memory(
                session_id=session_id,
                key="user_preference",
                value="dark_mode"
            )
            
            # 3. Guardar sesión
            session_data = {
                "session_id": session_id,
                "personality": "test",
                "messages": []
            }
            await client.storage.save_session(session_id, session_data)
            
            # 4. Cargar sesión
            loaded = await client.storage.load_session(session_id)
            assert loaded is not None
            
            # 5. Recuperar memoria
            preference = await client.memory_manager.get_memory(session_id, "user_preference")
            assert preference == "dark_mode"
            
            # 6. Verificar stats
            opt_stats = await client.get_optimization_stats()
            assert opt_stats is not None
            
            mem_stats = await client.memory_manager.get_stats()
            assert mem_stats is not None
            
        finally:
            await client.cleanup()


class TestSDKCoreIntegration:
    """Tests de integración específicos SDK-Core"""
    
    def test_sdk_imports_core_optimizer(self):
        """SDK debe poder importar Core Optimizer"""
        from luminoracore.optimization import OptimizationConfig, Optimizer
        
        config = OptimizationConfig()
        optimizer = Optimizer(config)
        
        assert optimizer is not None
        assert optimizer.config is not None
    
    def test_sdk_imports_core_blender(self):
        """SDK debe poder importar Core PersonaBlend"""
        from luminoracore.tools.blender import PersonaBlend
        
        blender = PersonaBlend()
        assert blender is not None
    
    def test_adapter_uses_core_blender(self):
        """Adapter debe usar Core PersonaBlend"""
        try:
            from luminoracore_sdk.personality.adapter import PersonaBlendAdapter
            from luminoracore.tools.blender import PersonaBlend
            
            adapter = PersonaBlendAdapter()
            assert adapter._core_blender is not None
            assert isinstance(adapter._core_blender, PersonaBlend)
        except ImportError:
            pytest.skip("Core not available")
    
    def test_storage_wrapper_uses_optimizer(self):
        """OptimizedStorageWrapper debe usar Core Optimizer"""
        from luminoracore.optimization import OptimizationConfig, Optimizer
        from luminoracore_sdk.session.storage import OptimizedStorageWrapper, InMemoryStorage
        from luminoracore_sdk.types.session import StorageConfig, StorageType
        
        config = OptimizationConfig()
        optimizer = Optimizer(config)
        
        storage = InMemoryStorage(StorageConfig(storage_type=StorageType.MEMORY))
        wrapper = OptimizedStorageWrapper(storage, optimizer)
        
        assert wrapper._optimizer is not None
        assert wrapper._optimizer == optimizer


# IMPORTANTE: Estos tests validan que toda la stack funciona junta
# y que SDK usa Core correctamente

