"""
Tests adicionales para validar refactor de PersonalityBlender

AGREGADOS: Tests específicos para validar que adapter funciona correctamente
MANTENER: Todos los tests existentes sin modificar
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock

from luminoracore_sdk.personality.blender import PersonalityBlender
from luminoracore_sdk.types.personality import PersonalityData
from luminoracore_sdk.utils.exceptions import PersonalityError

# Import adapter si disponible
try:
    from luminoracore_sdk.personality.adapter import PersonaBlendAdapter
    HAS_ADAPTER = True
except ImportError:
    HAS_ADAPTER = False
    PersonaBlendAdapter = None


class TestPersonalityBlenderRefactor:
    """Tests específicos del refactor para asegurar que adapter funciona"""
    
    @pytest.fixture
    def blender(self):
        """Create blender instance"""
        return PersonalityBlender()
    
    @pytest.fixture
    def sample_personalities(self):
        """Create sample personalities para tests"""
        p1 = PersonalityData(
            name="test_personality_1",
            description="Test personality 1 description",
            system_prompt="You are test personality 1",
            metadata={
                "version": "1.0.0",
                "author": "Test Author",
                "tags": ["test", "helper"],
                "language": "en"
            },
            core_traits={
                "archetype": "Helper",
                "temperament": "Friendly",
                "communication_style": "Warm"
            }
        )
        p2 = PersonalityData(
            name="test_personality_2",
            description="Test personality 2 description",
            system_prompt="You are test personality 2",
            metadata={
                "version": "1.0.0",
                "author": "Test Author",
                "tags": ["test", "thinker"],
                "language": "en"
            },
            core_traits={
                "archetype": "Thinker",
                "temperament": "Analytical",
                "communication_style": "Formal"
            }
        )
        return [p1, p2]
    
    def test_blender_uses_adapter(self, blender):
        """
        CRÍTICO: Verificar que PersonalityBlender usa adapter internamente
        """
        assert hasattr(blender, '_adapter')
        # Adapter puede ser None si Core no disponible (fallback)
        # Pero el atributo debe existir
        if HAS_ADAPTER:
            # Si Core disponible, adapter debe estar inicializado
            if blender._adapter is not None:
                assert isinstance(blender._adapter, PersonaBlendAdapter)
    
    @pytest.mark.asyncio
    async def test_blender_delegates_to_adapter(self, blender, sample_personalities):
        """
        CRÍTICO: Verificar que blend_personalities delega al adapter
        """
        # Solo testear si adapter está disponible
        if not HAS_ADAPTER or blender._adapter is None:
            pytest.skip("Adapter not available, skipping delegation test")
        
        # Mock del adapter
        mock_adapter = AsyncMock()
        mock_adapter.blend_personalities.return_value = PersonalityData(
            name="test_blend",
            description="Test blend",
            system_prompt="Test blend prompt",
            metadata={}
        )
        
        # Reemplazar adapter con mock
        blender._adapter = mock_adapter
        
        # Crear personalities de prueba
        personalities = sample_personalities
        weights = [0.6, 0.4]
        
        # Llamar blend
        result = await blender.blend_personalities(
            personalities=personalities,
            weights=weights,
            blend_name="test"
        )
        
        # Verificar que adapter fue llamado
        mock_adapter.blend_personalities.assert_called_once_with(
            personalities=personalities,
            weights=weights,
            blend_name="test"
        )
        
        # Verificar resultado
        assert result is not None
        assert isinstance(result, PersonalityData)
    
    @pytest.mark.asyncio
    async def test_blender_maintains_cache_behavior(self, blender, sample_personalities):
        """
        CRÍTICO: Cache debe seguir funcionando después del refactor
        """
        personalities = sample_personalities
        weights = [0.5, 0.5]
        
        # Limpiar cache primero
        await blender.clear_cache()
        
        # Primer blend (va al adapter o fallback)
        result1 = await blender.blend_personalities(
            personalities=personalities,
            weights=weights
        )
        
        # Segundo blend con mismos params (debe venir de cache)
        if blender._adapter:
            with patch.object(blender._adapter, 'blend_personalities') as mock_blend:
                result2 = await blender.blend_personalities(
                    personalities=personalities,
                    weights=weights
                )
                
                # Adapter NO debe ser llamado (viene de cache)
                mock_blend.assert_not_called()
        else:
            # Si no hay adapter, verificar que cache funciona igual
            with patch.object(blender, '_perform_blend') as mock_blend:
                result2 = await blender.blend_personalities(
                    personalities=personalities,
                    weights=weights
                )
                
                # Fallback NO debe ser llamado (viene de cache)
                mock_blend.assert_not_called()
        
        # Resultados deben ser idénticos
        assert result1.name == result2.name
    
    @pytest.mark.asyncio
    async def test_error_handling_preserved(self, blender):
        """
        CRÍTICO: Manejo de errores debe ser consistente
        """
        personalities = [
            PersonalityData(
                name="p1",
                description="Test",
                system_prompt="Test",
                metadata={}
            ),
        ]
        
        # Test con < 2 personalities
        with pytest.raises(PersonalityError, match="At least 2"):
            await blender.blend_personalities(
                personalities=personalities,
                weights=[1.0]
            )
        
        # Test con weights que no suman 1.0
        personalities.append(PersonalityData(
            name="p2",
            description="Test 2",
            system_prompt="Test 2",
            metadata={}
        ))
        
        with pytest.raises(PersonalityError, match="sum to 1.0"):
            await blender.blend_personalities(
                personalities=personalities,
                weights=[0.3, 0.3]  # Suma 0.6
            )
    
    @pytest.mark.asyncio
    async def test_blender_works_with_adapter(self, blender, sample_personalities):
        """
        Test que blender funciona correctamente con adapter
        """
        if not HAS_ADAPTER or blender._adapter is None:
            pytest.skip("Adapter not available")
        
        result = await blender.blend_personalities(
            personalities=sample_personalities,
            weights=[0.5, 0.5],
            blend_name="test_blend"
        )
        
        assert result is not None
        assert isinstance(result, PersonalityData)
        assert result.name == "test_blend"
    
    @pytest.mark.asyncio
    async def test_blender_works_without_adapter(self, blender, sample_personalities):
        """
        Test que blender funciona con fallback si adapter no disponible
        """
        # Forzar fallback
        original_adapter = blender._adapter
        blender._adapter = None
        
        try:
            result = await blender.blend_personalities(
                personalities=sample_personalities,
                weights=[0.5, 0.5],
                blend_name="test_fallback"
            )
            
            assert result is not None
            assert isinstance(result, PersonalityData)
            assert result.name == "test_fallback"
        finally:
            # Restaurar adapter original
            blender._adapter = original_adapter
    
    @pytest.mark.asyncio
    async def test_cache_methods_still_work(self, blender):
        """
        Test que métodos de cache siguen funcionando
        """
        # clear_cache debe funcionar
        await blender.clear_cache()
        
        # clear_blend_cache debe funcionar
        size = await blender.clear_blend_cache()
        assert size == 0
        
        # get_blend_cache_info debe funcionar
        info = await blender.get_blend_cache_info()
        assert "cache_size" in info
        assert info["cache_size"] == 0


# IMPORTANTE: NO modificar tests existentes
# Solo agregar estos nuevos tests

