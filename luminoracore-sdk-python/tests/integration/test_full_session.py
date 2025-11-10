"""Integration tests for full session workflow."""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch

from luminoracore_sdk.client import LuminoraCoreClient
from luminoracore_sdk.types.session import StorageConfig, MemoryConfig
from luminoracore_sdk.types.provider import ProviderConfig
from luminoracore_sdk.types.personality import PersonalityData


class TestFullSessionWorkflow:
    """Integration tests for complete session workflows."""
    
    @pytest.fixture
    def client(self):
        """Create a test client."""
        return LuminoraCoreClient()
    
    @pytest.fixture
    def personality_data(self):
        """Create test personality data."""
        return PersonalityData(
            name="test_personality",
            version="1.0.0",
            description="A helpful test personality",
            author="Test Author",
            tags=["test", "integration"],
            system_prompt="You are a helpful test personality. Always respond with 'Test response: ' followed by the user's message.",
            persona={
                "name": "test_personality",
                "description": "A helpful test personality",
                "archetype": "assistant",
                "version": "1.0.0",
                "author": "Test Author",
                "tags": ["test", "integration"]
            },
            core_traits=["helpful", "friendly", "test"],
            linguistic_profile={
                "tone": ["friendly", "helpful"],
                "vocabulary": ["test", "help", "assist", "response"],
                "speech_patterns": ["Test response:", "I can help you"],
                "formality_level": "casual",
                "response_length": "moderate"
            },
            behavioral_rules=[
                "Always respond with 'Test response: ' followed by the user's message",
                "Be helpful and friendly",
                "Provide accurate information"
            ],
            advanced_parameters={
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 500
            }
        )
    
    @pytest.fixture
    def provider_config(self):
        """Create test provider configuration."""
        return ProviderConfig(
            name="test_provider",
            api_key="test_api_key",
            model="test_model",
            base_url="https://api.test.com",
            extra={"timeout": 30, "max_retries": 3}
        )
    
    @pytest.mark.asyncio
    async def test_full_session_workflow(self, client, personality_data, provider_config):
        """Test complete session workflow."""
        # Mock personality manager
        client.personality_manager.get_personality = AsyncMock(return_value=personality_data)
        client.personality_manager.load_personality = AsyncMock(return_value=True)
        
        # Mock session manager
        client.session_manager.create_session = AsyncMock(return_value="test_session_id")
        
        # Mock provider response
        mock_response = Mock()
        mock_response.content = "Test response: Hello, world!"
        mock_response.role = "assistant"
        mock_response.finish_reason = "stop"
        mock_response.usage = {"prompt_tokens": 10, "completion_tokens": 5}
        mock_response.model = "test_model"
        mock_response.provider_metadata = {"test": "metadata"}
        
        client.session_manager.send_message = AsyncMock(return_value=mock_response)
        client.session_manager.get_conversation = AsyncMock(return_value=Mock(messages=[]))
        client.session_manager.clear_conversation = AsyncMock(return_value=True)
        client.session_manager.delete_session = AsyncMock(return_value=True)
        
        # Initialize client
        await client.initialize()
        
        # Create session
        session_id = await client.create_session(
            personality_name="test_personality",
            provider_config=provider_config
        )
        
        assert session_id == "test_session_id"
        
        # Send message
        response = await client.send_message(
            session_id=session_id,
            message="Hello, world!"
        )
        
        assert response.content == "Test response: Hello, world!"
        
        # Get conversation
        messages = await client.get_conversation(session_id)
        assert messages is not None
        
        # Clear conversation
        result = await client.clear_conversation(session_id)
        assert result is True
        
        # Delete session
        result = await client.delete_session(session_id)
        assert result is True
    
    @pytest.mark.asyncio
    async def test_streaming_workflow(self, client, personality_data, provider_config):
        """Test streaming message workflow."""
        # Mock personality manager
        client.personality_manager.get_personality = AsyncMock(return_value=personality_data)
        
        # Mock session manager
        client.session_manager.create_session = AsyncMock(return_value="test_session_id")
        
        # Mock streaming response
        mock_chunk1 = Mock()
        mock_chunk1.content = "Test"
        mock_chunk1.role = "assistant"
        mock_chunk1.finish_reason = None
        mock_chunk1.is_streaming = True
        
        mock_chunk2 = Mock()
        mock_chunk2.content = " response"
        mock_chunk2.role = "assistant"
        mock_chunk2.finish_reason = "stop"
        mock_chunk2.is_streaming = True
        
        async def mock_stream(session_id, message, **kwargs):
            yield mock_chunk1
            yield mock_chunk2
        
        client.session_manager.stream_message = mock_stream
        
        # Initialize client
        await client.initialize()
        
        # Create session
        session_id = await client.create_session(
            personality_name="test_personality",
            provider_config=provider_config
        )
        
        # Stream message
        chunks = []
        async for chunk in client.stream_message(
            session_id=session_id,
            message="Hello, world!"
        ):
            chunks.append(chunk.content)
        
        assert chunks == ["Test", " response"]
    
    @pytest.mark.asyncio
    async def test_personality_blending_workflow(self, client):
        """Test personality blending workflow."""
        # Create test personalities
        personality1 = PersonalityData(
            name="personality1",
            version="1.0.0",
            description="First personality",
            author="Test Author",
            tags=["test", "first"],
            system_prompt="You are the first personality. Be helpful and friendly.",
            persona={
                "name": "personality1",
                "description": "First personality",
                "archetype": "assistant",
                "version": "1.0.0",
                "author": "Test Author",
                "tags": ["test", "first"]
            },
            core_traits=["first", "helpful"],
            linguistic_profile={
                "tone": ["friendly"],
                "vocabulary": ["first", "help"],
                "speech_patterns": ["I am the first personality"],
                "formality_level": "casual",
                "response_length": "short"
            },
            behavioral_rules=[
                "You are the first personality",
                "Be helpful"
            ],
            advanced_parameters={"temperature": 0.7}
        )
        
        personality2 = PersonalityData(
            name="personality2",
            version="1.0.0",
            description="Second personality",
            author="Test Author",
            tags=["test", "second"],
            system_prompt="You are the second personality. Be helpful and friendly.",
            persona={
                "name": "personality2",
                "description": "Second personality",
                "archetype": "assistant",
                "version": "1.0.0",
                "author": "Test Author",
                "tags": ["test", "second"]
            },
            core_traits=["second", "helpful"],
            linguistic_profile={
                "tone": ["friendly"],
                "vocabulary": ["second", "help"],
                "speech_patterns": ["I am the second personality"],
                "formality_level": "casual",
                "response_length": "short"
            },
            behavioral_rules=[
                "You are the second personality",
                "Be helpful"
            ],
            advanced_parameters={"temperature": 0.7}
        )
        
        # Mock personality manager
        client.personality_manager.get_personality = AsyncMock(side_effect=[personality1, personality2])
        client.personality_manager.load_personality = AsyncMock(return_value=True)
        
        # Mock personality blender
        blended_personality = PersonalityData(
            name="blended_personality",
            version="1.0.0",
            description="Blended personality",
            author="Test Author",
            tags=["test", "blended"],
            system_prompt="You are a blended personality. Be helpful and friendly.",
            persona={
                "name": "blended_personality",
                "description": "Blended personality",
                "archetype": "assistant",
                "version": "1.0.0",
                "author": "Test Author",
                "tags": ["test", "blended"]
            },
            core_traits=["blended", "helpful"],
            linguistic_profile={
                "tone": ["friendly"],
                "vocabulary": ["blended", "help"],
                "speech_patterns": ["I am a blended personality"],
                "formality_level": "casual",
                "response_length": "moderate"
            },
            behavioral_rules=[
                "You are a blended personality",
                "Be helpful"
            ],
            advanced_parameters={"temperature": 0.7, "blend_type": "persona_blend"}
        )
        client.personality_blender.blend_personalities = AsyncMock(return_value=blended_personality)
        
        # Initialize client
        await client.initialize()
        
        # Blend personalities
        result = await client.blend_personalities(
            personality_names=["personality1", "personality2"],
            weights=[0.5, 0.5],
            blend_name="blended_personality"
        )
        
        assert result == blended_personality
        assert result.advanced_parameters["blend_type"] == "persona_blend"
    
    @pytest.mark.asyncio
    async def test_memory_workflow(self, client):
        """Test memory management workflow."""
        # Mock memory manager
        client.memory_manager.store_memory = AsyncMock(return_value=True)
        client.memory_manager.get_memory = AsyncMock(return_value="test_value")
        client.memory_manager.delete_memory = AsyncMock(return_value=True)
        client.memory_manager.clear_memory = AsyncMock(return_value=True)
        
        # Initialize client
        await client.initialize()
        
        # Store memory
        result = await client.store_memory("test_session", "test_key", "test_value")
        assert result is True
        
        # Get memory
        value = await client.get_memory("test_session", "test_key")
        assert value == "test_value"
        
        # Delete memory
        result = await client.delete_memory("test_session", "test_key")
        assert result is True
        
        # Clear memory
        result = await client.clear_memory("test_session")
        assert result is True
    
    @pytest.mark.asyncio
    async def test_error_handling(self, client):
        """Test error handling in workflows."""
        # Mock personality manager to raise exception
        client.personality_manager.get_personality = AsyncMock(side_effect=Exception("Test error"))
        
        # Initialize client
        await client.initialize()
        
        # Test that errors are properly handled
        result = await client.get_personality("non_existent")
        assert result is None
    
    @pytest.mark.asyncio
    async def test_client_context_manager(self, client):
        """Test client as context manager."""
        with patch.object(client, 'initialize') as mock_init:
            with patch.object(client, 'cleanup') as mock_cleanup:
                async with client:
                    mock_init.assert_called_once()
                mock_cleanup.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_concurrent_sessions(self, client, personality_data, provider_config):
        """Test handling multiple concurrent sessions."""
        # Mock personality manager
        client.personality_manager.get_personality = AsyncMock(return_value=personality_data)
        
        # Mock session manager
        client.session_manager.create_session = AsyncMock(side_effect=["session1", "session2"])
        client.session_manager.list_sessions = AsyncMock(return_value=["session1", "session2"])
        
        # Initialize client
        await client.initialize()
        
        # Create multiple sessions
        session1 = await client.create_session(
            personality_name="test_personality",
            provider_config=provider_config
        )
        
        session2 = await client.create_session(
            personality_name="test_personality",
            provider_config=provider_config
        )
        
        # List sessions
        sessions = await client.list_sessions()
        
        assert session1 == "session1"
        assert session2 == "session2"
        assert len(sessions) == 2
        assert "session1" in sessions
        assert "session2" in sessions
