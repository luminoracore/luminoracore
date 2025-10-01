"""
Personality compiler for LuminoraCore.
"""

import json
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import logging
from dataclasses import dataclass
from enum import Enum

from ..core.personality import Personality, PersonalityError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LLAMA = "llama"
    MISTRAL = "mistral"
    COHERE = "cohere"
    GOOGLE = "google"
    UNIVERSAL = "universal"


@dataclass
class CompilationResult:
    """Result of personality compilation."""
    provider: LLMProvider
    prompt: Union[str, Dict[str, Any]]
    token_estimate: int
    metadata: Dict[str, Any]


class PersonalityCompiler:
    """Compiles personalities into provider-specific prompts."""
    
    def __init__(self):
        """Initialize the compiler."""
        self.providers = {
            LLMProvider.OPENAI: self._compile_openai,
            LLMProvider.ANTHROPIC: self._compile_anthropic,
            LLMProvider.LLAMA: self._compile_llama,
            LLMProvider.MISTRAL: self._compile_mistral,
            LLMProvider.COHERE: self._compile_cohere,
            LLMProvider.GOOGLE: self._compile_google,
            LLMProvider.UNIVERSAL: self._compile_universal,
        }
    
    def compile(self, personality: Union[Personality, Dict[str, Any]], 
                provider: LLMProvider, 
                max_tokens: Optional[int] = None) -> CompilationResult:
        """
        Compile personality for a specific provider.
        
        Args:
            personality: Personality object or dictionary
            provider: Target LLM provider
            max_tokens: Maximum token limit (optional)
            
        Returns:
            CompilationResult with compiled prompt
        """
        try:
            if isinstance(personality, dict):
                personality_obj = Personality(personality)
            else:
                personality_obj = personality
            
            # Check compatibility
            if not personality_obj.is_compatible_with(provider.value):
                logger.warning(f"Personality {personality_obj.persona.name} may not be optimized for {provider.value}")
            
            # Compile for specific provider
            if provider in self.providers:
                prompt, metadata = self.providers[provider](personality_obj, max_tokens)
            else:
                raise PersonalityError(f"Unsupported provider: {provider}")
            
            # Estimate tokens (rough approximation)
            token_estimate = self._estimate_tokens(prompt)
            
            # Check token limit
            if max_tokens and token_estimate > max_tokens:
                logger.warning(f"Prompt may exceed token limit: {token_estimate} > {max_tokens}")
            
            return CompilationResult(
                provider=provider,
                prompt=prompt,
                token_estimate=token_estimate,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Compilation failed: {e}")
            raise PersonalityError(f"Failed to compile personality: {e}")
    
    def _compile_openai(self, personality: Personality, max_tokens: Optional[int] = None) -> tuple:
        """Compile for OpenAI GPT models."""
        system_prompt = self._build_system_prompt(personality)
        
        # OpenAI uses messages format
        prompt = {
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                }
            ],
            "model": "gpt-4",  # Default model
            "temperature": self._get_temperature(personality),
            "max_tokens": max_tokens
        }
        
        metadata = {
            "format": "messages",
            "model": "gpt-4",
            "temperature": prompt["temperature"]
        }
        
        return prompt, metadata
    
    def _compile_anthropic(self, personality: Personality, max_tokens: Optional[int] = None) -> tuple:
        """Compile for Anthropic Claude models."""
        system_prompt = self._build_system_prompt(personality)
        
        # Anthropic uses specific XML tags
        prompt = f"""<system>
{system_prompt}
</system>

<human>
</human>

<assistant>
"""
        
        metadata = {
            "format": "xml",
            "model": "claude-3-sonnet",
            "max_tokens": max_tokens
        }
        
        return prompt, metadata
    
    def _compile_llama(self, personality: Personality, max_tokens: Optional[int] = None) -> tuple:
        """Compile for Llama models."""
        system_prompt = self._build_system_prompt(personality)
        
        # Llama uses simple text format
        prompt = f"""### System:
{system_prompt}

### Human:

### Assistant:
"""
        
        metadata = {
            "format": "text",
            "model": "llama-2-70b",
            "max_tokens": max_tokens
        }
        
        return prompt, metadata
    
    def _compile_mistral(self, personality: Personality, max_tokens: Optional[int] = None) -> tuple:
        """Compile for Mistral models."""
        system_prompt = self._build_system_prompt(personality)
        
        # Mistral uses messages format similar to OpenAI
        prompt = {
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                }
            ],
            "model": "mistral-large",
            "temperature": self._get_temperature(personality),
            "max_tokens": max_tokens
        }
        
        metadata = {
            "format": "messages",
            "model": "mistral-large",
            "temperature": prompt["temperature"]
        }
        
        return prompt, metadata
    
    def _compile_cohere(self, personality: Personality, max_tokens: Optional[int] = None) -> tuple:
        """Compile for Cohere models."""
        system_prompt = self._build_system_prompt(personality)
        
        # Cohere uses simple text format
        prompt = f"""System: {system_prompt}

Human: 

Assistant:"""
        
        metadata = {
            "format": "text",
            "model": "command",
            "max_tokens": max_tokens
        }
        
        return prompt, metadata
    
    def _compile_google(self, personality: Personality, max_tokens: Optional[int] = None) -> tuple:
        """Compile for Google models."""
        system_prompt = self._build_system_prompt(personality)
        
        # Google uses messages format
        prompt = {
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                }
            ],
            "model": "gemini-pro",
            "temperature": self._get_temperature(personality),
            "max_tokens": max_tokens
        }
        
        metadata = {
            "format": "messages",
            "model": "gemini-pro",
            "temperature": prompt["temperature"]
        }
        
        return prompt, metadata
    
    def _compile_universal(self, personality: Personality, max_tokens: Optional[int] = None) -> tuple:
        """Compile for universal/portable format."""
        system_prompt = self._build_system_prompt(personality)
        
        # Universal format with metadata
        prompt = {
            "system_prompt": system_prompt,
            "personality_info": {
                "name": personality.persona.name,
                "version": personality.persona.version,
                "archetype": personality.core_traits.archetype,
                "temperament": personality.core_traits.temperament,
                "communication_style": personality.core_traits.communication_style
            },
            "settings": {
                "temperature": self._get_temperature(personality),
                "max_tokens": max_tokens
            }
        }
        
        metadata = {
            "format": "universal",
            "portable": True
        }
        
        return prompt, metadata
    
    def _build_system_prompt(self, personality: Personality) -> str:
        """Build the core system prompt from personality data."""
        prompt_parts = []
        
        # Basic identity
        prompt_parts.append(f"You are {personality.persona.name}, {personality.persona.description}")
        
        # Core traits
        prompt_parts.append(f"\nCore Traits:")
        prompt_parts.append(f"- Archetype: {personality.core_traits.archetype}")
        prompt_parts.append(f"- Temperament: {personality.core_traits.temperament}")
        prompt_parts.append(f"- Communication Style: {personality.core_traits.communication_style}")
        
        # Linguistic profile
        linguistic = personality.linguistic_profile
        prompt_parts.append(f"\nLinguistic Profile:")
        prompt_parts.append(f"- Tone: {', '.join(linguistic.tone)}")
        prompt_parts.append(f"- Syntax: {linguistic.syntax}")
        if linguistic.vocabulary:
            prompt_parts.append(f"- Characteristic vocabulary: {', '.join(linguistic.vocabulary[:10])}")
        if linguistic.fillers:
            prompt_parts.append(f"- Common fillers: {', '.join(linguistic.fillers[:5])}")
        
        # Behavioral rules
        prompt_parts.append(f"\nBehavioral Rules:")
        for i, rule in enumerate(personality.behavioral_rules, 1):
            prompt_parts.append(f"{i}. {rule}")
        
        # Trigger responses
        if personality.trigger_responses:
            prompt_parts.append(f"\nTrigger Responses:")
            triggers = personality.trigger_responses
            if triggers.on_greeting:
                prompt_parts.append(f"- On greeting: {triggers.on_greeting[0]}")
            if triggers.on_confusion:
                prompt_parts.append(f"- On confusion: {triggers.on_confusion[0]}")
            if triggers.on_success:
                prompt_parts.append(f"- On success: {triggers.on_success[0]}")
            if triggers.on_error:
                prompt_parts.append(f"- On error: {triggers.on_error[0]}")
            if triggers.on_goodbye:
                prompt_parts.append(f"- On goodbye: {triggers.on_goodbye[0]}")
        
        # Advanced parameters
        if personality.advanced_parameters:
            params = personality.advanced_parameters
            prompt_parts.append(f"\nAdvanced Parameters:")
            if params.verbosity is not None:
                prompt_parts.append(f"- Verbosity: {params.verbosity:.1f}")
            if params.formality is not None:
                prompt_parts.append(f"- Formality: {params.formality:.1f}")
            if params.humor is not None:
                prompt_parts.append(f"- Humor: {params.humor:.1f}")
            if params.empathy is not None:
                prompt_parts.append(f"- Empathy: {params.empathy:.1f}")
            if params.creativity is not None:
                prompt_parts.append(f"- Creativity: {params.creativity:.1f}")
            if params.directness is not None:
                prompt_parts.append(f"- Directness: {params.directness:.1f}")
        
        # Safety guards
        if personality.safety_guards:
            safety = personality.safety_guards
            prompt_parts.append(f"\nSafety Guidelines:")
            if safety.forbidden_topics:
                prompt_parts.append(f"- Avoid topics: {', '.join(safety.forbidden_topics)}")
            if safety.content_filters:
                prompt_parts.append(f"- Content filters: {', '.join(safety.content_filters)}")
        
        # Examples
        if personality.examples and personality.examples.sample_responses:
            prompt_parts.append(f"\nExample Interactions:")
            for i, example in enumerate(personality.examples.sample_responses[:3], 1):
                prompt_parts.append(f"Example {i}:")
                prompt_parts.append(f"  Input: {example.input}")
                prompt_parts.append(f"  Output: {example.output}")
        
        return "\n".join(prompt_parts)
    
    def _get_temperature(self, personality: Personality) -> float:
        """Get appropriate temperature based on personality parameters."""
        if personality.advanced_parameters:
            creativity = personality.advanced_parameters.creativity
            if creativity is not None:
                # Map creativity (0-1) to temperature (0.1-1.0)
                return 0.1 + (creativity * 0.9)
        
        # Default based on temperament
        temperament = personality.core_traits.temperament
        if temperament == "energetic":
            return 0.8
        elif temperament == "calm":
            return 0.3
        else:
            return 0.5
    
    def _estimate_tokens(self, prompt: Union[str, Dict[str, Any]]) -> int:
        """Estimate token count for a prompt."""
        if isinstance(prompt, dict):
            # For message format, count content
            if "messages" in prompt:
                content = " ".join(msg.get("content", "") for msg in prompt["messages"])
            else:
                content = str(prompt)
        else:
            content = prompt
        
        # Rough estimation: 1 token ≈ 4 characters
        return len(content) // 4
    
    def compile_all_providers(self, personality: Union[Personality, Dict[str, Any]]) -> Dict[LLMProvider, CompilationResult]:
        """
        Compile personality for all supported providers.
        
        Args:
            personality: Personality object or dictionary
            
        Returns:
            Dictionary mapping providers to compilation results
        """
        results = {}
        
        for provider in LLMProvider:
            if provider != LLMProvider.UNIVERSAL:  # Skip universal for individual compilation
                try:
                    results[provider] = self.compile(personality, provider)
                    logger.info(f"Compiled for {provider.value}")
                except Exception as e:
                    logger.error(f"Failed to compile for {provider.value}: {e}")
        
        return results
    
    def save_compiled(self, result: CompilationResult, output_path: Union[str, Path]) -> None:
        """
        Save compiled prompt to file.
        
        Args:
            result: CompilationResult to save
            output_path: Path to save the file
        """
        output_path = Path(output_path)
        
        if isinstance(result.prompt, dict):
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result.prompt, f, indent=2, ensure_ascii=False)
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.prompt)
        
        logger.info(f"Saved compiled prompt to {output_path}")
