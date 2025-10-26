#!/usr/bin/env python3
"""
Migration Validation Script
Automatically validates that the restructure doesn't break anything
"""

import os
import sys
import subprocess
import time
import importlib.util
from pathlib import Path

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 {description} - ERROR: {e}")
        return False

def test_imports():
    """Test that all imports work"""
    print("\n📦 Testing imports...")
    
    tests = [
        ("from luminoracore_sdk import LuminoraCoreClient", "SDK client import"),
        ("from luminoracore_sdk import LuminoraCoreClientV11", "SDK v1.1 client import"),
        ("from luminoracore_sdk.session import InMemoryStorageV11", "Storage import"),
        ("from luminoracore_sdk.types.provider import ProviderConfig", "Provider config import"),
    ]
    
    all_passed = True
    for import_statement, description in tests:
        if not run_command(f"python -c '{import_statement}'", description):
            all_passed = False
    
    return all_passed

def test_client_creation():
    """Test that clients can be created"""
    print("\n🔧 Testing client creation...")
    
    test_code = """
from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
from luminoracore_sdk.session import InMemoryStorageV11

# Test basic client creation
client = LuminoraCoreClient()
print("Basic client created successfully")

# Test v1.1 client creation
storage = InMemoryStorageV11()
client_v11 = LuminoraCoreClientV11(client, storage_v11=storage)
print("V1.1 client created successfully")

# Test storage creation
storage = InMemoryStorageV11()
print("Storage created successfully")
"""
    
    return run_command(f"python -c \"{test_code}\"", "Client creation")

def test_examples():
    """Test that examples still work"""
    print("\n📚 Testing examples...")
    
    examples_dir = Path("examples")
    if not examples_dir.exists():
        print("⚠️  Examples directory not found")
        return True
    
    all_passed = True
    for example_file in examples_dir.glob("*.py"):
        if example_file.name != "__init__.py":
            if not run_command(f"python -c \"import sys; sys.path.append('.'); exec(open('{example_file}').read())\"", f"Example {example_file.name}"):
                all_passed = False
    
    return all_passed

def test_sdk_examples():
    """Test that SDK examples still work"""
    print("\n🔧 Testing SDK examples...")
    
    sdk_examples_dir = Path("luminoracore-sdk-python/examples")
    if not sdk_examples_dir.exists():
        print("⚠️  SDK examples directory not found")
        return True
    
    all_passed = True
    for example_file in sdk_examples_dir.glob("*.py"):
        if example_file.name != "__init__.py":
            if not run_command(f"python -c \"import sys; sys.path.append('luminoracore-sdk-python'); exec(open('{example_file}').read())\"", f"SDK example {example_file.name}"):
                all_passed = False
    
    return all_passed

def test_cli():
    """Test that CLI still works"""
    print("\n🖥️  Testing CLI...")
    
    cli_dir = Path("luminoracore-cli")
    if not cli_dir.exists():
        print("⚠️  CLI directory not found")
        return True
    
    # Test CLI import
    if not run_command("python -c \"import sys; sys.path.append('luminoracore-cli'); from luminoracore_cli import main\"", "CLI import"):
        return False
    
    # Test CLI help
    if not run_command("python -c \"import sys; sys.path.append('luminoracore-cli'); from luminoracore_cli import main; main(['--help'])\"", "CLI help"):
        return False
    
    return True

def test_performance():
    """Test that performance is maintained"""
    print("\n⚡ Testing performance...")
    
    test_code = """
import time
from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
from luminoracore_sdk.session import InMemoryStorageV11

# Test client creation performance
start = time.time()
client = LuminoraCoreClient()
storage = InMemoryStorageV11()
client_v11 = LuminoraCoreClientV11(client, storage_v11=storage)
end = time.time()

creation_time = end - start
print(f"Client creation time: {creation_time:.3f}s")

# Should be fast (less than 1 second)
assert creation_time < 1.0, f"Client creation too slow: {creation_time:.2f}s"
print("Performance test passed")
"""
    
    return run_command(f"python -c \"{test_code}\"", "Performance test")

def test_memory_usage():
    """Test that memory usage is reasonable"""
    print("\n💾 Testing memory usage...")
    
    test_code = """
import psutil
import gc
from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
from luminoracore_sdk.session import InMemoryStorageV11

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

print(f"Memory used: {memory_used / 1024 / 1024:.1f}MB")

# Should use reasonable amount of memory (less than 100MB)
assert memory_used < 100 * 1024 * 1024, f"Memory usage too high: {memory_used / 1024 / 1024:.1f}MB"
print("Memory usage test passed")
"""
    
    try:
        return run_command(f"python -c \"{test_code}\"", "Memory usage test")
    except:
        print("⚠️  psutil not available, skipping memory test")
        return True

def test_no_breaking_changes():
    """Test that no breaking changes were introduced"""
    print("\n🔒 Testing for breaking changes...")
    
    test_code = """
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

# Test that v1.1 client has expected methods
storage = InMemoryStorageV11()
client_v11 = LuminoraCoreClientV11(client, storage_v11=storage)
expected_v11_methods = [
    'save_fact', 'get_facts', 'save_episode', 'get_episodes',
    'update_affinity', 'get_affinity', 'send_message_with_memory'
]

for method in expected_v11_methods:
    assert hasattr(client_v11, method), f"V1.1 method {method} not found"

print("No breaking changes detected")
"""
    
    return run_command(f"python -c \"{test_code}\"", "Breaking changes test")

def main():
    """Run all validation tests"""
    print("🚀 Starting migration validation...")
    print("=" * 50)
    
    start_time = time.time()
    
    tests = [
        ("Imports", test_imports),
        ("Client Creation", test_client_creation),
        ("Examples", test_examples),
        ("SDK Examples", test_sdk_examples),
        ("CLI", test_cli),
        ("Performance", test_performance),
        ("Memory Usage", test_memory_usage),
        ("Breaking Changes", test_no_breaking_changes),
    ]
    
    results = {}
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results[test_name] = result
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
            results[test_name] = False
            all_passed = False
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print("\n" + "=" * 50)
    print("📊 VALIDATION RESULTS")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:20} {status}")
    
    print(f"\nTotal time: {total_time:.2f}s")
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED - Migration is safe to continue!")
        return 0
    else:
        print("\n💥 SOME TESTS FAILED - Migration should be stopped!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
