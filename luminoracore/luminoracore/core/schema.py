"""
JSON Schema validation for LuminoraCore personalities.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import jsonschema
from jsonschema import validate, ValidationError

def _raise_personality_error(message: str):
    """Raise the shared PersonalityError without causing import cycles."""
    from .personality import PersonalityError  # local import to avoid circular dependency
    raise PersonalityError(message)


class PersonalitySchema:
    """Handles JSON Schema validation for personalities."""
    
    def __init__(self, schema_path: Optional[str] = None):
        """
        Initialize the schema validator.
        
        Args:
            schema_path: Path to the schema file. If None, uses default schema.
        """
        if schema_path is None:
            # Get the schema from the package
            package_dir = Path(__file__).parent.parent
            schema_path = package_dir / "schema" / "personality.schema.json"
        
        self.schema_path = Path(schema_path)
        self._schema = None
        self._load_schema()
    
    def _load_schema(self) -> None:
        """Load the JSON schema from file."""
        try:
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                self._schema = json.load(f)
        except FileNotFoundError:
            _raise_personality_error(f"Schema file not found: {self.schema_path}")
        except json.JSONDecodeError as e:
            _raise_personality_error(f"Invalid JSON schema: {e}")
    
    def validate(self, personality_data: Dict[str, Any]) -> bool:
        """
        Validate personality data against the schema.
        
        Args:
            personality_data: Dictionary containing personality data
            
        Returns:
            True if validation passes
            
        Raises:
            PersonalityError: If validation fails
        """
        try:
            validate(instance=personality_data, schema=self._schema)
            return True
        except ValidationError as e:
            _raise_personality_error(f"Schema validation failed: {e.message}")
    
    def get_schema(self) -> Dict[str, Any]:
        """Get the loaded schema."""
        return self._schema.copy()
    
    def validate_file(self, file_path: str) -> bool:
        """
        Validate a personality file against the schema.
        
        Args:
            file_path: Path to the personality JSON file
            
        Returns:
            True if validation passes
            
        Raises:
            PersonalityError: If validation fails
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                personality_data = json.load(f)
            return self.validate(personality_data)
        except FileNotFoundError:
            _raise_personality_error(f"Personality file not found: {file_path}")
        except json.JSONDecodeError as e:
            _raise_personality_error(f"Invalid JSON in personality file: {e}")
