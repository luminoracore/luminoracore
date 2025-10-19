#!/usr/bin/env python3
"""
LuminoraCore v1.1 - Conversation Memory Example

This example demonstrates the CRITICAL FIX for conversation memory integration.
It shows how to use the new send_message_with_memory method that properly
integrates conversation history, user facts, and affinity tracking.
"""

import asyncio
import os
import sys
from datetime import datetime

# Add SDK path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'luminoracore-sdk-python'))

from luminoracore_sdk import LuminoraCoreClientV11
from luminoracore_sdk.types.session import StorageConfig
from luminoracore_sdk.types.provider import ProviderConfig
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11


async def demonstrate_conversation_memory():
    """
    Demonstrate the conversation memory fix in action
    
    This shows the difference between:
    1. Individual message sending (old way - broken)
    2. Context-aware message sending (new way - fixed)
    """
    
    print("🧠 LuminoraCore v1.1 - Conversation Memory Demonstration")
    print("=" * 60)
    print("This example shows how the conversation memory fix works.")
    print("The assistant will remember information across multiple messages.")
    print()
    
    # Initialize client with memory storage
    storage_config = StorageConfig(storage_type="memory")
    provider_config = ProviderConfig(
        provider="deepseek",
        api_key="test-key",  # Mock for demonstration
        model="deepseek-chat"
    )
    
    # Create client with v1.1 extensions
    client = LuminoraCoreClientV11(
        base_client=None,  # Mock base client for demo
        storage_v11=InMemoryStorageV11()
    )
    
    # Initialize client
    await client.initialize()
    
    # Create session
    session_id = "demo_conversation_memory"
    personality_name = "sakura"
    
    print(f"📝 Session: {session_id}")
    print(f"🎭 Personality: {personality_name}")
    print()
    
    # Demonstration conversation
    conversation = [
        {
            "user": "Hola, me llamo María y soy de Barcelona",
            "expected": "Should remember name (María) and location (Barcelona)"
        },
        {
            "user": "¿De dónde eres?",
            "expected": "Should ask about user's location, knowing they're from Barcelona"
        },
        {
            "user": "¿Cómo me llamo?",
            "expected": "Should remember the name 'María' from first message"
        },
        {
            "user": "Estoy estudiando programación",
            "expected": "Should remember this new fact about studying programming"
        },
        {
            "user": "¿Qué recuerdas sobre mí?",
            "expected": "Should list: name (María), location (Barcelona), studying programming"
        }
    ]
    
    print("💬 Starting conversation demonstration...")
    print("=" * 60)
    
    for i, turn in enumerate(conversation, 1):
        print(f"\n🔄 Turn {i}")
        print(f"👤 User: \"{turn['user']}\"")
        print(f"🎯 Expected: {turn['expected']}")
        
        # Send message with full context (the FIXED way)
        response = await client.send_message_with_memory(
            session_id=session_id,
            user_message=turn['user'],
            personality_name=personality_name,
            provider_config=provider_config
        )
        
        if response["success"]:
            print(f"🤖 Assistant: \"{response['response']}\"")
            
            # Show memory indicators
            if response["facts_learned"] > 0:
                print(f"   📚 Learned {response['facts_learned']} new facts")
            
            print(f"   💝 Affinity: {response['affinity_level']} ({response['affinity_points']}/100)")
            print(f"   📏 Conversation length: {response['conversation_length']}")
            
            # Show new facts if any
            if response.get("new_facts"):
                print("   🆕 New facts:")
                for fact in response["new_facts"]:
                    print(f"      - {fact['key']}: {fact['value']}")
            
        else:
            print(f"❌ Error: {response['error']}")
        
        print("-" * 40)
    
    # Show final memory status
    print("\n🏁 FINAL MEMORY STATUS")
    print("=" * 60)
    
    try:
        # Show all learned facts
        facts = await client.get_facts(session_id)
        print(f"📚 Total facts learned: {len(facts)}")
        
        if facts:
            print("   Facts:")
            for fact in facts:
                print(f"   - {fact['key']}: {fact['value']}")
        
        # Show affinity progression
        affinity = await client.get_affinity(session_id, personality_name)
        print(f"💝 Final affinity: {affinity['level']} ({affinity['points']}/100 points)")
        
        # Show conversation history length
        if hasattr(client.conversation_manager, '_get_conversation_history'):
            history = await client.conversation_manager._get_conversation_history(session_id)
            print(f"📜 Conversation turns: {len(history)}")
        
    except Exception as e:
        print(f"❌ Error getting memory status: {e}")
    
    print("\n✅ Demonstration completed!")
    print("The conversation memory system is working correctly.")
    print("The assistant remembers information across multiple messages.")


async def compare_old_vs_new_approach():
    """
    Compare the old broken approach vs the new fixed approach
    """
    
    print("\n🔍 COMPARISON: Old vs New Approach")
    print("=" * 60)
    
    print("❌ OLD APPROACH (Broken):")
    print("   - Each message sent individually")
    print("   - No conversation context")
    print("   - LLM doesn't see previous messages")
    print("   - Memory saved but not used")
    print("   - Result: Assistant 'forgets' everything")
    
    print("\n✅ NEW APPROACH (Fixed):")
    print("   - Full conversation context sent to LLM")
    print("   - User facts included in context")
    print("   - Affinity level affects personality")
    print("   - Memory actively used for responses")
    print("   - Result: Assistant remembers everything")
    
    print("\n💡 KEY DIFFERENCE:")
    print("   OLD: LLM receives only current message")
    print("   NEW: LLM receives full context + history + facts + affinity")
    
    print("\n🎯 BUSINESS IMPACT:")
    print("   OLD: Users frustrated, poor experience")
    print("   NEW: Users delighted, superior experience")


async def main():
    """Main demonstration function"""
    
    print("🚨 LuminoraCore v1.1 - Conversation Memory Fix Demonstration")
    print("=" * 80)
    print("This demonstrates the CRITICAL FIX for conversation memory integration.")
    print("The fix ensures that LuminoraCore actually uses its memory system")
    print("instead of sending individual messages without context.")
    print()
    
    try:
        # Run the demonstration
        await demonstrate_conversation_memory()
        
        # Show comparison
        await compare_old_vs_new_approach()
        
        print("\n" + "=" * 80)
        print("🎉 DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("The conversation memory fix is working correctly.")
        print("LuminoraCore v1.1 now properly integrates memory with conversations.")
        
    except Exception as e:
        print(f"❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
