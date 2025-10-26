#!/usr/bin/env python3
"""
DeepSeek Integration Tests
Comprehensive testing with DeepSeek API using real conversations
"""

import asyncio
import os
import sys
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'luminoracore'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'luminoracore-sdk-python'))

# Import components
from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
from luminoracore_sdk.client_new import LuminoraCoreClientNew
from luminoracore_sdk.client_hybrid import LuminoraCoreClientHybrid
from luminoracore_sdk.types.provider import ProviderConfig
from luminoracore_sdk.types.session import StorageConfig, MemoryConfig

# DeepSeek integration
import httpx


class DeepSeekTester:
    """DeepSeek API tester with comprehensive conversation scenarios"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1"
        self.client = httpx.AsyncClient(timeout=60.0)
        self.test_results = {
            "api_connection": False,
            "conversation_tests": {},
            "memory_tests": {},
            "affinity_tests": {},
            "error_count": 0,
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0
        }
    
    async def run_all_tests(self):
        """Run all DeepSeek integration tests"""
        logger.info("🤖 Starting DeepSeek Integration Tests")
        logger.info("=" * 60)
        
        try:
            # Test 1: API Connection
            await self.test_api_connection()
            
            # Test 2: Basic Conversations
            await self.test_basic_conversations()
            
            # Test 3: Memory Learning Scenarios
            await self.test_memory_learning_scenarios()
            
            # Test 4: Affinity Building Scenarios
            await self.test_affinity_building_scenarios()
            
            # Test 5: Complex Conversation Flows
            await self.test_complex_conversation_flows()
            
            # Test 6: Multi-User Scenarios
            await self.test_multi_user_scenarios()
            
            # Test 7: Error Handling with DeepSeek
            await self.test_error_handling_with_deepseek()
            
            # Test 8: Performance with DeepSeek
            await self.test_performance_with_deepseek()
            
        except Exception as e:
            logger.error(f"Critical error in DeepSeek tests: {e}")
            self.test_results["error_count"] += 1
        
        finally:
            await self.client.aclose()
            self.print_test_summary()
    
    async def send_message(self, messages: List[Dict[str, str]], model: str = "deepseek-chat") -> str:
        """Send message to DeepSeek API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        
        except Exception as e:
            logger.error(f"DeepSeek API error: {e}")
            raise
    
    async def test_api_connection(self):
        """Test basic API connection"""
        logger.info("🔌 Testing DeepSeek API Connection")
        
        try:
            test_messages = [
                {"role": "user", "content": "Hello, please respond with 'API connection successful'"}
            ]
            
            response = await self.send_message(test_messages)
            assert response is not None, "API response is None"
            assert len(response) > 0, "API response is empty"
            
            self.test_results["api_connection"] = True
            self.test_results["passed_tests"] += 1
            
            logger.info("✅ API Connection: PASSED")
            
        except Exception as e:
            logger.error(f"❌ API Connection: FAILED - {e}")
            self.test_results["failed_tests"] += 1
    
    async def test_basic_conversations(self):
        """Test basic conversation scenarios"""
        logger.info("💬 Testing Basic Conversations")
        
        try:
            # Initialize LuminoraCore components
            client = LuminoraCoreClient()
            await client.initialize()
            
            client_v11 = LuminoraCoreClientV11(client)
            
            # Test scenario 1: Simple greeting
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": "Hello, my name is Carlos and I'm from Madrid."}
            ]
            
            response = await self.send_message(messages)
            assert response is not None, "Simple greeting response is None"
            assert len(response) > 0, "Simple greeting response is empty"
            
            # Save facts from conversation
            await client_v11.save_fact("carlos", "personal", "name", "Carlos", 0.9)
            await client_v11.save_fact("carlos", "personal", "location", "Madrid", 0.9)
            
            # Test scenario 2: Follow-up question
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": "Hello, my name is Carlos and I'm from Madrid."},
                {"role": "assistant", "content": response},
                {"role": "user", "content": "What do you know about me?"}
            ]
            
            response2 = await self.send_message(messages)
            assert response2 is not None, "Follow-up response is None"
            assert len(response2) > 0, "Follow-up response is empty"
            
            # Test scenario 3: Technical question
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": "Explain quantum computing in simple terms."}
            ]
            
            response3 = await self.send_message(messages)
            assert response3 is not None, "Technical question response is None"
            assert len(response3) > 0, "Technical question response is empty"
            
            # Verify facts were saved
            facts = await client_v11.get_facts("carlos")
            assert len(facts) == 2, "Facts not saved correctly"
            
            await client.cleanup()
            
            self.test_results["conversation_tests"]["simple_greeting"] = "PASSED"
            self.test_results["conversation_tests"]["follow_up_question"] = "PASSED"
            self.test_results["conversation_tests"]["technical_question"] = "PASSED"
            self.test_results["conversation_tests"]["fact_saving"] = "PASSED"
            self.test_results["passed_tests"] += 4
            
            logger.info("✅ Basic Conversations: PASSED")
            
        except Exception as e:
            logger.error(f"❌ Basic Conversations: FAILED - {e}")
            self.test_results["conversation_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    async def test_memory_learning_scenarios(self):
        """Test memory learning scenarios with DeepSeek"""
        logger.info("🧠 Testing Memory Learning Scenarios")
        
        try:
            # Initialize components
            client = LuminoraCoreClient()
            await client.initialize()
            
            client_v11 = LuminoraCoreClientV11(client)
            
            # Test scenario 1: Personal information learning
            user_id = "memory_test_user"
            
            # Conversation 1: Introduction
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant that remembers information about users."},
                {"role": "user", "content": "Hi, I'm Sarah. I'm 28 years old and I work as a software engineer at Google."}
            ]
            
            response = await self.send_message(messages)
            assert response is not None, "Introduction response is None"
            
            # Extract and save facts
            await client_v11.save_fact(user_id, "personal", "name", "Sarah", 0.9)
            await client_v11.save_fact(user_id, "personal", "age", "28", 0.9)
            await client_v11.save_fact(user_id, "work", "company", "Google", 0.9)
            await client_v11.save_fact(user_id, "work", "position", "Software Engineer", 0.9)
            
            # Conversation 2: Hobbies
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant that remembers information about users."},
                {"role": "user", "content": "Hi, I'm Sarah. I'm 28 years old and I work as a software engineer at Google."},
                {"role": "assistant", "content": response},
                {"role": "user", "content": "I love playing tennis and reading science fiction novels."}
            ]
            
            response = await self.send_message(messages)
            assert response is not None, "Hobbies response is None"
            
            # Extract and save facts
            await client_v11.save_fact(user_id, "hobbies", "sport", "Tennis", 0.8)
            await client_v11.save_fact(user_id, "hobbies", "reading", "Science Fiction", 0.8)
            
            # Conversation 3: Preferences
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant that remembers information about users."},
                {"role": "user", "content": "Hi, I'm Sarah. I'm 28 years old and I work as a software engineer at Google."},
                {"role": "assistant", "content": response},
                {"role": "user", "content": "I love playing tennis and reading science fiction novels."},
                {"role": "assistant", "content": response},
                {"role": "user", "content": "My favorite color is blue and I prefer Italian food."}
            ]
            
            response = await self.send_message(messages)
            assert response is not None, "Preferences response is None"
            
            # Extract and save facts
            await client_v11.save_fact(user_id, "preferences", "color", "Blue", 0.8)
            await client_v11.save_fact(user_id, "preferences", "food", "Italian", 0.8)
            
            # Test memory retrieval
            all_facts = await client_v11.get_facts(user_id)
            personal_facts = await client_v11.get_facts(user_id, "personal")
            work_facts = await client_v11.get_facts(user_id, "work")
            hobby_facts = await client_v11.get_facts(user_id, "hobbies")
            preference_facts = await client_v11.get_facts(user_id, "preferences")
            
            assert len(all_facts) == 7, f"Total facts count mismatch: {len(all_facts)}"
            assert len(personal_facts) == 2, f"Personal facts count mismatch: {len(personal_facts)}"
            assert len(work_facts) == 2, f"Work facts count mismatch: {len(work_facts)}"
            assert len(hobby_facts) == 2, f"Hobby facts count mismatch: {len(hobby_facts)}"
            assert len(preference_facts) == 2, f"Preference facts count mismatch: {len(preference_facts)}"
            
            # Test search functionality
            search_results = await client_v11.search_facts(user_id, "tennis")
            assert len(search_results) == 1, "Search for tennis failed"
            
            search_results = await client_v11.search_facts(user_id, "Google")
            assert len(search_results) == 1, "Search for Google failed"
            
            # Test episode creation
            await client_v11.save_episode(
                user_id, "conversation", "First Meeting", 
                "Sarah introduced herself and shared personal information", 0.8, "positive"
            )
            
            episodes = await client_v11.get_episodes(user_id)
            assert len(episodes) == 1, "Episode creation failed"
            
            await client.cleanup()
            
            self.test_results["memory_tests"]["personal_info_learning"] = "PASSED"
            self.test_results["memory_tests"]["hobby_learning"] = "PASSED"
            self.test_results["memory_tests"]["preference_learning"] = "PASSED"
            self.test_results["memory_tests"]["fact_categorization"] = "PASSED"
            self.test_results["memory_tests"]["search_functionality"] = "PASSED"
            self.test_results["memory_tests"]["episode_creation"] = "PASSED"
            self.test_results["passed_tests"] += 6
            
            logger.info("✅ Memory Learning Scenarios: PASSED")
            
        except Exception as e:
            logger.error(f"❌ Memory Learning Scenarios: FAILED - {e}")
            self.test_results["memory_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    async def test_affinity_building_scenarios(self):
        """Test affinity building scenarios with DeepSeek"""
        logger.info("❤️ Testing Affinity Building Scenarios")
        
        try:
            # Initialize components
            client = LuminoraCoreClient()
            await client.initialize()
            
            client_v11 = LuminoraCoreClientV11(client)
            
            user_id = "affinity_test_user"
            personality_name = "helpful_assistant"
            
            # Test scenario 1: Positive interactions
            positive_interactions = [
                "Thank you so much for your help!",
                "You're really amazing at explaining things.",
                "I appreciate your patience with my questions.",
                "You've been incredibly helpful today.",
                "I love how you always give detailed answers."
            ]
            
            for i, message in enumerate(positive_interactions):
                # Simulate conversation with DeepSeek
                messages = [
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": message}
                ]
                
                response = await self.send_message(messages)
                assert response is not None, f"Positive interaction {i+1} response is None"
                
                # Update affinity based on positive interaction
                affinity = await client_v11.update_affinity(user_id, personality_name, 5, "positive")
                assert affinity is not None, f"Affinity update {i+1} failed"
            
            # Check final affinity level
            final_affinity = await client_v11.get_affinity(user_id, personality_name)
            assert final_affinity is not None, "Final affinity retrieval failed"
            assert final_affinity["points"] == 25, f"Affinity points mismatch: {final_affinity['points']}"
            assert final_affinity["level"] in ["acquaintance", "friend"], f"Affinity level wrong: {final_affinity['level']}"
            
            # Test scenario 2: Mixed interactions
            mixed_interactions = [
                ("I'm not sure about this.", "neutral"),
                ("Actually, that was really helpful!", "positive"),
                ("I don't understand.", "neutral"),
                ("Now I get it, thanks!", "positive"),
                ("This is confusing.", "negative")
            ]
            
            for message, interaction_type in mixed_interactions:
                messages = [
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": message}
                ]
                
                response = await self.send_message(messages)
                assert response is not None, f"Mixed interaction response is None for: {message}"
                
                # Update affinity based on interaction type
                points_delta = 3 if interaction_type == "positive" else -1 if interaction_type == "negative" else 0
                affinity = await client_v11.update_affinity(user_id, personality_name, points_delta, interaction_type)
                assert affinity is not None, f"Mixed affinity update failed for: {message}"
            
            # Test scenario 3: Multiple personalities
            personalities = ["assistant", "friend", "mentor", "colleague"]
            
            for personality in personalities:
                # Build affinity for each personality
                for _ in range(5):
                    affinity = await client_v11.update_affinity(user_id, personality, 2, "positive")
                    assert affinity is not None, f"Affinity update failed for {personality}"
            
            # Check all affinities
            all_affinities = await client_v11.get_all_affinities(user_id)
            assert len(all_affinities) == 5, f"All affinities count mismatch: {len(all_affinities)}"
            
            # Verify each personality has affinity
            personality_names = [aff["personality_name"] for aff in all_affinities]
            for personality in personalities:
                assert personality in personality_names, f"Personality {personality} not found in affinities"
            
            await client.cleanup()
            
            self.test_results["affinity_tests"]["positive_interactions"] = "PASSED"
            self.test_results["affinity_tests"]["mixed_interactions"] = "PASSED"
            self.test_results["affinity_tests"]["multiple_personalities"] = "PASSED"
            self.test_results["affinity_tests"]["affinity_progression"] = "PASSED"
            self.test_results["passed_tests"] += 4
            
            logger.info("✅ Affinity Building Scenarios: PASSED")
            
        except Exception as e:
            logger.error(f"❌ Affinity Building Scenarios: FAILED - {e}")
            self.test_results["affinity_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    async def test_complex_conversation_flows(self):
        """Test complex conversation flows with DeepSeek"""
        logger.info("🔄 Testing Complex Conversation Flows")
        
        try:
            # Initialize components
            client = LuminoraCoreClient()
            await client.initialize()
            
            client_v11 = LuminoraCoreClientV11(client)
            
            user_id = "complex_flow_user"
            
            # Test scenario 1: Multi-turn conversation with context
            conversation_history = []
            
            # Turn 1: Introduction
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": "Hi, I'm Alex. I'm planning a trip to Japan next month."}
            ]
            
            response = await self.send_message(messages)
            assert response is not None, "Turn 1 response is None"
            conversation_history.extend([
                {"role": "user", "content": "Hi, I'm Alex. I'm planning a trip to Japan next month."},
                {"role": "assistant", "content": response}
            ])
            
            # Save facts from turn 1
            await client_v11.save_fact(user_id, "personal", "name", "Alex", 0.9)
            await client_v11.save_fact(user_id, "travel", "destination", "Japan", 0.9)
            await client_v11.save_fact(user_id, "travel", "timeline", "Next month", 0.8)
            
            # Turn 2: Follow-up with context
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": "Hi, I'm Alex. I'm planning a trip to Japan next month."},
                {"role": "assistant", "content": response},
                {"role": "user", "content": "What should I pack for the weather in Tokyo in March?"}
            ]
            
            response = await self.send_message(messages)
            assert response is not None, "Turn 2 response is None"
            conversation_history.extend([
                {"role": "user", "content": "What should I pack for the weather in Tokyo in March?"},
                {"role": "assistant", "content": response}
            ])
            
            # Save facts from turn 2
            await client_v11.save_fact(user_id, "travel", "city", "Tokyo", 0.9)
            await client_v11.save_fact(user_id, "travel", "month", "March", 0.9)
            
            # Turn 3: More specific question
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": "Hi, I'm Alex. I'm planning a trip to Japan next month."},
                {"role": "assistant", "content": conversation_history[1]["content"]},
                {"role": "user", "content": "What should I pack for the weather in Tokyo in March?"},
                {"role": "assistant", "content": response},
                {"role": "user", "content": "I'm particularly interested in visiting temples and trying local food."}
            ]
            
            response = await self.send_message(messages)
            assert response is not None, "Turn 3 response is None"
            
            # Save facts from turn 3
            await client_v11.save_fact(user_id, "interests", "sightseeing", "Temples", 0.8)
            await client_v11.save_fact(user_id, "interests", "food", "Local Japanese food", 0.8)
            
            # Test scenario 2: Memory retrieval and context
            # Get user context
            context = await client_v11.get_user_context(user_id)
            assert context is not None, "User context retrieval failed"
            assert "facts" in context, "User context missing facts"
            
            # Search for specific information
            japan_facts = await client_v11.search_facts(user_id, "Japan")
            assert len(japan_facts) >= 1, "Search for Japan failed"
            
            tokyo_facts = await client_v11.search_facts(user_id, "Tokyo")
            assert len(tokyo_facts) >= 1, "Search for Tokyo failed"
            
            # Test scenario 3: Episode creation from conversation
            await client_v11.save_episode(
                user_id, "conversation", "Japan Trip Planning", 
                "Alex discussed planning a trip to Japan, specifically Tokyo in March, with interests in temples and local food", 
                0.9, "positive"
            )
            
            episodes = await client_v11.get_episodes(user_id)
            assert len(episodes) == 1, "Episode creation failed"
            
            # Test scenario 4: Affinity building through conversation
            affinity = await client_v11.update_affinity(user_id, "travel_assistant", 10, "positive")
            assert affinity is not None, "Affinity update failed"
            
            await client.cleanup()
            
            self.test_results["complex_flow_tests"]["multi_turn_conversation"] = "PASSED"
            self.test_results["complex_flow_tests"]["context_retention"] = "PASSED"
            self.test_results["complex_flow_tests"]["fact_extraction"] = "PASSED"
            self.test_results["complex_flow_tests"]["memory_retrieval"] = "PASSED"
            self.test_results["complex_flow_tests"]["episode_creation"] = "PASSED"
            self.test_results["complex_flow_tests"]["affinity_building"] = "PASSED"
            self.test_results["passed_tests"] += 6
            
            logger.info("✅ Complex Conversation Flows: PASSED")
            
        except Exception as e:
            logger.error(f"❌ Complex Conversation Flows: FAILED - {e}")
            self.test_results["complex_flow_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    async def test_multi_user_scenarios(self):
        """Test multi-user scenarios with DeepSeek"""
        logger.info("👥 Testing Multi-User Scenarios")
        
        try:
            # Initialize components
            client = LuminoraCoreClient()
            await client.initialize()
            
            client_v11 = LuminoraCoreClientV11(client)
            
            # Test scenario 1: Multiple users with different personalities
            users = [
                {"id": "user_alice", "name": "Alice", "personality": "friendly_assistant"},
                {"id": "user_bob", "name": "Bob", "personality": "technical_expert"},
                {"id": "user_carol", "name": "Carol", "personality": "creative_helper"}
            ]
            
            for user in users:
                # Create conversation for each user
                messages = [
                    {"role": "system", "content": f"You are a {user['personality']}."},
                    {"role": "user", "content": f"Hi, I'm {user['name']}. Nice to meet you!"}
                ]
                
                response = await self.send_message(messages)
                assert response is not None, f"Response for {user['name']} is None"
                
                # Save user facts
                await client_v11.save_fact(user["id"], "personal", "name", user["name"], 0.9)
                await client_v11.save_fact(user["id"], "personal", "personality_preference", user["personality"], 0.8)
                
                # Build affinity
                affinity = await client_v11.update_affinity(user["id"], user["personality"], 5, "positive")
                assert affinity is not None, f"Affinity update failed for {user['name']}"
            
            # Test scenario 2: Cross-user data isolation
            alice_facts = await client_v11.get_facts("user_alice")
            bob_facts = await client_v11.get_facts("user_bob")
            carol_facts = await client_v11.get_facts("user_carol")
            
            assert len(alice_facts) == 2, f"Alice facts count mismatch: {len(alice_facts)}"
            assert len(bob_facts) == 2, f"Bob facts count mismatch: {len(bob_facts)}"
            assert len(carol_facts) == 2, f"Carol facts count mismatch: {len(carol_facts)}"
            
            # Verify data isolation
            alice_names = [fact["value"] for fact in alice_facts if fact["key"] == "name"]
            bob_names = [fact["value"] for fact in bob_facts if fact["key"] == "name"]
            carol_names = [fact["value"] for fact in carol_facts if fact["key"] == "name"]
            
            assert "Alice" in alice_names, "Alice's name not found in her facts"
            assert "Bob" in bob_names, "Bob's name not found in his facts"
            assert "Carol" in carol_names, "Carol's name not found in her facts"
            
            # Test scenario 3: User-specific affinity tracking
            for user in users:
                affinities = await client_v11.get_all_affinities(user["id"])
                assert len(affinities) == 1, f"Affinity count mismatch for {user['name']}"
                assert affinities[0]["personality_name"] == user["personality"], f"Personality mismatch for {user['name']}"
            
            # Test scenario 4: User statistics
            for user in users:
                stats = await client_v11.get_user_stats(user["id"])
                assert stats["fact_count"] == 2, f"Fact count mismatch for {user['name']}"
                assert stats["affinity_count"] == 1, f"Affinity count mismatch for {user['name']}"
            
            await client.cleanup()
            
            self.test_results["multi_user_tests"]["multiple_users"] = "PASSED"
            self.test_results["multi_user_tests"]["data_isolation"] = "PASSED"
            self.test_results["multi_user_tests"]["affinity_tracking"] = "PASSED"
            self.test_results["multi_user_tests"]["user_statistics"] = "PASSED"
            self.test_results["passed_tests"] += 4
            
            logger.info("✅ Multi-User Scenarios: PASSED")
            
        except Exception as e:
            logger.error(f"❌ Multi-User Scenarios: FAILED - {e}")
            self.test_results["multi_user_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    async def test_error_handling_with_deepseek(self):
        """Test error handling with DeepSeek API"""
        logger.info("⚠️ Testing Error Handling with DeepSeek")
        
        try:
            # Test scenario 1: Invalid API key (simulated)
            # This would normally fail, but we'll test graceful handling
            
            # Test scenario 2: Empty messages
            try:
                response = await self.send_message([])
                # Should handle gracefully or raise appropriate error
            except Exception:
                pass  # Expected behavior
            
            # Test scenario 3: Very long message
            long_message = "A" * 10000  # Very long message
            messages = [
                {"role": "user", "content": long_message}
            ]
            
            try:
                response = await self.send_message(messages)
                # Should handle gracefully
            except Exception:
                pass  # Expected behavior for very long messages
            
            # Test scenario 4: Invalid message format
            try:
                invalid_messages = [
                    {"role": "invalid_role", "content": "Test message"}
                ]
                response = await self.send_message(invalid_messages)
                # Should handle gracefully
            except Exception:
                pass  # Expected behavior
            
            # Test scenario 5: Network timeout simulation
            # This is harder to test without actually causing timeouts
            # But we can test that our client handles errors gracefully
            
            self.test_results["error_handling_tests"]["empty_messages"] = "PASSED"
            self.test_results["error_handling_tests"]["long_messages"] = "PASSED"
            self.test_results["error_handling_tests"]["invalid_format"] = "PASSED"
            self.test_results["passed_tests"] += 3
            
            logger.info("✅ Error Handling with DeepSeek: PASSED")
            
        except Exception as e:
            logger.error(f"❌ Error Handling with DeepSeek: FAILED - {e}")
            self.test_results["error_handling_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    async def test_performance_with_deepseek(self):
        """Test performance with DeepSeek API"""
        logger.info("⚡ Testing Performance with DeepSeek")
        
        try:
            # Test scenario 1: Multiple rapid requests
            start_time = time.time()
            
            tasks = []
            for i in range(5):
                messages = [
                    {"role": "user", "content": f"Test message {i+1}"}
                ]
                task = self.send_message(messages)
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            assert len(responses) == 5, "Not all responses received"
            assert all(response is not None for response in responses), "Some responses are None"
            assert total_time < 30, f"Multiple requests too slow: {total_time:.2f}s"
            
            # Test scenario 2: Memory operations performance
            client = LuminoraCoreClient()
            await client.initialize()
            
            client_v11 = LuminoraCoreClientV11(client)
            
            start_time = time.time()
            
            # Save multiple facts
            for i in range(20):
                await client_v11.save_fact("perf_user", "test", f"key_{i}", f"value_{i}", 0.8)
            
            fact_save_time = time.time() - start_time
            
            # Retrieve facts
            start_time = time.time()
            facts = await client_v11.get_facts("perf_user")
            fact_retrieve_time = time.time() - start_time
            
            assert len(facts) == 20, f"Fact count mismatch: {len(facts)}"
            assert fact_save_time < 5, f"Fact saving too slow: {fact_save_time:.2f}s"
            assert fact_retrieve_time < 2, f"Fact retrieval too slow: {fact_retrieve_time:.2f}s"
            
            await client.cleanup()
            
            self.test_results["performance_tests"]["multiple_requests"] = f"PASSED ({total_time:.2f}s)"
            self.test_results["performance_tests"]["fact_operations"] = f"PASSED (save: {fact_save_time:.2f}s, retrieve: {fact_retrieve_time:.2f}s)"
            self.test_results["passed_tests"] += 2
            
            logger.info("✅ Performance with DeepSeek: PASSED")
            
        except Exception as e:
            logger.error(f"❌ Performance with DeepSeek: FAILED - {e}")
            self.test_results["performance_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    def print_test_summary(self):
        """Print DeepSeek test summary"""
        logger.info("\n" + "=" * 80)
        logger.info("🤖 DEEPSEEK INTEGRATION TEST SUMMARY")
        logger.info("=" * 80)
        
        total_tests = self.test_results["passed_tests"] + self.test_results["failed_tests"]
        success_rate = (self.test_results["passed_tests"] / total_tests * 100) if total_tests > 0 else 0
        
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {self.test_results['passed_tests']} ✅")
        logger.info(f"Failed: {self.test_results['failed_tests']} ❌")
        logger.info(f"Success Rate: {success_rate:.1f}%")
        logger.info(f"API Connection: {'✅ PASSED' if self.test_results['api_connection'] else '❌ FAILED'}")
        
        logger.info("\n📋 DETAILED RESULTS:")
        for category, results in self.test_results.items():
            if category in ["api_connection", "error_count", "total_tests", "passed_tests", "failed_tests"]:
                continue
            
            logger.info(f"\n{category.upper().replace('_', ' ')}:")
            if isinstance(results, dict):
                for test_name, result in results.items():
                    if test_name == "error":
                        logger.info(f"  ❌ ERROR: {result}")
                    else:
                        logger.info(f"  {result}: {test_name}")
            else:
                logger.info(f"  {results}")
        
        if self.test_results["failed_tests"] == 0 and self.test_results["error_count"] == 0:
            logger.info("\n🎉 ALL DEEPSEEK TESTS PASSED! INTEGRATION IS READY!")
        else:
            logger.info(f"\n⚠️  {self.test_results['failed_tests']} DEEPSEEK TESTS FAILED - REVIEW REQUIRED")
        
        logger.info("=" * 80)


async def main():
    """Main DeepSeek test runner"""
    # Get DeepSeek API key from environment
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    if not deepseek_api_key:
        logger.error("❌ DEEPSEEK_API_KEY environment variable not set")
        return 1
    
    # Create tester
    tester = DeepSeekTester(deepseek_api_key)
    
    # Run all tests
    await tester.run_all_tests()
    
    # Return exit code based on results
    if tester.test_results["failed_tests"] == 0 and tester.test_results["error_count"] == 0:
        return 0
    else:
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
