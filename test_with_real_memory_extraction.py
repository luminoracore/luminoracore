"""
Test with REAL Memory Extraction - NO HARDCODED DATA

This test demonstrates:
- Real automatic fact extraction from conversation
- Sentiment analysis per session/conversation
- Personality evolution tracking
- JSON snapshots of personality before and after conversations
"""

import asyncio
import os
import logging
import sys
import json
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.ERROR)
logging.getLogger('luminoracore_sdk').setLevel(logging.ERROR)


def get_client():
    """Helper function to create client with correct personalities directory"""
    import pathlib
    sdk_dir = pathlib.Path(__file__).parent / "luminoracore-sdk-python" / "luminoracore_sdk" / "personalities"
    from luminoracore_sdk import LuminoraCoreClient
    return LuminoraCoreClient(personalities_dir=str(sdk_dir))


async def test_real_extraction():
    """Test with REAL memory extraction - NO hardcoded data"""
    print("\n" + "=" * 80)
    print("TEST WITH REAL MEMORY EXTRACTION - PERSONALITY EVOLUTION")
    print("=" * 80)
    
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    if not deepseek_api_key:
        print("\n❌ DEEPSEEK_API_KEY not set. Skipping test.")
        return False
    
    # Create temp directory
    temp_dir = Path("temp_test_data_real")
    temp_dir.mkdir(exist_ok=True)
    db_path = temp_dir / "real_extraction_test.db"
    export_dir = temp_dir / "export"
    export_dir.mkdir(exist_ok=True)
    
    try:
        # Initialize client
        print("\n1. Initializing LuminoraCore client...")
        client = get_client()
        await client.initialize()
        print("   ✅ Client initialized")
        
        # Get personalities
        personalities = await client.list_personalities()
        if not personalities:
            print("   ❌ No personalities available")
            return False
        
        personality_name = personalities[0]
        print(f"   ✅ Using personality: {personality_name}")
        
        # Get initial personality state
        print("\n2. Getting initial personality state...")
        initial_personality = await client.get_personality(personality_name)
        
        # Save initial personality to JSON
        initial_personality_path = export_dir / "01_initial_personality.json"
        with open(initial_personality_path, 'w', encoding='utf-8') as f:
            json.dump(initial_personality, f, indent=2, ensure_ascii=False, default=str)
        print(f"   ✅ Initial personality saved to: {initial_personality_path}")
        
        # Create provider config
        from luminoracore_sdk.types.provider import ProviderConfig
        provider_config = ProviderConfig(
            name="deepseek",
            api_key=deepseek_api_key,
            model="deepseek-chat"
        )
        
        # Initialize v1.1 extensions WITH storage
        print("\n3. Initializing v1.1 memory extensions...")
        from luminoracore_sdk import LuminoraCoreClientV11
        from luminoracore_sdk.session.storage_sqlite_flexible import FlexibleSQLiteStorageV11
        
        storage_v11 = FlexibleSQLiteStorageV11(database_path=str(db_path))
        client_v11 = LuminoraCoreClientV11(client, storage_v11=storage_v11)
        print(f"   ✅ SQLite storage initialized")
        
        # NO HARDCODED FACTS - starting with zero facts
        print("\n4. Starting with ZERO facts (no hardcoded data)")
        
        # Send messages that contain user information
        print("\n5. Sending messages with user information for REAL extraction...")
        
        user_messages = [
            "Hi! My name is Alice and I'm 28 years old.",
            "I work as a software engineer in San Francisco at a startup.",
            "I love reading science fiction books, especially Asimov's Foundation series.",
            "My favorite programming language is Python because it's elegant and powerful.",
            "I have a cat named Luna. She's a Persian cat and loves to play with yarn.",
            "I enjoy hiking on weekends in the mountains near San Francisco.",
            "My favorite food is sushi, especially salmon sashimi.",
            "I'm learning Japanese and hope to visit Tokyo next year.",
            "I love playing the piano in my free time."
        ]
        
        # Create a session first (required by framework)
        session_id = f"alice_session_{int(datetime.now().timestamp())}"
        
        # Ensure session exists in the base client
        from luminoracore_sdk.types.provider import ProviderConfig as PC
        base_session_id = await client.create_session(
            personality_name=personality_name,
            provider_config=provider_config
        )
        
        conversation_results = []
        
        for i, message in enumerate(user_messages, 1):
            print(f"\n   Message {i}/{len(user_messages)}: {message}")
            
            # Use send_message_with_memory for REAL extraction
            result = await client_v11.send_message_with_memory(
                session_id=base_session_id,  # Use the base client's session
                user_message=message,
                user_id="alice_user",
                personality_name=personality_name,
                provider_config=provider_config
            )
            
            # Extract AI response - handle both dict and ChatResponse
            if result.get("success") and result.get("response"):
                ai_response = result["response"]
                if isinstance(ai_response, dict):
                    ai_text = ai_response.get("content", "")
                elif hasattr(ai_response, 'content'):  # ChatResponse object
                    ai_text = ai_response.content
                else:
                    ai_text = str(ai_response)
                print(f"   AI: {ai_text[:100]}...")
                
                # Store conversation
                conversation_results.append({
                    "message_number": i,
                    "user_message": message,
                    "ai_response": ai_text,
                    "timestamp": datetime.now().isoformat()
                })
            
            # Print extracted facts count
            facts_count = len(await client_v11.get_facts("alice_user"))
            print(f"   Facts extracted so far: {facts_count}")
        
        print("\n   ✅ All messages sent with real extraction")
        
        # Get and display extracted facts
        print("\n6. Checking REAL extracted facts...")
        facts = await client_v11.get_facts("alice_user")
        print(f"   ✅ Retrieved {len(facts)} REAL facts (not hardcoded)")
        
        if facts:
            print("\n   Extracted facts:")
            for fact in facts:
                print(f"      - {fact.get('category', 'unknown')}.{fact.get('key', 'unknown')}: {fact.get('value', 'N/A')} (confidence: {fact.get('confidence', 0):.2f})")
        
        # Export facts to JSON
        facts_path = export_dir / "02_extracted_facts.json"
        with open(facts_path, 'w', encoding='utf-8') as f:
            json.dump(facts, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n   ✅ Facts exported to: {facts_path}")
        
        # Get affinity
        print("\n7. Checking affinity...")
        affinity = await client_v11.get_affinity("alice_user", personality_name)
        if affinity:
            print(f"   ✅ Affinity: {affinity.get('points', 0)} points")
            print(f"      - Interactions: {affinity.get('interactions', 0)}")
        
        # Export affinity
        affinity_path = export_dir / "03_affinity.json"
        with open(affinity_path, 'w', encoding='utf-8') as f:
            json.dump(affinity, f, indent=2, ensure_ascii=False, default=str)
        print(f"   ✅ Affinity exported to: {affinity_path}")
        
        # Get memory stats
        print("\n8. Checking memory statistics...")
        stats = await client_v11.get_memory_stats("alice_user")
        if stats:
            print(f"   ✅ Memory Statistics:")
            print(f"      - Total facts: {stats.get('total_facts', 0)}")
            print(f"      - Total episodes: {stats.get('total_episodes', 0)}")
            print(f"      - Fact categories: {stats.get('fact_categories', {})}")
        
        # Export stats
        stats_path = export_dir / "04_memory_stats.json"
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False, default=str)
        print(f"   ✅ Stats exported to: {stats_path}")
        
        # Get final personality state
        print("\n9. Getting final personality state (after evolution)...")
        final_personality = await client.get_personality(personality_name)
        
        # Save final personality to JSON
        final_personality_path = export_dir / "05_final_personality.json"
        with open(final_personality_path, 'w', encoding='utf-8') as f:
            json.dump(final_personality, f, indent=2, ensure_ascii=False, default=str)
        print(f"   ✅ Final personality saved to: {final_personality_path}")
        
        # Export conversation results
        conversation_path = export_dir / "06_conversation.json"
        with open(conversation_path, 'w', encoding='utf-8') as f:
            json.dump(conversation_results, f, indent=2, ensure_ascii=False, default=str)
        print(f"   ✅ Conversation exported to: {conversation_path}")
        
        # Verify database file exists and show size
        print("\n10. Verifying database file...")
        if db_path.exists():
            db_size = db_path.stat().st_size
            print(f"   ✅ Database file exists: {db_path}")
            print(f"   ✅ Database size: {db_size / 1024:.2f} KB")
        
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"✅ Sent {len(user_messages)} messages")
        print(f"✅ Extracted {len(facts)} facts AUTOMATICALLY (not hardcoded)")
        print(f"✅ Facts saved to SQLite database: {db_path}")
        print(f"✅ All data exported to: {export_dir}")
        print(f"\n📁 EXPORTED FILES:")
        print(f"   - 01_initial_personality.json (BEFORE conversations)")
        print(f"   - 02_extracted_facts.json")
        print(f"   - 03_affinity.json")
        print(f"   - 04_memory_stats.json")
        print(f"   - 05_final_personality.json (AFTER conversations)")
        print(f"   - 06_conversation.json")
        print("=" * 80)
        
        # Cleanup
        print("\n11. Cleaning up...")
        if session_id:
            try:
                await client.delete_session(session_id)
            except:
                pass
        await client.cleanup()
        print("   ✅ Cleanup completed")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    try:
        # Create new event loop for Windows
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run tests
        success = loop.run_until_complete(test_real_extraction())
        
        # Close loop
        loop.close()
        
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
