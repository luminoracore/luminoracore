"""Simple usage example for LuminoraCore SDK."""

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
    print("LuminoraCore SDK Simple Usage Example")
    print("=" * 50)
    
    # Initialize the client
    print("\n1. Initializing client...")
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
    print("[OK] Client initialized")
    
    # Create a provider configuration
    print("\n2. Creating provider configuration...")
    provider_config = ProviderConfig(
        name="openai",
        api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"),
        model="gpt-3.5-turbo",
        base_url="https://api.openai.com/v1",
        extra={
            "timeout": 30,
            "max_retries": 3
        }
    )
    print("[OK] Provider configuration created")
    
    # Test basic functionality
    print("\n3. Testing basic functionality...")
    
    # Test personality management
    print("  - Testing personality management...")
    try:
        # Create a simple personality data
        personality_data = {
            "name": "test_personality",
            "description": "A test personality for demonstration",
            "system_prompt": "You are a helpful and friendly AI assistant. Always be polite and provide accurate information. When responding, start with 'Test response:' to show this is a test personality.",
            "metadata": {
                "version": "1.0.0",
                "author": "Test Author",
                "tags": ["test", "demo"]
            }
        }
        
        # Load personality to the client
        await client.load_personality("test_personality", personality_data)
        print("    [OK] Personality loaded successfully")
        
    except Exception as e:
        print(f"    [ERROR] Failed to add personality: {e}")
        return
    
    # Test session creation
    print("  - Testing session creation...")
    try:
        session_id = await client.create_session(
            personality_name="test_personality",
            provider_config=provider_config
        )
        print(f"    [OK] Session created: {session_id}")
        
    except Exception as e:
        print(f"    [ERROR] Failed to create session: {e}")
        return
    
    # Test memory management
    print("  - Testing memory management...")
    try:
        # Store some memory
        await client.store_memory(
            session_id=session_id,
            key="user_preference",
            value="interested in AI personality blending"
        )
        print("    [OK] Memory stored successfully")
        
        # Retrieve memory
        memory = await client.get_memory(session_id, "user_preference")
        print(f"    [OK] Memory retrieved: {memory}")
        
    except Exception as e:
        print(f"    [ERROR] Memory management failed: {e}")
    
    # Test session info
    print("  - Testing session info...")
    try:
        info = await client.get_session_info(session_id)
        print(f"    [OK] Session info: {info}")
        
    except Exception as e:
        print(f"    [ERROR] Failed to get session info: {e}")
    
    # Test conversation management
    print("  - Testing conversation management...")
    try:
        messages = await client.get_conversation(session_id)
        print(f"    [OK] Conversation has {len(messages)} messages")
        
    except Exception as e:
        print(f"    [ERROR] Failed to get conversation: {e}")
    
    # Test personality blending
    print("  - Testing personality blending...")
    try:
        # Create another personality
        personality2_data = {
            "name": "test_personality_2",
            "description": "A creative test personality for demonstration",
            "system_prompt": "You are a creative and artistic AI assistant. Always be imaginative and provide creative solutions. When responding, start with 'Creative response:' to show this is a creative test personality.",
            "metadata": {
                "version": "1.0.0",
                "author": "Test Author",
                "tags": ["test", "demo", "creative"]
            }
        }
        
        await client.load_personality("test_personality_2", personality2_data)
        
        # Blend personalities
        blended = await client.blend_personalities(
            personality_names=["test_personality", "test_personality_2"],
            weights=[0.6, 0.4],
            blend_name="blended_test_personality"
        )
        print(f"    [OK] Personalities blended: {blended}")
        
    except Exception as e:
        print(f"    [ERROR] Personality blending failed: {e}")
    
    # Clean up
    print("\n4. Cleaning up...")
    try:
        await client.cleanup()
        print("[OK] Cleanup completed")
    except Exception as e:
        print(f"[ERROR] Cleanup failed: {e}")
    
    print("\nSimple usage example completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
