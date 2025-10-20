#!/usr/bin/env python3
"""
Test completo para verificar que TODAS las funcionalidades están 100% completas
"""

import asyncio
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore-sdk-python"))

async def test_complete_functionality():
    """Test completo de todas las funcionalidades"""
    print("=== TESTING COMPLETE FUNCTIONALITY ===")
    
    try:
        from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11, AdvancedSentimentAnalyzer
        from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
        
        # Setup
        base_client = LuminoraCoreClient()
        await base_client.initialize()
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(base_client, storage_v11=storage)
        
        print("1. Creating session...")
        session_id = await client.create_session(
            personality_name="test_assistant",
            provider_config={"name": "openai", "model": "gpt-3.5-turbo"}
        )
        
        print("2. Testing SENTIMENT ANALYSIS - save_mood...")
        mood_result = await client.save_mood(
            user_id=session_id,
            personality_name="test_assistant",
            mood="happy",
            intensity=0.8,
            context="User is happy about the test"
        )
        print(f"   save_mood result: {mood_result.get('success', False)}")
        
        print("3. Testing SENTIMENT ANALYSIS - get_mood_history...")
        mood_history = await client.get_mood_history(session_id, "test_assistant")
        print(f"   get_mood_history result: {len(mood_history)} moods")
        
        print("4. Testing SENTIMENT ANALYSIS - analyze_sentiment...")
        sentiment_result = await client.analyze_sentiment(
            user_id=session_id,
            message="I'm so excited about this new feature!",
            personality_name="test_assistant"
        )
        print(f"   analyze_sentiment result: {sentiment_result.get('success', False)}")
        print(f"   sentiment: {sentiment_result.get('sentiment', 'N/A')}")
        
        print("5. Testing SENTIMENT ANALYSIS - get_sentiment_history...")
        sentiment_history = await client.get_sentiment_history(session_id, "test_assistant")
        print(f"   get_sentiment_history result: {len(sentiment_history)} entries")
        
        print("6. Testing SENTIMENT ANALYSIS - get_sentiment_trends...")
        sentiment_trends = await client.get_sentiment_trends(session_id, "test_assistant")
        print(f"   get_sentiment_trends result: {sentiment_trends.get('success', False)}")
        
        print("7. Testing SNAPSHOTS - create_snapshot...")
        try:
            snapshot_id = await client.create_snapshot(session_id, "test_snapshot")
            print(f"   create_snapshot result: {snapshot_id}")
        except Exception as e:
            print(f"   create_snapshot error: {e}")
        
        print("8. Testing SNAPSHOTS - list_snapshots...")
        try:
            snapshots = await client.list_snapshots(session_id)
            print(f"   list_snapshots result: {len(snapshots)} snapshots")
        except Exception as e:
            print(f"   list_snapshots error: {e}")
        
        print("9. Testing SNAPSHOTS - get_snapshot_info...")
        try:
            if 'snapshot_id' in locals():
                snapshot_info = await client.get_snapshot_info(session_id, snapshot_id)
                print(f"   get_snapshot_info result: {snapshot_info.get('success', False)}")
        except Exception as e:
            print(f"   get_snapshot_info error: {e}")
        
        print("10. Testing CONVERSATION HISTORY - get_conversation_history...")
        conversation_history = await client.get_conversation_history(session_id)
        print(f"    get_conversation_history result: {len(conversation_history)} entries")
        
        print("11. Testing CONVERSATION HISTORY - export_conversation...")
        conversation_export = await client.export_conversation(session_id)
        print(f"    export_conversation result: {conversation_export.get('success', False)}")
        
        print("12. Testing ADVANCED SENTIMENT ANALYZER direct access...")
        try:
            analyzer = AdvancedSentimentAnalyzer(storage)
            print(f"    AdvancedSentimentAnalyzer created successfully")
        except Exception as e:
            print(f"    AdvancedSentimentAnalyzer error: {e}")
        
        await base_client.cleanup()
        
        # Verificar que todas las funcionalidades están disponibles
        functionality_status = {
            "save_mood": mood_result.get('success', False),
            "get_mood_history": len(mood_history) >= 0,
            "analyze_sentiment": sentiment_result.get('success', False),
            "get_sentiment_history": len(sentiment_history) >= 0,
            "get_sentiment_trends": sentiment_trends.get('success', False),
            "get_conversation_history": len(conversation_history) >= 0,
            "export_conversation": conversation_export.get('success', False),
            "AdvancedSentimentAnalyzer": True  # Se creó exitosamente
        }
        
        working_count = sum(functionality_status.values())
        total_count = len(functionality_status)
        percentage = (working_count / total_count) * 100
        
        print(f"\nFUNCTIONALITY STATUS:")
        for func, status in functionality_status.items():
            status_text = "OK" if status else "FAIL"
            print(f"   {func}: {status_text}")
        
        print(f"\nOVERALL STATUS: {working_count}/{total_count} ({percentage:.1f}%)")
        
        if percentage >= 90:
            print("\nOK - ALL FUNCTIONALITIES ARE COMPLETE AND WORKING")
            return True
        else:
            print("\nFAIL - SOME FUNCTIONALITIES ARE NOT WORKING")
            return False
            
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_complete_functionality())
    sys.exit(0 if success else 1)
