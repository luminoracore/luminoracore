"""
Personality blending functionality for LuminoraCore SDK.

REFACTORED: Ahora usa luminoracore.PersonaBlend via adapter
Mantiene 100% backward compatibility con API pública.

Autor: Refactor Arquitectura Fase 0
Fecha: 2025-11-21
"""

import asyncio
from typing import Dict, List, Optional, Any, Tuple
import logging
from datetime import datetime
import json

from ..types.personality import PersonalityData, PersonalityBlend
from ..utils.exceptions import PersonalityError
from ..utils.validation import validate_personality_blend
from ..utils.helpers import deep_merge_dicts

# NUEVO: Import adapter
try:
    from .adapter import PersonaBlendAdapter
    HAS_ADAPTER = True
except ImportError:
    HAS_ADAPTER = False
    PersonaBlendAdapter = None

logger = logging.getLogger(__name__)


class PersonalityBlender:
    """
    Advanced personality blending with PersonaBlend™ technology.
    
    REFACTORED: Ahora delega a luminoracore.PersonaBlend via adapter.
    API pública se mantiene idéntica para backward compatibility.
    """
    
    def __init__(self):
        """
        Initialize the personality blender.
        
        CHANGED: Ahora usa adapter en lugar de implementación propia.
        """
        # NUEVO: Usar adapter en lugar de implementación propia
        if HAS_ADAPTER:
            try:
                self._adapter = PersonaBlendAdapter()
                logger.info("PersonalityBlender using Core PersonaBlend via adapter")
            except ImportError as e:
                logger.warning(f"Core PersonaBlend not available, using fallback: {e}")
                self._adapter = None
        else:
            self._adapter = None
        
        # Mantener cache para backward compatibility
        self._blend_cache: Dict[str, PersonalityData] = {}
        self._lock = asyncio.Lock()
    
    async def blend_personalities(
        self,
        personalities: List[PersonalityData],
        weights: List[float],
        blend_name: Optional[str] = None
    ) -> PersonalityData:
        """
        Blend multiple personalities with custom weights.
        
        UNCHANGED: API pública idéntica.
        CHANGED: Implementación ahora delega al adapter.
        
        Args:
            personalities: List of personality data objects
            weights: List of weights for each personality (must sum to 1.0)
            blend_name: Optional name for the blended personality
            
        Returns:
            Blended personality data
            
        Raises:
            PersonalityError: If blending fails or validation fails
        """
        # Validaciones básicas (mantener para error messages consistentes)
        if len(personalities) != len(weights):
            raise PersonalityError(
                "Number of personalities must match number of weights"
            )
        
        if len(personalities) < 2:
            raise PersonalityError(
                "At least 2 personalities required for blending"
            )
        
        # Validate weights sum to 1.0
        weight_sum = sum(weights)
        if abs(weight_sum - 1.0) > 0.01:
            raise PersonalityError(
                f"Weights must sum to 1.0, got {weight_sum}"
            )
        
        # Validate all weights are non-negative
        if any(w < 0 for w in weights):
            raise PersonalityError("All weights must be non-negative")
        
        try:
            # Check cache first (mantener comportamiento)
            cache_key = self._generate_cache_key(personalities, weights)
            async with self._lock:
                if cache_key in self._blend_cache:
                    logger.info(f"Returning cached blend: {cache_key}")
                    return self._blend_cache[cache_key]
            
            # Generate blend name if not provided
            if not blend_name:
                blend_name = self._generate_blend_name(personalities, weights)
            
            # CAMBIO PRINCIPAL: Delegar al adapter (que usa Core) si disponible
            if self._adapter:
                blended_personality = await self._adapter.blend_personalities(
                    personalities=personalities,
                    weights=weights,
                    blend_name=blend_name
                )
            else:
                # Fallback a implementación propia si adapter no disponible
                logger.warning("Using fallback blending (adapter not available)")
                blended_personality = await self._perform_blend(personalities, weights, blend_name)
            
            # Cache the blend (mantener comportamiento)
            async with self._lock:
                self._blend_cache[cache_key] = blended_personality
            
            logger.info(
                f"Successfully blended {len(personalities)} personalities "
                f"into '{blend_name}'"
            )
            return blended_personality
            
        except Exception as e:
            logger.error(f"Failed to blend personalities: {e}")
            # Mantener tipo de excepción consistente
            if isinstance(e, PersonalityError):
                raise
            # Convertir ValueError del adapter a PersonalityError
            if isinstance(e, ValueError):
                raise PersonalityError(str(e))
            raise PersonalityError(f"Personality blending failed: {e}")
    
    async def blend_personalities_from_config(
        self,
        blend_config: Dict[str, float],
        personality_manager: Any
    ) -> PersonalityData:
        """
        Blend personalities from configuration dictionary.
        
        UNCHANGED: API pública idéntica, solo logging mejorado.
        
        Args:
            blend_config: Dictionary mapping personality names to weights
            personality_manager: PersonalityManager instance
            
        Returns:
            Blended personality data
            
        Raises:
            PersonalityError: If blending fails
        """
        try:
            # Validate blend configuration
            validate_personality_blend(blend_config)
            
            # Load personalities from manager
            personalities = []
            for name in blend_config.keys():
                personality = await personality_manager.get_personality(name)
                if not personality:
                    raise PersonalityError(
                        f"Personality not found: {name}"
                    )
                personalities.append(personality)
            
            # Extract weights
            weights = list(blend_config.values())
            
            # Blend using main method (que ahora usa adapter)
            blended = await self.blend_personalities(
                personalities=personalities,
                weights=weights
            )
            
            logger.info(f"Blended from config: {blend_config}")
            return blended
            
        except Exception as e:
            logger.error(f"Failed to blend from config: {e}")
            raise PersonalityError(
                f"Blending from config failed: {e}"
            )
    
    async def blend_personalities_with_validation(
        self,
        personalities: List[PersonalityData],
        weights: List[float],
        blend_name: Optional[str] = None,
        validation_rules: Optional[Dict[str, Any]] = None
    ) -> PersonalityData:
        """
        Blend personalities with additional validation rules.
        
        UNCHANGED: API pública idéntica.
        
        Args:
            personalities: List of personality data objects
            weights: List of weights for each personality
            blend_name: Optional name for the blended personality
            validation_rules: Optional validation rules
            
        Returns:
            Blended personality data
        """
        # Perform basic blending
        blended = await self.blend_personalities(personalities, weights, blend_name)
        
        # Apply additional validation if provided
        if validation_rules:
            await self._validate_blended_personality(blended, validation_rules)
        
        return blended
    
    async def get_cached_blend(
        self,
        personalities: List[PersonalityData],
        weights: List[float]
    ) -> Optional[PersonalityData]:
        """
        Get cached blend if available.
        
        UNCHANGED: API pública idéntica.
        
        Args:
            personalities: List of personality data objects
            weights: List of weights for each personality
            
        Returns:
            Cached blended personality or None
        """
        cache_key = self._generate_cache_key(personalities, weights)
        async with self._lock:
            return self._blend_cache.get(cache_key)
    
    async def clear_blend_cache(self) -> int:
        """
        Clear the blend cache.
        
        Returns:
            Number of cached blends cleared
        """
        async with self._lock:
            cache_size = len(self._blend_cache)
            self._blend_cache.clear()
        
        logger.info(f"Cleared {cache_size} cached blends")
        return cache_size
    
    async def clear_cache(self) -> None:
        """
        Clear the blend cache.
        
        UNCHANGED: Utility method mantiene API.
        Alias para clear_blend_cache() para backward compatibility.
        """
        await self.clear_blend_cache()
    
    async def get_blend_cache_info(self) -> Dict[str, Any]:
        """
        Get blend cache information.
        
        UNCHANGED: API pública idéntica.
        
        Returns:
            Cache information dictionary
        """
        async with self._lock:
            return {
                "cache_size": len(self._blend_cache),
                "cached_blends": list(self._blend_cache.keys()),
                "cache_entries": [
                    {
                        "name": blend.name,
                        "description": blend.description,
                        "created_at": blend.metadata.get("created_at"),
                    }
                    for blend in self._blend_cache.values()
                ]
            }
    
    async def _perform_blend(
        self,
        personalities: List[PersonalityData],
        weights: List[float],
        blend_name: str
    ) -> PersonalityData:
        """
        Perform the actual blending of personalities.
        
        FALLBACK: Solo usado si adapter no disponible.
        Mantenido para backward compatibility.
        
        Args:
            personalities: List of personality data objects
            weights: List of weights for each personality
            blend_name: Name for the blended personality
            
        Returns:
            Blended personality data
        """
        # Initialize blended personality with base structure
        blended = PersonalityData(
            name=blend_name,
            description="",
            system_prompt="",
            name_override=None,
            description_override=None,
            metadata={}
        )
        
        # Blend descriptions
        blended.description = await self._blend_texts(
            [p.description for p in personalities],
            weights
        )
        
        # Blend system prompts
        blended.system_prompt = await self._blend_texts(
            [p.system_prompt for p in personalities],
            weights
        )
        
        # Blend name overrides (if any)
        name_overrides = [p.name_override for p in personalities if p.name_override]
        if name_overrides:
            blended.name_override = await self._blend_texts(name_overrides, weights[:len(name_overrides)])
        
        # Blend description overrides (if any)
        desc_overrides = [p.description_override for p in personalities if p.description_override]
        if desc_overrides:
            blended.description_override = await self._blend_texts(desc_overrides, weights[:len(desc_overrides)])
        
        # Blend metadata
        blended.metadata = await self._blend_metadata(
            [p.metadata for p in personalities],
            weights
        )
        
        # Add blend-specific metadata
        blended.metadata.update({
            "blend_type": "persona_blend",
            "blended_personalities": [p.name for p in personalities],
            "blend_weights": weights,
            "created_at": datetime.utcnow().isoformat(),
            "blend_version": "1.0"
        })
        
        return blended
    
    async def _blend_texts(self, texts: List[str], weights: List[float]) -> str:
        """
        Blend multiple text strings using weighted combination.
        
        FALLBACK: Solo usado si adapter no disponible.
        
        Args:
            texts: List of text strings
            weights: List of weights for each text
            
        Returns:
            Blended text string
        """
        if not texts:
            return ""
        
        if len(texts) == 1:
            return texts[0]
        
        # Simple text blending - in a real implementation, this would use
        # more sophisticated NLP techniques like semantic similarity,
        # sentence-level blending, or even LLM-based blending
        
        # For now, we'll use a simple weighted concatenation approach
        blended_parts = []
        
        for text, weight in zip(texts, weights):
            if weight > 0 and text.strip():
                # Add weight as a prefix to indicate influence
                blended_parts.append(f"[Weight: {weight:.2f}] {text}")
        
        return "\n\n".join(blended_parts)
    
    async def _blend_metadata(
        self,
        metadata_list: List[Dict[str, Any]],
        weights: List[float]
    ) -> Dict[str, Any]:
        """
        Blend metadata dictionaries.
        
        FALLBACK: Solo usado si adapter no disponible.
        
        Args:
            metadata_list: List of metadata dictionaries
            weights: List of weights for each metadata
            
        Returns:
            Blended metadata dictionary
        """
        if not metadata_list:
            return {}
        
        if len(metadata_list) == 1:
            return metadata_list[0].copy()
        
        # Start with the first metadata
        blended = metadata_list[0].copy()
        
        # Merge additional metadata with weights
        for metadata, weight in zip(metadata_list[1:], weights[1:]):
            if weight > 0:
                # Deep merge metadata
                blended = deep_merge_dicts(blended, metadata)
        
        return blended
    
    async def _validate_blended_personality(
        self,
        personality: PersonalityData,
        validation_rules: Dict[str, Any]
    ) -> None:
        """
        Validate a blended personality against rules.
        
        UNCHANGED: Validación adicional del SDK.
        
        Args:
            personality: Blended personality to validate
            validation_rules: Validation rules to apply
            
        Raises:
            PersonalityError: If validation fails
        """
        # Check description length
        if "max_description_length" in validation_rules:
            max_len = validation_rules["max_description_length"]
            if len(personality.description) > max_len:
                raise PersonalityError(f"Description too long: {len(personality.description)} > {max_len}")
        
        # Check system prompt length
        if "max_system_prompt_length" in validation_rules:
            max_len = validation_rules["max_system_prompt_length"]
            if len(personality.system_prompt) > max_len:
                raise PersonalityError(f"System prompt too long: {len(personality.system_prompt)} > {max_len}")
        
        # Check for required fields
        if "required_fields" in validation_rules:
            required = validation_rules["required_fields"]
            for field in required:
                if not getattr(personality, field, None):
                    raise PersonalityError(f"Required field missing: {field}")
        
        # Check for prohibited content
        if "prohibited_content" in validation_rules:
            prohibited = validation_rules["prohibited_content"]
            for content in prohibited:
                if content.lower() in personality.description.lower():
                    raise PersonalityError(f"Prohibited content found in description: {content}")
                if content.lower() in personality.system_prompt.lower():
                    raise PersonalityError(f"Prohibited content found in system prompt: {content}")
    
    def _generate_blend_name(
        self,
        personalities: List[PersonalityData],
        weights: List[float]
    ) -> str:
        """
        Generate name for blended personality.
        
        UNCHANGED: Helper method mantiene misma lógica.
        """
        # Find dominant personality (highest weight)
        max_weight_idx = weights.index(max(weights))
        dominant = personalities[max_weight_idx].name
        
        # Create name showing blend composition
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"blend_{dominant}_{timestamp}"
    
    def _generate_cache_key(
        self,
        personalities: List[PersonalityData],
        weights: List[float]
    ) -> str:
        """
        Generate cache key for blend.
        
        UNCHANGED: Helper method mantiene misma lógica.
        """
        personality_names = sorted([p.name for p in personalities])
        weights_str = "_".join([f"{w:.2f}" for w in weights])
        return f"blend_{'_'.join(personality_names)}_{weights_str}"


# Mantener exports para backward compatibility
__all__ = ['PersonalityBlender']
