"""Mistral provider for LuminoraCore SDK."""

from typing import Any, Dict, List, Optional, AsyncGenerator
import logging

from .base import BaseProvider
from ..types.provider import ProviderConfig, ChatMessage, ChatResponse
from ..utils.exceptions import ProviderError

logger = logging.getLogger(__name__)


class MistralProvider(BaseProvider):
    """Mistral provider implementation."""
    
    def __init__(self, config: Optional[ProviderConfig] = None, **kwargs):
        """
        Initialize Mistral provider.
        
        Args:
            config: Provider configuration (preferred)
            **kwargs: Alternative initialization parameters for backward compatibility
        """
        if config is None:
            # Create config from kwargs for backward compatibility
            from ..types.provider import ProviderConfig
            config = ProviderConfig(
                name=kwargs.get('name', 'mistral'),
                api_key=kwargs.get('api_key'),
                model=kwargs.get('model', 'mistral-tiny'),
                base_url=kwargs.get('base_url'),
                extra=kwargs.get('extra', {})
            )
        
        super().__init__(config)
    
    def get_default_model(self) -> str:
        """Get the default Mistral model."""
        return "mistral-tiny"
    
    async def chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatResponse:
        """
        Send a chat request to Mistral.
        
        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Mistral-specific parameters
            
        Returns:
            Chat response from Mistral
        """
        url = f"{self.base_url or 'https://api.mistral.ai/v1'}/chat/completions"
        
        params = self.get_request_params(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        try:
            response_data = await self.make_request(url, data=params)
            
            if "choices" not in response_data or not response_data["choices"]:
                raise ProviderError("Invalid response from Mistral API")
            
            choice = response_data["choices"][0]
            message = choice["message"]
            
            return ChatResponse(
                content=message["content"],
                role=message["role"],
                finish_reason=choice.get("finish_reason"),
                usage=response_data.get("usage"),
                model=response_data.get("model"),
                provider_metadata=response_data
            )
            
        except Exception as e:
            if isinstance(e, ProviderError):
                raise e
            raise ProviderError(f"Mistral API error: {e}")
    
    async def stream_chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[ChatResponse, None]:
        """
        Stream a chat request to Mistral.
        
        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Mistral-specific parameters
            
        Yields:
            Chat response chunks from Mistral
        """
        url = f"{self.base_url or 'https://api.mistral.ai/v1'}/chat/completions"
        
        params = self.get_request_params(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
            **kwargs
        )
        
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
                                
                                if "choices" in chunk_data and chunk_data["choices"]:
                                    choice = chunk_data["choices"][0]
                                    delta = choice.get("delta", {})
                                    
                                    if "content" in delta:
                                        yield ChatResponse(
                                            content=delta["content"],
                                            role=delta.get("role", "assistant"),
                                            finish_reason=choice.get("finish_reason"),
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
            raise ProviderError(f"Mistral streaming error: {e}")
    
    def get_request_params(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get request parameters for Mistral.
        
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
        
        # Mistral-specific parameters
        if "stream" in kwargs:
            params["stream"] = kwargs["stream"]
        
        if "top_p" in kwargs:
            params["top_p"] = kwargs["top_p"]
        
        if "random_seed" in kwargs:
            params["random_seed"] = kwargs["random_seed"]
        
        if "safe_prompt" in kwargs:
            params["safe_prompt"] = kwargs["safe_prompt"]
        
        return params
