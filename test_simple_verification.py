#!/usr/bin/env python3
"""
Simple Verification Test
Basic test to verify all components work correctly
"""

import asyncio
import os
import sys
import time
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "luminoracore"))
sys.path.insert(0, str(project_root / "luminoracore-sdk-python"))
sys.path.insert(0, str(project_root / "luminoracore-cli"))

print("🔍 LUMINORACORE SIMPLE VERIFICATION TEST")
print("=" * 50)

# Test 1: Core Components
print("\n1. Testing Core Components...")
try:
    from luminoracore import PersonalityEngine, MemorySystem, EvolutionEngine
    from luminoracore.interfaces import StorageInterface, MemoryInterface
    from luminoracore.storage import BaseStorage, InMemoryStorage
    
    # Test instantiation
    engine = PersonalityEngine()
    storage = InMemoryStorage()
    memory = MemorySystem(storage)
    evolution = EvolutionEngine()
    
    print("  ✅ Core components imported and instantiated successfully")
    
except Exception as e:
    print(f"  ❌ Core components failed: {e}")
    sys.exit(1)

# Test 2: SDK Components
print("\n2. Testing SDK Components...")
try:
    from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
    from luminoracore_sdk.client_new import LuminoraCoreClientNew
    from luminoracore_sdk.client_hybrid import LuminoraCoreClientHybrid
    
    # Test instantiation
    client = LuminoraCoreClient()
    client_v11 = LuminoraCoreClientV11(client)
    client_new = LuminoraCoreClientNew()
    client_hybrid = LuminoraCoreClientHybrid()
    
    print("  ✅ SDK components imported and instantiated successfully")
    
except Exception as e:
    print(f"  ❌ SDK components failed: {e}")
    sys.exit(1)

# Test 3: CLI Components
print("\n3. Testing CLI Components...")
try:
    from luminoracore_cli.commands_new.memory_new import MemoryCommandNew
    
    # Test instantiation
    cli_command = MemoryCommandNew()
    
    print("  ✅ CLI components imported and instantiated successfully")
    
except Exception as e:
    print(f"  ❌ CLI components failed: {e}")
    sys.exit(1)

# Test 4: Basic Functionality
print("\n4. Testing Basic Functionality...")
async def test_basic_functionality():
    try:
        # Initialize client
        client = LuminoraCoreClient()
        await client.initialize()
        
        client_v11 = LuminoraCoreClientV11(client)
        
        # Test fact saving
        fact_saved = await client_v11.save_fact("test_user", "personal", "name", "Test User", 0.9)
        if not fact_saved:
            raise Exception("Fact saving failed")
        
        # Test fact retrieval
        facts = await client_v11.get_facts("test_user")
        if len(facts) != 1:
            raise Exception(f"Fact retrieval failed: expected 1, got {len(facts)}")
        
        # Test episode saving
        episode_saved = await client_v11.save_episode(
            "test_user", "conversation", "Test Episode", "A test conversation", 0.8, "positive"
        )
        if not episode_saved:
            raise Exception("Episode saving failed")
        
        # Test episode retrieval
        episodes = await client_v11.get_episodes("test_user")
        if len(episodes) != 1:
            raise Exception(f"Episode retrieval failed: expected 1, got {len(episodes)}")
        
        # Test affinity update
        affinity = await client_v11.update_affinity("test_user", "test_personality", 10, "positive")
        if not affinity:
            raise Exception("Affinity update failed")
        
        # Test affinity retrieval
        retrieved_affinity = await client_v11.get_affinity("test_user", "test_personality")
        if not retrieved_affinity:
            raise Exception("Affinity retrieval failed")
        
        # Test search
        search_results = await client_v11.search_facts("test_user", "name")
        if len(search_results) != 1:
            raise Exception(f"Search failed: expected 1, got {len(search_results)}")
        
        # Test user context
        context = await client_v11.get_user_context("test_user")
        if not context:
            raise Exception("User context retrieval failed")
        
        # Test user stats
        stats = await client_v11.get_user_stats("test_user")
        if not stats:
            raise Exception("User stats retrieval failed")
        
        # Test health check
        health = await client_v11.health_check()
        if not health or health.get("status") != "healthy":
            raise Exception("Health check failed")
        
        # Cleanup
        await client.cleanup()
        
        print("  ✅ Basic functionality test passed")
        
    except Exception as e:
        print(f"  ❌ Basic functionality test failed: {e}")
        raise

# Run the async test
asyncio.run(test_basic_functionality())

# Test 5: DeepSeek Integration
print("\n5. Testing DeepSeek Integration...")
async def test_deepseek_integration():
    try:
        import httpx
        
        # Get API key
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            print("  ⚠️  DEEPSEEK_API_KEY not set, skipping DeepSeek test")
            return
        
        # Test API connection
        async with httpx.AsyncClient(timeout=30.0) as client:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": "Hello, please respond with 'DeepSeek connection successful'"}],
                "temperature": 0.7,
                "max_tokens": 100
            }
            
            response = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            response.raise_for_status()
            result = response.json()
            
            if not result["choices"][0]["message"]["content"]:
                raise Exception("DeepSeek response is empty")
            
            print("  ✅ DeepSeek integration test passed")
            
    except Exception as e:
        print(f"  ❌ DeepSeek integration test failed: {e}")
        raise

# Run the async DeepSeek test
asyncio.run(test_deepseek_integration())

# Test 6: Cross-Component Compatibility
print("\n6. Testing Cross-Component Compatibility...")
async def test_cross_component_compatibility():
    try:
        # Test that all components can work together
        client = LuminoraCoreClient()
        await client.initialize()
        
        client_v11 = LuminoraCoreClientV11(client)
        client_new = LuminoraCoreClientNew()
        client_hybrid = LuminoraCoreClientHybrid()
        
        cli_command = MemoryCommandNew()
        
        # Test shared storage
        user_id = "compatibility_test_user"
        
        # Save facts using different clients
        await client_v11.save_fact(user_id, "personal", "name", "Compatibility Test", 0.9)
        await client_new.save_fact(user_id, "personal", "age", "25", 0.8)
        await client_hybrid.save_fact(user_id, "personal", "city", "Madrid", 0.7)
        
        # Verify facts are accessible from all clients
        facts_v11 = await client_v11.get_facts(user_id)
        facts_new = await client_new.get_facts(user_id)
        facts_hybrid = await client_hybrid.get_facts(user_id)
        facts_cli = await cli_command.list_facts(user_id)
        
        if len(facts_v11) != 3:
            raise Exception(f"V11 client facts count mismatch: {len(facts_v11)}")
        if len(facts_new) != 3:
            raise Exception(f"New client facts count mismatch: {len(facts_new)}")
        if len(facts_hybrid) != 3:
            raise Exception(f"Hybrid client facts count mismatch: {len(facts_hybrid)}")
        if len(facts_cli) != 3:
            raise Exception(f"CLI facts count mismatch: {len(facts_cli)}")
        
        await client.cleanup()
        
        print("  ✅ Cross-component compatibility test passed")
        
    except Exception as e:
        print(f"  ❌ Cross-component compatibility test failed: {e}")
        raise

# Run the async compatibility test
asyncio.run(test_cross_component_compatibility())

# Test 7: Performance Test
print("\n7. Testing Performance...")
async def test_performance():
    try:
        client = LuminoraCoreClient()
        await client.initialize()
        
        client_v11 = LuminoraCoreClientV11(client)
        
        # Test fact saving performance
        start_time = time.time()
        for i in range(50):
            await client_v11.save_fact("perf_user", "test", f"key_{i}", f"value_{i}", 0.8)
        fact_save_time = time.time() - start_time
        
        if fact_save_time > 10:
            raise Exception(f"Fact saving too slow: {fact_save_time:.2f}s")
        
        # Test fact retrieval performance
        start_time = time.time()
        facts = await client_v11.get_facts("perf_user")
        fact_retrieve_time = time.time() - start_time
        
        if fact_retrieve_time > 5:
            raise Exception(f"Fact retrieval too slow: {fact_retrieve_time:.2f}s")
        
        if len(facts) != 50:
            raise Exception(f"Fact count mismatch: {len(facts)}")
        
        await client.cleanup()
        
        print(f"  ✅ Performance test passed (save: {fact_save_time:.2f}s, retrieve: {fact_retrieve_time:.2f}s)")
        
    except Exception as e:
        print(f"  ❌ Performance test failed: {e}")
        raise

# Run the async performance test
asyncio.run(test_performance())

print("\n" + "=" * 50)
print("🎉 ALL TESTS PASSED! SYSTEM IS READY FOR PRODUCTION!")
print("=" * 50)
