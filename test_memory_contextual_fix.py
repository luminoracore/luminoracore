#!/usr/bin/env python3
"""
Test específico para verificar la corrección de memoria contextual
"""

import asyncio
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore-sdk-python"))

async def test_memory_contextual_fix():
    """Test específico para verificar la corrección de memoria contextual"""
    print("=== TEST CORRECCION MEMORIA CONTEXTUAL ===")
    
    try:
        from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
        from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
        
        # Initialize
        base_client = LuminoraCoreClient()
        await base_client.initialize()
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(base_client, storage_v11=storage)
        
        # Test 1: Create session and save facts
        session_id = await client.create_session(
            user_id="test_memory_user",
            personality_name="alicia"
        )
        print(f"Session created: {session_id}")
        
        # Save some facts
        await client.save_fact("test_memory_user", "personal_info", "name", "Carlos", confidence=0.9)
        await client.save_fact("test_memory_user", "preferences", "language", "Python", confidence=0.8)
        
        # Verify facts are saved
        facts = await client.get_facts("test_memory_user")
        print(f"Facts saved: {len(facts)} facts")
        for fact in facts:
            print(f"  - {fact.get('key')}: {fact.get('value')}")
        
        # Test 2: Send message WITHOUT explicit user_id (should use session_id as user_id)
        print("\n--- TEST WITHOUT EXPLICIT USER_ID ---")
        result1 = await client.send_message_with_memory(
            session_id=session_id,
            user_message="What do you remember about me?",
            personality_name="alicia"
        )
        
        print(f"Response 1: {result1.get('response', 'No response')[:200]}...")
        print(f"Context used: {result1.get('context_used', False)}")
        print(f"Facts learned: {result1.get('facts_learned', 0)}")
        
        # Test 3: Send message WITH explicit user_id
        print("\n--- TEST WITH EXPLICIT USER_ID ---")
        result2 = await client.send_message_with_memory(
            session_id=session_id,
            user_message="Tell me about my preferences",
            user_id="test_memory_user",
            personality_name="alicia"
        )
        
        print(f"Response 2: {result2.get('response', 'No response')[:200]}...")
        print(f"Context used: {result2.get('context_used', False)}")
        print(f"Facts learned: {result2.get('facts_learned', 0)}")
        
        # Test 4: Verify memory is being used
        print("\n--- VERIFICATION ---")
        memory_used_1 = result1.get('context_used', False)
        memory_used_2 = result2.get('context_used', False)
        
        print(f"Memory used in test 1: {memory_used_1}")
        print(f"Memory used in test 2: {memory_used_2}")
        
        if memory_used_1 and memory_used_2:
            print("[OK] SUCCESS: Memory contextual is working correctly")
            return True
        else:
            print("[FAIL] FAIL: Memory contextual is not working")
            return False
        
        await base_client.cleanup()
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_memory_contextual_fix())
    sys.exit(0 if success else 1)
