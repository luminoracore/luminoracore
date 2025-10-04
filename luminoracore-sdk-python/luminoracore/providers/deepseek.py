"""DeepSeek provider for LuminoraCore SDK."""

from typing import Any, Dict, List, Optional, AsyncGenerator
import logging

from .base import BaseProvider
from ..types.provider import ProviderConfig, ChatMessage, ChatResponse
from ..utils.exceptions import ProviderError

logger = logging.getLogger(__name__)


class DeepSeekProvider(BaseProvider):
    """
    DeepSeek provider implementation.
    
    DeepSeek is a cost-effective LLM provider that uses an OpenAI-compatible API.
    It's particularly popular among developers for its low pricing.
    """
    
    def get_default_model(self) -> str:
        """Get the default DeepSeek model."""
        return "deepseek-chat"
    
    async def chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatResponse:
        """
        Send a chat request to DeepSeek.
        
        Args:
            messages: List of chat messages
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional DeepSeek-specific parameters
            
        Returns:
            Chat response from DeepSeek
        """
        url = f"{self.base_url or 'https://api.deepseek.com/v1'}/chat/completions"
        
        params = self.get_request_params(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        try:
            response_data = await self.make_request(url, data=params)
            
            if "choices" not in response_data or not response_data["choices"]:
                raise ProviderError("Invalid response from DeepSeek API")
            
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
            raise ProviderError(f"DeepSeek API error: {e}")
    
    async def stream_chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[ChatResponse, None]:
        """
        Stream a chat request to DeepSeek.
        
        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional DeepSeek-specific parameters
            
        Yields:
            Chat response chunks from DeepSeek
        """
        url = f"{self.base_url or 'https://api.deepseek.com/v1'}/chat/completions"
        
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
            raise ProviderError(f"DeepSeek streaming error: {e}")
    
    def get_request_params(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get request parameters for DeepSeek.
        
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
        
        # DeepSeek-specific parameters (OpenAI-compatible)
        if "stream" in kwargs:
            params["stream"] = kwargs["stream"]
        
        if "top_p" in kwargs:
            params["top_p"] = kwargs["top_p"]
        
        if "frequency_penalty" in kwargs:
            params["frequency_penalty"] = kwargs["frequency_penalty"]
        
        if "presence_penalty" in kwargs:
            params["presence_penalty"] = kwargs["presence_penalty"]
        
        if "stop" in kwargs:
            params["stop"] = kwargs["stop"]
        
        return params

