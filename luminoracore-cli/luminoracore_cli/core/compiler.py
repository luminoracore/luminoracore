"""Personality compiler for LuminoraCore CLI."""

import json
from typing import Dict, Any, Optional
from datetime import datetime

from luminoracore_cli.utils.errors import CLIError


class PersonalityCompiler:
    """Compiles personalities to provider-specific prompts."""
    
    def __init__(self):
        """Initialize the compiler."""
        self.providers = {
            "openai": self._compile_openai,
            "anthropic": self._compile_anthropic,
            "google": self._compile_google,
            "cohere": self._compile_cohere,
            "huggingface": self._compile_huggingface
        }
    
    def compile(
        self,
        personality_data: Dict[str, Any],
        provider: str,
        model: Optional[str] = None,
        include_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        Compile personality to provider-specific prompt.
        
        Args:
            personality_data: Personality data to compile
            provider: Target LLM provider
            model: Specific model (optional)
            include_metadata: Include compilation metadata
        
        Returns:
            Compilation result dictionary
        """
        try:
            # Validate provider
            if provider not in self.providers:
                raise CLIError(f"Unsupported provider: {provider}")
            
            # Get compilation function
            compile_func = self.providers[provider]
            
            # Compile personality
            prompt = compile_func(personality_data, model)
            
            # Create result
            result = {
                "prompt": prompt,
                "provider": provider,
                "model": model,
                "personality_name": personality_data.get("persona", {}).get("name", "Unknown"),
                "compiled_at": datetime.now().isoformat()
            }
            
            # Add metadata if requested
            if include_metadata:
                result["metadata"] = {
                    "personality_version": personality_data.get("persona", {}).get("version", "Unknown"),
                    "archetype": personality_data.get("persona", {}).get("archetype", "Unknown"),
                    "compilation_method": "luminoracore_cli",
                    "source_file": "unknown"
                }
            
            return result
            
        except Exception as e:
            raise CLIError(f"Compilation failed: {e}")
    
    def _compile_openai(self, personality_data: Dict[str, Any], model: Optional[str] = None) -> str:
        """Compile personality for OpenAI models."""
        persona = personality_data.get("persona", {})
        core_traits = personality_data.get("core_traits", {})
        linguistic = personality_data.get("linguistic_profile", {})
        rules = personality_data.get("behavioral_rules", [])
        
        # Build system prompt
        prompt_parts = []
        
        # Basic identity
        prompt_parts.append(f"You are {persona.get('name', 'an AI assistant')}.")
        
        if persona.get('description'):
            prompt_parts.append(f"Description: {persona['description']}")
        
        # Core traits
        if core_traits.get('temperament'):
            prompt_parts.append(f"Temperament: {core_traits['temperament']}")
        
        if core_traits.get('communication_style'):
            prompt_parts.append(f"Communication style: {core_traits['communication_style']}")
        
        # Values and motivations
        if core_traits.get('values'):
            values = ', '.join(core_traits['values'])
            prompt_parts.append(f"Core values: {values}")
        
        if core_traits.get('motivations'):
            motivations = ', '.join(core_traits['motivations'])
            prompt_parts.append(f"Motivations: {motivations}")
        
        # Linguistic profile
        if linguistic.get('tone'):
            tone = ', '.join(linguistic['tone'])
            prompt_parts.append(f"Tone: {tone}")
        
        if linguistic.get('formality_level'):
            prompt_parts.append(f"Formality level: {linguistic['formality_level']}")
        
        if linguistic.get('response_length'):
            prompt_parts.append(f"Response length: {linguistic['response_length']}")
        
        # Behavioral rules
        if rules:
            prompt_parts.append("Behavioral rules:")
            for i, rule in enumerate(rules, 1):
                prompt_parts.append(f"{i}. {rule}")
        
        # Join parts
        system_prompt = "\n".join(prompt_parts)
        
        return system_prompt
    
    def _compile_anthropic(self, personality_data: Dict[str, Any], model: Optional[str] = None) -> str:
        """Compile personality for Anthropic Claude models."""
        persona = personality_data.get("persona", {})
        core_traits = personality_data.get("core_traits", {})
        linguistic = personality_data.get("linguistic_profile", {})
        rules = personality_data.get("behavioral_rules", [])
        
        # Build system prompt for Claude
        prompt_parts = []
        
        # Header
        prompt_parts.append(f"# {persona.get('name', 'AI Assistant')}")
        
        if persona.get('description'):
            prompt_parts.append(f"\n{persona['description']}")
        
        # Core traits section
        prompt_parts.append("\n## Core Traits")
        
        if core_traits.get('temperament'):
            prompt_parts.append(f"- **Temperament**: {core_traits['temperament']}")
        
        if core_traits.get('communication_style'):
            prompt_parts.append(f"- **Communication Style**: {core_traits['communication_style']}")
        
        if core_traits.get('values'):
            values = ', '.join(core_traits['values'])
            prompt_parts.append(f"- **Values**: {values}")
        
        if core_traits.get('motivations'):
            motivations = ', '.join(core_traits['motivations'])
            prompt_parts.append(f"- **Motivations**: {motivations}")
        
        # Linguistic profile section
        prompt_parts.append("\n## Linguistic Profile")
        
        if linguistic.get('tone'):
            tone = ', '.join(linguistic['tone'])
            prompt_parts.append(f"- **Tone**: {tone}")
        
        if linguistic.get('formality_level'):
            prompt_parts.append(f"- **Formality**: {linguistic['formality_level']}")
        
        if linguistic.get('response_length'):
            prompt_parts.append(f"- **Response Length**: {linguistic['response_length']}")
        
        # Behavioral rules section
        if rules:
            prompt_parts.append("\n## Behavioral Rules")
            for rule in rules:
                prompt_parts.append(f"- {rule}")
        
        # Join parts
        system_prompt = "\n".join(prompt_parts)
        
        return system_prompt
    
    def _compile_google(self, personality_data: Dict[str, Any], model: Optional[str] = None) -> str:
        """Compile personality for Google models."""
        # Similar to OpenAI but with Google-specific formatting
        return self._compile_openai(personality_data, model)
    
    def _compile_cohere(self, personality_data: Dict[str, Any], model: Optional[str] = None) -> str:
        """Compile personality for Cohere models."""
        # Similar to OpenAI but with Cohere-specific formatting
        return self._compile_openai(personality_data, model)
    
    def _compile_huggingface(self, personality_data: Dict[str, Any], model: Optional[str] = None) -> str:
        """Compile personality for Hugging Face models."""
        # Similar to OpenAI but with Hugging Face-specific formatting
        return self._compile_openai(personality_data, model)
