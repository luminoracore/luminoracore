"""Personality manager for LuminoraCore SDK."""

import asyncio
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime
import json
from pathlib import Path

from ..types.personality import PersonalityData
from ..utils.exceptions import PersonalityError
from ..utils.helpers import parse_config, validate_personality_data
from .validator import PersonalityValidator

logger = logging.getLogger(__name__)


class PersonalityManager:
    """Manages AI personalities and their configurations."""
    
    def __init__(self, personalities_dir: Optional[str] = None):
        """
        Initialize the personality manager.
        
        Args:
            personalities_dir: Directory containing personality files
        """
        self.personalities_dir = personalities_dir or "personalities"
        self._personalities: Dict[str, PersonalityData] = {}
        self._validator = PersonalityValidator()
        self._lock = asyncio.Lock()
    
    async def load_personality(self, name: str, config: Dict[str, Any]) -> PersonalityData:
        """
        Load a personality from configuration.
        
        Args:
            name: Personality name
            config: Personality configuration
            
        Returns:
            Personality data object
            
        Raises:
            PersonalityError: If personality loading fails
        """
        try:
            # Validate configuration
            await self._validator.validate_personality_config(config)
            
            # Create personality data object
            personality = PersonalityData(
                name=name,
                description=config.get("description", ""),
                system_prompt=config.get("system_prompt", ""),
                name_override=config.get("name_override"),
                description_override=config.get("description_override"),
                metadata=config.get("metadata", {})
            )
            
            # Validate personality data
            validate_personality_data(personality)
            
            # Store in memory
            async with self._lock:
                self._personalities[name] = personality
            
            logger.info(f"Loaded personality: {name}")
            return personality
            
        except Exception as e:
            logger.error(f"Failed to load personality {name}: {e}")
            raise PersonalityError(f"Failed to load personality {name}: {e}")
    
    async def load_personality_from_file(self, file_path: str) -> PersonalityData:
        """
        Load a personality from a JSON file.
        
        Args:
            file_path: Path to personality file
            
        Returns:
            Personality data object
        """
        try:
            # Parse configuration from file
            config = parse_config(file_path)
            
            # Handle nested format (persona.name) vs flat format (name)
            if "persona" in config:
                # New nested format
                persona = config["persona"]
                # Use filename as key (safe identifier), persona name as display name
                name = Path(file_path).stem  # Safe identifier like "dr_luna"
                display_name = persona.get("name", name)  # Display name like "Dr. Luna"
                description = persona.get("description", "")
                
                # Build system prompt from personality data
                system_prompt_parts = []
                system_prompt_parts.append(f"You are {display_name}. {description}")
                
                if "core_traits" in config:
                    traits = config["core_traits"]
                    if traits.get("archetype"):
                        system_prompt_parts.append(f"Archetype: {traits['archetype']}")
                
                if "behavioral_rules" in config:
                    rules = config["behavioral_rules"]
                    if rules:
                        system_prompt_parts.append("\nBehavioral rules:")
                        for rule in rules:
                            system_prompt_parts.append(f"- {rule}")
                
                system_prompt = "\n".join(system_prompt_parts)
                
            else:
                # Old flat format
                name = config.get("name") or Path(file_path).stem
                description = config.get("description", "")
                system_prompt = config.get("system_prompt", "")
            
            # Create proper config for load_personality
            proper_config = {
                "name": name,
                "description": description,
                "system_prompt": system_prompt,
                "metadata": config.get("metadata", {})
            }
            
            return await self.load_personality(name, proper_config)
            
        except Exception as e:
            logger.error(f"Failed to load personality from file {file_path}: {e}")
            raise PersonalityError(f"Failed to load personality from file {file_path}: {e}")
    
    async def load_personalities_from_directory(self, directory: Optional[str] = None) -> List[str]:
        """
        Load all personalities from a directory.
        
        Args:
            directory: Directory to load from (defaults to personalities_dir)
            
        Returns:
            List of loaded personality names
        """
        directory = directory or self.personalities_dir
        loaded_names = []
        
        try:
            personalities_path = Path(directory)
            if not personalities_path.exists():
                logger.warning(f"Personalities directory not found: {directory}")
                return loaded_names
            
            # Find all JSON files
            json_files = list(personalities_path.glob("*.json"))
            
            for json_file in json_files:
                try:
                    personality = await self.load_personality_from_file(str(json_file))
                    loaded_names.append(personality.name)
                except Exception as e:
                    logger.error(f"Failed to load personality from {json_file}: {e}")
                    continue
            
            logger.info(f"Loaded {len(loaded_names)} personalities from {directory}")
            return loaded_names
            
        except Exception as e:
            logger.error(f"Failed to load personalities from directory {directory}: {e}")
            raise PersonalityError(f"Failed to load personalities from directory {directory}: {e}")
    
    async def get_personality(self, name: str) -> Optional[PersonalityData]:
        """
        Get a personality by name.
        
        Args:
            name: Personality name
            
        Returns:
            Personality data or None if not found
        """
        async with self._lock:
            return self._personalities.get(name)
    
    async def list_personalities(self) -> List[str]:
        """
        List all loaded personality names.
        
        Returns:
            List of personality names
        """
        async with self._lock:
            return list(self._personalities.keys())
    
    async def delete_personality(self, name: str) -> bool:
        """
        Delete a personality.
        
        Args:
            name: Personality name
            
        Returns:
            True if personality was deleted
        """
        async with self._lock:
            if name in self._personalities:
                del self._personalities[name]
                logger.info(f"Deleted personality: {name}")
                return True
        
        return False
    
    async def update_personality(self, name: str, config: Dict[str, Any]) -> bool:
        """
        Update a personality configuration.
        
        Args:
            name: Personality name
            config: New personality configuration
            
        Returns:
            True if personality was updated
        """
        try:
            # Validate new configuration
            await self._validator.validate_personality_config(config)
            
            # Create updated personality data
            personality = PersonalityData(
                name=name,
                description=config.get("description", ""),
                system_prompt=config.get("system_prompt", ""),
                name_override=config.get("name_override"),
                description_override=config.get("description_override"),
                metadata=config.get("metadata", {})
            )
            
            # Validate personality data
            validate_personality_data(personality)
            
            # Update in memory
            async with self._lock:
                self._personalities[name] = personality
            
            logger.info(f"Updated personality: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update personality {name}: {e}")
            raise PersonalityError(f"Failed to update personality {name}: {e}")
    
    async def get_personality_info(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get personality information.
        
        Args:
            name: Personality name
            
        Returns:
            Personality information or None if not found
        """
        personality = await self.get_personality(name)
        if not personality:
            return None
        
        return {
            "name": personality.name,
            "description": personality.description,
            "system_prompt_length": len(personality.system_prompt),
            "name_override": personality.name_override,
            "description_override": personality.description_override,
            "metadata": personality.metadata,
        }
    
    async def search_personalities(self, query: str) -> List[str]:
        """
        Search personalities by name or description.
        
        Args:
            query: Search query
            
        Returns:
            List of matching personality names
        """
        query_lower = query.lower()
        matching_names = []
        
        async with self._lock:
            for name, personality in self._personalities.items():
                # Search in name
                if query_lower in name.lower():
                    matching_names.append(name)
                    continue
                
                # Search in description
                if query_lower in personality.description.lower():
                    matching_names.append(name)
                    continue
                
                # Search in system prompt
                if query_lower in personality.system_prompt.lower():
                    matching_names.append(name)
                    continue
        
        return matching_names
    
    async def validate_personality(self, name: str) -> Dict[str, Any]:
        """
        Validate a personality configuration.
        
        Args:
            name: Personality name
            
        Returns:
            Validation results
        """
        personality = await self.get_personality(name)
        if not personality:
            return {"valid": False, "errors": [f"Personality not found: {name}"]}
        
        try:
            # Validate personality data
            validate_personality_data(personality)
            
            # Additional validation
            await self._validator.validate_personality_data(personality)
            
            return {"valid": True, "errors": []}
            
        except Exception as e:
            return {"valid": False, "errors": [str(e)]}
    
    async def export_personality(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Export a personality to a dictionary.
        
        Args:
            name: Personality name
            
        Returns:
            Personality configuration dictionary or None if not found
        """
        personality = await self.get_personality(name)
        if not personality:
            return None
        
        return {
            "name": personality.name,
            "description": personality.description,
            "system_prompt": personality.system_prompt,
            "name_override": personality.name_override,
            "description_override": personality.description_override,
            "metadata": personality.metadata,
            "exported_at": datetime.utcnow().isoformat(),
        }
    
    async def import_personality(self, config: Dict[str, Any]) -> str:
        """
        Import a personality from a configuration dictionary.
        
        Args:
            config: Personality configuration
            
        Returns:
            Imported personality name
        """
        name = config.get("name")
        if not name:
            raise PersonalityError("Personality name is required")
        
        await self.load_personality(name, config)
        return name
    
    async def get_personality_stats(self) -> Dict[str, Any]:
        """
        Get statistics about loaded personalities.
        
        Returns:
            Statistics dictionary
        """
        async with self._lock:
            total_personalities = len(self._personalities)
            
            if total_personalities == 0:
                return {
                    "total_personalities": 0,
                    "average_description_length": 0,
                    "average_system_prompt_length": 0,
                    "personalities_with_overrides": 0,
                }
            
            total_desc_length = sum(len(p.description) for p in self._personalities.values())
            total_prompt_length = sum(len(p.system_prompt) for p in self._personalities.values())
            personalities_with_overrides = sum(
                1 for p in self._personalities.values()
                if p.name_override or p.description_override
            )
            
            return {
                "total_personalities": total_personalities,
                "average_description_length": total_desc_length / total_personalities,
                "average_system_prompt_length": total_prompt_length / total_personalities,
                "personalities_with_overrides": personalities_with_overrides,
                "personality_names": list(self._personalities.keys()),
            }
    
    async def clear_all_personalities(self) -> int:
        """
        Clear all loaded personalities.
        
        Returns:
            Number of personalities cleared
        """
        async with self._lock:
            count = len(self._personalities)
            self._personalities.clear()
        
        logger.info(f"Cleared {count} personalities")
        return count
