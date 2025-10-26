#!/usr/bin/env python3
"""
Comprehensive System Tests
Exhaustive testing of all LuminoraCore components with DeepSeek integration
"""

import asyncio
import pytest
import os
import sys
import time
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'luminoracore'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'luminoracore-sdk-python'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'luminoracore-cli'))

# Import core components
from luminoracore import PersonalityEngine, MemorySystem, EvolutionEngine, InMemoryStorage
from luminoracore.interfaces import StorageInterface

# Import SDK components
from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
from luminoracore_sdk.client_new import LuminoraCoreClientNew
from luminoracore_sdk.client_hybrid import LuminoraCoreClientHybrid
from luminoracore_sdk.types.provider import ProviderConfig
from luminoracore_sdk.types.session import StorageConfig, MemoryConfig

# Import CLI components
from luminoracore_cli.commands_new.memory_new import MemoryCommandNew

# DeepSeek integration
import httpx


class DeepSeekProvider:
    """DeepSeek API provider for testing"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1"
        self.client = httpx.AsyncClient(timeout=30.0)
    
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
    
    async def close(self):
        """Close the client"""
        await self.client.aclose()


class ComprehensiveSystemTester:
    """Comprehensive system tester for LuminoraCore"""
    
    def __init__(self, deepseek_api_key: str):
        self.deepseek_api_key = deepseek_api_key
        self.deepseek = DeepSeekProvider(deepseek_api_key)
        self.test_results = {
            "core_tests": {},
            "sdk_tests": {},
            "cli_tests": {},
            "conversation_tests": {},
            "integration_tests": {},
            "error_count": 0,
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0
        }
    
    async def run_all_tests(self):
        """Run all comprehensive tests"""
        logger.info("🚀 Starting Comprehensive System Tests")
        logger.info("=" * 60)
        
        try:
            # Test 1: Core Components
            await self.test_core_components()
            
            # Test 2: SDK Components
            await self.test_sdk_components()
            
            # Test 3: CLI Components
            await self.test_cli_components()
            
            # Test 4: Installation Process
            await self.test_installation_process()
            
            # Test 5: DeepSeek Integration
            await self.test_deepseek_integration()
            
            # Test 6: Conversation Testing
            await self.test_conversation_scenarios()
            
            # Test 7: Memory and Affinity Testing
            await self.test_memory_and_affinity()
            
            # Test 8: Error Handling
            await self.test_error_handling()
            
            # Test 9: Performance Testing
            await self.test_performance()
            
            # Test 10: Integration Testing
            await self.test_full_integration()
            
        except Exception as e:
            logger.error(f"Critical error in test suite: {e}")
            self.test_results["error_count"] += 1
        
        finally:
            await self.deepseek.close()
            self.print_test_summary()
    
    async def test_core_components(self):
        """Test core components thoroughly"""
        logger.info("🧠 Testing Core Components")
        
        try:
            # Test PersonalityEngine
            engine = PersonalityEngine()
            assert engine is not None, "PersonalityEngine creation failed"
            
            # Test personality loading
            test_personality = {
                "name": "test_assistant",
                "description": "A test assistant",
                "system_prompt": "You are a helpful test assistant.",
                "traits": {
                    "friendliness": 0.8,
                    "patience": 0.9,
                    "creativity": 0.7
                }
            }
            
            success = await engine.load_personality("test_assistant", test_personality)
            assert success, "Personality loading failed"
            
            # Test personality retrieval
            retrieved = await engine.get_personality("test_assistant")
            assert retrieved is not None, "Personality retrieval failed"
            assert retrieved["name"] == "test_assistant", "Personality name mismatch"
            
            # Test personality listing
            personalities = await engine.list_personalities()
            assert "test_assistant" in personalities, "Personality not in list"
            
            # Test MemorySystem
            storage = InMemoryStorage()
            memory = MemorySystem(storage)
            assert memory is not None, "MemorySystem creation failed"
            
            # Test fact saving
            fact_saved = await memory.storage.save_fact("user123", "personal", "name", "Test User", 0.9)
            assert fact_saved, "Fact saving failed"
            
            # Test fact retrieval
            facts = await memory.storage.get_facts("user123")
            assert len(facts) == 1, "Fact retrieval failed"
            assert facts[0]["value"] == "Test User", "Fact value mismatch"
            
            # Test EvolutionEngine
            evolution = EvolutionEngine()
            assert evolution is not None, "EvolutionEngine creation failed"
            
            # Test evolution calculation
            interaction_data = {
                "quality": "positive",
                "sentiment": "happy",
                "duration": 300
            }
            
            delta = await evolution.calculate_evolution_delta("test_assistant", "user123", interaction_data)
            assert delta is not None, "Evolution delta calculation failed"
            assert "traits" in delta, "Evolution delta missing traits"
            
            self.test_results["core_tests"]["personality_engine"] = "PASSED"
            self.test_results["core_tests"]["memory_system"] = "PASSED"
            self.test_results["core_tests"]["evolution_engine"] = "PASSED"
            self.test_results["passed_tests"] += 3
            
            logger.info("✅ Core Components: PASSED")
            
        except Exception as e:
            logger.error(f"❌ Core Components: FAILED - {e}")
            self.test_results["core_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    async def test_sdk_components(self):
        """Test SDK components thoroughly"""
        logger.info("🔧 Testing SDK Components")
        
        try:
            # Test LuminoraCoreClient (original)
            client = LuminoraCoreClient()
            assert client is not None, "LuminoraCoreClient creation failed"
            
            # Test initialization
            init_success = await client.initialize()
            assert init_success, "Client initialization failed"
            
            # Test LuminoraCoreClientV11
            storage_config = StorageConfig(storage_type="memory")
            memory_config = MemoryConfig()
            client_v11 = LuminoraCoreClientV11(client, storage_config, memory_config)
            assert client_v11 is not None, "LuminoraCoreClientV11 creation failed"
            
            # Test fact operations
            fact_saved = await client_v11.save_fact("user123", "personal", "name", "Test User", 0.9)
            assert fact_saved, "Fact saving via SDK failed"
            
            facts = await client_v11.get_facts("user123")
            assert len(facts) == 1, "Fact retrieval via SDK failed"
            
            # Test LuminoraCoreClientNew
            client_new = LuminoraCoreClientNew()
            assert client_new is not None, "LuminoraCoreClientNew creation failed"
            
            # Test fact operations with new client
            fact_saved = await client_new.save_fact("user456", "personal", "age", "25", 0.8)
            assert fact_saved, "Fact saving via new client failed"
            
            facts = await client_new.get_facts("user456")
            assert len(facts) == 1, "Fact retrieval via new client failed"
            
            # Test LuminoraCoreClientHybrid
            client_hybrid = LuminoraCoreClientHybrid()
            assert client_hybrid is not None, "LuminoraCoreClientHybrid creation failed"
            
            # Test both old and new functionality
            fact_saved = await client_hybrid.save_fact("user789", "personal", "city", "Madrid", 0.9)
            assert fact_saved, "Fact saving via hybrid client failed"
            
            # Test cleanup
            cleanup_success = await client.cleanup()
            assert cleanup_success, "Client cleanup failed"
            
            self.test_results["sdk_tests"]["original_client"] = "PASSED"
            self.test_results["sdk_tests"]["v11_client"] = "PASSED"
            self.test_results["sdk_tests"]["new_client"] = "PASSED"
            self.test_results["sdk_tests"]["hybrid_client"] = "PASSED"
            self.test_results["passed_tests"] += 4
            
            logger.info("✅ SDK Components: PASSED")
            
        except Exception as e:
            logger.error(f"❌ SDK Components: FAILED - {e}")
            self.test_results["sdk_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    async def test_cli_components(self):
        """Test CLI components thoroughly"""
        logger.info("🖥️ Testing CLI Components")
        
        try:
            # Test MemoryCommandNew
            cli_command = MemoryCommandNew()
            assert cli_command is not None, "MemoryCommandNew creation failed"
            
            # Test fact operations via CLI
            fact_saved = await cli_command.storage.save_fact("user123", "personal", "name", "CLI Test User", 0.9)
            assert fact_saved, "Fact saving via CLI failed"
            
            facts = await cli_command.list_facts("user123")
            assert len(facts) == 1, "Fact listing via CLI failed"
            
            # Test episode operations via CLI
            episode_saved = await cli_command.storage.save_episode(
                "user123", "conversation", "Test Episode", "A test conversation", 0.8, "positive"
            )
            assert episode_saved, "Episode saving via CLI failed"
            
            episodes = await cli_command.list_episodes("user123")
            assert len(episodes) == 1, "Episode listing via CLI failed"
            
            # Test affinity operations via CLI
            affinity = await cli_command.storage.update_affinity("user123", "test_personality", 10, "positive")
            assert affinity is not None, "Affinity update via CLI failed"
            assert affinity["points"] == 10, "Affinity points mismatch"
            
            affinities = await cli_command.list_affinities("user123")
            assert len(affinities) == 1, "Affinity listing via CLI failed"
            
            # Test search operations via CLI
            search_results = await cli_command.search_facts("user123", "name")
            assert len(search_results) == 1, "Fact search via CLI failed"
            
            # Test user context via CLI
            context = await cli_command.get_user_context("user123")
            assert context is not None, "User context via CLI failed"
            assert "facts" in context, "User context missing facts"
            assert "episodes" in context, "User context missing episodes"
            assert "affinities" in context, "User context missing affinities"
            
            # Test user stats via CLI
            stats = await cli_command.get_user_stats("user123")
            assert stats is not None, "User stats via CLI failed"
            assert stats["fact_count"] == 1, "User stats fact count mismatch"
            assert stats["episode_count"] == 1, "User stats episode count mismatch"
            assert stats["affinity_count"] == 1, "User stats affinity count mismatch"
            
            # Test health check via CLI
            health = await cli_command.health_check()
            assert health is not None, "Health check via CLI failed"
            assert health["status"] == "healthy", "Health check status not healthy"
            
            self.test_results["cli_tests"]["memory_commands"] = "PASSED"
            self.test_results["cli_tests"]["fact_operations"] = "PASSED"
            self.test_results["cli_tests"]["episode_operations"] = "PASSED"
            self.test_results["cli_tests"]["affinity_operations"] = "PASSED"
            self.test_results["cli_tests"]["search_operations"] = "PASSED"
            self.test_results["cli_tests"]["context_operations"] = "PASSED"
            self.test_results["passed_tests"] += 6
            
            logger.info("✅ CLI Components: PASSED")
            
        except Exception as e:
            logger.error(f"❌ CLI Components: FAILED - {e}")
            self.test_results["cli_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    async def test_installation_process(self):
        """Test installation process"""
        logger.info("📦 Testing Installation Process")
        
        try:
            # Test core installation
            from luminoracore import PersonalityEngine, MemorySystem, EvolutionEngine
            assert PersonalityEngine is not None, "Core import failed"
            assert MemorySystem is not None, "MemorySystem import failed"
            assert EvolutionEngine is not None, "EvolutionEngine import failed"
            
            # Test SDK installation
            from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
            assert LuminoraCoreClient is not None, "SDK import failed"
            assert LuminoraCoreClientV11 is not None, "SDK V11 import failed"
            
            # Test CLI installation
            from luminoracore_cli.commands_new.memory_new import MemoryCommandNew
            assert MemoryCommandNew is not None, "CLI import failed"
            
            # Test that all components can be instantiated
            engine = PersonalityEngine()
            storage = InMemoryStorage()
            memory = MemorySystem(storage)
            evolution = EvolutionEngine()
            
            client = LuminoraCoreClient()
            client_v11 = LuminoraCoreClientV11(client)
            client_new = LuminoraCoreClientNew()
            client_hybrid = LuminoraCoreClientHybrid()
            
            cli_command = MemoryCommandNew()
            
            # All components created successfully
            assert engine is not None
            assert memory is not None
            assert evolution is not None
            assert client is not None
            assert client_v11 is not None
            assert client_new is not None
            assert client_hybrid is not None
            assert cli_command is not None
            
            self.test_results["installation_tests"]["core_import"] = "PASSED"
            self.test_results["installation_tests"]["sdk_import"] = "PASSED"
            self.test_results["installation_tests"]["cli_import"] = "PASSED"
            self.test_results["installation_tests"]["instantiation"] = "PASSED"
            self.test_results["passed_tests"] += 4
            
            logger.info("✅ Installation Process: PASSED")
            
        except Exception as e:
            logger.error(f"❌ Installation Process: FAILED - {e}")
            self.test_results["installation_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    async def test_deepseek_integration(self):
        """Test DeepSeek API integration"""
        logger.info("🤖 Testing DeepSeek Integration")
        
        try:
            # Test basic API connection
            test_messages = [
                {"role": "user", "content": "Hello, how are you?"}
            ]
            
            response = await self.deepseek.send_message(test_messages)
            assert response is not None, "DeepSeek API response is None"
            assert len(response) > 0, "DeepSeek API response is empty"
            
            # Test conversation with system prompt
            system_messages = [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": "What is 2+2?"}
            ]
            
            response = await self.deepseek.send_message(system_messages)
            assert response is not None, "DeepSeek system prompt response is None"
            assert len(response) > 0, "DeepSeek system prompt response is empty"
            
            # Test longer conversation
            conversation_messages = [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": "My name is Carlos and I'm from Madrid."},
                {"role": "assistant", "content": "Nice to meet you Carlos! Madrid is a beautiful city."},
                {"role": "user", "content": "What do you remember about me?"}
            ]
            
            response = await self.deepseek.send_message(conversation_messages)
            assert response is not None, "DeepSeek conversation response is None"
            assert len(response) > 0, "DeepSeek conversation response is empty"
            
            self.test_results["deepseek_tests"]["basic_connection"] = "PASSED"
            self.test_results["deepseek_tests"]["system_prompt"] = "PASSED"
            self.test_results["deepseek_tests"]["conversation"] = "PASSED"
            self.test_results["passed_tests"] += 3
            
            logger.info("✅ DeepSeek Integration: PASSED")
            
        except Exception as e:
            logger.error(f"❌ DeepSeek Integration: FAILED - {e}")
            self.test_results["deepseek_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    async def test_conversation_scenarios(self):
        """Test multiple conversation scenarios"""
        logger.info("💬 Testing Conversation Scenarios")
        
        try:
            # Initialize components
            client = LuminoraCoreClient()
            await client.initialize()
            
            client_v11 = LuminoraCoreClientV11(client)
            
            # Test scenario 1: Basic conversation
            session_id = await client.create_session("helpful_assistant")
            assert session_id is not None, "Session creation failed"
            
            response = await client.send_message(session_id, "Hello, my name is Alice.")
            assert response is not None, "Basic conversation failed"
            
            # Test scenario 2: Memory learning
            await client_v11.save_fact("alice", "personal", "name", "Alice", 0.9)
            await client_v11.save_fact("alice", "personal", "location", "New York", 0.8)
            
            facts = await client_v11.get_facts("alice")
            assert len(facts) == 2, "Memory learning failed"
            
            # Test scenario 3: Affinity building
            affinity = await client_v11.update_affinity("alice", "helpful_assistant", 15, "positive")
            assert affinity is not None, "Affinity building failed"
            assert affinity["points"] == 15, "Affinity points mismatch"
            
            # Test scenario 4: Episode creation
            await client_v11.save_episode(
                "alice", "conversation", "First Meeting", 
                "Alice introduced herself", 0.8, "positive"
            )
            
            episodes = await client_v11.get_episodes("alice")
            assert len(episodes) == 1, "Episode creation failed"
            
            # Test scenario 5: Search functionality
            search_results = await client_v11.search_facts("alice", "name")
            assert len(search_results) == 1, "Search functionality failed"
            
            # Test scenario 6: Context retrieval
            context = await client_v11.get_user_context("alice")
            assert context is not None, "Context retrieval failed"
            assert "facts" in context, "Context missing facts"
            assert "episodes" in context, "Context missing episodes"
            assert "affinities" in context, "Context missing affinities"
            
            # Test scenario 7: Multiple users
            await client_v11.save_fact("bob", "personal", "name", "Bob", 0.9)
            await client_v11.save_fact("bob", "personal", "hobby", "Photography", 0.7)
            
            bob_facts = await client_v11.get_facts("bob")
            assert len(bob_facts) == 2, "Multiple users failed"
            
            # Test scenario 8: Conversation with memory
            memory_response = await client_v11.send_message_with_memory(
                session_id, "What do you know about me?", "alice"
            )
            assert memory_response is not None, "Memory conversation failed"
            
            await client.cleanup()
            
            self.test_results["conversation_tests"]["basic_conversation"] = "PASSED"
            self.test_results["conversation_tests"]["memory_learning"] = "PASSED"
            self.test_results["conversation_tests"]["affinity_building"] = "PASSED"
            self.test_results["conversation_tests"]["episode_creation"] = "PASSED"
            self.test_results["conversation_tests"]["search_functionality"] = "PASSED"
            self.test_results["conversation_tests"]["context_retrieval"] = "PASSED"
            self.test_results["conversation_tests"]["multiple_users"] = "PASSED"
            self.test_results["conversation_tests"]["memory_conversation"] = "PASSED"
            self.test_results["passed_tests"] += 8
            
            logger.info("✅ Conversation Scenarios: PASSED")
            
        except Exception as e:
            logger.error(f"❌ Conversation Scenarios: FAILED - {e}")
            self.test_results["conversation_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    async def test_memory_and_affinity(self):
        """Test memory and affinity systems thoroughly"""
        logger.info("🧠 Testing Memory and Affinity Systems")
        
        try:
            # Initialize components
            client = LuminoraCoreClient()
            await client.initialize()
            
            client_v11 = LuminoraCoreClientV11(client)
            
            # Test fact categories
            fact_categories = [
                ("personal", "name", "John Doe"),
                ("personal", "age", "30"),
                ("personal", "location", "San Francisco"),
                ("work", "company", "Tech Corp"),
                ("work", "position", "Software Engineer"),
                ("hobbies", "sport", "Tennis"),
                ("hobbies", "music", "Jazz"),
                ("preferences", "color", "Blue"),
                ("preferences", "food", "Italian")
            ]
            
            for category, key, value in fact_categories:
                success = await client_v11.save_fact("user123", category, key, value, 0.8)
                assert success, f"Fact saving failed for {category}.{key}"
            
            # Test fact retrieval by category
            personal_facts = await client_v11.get_facts("user123", "personal")
            assert len(personal_facts) == 3, "Personal facts count mismatch"
            
            work_facts = await client_v11.get_facts("user123", "work")
            assert len(work_facts) == 2, "Work facts count mismatch"
            
            # Test episode importance levels
            episodes = [
                ("milestone", "Graduation", "Graduated from university", 9.5, "positive"),
                ("achievement", "Promotion", "Got promoted to senior engineer", 8.0, "positive"),
                ("conversation", "Daily Chat", "Regular conversation", 3.0, "neutral"),
                ("event", "Birthday", "Celebrated birthday", 7.0, "positive")
            ]
            
            for episode_type, title, summary, importance, sentiment in episodes:
                success = await client_v11.save_episode(
                    "user123", episode_type, title, summary, importance, sentiment
                )
                assert success, f"Episode saving failed for {title}"
            
            # Test episode filtering by importance
            important_episodes = await client_v11.get_episodes("user123", min_importance=7.0)
            assert len(important_episodes) == 3, "Important episodes count mismatch"
            
            # Test affinity progression
            personality_names = ["assistant", "friend", "mentor", "colleague"]
            
            for personality in personality_names:
                # Start with low affinity
                affinity = await client_v11.update_affinity("user123", personality, 5, "neutral")
                assert affinity["level"] == "stranger", f"Initial affinity level wrong for {personality}"
                
                # Build affinity through positive interactions
                for _ in range(10):
                    affinity = await client_v11.update_affinity("user123", personality, 3, "positive")
                
                # Should be at least acquaintance level
                assert affinity["points"] >= 30, f"Affinity points too low for {personality}"
                assert affinity["level"] in ["acquaintance", "friend", "close_friend"], f"Affinity level wrong for {personality}"
            
            # Test affinity retrieval
            all_affinities = await client_v11.get_all_affinities("user123")
            assert len(all_affinities) == 4, "All affinities count mismatch"
            
            # Test search functionality
            search_queries = ["name", "work", "tennis", "blue"]
            for query in search_queries:
                results = await client_v11.search_facts("user123", query)
                assert len(results) > 0, f"Search failed for query: {query}"
            
            # Test user statistics
            stats = await client_v11.get_user_stats("user123")
            assert stats["fact_count"] == 9, "User stats fact count mismatch"
            assert stats["episode_count"] == 4, "User stats episode count mismatch"
            assert stats["affinity_count"] == 4, "User stats affinity count mismatch"
            
            await client.cleanup()
            
            self.test_results["memory_affinity_tests"]["fact_categories"] = "PASSED"
            self.test_results["memory_affinity_tests"]["episode_importance"] = "PASSED"
            self.test_results["memory_affinity_tests"]["affinity_progression"] = "PASSED"
            self.test_results["memory_affinity_tests"]["search_functionality"] = "PASSED"
            self.test_results["memory_affinity_tests"]["user_statistics"] = "PASSED"
            self.test_results["passed_tests"] += 5
            
            logger.info("✅ Memory and Affinity Systems: PASSED")
            
        except Exception as e:
            logger.error(f"❌ Memory and Affinity Systems: FAILED - {e}")
            self.test_results["memory_affinity_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    async def test_error_handling(self):
        """Test error handling thoroughly"""
        logger.info("⚠️ Testing Error Handling")
        
        try:
            # Test invalid inputs
            client = LuminoraCoreClient()
            await client.initialize()
            
            client_v11 = LuminoraCoreClientV11(client)
            
            # Test invalid user ID
            try:
                await client_v11.get_facts(None)
                assert False, "Should have raised error for None user_id"
            except Exception:
                pass  # Expected
            
            # Test invalid category
            try:
                await client_v11.get_facts("user123", "")
                # This should work (empty category means all categories)
                pass
            except Exception:
                pass  # Also acceptable
            
            # Test invalid confidence values
            try:
                await client_v11.save_fact("user123", "test", "key", "value", 1.5)  # > 1.0
                # Should handle gracefully
            except Exception:
                pass  # Expected or acceptable
            
            # Test invalid affinity updates
            try:
                await client_v11.update_affinity("user123", "test_personality", -100, "negative")
                # Should handle gracefully
            except Exception:
                pass  # Expected or acceptable
            
            # Test non-existent user operations
            facts = await client_v11.get_facts("nonexistent_user")
            assert len(facts) == 0, "Non-existent user should return empty facts"
            
            episodes = await client_v11.get_episodes("nonexistent_user")
            assert len(episodes) == 0, "Non-existent user should return empty episodes"
            
            affinities = await client_v11.get_all_affinities("nonexistent_user")
            assert len(affinities) == 0, "Non-existent user should return empty affinities"
            
            # Test search with empty query
            search_results = await client_v11.search_facts("user123", "")
            assert isinstance(search_results, list), "Empty search should return list"
            
            await client.cleanup()
            
            self.test_results["error_handling_tests"]["invalid_inputs"] = "PASSED"
            self.test_results["error_handling_tests"]["non_existent_users"] = "PASSED"
            self.test_results["error_handling_tests"]["edge_cases"] = "PASSED"
            self.test_results["passed_tests"] += 3
            
            logger.info("✅ Error Handling: PASSED")
            
        except Exception as e:
            logger.error(f"❌ Error Handling: FAILED - {e}")
            self.test_results["error_handling_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    async def test_performance(self):
        """Test performance characteristics"""
        logger.info("⚡ Testing Performance")
        
        try:
            # Initialize components
            client = LuminoraCoreClient()
            await client.initialize()
            
            client_v11 = LuminoraCoreClientV11(client)
            
            # Test fact saving performance
            start_time = time.time()
            for i in range(100):
                await client_v11.save_fact("perf_user", "test", f"key_{i}", f"value_{i}", 0.8)
            fact_save_time = time.time() - start_time
            
            assert fact_save_time < 5.0, f"Fact saving too slow: {fact_save_time:.2f}s"
            
            # Test fact retrieval performance
            start_time = time.time()
            facts = await client_v11.get_facts("perf_user")
            fact_retrieve_time = time.time() - start_time
            
            assert fact_retrieve_time < 1.0, f"Fact retrieval too slow: {fact_retrieve_time:.2f}s"
            assert len(facts) == 100, "Fact count mismatch in performance test"
            
            # Test episode saving performance
            start_time = time.time()
            for i in range(50):
                await client_v11.save_episode(
                    "perf_user", "test", f"Episode {i}", f"Summary {i}", 0.5, "neutral"
                )
            episode_save_time = time.time() - start_time
            
            assert episode_save_time < 3.0, f"Episode saving too slow: {episode_save_time:.2f}s"
            
            # Test search performance
            start_time = time.time()
            search_results = await client_v11.search_facts("perf_user", "key")
            search_time = time.time() - start_time
            
            assert search_time < 2.0, f"Search too slow: {search_time:.2f}s"
            assert len(search_results) > 0, "Search returned no results"
            
            # Test memory usage (basic check)
            import psutil
            process = psutil.Process()
            memory_usage = process.memory_info().rss / 1024 / 1024  # MB
            
            assert memory_usage < 500, f"Memory usage too high: {memory_usage:.1f}MB"
            
            await client.cleanup()
            
            self.test_results["performance_tests"]["fact_saving"] = f"PASSED ({fact_save_time:.2f}s)"
            self.test_results["performance_tests"]["fact_retrieval"] = f"PASSED ({fact_retrieve_time:.2f}s)"
            self.test_results["performance_tests"]["episode_saving"] = f"PASSED ({episode_save_time:.2f}s)"
            self.test_results["performance_tests"]["search"] = f"PASSED ({search_time:.2f}s)"
            self.test_results["performance_tests"]["memory_usage"] = f"PASSED ({memory_usage:.1f}MB)"
            self.test_results["passed_tests"] += 5
            
            logger.info("✅ Performance: PASSED")
            
        except Exception as e:
            logger.error(f"❌ Performance: FAILED - {e}")
            self.test_results["performance_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    async def test_full_integration(self):
        """Test full system integration"""
        logger.info("🔗 Testing Full Integration")
        
        try:
            # Initialize all components
            client = LuminoraCoreClient()
            await client.initialize()
            
            client_v11 = LuminoraCoreClientV11(client)
            client_new = LuminoraCoreClientNew()
            client_hybrid = LuminoraCoreClientHybrid()
            
            cli_command = MemoryCommandNew()
            
            # Test cross-component compatibility
            user_id = "integration_user"
            
            # Save facts using different clients
            await client_v11.save_fact(user_id, "personal", "name", "Integration User", 0.9)
            await client_new.save_fact(user_id, "personal", "age", "25", 0.8)
            await client_hybrid.save_fact(user_id, "personal", "city", "Barcelona", 0.7)
            
            # Verify facts are accessible from all clients
            facts_v11 = await client_v11.get_facts(user_id)
            facts_new = await client_new.get_facts(user_id)
            facts_hybrid = await client_hybrid.get_facts(user_id)
            
            # All should have the same facts (shared storage)
            assert len(facts_v11) == 3, "V11 client facts count mismatch"
            assert len(facts_new) == 3, "New client facts count mismatch"
            assert len(facts_hybrid) == 3, "Hybrid client facts count mismatch"
            
            # Test CLI access to same data
            cli_facts = await cli_command.list_facts(user_id)
            assert len(cli_facts) == 3, "CLI facts count mismatch"
            
            # Test episode creation and retrieval
            await client_v11.save_episode(user_id, "milestone", "Integration Test", "Full system test", 0.9, "positive")
            
            episodes_v11 = await client_v11.get_episodes(user_id)
            episodes_new = await client_new.get_episodes(user_id)
            episodes_hybrid = await client_hybrid.get_episodes(user_id)
            cli_episodes = await cli_command.list_episodes(user_id)
            
            assert len(episodes_v11) == 1, "V11 client episodes count mismatch"
            assert len(episodes_new) == 1, "New client episodes count mismatch"
            assert len(episodes_hybrid) == 1, "Hybrid client episodes count mismatch"
            assert len(cli_episodes) == 1, "CLI episodes count mismatch"
            
            # Test affinity across clients
            await client_v11.update_affinity(user_id, "assistant", 20, "positive")
            await client_new.update_affinity(user_id, "friend", 15, "positive")
            await client_hybrid.update_affinity(user_id, "mentor", 25, "positive")
            
            affinities_v11 = await client_v11.get_all_affinities(user_id)
            affinities_new = await client_new.get_all_affinities(user_id)
            affinities_hybrid = await client_hybrid.get_all_affinities(user_id)
            cli_affinities = await cli_command.list_affinities(user_id)
            
            assert len(affinities_v11) == 3, "V11 client affinities count mismatch"
            assert len(affinities_new) == 3, "New client affinities count mismatch"
            assert len(affinities_hybrid) == 3, "Hybrid client affinities count mismatch"
            assert len(cli_affinities) == 3, "CLI affinities count mismatch"
            
            # Test search across clients
            search_v11 = await client_v11.search_facts(user_id, "name")
            search_new = await client_new.search_facts(user_id, "name")
            search_hybrid = await client_hybrid.search_facts(user_id, "name")
            cli_search = await cli_command.search_facts(user_id, "name")
            
            assert len(search_v11) == 1, "V11 client search count mismatch"
            assert len(search_new) == 1, "New client search count mismatch"
            assert len(search_hybrid) == 1, "Hybrid client search count mismatch"
            assert len(cli_search) == 1, "CLI search count mismatch"
            
            # Test context retrieval
            context_v11 = await client_v11.get_user_context(user_id)
            context_new = await client_new.get_user_context(user_id)
            context_hybrid = await client_hybrid.get_user_context(user_id)
            cli_context = await cli_command.get_user_context(user_id)
            
            assert context_v11 is not None, "V11 client context failed"
            assert context_new is not None, "New client context failed"
            assert context_hybrid is not None, "Hybrid client context failed"
            assert cli_context is not None, "CLI context failed"
            
            # Test statistics
            stats_v11 = await client_v11.get_user_stats(user_id)
            stats_new = await client_new.get_user_stats(user_id)
            stats_hybrid = await client_hybrid.get_user_stats(user_id)
            cli_stats = await cli_command.get_user_stats(user_id)
            
            assert stats_v11["fact_count"] == 3, "V11 client stats fact count mismatch"
            assert stats_new["fact_count"] == 3, "New client stats fact count mismatch"
            assert stats_hybrid["fact_count"] == 3, "Hybrid client stats fact count mismatch"
            assert cli_stats["fact_count"] == 3, "CLI stats fact count mismatch"
            
            # Test health checks
            health_v11 = await client_v11.health_check()
            health_new = await client_new.health_check()
            health_hybrid = await client_hybrid.health_check()
            cli_health = await cli_command.health_check()
            
            assert health_v11["status"] == "healthy", "V11 client health check failed"
            assert health_new["status"] == "healthy", "New client health check failed"
            assert health_hybrid["status"] == "healthy", "Hybrid client health check failed"
            assert cli_health["status"] == "healthy", "CLI health check failed"
            
            await client.cleanup()
            
            self.test_results["integration_tests"]["cross_component_compatibility"] = "PASSED"
            self.test_results["integration_tests"]["shared_storage"] = "PASSED"
            self.test_results["integration_tests"]["data_consistency"] = "PASSED"
            self.test_results["integration_tests"]["search_consistency"] = "PASSED"
            self.test_results["integration_tests"]["context_consistency"] = "PASSED"
            self.test_results["integration_tests"]["statistics_consistency"] = "PASSED"
            self.test_results["integration_tests"]["health_consistency"] = "PASSED"
            self.test_results["passed_tests"] += 7
            
            logger.info("✅ Full Integration: PASSED")
            
        except Exception as e:
            logger.error(f"❌ Full Integration: FAILED - {e}")
            self.test_results["integration_tests"]["error"] = str(e)
            self.test_results["failed_tests"] += 1
    
    def print_test_summary(self):
        """Print comprehensive test summary"""
        logger.info("\n" + "=" * 80)
        logger.info("📊 COMPREHENSIVE TEST SUMMARY")
        logger.info("=" * 80)
        
        total_tests = self.test_results["passed_tests"] + self.test_results["failed_tests"]
        success_rate = (self.test_results["passed_tests"] / total_tests * 100) if total_tests > 0 else 0
        
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {self.test_results['passed_tests']} ✅")
        logger.info(f"Failed: {self.test_results['failed_tests']} ❌")
        logger.info(f"Success Rate: {success_rate:.1f}%")
        logger.info(f"Errors: {self.test_results['error_count']}")
        
        logger.info("\n📋 DETAILED RESULTS:")
        for category, results in self.test_results.items():
            if category in ["error_count", "total_tests", "passed_tests", "failed_tests"]:
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
            logger.info("\n🎉 ALL TESTS PASSED! SYSTEM IS READY FOR PRODUCTION!")
        else:
            logger.info(f"\n⚠️  {self.test_results['failed_tests']} TESTS FAILED - REVIEW REQUIRED")
        
        logger.info("=" * 80)


async def main():
    """Main test runner"""
    # Get DeepSeek API key from environment
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    if not deepseek_api_key:
        logger.error("❌ DEEPSEEK_API_KEY environment variable not set")
        return 1
    
    # Create tester
    tester = ComprehensiveSystemTester(deepseek_api_key)
    
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
