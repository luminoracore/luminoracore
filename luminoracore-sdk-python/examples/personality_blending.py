"""Personality blending example for LuminoraCore SDK."""

import asyncio
import os
from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types.provider import ProviderConfig
from luminoracore_sdk.types.session import StorageConfig, MemoryConfig


async def main():
    """Main example function."""
    # Initialize the client
    client = LuminoraCoreClient(
        storage_config=StorageConfig(
            storage_type="memory",
            ttl=3600
        ),
        memory_config=MemoryConfig(
            max_tokens=10000,
            max_messages=100,
            ttl=1800
        )
    )
    
    # Initialize the client
    await client.initialize()
    
    # Create a provider configuration
    provider_config = ProviderConfig(
        name="openai",
        api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"),
        model="gpt-3.5-turbo",
        base_url="https://api.openai.com/v1",
        timeout=30,
        max_retries=3
    )
    
    # Load some personalities
    await client.load_personality("creative_writer", {
        "name": "creative_writer",
        "description": "A creative and imaginative writer",
        "system_prompt": "You are a creative writer with a vivid imagination. You love crafting stories and coming up with unique ideas.",
        "metadata": {"category": "creative", "style": "imaginative"}
    })
    
    await client.load_personality("technical_expert", {
        "name": "technical_expert",
        "description": "A technical expert with deep knowledge",
        "system_prompt": "You are a technical expert with deep knowledge in various fields. You provide clear, accurate, and detailed explanations.",
        "metadata": {"category": "technical", "style": "analytical"}
    })
    
    # Blend personalities
    blended_personality = await client.blend_personalities(
        personality_names=["creative_writer", "technical_expert"],
        weights=[0.3, 0.7],
        blend_name="creative_technical_expert"
    )
    
    print(f"Created blended personality: {blended_personality.name}")
    print(f"Description: {blended_personality.description}")
    
    # Create a session with the blended personality
    session_id = await client.create_session(
        personality_name="creative_technical_expert",
        provider_config=provider_config
    )
    
    print(f"Created session with blended personality: {session_id}")
    
    # Test the blended personality
    response = await client.send_message(
        session_id=session_id,
        message="Explain quantum computing in a creative and engaging way."
    )
    
    print(f"Blended personality response: {response.content}")
    
    # Test with different blend weights
    blended_personality2 = await client.blend_personalities(
        personality_names=["creative_writer", "technical_expert"],
        weights=[0.7, 0.3],
        blend_name="creative_technical_expert_2"
    )
    
    print(f"Created second blended personality: {blended_personality2.name}")
    
    # Create another session
    session_id2 = await client.create_session(
        personality_name="creative_technical_expert_2",
        provider_config=provider_config
    )
    
    # Test the second blend
    response2 = await client.send_message(
        session_id=session_id2,
        message="Explain quantum computing in a creative and engaging way."
    )
    
    print(f"Second blended personality response: {response2.content}")
    
    # Compare the responses
    print("\nComparison:")
    print(f"Technical-heavy blend: {response.content[:100]}...")
    print(f"Creative-heavy blend: {response2.content[:100]}...")
    
    # Clean up
    await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
