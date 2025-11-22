"""Basic usage example for LuminoraCore SDK."""

import asyncio
import os
import sys
from pathlib import Path

# Add the parent directory to the path to import luminoracore_sdk
sys.path.insert(0, str(Path(__file__).parent.parent))

from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types.provider import ProviderConfig
from luminoracore_sdk.types.session import StorageConfig, MemoryConfig


async def main():
    """Main example function."""
    # Initialize the client
    client = LuminoraCoreClient(
        storage_config=StorageConfig(
            storage_type="memory"
        ),
        memory_config=MemoryConfig(
            max_entries=1000,
            decay_factor=0.1
        )
    )
    
    # Initialize the client
    await client.initialize()
    
    # Create a provider configuration (mock for demo)
    provider_config = ProviderConfig(
        name="openai",
        api_key="mock-key-for-demo",
        model="gpt-3.5-turbo",
        base_url="https://api.openai.com/v1",
        extra={
            "timeout": 30,
            "max_retries": 3
        }
    )
    
    # Load a personality first
    personality_data = {
        "name": "helpful_assistant",
        "description": "A helpful AI assistant",
        "system_prompt": "You are a helpful AI assistant. Always be polite and provide accurate information.",
        "metadata": {"version": "1.0.0", "author": "Demo"}
    }
    
    await client.load_personality("helpful_assistant", personality_data)
    
    # Create a session
    session_id = await client.create_session(
        personality_name="helpful_assistant",
        provider_config=provider_config
    )
    
    print(f"Created session: {session_id}")
    
    # Send a message (mock response for demo)
    print("Demo message: Hello! Can you help me understand what LuminoraCore is?")
    print("Mock response: Hello! LuminoraCore is a framework for managing AI personalities...")
    
    # Send another message (mock response for demo)
    print("Demo message: That's interesting! Can you tell me more about personality blending?")
    print("Mock response: Personality blending allows you to combine multiple AI personalities...")
    
    # Get conversation history
    messages = await client.get_conversation(session_id)
    print(f"Conversation has {len(messages)} messages")
    
    # Store some memory
    await client.store_memory(
        session_id=session_id,
        key="user_preference",
        value="interested in AI personality blending"
    )
    
    # Retrieve memory
    memory = await client.get_memory(session_id, "user_preference")
    print(f"Retrieved memory: {memory}")
    
    # Get session info
    info = await client.get_session_info(session_id)
    print(f"Session info: {info}")
    
    # Clean up
    await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
