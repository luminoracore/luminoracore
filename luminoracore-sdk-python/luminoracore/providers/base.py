"""Base provider class for LuminoraCore SDK."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, AsyncGenerator
import asyncio
import logging
import sys
from pathlib import Path

# Add Core to path for imports
core_path = Path(__file__).parent.parent.parent.parent / "luminoracore"
if str(core_path) not in sys.path:
    sys.path.insert(0, str(core_path))

from ..types.provider import ProviderConfig, ChatMessage, ChatResponse
from ..utils.exceptions import ProviderError
from ..utils.retry import async_retry

logger = logging.getLogger(__name__)


class BaseProvider(ABC):
    """Base class for all LLM providers."""
    
    def __init__(self, config: ProviderConfig):
        """
        Initialize the provider.
        
        Args:
            config: Provider configuration
        """
        self.config = config
        self.name = config.name
        self.api_key = config.api_key
        self.base_url = config.base_url
        self.timeout = config.extra.get("timeout", 30.0) if config.extra else 30.0
        self.max_retries = config.extra.get("max_retries", 3) if config.extra else 3
        self.model = config.model or self.get_default_model()
        
        # Validate configuration
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate provider configuration."""
        if not self.api_key:
            raise ProviderError("API key is required")
        
        if not self.model:
            raise ProviderError("Model is required")
    
    @abstractmethod
    def get_default_model(self) -> str:
        """Get the default model for this provider."""
        pass
    
    @abstractmethod
    async def chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatResponse:
        """
        Send a chat request to the provider.
        
        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Chat response from the provider
        """
        pass
    
    @abstractmethod
    async def stream_chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[ChatResponse, None]:
        """
        Stream a chat request to the provider.
        
        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters
            
        Yields:
            Chat response chunks from the provider
        """
        pass
    
    async def chat_with_retry(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatResponse:
        """
        Send a chat request with retry logic.
        
        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Chat response from the provider
        """
        return await async_retry(
            self.chat,
            max_attempts=self.max_retries,
            delay=1.0,
            backoff_factor=2.0,
            exceptions=(ProviderError,),
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
    
    async def stream_chat_with_retry(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[ChatResponse, None]:
        """
        Stream a chat request with retry logic.
        
        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters
            
        Yields:
            Chat response chunks from the provider
        """
        # For streaming, we'll retry the entire stream if it fails
        try:
            async for chunk in self.stream_chat(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            ):
                yield chunk
        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            raise ProviderError(f"Streaming failed: {e}")
    
    async def chat_with_personality(
        self,
        personality_data: Dict[str, Any],
        user_message: str,
        conversation_history: Optional[List[ChatMessage]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatResponse:
        """
        Chat with LLM applying a personality.
        
        THIS IS THE KEY METHOD that makes personalities actually work!
        It uses compile_system_prompt() to convert personality JSON into
        a system prompt that guides the LLM's behavior.
        
        Args:
            personality_data: Personality data dictionary
            user_message: User's message
            conversation_history: Previous conversation messages
            temperature: Sampling temperature (overrides personality default)
            max_tokens: Maximum tokens (overrides personality default)
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Chat response with personality applied
        """
        try:
            # Import Core components
            from luminoracore import Personality, PersonalityCompiler
            
            # Load personality
            personality = Personality(personality_data)
            
            # Compile system prompt
            compiler = PersonalityCompiler()
            system_prompt = compiler.compile_system_prompt(personality, include_examples=True)
            
            logger.info(f"Applying personality: {personality.persona.name}")
            logger.debug(f"System prompt length: {len(system_prompt)} chars")
            
            # Build message list
            messages = []
            
            # Add system prompt
            messages.append(ChatMessage(role="system", content=system_prompt))
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current user message
            messages.append(ChatMessage(role="user", content=user_message))
            
            # Use personality's advanced parameters if not overridden
            if temperature is None and personality.advanced_parameters:
                temperature = getattr(personality.advanced_parameters, 'temperature', 0.7)
            
            if max_tokens is None and personality.advanced_parameters:
                max_tokens = getattr(personality.advanced_parameters, 'max_tokens', None)
            
            # Call the provider's chat method
            response = await self.chat(
                messages=messages,
                temperature=temperature or 0.7,
                max_tokens=max_tokens,
                **kwargs
            )
            
            logger.info(f"Response generated with personality: {personality.persona.name}")
            
            return response
            
        except ImportError as e:
            logger.error(f"Failed to import LuminoraCore: {e}")
            raise ProviderError(f"LuminoraCore not available: {e}")
        except Exception as e:
            logger.error(f"Failed to apply personality: {e}")
            raise ProviderError(f"Personality application failed: {e}")
    
    async def stream_chat_with_personality(
        self,
        personality_data: Dict[str, Any],
        user_message: str,
        conversation_history: Optional[List[ChatMessage]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[ChatResponse, None]:
        """
        Stream chat with LLM applying a personality.
        
        Args:
            personality_data: Personality data dictionary
            user_message: User's message
            conversation_history: Previous conversation messages
            temperature: Sampling temperature (overrides personality default)
            max_tokens: Maximum tokens (overrides personality default)
            **kwargs: Additional provider-specific parameters
            
        Yields:
            Chat response chunks with personality applied
        """
        try:
            # Import Core components
            from luminoracore import Personality, PersonalityCompiler
            
            # Load personality
            personality = Personality(personality_data)
            
            # Compile system prompt
            compiler = PersonalityCompiler()
            system_prompt = compiler.compile_system_prompt(personality, include_examples=False)
            
            logger.info(f"Streaming with personality: {personality.persona.name}")
            
            # Build message list
            messages = []
            
            # Add system prompt
            messages.append(ChatMessage(role="system", content=system_prompt))
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current user message
            messages.append(ChatMessage(role="user", content=user_message))
            
            # Use personality's advanced parameters if not overridden
            if temperature is None and personality.advanced_parameters:
                temperature = getattr(personality.advanced_parameters, 'temperature', 0.7)
            
            if max_tokens is None and personality.advanced_parameters:
                max_tokens = getattr(personality.advanced_parameters, 'max_tokens', None)
            
            # Stream from the provider
            async for chunk in self.stream_chat(
                messages=messages,
                temperature=temperature or 0.7,
                max_tokens=max_tokens,
                **kwargs
            ):
                yield chunk
            
            logger.info(f"Streaming completed with personality: {personality.persona.name}")
            
        except ImportError as e:
            logger.error(f"Failed to import LuminoraCore: {e}")
            raise ProviderError(f"LuminoraCore not available: {e}")
        except Exception as e:
            logger.error(f"Failed to stream with personality: {e}")
            raise ProviderError(f"Personality streaming failed: {e}")
    
    def format_messages(self, messages: List[ChatMessage]) -> List[Dict[str, Any]]:
        """
        Format messages for the provider.
        
        Args:
            messages: List of chat messages
            
        Returns:
            Formatted messages for the provider
        """
        formatted = []
        for message in messages:
            formatted.append({
                "role": message.role,
                "content": message.content
            })
        return formatted
    
    def get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for the provider."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
    
    def get_request_params(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get request parameters for the provider.
        
        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters
            
        Returns:
            Request parameters
        """
        params = {
            "model": self.model,
            "messages": self.format_messages(messages),
            "temperature": temperature,
        }
        
        if max_tokens:
            params["max_tokens"] = max_tokens
        
        # Add provider-specific parameters
        params.update(kwargs)
        
        return params
    
    async def make_request(
        self,
        url: str,
        method: str = "POST",
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the provider.
        
        Args:
            url: Request URL
            method: HTTP method
            headers: HTTP headers
            data: Request data
            params: Query parameters
            
        Returns:
            Response data
            
        Raises:
            ProviderError: If request fails
        """
        import aiohttp
        
        if headers is None:
            headers = self.get_headers()
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                    params=params
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        raise ProviderError(
                            f"HTTP {response.status}: {error_text}",
                            error_code=f"HTTP_{response.status}"
                        )
        except aiohttp.ClientError as e:
            raise ProviderError(f"Request failed: {e}", error_code="REQUEST_FAILED")
        except Exception as e:
            raise ProviderError(f"Unexpected error: {e}", error_code="UNEXPECTED_ERROR")
    
    def __str__(self) -> str:
        """String representation of the provider."""
        return f"{self.__class__.__name__}(name={self.name}, model={self.model})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the provider."""
        return (
            f"{self.__class__.__name__}("
            f"name={self.name}, "
            f"model={self.model}, "
            f"base_url={self.base_url}, "
            f"timeout={self.timeout}, "
            f"max_retries={self.max_retries})"
        )
