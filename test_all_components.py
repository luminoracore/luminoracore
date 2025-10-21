#!/usr/bin/env python3
"""
Test all components: Core, CLI, SDK
"""

import asyncio
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore-sdk-python"))

async def test_all_components():
    """Test all components"""
    print("=== TESTING ALL COMPONENTS ===")
    print("Core, CLI, SDK")
    print("=" * 50)
    
    # TEST 1: CORE
    print("\n1. TESTING CORE:")
    try:
        from luminoracore import Personality, PersonalityCompiler, LLMProvider
        from luminoracore.storage.flexible_storage import FlexibleStorageManager
        
        # Test personality creation
        personality_data = {
            "persona": {
                "name": "test_personality",
                "version": "1.1.0",
                "description": "Test personality",
                "author": "Test",
                "tags": ["test"],
                "language": "en",
                "compatibility": ["openai"]
            },
            "core_traits": {
                "archetype": "caregiver",
                "temperament": "calm",
                "communication_style": "formal"
            },
            "linguistic_profile": {
                "tone": ["friendly", "professional"],
                "syntax": "simple",
                "vocabulary": ["technical", "accessible"]
            },
            "behavioral_rules": [
                "Be helpful and professional"
            ]
        }
        
        personality = Personality(personality_data)
        compiler = PersonalityCompiler()
        compiled = compiler.compile(personality, LLMProvider.OPENAI)
        
        print(f"   [OK] Core personality: {personality.persona.name}")
        print(f"   [OK] Core compilation: {type(compiled).__name__}")
        
        # Test storage manager
        storage_manager = FlexibleStorageManager()
        storage = storage_manager.get_storage()
        print(f"   [OK] Core storage: {type(storage).__name__}")
        
    except Exception as e:
        print(f"   [FAIL] Core error: {e}")
    
    # TEST 2: SDK
    print("\n2. TESTING SDK:")
    try:
        from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
        from luminoracore_sdk.session.storage_v1_1 import (
            InMemoryStorageV11,
            FlexibleDynamoDBStorageV11,
            FlexibleSQLiteStorageV11,
            FlexiblePostgreSQLStorageV11,
            FlexibleRedisStorageV11,
            FlexibleMongoDBStorageV11
        )
        
        # Test client creation
        base_client = LuminoraCoreClient()
        await base_client.initialize()
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(base_client, storage_v11=storage)
        
        # Test storage flexible
        dynamodb_storage = FlexibleDynamoDBStorageV11("test_table", "us-east-1")
        sqlite_storage = FlexibleSQLiteStorageV11("test.db")
        
        print(f"   [OK] SDK client: {type(client).__name__}")
        print(f"   [OK] SDK DynamoDB: {type(dynamodb_storage).__name__}")
        print(f"   [OK] SDK SQLite: {type(sqlite_storage).__name__}")
        
        await base_client.cleanup()
        
    except Exception as e:
        print(f"   [FAIL] SDK error: {e}")
    
    # TEST 3: CLI
    print("\n3. TESTING CLI:")
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, "-m", "luminoracore_cli.main", "--help"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"   [OK] CLI help: {len(result.stdout)} characters")
        else:
            print(f"   [FAIL] CLI error: {result.stderr}")
            
    except Exception as e:
        print(f"   [FAIL] CLI error: {e}")
    
    print("\n" + "=" * 50)
    print("ALL COMPONENTS TESTED")

if __name__ == "__main__":
    asyncio.run(test_all_components())
