"""Unit tests for LuminoraCore client."""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch

from luminoracore_sdk.client import LuminoraCoreClient
from luminoracore_sdk.types.session import StorageConfig, MemoryConfig
from luminoracore_sdk.types.provider import ProviderConfig
from luminoracore_sdk.types.personality import PersonalityData
from luminoracore_sdk.utils.exceptions import LuminoraCoreSDKError


class TestLuminoraCoreClient:
    """Test cases for LuminoraCoreClient."""
    
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
            description="Test personality",
            author="Test Author",
            tags=["test"],
            system_prompt="You are a helpful test personality. Always respond with test prefix.",
            persona={
                "name": "test_personality",
                "description": "Test personality",
                "archetype": "assistant",
                "version": "1.0.0",
                "author": "Test Author",
                "tags": ["test"]
            },
            core_traits=["helpful", "friendly", "test"],
            linguistic_profile={
                "tone": ["friendly", "helpful"],
                "vocabulary": ["test", "help", "assist"],
                "speech_patterns": ["I can help you", "Let me test"],
                "formality_level": "casual",
                "response_length": "moderate"
            },
            behavioral_rules=[
                "Be helpful and friendly",
                "Always respond with test prefix",
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
    async def test_client_initialization(self, client):
        """Test client initialization."""
        assert client.session_manager is not None
        assert client.conversation_manager is not None
        assert client.memory_manager is not None
        assert client.personality_manager is not None
        assert client.personality_blender is not None
    
    @pytest.mark.asyncio
    async def test_initialize(self, client):
        """Test client initialization."""
        with patch.object(client.personality_manager, 'load_personalities_from_directory') as mock_load:
            mock_load.return_value = []
            await client.initialize()
            mock_load.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_session(self, client, personality_data, provider_config):
        """Test session creation."""
        # Mock personality manager
        client.personality_manager.get_personality = AsyncMock(return_value=personality_data)
        
        # Mock session manager
        client.session_manager.create_session = AsyncMock(return_value="test_session_id")
        
        session_id = await client.create_session(
            personality_name="test_personality",
            provider_config=provider_config
        )
        
        assert session_id == "test_session_id"
        client.session_manager.create_session.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_session_personality_not_found(self, client, provider_config):
        """Test session creation with non-existent personality."""
        # Mock personality manager to return None
        client.personality_manager.get_personality = AsyncMock(return_value=None)
        
        with pytest.raises(LuminoraCoreSDKError, match="Personality not found"):
            await client.create_session(
                personality_name="non_existent",
                provider_config=provider_config
            )
    
    @pytest.mark.asyncio
    async def test_send_message(self, client):
        """Test sending a message."""
        # Mock session manager
        mock_response = Mock()
        mock_response.content = "Test response"
        client.session_manager.send_message = AsyncMock(return_value=mock_response)
        
        response = await client.send_message(
            session_id="test_session",
            message="Hello, world!"
        )
        
        assert response.content == "Test response"
        client.session_manager.send_message.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_stream_message(self, client):
        """Test streaming a message."""
        # Mock session manager
        mock_chunk1 = Mock()
        mock_chunk1.content = "Test"
        mock_chunk2 = Mock()
        mock_chunk2.content = " response"
        
        async def mock_stream(session_id, message, **kwargs):
            yield mock_chunk1
            yield mock_chunk2
        
        client.session_manager.stream_message = mock_stream
        
        chunks = []
        async for chunk in client.stream_message(
            session_id="test_session",
            message="Hello, world!"
        ):
            chunks.append(chunk.content)
        
        assert chunks == ["Test", " response"]
    
    @pytest.mark.asyncio
    async def test_get_conversation(self, client):
        """Test getting conversation history."""
        # Mock session manager
        mock_conversation = Mock()
        mock_conversation.messages = [
            Mock(role="user", content="Hello"),
            Mock(role="assistant", content="Hi there!")
        ]
        client.session_manager.get_conversation = AsyncMock(return_value=mock_conversation)
        
        messages = await client.get_conversation("test_session")
        
        assert len(messages) == 2
        assert messages[0].role == "user"
        assert messages[0].content == "Hello"
        assert messages[1].role == "assistant"
        assert messages[1].content == "Hi there!"
    
    @pytest.mark.asyncio
    async def test_clear_conversation(self, client):
        """Test clearing conversation."""
        # Mock session manager
        client.session_manager.clear_conversation = AsyncMock(return_value=True)
        
        result = await client.clear_conversation("test_session")
        
        assert result is True
        client.session_manager.clear_conversation.assert_called_once_with("test_session")
    
    @pytest.mark.asyncio
    async def test_delete_session(self, client):
        """Test deleting a session."""
        # Mock session manager
        client.session_manager.delete_session = AsyncMock(return_value=True)
        
        result = await client.delete_session("test_session")
        
        assert result is True
        client.session_manager.delete_session.assert_called_once_with("test_session")
    
    @pytest.mark.asyncio
    async def test_list_sessions(self, client):
        """Test listing sessions."""
        # Mock session manager
        client.session_manager.list_sessions = AsyncMock(return_value=["session1", "session2"])
        
        sessions = await client.list_sessions()
        
        assert sessions == ["session1", "session2"]
    
    @pytest.mark.asyncio
    async def test_get_session_info(self, client):
        """Test getting session info."""
        # Mock session manager
        mock_info = {
            "session_id": "test_session",
            "personality": "test_personality",
            "provider": "test_provider"
        }
        client.session_manager.get_session_info = AsyncMock(return_value=mock_info)
        
        info = await client.get_session_info("test_session")
        
        assert info == mock_info
    
    @pytest.mark.asyncio
    async def test_load_personality(self, client):
        """Test loading a personality."""
        # Mock personality manager
        client.personality_manager.load_personality = AsyncMock(return_value=True)
        
        result = await client.load_personality("test_personality", {})
        
        assert result is True
        client.personality_manager.load_personality.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_personality(self, client, personality_data):
        """Test getting a personality."""
        # Mock personality manager
        client.personality_manager.get_personality = AsyncMock(return_value=personality_data)
        
        personality = await client.get_personality("test_personality")
        
        assert personality == personality_data
    
    @pytest.mark.asyncio
    async def test_list_personalities(self, client):
        """Test listing personalities."""
        # Mock personality manager
        client.personality_manager.list_personalities = AsyncMock(return_value=["personality1", "personality2"])
        
        personalities = await client.list_personalities()
        
        assert personalities == ["personality1", "personality2"]
    
    @pytest.mark.asyncio
    async def test_delete_personality(self, client):
        """Test deleting a personality."""
        # Mock personality manager
        client.personality_manager.delete_personality = AsyncMock(return_value=True)
        
        result = await client.delete_personality("test_personality")
        
        assert result is True
    
    @pytest.mark.asyncio
    async def test_blend_personalities(self, client, personality_data):
        """Test blending personalities."""
        # Mock personality manager
        client.personality_manager.get_personality = AsyncMock(return_value=personality_data)
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
            advanced_parameters={"temperature": 0.7},
            metadata={}
        )
        client.personality_blender.blend_personalities = AsyncMock(return_value=blended_personality)
        
        result = await client.blend_personalities(
            personality_names=["personality1", "personality2"],
            weights=[0.5, 0.5]
        )
        
        assert result == blended_personality
    
    @pytest.mark.asyncio
    async def test_store_memory(self, client):
        """Test storing memory."""
        # Mock memory manager
        client.memory_manager.store_memory = AsyncMock(return_value=True)
        
        result = await client.store_memory("test_session", "test_key", "test_value")
        
        assert result is True
        client.memory_manager.store_memory.assert_called_once_with("test_session", "test_key", "test_value", None)
    
    @pytest.mark.asyncio
    async def test_get_memory(self, client):
        """Test getting memory."""
        # Mock memory manager
        client.memory_manager.get_memory = AsyncMock(return_value="test_value")
        
        value = await client.get_memory("test_session", "test_key")
        
        assert value == "test_value"
        client.memory_manager.get_memory.assert_called_once_with("test_session", "test_key")
    
    @pytest.mark.asyncio
    async def test_delete_memory(self, client):
        """Test deleting memory."""
        # Mock memory manager
        client.memory_manager.delete_memory = AsyncMock(return_value=True)
        
        result = await client.delete_memory("test_session", "test_key")
        
        assert result is True
        client.memory_manager.delete_memory.assert_called_once_with("test_session", "test_key")
    
    @pytest.mark.asyncio
    async def test_clear_memory(self, client):
        """Test clearing memory."""
        # Mock memory manager
        client.memory_manager.clear_memory = AsyncMock(return_value=True)
        
        result = await client.clear_memory("test_session")
        
        assert result is True
        client.memory_manager.clear_memory.assert_called_once_with("test_session")
    
    @pytest.mark.asyncio
    async def test_get_client_info(self, client):
        """Test getting client info."""
        # Mock managers
        client.personality_manager.list_personalities = AsyncMock(return_value=["personality1"])
        client.session_manager.list_sessions = AsyncMock(return_value=["session1"])
        
        info = await client.get_client_info()
        
        assert info["total_personalities"] == 1
        assert info["total_sessions"] == 1
        assert info["personality_names"] == ["personality1"]
        assert info["session_ids"] == ["session1"]
    
    @pytest.mark.asyncio
    async def test_cleanup(self, client):
        """Test client cleanup."""
        # Mock managers
        client.memory_manager.cleanup_expired_memories = AsyncMock(return_value=0)
        client.personality_blender.clear_blend_cache = AsyncMock(return_value=0)
        
        await client.cleanup()
        
        client.memory_manager.cleanup_expired_memories.assert_called_once()
        client.personality_blender.clear_blend_cache.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_context_manager(self, client):
        """Test client as context manager."""
        with patch.object(client, 'initialize') as mock_init:
            with patch.object(client, 'cleanup') as mock_cleanup:
                async with client:
                    mock_init.assert_called_once()
                mock_cleanup.assert_called_once()
