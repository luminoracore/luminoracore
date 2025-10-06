"""Core client for LuminoraCore CLI."""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime

from luminoracore_cli.utils.errors import CLIError
from luminoracore_cli.utils.console import console
from luminoracore_cli.utils.http import create_http_client
from luminoracore_cli.utils.cache import get_cache_manager
from luminoracore_cli.config.settings import load_settings


class LuminoraCoreClient:
    """Client for interacting with LuminoraCore services."""
    
    def __init__(self, settings: Optional[Dict[str, Any]] = None):
        """
        Initialize LuminoraCore client.
        
        Args:
            settings: Optional settings override
        """
        self.settings = settings or load_settings()
        self.http_client = create_http_client(
            base_url=getattr(self.settings, "repository_url", None),
            api_key=getattr(self.settings, "api_key", None),
            timeout=getattr(self.settings, "timeout", 30),
            max_retries=getattr(self.settings, "max_retries", 3)
        )
        self.cache_manager = get_cache_manager(
            cache_dir=getattr(self.settings, "cache_dir", None)
        )
    
    async def validate_personality(self, personality_data: Dict[str, Any], strict: bool = False) -> Dict[str, Any]:
        """
        Validate personality data.
        
        Args:
            personality_data: Personality data to validate
            strict: Use strict validation rules
        
        Returns:
            Validation result dictionary
        """
        try:
            # Check cache first
            cache_key = f"validation_{hash(str(personality_data))}"
            cached_result = self.cache_manager.get(cache_key)
            
            if cached_result:
                return cached_result
            
            # Perform validation
            from luminoracore_cli.core.validator import PersonalityValidator
            
            validator = PersonalityValidator()
            result = validator.validate(personality_data, strict=strict)
            
            # Cache result
            self.cache_manager.set(cache_key, result)
            
            return result
            
        except Exception as e:
            raise CLIError(f"Validation failed: {e}")
    
    async def compile_personality(
        self,
        personality_data: Dict[str, Any],
        provider: str,
        model: Optional[str] = None,
        include_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        Compile personality to provider-specific prompt.
        
        Args:
            personality_data: Personality data to compile
            provider: Target LLM provider
            model: Specific model (optional)
            include_metadata: Include compilation metadata
        
        Returns:
            Compilation result dictionary
        """
        try:
            # Get default model if not specified
            if not model:
                model = getattr(self.settings, "default_model", "gpt-3.5-turbo")
            
            # Check cache first
            cache_key = f"compile_{hash(str(personality_data))}_{provider}_{model}"
            cached_result = self.cache_manager.get(cache_key)
            
            if cached_result:
                return cached_result
            
            # Perform compilation
            from luminoracore_cli.core.compiler import PersonalityCompiler
            
            compiler = PersonalityCompiler()
            result = compiler.compile(
                personality_data=personality_data,
                provider=provider,
                model=model,
                include_metadata=include_metadata
            )
            
            # Cache result
            self.cache_manager.set(cache_key, result)
            
            return result
            
        except Exception as e:
            raise CLIError(f"Compilation failed: {e}")
    
    async def get_personality(self, personality_id: str) -> Dict[str, Any]:
        """
        Get personality by ID.
        
        Args:
            personality_id: Personality identifier
        
        Returns:
            Personality data dictionary
        """
        try:
            # Check cache first
            cache_key = f"personality_{personality_id}"
            cached_personality = self.cache_manager.get(cache_key)
            
            if cached_personality:
                return cached_personality
            
            # Fetch from repository
            response = await self.http_client.get(f"/personalities/{personality_id}")
            
            if not response:
                raise CLIError(f"Personality '{personality_id}' not found")
            
            # Cache result
            self.cache_manager.set(cache_key, response)
            
            return response
            
        except Exception as e:
            raise CLIError(f"Failed to get personality: {e}")
    
    async def list_personalities(self) -> List[Dict[str, Any]]:
        """
        List all available personalities.
        
        Returns:
            List of personality information dictionaries
        """
        try:
            # Check cache first
            cache_key = "personalities_list"
            cached_list = self.cache_manager.get(cache_key)
            
            if cached_list:
                return cached_list
            
            # Fetch from repository
            response = await self.http_client.get("/personalities")
            
            if not response or "personalities" not in response:
                raise CLIError("Invalid response from repository")
            
            personalities = response["personalities"]
            
            # Cache result
            self.cache_manager.set(cache_key, personalities)
            
            return personalities
            
        except Exception as e:
            raise CLIError(f"Failed to list personalities: {e}")
    
    async def blend_personalities(
        self,
        personality_weights: Dict[str, float],
        custom_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Blend multiple personalities with custom weights.
        
        Args:
            personality_weights: Dictionary mapping personality IDs to weights
            custom_name: Custom name for blended personality
        
        Returns:
            Blended personality data
        """
        try:
            # Validate weights
            total_weight = sum(personality_weights.values())
            if abs(total_weight - 1.0) > 0.01:
                raise CLIError("Personality weights must sum to 1.0")
            
            # Get personalities
            personalities = []
            for personality_id, weight in personality_weights.items():
                personality = await self.get_personality(personality_id)
                personalities.append((personality, weight))
            
            # Perform blending
            from luminoracore_cli.core.blender import PersonalityBlender
            
            blender = PersonalityBlender()
            blended_personality = blender.blend(personalities, custom_name)
            
            return blended_personality
            
        except Exception as e:
            raise CLIError(f"Personality blending failed: {e}")
    
    async def test_personality(
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
            # Get default model if not specified
            if not model:
                model = getattr(self.settings, "default_model", "gpt-3.5-turbo")
            
            # Compile personality
            compilation_result = await self.compile_personality(
                personality_data=personality_data,
                provider=provider,
                model=model,
                include_metadata=True
            )
            
            # Test with provider
            from luminoracore_cli.core.tester import PersonalityTester
            
            tester = PersonalityTester()
            test_result = await tester.test(
                personality_data=personality_data,
                provider=provider,
                model=model,
                test_message=test_message
            )
            
            return {
                "compilation": compilation_result,
                "test_result": test_result,
                "provider": provider,
                "model": model,
                "test_message": test_message,
                "tested_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise CLIError(f"Personality testing failed: {e}")
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check service health.
        
        Returns:
            Health status dictionary
        """
        try:
            response = await self.http_client.get("/health")
            return response
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "checked_at": datetime.now().isoformat()
            }


def get_client(settings: Optional[Dict[str, Any]] = None) -> LuminoraCoreClient:
    """
    Get LuminoraCore client instance.
    
    Args:
        settings: Optional settings override
    
    Returns:
        LuminoraCoreClient instance
    """
    return LuminoraCoreClient(settings)
