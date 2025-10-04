"""Google provider for LuminoraCore SDK."""

from typing import Any, Dict, List, Optional, AsyncGenerator
import logging

from .base import BaseProvider
from ..types.provider import ProviderConfig, ChatMessage, ChatResponse
from ..utils.exceptions import ProviderError

logger = logging.getLogger(__name__)


class GoogleProvider(BaseProvider):
    """Google provider implementation."""
    
    def get_default_model(self) -> str:
        """Get the default Google model."""
        return "gemini-pro"
    
    async def chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatResponse:
        """
        Send a chat request to Google.
        
        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Google-specific parameters
            
        Returns:
            Chat response from Google
        """
        url = f"{self.base_url or 'https://generativelanguage.googleapis.com/v1beta'}/models/{self.model}:generateContent"
        
        # Convert messages to Google format
        contents = []
        for message in messages:
            if message.role == "user":
                contents.append({
                    "role": "user",
                    "parts": [{"text": message.content}]
                })
            elif message.role == "assistant":
                contents.append({
                    "role": "model",
                    "parts": [{"text": message.content}]
                })
        
        params = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens or 1000,
            }
        }
        
        # Google-specific parameters
        if "safetySettings" in kwargs:
            params["safetySettings"] = kwargs["safetySettings"]
        
        if "tools" in kwargs:
            params["tools"] = kwargs["tools"]
        
        if "systemInstruction" in kwargs:
            params["systemInstruction"] = kwargs["systemInstruction"]
        
        try:
            response_data = await self.make_request(url, data=params)
            
            if "candidates" not in response_data or not response_data["candidates"]:
                raise ProviderError("Invalid response from Google API")
            
            candidate = response_data["candidates"][0]
            content = candidate["content"]["parts"][0]["text"]
            
            return ChatResponse(
                content=content,
                role="assistant",
                finish_reason=candidate.get("finishReason"),
                usage=response_data.get("usageMetadata"),
                model=response_data.get("model"),
                provider_metadata=response_data
            )
            
        except Exception as e:
            if isinstance(e, ProviderError):
                raise e
            raise ProviderError(f"Google API error: {e}")
    
    async def stream_chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[ChatResponse, None]:
        """
        Stream a chat request to Google.
        
        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Google-specific parameters
            
        Yields:
            Chat response chunks from Google
        """
        url = f"{self.base_url or 'https://generativelanguage.googleapis.com/v1beta'}/models/{self.model}:streamGenerateContent"
        
        # Convert messages to Google format
        contents = []
        for message in messages:
            if message.role == "user":
                contents.append({
                    "role": "user",
                    "parts": [{"text": message.content}]
                })
            elif message.role == "assistant":
                contents.append({
                    "role": "model",
                    "parts": [{"text": message.content}]
                })
        
        params = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens or 1000,
            }
        }
        
        # Google-specific parameters
        if "safetySettings" in kwargs:
            params["safetySettings"] = kwargs["safetySettings"]
        
        if "tools" in kwargs:
            params["tools"] = kwargs["tools"]
        
        if "systemInstruction" in kwargs:
            params["systemInstruction"] = kwargs["systemInstruction"]
        
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
                                
                                if "candidates" in chunk_data and chunk_data["candidates"]:
                                    candidate = chunk_data["candidates"][0]
                                    if "content" in candidate and "parts" in candidate["content"]:
                                        for part in candidate["content"]["parts"]:
                                            if "text" in part:
                                                yield ChatResponse(
                                                    content=part["text"],
                                                    role="assistant",
                                                    finish_reason=candidate.get("finishReason"),
                                                    usage=chunk_data.get("usageMetadata"),
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
            raise ProviderError(f"Google streaming error: {e}")
