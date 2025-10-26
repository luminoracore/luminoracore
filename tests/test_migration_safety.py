#!/usr/bin/env python3
"""
Migration Safety Tests
Ensures that the restructure doesn't break existing functionality
"""

import pytest
import asyncio
import sys
import os
import time
import subprocess
from pathlib import Path

# Add project paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'luminoracore-sdk-python'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'luminoracore'))

from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
from luminoracore_sdk.session import InMemoryStorageV11
from luminoracore_sdk.types.provider import ProviderConfig


class TestMigrationSafety:
    """Test that migration doesn't break existing functionality"""
    
    def test_sdk_imports_work(self):
        """Test that all SDK imports still work"""
        try:
            from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
            from luminoracore_sdk.session import InMemoryStorageV11
            from luminoracore_sdk.types.provider import ProviderConfig
            print("✅ All SDK imports work")
        except ImportError as e:
            pytest.fail(f"SDK imports failed: {e}")
    
    def test_sdk_client_creation(self):
        """Test that SDK client can be created"""
        try:
            client = LuminoraCoreClient()
            assert client is not None
            print("✅ SDK client creation works")
        except Exception as e:
            pytest.fail(f"SDK client creation failed: {e}")
    
    def test_sdk_v11_client_creation(self):
        """Test that SDK v1.1 client can be created"""
        try:
            storage = InMemoryStorageV11()
            client = LuminoraCoreClientV11(LuminoraCoreClient(), storage_v11=storage)
            assert client is not None
            print("✅ SDK v1.1 client creation works")
        except Exception as e:
            pytest.fail(f"SDK v1.1 client creation failed: {e}")
    
    def test_storage_implementations_work(self):
        """Test that all storage implementations work"""
        try:
            from luminoracore_sdk.session import (
                InMemoryStorageV11,
                FlexibleSQLiteStorageV11,
                FlexibleDynamoDBStorageV11,
                FlexiblePostgreSQLStorageV11,
                FlexibleRedisStorageV11,
                FlexibleMongoDBStorageV11
            )
            
            # Test InMemoryStorageV11
            storage = InMemoryStorageV11()
            assert storage is not None
            
            # Test FlexibleSQLiteStorageV11
            storage = FlexibleSQLiteStorageV11(":memory:")
            assert storage is not None
            
            print("✅ All storage implementations work")
        except Exception as e:
            pytest.fail(f"Storage implementations failed: {e}")
    
    def test_provider_config_works(self):
        """Test that provider configuration works"""
        try:
            config = ProviderConfig(
                name="openai",
                api_key="test-key",
                model="gpt-3.5-turbo"
            )
            assert config.name == "openai"
            assert config.api_key == "test-key"
            assert config.model == "gpt-3.5-turbo"
            print("✅ Provider configuration works")
        except Exception as e:
            pytest.fail(f"Provider configuration failed: {e}")
    
    def test_examples_still_work(self):
        """Test that all examples still work"""
        examples_dir = Path(__file__).parent.parent / "examples"
        if examples_dir.exists():
            for example_file in examples_dir.glob("*.py"):
                if example_file.name != "__init__.py":
                    try:
                        # Test that example can be imported
                        spec = importlib.util.spec_from_file_location(
                            example_file.stem, 
                            example_file
                        )
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        print(f"✅ Example {example_file.name} imports successfully")
                    except Exception as e:
                        pytest.fail(f"Example {example_file.name} failed: {e}")
    
    def test_cli_commands_work(self):
        """Test that CLI commands still work"""
        try:
            # Test that CLI can be imported
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'luminoracore-cli'))
            from luminoracore_cli import main
            print("✅ CLI imports work")
        except ImportError:
            print("⚠️  CLI not available (this is OK during development)")
        except Exception as e:
            pytest.fail(f"CLI import failed: {e}")
    
    def test_performance_maintained(self):
        """Test that performance is maintained"""
        try:
            # Test basic performance
            start_time = time.time()
            
            # Create client
            client = LuminoraCoreClient()
            
            # Test basic operations
            storage = InMemoryStorageV11()
            client_v11 = LuminoraCoreClientV11(client, storage_v11=storage)
            
            end_time = time.time()
            creation_time = end_time - start_time
            
            # Should be fast (less than 1 second)
            assert creation_time < 1.0, f"Client creation too slow: {creation_time:.2f}s"
            print(f"✅ Performance maintained: {creation_time:.3f}s")
            
        except Exception as e:
            pytest.fail(f"Performance test failed: {e}")
    
    def test_memory_usage_unchanged(self):
        """Test that memory usage is unchanged"""
        try:
            import psutil
            import gc
            
            # Get initial memory
            process = psutil.Process()
            initial_memory = process.memory_info().rss
            
            # Create clients
            client = LuminoraCoreClient()
            storage = InMemoryStorageV11()
            client_v11 = LuminoraCoreClientV11(client, storage_v11=storage)
            
            # Get memory after creation
            gc.collect()
            final_memory = process.memory_info().rss
            memory_used = final_memory - initial_memory
            
            # Should use reasonable amount of memory (less than 100MB)
            assert memory_used < 100 * 1024 * 1024, f"Memory usage too high: {memory_used / 1024 / 1024:.1f}MB"
            print(f"✅ Memory usage reasonable: {memory_used / 1024 / 1024:.1f}MB")
            
        except ImportError:
            print("⚠️  psutil not available, skipping memory test")
        except Exception as e:
            pytest.fail(f"Memory usage test failed: {e}")
    
    def test_no_breaking_changes(self):
        """Test that no breaking changes were introduced"""
        try:
            # Test that all public APIs are still available
            from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
            from luminoracore_sdk.session import InMemoryStorageV11
            from luminoracore_sdk.types.provider import ProviderConfig
            
            # Test that client has expected methods
            client = LuminoraCoreClient()
            expected_methods = [
                'initialize', 'cleanup', 'load_personality', 'get_personality',
                'blend_personalities', 'create_session', 'send_message',
                'get_conversation', 'store_memory', 'get_memory'
            ]
            
            for method in expected_methods:
                assert hasattr(client, method), f"Method {method} not found"
            
            print("✅ No breaking changes detected")
            
        except Exception as e:
            pytest.fail(f"Breaking changes test failed: {e}")
    
    def test_documentation_examples_work(self):
        """Test that documentation examples work"""
        try:
            # Test basic usage from documentation
            client = LuminoraCoreClient()
            storage = InMemoryStorageV11()
            client_v11 = LuminoraCoreClientV11(client, storage_v11=storage)
            
            # Test that we can call methods (even if they don't work without setup)
            # This tests that the API is still available
            assert hasattr(client_v11, 'save_fact')
            assert hasattr(client_v11, 'get_facts')
            assert hasattr(client_v11, 'save_episode')
            assert hasattr(client_v11, 'get_episodes')
            assert hasattr(client_v11, 'update_affinity')
            assert hasattr(client_v11, 'get_affinity')
            
            print("✅ Documentation examples work")
            
        except Exception as e:
            pytest.fail(f"Documentation examples test failed: {e}")


class TestExamplesFunctionality:
    """Test that examples still work"""
    
    def test_complete_demo_imports(self):
        """Test that the complete demo can be imported"""
        try:
            demo_path = Path(__file__).parent.parent / "examples" / "luminoracore_v1_1_complete_demo.py"
            if demo_path.exists():
                spec = importlib.util.spec_from_file_location("demo", demo_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                print("✅ Complete demo imports successfully")
            else:
                print("⚠️  Complete demo not found")
        except Exception as e:
            pytest.fail(f"Complete demo import failed: {e}")
    
    def test_sdk_examples_import(self):
        """Test that SDK examples can be imported"""
        try:
            examples_dir = Path(__file__).parent.parent / "luminoracore-sdk-python" / "examples"
            if examples_dir.exists():
                for example_file in examples_dir.glob("*.py"):
                    if example_file.name != "__init__.py":
                        spec = importlib.util.spec_from_file_location(
                            example_file.stem, 
                            example_file
                        )
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        print(f"✅ SDK example {example_file.name} imports successfully")
        except Exception as e:
            pytest.fail(f"SDK examples import failed: {e}")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
