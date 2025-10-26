"""
Comprehensive Storage Backend Tests for LuminoraCore

Tests JSON, In-Memory, and SQLite storage implementations
"""

import asyncio
import os
import tempfile
import shutil
from pathlib import Path
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Suppress specific warnings and info messages
logging.getLogger('luminoracore_sdk.personality.manager').setLevel(logging.ERROR)
logging.getLogger('luminoracore_sdk.client').setLevel(logging.ERROR)
logging.getLogger('luminoracore_sdk.personality.blender').setLevel(logging.ERROR)
logging.getLogger('luminoracore_sdk.session.storage_v1_1').setLevel(logging.ERROR)


async def test_in_memory_storage():
    """Test In-Memory Storage"""
    print("\n" + "=" * 80)
    print("TEST 1: IN-MEMORY STORAGE")
    print("=" * 80)
    
    try:
        from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
        from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
        from luminoracore_sdk.types.provider import ProviderConfig
        
        # Initialize client
        print("\n1. Initializing In-Memory Storage...")
        client = LuminoraCoreClient()
        await client.initialize()
        
        storage = InMemoryStorageV11()
        client_v11 = LuminoraCoreClientV11(client, storage_v11=storage)
        print("   ✅ In-Memory Storage initialized")
        
        # Test fact saving
        print("\n2. Testing fact saving and retrieval...")
        fact_saved = await client_v11.save_fact(
            "test_user_memory",
            "personal",
            "name",
            "Test User Memory",
            confidence=0.9
        )
        assert fact_saved, "Fact saving failed"
        print("   ✅ Fact saved successfully")
        
        facts = await client_v11.get_facts("test_user_memory")
        assert len(facts) == 1, f"Expected 1 fact, got {len(facts)}"
        assert facts[0]['value'] == "Test User Memory"
        print(f"   ✅ Fact retrieved: {facts[0]['key']} = {facts[0]['value']}")
        
        # Test episode saving
        print("\n3. Testing episode saving and retrieval...")
        episode_saved = await client_v11.save_episode(
            "test_user_memory",
            "milestone",
            "First Test",
            "Completed first memory test",
            0.8,
            "positive"
        )
        assert episode_saved, "Episode saving failed"
        print("   ✅ Episode saved successfully")
        
        episodes = await client_v11.get_episodes("test_user_memory")
        assert len(episodes) == 1, f"Expected 1 episode, got {len(episodes)}"
        print(f"   ✅ Episode retrieved: {episodes[0]['title']}")
        
        # Test affinity update
        print("\n4. Testing affinity update...")
        affinity = await client_v11.update_affinity(
            "test_user_memory",
            "test_personality",
            10,
            "positive"
        )
        assert affinity is not None, "Affinity update failed"
        print("   ✅ Affinity updated successfully")
        
        # Test memory stats
        print("\n5. Testing memory stats...")
        stats = await client_v11.get_memory_stats("test_user_memory")
        assert stats is not None, "Memory stats retrieval failed"
        print(f"   ✅ Memory stats retrieved: {stats}")
        
        # Cleanup
        await client.cleanup()
        
        print("\n" + "=" * 80)
        print("✅ IN-MEMORY STORAGE TEST PASSED")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"\n❌ IN-MEMORY STORAGE TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_json_storage():
    """Test JSON File Storage"""
    print("\n" + "=" * 80)
    print("TEST 2: JSON FILE STORAGE")
    print("=" * 80)
    
    temp_dir = None
    json_file_path = None
    
    try:
        print("[DEBUG] Importing modules...")
        from luminoracore_sdk import LuminoraCoreClient
        from luminoracore_sdk.session.storage import JSONFileStorage
        from luminoracore_sdk.types.session import StorageConfig, StorageType
        print("[DEBUG] Modules imported successfully")
        
        # Create temporary directory for JSON file
        temp_dir = tempfile.mkdtemp()
        json_file_path = os.path.join(temp_dir, "test_sessions.json")
        
        # Initialize JSON storage
        print(f"\n1. Initializing JSON File Storage at {json_file_path}...")
        storage_config = StorageConfig(
            storage_type=StorageType.JSON,
            connection_string=json_file_path
        )
        
        json_storage = JSONFileStorage(storage_config)
        print("   ✅ JSON File Storage initialized")
        
        # Test session operations
        print("\n2. Testing session operations...")
        test_session_id = "test_json_session"
        test_session_data = {
            "user_id": "test_user_json",
            "personality_name": "test",
            "created_at": "2024-01-01T00:00:00",
            "expires_at": "2024-12-31T23:59:59"
        }
        
        # Save session
        saved = await json_storage.save_session(test_session_id, test_session_data)
        assert saved, "Session save failed"
        print("   ✅ Session saved to JSON file")
        
        # Check file exists
        assert os.path.exists(json_file_path), "JSON file was not created"
        print(f"   ✅ JSON file created: {json_file_path}")
        
        # Load session
        loaded_session = await json_storage.load_session(test_session_id)
        assert loaded_session is not None, "Session load failed"
        assert loaded_session["user_id"] == "test_user_json"
        print("   ✅ Session loaded from JSON file")
        
        # List sessions
        sessions = await json_storage.list_sessions()
        assert test_session_id in sessions, "Session not in list"
        print(f"   ✅ Session listed: {len(sessions)} session(s)")
        
        # Check session exists
        exists = await json_storage.session_exists(test_session_id)
        assert exists, "Session existence check failed"
        print("   ✅ Session existence verified")
        
        # Delete session
        print("   [DEBUG] About to delete session...")
        try:
            deleted = await asyncio.wait_for(json_storage.delete_session(test_session_id), timeout=5.0)
            print(f"   [DEBUG] Delete returned: {deleted}")
        except asyncio.TimeoutError:
            print("   ❌ Delete operation timed out!")
            return False
        except Exception as e:
            print(f"   ❌ Delete operation failed: {e}")
            return False
            
        assert deleted, "Session deletion failed"
        print("   ✅ Session deleted from JSON file")
        
        # Verify deletion
        print("   [DEBUG] Verifying deletion...")
        loaded_after_delete = await json_storage.load_session(test_session_id)
        assert loaded_after_delete is None, "Session should be deleted"
        print("   ✅ Deletion verified")
        
        print("\n" + "=" * 80)
        print("✅ JSON FILE STORAGE TEST PASSED")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"\n❌ JSON FILE STORAGE TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


async def test_sqlite_storage():
    """Test SQLite Storage"""
    print("\n" + "=" * 80)
    print("TEST 3: SQLITE STORAGE")
    print("=" * 80)
    
    temp_dir = None
    db_path = None
    
    try:
        from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
        from luminoracore_sdk.session.storage_sqlite_flexible import FlexibleSQLiteStorageV11
        
        # Create temporary directory for SQLite database
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_luminora.db")
        
        # Initialize SQLite storage
        print(f"\n1. Initializing SQLite Storage at {db_path}...")
        storage = FlexibleSQLiteStorageV11(
            database_path=db_path,
            auto_create_tables=True
        )
        print("   ✅ SQLite Storage initialized")
        print(f"   📊 Database file: {db_path}")
        print(f"   📋 Tables: {storage.facts_table}, {storage.affinity_table}, {storage.episodes_table}")
        
        # Initialize client
        client = LuminoraCoreClient()
        await client.initialize()
        client_v11 = LuminoraCoreClientV11(client, storage_v11=storage)
        
        # Test fact saving
        print("\n2. Testing fact saving and retrieval...")
        fact_saved = await client_v11.save_fact(
            "test_user_sqlite",
            "personal",
            "name",
            "Test User SQLite",
            confidence=0.95
        )
        assert fact_saved, "Fact saving failed"
        print("   ✅ Fact saved to SQLite database")
        
        # Add more facts
        await client_v11.save_fact("test_user_sqlite", "personal", "age", "25", confidence=0.9)
        await client_v11.save_fact("test_user_sqlite", "preferences", "language", "Python", confidence=0.85)
        print("   ✅ Multiple facts saved")
        
        # Retrieve facts
        facts = await client_v11.get_facts("test_user_sqlite")
        assert len(facts) >= 3, f"Expected at least 3 facts, got {len(facts)}"
        print(f"   ✅ Retrieved {len(facts)} facts from SQLite database")
        for fact in facts:
            print(f"      - {fact['key']}: {fact['value']} (confidence: {fact.get('confidence', 'N/A')})")
        
        # Test episode saving
        print("\n3. Testing episode saving and retrieval...")
        episode_saved = await client_v11.save_episode(
            "test_user_sqlite",
            "milestone",
            "First SQLite Test",
            "Completed first SQLite storage test",
            0.9,
            "positive"
        )
        assert episode_saved, "Episode saving failed"
        print("   ✅ Episode saved to SQLite database")
        
        episodes = await client_v11.get_episodes("test_user_sqlite")
        assert len(episodes) == 1, f"Expected 1 episode, got {len(episodes)}"
        print(f"   ✅ Retrieved episode: {episodes[0]['title']}")
        
        # Test affinity update
        print("\n4. Testing affinity update...")
        affinity = await client_v11.update_affinity(
            "test_user_sqlite",
            "test_personality",
            15,
            "positive"
        )
        assert affinity is not None, "Affinity update failed"
        print("   ✅ Affinity updated in SQLite database")
        
        # Test memory stats
        print("\n5. Testing memory stats...")
        stats = await client_v11.get_memory_stats("test_user_sqlite")
        assert stats is not None, "Memory stats retrieval failed"
        print(f"   ✅ Memory stats retrieved: {stats}")
        
        # Verify file size
        if os.path.exists(db_path):
            file_size = os.path.getsize(db_path)
            print(f"\n   📊 Database file size: {file_size} bytes")
        
        # Cleanup
        await client.cleanup()
        
        print("\n" + "=" * 80)
        print("✅ SQLITE STORAGE TEST PASSED")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"\n❌ SQLITE STORAGE TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


async def run_all_storage_tests():
    """Run all storage backend tests"""
    print("\n" + "=" * 80)
    print("LUMINORACORE STORAGE BACKEND COMPREHENSIVE TESTS")
    print("=" * 80)
    print("\nTesting JSON, In-Memory, and SQLite storage implementations...")
    
    results = {
        "In-Memory": False,
        "JSON": False,
        "SQLite": False
    }
    
    # Test 1: In-Memory Storage
    results["In-Memory"] = await test_in_memory_storage()
    
    # Test 2: JSON Storage
    results["JSON"] = await test_json_storage()
    
    # Test 3: SQLite Storage
    results["SQLite"] = await test_sqlite_storage()
    
    # Summary
    print("\n" + "=" * 80)
    print("STORAGE BACKEND TEST SUMMARY")
    print("=" * 80)
    
    for storage_type, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{storage_type}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    print("\n" + "=" * 80)
    print(f"RESULTS: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("🎉 ALL STORAGE BACKEND TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED")
    
    print("=" * 80)
    
    return total_passed == total_tests


if __name__ == "__main__":
    try:
        # Create new event loop for Windows
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run tests
        results = loop.run_until_complete(run_all_storage_tests())
        
        # Close loop
        loop.close()
        
        sys.exit(0 if results else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
