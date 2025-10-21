#!/usr/bin/env python3
"""
CLI Command: conversation-memory

Test conversation memory integration - CRITICAL FIX VALIDATION
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any, List

# Add SDK path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'luminoracore-sdk-python'))

from luminoracore_sdk import LuminoraCoreClientV11
from luminoracore_sdk.types.session import StorageConfig
from luminoracore_sdk.types.provider import ProviderConfig
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11


async def test_conversation_memory_interactive():
    """Interactive test of conversation memory"""
    
    print("🧠 LuminoraCore v1.1 - Conversation Memory Test")
    print("=" * 50)
    print("This test validates that conversation memory is working correctly.")
    print("The assistant should remember information across multiple messages.")
    print()
    
    # Initialize client
    client = LuminoraCoreClientV11(
        base_client=None,
        storage_v11=InMemoryStorageV11()
    )
    
    await client.initialize()
    
    # Get session details
    session_id = input("Enter session ID (or press Enter for 'test_session'): ").strip()
    if not session_id:
        session_id = f"test_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    personality_name = input("Enter personality name (or press Enter for 'sakura'): ").strip()
    if not personality_name:
        personality_name = "sakura"
    
    print(f"\n📝 Session: {session_id}")
    print(f"🎭 Personality: {personality_name}")
    print("\n💬 Start the conversation! Type 'quit' to exit, 'status' to see memory status.")
    print("=" * 50)
    
    turn_count = 0
    
    while True:
        try:
            # Get user input
            user_message = input(f"\n[{turn_count + 1}] You: ").strip()
            
            if user_message.lower() == 'quit':
                break
            elif user_message.lower() == 'status':
                await show_memory_status(client, session_id, personality_name)
                continue
            elif not user_message:
                continue
            
            # Send message with memory
            print("🤖 Assistant: ", end="", flush=True)
            
            response = await client.send_message_with_memory(
                session_id=session_id,
                user_message=user_message,
                user_id=session_id,  # CRITICAL FIX: Use session_id as user_id
                personality_name=personality_name
            )
            
            if response["success"]:
                print(response["response"])
                
                # Show memory indicators
                if response["facts_learned"] > 0:
                    print(f"   📚 Learned {response['facts_learned']} new facts")
                
                if response["affinity_change"]:
                    change = response["affinity_change"]
                    print(f"   💝 Affinity: {response['affinity_level']} ({response['affinity_points']}/100)")
                
                print(f"   📏 Conversation length: {response['conversation_length']}")
                
            else:
                print(f"❌ Error: {response['error']}")
            
            turn_count += 1
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    # Final status
    print("\n" + "=" * 50)
    print("🏁 Final Memory Status:")
    await show_memory_status(client, session_id, personality_name)


async def show_memory_status(client: LuminoraCoreClientV11, session_id: str, personality_name: str):
    """Show current memory status"""
    
    print("\n📊 MEMORY STATUS")
    print("-" * 30)
    
    try:
        # Show facts
        facts = await client.get_facts(session_id)  # Use session_id as user_id
        print(f"📚 Facts learned: {len(facts)}")
        
        if facts:
            for fact in facts:
                print(f"   - {fact['key']}: {fact['value']}")
        
        # Show affinity
        affinity = await client.get_affinity(session_id, personality_name)  # Use session_id as user_id
        print(f"💝 Affinity: {affinity['level']} ({affinity['points']}/100 points)")
        
        # Show conversation history
        if hasattr(client.conversation_manager, '_get_conversation_history'):
            history = await client.conversation_manager._get_conversation_history(session_id)
            print(f"📜 Conversation turns: {len(history)}")
            
            if history:
                print("   Recent turns:")
                for turn in history[-3:]:  # Show last 3 turns
                    print(f"   - User: {turn.user_message[:50]}...")
                    print(f"     Assistant: {turn.assistant_response[:50]}...")
        
    except Exception as e:
        print(f"❌ Error getting memory status: {e}")


async def run_preset_conversation_test():
    """Run the exact conversation test from the JSON example"""
    
    print("🧪 PRESET CONVERSATION TEST")
    print("=" * 50)
    print("Testing the exact scenario from the JSON example:")
    print("1. 'ire al himalaya que te parece, soy carlos'")
    print("2. 'como te llamas?'")
    print("3. 'vaya no lo sabes??'")
    print()
    
    # Initialize client
    client = LuminoraCoreClientV11(
        base_client=None,
        storage_v11=InMemoryStorageV11()
    )
    
    await client.initialize()
    
    session_id = "preset_test_session"
    personality_name = "sakura"
    
    test_messages = [
        "ire al himalaya que te parece, soy carlos",
        "como te llamas?",
        "vaya no lo sabes??"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"💬 Turn {i}:")
        print(f"   User: \"{message}\"")
        
        response = await client.send_message_with_memory(
            session_id=session_id,
            user_message=message,
            user_id=session_id,  # CRITICAL FIX: Use session_id as user_id
            personality_name=personality_name
        )
        
        if response["success"]:
            print(f"   Assistant: \"{response['response']}\"")
            print(f"   📚 Facts learned: {response['facts_learned']}")
            print(f"   💝 Affinity: {response['affinity_level']}")
        else:
            print(f"   ❌ Error: {response['error']}")
        
        print()
    
    # Show final status
    print("🏁 FINAL STATUS:")
    await show_memory_status(client, session_id, personality_name)


def main():
    """Main CLI function"""
    
    if len(sys.argv) > 1 and sys.argv[1] == "preset":
        asyncio.run(run_preset_conversation_test())
    else:
        asyncio.run(test_conversation_memory_interactive())


# Export the main function for CLI
conversation_memory = main

if __name__ == "__main__":
    main()
