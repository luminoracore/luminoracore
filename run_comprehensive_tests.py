#!/usr/bin/env python3
"""
Comprehensive Test Runner
Master script to run all tests with DeepSeek integration
"""

import os
import sys
import asyncio
import subprocess
import time
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ComprehensiveTestRunner:
    """Master test runner for all LuminoraCore tests"""
    
    def __init__(self, deepseek_api_key: str):
        self.deepseek_api_key = deepseek_api_key
        self.project_root = Path(__file__).parent
        self.test_results = {
            "installation_tests": {"status": "pending", "results": {}},
            "comprehensive_system_tests": {"status": "pending", "results": {}},
            "deepseek_integration_tests": {"status": "pending", "results": {}},
            "overall_status": "pending",
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "error_count": 0
        }
    
    async def run_all_tests(self):
        """Run all comprehensive tests"""
        logger.info("🚀 Starting Comprehensive Test Suite")
        logger.info("=" * 80)
        
        start_time = time.time()
        
        try:
            # Test 1: Installation Process
            await self.run_installation_tests()
            
            # Test 2: Comprehensive System Tests
            await self.run_comprehensive_system_tests()
            
            # Test 3: DeepSeek Integration Tests
            await self.run_deepseek_integration_tests()
            
            # Test 4: Final Validation
            await self.run_final_validation()
            
        except Exception as e:
            logger.error(f"Critical error in test suite: {e}")
            self.test_results["error_count"] += 1
        
        finally:
            end_time = time.time()
            total_time = end_time - start_time
            
            self.print_final_summary(total_time)
    
    async def run_installation_tests(self):
        """Run installation process tests"""
        logger.info("\n📦 Running Installation Process Tests")
        logger.info("-" * 50)
        
        try:
            # Set environment variable for DeepSeek
            env = os.environ.copy()
            env["DEEPSEEK_API_KEY"] = self.deepseek_api_key
            
            # Run installation tests
            result = subprocess.run([
                sys.executable, "tests/test_installation_process.py"
            ], capture_output=True, text=True, timeout=300, env=env)
            
            if result.returncode == 0:
                self.test_results["installation_tests"]["status"] = "PASSED"
                logger.info("✅ Installation Tests: PASSED")
            else:
                self.test_results["installation_tests"]["status"] = "FAILED"
                self.test_results["installation_tests"]["error"] = result.stderr
                logger.error(f"❌ Installation Tests: FAILED - {result.stderr}")
                self.test_results["failed_tests"] += 1
            
        except Exception as e:
            self.test_results["installation_tests"]["status"] = "ERROR"
            self.test_results["installation_tests"]["error"] = str(e)
            logger.error(f"❌ Installation Tests: ERROR - {e}")
            self.test_results["error_count"] += 1
    
    async def run_comprehensive_system_tests(self):
        """Run comprehensive system tests"""
        logger.info("\n🧠 Running Comprehensive System Tests")
        logger.info("-" * 50)
        
        try:
            # Set environment variable for DeepSeek
            env = os.environ.copy()
            env["DEEPSEEK_API_KEY"] = self.deepseek_api_key
            
            # Run comprehensive system tests
            result = subprocess.run([
                sys.executable, "tests/test_comprehensive_system.py"
            ], capture_output=True, text=True, timeout=600, env=env)
            
            if result.returncode == 0:
                self.test_results["comprehensive_system_tests"]["status"] = "PASSED"
                logger.info("✅ Comprehensive System Tests: PASSED")
            else:
                self.test_results["comprehensive_system_tests"]["status"] = "FAILED"
                self.test_results["comprehensive_system_tests"]["error"] = result.stderr
                logger.error(f"❌ Comprehensive System Tests: FAILED - {result.stderr}")
                self.test_results["failed_tests"] += 1
            
        except Exception as e:
            self.test_results["comprehensive_system_tests"]["status"] = "ERROR"
            self.test_results["comprehensive_system_tests"]["error"] = str(e)
            logger.error(f"❌ Comprehensive System Tests: ERROR - {e}")
            self.test_results["error_count"] += 1
    
    async def run_deepseek_integration_tests(self):
        """Run DeepSeek integration tests"""
        logger.info("\n🤖 Running DeepSeek Integration Tests")
        logger.info("-" * 50)
        
        try:
            # Set environment variable for DeepSeek
            env = os.environ.copy()
            env["DEEPSEEK_API_KEY"] = self.deepseek_api_key
            
            # Run DeepSeek integration tests
            result = subprocess.run([
                sys.executable, "tests/test_deepseek_integration.py"
            ], capture_output=True, text=True, timeout=900, env=env)
            
            if result.returncode == 0:
                self.test_results["deepseek_integration_tests"]["status"] = "PASSED"
                logger.info("✅ DeepSeek Integration Tests: PASSED")
            else:
                self.test_results["deepseek_integration_tests"]["status"] = "FAILED"
                self.test_results["deepseek_integration_tests"]["error"] = result.stderr
                logger.error(f"❌ DeepSeek Integration Tests: FAILED - {result.stderr}")
                self.test_results["failed_tests"] += 1
            
        except Exception as e:
            self.test_results["deepseek_integration_tests"]["status"] = "ERROR"
            self.test_results["deepseek_integration_tests"]["error"] = str(e)
            logger.error(f"❌ DeepSeek Integration Tests: ERROR - {e}")
            self.test_results["error_count"] += 1
    
    async def run_final_validation(self):
        """Run final validation tests"""
        logger.info("\n🔍 Running Final Validation Tests")
        logger.info("-" * 50)
        
        try:
            # Test 1: Import all components
            await self.test_all_imports()
            
            # Test 2: Basic functionality
            await self.test_basic_functionality()
            
            # Test 3: Memory operations
            await self.test_memory_operations()
            
            # Test 4: Affinity operations
            await self.test_affinity_operations()
            
            # Test 5: DeepSeek connection
            await self.test_deepseek_connection()
            
            self.test_results["final_validation"] = {"status": "PASSED"}
            logger.info("✅ Final Validation: PASSED")
            
        except Exception as e:
            self.test_results["final_validation"] = {"status": "FAILED", "error": str(e)}
            logger.error(f"❌ Final Validation: FAILED - {e}")
            self.test_results["failed_tests"] += 1
    
    async def test_all_imports(self):
        """Test all imports"""
        try:
            # Core imports
            from luminoracore import PersonalityEngine, MemorySystem, EvolutionEngine
            from luminoracore.interfaces import StorageInterface, MemoryInterface
            from luminoracore.storage import BaseStorage, InMemoryStorage
            
            # SDK imports
            from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
            from luminoracore_sdk.client_new import LuminoraCoreClientNew
            from luminoracore_sdk.client_hybrid import LuminoraCoreClientHybrid
            
            # CLI imports
            from luminoracore_cli.commands_new.memory_new import MemoryCommandNew
            
            logger.info("  ✅ All imports successful")
            
        except Exception as e:
            raise Exception(f"Import test failed: {e}")
    
    async def test_basic_functionality(self):
        """Test basic functionality"""
        try:
            # Test core components
            engine = PersonalityEngine()
            storage = InMemoryStorage()
            memory = MemorySystem(storage)
            evolution = EvolutionEngine()
            
            # Test SDK components
            client = LuminoraCoreClient()
            await client.initialize()
            
            client_v11 = LuminoraCoreClientV11(client)
            client_new = LuminoraCoreClientNew()
            client_hybrid = LuminoraCoreClientHybrid()
            
            # Test CLI components
            cli_command = MemoryCommandNew()
            
            # Test basic operations
            fact_saved = await client_v11.save_fact("test_user", "personal", "name", "Test User", 0.9)
            assert fact_saved, "Fact saving failed"
            
            facts = await client_v11.get_facts("test_user")
            assert len(facts) == 1, "Fact retrieval failed"
            
            await client.cleanup()
            
            logger.info("  ✅ Basic functionality test passed")
            
        except Exception as e:
            raise Exception(f"Basic functionality test failed: {e}")
    
    async def test_memory_operations(self):
        """Test memory operations"""
        try:
            client = LuminoraCoreClient()
            await client.initialize()
            
            client_v11 = LuminoraCoreClientV11(client)
            
            # Test fact operations
            await client_v11.save_fact("memory_test", "personal", "name", "Memory Test", 0.9)
            await client_v11.save_fact("memory_test", "personal", "age", "25", 0.8)
            
            facts = await client_v11.get_facts("memory_test")
            assert len(facts) == 2, "Fact count mismatch"
            
            # Test episode operations
            await client_v11.save_episode("memory_test", "conversation", "Test Episode", "A test conversation", 0.8, "positive")
            
            episodes = await client_v11.get_episodes("memory_test")
            assert len(episodes) == 1, "Episode count mismatch"
            
            # Test search
            search_results = await client_v11.search_facts("memory_test", "name")
            assert len(search_results) == 1, "Search failed"
            
            await client.cleanup()
            
            logger.info("  ✅ Memory operations test passed")
            
        except Exception as e:
            raise Exception(f"Memory operations test failed: {e}")
    
    async def test_affinity_operations(self):
        """Test affinity operations"""
        try:
            client = LuminoraCoreClient()
            await client.initialize()
            
            client_v11 = LuminoraCoreClientV11(client)
            
            # Test affinity building
            affinity = await client_v11.update_affinity("affinity_test", "test_personality", 10, "positive")
            assert affinity is not None, "Affinity update failed"
            assert affinity["points"] == 10, "Affinity points mismatch"
            
            # Test affinity retrieval
            retrieved_affinity = await client_v11.get_affinity("affinity_test", "test_personality")
            assert retrieved_affinity is not None, "Affinity retrieval failed"
            assert retrieved_affinity["points"] == 10, "Retrieved affinity points mismatch"
            
            # Test all affinities
            all_affinities = await client_v11.get_all_affinities("affinity_test")
            assert len(all_affinities) == 1, "All affinities count mismatch"
            
            await client.cleanup()
            
            logger.info("  ✅ Affinity operations test passed")
            
        except Exception as e:
            raise Exception(f"Affinity operations test failed: {e}")
    
    async def test_deepseek_connection(self):
        """Test DeepSeek connection"""
        try:
            import httpx
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                headers = {
                    "Authorization": f"Bearer {self.deepseek_api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": "Hello, please respond with 'Connection successful'"}],
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
                
                assert result["choices"][0]["message"]["content"] is not None, "DeepSeek response is None"
                
            logger.info("  ✅ DeepSeek connection test passed")
            
        except Exception as e:
            raise Exception(f"DeepSeek connection test failed: {e}")
    
    def print_final_summary(self, total_time):
        """Print final test summary"""
        logger.info("\n" + "=" * 80)
        logger.info("📊 COMPREHENSIVE TEST SUITE SUMMARY")
        logger.info("=" * 80)
        
        # Calculate totals
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        
        for test_category, results in self.test_results.items():
            if test_category in ["overall_status", "total_tests", "passed_tests", "failed_tests", "error_count"]:
                continue
            
            if isinstance(results, dict) and "status" in results:
                total_tests += 1
                if results["status"] == "PASSED":
                    passed_tests += 1
                elif results["status"] in ["FAILED", "ERROR"]:
                    failed_tests += 1
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        logger.info(f"Total Test Categories: {total_tests}")
        logger.info(f"Passed: {passed_tests} ✅")
        logger.info(f"Failed: {failed_tests} ❌")
        logger.info(f"Success Rate: {success_rate:.1f}%")
        logger.info(f"Total Time: {total_time:.2f} seconds")
        logger.info(f"Errors: {self.test_results['error_count']}")
        
        logger.info("\n📋 DETAILED RESULTS:")
        for test_category, results in self.test_results.items():
            if test_category in ["overall_status", "total_tests", "passed_tests", "failed_tests", "error_count"]:
                continue
            
            if isinstance(results, dict) and "status" in results:
                status_emoji = "✅" if results["status"] == "PASSED" else "❌" if results["status"] in ["FAILED", "ERROR"] else "⏳"
                logger.info(f"  {status_emoji} {test_category.replace('_', ' ').title()}: {results['status']}")
                
                if "error" in results:
                    logger.info(f"    Error: {results['error']}")
        
        # Overall status
        if failed_tests == 0 and self.test_results["error_count"] == 0:
            self.test_results["overall_status"] = "PASSED"
            logger.info("\n🎉 ALL TESTS PASSED! SYSTEM IS READY FOR PRODUCTION!")
        else:
            self.test_results["overall_status"] = "FAILED"
            logger.info(f"\n⚠️  {failed_tests} TEST CATEGORIES FAILED - REVIEW REQUIRED")
        
        logger.info("=" * 80)
        
        # Return appropriate exit code
        if self.test_results["overall_status"] == "PASSED":
            return 0
        else:
            return 1


async def main():
    """Main test runner"""
    # Get DeepSeek API key
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    if not deepseek_api_key:
        logger.error("❌ DEEPSEEK_API_KEY environment variable not set")
        logger.error("Please set it with: $env:DEEPSEEK_API_KEY=\"your_api_key_here\"")
        return 1
    
    # Create test runner
    runner = ComprehensiveTestRunner(deepseek_api_key)
    
    # Run all tests
    exit_code = await runner.run_all_tests()
    
    return exit_code


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
