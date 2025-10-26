"""
Comprehensive Client Capabilities Test for LuminoraCore

Tests all client functionalities including sessions, messages, memory, and providers.
"""

import asyncio
import os
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


def get_client():
    """Helper function to create client with correct personalities directory"""
    import pathlib
    sdk_dir = pathlib.Path(__file__).parent / "luminoracore-sdk-python" / "luminoracore_sdk" / "personalities"
    from luminoracore_sdk import LuminoraCoreClient
    return LuminoraCoreClient(personalities_dir=str(sdk_dir))


async def test_client_initialization():
    """Test basic client initialization"""
    print("\n" + "=" * 80)
    print("TEST 1: CLIENT INITIALIZATION")
    print("=" * 80)
    
    try:
        print("\n1. Creating LuminoraCore client...")
        client = get_client()
        print("   ✅ Client created")
        
        print("\n2. Initializing client...")
        await client.initialize()
        print("   ✅ Client initialized successfully")
        
        print("\n3. Checking client attributes...")
        assert hasattr(client, 'session_manager'), "Client missing session_manager"
        assert hasattr(client, 'personality_manager'), "Client missing personality_manager"
        print("   ✅ All required attributes present")
        
        print("\n4. Cleaning up...")
        await client.cleanup()
        print("   ✅ Client cleaned up successfully")
        
        print("\n" + "=" * 80)
        print("✅ CLIENT INITIALIZATION TEST PASSED")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"\n❌ CLIENT INITIALIZATION TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_session_management():
    """Test session creation and management"""
    print("\n" + "=" * 80)
    print("TEST 2: SESSION MANAGEMENT")
    print("=" * 80)
    
    try:
        from luminoracore_sdk import LuminoraCoreClient
        from luminoracore_sdk.types.provider import ProviderConfig
        
        # Initialize client
        print("\n1. Initializing client...")
        client = get_client()
        await client.initialize()
        print("   ✅ Client initialized")
        
        # Get DeepSeek API key from environment
        print("\n2. Getting DeepSeek API key...")
        deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        if not deepseek_api_key:
            print("   ⚠️  DEEPSEEK_API_KEY not set, skipping session creation test")
            await client.cleanup()
            return True
        
        print("   ✅ API key found")
        
        # Create provider configuration
        print("\n3. Creating provider configuration...")
        provider_config = ProviderConfig(
            name="deepseek",
            api_key=deepseek_api_key,
            model="deepseek-chat"
        )
        print("   ✅ Provider configuration created")
        
        # Create session
        print("\n4. Creating session...")
        session_id = await client.create_session(
            personality_name="dr_luna",
            provider_config=provider_config
        )
        print(f"   ✅ Session created: {session_id}")
        
        # Verify session was created (session ID exists)
        print("\n5. Verifying session creation...")
        assert session_id is not None, "Session ID should not be None"
        assert len(session_id) > 0, "Session ID should not be empty"
        print("   ✅ Session verification successful")
        
        # Cleanup
        print("\n6. Cleaning up...")
        await client.cleanup()
        print("   ✅ Client cleaned up")
        
        print("\n" + "=" * 80)
        print("✅ SESSION MANAGEMENT TEST PASSED")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"\n❌ SESSION MANAGEMENT TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_message_sending():
    """Test sending messages to the AI"""
    print("\n" + "=" * 80)
    print("TEST 3: MESSAGE SENDING")
    print("=" * 80)
    
    try:
        from luminoracore_sdk import LuminoraCoreClient
        from luminoracore_sdk.types.provider import ProviderConfig
        
        # Get DeepSeek API key
        deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        if not deepseek_api_key:
            print("   ⚠️  DEEPSEEK_API_KEY not set, skipping message test")
            return True
        
        # Initialize client
        print("\n1. Initializing client...")
        client = get_client()
        await client.initialize()
        
        # Create provider configuration
        print("\n2. Creating provider configuration...")
        provider_config = ProviderConfig(
            name="deepseek",
            api_key=deepseek_api_key,
            model="deepseek-chat"
        )
        
        # Create session
        print("\n3. Creating session...")
        session_id = await client.create_session(
            personality_name="dr_luna",
            provider_config=provider_config
        )
        print(f"   ✅ Session created: {session_id}")
        
        # Send first message
        print("\n4. Sending first message...")
        message1 = "Hello! What is 2+2?"
        print(f"   Message: '{message1}'")
        response1 = await client.send_message(
            session_id=session_id,
            message=message1
        )
        assert response1 is not None, "Response should not be None"
        assert hasattr(response1, 'content'), "Response should have content"
        print(f"   ✅ Response received: {response1.content[:100]}...")
        
        # Send second message
        print("\n5. Sending second message...")
        message2 = "What about 3+3?"
        print(f"   Message: '{message2}'")
        response2 = await client.send_message(
            session_id=session_id,
            message=message2
        )
        assert response2 is not None, "Response should not be None"
        print(f"   ✅ Response received: {response2.content[:100]}...")
        
        # Check conversation history
        print("\n6. Checking conversation context...")
        if hasattr(response2, 'conversation_history'):
            print(f"   ✅ Conversation history has {len(response2.conversation_history)} messages")
        
        # Cleanup
        print("\n7. Cleaning up...")
        await client.cleanup()
        
        print("\n" + "=" * 80)
        print("✅ MESSAGE SENDING TEST PASSED")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"\n❌ MESSAGE SENDING TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_client_v11_extensions():
    """Test v1.1 client extensions"""
    print("\n" + "=" * 80)
    print("TEST 4: CLIENT V1.1 EXTENSIONS")
    print("=" * 80)
    
    try:
        from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
        from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
        
        # Initialize base client
        print("\n1. Initializing base client...")
        client = get_client()
        await client.initialize()
        
        # Create v1.1 storage
        print("\n2. Creating v1.1 storage...")
        storage_v11 = InMemoryStorageV11()
        print("   ✅ Storage created")
        
        # Create v1.1 client extensions
        print("\n3. Creating v1.1 client extensions...")
        client_v11 = LuminoraCoreClientV11(client, storage_v11=storage_v11)
        print("   ✅ V1.1 client extensions created")
        
        # Test v1.1 methods
        print("\n4. Testing v1.1 methods...")
        
        # Save fact
        print("   4a. Testing save_fact...")
        fact_saved = await client_v11.save_fact(
            "test_user_v11",
            "personal",
            "name",
            "Test User V11",
            confidence=0.9
        )
        assert fact_saved, "Fact saving should succeed"
        print("      ✅ Fact saved")
        
        # Get facts
        print("   4b. Testing get_facts...")
        facts = await client_v11.get_facts("test_user_v11")
        assert len(facts) > 0, "Should have at least one fact"
        print(f"      ✅ Retrieved {len(facts)} fact(s)")
        
        # Save episode
        print("   4c. Testing save_episode...")
        episode_saved = await client_v11.save_episode(
            "test_user_v11",
            "milestone",
            "First V11 Test",
            "Testing v1.1 extensions",
            0.8,
            "positive"
        )
        assert episode_saved, "Episode saving should succeed"
        print("      ✅ Episode saved")
        
        # Get episodes
        print("   4d. Testing get_episodes...")
        episodes = await client_v11.get_episodes("test_user_v11")
        assert len(episodes) > 0, "Should have at least one episode"
        print(f"      ✅ Retrieved {len(episodes)} episode(s)")
        
        # Update affinity
        print("   4e. Testing update_affinity...")
        affinity = await client_v11.update_affinity(
            "test_user_v11",
            "test_personality",
            10,
            "positive"
        )
        assert affinity is not None, "Affinity update should succeed"
        print("      ✅ Affinity updated")
        
        # Get memory stats
        print("   4f. Testing get_memory_stats...")
        stats = await client_v11.get_memory_stats("test_user_v11")
        assert stats is not None, "Memory stats should be available"
        print(f"      ✅ Memory stats: {stats}")
        
        # Cleanup
        print("\n5. Cleaning up...")
        await client.cleanup()
        
        print("\n" + "=" * 80)
        print("✅ CLIENT V1.1 EXTENSIONS TEST PASSED")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"\n❌ CLIENT V1.1 EXTENSIONS TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_conversation_memory():
    """Test conversation memory capabilities"""
    print("\n" + "=" * 80)
    print("TEST 5: CONVERSATION MEMORY")
    print("=" * 80)
    
    try:
        from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
        from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
        from luminoracore_sdk.types.provider import ProviderConfig
        
        # Get DeepSeek API key
        deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        if not deepseek_api_key:
            print("   ⚠️  DEEPSEEK_API_KEY not set, skipping conversation memory test")
            return True
        
        # Initialize clients
        print("\n1. Initializing clients...")
        client = get_client()
        await client.initialize()
        
        storage_v11 = InMemoryStorageV11()
        client_v11 = LuminoraCoreClientV11(client, storage_v11=storage_v11)
        
        # Create provider configuration
        print("\n2. Creating provider configuration...")
        provider_config = ProviderConfig(
            name="deepseek",
            api_key=deepseek_api_key,
            model="deepseek-chat"
        )
        
        # Create session
        print("\n3. Creating session...")
        session_id = await client.create_session(
            personality_name="dr_luna",
            provider_config=provider_config
        )
        print(f"   ✅ Session created: {session_id}")
        
        # Save user information
        print("\n4. Saving user information...")
        await client_v11.save_fact(
            "conversation_user",
            "personal",
            "name",
            "Alice",
            confidence=0.9
        )
        await client_v11.save_fact(
            "conversation_user",
            "personal",
            "favorite_color",
            "blue",
            confidence=0.85
        )
        print("   ✅ User information saved")
        
        # Send message with memory
        print("\n5. Sending message with conversation memory...")
        message = "What's my name?"
        print(f"   Message: '{message}'")
        response = await client.send_message(
            session_id=session_id,
            message=message
        )
        print(f"   ✅ Response: {response.content[:150]}...")
        
        # Cleanup
        print("\n6. Cleaning up...")
        await client.cleanup()
        
        print("\n" + "=" * 80)
        print("✅ CONVERSATION MEMORY TEST PASSED")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"\n❌ CONVERSATION MEMORY TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_multiple_providers():
    """Test using different providers"""
    print("\n" + "=" * 80)
    print("TEST 6: MULTIPLE PROVIDERS")
    print("=" * 80)
    
    try:
        from luminoracore_sdk import LuminoraCoreClient
        from luminoracore_sdk.types.provider import ProviderConfig
        
        # Get DeepSeek API key
        deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        if not deepseek_api_key:
            print("   ⚠️  DEEPSEEK_API_KEY not set, skipping provider test")
            return True
        
        # Initialize client
        print("\n1. Initializing client...")
        client = get_client()
        await client.initialize()
        
        # Test DeepSeek
        print("\n2. Testing DeepSeek provider...")
        provider_config = ProviderConfig(
            name="deepseek",
            api_key=deepseek_api_key,
            model="deepseek-chat"
        )
        
        session_id = await client.create_session(
            personality_name="dr_luna",
            provider_config=provider_config
        )
        
        response = await client.send_message(
            session_id=session_id,
            message="Say hello in one word"
        )
        
        assert response is not None, "Response should not be None"
        print(f"   ✅ DeepSeek response: {response.content[:100]}")
        
        # Cleanup
        print("\n3. Cleaning up...")
        await client.cleanup()
        
        print("\n" + "=" * 80)
        print("✅ MULTIPLE PROVIDERS TEST PASSED")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"\n❌ MULTIPLE PROVIDERS TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_all_client_tests():
    """Run all client capability tests"""
    print("\n" + "=" * 80)
    print("LUMINORACORE CLIENT CAPABILITIES COMPREHENSIVE TESTS")
    print("=" * 80)
    print("\nTesting client initialization, sessions, messages, v1.1 extensions, and providers...")
    
    results = {
        "Client Initialization": False,
        "Session Management": False,
        "Message Sending": False,
        "Client V1.1 Extensions": False,
        "Conversation Memory": False,
        "Multiple Providers": False
    }
    
    # Run tests
    results["Client Initialization"] = await test_client_initialization()
    results["Session Management"] = await test_session_management()
    results["Message Sending"] = await test_message_sending()
    results["Client V1.1 Extensions"] = await test_client_v11_extensions()
    results["Conversation Memory"] = await test_conversation_memory()
    results["Multiple Providers"] = await test_multiple_providers()
    
    # Summary
    print("\n" + "=" * 80)
    print("CLIENT CAPABILITIES TEST SUMMARY")
    print("=" * 80)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    print("\n" + "=" * 80)
    print(f"RESULTS: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("🎉 ALL CLIENT CAPABILITIES TESTS PASSED!")
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
        results = loop.run_until_complete(run_all_client_tests())
        
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
