#!/usr/bin/env python3
"""
CRITICAL TEST: Conversation Memory Integration Fix (Windows Compatible)

This test validates that LuminoraCore v1.1 properly uses conversation memory
instead of sending individual messages without context.

The test simulates the exact scenario from the JSON provided:
- User says "ire al himalaya que te parece, soy carlos"
- User asks "como te llamas?"
- User says "vaya no lo sabes??"

Expected behavior AFTER the fix:
- Assistant remembers "Carlos" from the first message
- Assistant remembers the Himalayas trip
- Assistant shows awareness of previous conversation
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


async def test_conversation_memory_fix():
    """
    Test the critical conversation memory fix
    
    This test validates that:
    1. User facts are extracted and remembered
    2. Conversation history is maintained
    3. LLM receives full context for responses
    4. Assistant shows awareness of previous messages
    """
    
    print("TESTING: Conversation Memory Integration Fix")
    print("=" * 60)
    
    # Initialize client with memory storage
    storage_config = StorageConfig(storage_type="memory")
    provider_config = ProviderConfig(
        name="deepseek",
        api_key="test-key",  # Mock for testing
        model="deepseek-chat"
    )
    
    # Create client with v1.1 extensions
    client = LuminoraCoreClientV11(
        base_client=None,  # Mock base client
        storage_v11=InMemoryStorageV11()
    )
    
    # Create test session
    session_id = "test_conversation_memory"
    personality_name = "sakura"
    
    print(f"Session ID: {session_id}")
    print(f"Personality: {personality_name}")
    print()
    
    # Test conversation - EXACT scenario from the JSON
    test_messages = [
        {
            "user": "ire al himalaya que te parece, soy carlos",
            "expected_keywords": ["carlos", "himalaya", "viaje", "aventura"],
            "description": "User introduces themselves and mentions Himalayas trip"
        },
        {
            "user": "como te llamas?",
            "expected_keywords": ["sakura", "carlos"],
            "description": "User asks for assistant's name"
        },
        {
            "user": "vaya no lo sabes??",
            "expected_keywords": ["carlos", "himalaya", "recuerdo", "sabes"],
            "description": "User is surprised assistant doesn't remember"
        }
    ]
    
    responses = []
    
    for i, test_case in enumerate(test_messages, 1):
        print(f"Turn {i}: {test_case['description']}")
        print(f"   User: \"{test_case['user']}\"")
        
        # Send message with full context
        try:
            response = await client.send_message_with_memory(
                session_id=session_id,
                user_message=test_case['user'],
                personality_name=personality_name,
                provider_config=provider_config
            )
            
            if response["success"]:
                assistant_response = response["response"]
                facts_learned = response["facts_learned"]
                affinity_level = response["affinity_level"]
                conversation_length = response["conversation_length"]
                
                print(f"   Assistant: \"{assistant_response}\"")
                print(f"   Facts learned: {facts_learned}")
                print(f"   Affinity: {affinity_level}")
                print(f"   Conversation length: {conversation_length}")
                
                # Check if response contains expected keywords
                response_lower = assistant_response.lower()
                found_keywords = [kw for kw in test_case['expected_keywords'] if kw in response_lower]
                
                if found_keywords:
                    print(f"   SUCCESS: Found expected keywords: {found_keywords}")
                else:
                    print(f"   WARNING: Missing expected keywords: {test_case['expected_keywords']}")
                
                responses.append({
                    "turn": i,
                    "user_message": test_case['user'],
                    "assistant_response": assistant_response,
                    "facts_learned": facts_learned,
                    "affinity_level": affinity_level,
                    "found_keywords": found_keywords
                })
                
            else:
                print(f"   ERROR: {response['error']}")
                responses.append({
                    "turn": i,
                    "user_message": test_case['user'],
                    "error": response['error']
                })
                
        except Exception as e:
            print(f"   EXCEPTION: {str(e)}")
            responses.append({
                "turn": i,
                "user_message": test_case['user'],
                "error": str(e)
            })
        
        print()
    
    # Validate results
    print("VALIDATION RESULTS")
    print("=" * 60)
    
    # Check if memory is working
    try:
        facts = await client.get_facts(session_id)
        print(f"Total facts learned: {len(facts)}")
        
        if facts:
            print("   Facts:")
            for fact in facts:
                print(f"   - {fact['key']}: {fact['value']}")
        else:
            print("   WARNING: No facts learned - this indicates a problem!")
            
    except Exception as e:
        print(f"   ERROR getting facts: {e}")
    
    # Check conversation history
    try:
        if hasattr(client.conversation_manager, '_get_conversation_history'):
            history = await client.conversation_manager._get_conversation_history(session_id)
            print(f"Conversation history length: {len(history)}")
        else:
            print("   WARNING: Conversation history method not available")
            
    except Exception as e:
        print(f"   ERROR getting conversation history: {e}")
    
    # Check affinity
    try:
        affinity = await client.get_affinity(session_id, personality_name)
        print(f"Final affinity: {affinity['level']} ({affinity['points']}/100 points)")
        
    except Exception as e:
        print(f"   ERROR getting affinity: {e}")
    
    # Analyze responses for memory awareness
    print("\nMEMORY AWARENESS ANALYSIS")
    print("=" * 60)
    
    memory_indicators = {
        "remembers_name": False,
        "remembers_himalayas": False,
        "shows_context_awareness": False
    }
    
    for response in responses:
        if response.get("assistant_response"):
            response_text = response["assistant_response"].lower()
            
            # Check if assistant remembers the name
            if "carlos" in response_text and response["turn"] > 1:
                memory_indicators["remembers_name"] = True
                print(f"SUCCESS Turn {response['turn']}: Remembers name 'Carlos'")
            
            # Check if assistant remembers Himalayas
            if "himalaya" in response_text and response["turn"] > 1:
                memory_indicators["remembers_himalayas"] = True
                print(f"SUCCESS Turn {response['turn']}: Remembers Himalayas trip")
            
            # Check for context awareness
            if any(word in response_text for word in ["recuerdo", "sabes", "mencionaste", "dijiste"]):
                memory_indicators["shows_context_awareness"] = True
                print(f"SUCCESS Turn {response['turn']}: Shows context awareness")
    
    # Final assessment
    print("\nFINAL ASSESSMENT")
    print("=" * 60)
    
    if memory_indicators["remembers_name"] and memory_indicators["remembers_himalayas"]:
        print("SUCCESS: Conversation memory is working correctly!")
        print("   - Assistant remembers user's name")
        print("   - Assistant remembers user's travel plans")
        print("   - Context is being maintained across turns")
        
        if memory_indicators["shows_context_awareness"]:
            print("   - Assistant shows explicit awareness of previous conversation")
        
        print("\nSUCCESS: The fix has resolved the conversation memory issue!")
        print("   LuminoraCore now properly uses memory instead of sending individual messages.")
        
    else:
        print("FAILURE: Conversation memory is NOT working correctly!")
        print("   - Assistant does not remember user information")
        print("   - Context is not being maintained")
        print("   - The fix needs more work")
        
        if not memory_indicators["remembers_name"]:
            print("   - Missing: Name memory")
        if not memory_indicators["remembers_himalayas"]:
            print("   - Missing: Travel plan memory")
        if not memory_indicators["shows_context_awareness"]:
            print("   - Missing: Context awareness")
    
    return memory_indicators


async def main():
    """Main test function"""
    print("CRITICAL TEST: Conversation Memory Integration Fix")
    print("Testing the fix for the conversation memory issue identified")
    print("=" * 80)
    
    try:
        results = await test_conversation_memory_fix()
        
        print("\n" + "=" * 80)
        if all(results.values()):
            print("TEST PASSED: Conversation memory fix is working!")
            print("   LuminoraCore v1.1 now properly integrates memory with conversations.")
        else:
            print("TEST FAILED: Conversation memory fix needs more work.")
            print("   The issue identified by the frontend team is not yet resolved.")
        
    except Exception as e:
        print(f"Test failed with exception: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
