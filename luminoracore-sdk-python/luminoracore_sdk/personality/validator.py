"""Personality validation for LuminoraCore SDK."""

import re
from typing import Dict, List, Any, Optional
import logging

from ..types.personality import PersonalityData
from ..utils.exceptions import PersonalityError, ValidationError

logger = logging.getLogger(__name__)


class PersonalityValidator:
    """Validates personality configurations and data."""
    
    def __init__(self):
        """Initialize the personality validator."""
        self.max_description_length = 1000
        self.max_system_prompt_length = 10000
        self.max_name_override_length = 50
        self.max_description_override_length = 200
        self.prohibited_content = [
            "hate speech",
            "violence",
            "illegal content",
            "explicit content",
        ]
        self.required_fields = ["name", "description", "system_prompt"]
    
    async def validate_personality_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate a personality configuration dictionary.
        
        Args:
            config: Personality configuration
            
        Returns:
            True if valid
            
        Raises:
            ValidationError: If configuration is invalid
        """
        # Check required fields
        for field in self.required_fields:
            if field not in config:
                raise ValidationError(f"Required field missing: {field}")
            
            if not config[field] or not isinstance(config[field], str):
                raise ValidationError(f"Field {field} must be a non-empty string")
        
        # Validate field lengths
        if len(config["description"]) > self.max_description_length:
            raise ValidationError(
                f"Description too long: {len(config['description'])} > {self.max_description_length}"
            )
        
        if len(config["system_prompt"]) > self.max_system_prompt_length:
            raise ValidationError(
                f"System prompt too long: {len(config['system_prompt'])} > {self.max_system_prompt_length}"
            )
        
        # Validate optional fields
        if "name_override" in config and config["name_override"]:
            if len(config["name_override"]) > self.max_name_override_length:
                raise ValidationError(
                    f"Name override too long: {len(config['name_override'])} > {self.max_name_override_length}"
                )
        
        if "description_override" in config and config["description_override"]:
            if len(config["description_override"]) > self.max_description_override_length:
                raise ValidationError(
                    f"Description override too long: {len(config['description_override'])} > {self.max_description_override_length}"
                )
        
        # Validate metadata
        if "metadata" in config:
            if not isinstance(config["metadata"], dict):
                raise ValidationError("Metadata must be a dictionary")
        
        # Check for prohibited content
        await self._check_prohibited_content(config)
        
        # Validate name format
        await self._validate_name_format(config["name"])
        
        return True
    
    async def validate_personality_data(self, personality: PersonalityData) -> bool:
        """
        Validate a personality data object.
        
        Args:
            personality: Personality data object
            
        Returns:
            True if valid
            
        Raises:
            ValidationError: If personality data is invalid
        """
        # Check required fields
        if not personality.name:
            raise ValidationError("Personality name is required")
        
        if not personality.description:
            raise ValidationError("Personality description is required")
        
        if not personality.system_prompt:
            raise ValidationError("System prompt is required")
        
        # Validate field lengths
        if len(personality.description) > self.max_description_length:
            raise ValidationError(
                f"Description too long: {len(personality.description)} > {self.max_description_length}"
            )
        
        if len(personality.system_prompt) > self.max_system_prompt_length:
            raise ValidationError(
                f"System prompt too long: {len(personality.system_prompt)} > {self.max_system_prompt_length}"
            )
        
        # Validate optional fields
        if personality.name_override and len(personality.name_override) > self.max_name_override_length:
            raise ValidationError(
                f"Name override too long: {len(personality.name_override)} > {self.max_name_override_length}"
            )
        
        if personality.description_override and len(personality.description_override) > self.max_description_override_length:
            raise ValidationError(
                f"Description override too long: {len(personality.description_override)} > {self.max_description_override_length}"
            )
        
        # Check for prohibited content
        await self._check_prohibited_content_personality(personality)
        
        # Validate name format
        await self._validate_name_format(personality.name)
        
        return True
    
    async def validate_personality_blend(
        self,
        personalities: List[PersonalityData],
        weights: List[float]
    ) -> bool:
        """
        Validate a personality blend configuration.
        
        Args:
            personalities: List of personality data objects
            weights: List of weights for each personality
            
        Returns:
            True if valid
            
        Raises:
            ValidationError: If blend configuration is invalid
        """
        if len(personalities) != len(weights):
            raise ValidationError("Number of personalities must match number of weights")
        
        if len(personalities) < 2:
            raise ValidationError("At least 2 personalities required for blending")
        
        if len(personalities) > 10:
            raise ValidationError("Maximum 10 personalities allowed for blending")
        
        # Validate weights
        weight_sum = sum(weights)
        if abs(weight_sum - 1.0) > 0.01:  # Allow small floating point errors
            raise ValidationError(f"Weights must sum to 1.0, got {weight_sum}")
        
        if any(w < 0 for w in weights):
            raise ValidationError("All weights must be non-negative")
        
        if any(w > 1 for w in weights):
            raise ValidationError("All weights must be <= 1.0")
        
        # Validate individual personalities
        for personality in personalities:
            await self.validate_personality_data(personality)
        
        return True
    
    async def _check_prohibited_content(self, config: Dict[str, Any]) -> None:
        """
        Check for prohibited content in configuration.
        
        Args:
            config: Configuration to check
            
        Raises:
            ValidationError: If prohibited content is found
        """
        text_fields = ["description", "system_prompt", "name_override", "description_override"]
        
        for field in text_fields:
            if field in config and config[field]:
                content = config[field].lower()
                for prohibited in self.prohibited_content:
                    if prohibited.lower() in content:
                        raise ValidationError(f"Prohibited content found in {field}: {prohibited}")
    
    async def _check_prohibited_content_personality(self, personality: PersonalityData) -> None:
        """
        Check for prohibited content in personality data.
        
        Args:
            personality: Personality data to check
            
        Raises:
            ValidationError: If prohibited content is found
        """
        text_fields = [
            ("description", personality.description),
            ("system_prompt", personality.system_prompt),
            ("name_override", personality.name_override),
            ("description_override", personality.description_override),
        ]
        
        for field_name, field_value in text_fields:
            if field_value:
                content = field_value.lower()
                for prohibited in self.prohibited_content:
                    if prohibited.lower() in content:
                        raise ValidationError(f"Prohibited content found in {field_name}: {prohibited}")
    
    async def _validate_name_format(self, name: str) -> None:
        """
        Validate personality name format.
        
        Args:
            name: Name to validate
            
        Raises:
            ValidationError: If name format is invalid
        """
        if not name or not isinstance(name, str):
            raise ValidationError("Name must be a non-empty string")
        
        if len(name) < 2:
            raise ValidationError("Name must be at least 2 characters long")
        
        if len(name) > 100:
            raise ValidationError("Name must be 100 characters or less")
        
        # Check for valid characters (alphanumeric, spaces, hyphens, underscores)
        if not re.match(r'^[a-zA-Z0-9\s_-]+$', name):
            raise ValidationError("Name contains invalid characters")
        
        # Check for consecutive spaces
        if '  ' in name:
            raise ValidationError("Name cannot contain consecutive spaces")
        
        # Check for leading/trailing spaces
        if name != name.strip():
            raise ValidationError("Name cannot have leading or trailing spaces")
    
    async def validate_personality_file(self, file_path: str) -> Dict[str, Any]:
        """
        Validate a personality file.
        
        Args:
            file_path: Path to personality file
            
        Returns:
            Validation results
        """
        try:
            import json
            from pathlib import Path
            
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return {"valid": False, "errors": [f"File not found: {file_path}"]}
            
            if file_path_obj.suffix.lower() != '.json':
                return {"valid": False, "errors": [f"File must be a JSON file: {file_path}"]}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            await self.validate_personality_config(config)
            
            return {"valid": True, "errors": []}
            
        except json.JSONDecodeError as e:
            return {"valid": False, "errors": [f"Invalid JSON: {e}"]}
        except Exception as e:
            return {"valid": False, "errors": [str(e)]}
    
    async def validate_personality_directory(self, directory: str) -> Dict[str, Any]:
        """
        Validate all personality files in a directory.
        
        Args:
            directory: Directory to validate
            
        Returns:
            Validation results
        """
        from pathlib import Path
        
        results = {
            "valid": True,
            "total_files": 0,
            "valid_files": 0,
            "invalid_files": 0,
            "errors": []
        }
        
        try:
            personalities_path = Path(directory)
            if not personalities_path.exists():
                results["valid"] = False
                results["errors"].append(f"Directory not found: {directory}")
                return results
            
            # Find all JSON files
            json_files = list(personalities_path.glob("*.json"))
            results["total_files"] = len(json_files)
            
            for json_file in json_files:
                file_result = await self.validate_personality_file(str(json_file))
                if file_result["valid"]:
                    results["valid_files"] += 1
                else:
                    results["invalid_files"] += 1
                    results["errors"].extend([f"{json_file}: {error}" for error in file_result["errors"]])
            
            if results["invalid_files"] > 0:
                results["valid"] = False
            
            return results
            
        except Exception as e:
            results["valid"] = False
            results["errors"].append(str(e))
            return results
