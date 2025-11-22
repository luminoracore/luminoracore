#!/usr/bin/env python3
"""
LuminoraCore SDK - Personality Blending Example

This example demonstrates how to blend multiple AI personalities
to create unique combinations with different characteristics.
"""

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
    
    # Load some personalities
    await client.load_personality("creative_writer", {
        "name": "creative_writer",
        "description": "A creative and imaginative writer",
        "system_prompt": "You are a creative writer with vivid imagination and engaging storytelling skills.",
        "metadata": {"style": "creative", "tone": "imaginative"}
    })
    
    await client.load_personality("technical_expert", {
        "name": "technical_expert", 
        "description": "A technical expert with deep knowledge",
        "system_prompt": "You are a technical expert who explains complex concepts clearly and accurately.",
        "metadata": {"style": "technical", "tone": "professional"}
    })
    
    # Create a blended personality (50/50 mix)
    blended_personality = await client.blend_personalities(
        personality_names=["creative_writer", "technical_expert"],
        weights=[0.5, 0.5],
        blend_name="creative_technical_expert"
    )
    
    print(f"Created blended personality: {blended_personality.name}")
    
    # Create a session with the blended personality
    session_id = await client.create_session(
        personality_name="creative_technical_expert",
        provider_config=provider_config
    )
    
    print(f"Created session with blended personality: {session_id}")
    
    # Test the blended personality (mock response for demo)
    print("Demo message: Explain quantum computing in a creative and engaging way.")
    print("Mock response: Quantum computing is like having a magical calculator that can solve problems in parallel universes...")
    
    # Test with different blend weights (mock for demo)
    print("\nDemo: Creating second blend with weights [0.7, 0.3]")
    print("Demo message: How would you describe machine learning?")
    print("Mock response: Machine learning is like teaching a computer to recognize patterns...")
    
    # Compare the responses (mock for demo)
    print("\nComparison:")
    print("First blend (50/50): Quantum computing is like having a magical calculator...")
    print("Second blend (70/30): Machine learning is like teaching a computer...")
    
    # Cleanup
    await client.cleanup()
    print("\n[OK] Demo completed successfully!")


if __name__ == "__main__":
    print("LuminoraCore SDK - Personality Blending Example")
    print("=" * 50)
    print("[INFO] This demo shows personality blending capabilities")
    print("[INFO] In production, set your API key environment variable")
    print("   export OPENAI_API_KEY='your-key'  (Linux/Mac)")
    print("   $env:OPENAI_API_KEY='your-key'  (Windows)\n")
    
    asyncio.run(main())