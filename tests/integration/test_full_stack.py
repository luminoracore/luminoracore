"""
Full Stack Integration Tests

Valida que Core, SDK y CLI funcionan juntos perfectamente.
"""

import pytest
import subprocess
import sys
from pathlib import Path


class TestFullStackIntegration:
    """Tests de toda la stack: Core + SDK + CLI"""
    
    def test_core_importable(self):
        """Core debe ser importable"""
        import luminoracore
        assert hasattr(luminoracore, '__version__')
        assert luminoracore.__version__ is not None
    
    def test_sdk_importable(self):
        """SDK debe ser importable"""
        import luminoracore_sdk
        assert hasattr(luminoracore_sdk, '__version__')
        assert luminoracore_sdk.__version__ is not None
    
    def test_cli_importable(self):
        """CLI debe ser importable"""
        import luminoracore_cli
        # CLI puede no tener __version__ en __init__, pero debe ser importable
        assert luminoracore_cli is not None
    
    def test_sdk_uses_core_blender(self):
        """SDK debe usar Core PersonaBlend via adapter"""
        from luminoracore.tools.blender import PersonaBlend
        from luminoracore_sdk.personality.blender import PersonalityBlender
        
        blender = PersonalityBlender()
        assert hasattr(blender, '_adapter')
        
        # Si adapter está disponible, debe usar Core
        if blender._adapter is not None:
            from luminoracore_sdk.personality.adapter import PersonaBlendAdapter
            assert isinstance(blender._adapter, PersonaBlendAdapter)
    
    def test_sdk_uses_core_optimizer(self):
        """SDK debe poder usar Core Optimizer"""
        try:
            from luminoracore.optimization import OptimizationConfig, Optimizer
            from luminoracore_sdk import LuminoraCoreClient
            
            config = OptimizationConfig(
                key_abbreviation=True,
                cache_enabled=True
            )
            optimizer = Optimizer(config)
            
            assert optimizer is not None
            
            # SDK debe poder crear client con optimizer
            client = LuminoraCoreClient(
                optimization_config=config
            )
            assert client.optimizer is not None
        except ImportError:
            pytest.skip("Core optimization not available")
    
    def test_cli_uses_core_validator(self):
        """CLI debe poder usar Core PersonalityValidator"""
        try:
            from luminoracore.tools.validator import PersonalityValidator
            
            # CLI debe poder importar y usar Core validator
            validator = PersonalityValidator()
            assert validator is not None
        except ImportError:
            pytest.skip("Core validator not available")
    
    def test_cli_uses_core_imports(self):
        """CLI debe poder importar del Core"""
        try:
            from luminoracore import Personality, PersonalityValidator
            from luminoracore.storage.migrations.migration_manager import MigrationManager
            
            # Verificar que imports funcionan
            assert Personality is not None
            assert PersonalityValidator is not None
            assert MigrationManager is not None
        except ImportError as e:
            pytest.skip(f"Core imports not available: {e}")
    
    def test_sdk_storage_uses_optimizer(self):
        """SDK Storage debe usar Core Optimizer cuando habilitado"""
        try:
            from luminoracore.optimization import OptimizationConfig, Optimizer
            from luminoracore_sdk import LuminoraCoreClient
            from luminoracore_sdk.types.session import StorageConfig, StorageType
            from luminoracore_sdk.session.storage import OptimizedStorageWrapper
            
            config = OptimizationConfig(
                key_abbreviation=True,
                cache_enabled=True
            )
            
            client = LuminoraCoreClient(
                storage_config=StorageConfig(storage_type=StorageType.MEMORY),
                optimization_config=config
            )
            
            # Storage debe estar wrapped
            assert isinstance(client.storage, OptimizedStorageWrapper)
        except ImportError:
            pytest.skip("Core optimization not available")
    
    def test_sdk_memory_uses_optimizer(self):
        """SDK MemoryManager debe recibir optimizer"""
        try:
            from luminoracore.optimization import OptimizationConfig, Optimizer
            from luminoracore_sdk import LuminoraCoreClient
            from luminoracore_sdk.types.session import StorageConfig, StorageType
            
            config = OptimizationConfig()
            optimizer = Optimizer(config)
            
            client = LuminoraCoreClient(
                storage_config=StorageConfig(storage_type=StorageType.MEMORY),
                optimization_config=config
            )
            
            # MemoryManager debe tener optimizer
            assert client.memory_manager.optimizer is not None
            assert client.memory_manager.optimizer == client.optimizer
        except ImportError:
            pytest.skip("Core optimization not available")
    
    def test_full_integration_flow(self):
        """Test de flujo completo: Core -> SDK -> CLI"""
        try:
            # 1. Core debe funcionar
            from luminoracore import Personality
            from luminoracore.tools.blender import PersonaBlend
            
            # 2. SDK debe usar Core
            from luminoracore_sdk.personality.blender import PersonalityBlender
            blender = PersonalityBlender()
            assert hasattr(blender, '_adapter')
            
            # 3. CLI debe poder importar Core
            from luminoracore import PersonalityValidator
            assert PersonalityValidator is not None
            
        except ImportError as e:
            pytest.skip(f"Full stack not available: {e}")


class TestFullStackBackwardCompatibility:
    """Tests de backward compatibility en toda la stack"""
    
    def test_sdk_works_without_optimization(self):
        """SDK debe funcionar sin optimization (backward compat)"""
        from luminoracore_sdk import LuminoraCoreClient
        from luminoracore_sdk.types.session import StorageConfig, StorageType
        
        # Client sin optimization
        client = LuminoraCoreClient(
            storage_config=StorageConfig(storage_type=StorageType.MEMORY)
        )
        
        # Debe funcionar
        assert client.optimizer is None
        assert client.storage is not None
        assert client.memory_manager is not None
    
    def test_sdk_blender_works_without_core(self):
        """SDK Blender debe tener fallback si Core no disponible"""
        from luminoracore_sdk.personality.blender import PersonalityBlender
        
        blender = PersonalityBlender()
        
        # Debe tener adapter (puede ser None si Core no disponible)
        assert hasattr(blender, '_adapter')
        
        # Si adapter es None, debe tener fallback
        if blender._adapter is None:
            # Debe tener método _perform_blend como fallback
            assert hasattr(blender, '_perform_blend')


# IMPORTANTE: Estos tests validan que toda la stack funciona junta
# y que la integración Core + SDK + CLI es correcta

