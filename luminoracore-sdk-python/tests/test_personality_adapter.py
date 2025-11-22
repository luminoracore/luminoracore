"""
Tests para PersonaBlendAdapter

Valida que adapter funciona correctamente con Core.
"""

import pytest
import asyncio
from pathlib import Path

try:
    from luminoracore_sdk.personality.adapter import PersonaBlendAdapter
    from luminoracore_sdk.types.personality import PersonalityData
    from luminoracore.tools.blender import PersonaBlend
    from luminoracore.core.personality import Personality
    HAS_CORE = True
except ImportError:
    HAS_CORE = False
    pytest.skip("luminoracore not available", allow_module_level=True)


class TestPersonaBlendAdapter:
    """Test suite para adapter"""
    
    @pytest.fixture
    def adapter(self):
        """Create adapter instance"""
        return PersonaBlendAdapter()
    
    @pytest.fixture
    def sample_personalities(self):
        """Create sample personalities para tests"""
        # Crear personalidades mínimas compatibles con ambos sistemas
        p1 = PersonalityData(
            name="test_personality_1",
            description="Test personality 1 description",
            system_prompt="You are test personality 1",
            metadata={
                "version": "1.0.0",
                "author": "Test Author",
                "tags": ["test", "helper"],
                "language": "en",
                "compatibility": ["openai"]
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
                "language": "en",
                "compatibility": ["openai"]
            },
            core_traits={
                "archetype": "Thinker",
                "temperament": "Analytical",
                "communication_style": "Formal"
            }
        )
        return [p1, p2]
    
    @pytest.mark.asyncio
    async def test_adapter_initialization(self, adapter):
        """Adapter debe inicializarse correctamente"""
        assert adapter is not None
        assert adapter._core_blender is not None
        assert isinstance(adapter._core_blender, PersonaBlend)
    
    @pytest.mark.asyncio
    async def test_blend_personalities_basic(
        self, 
        adapter, 
        sample_personalities
    ):
        """Debe blender personalities correctamente"""
        result = await adapter.blend_personalities(
            personalities=sample_personalities,
            weights=[0.5, 0.5],
            blend_name="test_blend"
        )
        
        assert result is not None
        assert isinstance(result, PersonalityData)
        assert result.name == "test_blend"
        # Validar que tiene campos básicos
        assert hasattr(result, "description")
        assert hasattr(result, "system_prompt")
    
    @pytest.mark.asyncio
    async def test_blend_validates_inputs(self, adapter, sample_personalities):
        """Debe validar inputs correctamente"""
        
        # Mismatch en número de weights
        with pytest.raises(ValueError, match="must match"):
            await adapter.blend_personalities(
                personalities=sample_personalities,
                weights=[0.5],  # Solo 1 weight para 2 personalities
            )
        
        # Menos de 2 personalities
        with pytest.raises(ValueError, match="At least 2"):
            await adapter.blend_personalities(
                personalities=[sample_personalities[0]],
                weights=[1.0],
            )
        
        # Weights no suman 1.0
        with pytest.raises(ValueError, match="sum to 1.0"):
            await adapter.blend_personalities(
                personalities=sample_personalities,
                weights=[0.3, 0.3],  # Suma 0.6
            )
    
    @pytest.mark.asyncio
    async def test_sdk_to_core_conversion(self, adapter, sample_personalities):
        """Conversión SDK → Core debe funcionar"""
        sdk_personality = sample_personalities[0]
        
        # Convertir
        core_personality = adapter._sdk_to_core_personality(sdk_personality)
        
        # Validar tipo
        assert isinstance(core_personality, Personality)
        
        # Validar contenido preservado
        assert core_personality.persona.name == sdk_personality.name
        assert core_personality.persona.description == sdk_personality.description
    
    @pytest.mark.asyncio
    async def test_core_to_sdk_conversion(self, adapter, sample_personalities):
        """Conversión Core → SDK debe funcionar"""
        # Crear Core personality desde SDK personality
        sdk_personality = sample_personalities[0]
        core_personality = adapter._sdk_to_core_personality(sdk_personality)
        
        # Convertir de vuelta
        sdk_personality_restored = adapter._core_to_sdk_personality(core_personality)
        
        # Validar tipo
        assert isinstance(sdk_personality_restored, PersonalityData)
        
        # Validar contenido preservado
        assert sdk_personality_restored.name == core_personality.persona.name
        assert sdk_personality_restored.description == core_personality.persona.description
    
    @pytest.mark.asyncio
    async def test_roundtrip_conversion(self, adapter, sample_personalities):
        """Conversión SDK → Core → SDK debe preservar datos"""
        sdk_personality = sample_personalities[0]
        
        # SDK → Core → SDK
        core_personality = adapter._sdk_to_core_personality(sdk_personality)
        sdk_restored = adapter._core_to_sdk_personality(core_personality)
        
        # Validar que datos clave se preservan
        assert sdk_restored.name == sdk_personality.name
        assert sdk_restored.description == sdk_personality.description
    
    @pytest.mark.asyncio
    async def test_blend_with_different_weights(self, adapter, sample_personalities):
        """Debe blender con diferentes pesos"""
        result = await adapter.blend_personalities(
            personalities=sample_personalities,
            weights=[0.7, 0.3],
            blend_name="weighted_blend"
        )
        
        assert result is not None
        assert result.name == "weighted_blend"
        assert isinstance(result, PersonalityData)


# IMPORTANTE: Estos tests DEBEN pasar antes de seguir

