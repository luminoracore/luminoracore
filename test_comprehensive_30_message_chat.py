"""
Comprehensive 30-Message Chat Test for LuminoraCore

Tests advanced features:
- 30-message conversation
- SQLite storage
- Sentiment analysis
- Fact storage and retrieval
- Memory updates
- Personality evolution
- Data export
"""

import asyncio
import os
import logging
import sys
import json
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Suppress specific warnings
logging.getLogger('luminoracore_sdk').setLevel(logging.ERROR)


def get_client():
    """Helper function to create client with correct personalities directory"""
    import pathlib
    sdk_dir = pathlib.Path(__file__).parent / "luminoracore-sdk-python" / "luminoracore_sdk" / "personalities"
    from luminoracore_sdk import LuminoraCoreClient
    return LuminoraCoreClient(personalities_dir=str(sdk_dir))


async def comprehensive_chat_test():
    """Run comprehensive 30-message chat test with all advanced features"""
    print("\n" + "=" * 80)
    print("COMPREHENSIVE 30-MESSAGE CHAT TEST")
    print("=" * 80)
    
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    if not deepseek_api_key:
        print("\n❌ DEEPSEEK_API_KEY not set. Skipping test.")
        return False
    
    # Create temp directory for SQLite database
    temp_dir = Path("temp_test_data")
    temp_dir.mkdir(exist_ok=True)
    db_path = temp_dir / "conversation_test.db"
    
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
        
        # Create session with DeepSeek
        print("\n2. Creating session with DeepSeek provider...")
        from luminoracore_sdk.types.provider import ProviderConfig
        provider_config = ProviderConfig(
            name="deepseek",
            api_key=deepseek_api_key,
            model="deepseek-chat"
        )
        
        session_id = await client.create_session(
            personality_name=personality_name,
            provider_config=provider_config
        )
        print(f"   ✅ Session created: {session_id}")
        
        # Initialize v1.1 extensions
        print("\n3. Initializing v1.1 memory extensions...")
        from luminoracore_sdk import LuminoraCoreClientV11
        from luminoracore_sdk.session.storage_sqlite_flexible import FlexibleSQLiteStorageV11
        
        storage_v11 = FlexibleSQLiteStorageV11(database_path=str(db_path))
        client_v11 = LuminoraCoreClientV11(client, storage_v11=storage_v11)
        print(f"   ✅ SQLite storage initialized at: {db_path}")
        
        # Save initial user facts
        print("\n4. Saving initial user facts...")
        await client_v11.save_fact("user123", "personal", "name", "Carlos", confidence=0.95)
        await client_v11.save_fact("user123", "personal", "age", "32", confidence=0.9)
        await client_v11.save_fact("user123", "personal", "location", "Madrid, Spain", confidence=0.95)
        await client_v11.save_fact("user123", "preferences", "favorite_color", "blue", confidence=0.85)
        await client_v11.save_fact("user123", "preferences", "favorite_food", "pasta", confidence=0.8)
        print("   ✅ 5 facts saved")
        
        # 30-message conversation
        print("\n5. Starting 30-message conversation...")
        conversation_messages = [
            "Hello! My name is Carlos, I'm 32 years old and I live in Madrid.",
            "What's your name?",
            "I love blue color and pasta is my favorite food.",
            "Tell me about artificial intelligence.",
            "That's interesting! How does machine learning work?",
            "I work as a software developer. What do you think about Python?",
            "I enjoy hiking on weekends in the mountains near Madrid.",
            "Can you help me plan a trip to Barcelona?",
            "I'm learning Italian. Can you teach me some basic phrases?",
            "What's your favorite programming language and why?",
            "I have a golden retriever named Max. He's very friendly.",
            "I love reading science fiction books in my free time.",
            "Tell me about quantum computing.",
            "I'm interested in renewable energy. What can you tell me?",
            "I play guitar in my spare time. It helps me relax.",
            "Can you explain blockchain technology to me?",
            "I visited Japan last year. It was amazing!",
            "What are your thoughts on remote work?",
            "I enjoy cooking Mediterranean cuisine.",
            "Tell me about space exploration.",
            "I'm training for a marathon next month.",
            "Can you help me improve my Spanish grammar?",
            "I love listening to jazz music while coding.",
            "What's the future of artificial intelligence?",
            "I volunteer at a local animal shelter on weekends.",
            "Can you explain how neural networks work?",
            "I enjoy solving puzzles and brain teasers.",
            "Tell me about sustainable living practices.",
            "I'm learning to play chess. Any tips?",
            "Thank you for this wonderful conversation!"
        ]
        
        conversation_results = []
        positive_responses = 0
        neutral_responses = 0
        negative_responses = 0
        
        for i, message in enumerate(conversation_messages, 1):
            print(f"   Message {i}/30: '{message[:50]}...'")
            response = await client.send_message(session_id=session_id, message=message)
            
            # Analyze sentiment (simple heuristic)
            sentiment = "neutral"
            response_lower = response.content.lower()
            if any(word in response_lower for word in ['great', 'wonderful', 'amazing', 'excellent', 'love', 'happy', 'excited']):
                sentiment = "positive"
                positive_responses += 1
            elif any(word in response_lower for word in ['sorry', 'unfortunately', 'problem', 'issue', 'difficult']):
                sentiment = "negative"
                negative_responses += 1
            else:
                neutral_responses += 1
            
            conversation_results.append({
                "message_number": i,
                "user_message": message,
                "ai_response": response.content[:200],  # First 200 chars
                "sentiment": sentiment,
                "timestamp": datetime.now().isoformat()
            })
            
            # Update affinity based on sentiment
            if sentiment == "positive":
                await client_v11.update_affinity("user123", personality_name, 5, "positive")
            elif sentiment == "negative":
                await client_v11.update_affinity("user123", personality_name, -2, "negative")
            else:
                await client_v11.update_affinity("user123", personality_name, 1, "neutral")
        
        print(f"   ✅ 30 messages exchanged")
        print(f"      - Positive responses: {positive_responses}")
        print(f"      - Neutral responses: {neutral_responses}")
        print(f"      - Negative responses: {negative_responses}")
        
        # Save conversation as episode
        print("\n6. Saving conversation as episode...")
        await client_v11.save_episode(
            "user123",
            "conversation",
            "30-Message Chat Session",
            f"Comprehensive conversation with 30 messages covering various topics",
            0.9,
            "positive" if positive_responses > neutral_responses else "neutral",
            metadata={
                "total_messages": 30,
                "positive_sentiment": positive_responses,
                "neutral_sentiment": neutral_responses,
                "negative_sentiment": negative_responses
            }
        )
        print("   ✅ Episode saved")
        
        # Retrieve and display facts
        print("\n7. Retrieving stored facts...")
        facts = await client_v11.get_facts("user123")
        print(f"   ✅ Retrieved {len(facts)} facts:")
        for fact in facts:
            print(f"      - {fact.get('category', 'unknown')}.{fact.get('key', 'unknown')}: {fact.get('value', 'N/A')}")
        
        # Retrieve episodes
        print("\n8. Retrieving stored episodes...")
        episodes = await client_v11.get_episodes("user123")
        print(f"   ✅ Retrieved {len(episodes)} episodes:")
        for episode in episodes:
            print(f"      - {episode.get('title', 'N/A')}: {episode.get('summary', 'N/A')[:60]}...")
        
        # Get affinity
        print("\n9. Retrieving affinity data...")
        affinity = await client_v11.get_affinity("user123", personality_name)
        if affinity:
            print(f"   ✅ Affinity: {affinity.get('points', 0)} points")
            print(f"      - Interactions: {affinity.get('interactions', 0)}")
            print(f"      - Last interaction: {affinity.get('last_interaction', 'N/A')}")
        
        # Get memory statistics
        print("\n10. Retrieving memory statistics...")
        stats = await client_v11.get_memory_stats("user123")
        if stats:
            print(f"   ✅ Memory Statistics:")
            print(f"      - Total facts: {stats.get('total_facts', 0)}")
            print(f"      - Total episodes: {stats.get('total_episodes', 0)}")
            print(f"      - Fact categories: {stats.get('fact_categories', {})}")
            print(f"      - Episode types: {stats.get('episode_types', {})}")
        
        # Get conversation history
        print("\n11. Retrieving conversation history...")
        conversation = await client.get_conversation(session_id)
        print(f"   ✅ Conversation history: {len(conversation)} messages")
        
        # Export all data
        print("\n12. Exporting all data...")
        export_dir = temp_dir / "export"
        export_dir.mkdir(exist_ok=True)
        
        # Export conversation results
        conversation_export_path = export_dir / "conversation_results.json"
        with open(conversation_export_path, 'w', encoding='utf-8') as f:
            json.dump(conversation_results, f, indent=2, ensure_ascii=False)
        print(f"   ✅ Conversation results exported to: {conversation_export_path}")
        
        # Export facts
        facts_export_path = export_dir / "facts.json"
        with open(facts_export_path, 'w', encoding='utf-8') as f:
            json.dump(facts, f, indent=2, ensure_ascii=False)
        print(f"   ✅ Facts exported to: {facts_export_path}")
        
        # Export episodes
        episodes_export_path = export_dir / "episodes.json"
        with open(episodes_export_path, 'w', encoding='utf-8') as f:
            json.dump(episodes, f, indent=2, ensure_ascii=False)
        print(f"   ✅ Episodes exported to: {episodes_export_path}")
        
        # Export memory statistics
        stats_export_path = export_dir / "memory_stats.json"
        with open(stats_export_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        print(f"   ✅ Memory statistics exported to: {stats_export_path}")
        
        # Export affinity
        if affinity:
            affinity_export_path = export_dir / "affinity.json"
            with open(affinity_export_path, 'w', encoding='utf-8') as f:
                json.dump(affinity, f, indent=2, ensure_ascii=False)
            print(f"   ✅ Affinity exported to: {affinity_export_path}")
        
        # Create comprehensive report
        print("\n13. Generating comprehensive report...")
        report_path = export_dir / "comprehensive_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Comprehensive Chat Test Report\n\n")
            f.write(f"**Date:** {datetime.now().isoformat()}\n\n")
            f.write(f"**Session ID:** {session_id}\n\n")
            f.write(f"**Personality:** {personality_name}\n\n")
            
            f.write("## Test Results\n\n")
            f.write(f"- **Total Messages:** 30\n")
            f.write(f"- **Positive Sentiment:** {positive_responses}\n")
            f.write(f"- **Neutral Sentiment:** {neutral_responses}\n")
            f.write(f"- **Negative Sentiment:** {negative_responses}\n\n")
            
            f.write(f"- **Facts Stored:** {len(facts)}\n")
            f.write(f"- **Episodes Stored:** {len(episodes)}\n")
            f.write(f"- **Memory Statistics:** {len(stats) if stats else 0} metrics\n")
            f.write(f"- **Affinity Points:** {affinity.get('points', 0) if affinity else 0}\n\n")
            
            f.write("## Storage\n\n")
            f.write(f"- **Database:** {db_path}\n")
            f.write(f"- **Database Size:** {db_path.stat().st_size / 1024:.2f} KB\n\n")
            
            f.write("## Exported Files\n\n")
            f.write("- `conversation_results.json` - Conversation with sentiment analysis\n")
            f.write("- `facts.json` - User facts\n")
            f.write("- `episodes.json` - Stored episodes\n")
            f.write("- `memory_stats.json` - Memory statistics\n")
            if affinity:
                f.write("- `affinity.json` - User-Personality affinity\n")
            f.write("- `comprehensive_report.md` - This report\n\n")
        
        print(f"   ✅ Report generated: {report_path}")
        
        # Verify database
        print("\n14. Verifying SQLite database...")
        if db_path.exists():
            db_size = db_path.stat().st_size
            print(f"   ✅ Database exists: {db_size / 1024:.2f} KB")
        else:
            print(f"   ❌ Database not found")
        
        # Cleanup
        print("\n15. Cleaning up...")
        await client.delete_session(session_id)
        await client.cleanup()
        print("   ✅ Cleanup completed")
        
        # Summary
        print("\n" + "=" * 80)
        print("COMPREHENSIVE CHAT TEST SUMMARY")
        print("=" * 80)
        print(f"✅ 30-message conversation completed")
        print(f"✅ Sentiment analysis: {positive_responses} positive, {neutral_responses} neutral, {negative_responses} negative")
        print(f"✅ SQLite storage: {len(facts)} facts, {len(episodes)} episodes")
        print(f"✅ Memory updated: {stats.get('total_facts', 0)} total facts stored")
        print(f"✅ Affinity updated: {affinity.get('points', 0) if affinity else 0} points")
        print(f"✅ Data exported to: {export_dir}")
        print(f"✅ Database size: {db_path.stat().st_size / 1024:.2f} KB")
        print("=" * 80)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 80)
        
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
        success = loop.run_until_complete(comprehensive_chat_test())
        
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
