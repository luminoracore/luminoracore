"""Provider factory for LuminoraCore SDK."""

from typing import Dict, Type, Optional
import logging

from .base import BaseProvider
from .openai import OpenAIProvider
from .anthropic import AnthropicProvider
from .llama import LlamaProvider
from .mistral import MistralProvider
from .cohere import CohereProvider
from .google import GoogleProvider
from ..types.provider import ProviderConfig
from ..utils.exceptions import ProviderError

logger = logging.getLogger(__name__)


class ProviderFactory:
    """Factory class for creating LLM providers."""
    
    # Registry of available providers
    _providers: Dict[str, Type[BaseProvider]] = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "llama": LlamaProvider,
        "mistral": MistralProvider,
        "cohere": CohereProvider,
        "google": GoogleProvider,
    }
    
    @classmethod
    def create_provider(cls, config: ProviderConfig) -> BaseProvider:
        """
        Create a provider instance from configuration.
        
        Args:
            config: Provider configuration
            
        Returns:
            Provider instance
            
        Raises:
            ProviderError: If provider type is not supported
        """
        provider_type = config.name.lower()
        
        if provider_type not in cls._providers:
            available = ", ".join(cls._providers.keys())
            raise ProviderError(
                f"Unsupported provider type: {provider_type}. "
                f"Available providers: {available}"
            )
        
        provider_class = cls._providers[provider_type]
        
        try:
            return provider_class(config)
        except Exception as e:
            raise ProviderError(f"Failed to create provider {provider_type}: {e}")
    
    @classmethod
    def register_provider(cls, name: str, provider_class: Type[BaseProvider]) -> None:
        """
        Register a new provider type.
        
        Args:
            name: Provider name
            provider_class: Provider class
        """
        if not issubclass(provider_class, BaseProvider):
            raise ProviderError(
                f"Provider class must inherit from BaseProvider: {provider_class}"
            )
        
        cls._providers[name.lower()] = provider_class
        logger.info(f"Registered provider: {name}")
    
    @classmethod
    def unregister_provider(cls, name: str) -> None:
        """
        Unregister a provider type.
        
        Args:
            name: Provider name
        """
        if name.lower() in cls._providers:
            del cls._providers[name.lower()]
            logger.info(f"Unregistered provider: {name}")
        else:
            logger.warning(f"Provider not found: {name}")
    
    @classmethod
    def get_available_providers(cls) -> list[str]:
        """
        Get list of available provider types.
        
        Returns:
            List of available provider names
        """
        return list(cls._providers.keys())
    
    @classmethod
    def is_provider_available(cls, name: str) -> bool:
        """
        Check if a provider type is available.
        
        Args:
            name: Provider name
            
        Returns:
            True if provider is available
        """
        return name.lower() in cls._providers
    
    @classmethod
    def get_provider_class(cls, name: str) -> Optional[Type[BaseProvider]]:
        """
        Get provider class by name.
        
        Args:
            name: Provider name
            
        Returns:
            Provider class or None if not found
        """
        return cls._providers.get(name.lower())
    
    @classmethod
    def create_provider_from_dict(cls, config_dict: Dict) -> BaseProvider:
        """
        Create a provider instance from dictionary configuration.
        
        Args:
            config_dict: Provider configuration dictionary
            
        Returns:
            Provider instance
            
        Raises:
            ProviderError: If configuration is invalid
        """
        try:
            config = ProviderConfig(**config_dict)
            return cls.create_provider(config)
        except Exception as e:
            raise ProviderError(f"Invalid provider configuration: {e}")
    
    @classmethod
    def create_provider_from_env(cls, provider_type: str, **kwargs) -> BaseProvider:
        """
        Create a provider instance from environment variables.
        
        Args:
            provider_type: Type of provider to create
            **kwargs: Additional configuration parameters
            
        Returns:
            Provider instance
            
        Raises:
            ProviderError: If provider type is not supported or configuration is invalid
        """
        import os
        
        # Get API key from environment
        api_key = kwargs.get("api_key")
        if not api_key:
            # Try to get from environment variables
            env_var = f"{provider_type.upper()}_API_KEY"
            api_key = os.getenv(env_var)
            if not api_key:
                raise ProviderError(
                    f"API key not provided and {env_var} environment variable not set"
                )
        
        config = ProviderConfig(
            name=provider_type,
            api_key=api_key,
            model=kwargs.get("model"),
            base_url=kwargs.get("base_url"),
            extra={
                "timeout": kwargs.get("timeout", 30),
                "max_retries": kwargs.get("max_retries", 3)
            }
        )
        
        return cls.create_provider(config)
    
    @classmethod
    def create_multiple_providers(cls, configs: list[ProviderConfig]) -> Dict[str, BaseProvider]:
        """
        Create multiple provider instances.
        
        Args:
            configs: List of provider configurations
            
        Returns:
            Dictionary mapping provider names to instances
        """
        providers = {}
        
        for config in configs:
            try:
                provider = cls.create_provider(config)
                providers[config.name] = provider
            except Exception as e:
                logger.error(f"Failed to create provider {config.name}: {e}")
                continue
        
        return providers
    
    @classmethod
    def get_provider_info(cls, name: str) -> Dict:
        """
        Get information about a provider.
        
        Args:
            name: Provider name
            
        Returns:
            Provider information dictionary
        """
        provider_class = cls.get_provider_class(name)
        if not provider_class:
            return {"available": False}
        
        return {
            "available": True,
            "class": provider_class.__name__,
            "module": provider_class.__module__,
            "default_model": provider_class().get_default_model() if hasattr(provider_class(), 'get_default_model') else None,
        }
