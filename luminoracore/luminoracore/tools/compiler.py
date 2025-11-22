"""
Personality compiler for LuminoraCore.
"""

import json
import hashlib
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import logging
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache

from ..core.personality import Personality, PersonalityError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"
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
    
    def __init__(self, cache_size: int = 128):
        """
        Initialize the compiler.
        
        Args:
            cache_size: Maximum number of compiled results to cache
        """
        self.providers = {
            LLMProvider.OPENAI: self._compile_openai,
            LLMProvider.ANTHROPIC: self._compile_anthropic,
            LLMProvider.DEEPSEEK: self._compile_deepseek,
            LLMProvider.LLAMA: self._compile_llama,
            LLMProvider.MISTRAL: self._compile_mistral,
            LLMProvider.COHERE: self._compile_cohere,
            LLMProvider.GOOGLE: self._compile_google,
            LLMProvider.UNIVERSAL: self._compile_universal,
        }
        self._cache = {}
        self._cache_size = cache_size
        self._cache_hits = 0
        self._cache_misses = 0
    
    def compile_system_prompt(self, personality: Personality, include_examples: bool = True) -> str:
        """
        Convert personality into a system prompt for LLMs.
        
        This is the CRITICAL method that makes personalities actually work.
        It transforms the JSON personality definition into a coherent system prompt
        that guides the LLM's behavior.
        
        Args:
            personality: Personality object to compile
            include_examples: Whether to include example interactions
            
        Returns:
            Complete system prompt as string
        """
        prompt_parts = []
        
        # 1. Identity and role
        prompt_parts.append(f"You are {personality.persona.name}.")
        prompt_parts.append(f"{personality.persona.description}")
        
        # 2. Core traits
        if personality.core_traits and len(personality.core_traits) > 0:
            prompt_parts.append("\n## Your Core Personality Traits:")
            for trait in personality.core_traits:
                prompt_parts.append(f"- {trait}")
        
        # 3. Linguistic profile
        if personality.linguistic_profile:
            prompt_parts.append("\n## Your Communication Style:")
            
            # Tone
            if personality.linguistic_profile.tone:
                tones = ", ".join(personality.linguistic_profile.tone)
                prompt_parts.append(f"- Tone: {tones}")
            
            # Formality level
            if personality.linguistic_profile.formality_level:
                prompt_parts.append(f"- Formality: {personality.linguistic_profile.formality_level}")
            
            # Response length preference
            if personality.linguistic_profile.response_length:
                prompt_parts.append(f"- Response length: {personality.linguistic_profile.response_length}")
            
            # Vocabulary preferences
            if personality.linguistic_profile.vocabulary and len(personality.linguistic_profile.vocabulary) > 0:
                vocab_sample = ", ".join(personality.linguistic_profile.vocabulary[:10])
                prompt_parts.append(f"- Preferred vocabulary: {vocab_sample}")
            
            # Speech patterns
            if personality.linguistic_profile.speech_patterns and len(personality.linguistic_profile.speech_patterns) > 0:
                prompt_parts.append(f"- Speech patterns:")
                for pattern in personality.linguistic_profile.speech_patterns[:5]:
                    prompt_parts.append(f"  • \"{pattern}\"")
        
        # 4. Behavioral rules
        if personality.behavioral_rules and len(personality.behavioral_rules) > 0:
            prompt_parts.append("\n## Behavioral Guidelines:")
            for i, rule in enumerate(personality.behavioral_rules, 1):
                prompt_parts.append(f"{i}. {rule}")
        
        # 5. Trigger responses (if available)
        if hasattr(personality, 'trigger_responses') and personality.trigger_responses:
            triggers = personality.trigger_responses
            
            if hasattr(triggers, 'on_greeting') and triggers.on_greeting:
                prompt_parts.append("\n## How to respond to greetings:")
                for greeting in triggers.on_greeting[:3]:
                    prompt_parts.append(f"- \"{greeting}\"")
            
            if hasattr(triggers, 'on_confusion') and triggers.on_confusion:
                prompt_parts.append("\n## How to handle confusion:")
                for response in triggers.on_confusion[:2]:
                    prompt_parts.append(f"- \"{response}\"")
        
        # 6. Safety guards (if available)
        if hasattr(personality, 'safety_guards') and personality.safety_guards:
            guards = personality.safety_guards
            
            if hasattr(guards, 'forbidden_topics') and guards.forbidden_topics:
                prompt_parts.append("\n## Topics to avoid:")
                for topic in guards.forbidden_topics:
                    prompt_parts.append(f"- {topic}")
        
        # 7. Examples (if requested and available)
        if include_examples and hasattr(personality, 'examples') and personality.examples:
            examples = personality.examples
            if hasattr(examples, 'sample_responses') and examples.sample_responses:
                prompt_parts.append("\n## Example Interactions:")
                for i, example in enumerate(examples.sample_responses[:3], 1):
                    if hasattr(example, 'input') and hasattr(example, 'output'):
                        prompt_parts.append(f"\nExample {i}:")
                        prompt_parts.append(f"User: {example.input}")
                        prompt_parts.append(f"You: {example.output}")
        
        # 8. Advanced parameters guidance
        if personality.advanced_parameters:
            params = personality.advanced_parameters
            prompt_parts.append("\n## Response Style Guidance:")
            
            if hasattr(params, 'temperature'):
                if params.temperature < 0.3:
                    prompt_parts.append("- Be precise, consistent, and focused")
                elif params.temperature > 0.7:
                    prompt_parts.append("- Be creative, varied, and exploratory")
            
            if hasattr(params, 'response_length'):
                if params.response_length == "concise":
                    prompt_parts.append("- Keep responses brief and to the point")
                elif params.response_length == "detailed":
                    prompt_parts.append("- Provide thorough, comprehensive responses")
        
        # 9. Final instruction
        prompt_parts.append("\n## Important:")
        prompt_parts.append("Stay in character at all times. Your responses should consistently reflect your personality traits, communication style, and behavioral guidelines.")
        
        return "\n".join(prompt_parts)
    
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
            
            # Generate cache key
            cache_key = self._generate_cache_key(personality_obj, provider, max_tokens)
            
            # Check cache first
            if cache_key in self._cache:
                self._cache_hits += 1
                logger.debug(f"Cache hit for {personality_obj.persona.name} -> {provider.value}")
                return self._cache[cache_key]
            
            self._cache_misses += 1
            
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
            
            result = CompilationResult(
                provider=provider,
                prompt=prompt,
                token_estimate=token_estimate,
                metadata=metadata
            )
            
            # Cache the result
            self._cache_result(cache_key, result)
            
            return result
            
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
    
    def _compile_deepseek(self, personality: Personality, max_tokens: Optional[int] = None) -> tuple:
        """Compile for DeepSeek models."""
        system_prompt = self._build_system_prompt(personality)
        
        # DeepSeek uses OpenAI-compatible messages format
        prompt = {
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                }
            ],
            "model": "deepseek-chat",  # Default model
            "temperature": self._get_temperature(personality),
            "max_tokens": max_tokens
        }
        
        metadata = {
            "format": "messages",
            "model": "deepseek-chat",
            "temperature": prompt["temperature"]
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
    
    @lru_cache(maxsize=64)
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
    
    def _generate_cache_key(self, personality: Personality, provider: LLMProvider, max_tokens: Optional[int]) -> str:
        """Generate a cache key for the compilation."""
        # Create a hash of the personality data and compilation parameters
        data = {
            'personality_hash': hashlib.md5(json.dumps(personality.to_dict(), sort_keys=True).encode()).hexdigest(),
            'provider': provider.value,
            'max_tokens': max_tokens
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:16]
    
    def _cache_result(self, cache_key: str, result: CompilationResult) -> None:
        """Cache a compilation result."""
        # Remove oldest entries if cache is full
        if len(self._cache) >= self._cache_size:
            # Remove the first (oldest) entry
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        
        self._cache[cache_key] = result
        logger.debug(f"Cached compilation result for key: {cache_key}")
    
    def clear_cache(self) -> None:
        """Clear the compilation cache."""
        self._cache.clear()
        self._cache_hits = 0
        self._cache_misses = 0
        logger.info("Compilation cache cleared")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self._cache_hits + self._cache_misses
        hit_rate = (self._cache_hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'cache_size': len(self._cache),
            'max_cache_size': self._cache_size,
            'cache_hits': self._cache_hits,
            'cache_misses': self._cache_misses,
            'hit_rate': round(hit_rate, 2),
            'total_requests': total_requests
        }
