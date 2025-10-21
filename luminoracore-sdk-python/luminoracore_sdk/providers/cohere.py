"""Cohere provider for LuminoraCore SDK."""

from typing import Any, Dict, List, Optional, AsyncGenerator
import logging

from .base import BaseProvider
from ..types.provider import ProviderConfig, ChatMessage, ChatResponse
from ..utils.exceptions import ProviderError

logger = logging.getLogger(__name__)


class CohereProvider(BaseProvider):
    """Cohere provider implementation."""
    
    def __init__(self, config: Optional[ProviderConfig] = None, **kwargs):
        """
        Initialize Cohere provider.
        
        Args:
            config: Provider configuration (preferred)
            **kwargs: Alternative initialization parameters for backward compatibility
        """
        if config is None:
            # Create config from kwargs for backward compatibility
            from ..types.provider import ProviderConfig
            config = ProviderConfig(
                name=kwargs.get('name', 'cohere'),
                api_key=kwargs.get('api_key'),
                model=kwargs.get('model', 'command'),
                base_url=kwargs.get('base_url'),
                extra=kwargs.get('extra', {})
            )
        
        super().__init__(config)
    
    def get_default_model(self) -> str:
        """Get the default Cohere model."""
        return "command"
    
    async def chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatResponse:
        """
        Send a chat request to Cohere.
        
        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Cohere-specific parameters
            
        Returns:
            Chat response from Cohere
        """
        url = f"{self.base_url or 'https://api.cohere.ai/v1'}/chat"
        
        # Convert messages to Cohere format
        chat_history = []
        message = ""
        
        for msg in messages:
            if msg.role == "user":
                if message:  # If there's a pending message, add it to history
                    chat_history.append({"role": "user", "message": message})
                message = msg.content
            elif msg.role == "assistant":
                if message:  # If there's a pending user message, add it to history
                    chat_history.append({"role": "user", "message": message})
                    message = ""
                chat_history.append({"role": "chatbot", "message": msg.content})
        
        params = {
            "model": self.model,
            "message": message,
            "chat_history": chat_history,
            "temperature": temperature,
            "max_tokens": max_tokens or 1000,
        }
        
        # Cohere-specific parameters
        if "preamble" in kwargs:
            params["preamble"] = kwargs["preamble"]
        
        if "connectors" in kwargs:
            params["connectors"] = kwargs["connectors"]
        
        if "search_queries_only" in kwargs:
            params["search_queries_only"] = kwargs["search_queries_only"]
        
        if "documents" in kwargs:
            params["documents"] = kwargs["documents"]
        
        try:
            response_data = await self.make_request(url, data=params)
            
            if "text" not in response_data:
                raise ProviderError("Invalid response from Cohere API")
            
            return ChatResponse(
                content=response_data["text"],
                role="assistant",
                finish_reason="stop",
                usage=response_data.get("meta"),
                model=response_data.get("model"),
                provider_metadata=response_data
            )
            
        except Exception as e:
            if isinstance(e, ProviderError):
                raise e
            raise ProviderError(f"Cohere API error: {e}")
    
    async def stream_chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[ChatResponse, None]:
        """
        Stream a chat request to Cohere.
        
        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Cohere-specific parameters
            
        Yields:
            Chat response chunks from Cohere
        """
        url = f"{self.base_url or 'https://api.cohere.ai/v1'}/chat"
        
        # Convert messages to Cohere format
        chat_history = []
        message = ""
        
        for msg in messages:
            if msg.role == "user":
                if message:  # If there's a pending message, add it to history
                    chat_history.append({"role": "user", "message": message})
                message = msg.content
            elif msg.role == "assistant":
                if message:  # If there's a pending user message, add it to history
                    chat_history.append({"role": "user", "message": message})
                    message = ""
                chat_history.append({"role": "chatbot", "message": msg.content})
        
        params = {
            "model": self.model,
            "message": message,
            "chat_history": chat_history,
            "temperature": temperature,
            "max_tokens": max_tokens or 1000,
            "stream": True,
        }
        
        # Cohere-specific parameters
        if "preamble" in kwargs:
            params["preamble"] = kwargs["preamble"]
        
        if "connectors" in kwargs:
            params["connectors"] = kwargs["connectors"]
        
        if "search_queries_only" in kwargs:
            params["search_queries_only"] = kwargs["search_queries_only"]
        
        if "documents" in kwargs:
            params["documents"] = kwargs["documents"]
        
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
                                
                                if "event_type" in chunk_data and chunk_data["event_type"] == "text-generation":
                                    yield ChatResponse(
                                        content=chunk_data.get("text", ""),
                                        role="assistant",
                                        finish_reason="stop",
                                        usage=chunk_data.get("meta"),
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
            raise ProviderError(f"Cohere streaming error: {e}")
