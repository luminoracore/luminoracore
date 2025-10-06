"""
Personality validation module for LuminoraCore CLI.

This module provides comprehensive validation for personality files,
ensuring they conform to the LuminoraCore schema and best practices.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel, ValidationError, field_validator, ConfigDict
from rich.console import Console

from ..utils.errors import ValidationError as CLIValidationError
from ..utils.files import read_json_file, read_yaml_file


class ValidationLevel(Enum):
    """Validation severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationResult:
    """Result of a validation check."""
    level: ValidationLevel
    message: str
    field: Optional[str] = None
    suggestion: Optional[str] = None


class PersonalitySchema(BaseModel):
    """Pydantic model for personality validation."""
    
    # Core personality data (required)
    persona: Dict[str, Any]
    
    # All other fields are optional
    name: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    tags: Optional[List[str]] = None
    core_traits: Optional[Union[List[str], Dict[str, Any]]] = None
    linguistic_profile: Optional[Dict[str, Any]] = None
    behavioral_rules: Optional[List[str]] = None
    advanced_parameters: Optional[Dict[str, Any]] = None
    
    # Allow extra fields
    model_config = ConfigDict(extra="allow")
    
    # Validation methods
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        if len(v) > 100:
            raise ValueError('Name is too long (max 100 characters)')
        return v.strip()
    
    @field_validator('version')
    @classmethod
    def validate_version(cls, v):
        if not v or not v.strip():
            raise ValueError('Version cannot be empty')
        # Basic semantic versioning check
        parts = v.split('.')
        if len(parts) < 2:
            raise ValueError('Version should follow semantic versioning (e.g., 1.0.0)')
        return v.strip()
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if not v or not v.strip():
            raise ValueError('Description cannot be empty')
        if len(v) < 10:
            raise ValueError('Description should be at least 10 characters')
        if len(v) > 500:
            raise ValueError('Description is too long (max 500 characters)')
        return v.strip()
    
    @field_validator('core_traits')
    @classmethod
    def validate_core_traits(cls, v):
        # Accept any type for core_traits
        return v
    
    @field_validator('behavioral_rules')
    @classmethod
    def validate_behavioral_rules(cls, v):
        if not v:
            raise ValueError('At least one behavioral rule is required')
        if len(v) > 50:
            raise ValueError('Too many behavioral rules (max 50)')
        return v
    
    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        if v and len(v) > 10:
            raise ValueError('Too many tags (max 10)')
        return v or []


class PersonalityValidator:
    """Main validator class for personality files."""
    
    def __init__(self, console: Optional[Console] = None):
        """Initialize the validator.
        
        Args:
            console: Optional Rich console for output
        """
        self.console = console or Console()
        self.results: List[ValidationResult] = []
    
    def validate_file(self, file_path: Union[str, Path]) -> List[ValidationResult]:
        """Validate a personality file.
        
        Args:
            file_path: Path to the personality file
            
        Returns:
            List of validation results
        """
        self.results = []
        file_path = Path(file_path)
        
        if not file_path.exists():
            self.results.append(ValidationResult(
                level=ValidationLevel.CRITICAL,
                message=f"File does not exist: {file_path}",
                field="file_path"
            ))
            return self.results
        
        # Check file extension
        if file_path.suffix not in ['.json', '.yaml', '.yml']:
            self.results.append(ValidationResult(
                level=ValidationLevel.ERROR,
                message=f"Unsupported file format: {file_path.suffix}",
                field="file_format",
                suggestion="Use .json or .yaml files"
            ))
            return self.results
        
        # Load file content
        try:
            if file_path.suffix == '.json':
                data = read_json_file(file_path)
            else:
                data = read_yaml_file(file_path)
        except Exception as e:
            self.results.append(ValidationResult(
                level=ValidationLevel.CRITICAL,
                message=f"Failed to parse file: {str(e)}",
                field="file_parsing"
            ))
            return self.results
        
        # Validate structure
        self._validate_structure(data)
        
        # Validate schema
        self._validate_schema(data)
        
        # Validate content
        self._validate_content(data)
        
        # Validate best practices
        self._validate_best_practices(data)
        
        return self.results
    
    def _validate_structure(self, data: Dict[str, Any]) -> None:
        """Validate basic file structure."""
        required_fields = ['name', 'version', 'description', 'persona', 'core_traits', 'linguistic_profile', 'behavioral_rules']
        
        for field in required_fields:
            if field not in data:
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    message=f"Missing required field: {field}",
                    field=field
                ))
        
        # Check for unexpected fields
        expected_fields = required_fields + ['author', 'tags', 'advanced_parameters']
        for field in data.keys():
            if field not in expected_fields:
                self.results.append(ValidationResult(
                    level=ValidationLevel.WARNING,
                    message=f"Unexpected field: {field}",
                    field=field,
                    suggestion="Consider removing or documenting this field"
                ))
    
    def _validate_schema(self, data: Dict[str, Any]) -> None:
        """Validate against Pydantic schema."""
        try:
            # Extract fields from persona if they exist there
            if 'persona' in data and isinstance(data['persona'], dict):
                persona = data['persona']
                # Copy fields from persona to root level for validation
                if 'name' in persona:
                    data['name'] = persona['name']
                if 'version' in persona:
                    data['version'] = persona['version']
                if 'description' in persona:
                    data['description'] = persona['description']
                if 'author' in persona:
                    data['author'] = persona['author']
                if 'tags' in persona:
                    data['tags'] = persona['tags']
            
            PersonalitySchema(**data)
        except ValidationError as e:
            for error in e.errors():
                field = '.'.join(str(x) for x in error['loc'])
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    message=error['msg'],
                    field=field
                ))
    
    def _validate_content(self, data: Dict[str, Any]) -> None:
        """Validate content quality and consistency."""
        # Validate persona structure
        if 'persona' in data:
            self._validate_persona(data['persona'])
        
        # Validate linguistic profile
        if 'linguistic_profile' in data:
            self._validate_linguistic_profile(data['linguistic_profile'])
        
        # Validate core traits
        if 'core_traits' in data:
            self._validate_core_traits(data['core_traits'])
        
        # Validate behavioral rules
        if 'behavioral_rules' in data:
            self._validate_behavioral_rules(data['behavioral_rules'])
        
        # Validate advanced parameters
        if 'advanced_parameters' in data:
            self._validate_advanced_parameters(data['advanced_parameters'])
    
    def _validate_persona(self, persona: Dict[str, Any]) -> None:
        """Validate persona structure and content."""
        if not isinstance(persona, dict):
            self.results.append(ValidationResult(
                level=ValidationLevel.ERROR,
                message="Persona must be a dictionary",
                field="persona"
            ))
            return
        
        # Check for required persona fields
        persona_fields = ['background', 'personality', 'expertise', 'communication_style']
        for field in persona_fields:
            if field not in persona:
                self.results.append(ValidationResult(
                    level=ValidationLevel.WARNING,
                    message=f"Missing recommended persona field: {field}",
                    field=f"persona.{field}",
                    suggestion="Consider adding this field for better personality definition"
                ))
        
        # Validate field content
        for field, value in persona.items():
            if isinstance(value, str) and len(value.strip()) == 0:
                self.results.append(ValidationResult(
                    level=ValidationLevel.WARNING,
                    message=f"Empty persona field: {field}",
                    field=f"persona.{field}"
                ))
    
    def _validate_linguistic_profile(self, profile: Dict[str, Any]) -> None:
        """Validate linguistic profile structure."""
        if not isinstance(profile, dict):
            self.results.append(ValidationResult(
                level=ValidationLevel.ERROR,
                message="Linguistic profile must be a dictionary",
                field="linguistic_profile"
            ))
            return
        
        # Check for common linguistic profile fields
        common_fields = ['tone', 'formality', 'vocabulary_level', 'sentence_structure']
        for field in common_fields:
            if field not in profile:
                self.results.append(ValidationResult(
                    level=ValidationLevel.INFO,
                    message=f"Missing linguistic profile field: {field}",
                    field=f"linguistic_profile.{field}",
                    suggestion="Consider adding this field for better language specification"
                ))
    
    def _validate_core_traits(self, traits) -> None:
        """Validate core traits."""
        if traits is None:
            return
        if not isinstance(traits, (list, dict)):
            self.results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                message="Core traits should be a list or dict",
                field="core_traits"
            ))
            return
        
        if isinstance(traits, list):
            for i, trait in enumerate(traits):
                if not isinstance(trait, str):
                    self.results.append(ValidationResult(
                        level=ValidationLevel.ERROR,
                        message=f"Core trait {i} must be a string",
                        field=f"core_traits[{i}]"
                    ))
                elif len(trait.strip()) == 0:
                    self.results.append(ValidationResult(
                        level=ValidationLevel.ERROR,
                        message=f"Empty core trait at index {i}",
                        field=f"core_traits[{i}]"
                    ))
                elif len(trait) > 100:
                    self.results.append(ValidationResult(
                        level=ValidationLevel.WARNING,
                        message=f"Core trait {i} is very long",
                        field=f"core_traits[{i}]",
                        suggestion="Consider shortening this trait"
                ))
    
    def _validate_behavioral_rules(self, rules: List[str]) -> None:
        """Validate behavioral rules."""
        if not isinstance(rules, list):
            self.results.append(ValidationResult(
                level=ValidationLevel.ERROR,
                message="Behavioral rules must be a list",
                field="behavioral_rules"
            ))
            return
        
        for i, rule in enumerate(rules):
            if not isinstance(rule, str):
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    message=f"Behavioral rule {i} must be a string",
                    field=f"behavioral_rules[{i}]"
                ))
            elif len(rule.strip()) == 0:
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    message=f"Empty behavioral rule at index {i}",
                    field=f"behavioral_rules[{i}]"
                ))
            elif len(rule) < 10:
                self.results.append(ValidationResult(
                    level=ValidationLevel.WARNING,
                    message=f"Behavioral rule {i} is very short",
                    field=f"behavioral_rules[{i}]",
                    suggestion="Consider providing more detail"
                ))
    
    def _validate_advanced_parameters(self, params: Dict[str, Any]) -> None:
        """Validate advanced parameters."""
        if not isinstance(params, dict):
            self.results.append(ValidationResult(
                level=ValidationLevel.ERROR,
                message="Advanced parameters must be a dictionary",
                field="advanced_parameters"
            ))
            return
        
        # Check for common advanced parameters
        common_params = ['temperature', 'max_tokens', 'top_p', 'frequency_penalty', 'presence_penalty']
        for param in common_params:
            if param in params:
                value = params[param]
                if not isinstance(value, (int, float)):
                    self.results.append(ValidationResult(
                        level=ValidationLevel.WARNING,
                        message=f"Advanced parameter '{param}' should be numeric",
                        field=f"advanced_parameters.{param}"
                    ))
    
    def _validate_best_practices(self, data: Dict[str, Any]) -> None:
        """Validate best practices and provide suggestions."""
        # Check description length
        if 'description' in data:
            desc = data['description']
            if len(desc) < 50:
                self.results.append(ValidationResult(
                    level=ValidationLevel.INFO,
                    message="Description is quite short",
                    field="description",
                    suggestion="Consider adding more detail about the personality's purpose and characteristics"
                ))
        
        # Check for author information
        if 'author' not in data:
            self.results.append(ValidationResult(
                level=ValidationLevel.INFO,
                message="No author information provided",
                field="author",
                suggestion="Consider adding author information for attribution"
            ))
        
        # Check for tags
        if 'tags' not in data or not data['tags']:
            self.results.append(ValidationResult(
                level=ValidationLevel.INFO,
                message="No tags provided",
                field="tags",
                suggestion="Consider adding tags to help categorize this personality"
            ))
    
    def get_summary(self) -> Dict[str, int]:
        """Get validation summary statistics."""
        summary = {
            'total': len(self.results),
            'critical': 0,
            'error': 0,
            'warning': 0,
            'info': 0
        }
        
        for result in self.results:
            summary[result.level.value] += 1
        
        return summary
    
    def is_valid(self) -> bool:
        """Check if the validation passed without critical errors."""
        return all(
            result.level not in [ValidationLevel.CRITICAL, ValidationLevel.ERROR]
            for result in self.results
        )
    
    def validate(self, data: Dict[str, Any], strict: bool = False) -> Dict[str, Any]:
        """Validate personality data.
        
        Args:
            data: Personality data to validate
            strict: Use strict validation rules
            
        Returns:
            Validation result dictionary
        """
        self.results = []
        
        # Validate schema
        self._validate_schema(data)
        
        # Validate content
        self._validate_content(data)
        
        # Check if validation passed
        errors = [r for r in self.results if r.level in [ValidationLevel.ERROR, ValidationLevel.CRITICAL]]
        warnings = [r for r in self.results if r.level == ValidationLevel.WARNING]
        info = [r for r in self.results if r.level == ValidationLevel.INFO]
        
        return {
            "valid": len(errors) == 0,
            "errors": [f"{r.field}: {r.message}" for r in errors],
            "warnings": [f"{r.field}: {r.message}" for r in warnings],
            "info": [f"{r.field}: {r.message}" for r in info],
            "total_issues": len(self.results)
        }
    
    async def validate_async(self, data: Dict[str, Any]) -> 'ValidationResult':
        """Async validation method for compatibility with CLI commands."""
        # Create a temporary file to validate
        import tempfile
        import json
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        
        try:
            results = self.validate_file(temp_path)
            is_valid = self.is_valid()
            
            # Create a simple result object
            class SimpleValidationResult:
                def __init__(self, is_valid: bool, errors: List[ValidationResult]):
                    self.is_valid = is_valid
                    self.errors = [r for r in errors if r.level in [ValidationLevel.CRITICAL, ValidationLevel.ERROR]]
            
            return SimpleValidationResult(is_valid, results)
        finally:
            import os
            try:
                os.unlink(temp_path)
            except:
                pass


def validate_personality_file(file_path: Union[str, Path], console: Optional[Console] = None) -> Tuple[bool, List[ValidationResult]]:
    """Convenience function to validate a personality file.
    
    Args:
        file_path: Path to the personality file
        console: Optional Rich console for output
        
    Returns:
        Tuple of (is_valid, validation_results)
    """
    validator = PersonalityValidator(console)
    results = validator.validate_file(file_path)
    return validator.is_valid(), results