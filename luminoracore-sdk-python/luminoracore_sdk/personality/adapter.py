"""
Adapter para usar luminoracore.PersonaBlend con API del SDK

PROPÓSITO:
- Permitir migración gradual sin romper API pública
- Traducir entre tipos SDK (PersonalityData) y Core (Personality)
- Mantener 100% backward compatibility

Autor: Refactor Arquitectura Fase 0
Fecha: 2025-11-21
"""

from typing import List, Optional, Dict, Any
import asyncio
from pathlib import Path

# Imports del Core
try:
    from luminoracore.tools.blender import PersonaBlend as CorePersonaBlend
    from luminoracore.core.personality import Personality as CorePersonality
    HAS_CORE = True
except ImportError:
    HAS_CORE = False
    CorePersonaBlend = None
    CorePersonality = None

# Imports del SDK
from ..types.personality import PersonalityData


class PersonaBlendAdapter:
    """
    Adapter que traduce entre SDK y Core para personality blending
    
    Permite usar luminoracore.PersonaBlend manteniendo API del SDK.
    """
    
    def __init__(self):
        """Initialize adapter with Core blender"""
        if not HAS_CORE:
            raise ImportError(
                "luminoracore not available. Install luminoracore>=1.2.0 to use PersonaBlendAdapter"
            )
        self._core_blender = CorePersonaBlend()
    
    async def blend_personalities(
        self,
        personalities: List[PersonalityData],
        weights: List[float],
        blend_name: Optional[str] = None
    ) -> PersonalityData:
        """
        Blend personalities usando Core blender
        
        Args:
            personalities: Lista de SDK PersonalityData objects
            weights: Pesos para cada personality
            blend_name: Nombre opcional para el blend
            
        Returns:
            PersonalityData: Resultado del blend en formato SDK
            
        Raises:
            ValueError: Si inputs inválidos
        """
        # Validar inputs (mantener validación del SDK)
        if len(personalities) != len(weights):
            raise ValueError(
                f"Number of personalities ({len(personalities)}) "
                f"must match number of weights ({len(weights)})"
            )
        
        if len(personalities) < 2:
            raise ValueError(
                "At least 2 personalities required for blending"
            )
        
        # Validar weights sum to 1.0
        weight_sum = sum(weights)
        if abs(weight_sum - 1.0) > 0.01:
            raise ValueError(
                f"Weights must sum to 1.0, got {weight_sum}"
            )
        
        # Convertir SDK PersonalityData → Core Personality
        core_personalities = [
            self._sdk_to_core_personality(p) 
            for p in personalities
        ]
        
        # Crear weights dict para Core API
        weights_dict = {
            core_personalities[i].persona.name: weights[i]
            for i in range(len(core_personalities))
        }
        
        # Llamar al Core blender (sync)
        # NOTA: Core blender es sync, lo ejecutamos en executor
        loop = asyncio.get_event_loop()
        blend_result = await loop.run_in_executor(
            None,
            self._core_blender.blend,
            core_personalities,
            weights_dict,
            "weighted_average",  # strategy por defecto
            blend_name
        )
        
        # Convertir resultado Core → SDK PersonalityData
        result = self._core_to_sdk_personality(blend_result.blended_personality)
        
        return result
    
    def _sdk_to_core_personality(
        self, 
        sdk_personality: PersonalityData
    ) -> CorePersonality:
        """
        Convierte SDK PersonalityData a Core Personality
        
        Args:
            sdk_personality: PersonalityData del SDK
            
        Returns:
            CorePersonality: Personality del Core
        """
        # PersonalityData es Pydantic BaseModel, convertir a dict
        if hasattr(sdk_personality, 'model_dump'):
            personality_dict = sdk_personality.model_dump()
        else:
            personality_dict = sdk_personality.dict()
        
        # Core Personality puede inicializarse desde dict o Path
        # Necesitamos construir estructura compatible con Core
        # El Core espera estructura completa con persona, core_traits, etc.
        
        # Si el dict ya tiene estructura completa, usarlo directamente
        if "persona" in personality_dict and isinstance(personality_dict["persona"], dict):
            # Ya tiene estructura Core, crear Personality desde dict
            core_personality = CorePersonality(personality_dict)
        else:
            # Convertir estructura SDK a estructura Core
            core_dict = self._convert_sdk_to_core_structure(personality_dict)
            core_personality = CorePersonality(core_dict)
        
        return core_personality
    
    def _convert_sdk_to_core_structure(self, sdk_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convierte estructura SDK a estructura Core
        
        Args:
            sdk_dict: Dict de PersonalityData
            
        Returns:
            Dict compatible con Core Personality
        """
        # Obtener metadata (puede ser dict o None)
        metadata = sdk_dict.get("metadata", {})
        if metadata is None:
            metadata = {}
        
        # Obtener core_traits (puede ser dict o None)
        core_traits = sdk_dict.get("core_traits", {})
        if core_traits is None:
            core_traits = {}
        elif not isinstance(core_traits, dict):
            # Si core_traits es lista u otro tipo, crear dict vacío
            core_traits = {}
        
        # Estructura mínima para Core Personality
        core_dict = {
            "persona": {
                "name": sdk_dict.get("name", "Unknown"),
                "version": metadata.get("version", "1.0.0"),
                "description": sdk_dict.get("description", ""),
                "author": metadata.get("author", "Unknown"),
                "tags": metadata.get("tags", []),
                "language": metadata.get("language", "en"),
                "compatibility": metadata.get("compatibility", [])
            },
            "core_traits": {
                "archetype": core_traits.get("archetype", "neutral"),
                "temperament": core_traits.get("temperament", "balanced"),
                "communication_style": core_traits.get("communication_style", "neutral")
            },
            "linguistic_profile": {
                "tone": [],
                "syntax": "varied",
                "vocabulary": [],
                "fillers": [],
                "punctuation_style": "moderate"
            },
            "behavioral_rules": [],
            "metadata": {}
        }
        
        # Agregar campos adicionales si existen
        if "system_prompt" in sdk_dict:
            # Core puede tener system_prompt en diferentes lugares
            # Por ahora, lo agregamos como metadata
            core_dict["metadata"]["system_prompt"] = sdk_dict["system_prompt"]
        
        # Preservar otros campos del SDK en metadata
        if isinstance(metadata, dict):
            core_dict["metadata"].update(metadata)
        
        return core_dict
    
    def _core_to_sdk_personality(
        self,
        core_personality: CorePersonality
    ) -> PersonalityData:
        """
        Convierte Core Personality a SDK PersonalityData
        
        Args:
            core_personality: Personality del Core
            
        Returns:
            PersonalityData: PersonalityData del SDK
        """
        # Core Personality tiene to_dict()
        personality_dict = core_personality.to_dict()
        
        # Convertir estructura Core a estructura SDK
        sdk_dict = self._convert_core_to_sdk_structure(personality_dict)
        
        # PersonalityData del SDK (Pydantic)
        sdk_personality = PersonalityData(**sdk_dict)
        
        return sdk_personality
    
    def _convert_core_to_sdk_structure(self, core_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convierte estructura Core a estructura SDK
        
        Args:
            core_dict: Dict de Core Personality
            
        Returns:
            Dict compatible con PersonalityData
        """
        # Extraer información de persona
        persona = core_dict.get("persona", {})
        
        sdk_dict = {
            "name": persona.get("name", "Unknown"),
            "description": persona.get("description", ""),
            "system_prompt": core_dict.get("metadata", {}).get("system_prompt", ""),
            "name_override": None,
            "description_override": None,
            "metadata": {
                "version": persona.get("version", "1.0.0"),
                "author": persona.get("author", "Unknown"),
                "tags": persona.get("tags", []),
                "language": persona.get("language", "en"),
                "compatibility": persona.get("compatibility", [])
            }
        }
        
        # Agregar core_traits si existen
        if "core_traits" in core_dict:
            sdk_dict["core_traits"] = core_dict["core_traits"]
        
        # Preservar metadata adicional
        if "metadata" in core_dict:
            sdk_dict["metadata"].update(core_dict["metadata"])
        
        return sdk_dict


# Para tests: export adapter
__all__ = ['PersonaBlendAdapter']

