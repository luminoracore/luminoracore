"""Llama provider for LuminoraCore SDK."""

from typing import Any, Dict, List, Optional, AsyncGenerator
import logging

from .base import BaseProvider
from ..types.provider import ProviderConfig, ChatMessage, ChatResponse
from ..utils.exceptions import ProviderError

logger = logging.getLogger(__name__)


class LlamaProvider(BaseProvider):
    """Llama provider implementation."""
    
    def get_default_model(self) -> str:
        """Get the default Llama model."""
        return "llama-2-7b-chat"
    
    async def chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatResponse:
        """
        Send a chat request to Llama.
        
        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Llama-specific parameters
            
        Returns:
            Chat response from Llama
        """
        url = f"{self.base_url or 'https://api.replicate.com/v1'}/predictions"
        
        # Convert messages to prompt format for Llama
        prompt = self._messages_to_prompt(messages)
        
        params = {
            "version": self.model,
            "input": {
                "prompt": prompt,
                "temperature": temperature,
                "max_new_tokens": max_tokens or 1000,
                "top_p": kwargs.get("top_p", 0.9),
                "repetition_penalty": kwargs.get("repetition_penalty", 1.0),
            }
        }
        
        try:
            response_data = await self.make_request(url, data=params)
            
            if "output" not in response_data:
                raise ProviderError("Invalid response from Llama API")
            
            output = response_data["output"]
            if isinstance(output, list):
                output = "\n".join(output)
            
            return ChatResponse(
                content=output,
                role="assistant",
                finish_reason="stop",
                usage={"prompt_tokens": len(prompt.split()), "completion_tokens": len(output.split())},
                model=self.model,
                provider_metadata=response_data
            )
            
        except Exception as e:
            if isinstance(e, ProviderError):
                raise e
            raise ProviderError(f"Llama API error: {e}")
    
    async def stream_chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[ChatResponse, None]:
        """
        Stream a chat request to Llama.
        
        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Llama-specific parameters
            
        Yields:
            Chat response chunks from Llama
        """
        # For streaming, we'll simulate it by making a regular request
        # and yielding chunks of the response
        response = await self.chat(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        # Split response into chunks
        content = response.content
        chunk_size = 50  # characters per chunk
        
        for i in range(0, len(content), chunk_size):
            chunk_content = content[i:i + chunk_size]
            yield ChatResponse(
                content=chunk_content,
                role="assistant",
                finish_reason="stop" if i + chunk_size >= len(content) else None,
                usage=response.usage,
                model=response.model,
                provider_metadata=response.provider_metadata,
                is_streaming=True
            )
    
    def _messages_to_prompt(self, messages: List[ChatMessage]) -> str:
        """
        Convert messages to prompt format for Llama.
        
        Args:
            messages: List of chat messages
            
        Returns:
            Formatted prompt string
        """
        prompt_parts = []
        
        for message in messages:
            if message.role == "system":
                prompt_parts.append(f"System: {message.content}")
            elif message.role == "user":
                prompt_parts.append(f"Human: {message.content}")
            elif message.role == "assistant":
                prompt_parts.append(f"Assistant: {message.content}")
        
        prompt_parts.append("Assistant:")
        return "\n".join(prompt_parts)
    
    def get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for Llama."""
        return {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json",
        }
