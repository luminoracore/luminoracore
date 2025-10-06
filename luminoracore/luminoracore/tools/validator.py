"""
Personality validator for LuminoraCore.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
import logging
from dataclasses import dataclass

from ..core.schema import PersonalitySchema
from ..core.personality import Personality, PersonalityError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of personality validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]


class PersonalityValidator:
    """Validates personalities against schema and best practices."""
    
    def __init__(self, schema_path: Optional[str] = None, enable_performance_checks: bool = True):
        """
        Initialize the validator.
        
        Args:
            schema_path: Path to the schema file. If None, uses default schema.
            enable_performance_checks: Enable performance-related validations
        """
        self.schema = PersonalitySchema(schema_path)
        self.enable_performance_checks = enable_performance_checks
        self.validation_rules = self._load_validation_rules()
    
    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load additional validation rules beyond schema validation."""
        return {
            "coherence_rules": {
                "archetype_behavior_mismatch": [
                    ("scientist", ["always maintain a professional demeanor"]),
                    ("adventurer", ["transform every task into an exciting adventure"]),
                    ("caregiver", ["always speak with warmth and genuine care"]),
                ],
                "temperament_communication_mismatch": [
                    ("energetic", ["casual", "conversational"]),
                    ("serious", ["formal", "technical"]),
                    ("playful", ["casual", "conversational"]),
                ]
            },
            "quality_rules": {
                "min_examples": 2,
                "min_behavioral_rules": 3,
                "max_behavioral_rule_length": 200,
                "min_description_length": 10,
                "max_description_length": 500,
            }
        }
    
    def validate(self, personality_data: Union[Dict[str, Any], str, Path]) -> ValidationResult:
        """
        Validate personality data.
        
        Args:
            personality_data: Dictionary, file path, or Personality object
            
        Returns:
            ValidationResult with validation status and feedback
        """
        errors = []
        warnings = []
        suggestions = []
        
        try:
            # Load personality data
            if isinstance(personality_data, (str, Path)):
                with open(personality_data, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            elif isinstance(personality_data, Personality):
                data = personality_data.to_dict()
            else:
                data = personality_data
            
            # Schema validation
            try:
                self.schema.validate(data)
                logger.info("Schema validation passed")
            except PersonalityError as e:
                errors.append(f"Schema validation failed: {e}")
                return ValidationResult(False, errors, warnings, suggestions)
            
            # Additional quality validations
            self._validate_quality(data, errors, warnings, suggestions)
            
            # Coherence validations
            self._validate_coherence(data, errors, warnings, suggestions)
            
            # Security validations
            self._validate_security(data, errors, warnings, suggestions)
            
            # Performance validations
            if self.enable_performance_checks:
                performance_warnings = self._validate_performance(data)
                warnings.extend(performance_warnings)
                
                efficiency_suggestions = self._validate_token_efficiency(data)
                suggestions.extend(efficiency_suggestions)
            
            is_valid = len(errors) == 0
            
            if is_valid:
                logger.info("All validations passed")
            else:
                logger.warning(f"Validation failed with {len(errors)} errors")
            
            return ValidationResult(is_valid, errors, warnings, suggestions)
            
        except Exception as e:
            error_msg = f"Validation error: {e}"
            logger.error(error_msg)
            return ValidationResult(False, [error_msg], warnings, suggestions)
    
    def _validate_quality(self, data: Dict[str, Any], errors: List[str], warnings: List[str], suggestions: List[str]) -> None:
        """Validate quality aspects of the personality."""
        rules = self.validation_rules["quality_rules"]
        
        # Check description length (warn, not error)
        description = data.get("persona", {}).get("description", "")
        if len(description) < rules["min_description_length"]:
            warnings.append(f"Description is short; aim for at least {rules['min_description_length']} characters")
        elif len(description) > rules["max_description_length"]:
            warnings.append(f"Description quite long ({len(description)} characters)")
        
        # Check behavioral rules
        behavioral_rules = data.get("behavioral_rules", [])
        if len(behavioral_rules) < rules["min_behavioral_rules"]:
            warnings.append(f"Consider adding more behavioral rules (minimum {rules['min_behavioral_rules']} recommended)")
        
        for i, rule in enumerate(behavioral_rules):
            if len(rule) > rules["max_behavioral_rule_length"]:
                warnings.append(f"Behavioral rule {i+1} is quite long ({len(rule)} characters)")
        
        # Check examples
        examples = data.get("examples", {}).get("sample_responses", [])
        if len(examples) < rules["min_examples"]:
            warnings.append(f"Consider adding more examples (minimum {rules['min_examples']} recommended)")
        
        # Check vocabulary diversity
        vocabulary = data.get("linguistic_profile", {}).get("vocabulary", [])
        if len(vocabulary) < 5:
            suggestions.append("Consider adding more characteristic vocabulary words")
        
        # Check trigger responses
        trigger_responses = data.get("trigger_responses", {})
        for trigger_type in ["on_greeting", "on_confusion", "on_success", "on_error", "on_goodbye"]:
            if trigger_type not in trigger_responses:
                suggestions.append(f"Consider adding {trigger_type} responses for better personality expression")
    
    def _validate_coherence(self, data: Dict[str, Any], errors: List[str], warnings: List[str], suggestions: List[str]) -> None:
        """Validate coherence between different personality aspects."""
        core_traits = data.get("core_traits", {})
        archetype = core_traits.get("archetype")
        temperament = core_traits.get("temperament")
        communication_style = core_traits.get("communication_style")
        behavioral_rules = data.get("behavioral_rules", [])
        
        # Check archetype-behavioral rules coherence
        if archetype and behavioral_rules:
            archetype_rules = self.validation_rules["coherence_rules"]["archetype_behavior_mismatch"]
            for expected_archetype, expected_behaviors in archetype_rules:
                if archetype == expected_archetype:
                    has_expected_behavior = any(
                        any(expected_behavior.lower() in rule.lower() for rule in behavioral_rules)
                        for expected_behavior in expected_behaviors
                    )
                    if not has_expected_behavior:
                        suggestions.append(f"Consider adding behavioral rules that align with the {archetype} archetype")
        
        # Check temperament-communication style coherence
        if temperament and communication_style:
            temperament_matches = self.validation_rules["coherence_rules"]["temperament_communication_mismatch"]
            for expected_temperament, expected_styles in temperament_matches:
                if temperament == expected_temperament and communication_style not in expected_styles:
                    suggestions.append(f"Communication style '{communication_style}' might not align well with temperament '{temperament}'")
        
        # Check tone consistency
        linguistic_profile = data.get("linguistic_profile", {})
        tone = linguistic_profile.get("tone", [])
        if temperament == "energetic" and "energetic" not in tone:
            suggestions.append("Consider adding 'energetic' to tone list to match temperament")
        elif temperament == "calm" and "calm" not in tone:
            suggestions.append("Consider adding 'calm' to tone list to match temperament")
    
    def _validate_security(self, data: Dict[str, Any], errors: List[str], warnings: List[str], suggestions: List[str]) -> None:
        """Validate security and safety aspects."""
        # Check for potentially harmful content
        behavioral_rules = data.get("behavioral_rules", [])
        for rule in behavioral_rules:
            if any(harmful_word in rule.lower() for harmful_word in ["harm", "hurt", "dangerous", "illegal"]):
                warnings.append("Behavioral rule contains potentially concerning language")
        
        # Check safety guards
        safety_guards = data.get("safety_guards", {})
        if not safety_guards:
            suggestions.append("Consider adding safety guards for responsible AI usage")
        
        # Check forbidden topics
        forbidden_topics = safety_guards.get("forbidden_topics", [])
        if not forbidden_topics:
            suggestions.append("Consider specifying forbidden topics for safety")
        
        # Check content filters
        content_filters = safety_guards.get("content_filters", [])
        if not content_filters:
            suggestions.append("Consider adding content filters for appropriate usage")
    
    def validate_file(self, file_path: Union[str, Path]) -> ValidationResult:
        """
        Validate a personality file.
        
        Args:
            file_path: Path to the personality JSON file
            
        Returns:
            ValidationResult with validation status and feedback
        """
        return self.validate(file_path)
    
    def validate_directory(self, directory_path: Union[str, Path]) -> Dict[str, ValidationResult]:
        """
        Validate all personality files in a directory.
        
        Args:
            directory_path: Path to directory containing personality files
            
        Returns:
            Dictionary mapping filenames to validation results
        """
        results = {}
        directory = Path(directory_path)
        
        if not directory.exists():
            logger.error(f"Directory not found: {directory_path}")
            return results
        
        json_files = list(directory.glob("*.json"))
        if not json_files:
            logger.warning(f"No JSON files found in {directory_path}")
            return results
        
        for file_path in json_files:
            logger.info(f"Validating {file_path.name}")
            results[file_path.name] = self.validate(file_path)
        
        return results
    
    def get_validation_summary(self, results: Dict[str, ValidationResult]) -> Dict[str, Any]:
        """
        Get a summary of validation results.
        
        Args:
            results: Dictionary of validation results
            
        Returns:
            Summary statistics and issues
        """
        total_files = len(results)
        valid_files = sum(1 for result in results.values() if result.is_valid)
        invalid_files = total_files - valid_files
        
        total_errors = sum(len(result.errors) for result in results.values())
        total_warnings = sum(len(result.warnings) for result in results.values())
        total_suggestions = sum(len(result.suggestions) for result in results.values())
        
        return {
            "total_files": total_files,
            "valid_files": valid_files,
            "invalid_files": invalid_files,
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "total_suggestions": total_suggestions,
            "validation_rate": valid_files / total_files if total_files > 0 else 0
        }
    
    def _validate_performance(self, personality_data: Dict[str, Any]) -> List[str]:
        """Validate performance-related aspects of the personality."""
        warnings = []
        
        if not self.enable_performance_checks:
            return warnings
        
        # Check for large vocabulary lists that might slow down compilation
        linguistic = personality_data.get("linguistic_profile", {})
        vocabulary = linguistic.get("vocabulary", [])
        if len(vocabulary) > 50:
            warnings.append(f"Large vocabulary list ({len(vocabulary)} items) may impact compilation performance")
        
        # Check for excessive behavioral rules
        behavioral_rules = personality_data.get("behavioral_rules", [])
        if len(behavioral_rules) > 20:
            warnings.append(f"Many behavioral rules ({len(behavioral_rules)}) may impact prompt generation speed")
        
        # Check for large examples
        examples = personality_data.get("examples", {})
        sample_responses = examples.get("sample_responses", [])
        if len(sample_responses) > 10:
            warnings.append(f"Many example responses ({len(sample_responses)}) may impact compilation performance")
        
        # Check for very long descriptions
        description = personality_data.get("persona", {}).get("description", "")
        if len(description) > 500:
            warnings.append("Very long description may impact token efficiency")
        
        # Check for excessive trigger responses
        trigger_responses = personality_data.get("trigger_responses", {})
        total_triggers = sum(len(responses) for responses in trigger_responses.values() if isinstance(responses, list))
        if total_triggers > 20:
            warnings.append(f"Many trigger responses ({total_triggers}) may impact compilation performance")
        
        return warnings
    
    def _validate_token_efficiency(self, personality_data: Dict[str, Any]) -> List[str]:
        """Validate token efficiency of the personality."""
        suggestions = []
        
        if not self.enable_performance_checks:
            return suggestions
        
        # Check for redundant information
        persona = personality_data.get("persona", {})
        core_traits = personality_data.get("core_traits", {})
        
        # Check if archetype is mentioned in both persona and core_traits
        persona_archetype = persona.get("archetype", "").lower()
        core_archetype = core_traits.get("archetype", "").lower()
        if persona_archetype and core_archetype and persona_archetype == core_archetype:
            suggestions.append("Archetype mentioned in both persona and core_traits - consider consolidating")
        
        # Check for very long behavioral rules
        behavioral_rules = personality_data.get("behavioral_rules", [])
        long_rules = [rule for rule in behavioral_rules if len(rule) > 200]
        if long_rules:
            suggestions.append(f"Consider shortening {len(long_rules)} long behavioral rules for better token efficiency")
        
        # Check for excessive vocabulary
        linguistic = personality_data.get("linguistic_profile", {})
        vocabulary = linguistic.get("vocabulary", [])
        if len(vocabulary) > 30:
            suggestions.append("Consider reducing vocabulary list to most essential terms for better token efficiency")
        
        return suggestions
