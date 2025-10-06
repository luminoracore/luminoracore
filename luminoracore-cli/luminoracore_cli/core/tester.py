"""Personality tester for LuminoraCore CLI."""

import asyncio
import os
import sys
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Add SDK to path for imports
sdk_path = Path(__file__).parent.parent.parent.parent / "luminoracore-sdk-python"
sys.path.insert(0, str(sdk_path))

from luminoracore_cli.utils.errors import CLIError
from luminoracore_cli.utils.console import console


class PersonalityTester:
    """Tests personalities with real LLM providers."""
    
    def __init__(self):
        """Initialize the tester."""
        self.sdk_client = None
        self._initialize_sdk()
    
    def _initialize_sdk(self):
        """Initialize the SDK client."""
        try:
            from luminoracore import LuminoraCoreClient
            self.sdk_client = LuminoraCoreClient()
        except ImportError as e:
            console.print(f"[yellow]Warning: Could not import SDK: {e}[/yellow]")
            console.print("[yellow]Testing will use mock responses[/yellow]")
            self.sdk_client = None
    
    async def test(
        self,
        personality_data: Dict[str, Any],
        provider: str,
        model: Optional[str] = None,
        test_message: str = "Hello, how are you?"
    ) -> Dict[str, Any]:
        """
        Test personality with a real LLM provider.
        
        Args:
            personality_data: Personality data to test
            provider: LLM provider to use
            model: Specific model (optional)
            test_message: Test message to send
        
        Returns:
            Test result dictionary
        """
        try:
            # Check if we have API key
            api_key = self._get_api_key(provider)
            if not api_key:
                return await self._test_mock(personality_data, provider, model, test_message)
            
            # Use real SDK if available
            if self.sdk_client:
                return await self._test_real(personality_data, provider, model, test_message, api_key)
            else:
                return await self._test_mock(personality_data, provider, model, test_message)
            
        except Exception as e:
            console.print(f"[yellow]Real testing failed, using mock: {e}[/yellow]")
            return await self._test_mock(personality_data, provider, model, test_message)
    
    def _get_api_key(self, provider: str) -> Optional[str]:
        """Get API key for provider from environment."""
        key_mapping = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY", 
            "google": "GOOGLE_API_KEY",
            "cohere": "COHERE_API_KEY",
            "mistral": "MISTRAL_API_KEY"
        }
        
        env_var = key_mapping.get(provider.lower())
        if env_var:
            return os.getenv(env_var)
        return None
    
    async def _test_real(
        self,
        personality_data: Dict[str, Any],
        provider: str,
        model: Optional[str],
        test_message: str,
        api_key: str
    ) -> Dict[str, Any]:
        """Test with real SDK."""
        try:
            # Configure provider
            from luminoracore.types.provider import ProviderConfig
            
            provider_config = ProviderConfig(
                name=provider,
                api_key=api_key,
                model=model or self._get_default_model(provider),
                extra={"timeout": 30, "max_retries": 3}
            )
            
            # Create session
            session = await self.sdk_client.create_session(
                personality=personality_data,
                provider_config=provider_config
            )
            
            # Send message
            response = await session.send_message(test_message)
            
            return {
                "success": True,
                "response": response.content,
                "usage": response.usage,
                "model_used": response.model,
                "provider": provider,
                "test_message": test_message,
                "tested_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise CLIError(f"Real testing failed: {e}")
    
    async def _test_mock(
        self,
        personality_data: Dict[str, Any],
        provider: str,
        model: Optional[str],
        test_message: str
    ) -> Dict[str, Any]:
        """Test with mock response."""
        personality_name = personality_data.get('persona', {}).get('name', 'AI Assistant')
        
        # Generate contextual response based on personality
        if "scientist" in personality_name.lower() or "dr" in personality_name.lower():
            response = f"🔬 Fascinating! As {personality_name}, I'm excited to explore this question: '{test_message}'. Let me analyze this from a scientific perspective..."
        elif "pirate" in personality_name.lower() or "captain" in personality_name.lower():
            response = f"🏴‍☠️ Ahoy! {personality_name} here! '{test_message}' - that be a fine question, matey! Let me tell ye what I know..."
        elif "grandma" in personality_name.lower() or "abuela" in personality_name.lower():
            response = f"💕 Oh my dear, {personality_name} is so happy to hear from you! '{test_message}' - let me share some wisdom with you..."
        else:
            response = f"Hello! I'm {personality_name}. You asked: '{test_message}'. Let me help you with that!"
        
        return {
            "success": True,
            "response": response,
            "usage": {
                "prompt_tokens": 50,
                "completion_tokens": 30,
                "total_tokens": 80
            },
            "model_used": model or self._get_default_model(provider),
            "provider": provider,
            "test_message": test_message,
            "tested_at": datetime.now().isoformat(),
            "note": "Mock response - set API key for real testing"
        }
    
    def _get_default_model(self, provider: str) -> str:
        """Get default model for provider."""
        defaults = {
            "openai": "gpt-3.5-turbo",
            "anthropic": "claude-3-sonnet",
            "google": "gemini-pro",
            "cohere": "command",
            "mistral": "mistral-medium"
        }
        return defaults.get(provider.lower(), "gpt-3.5-turbo")
