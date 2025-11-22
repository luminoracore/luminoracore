"""Anthropic provider for LuminoraCore SDK."""

from typing import Any, Dict, List, Optional, AsyncGenerator
import logging

from .base import BaseProvider
from ..types.provider import ProviderConfig, ChatMessage, ChatResponse
from ..utils.exceptions import ProviderError

logger = logging.getLogger(__name__)


class AnthropicProvider(BaseProvider):
    """Anthropic provider implementation."""
    
    def __init__(self, config: Optional[ProviderConfig] = None, **kwargs):
        """
        Initialize Anthropic provider.
        
        Args:
            config: Provider configuration (preferred)
            **kwargs: Alternative initialization parameters for backward compatibility
        """
        if config is None:
            # Create config from kwargs for backward compatibility
            from ..types.provider import ProviderConfig
            config = ProviderConfig(
                name=kwargs.get('name', 'anthropic'),
                api_key=kwargs.get('api_key'),
                model=kwargs.get('model', 'claude-3-sonnet-20240229'),
                base_url=kwargs.get('base_url'),
                extra=kwargs.get('extra', {})
            )
        
        super().__init__(config)
    
    def get_default_model(self) -> str:
        """Get the default Anthropic model."""
        return "claude-3-sonnet-20240229"
    
    def format_messages(self, messages: List[ChatMessage]) -> List[Dict[str, Any]]:
        """
        Format messages for Anthropic API.
        
        Args:
            messages: List of chat messages
            
        Returns:
            Formatted messages for Anthropic
        """
        formatted = []
        for message in messages:
            # Anthropic uses 'user' and 'assistant' roles
            role = "user" if message.role == "user" else "assistant"
            formatted.append({
                "role": role,
                "content": message.content
            })
        return formatted
    
    async def chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatResponse:
        """
        Send a chat request to Anthropic.
        
        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Anthropic-specific parameters
            
        Returns:
            Chat response from Anthropic
        """
        url = f"{self.base_url or 'https://api.anthropic.com/v1'}/messages"
        
        # Anthropic requires a system message and user messages
        system_message = None
        user_messages = []
        
        for message in messages:
            if message.role == "system":
                system_message = message.content
            else:
                user_messages.append(message)
        
        params = {
            "model": self.model,
            "max_tokens": max_tokens or 1000,
            "temperature": temperature,
            "messages": self.format_messages(user_messages),
        }
        
        if system_message:
            params["system"] = system_message
        
        # Anthropic-specific parameters
        if "top_p" in kwargs:
            params["top_p"] = kwargs["top_p"]
        
        if "top_k" in kwargs:
            params["top_k"] = kwargs["top_k"]
        
        if "stop_sequences" in kwargs:
            params["stop_sequences"] = kwargs["stop_sequences"]
        
        try:
            response_data = await self.make_request(url, data=params)
            
            if "content" not in response_data or not response_data["content"]:
                raise ProviderError("Invalid response from Anthropic API")
            
            content = response_data["content"][0]["text"]
            
            return ChatResponse(
                content=content,
                role="assistant",
                finish_reason=response_data.get("stop_reason"),
                usage=response_data.get("usage"),
                model=response_data.get("model"),
                provider_metadata=response_data
            )
            
        except Exception as e:
            if isinstance(e, ProviderError):
                raise e
            raise ProviderError(f"Anthropic API error: {e}")
    
    async def stream_chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[ChatResponse, None]:
        """
        Stream a chat request to Anthropic.
        
        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Anthropic-specific parameters
            
        Yields:
            Chat response chunks from Anthropic
        """
        url = f"{self.base_url or 'https://api.anthropic.com/v1'}/messages"
        
        # Anthropic requires a system message and user messages
        system_message = None
        user_messages = []
        
        for message in messages:
            if message.role == "system":
                system_message = message.content
            else:
                user_messages.append(message)
        
        params = {
            "model": self.model,
            "max_tokens": max_tokens or 1000,
            "temperature": temperature,
            "messages": self.format_messages(user_messages),
            "stream": True,
        }
        
        if system_message:
            params["system"] = system_message
        
        # Anthropic-specific parameters
        if "top_p" in kwargs:
            params["top_p"] = kwargs["top_p"]
        
        if "top_k" in kwargs:
            params["top_k"] = kwargs["top_k"]
        
        if "stop_sequences" in kwargs:
            params["stop_sequences"] = kwargs["stop_sequences"]
        
        try:
            import aiohttp
            
            headers = self.get_headers()
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(url, headers=headers, json=params) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise ProviderError(f"HTTP {response.status}: {error_text}")
                    
                    async for line in response.content:
                        line = line.decode('utf-8').strip()
                        
                        if line.startswith('data: '):
                            data = line[6:]  # Remove 'data: ' prefix
                            
                            if data == '[DONE]':
                                break
                            
                            try:
                                import json
                                chunk_data = json.loads(data)
                                
                                if chunk_data.get("type") == "content_block_delta":
                                    delta = chunk_data.get("delta", {})
                                    if "text" in delta:
                                        yield ChatResponse(
                                            content=delta["text"],
                                            role="assistant",
                                            finish_reason=chunk_data.get("stop_reason"),
                                            usage=chunk_data.get("usage"),
                                            model=chunk_data.get("model"),
                                            provider_metadata=chunk_data,
                                            is_streaming=True
                                        )
                            except json.JSONDecodeError:
                                logger.warning(f"Failed to parse streaming chunk: {data}")
                                continue
                                
        except Exception as e:
            if isinstance(e, ProviderError):
                raise e
            raise ProviderError(f"Anthropic streaming error: {e}")
    
    def get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for Anthropic."""
        return {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }
