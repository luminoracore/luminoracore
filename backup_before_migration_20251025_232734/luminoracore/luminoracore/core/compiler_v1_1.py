"""
Dynamic Personality Compiler for v1.1

Compiles personality dynamically based on current state (affinity, mood).
Works alongside existing v1.0 compiler.
"""

from typing import Dict, Any, Optional, List
from copy import deepcopy
import logging

from .personality_v1_1 import (
    PersonalityV11Extensions,
    LevelModifiers
)

logger = logging.getLogger(__name__)


class DynamicPersonalityCompiler:
    """Compiles personality dynamically based on runtime state"""
    
    def __init__(
        self,
        base_personality: Dict[str, Any],
        extensions: PersonalityV11Extensions
    ):
        """
        Initialize compiler
        
        Args:
            base_personality: Base personality dict (v1.0 format)
            extensions: v1.1 extensions extracted from JSON
        """
        self.base = base_personality
        self.extensions = extensions
    
    def compile(
        self,
        affinity_points: Optional[int] = None,
        current_mood: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compile personality with current state modifiers
        
        Args:
            affinity_points: Current affinity (0-100), None = no level modifiers
            current_mood: Current mood name, None = no mood modifiers
            
        Returns:
            Compiled personality dictionary with modifiers applied
        """
        # Start with deep copy of base (immutable operation)
        compiled = deepcopy(self.base)
        
        # Apply relationship level modifiers if enabled and affinity provided
        if self.extensions.has_hierarchical() and affinity_points is not None:
            level_config = self.extensions.hierarchical_config.get_level_for_affinity(affinity_points)
            if level_config:
                logger.debug(f"Applying level modifiers: {level_config.name}")
                self._apply_modifiers(compiled, level_config.modifiers)
        
        # Apply mood modifiers if enabled and mood provided
        if self.extensions.has_moods() and current_mood is not None:
            mood_config = self.extensions.mood_config.get_mood_config(current_mood)
            if mood_config:
                logger.debug(f"Applying mood modifiers: {current_mood}")
                self._apply_modifiers(compiled, mood_config.modifiers)
        
        return compiled
    
    def _apply_modifiers(
        self,
        personality: Dict[str, Any],
        modifiers: LevelModifiers
    ) -> None:
        """Apply modifiers to personality dictionary (in-place)"""
        # Apply advanced parameter modifiers
        if 'advanced_parameters' in personality:
            personality['advanced_parameters'] = modifiers.advanced_parameters.apply_to(
                personality['advanced_parameters']
            )
        
        # Apply linguistic profile modifiers
        if 'linguistic_profile' in personality:
            personality['linguistic_profile'] = modifiers.linguistic_profile.apply_to(
                personality['linguistic_profile']
            )
        
        # Apply system prompt modifiers
        if modifiers.system_prompt_additions.prefix or modifiers.system_prompt_additions.suffix:
            current_prompt = personality.get('system_prompt', '')
            personality['system_prompt'] = modifiers.system_prompt_additions.apply_to(current_prompt)
    
    def get_active_level(self, affinity_points: int) -> Optional[str]:
        """Get name of active relationship level for given affinity"""
        if not self.extensions.has_hierarchical():
            return None
        
        level_config = self.extensions.hierarchical_config.get_level_for_affinity(affinity_points)
        return level_config.name if level_config else None
    
    def get_available_moods(self) -> List[str]:
        """Get list of available mood names"""
        if not self.extensions.has_moods():
            return []
        
        return self.extensions.mood_config.get_mood_names()
    
    def is_v1_0_compatible(self) -> bool:
        """Check if this personality is v1.0 compatible (no v1.1 features)"""
        return self.extensions.is_v1_0_only()

