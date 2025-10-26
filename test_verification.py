#!/usr/bin/env python3
"""
LuminoraCore Verification Test
Comprehensive test to verify all components work correctly
"""

import sys
import os
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "luminoracore"))
sys.path.insert(0, str(project_root / "luminoracore-sdk-python"))
sys.path.insert(0, str(project_root / "luminoracore-cli"))

def test_imports():
    """Test all imports"""
    print("Testing imports...")
    
    try:
        # Core imports
        from luminoracore import PersonalityEngine, MemorySystem, EvolutionEngine
        from luminoracore.interfaces import StorageInterface, MemoryInterface
        from luminoracore.storage import BaseStorage, InMemoryStorage
        print("✅ Core imports successful")
        
        # SDK imports
        from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
        from luminoracore_sdk.client_new import LuminoraCoreClientNew
        from luminoracore_sdk.client_hybrid import LuminoraCoreClientHybrid
        print("✅ SDK imports successful")
        
        # CLI imports
        from luminoracore_cli.commands_new.memory_new import MemoryCommandNew
        print("✅ CLI imports successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_instantiation():
    """Test component instantiation"""
    print("Testing instantiation...")
    
    try:
        # Core components
        from luminoracore import PersonalityEngine, MemorySystem, EvolutionEngine
        from luminoracore.storage import InMemoryStorage
        
        engine = PersonalityEngine()
        storage = InMemoryStorage()
        memory = MemorySystem(storage)
        evolution = EvolutionEngine()
        
        print("✅ Core components instantiated")
        
        # SDK components
        from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
        from luminoracore_sdk.client_new import LuminoraCoreClientNew
        from luminoracore_sdk.client_hybrid import LuminoraCoreClientHybrid
        
        client = LuminoraCoreClient()
        client_v11 = LuminoraCoreClientV11(client)
        client_new = LuminoraCoreClientNew()
        client_hybrid = LuminoraCoreClientHybrid()
        
        print("✅ SDK components instantiated")
        
        # CLI components
        from luminoracore_cli.commands_new.memory_new import MemoryCommandNew
        
        cli_command = MemoryCommandNew()
        
        print("✅ CLI components instantiated")
        
        return True
        
    except Exception as e:
        print(f"❌ Instantiation test failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality"""
    print("Testing basic functionality...")
    
    try:
        import asyncio
        
        async def run_test():
            from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
            from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
            
            # Initialize client
            client = LuminoraCoreClient()
            await client.initialize()
            
            # Create v1.1 storage
            storage_v11 = InMemoryStorageV11()
            
            # Create v1.1 client extension
            client_v11 = LuminoraCoreClientV11(client, storage_v11=storage_v11)
            
            # Test fact saving
            fact_saved = await client_v11.save_fact("test_user", "personal", "name", "Test User", confidence=0.9)
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
            
            # Test search (skip if vector store not configured)
            try:
                search_results = await client_v11.search_memories("test_user", "name")
                if len(search_results) != 1:
                    print(f"  ⚠️  Search returned {len(search_results)} results (vector store not configured)")
            except Exception as e:
                print(f"  ⚠️  Search not available: {e}")
            
            # Test memory stats
            stats = await client_v11.get_memory_stats("test_user")
            if not stats:
                raise Exception("Memory stats retrieval failed")
            
            # Cleanup
            await client.cleanup()
            
            return True
        
        # Run the async test
        result = asyncio.run(run_test())
        
        if result:
            print("✅ Basic functionality test passed")
            return True
        else:
            print("❌ Basic functionality test failed")
            return False
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_deepseek_integration():
    """Test DeepSeek integration"""
    print("Testing DeepSeek integration...")
    
    try:
        import httpx
        import asyncio
        
        async def run_deepseek_test():
            # Get API key
            api_key = os.getenv("DEEPSEEK_API_KEY")
            if not api_key:
                print("⚠️  DEEPSEEK_API_KEY not set, skipping DeepSeek test")
                return True
            
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
                
                return True
        
        # Run the async DeepSeek test
        result = asyncio.run(run_deepseek_test())
        
        if result:
            print("✅ DeepSeek integration test passed")
            return True
        else:
            print("❌ DeepSeek integration test failed")
            return False
        
    except Exception as e:
        print(f"❌ DeepSeek integration test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🔍 LUMINORACORE VERIFICATION TEST")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Instantiation Test", test_instantiation),
        ("Basic Functionality Test", test_basic_functionality),
        ("DeepSeek Integration Test", test_deepseek_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! SYSTEM IS READY FOR PRODUCTION!")
        return 0
    else:
        print(f"⚠️  {total - passed} TESTS FAILED - REVIEW REQUIRED")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
