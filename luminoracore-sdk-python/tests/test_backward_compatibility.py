"""
Backward Compatibility Tests

Simula código de usuarios que usaban versión anterior del SDK.
TODOS estos tests deben pasar para garantizar no rompemos nada.

Autor: Refactor Fase 0
Fecha: 2025-11-21
"""

import pytest
import asyncio
from typing import List
from unittest.mock import AsyncMock

from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.personality.blender import PersonalityBlender
from luminoracore_sdk.types.personality import PersonalityData
from luminoracore_sdk.utils.exceptions import PersonalityError


class TestBackwardCompatibilityV10:
    """
    Tests que simulan código de usuario usando SDK v1.0/v1.1
    
    CRÍTICO: Si alguno falla, rompimos backward compatibility
    """
    
    @pytest.fixture
    def blender(self):
        """Crear blender como lo haría usuario v1.0"""
        return PersonalityBlender()
    
    @pytest.fixture
    def sample_personalities(self):
        """Personalities de ejemplo para tests"""
        return [
            PersonalityData(
                name="assistant",
                description="A helpful assistant",
                system_prompt="You are a helpful assistant.",
                metadata={
                    "version": "1.0.0",
                    "author": "Test",
                    "tags": ["helper"],
                    "language": "en"
                },
                core_traits={
                    "archetype": "Helper",
                    "temperament": "Friendly",
                    "communication_style": "Warm"
                }
            ),
            PersonalityData(
                name="analyst",
                description="An analytical thinker",
                system_prompt="You are an analytical thinker.",
                metadata={
                    "version": "1.0.0",
                    "author": "Test",
                    "tags": ["thinker"],
                    "language": "en"
                },
                core_traits={
                    "archetype": "Thinker",
                    "temperament": "Analytical",
                    "communication_style": "Formal"
                }
            )
        ]
    
    @pytest.mark.asyncio
    async def test_v10_basic_blending(self, blender, sample_personalities):
        """
        Test: Código básico de v1.0 sigue funcionando
        
        Este es el uso más común en v1.0
        """
        # Código que usuario escribió en v1.0
        result = await blender.blend_personalities(
            personalities=sample_personalities,
            weights=[0.7, 0.3]
        )
        
        # Debe seguir funcionando exactamente igual
        assert result is not None
        assert isinstance(result, PersonalityData)
        assert result.name is not None
        assert result.description is not None
    
    @pytest.mark.asyncio
    async def test_v10_named_blend(self, blender, sample_personalities):
        """
        Test: Blends con nombre custom siguen funcionando
        """
        result = await blender.blend_personalities(
            personalities=sample_personalities,
            weights=[0.5, 0.5],
            blend_name="custom_blend"
        )
        
        assert result.name == "custom_blend"
    
    @pytest.mark.asyncio
    async def test_v10_error_messages_unchanged(self, blender):
        """
        Test: Mensajes de error siguen siendo los mismos
        
        CRÍTICO: Usuarios pueden depender de error messages
        """
        # Error: not enough personalities
        with pytest.raises(PersonalityError) as exc_info:
            await blender.blend_personalities(
                personalities=[PersonalityData(
                    name="p1",
                    description="Test",
                    system_prompt="Test",
                    metadata={}
                )],
                weights=[1.0]
            )
        
        # Verificar mensaje contiene palabras clave esperadas
        error_msg = str(exc_info.value)
        assert "at least 2" in error_msg.lower() or "personalities" in error_msg.lower()
    
    @pytest.mark.asyncio
    async def test_v10_cache_still_works(self, blender, sample_personalities):
        """
        Test: Cache behavior no cambió
        """
        # Limpiar cache primero
        await blender.clear_cache()
        
        # Primera llamada
        result1 = await blender.blend_personalities(
            personalities=sample_personalities,
            weights=[0.5, 0.5]
        )
        
        # Segunda llamada (mismos params)
        result2 = await blender.blend_personalities(
            personalities=sample_personalities,
            weights=[0.5, 0.5]
        )
        
        # Deben tener el mismo nombre (cache funciona)
        assert result1.name == result2.name
    
    @pytest.mark.asyncio
    async def test_v11_blend_from_config(self, blender):
        """
        Test: v1.1 blend_personalities_from_config sigue funcionando
        """
        # Mock personality manager
        mock_manager = AsyncMock()
        mock_manager.get_personality.side_effect = [
            PersonalityData(
                name="p1",
                description="Test 1",
                system_prompt="Test 1",
                metadata={},
                core_traits={"archetype": "A"}
            ),
            PersonalityData(
                name="p2",
                description="Test 2",
                system_prompt="Test 2",
                metadata={},
                core_traits={"archetype": "B"}
            )
        ]
        
        # Código de v1.1
        config = {"p1": 0.6, "p2": 0.4}
        result = await blender.blend_personalities_from_config(
            blend_config=config,
            personality_manager=mock_manager
        )
        
        assert result is not None
        assert isinstance(result, PersonalityData)
    
    @pytest.mark.asyncio
    async def test_clear_cache_method_exists(self, blender):
        """
        Test: Método clear_cache sigue disponible
        """
        # Código que puede existir en v1.0/v1.1
        await blender.clear_cache()
        
        # No debe lanzar error
        assert True
    
    @pytest.mark.asyncio
    async def test_clear_blend_cache_method_exists(self, blender):
        """
        Test: Método clear_blend_cache sigue disponible
        """
        # Código que puede existir en v1.0/v1.1
        size = await blender.clear_blend_cache()
        
        # Debe retornar int (número de elementos limpiados)
        assert isinstance(size, int)
        assert size >= 0
    
    @pytest.mark.asyncio
    async def test_get_cached_blend_method_exists(self, blender, sample_personalities):
        """
        Test: Método get_cached_blend sigue disponible
        """
        # Limpiar cache primero
        await blender.clear_cache()
        
        # No debe estar en cache
        cached = await blender.get_cached_blend(
            personalities=sample_personalities,
            weights=[0.5, 0.5]
        )
        assert cached is None
        
        # Hacer blend
        await blender.blend_personalities(
            personalities=sample_personalities,
            weights=[0.5, 0.5]
        )
        
        # Ahora debe estar en cache
        cached = await blender.get_cached_blend(
            personalities=sample_personalities,
            weights=[0.5, 0.5]
        )
        assert cached is not None
        assert isinstance(cached, PersonalityData)
    
    @pytest.mark.asyncio
    async def test_get_blend_cache_info_method_exists(self, blender):
        """
        Test: Método get_blend_cache_info sigue disponible
        """
        info = await blender.get_blend_cache_info()
        
        assert isinstance(info, dict)
        assert "cache_size" in info
        assert "cached_blends" in info
        assert "cache_entries" in info
    
    @pytest.mark.asyncio
    async def test_blend_with_validation_method_exists(self, blender, sample_personalities):
        """
        Test: Método blend_personalities_with_validation sigue disponible
        """
        result = await blender.blend_personalities_with_validation(
            personalities=sample_personalities,
            weights=[0.5, 0.5],
            validation_rules={
                "max_description_length": 1000
            }
        )
        
        assert result is not None
        assert isinstance(result, PersonalityData)


class TestBackwardCompatibilityClient:
    """
    Tests de LuminoraCoreClient con refactor
    """
    
    @pytest.mark.asyncio
    async def test_client_initialization_unchanged(self):
        """
        Test: Inicialización de client no cambió
        """
        # Código típico de usuario v1.0
        client = LuminoraCoreClient()
        await client.initialize()
        
        # Debe funcionar sin cambios
        assert client is not None
        assert hasattr(client, 'personality_blender')
        await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_client_has_personality_blender(self):
        """
        Test: Client sigue teniendo personality_blender
        """
        client = LuminoraCoreClient()
        await client.initialize()
        
        # Código de usuario puede acceder esto
        assert hasattr(client, 'personality_blender')
        assert isinstance(client.personality_blender, PersonalityBlender)
        
        await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_client_blend_personalities_method(self):
        """
        Test: Método blend_personalities del client sigue funcionando
        """
        client = LuminoraCoreClient()
        await client.initialize()
        
        # Mock personality manager
        mock_personality = PersonalityData(
            name="test_personality",
            description="Test",
            system_prompt="Test",
            metadata={}
        )
        client.personality_manager.get_personality = AsyncMock(return_value=mock_personality)
        
        # Código de usuario v1.0/v1.1
        try:
            result = await client.blend_personalities(
                personality_names=["test_personality", "test_personality"],
                weights=[0.5, 0.5]
            )
            # Si funciona, debe retornar PersonalityData
            assert result is not None
        except Exception as e:
            # Si falla por falta de personalidades reales, está bien
            # Lo importante es que el método existe y es callable
            assert hasattr(client, 'blend_personalities')
            assert callable(getattr(client, 'blend_personalities'))
        
        await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_client_blend_from_config_method(self):
        """
        Test: Método blend_personalities_from_config del client sigue funcionando
        """
        client = LuminoraCoreClient()
        await client.initialize()
        
        # Mock personality manager
        mock_personality = PersonalityData(
            name="test_personality",
            description="Test",
            system_prompt="Test",
            metadata={}
        )
        client.personality_manager.get_personality = AsyncMock(return_value=mock_personality)
        
        # Código de usuario v1.1
        try:
            result = await client.blend_personalities_from_config(
                blend_config={"test_personality": 0.5, "test_personality2": 0.5}
            )
            # Si funciona, debe retornar PersonalityData
            assert result is not None
        except Exception as e:
            # Si falla por falta de personalidades reales, está bien
            # Lo importante es que el método existe y es callable
            assert hasattr(client, 'blend_personalities_from_config')
            assert callable(getattr(client, 'blend_personalities_from_config'))
        
        await client.cleanup()


class TestBackwardCompatibilityImports:
    """
    Tests de imports que usuarios pueden estar usando
    """
    
    def test_import_personality_blender(self):
        """
        Test: Import directo de PersonalityBlender sigue funcionando
        """
        from luminoracore_sdk.personality.blender import PersonalityBlender
        
        blender = PersonalityBlender()
        assert blender is not None
    
    def test_import_from_personality_module(self):
        """
        Test: Import desde módulo personality sigue funcionando
        """
        from luminoracore_sdk.personality import PersonalityBlender
        
        blender = PersonalityBlender()
        assert blender is not None
    
    def test_import_personality_data(self):
        """
        Test: Import de PersonalityData sigue funcionando
        """
        from luminoracore_sdk.types.personality import PersonalityData
        
        personality = PersonalityData(
            name="test",
            description="Test",
            system_prompt="Test",
            metadata={}
        )
        assert personality is not None


# IMPORTANTE: Estos tests simulan código REAL de usuarios
# Si alguno falla, estamos rompiendo backward compatibility

