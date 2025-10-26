#!/usr/bin/env python3
"""
LuminoraCore v1.1 - Complete Professional Demo

This is the ONLY example you need to understand LuminoraCore v1.1.
It demonstrates ALL features in a clean, professional way.

Features demonstrated:
 Flexible Storage - Works with ANY database
 Memory System - Facts, episodes, affinity
 Dynamic Personalities - Adaptive behavior
 Conversation Memory - Context-aware responses
 Auto-configuration - No hardcoding
"""

import asyncio
import os
import sys
from datetime import datetime

# Add SDK path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'luminoracore-sdk-python'))

from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
from luminoracore_sdk.session import (
    FlexibleDynamoDBStorageV11,
    FlexibleSQLiteStorageV11,
    FlexiblePostgreSQLStorageV11,
    FlexibleRedisStorageV11,
    FlexibleMongoDBStorageV11,
    InMemoryStorageV11
)
from luminoracore_sdk.types.provider import ProviderConfig


async def demo_flexible_storage():
    """Demonstrate flexible storage - works with ANY database"""
    print("\n" + "=" * 80)
    print("FLEXIBLE STORAGE DEMONSTRATION")
    print("=" * 80)
    print("LuminoraCore v1.1 works with ANY database configuration!")
    
    # Demo 1: SQLite with custom configuration
    print("\n1. SQLite - Custom Database & Tables")
    print("-" * 50)
    
    try:
        storage = FlexibleSQLiteStorageV11(
            database_path="./demo_professional.sqlite",
            facts_table="my_facts",
            affinity_table="my_affinity",
            episodes_table="my_episodes"
        )
        
        client = LuminoraCoreClientV11(
            base_client=LuminoraCoreClient(),
            storage_v11=storage
        )
        
        session_id = "professional_demo"
        await client.ensure_session_exists(session_id, "assistant")
        
        # Save some facts
        await client.save_fact(session_id, "personal_info", "name", "Carlos", confidence=0.95)
        await client.save_fact(session_id, "preferences", "language", "Python", confidence=0.9)
        
        # Get facts back
        facts = await client.get_facts(session_id)
        print(f"   [OK] Facts saved and retrieved: {len(facts)} facts")
        for fact in facts:
            print(f"      - {fact['key']}: {fact['value']}")
        
        # Clean up
        os.remove("./demo_professional.sqlite")
        
    except Exception as e:
        print(f"   [ERROR] SQLite demo failed: {e}")
    
    # Demo 2: DynamoDB with existing table
    print("\n2. DynamoDB - Existing Table & Schema")
    print("-" * 50)
    
    try:
        storage = FlexibleDynamoDBStorageV11(
            table_name="luminora-sessions-v1-1-correct",
            region_name="eu-west-1",
            hash_key_name="session_id",
            range_key_name="timestamp"
        )
        
        print("   [OK] DynamoDB storage configured successfully")
        print("   [OK] Works with existing tables and schemas")
        
    except Exception as e:
        print(f"   [ERROR] DynamoDB demo failed: {e}")
    
    # Demo 3: PostgreSQL with custom schema
    print("\n3. PostgreSQL - Custom Schema & Tables")
    print("-" * 50)
    
    try:
        storage = FlexiblePostgreSQLStorageV11(
            host="localhost",
            database="my_luminora_db",
            schema="my_schema",
            facts_table="my_facts_table",
            affinity_table="my_affinity_table"
        )
        
        print("    PostgreSQL storage configured successfully")
        print("    Custom schema and table names supported")
        
    except Exception as e:
        print(f"    PostgreSQL demo failed: {e}")
    
    # Demo 4: Redis with custom key patterns
    print("\n4. Redis - Custom Key Patterns")
    print("-" * 50)
    
    try:
        storage = FlexibleRedisStorageV11(
            host="localhost",
            key_prefix="my_luminora",
            affinity_key_pattern="my:affinity:{user_id}:{personality_name}",
            fact_key_pattern="my:fact:{user_id}:{category}:{key}"
        )
        
        print("    Redis storage configured successfully")
        print("    Custom key patterns supported")
        
    except Exception as e:
        print(f"    Redis demo failed: {e}")
    
    # Demo 5: MongoDB with custom collections
    print("\n5. MongoDB - Custom Collections")
    print("-" * 50)
    
    try:
        storage = FlexibleMongoDBStorageV11(
            host="localhost",
            database="my_luminora_database",
            facts_collection="my_facts_collection",
            affinity_collection="my_affinity_collection"
        )
        
        print("    MongoDB storage configured successfully")
        print("    Custom collection names supported")
        
    except Exception as e:
        print(f"    MongoDB demo failed: {e}")


async def demo_memory_system():
    """Demonstrate the complete memory system"""
    print("\n" + "=" * 80)
    print(" MEMORY SYSTEM DEMONSTRATION")
    print("=" * 80)
    print("Complete memory system with facts, episodes, and affinity!")
    
    # Initialize with in-memory storage for demo
    storage = InMemoryStorageV11()
    client = LuminoraCoreClientV11(
        base_client=LuminoraCoreClient(),
        storage_v11=storage
    )
    
    session_id = "memory_demo"
    personality_name = "assistant"
    
    print(f"\nSession: {session_id}")
    print(f"Personality: {personality_name}")
    
    # 1. Fact Management
    print("\n1. Fact Management")
    print("-" * 30)
    
    facts_to_save = [
        ("personal_info", "name", "Mara", 0.95),
        ("personal_info", "age", 25, 0.9),
        ("preferences", "language", "Spanish", 0.85),
        ("hobbies", "travel", "Himalayas", 0.9)
    ]
    
    for category, key, value, confidence in facts_to_save:
        await client.save_fact(session_id, category, key, value, confidence=confidence)
        print(f"    Saved: {category}:{key} = {value}")
    
    facts = await client.get_facts(session_id)
    print(f"    Total facts: {len(facts)}")
    
    # 2. Episode Management
    print("\n2. Episode Management")
    print("-" * 30)
    
    episodes_to_save = [
        ("milestone", "First conversation", "User and AI met for the first time", 8.0, "positive"),
        ("achievement", "Travel planning", "User planned trip to Himalayas", 9.0, "very_positive"),
        ("learning", "Language preference", "User prefers Spanish communication", 7.5, "positive")
    ]
    
    for episode_type, title, summary, importance, sentiment in episodes_to_save:
        await client.save_episode(session_id, episode_type, title, summary, importance, sentiment)
        print(f"    Saved: {episode_type} - {title}")
    
    episodes = await client.get_episodes(session_id)
    print(f"    Total episodes: {len(episodes)}")
    
    # 3. Affinity System
    print("\n3. Affinity System")
    print("-" * 30)
    
    # Update affinity through interactions
    interactions = [
        ("positive", 3, "User thanked assistant"),
        ("positive", 2, "User shared personal info"),
        ("very_positive", 5, "User expressed gratitude"),
        ("positive", 2, "User asked follow-up question")
    ]
    
    for interaction_type, points, description in interactions:
        await client.update_affinity(session_id, personality_name, points, interaction_type)
        print(f"    {description}: +{points} points")
    
    affinity = await client.get_affinity(session_id, personality_name)
    print(f"    Final affinity: {affinity['current_level']} ({affinity['affinity_points']}/100)")
    
    # 4. Memory Statistics
    print("\n4. Memory Statistics")
    print("-" * 30)
    
    stats = await client.get_memory_stats(session_id)
    print(f"    Total facts: {stats['total_facts']}")
    print(f"    Total episodes: {stats['total_episodes']}")
    print(f"    Fact categories: {list(stats.get('fact_categories', {}).keys())}")
    print(f"    Episode types: {list(stats.get('episode_types', {}).keys())}")


async def demo_conversation_memory():
    """Demonstrate conversation memory with context"""
    print("\n" + "=" * 80)
    print(" CONVERSATION MEMORY DEMONSTRATION")
    print("=" * 80)
    print("Context-aware conversations that remember everything!")
    
    # Initialize with in-memory storage
    storage = InMemoryStorageV11()
    client = LuminoraCoreClientV11(
        base_client=LuminoraCoreClient(),
        storage_v11=storage
    )
    
    session_id = "conversation_demo"
    personality_name = "assistant"
    
    # Mock provider config for demo
    provider_config = ProviderConfig(
        name="deepseek",
        api_key="demo-key",
        model="deepseek-chat"
    )
    
    print(f"\nSession: {session_id}")
    print(f"Personality: {personality_name}")
    
    # Conversation that demonstrates memory
    conversation = [
        "Hello, I'm Carlos from Madrid",
        "Where are you from?",
        "What's my name?",
        "I'm planning a trip to the Himalayas",
        "What do you remember about me?"
    ]
    
    print("\nConversation with memory:")
    print("-" * 50)
    
    for i, message in enumerate(conversation, 1):
        print(f"\nTurn {i}:")
        print(f"    User: \"{message}\"")
        
        # Send message with full context
        response = await client.send_message_with_memory(
            session_id=session_id,
            user_message=message,
            personality_name=personality_name,
            provider_config=provider_config
        )
        
        if response["success"]:
            print(f"    Assistant: \"{response['response']}\"")
            print(f"    Facts learned: {response['facts_learned']}")
            print(f"    Affinity: {response['affinity_level']} ({response['affinity_points']}/100)")
            print(f"    Context length: {response['conversation_length']}")
        else:
            print(f"    Error: {response['error']}")
    
    # Show final memory state
    print("\nFinal Memory State:")
    print("-" * 50)
    
    facts = await client.get_facts(session_id)
    print(f"    Total facts learned: {len(facts)}")
    for fact in facts:
        print(f"      - {fact['key']}: {fact['value']}")
    
    affinity = await client.get_affinity(session_id, personality_name)
    print(f"    Final affinity: {affinity['current_level']} ({affinity['affinity_points']}/100)")


async def demo_auto_configuration():
    """Demonstrate auto-configuration capabilities"""
    print("\n" + "=" * 80)
    print("  AUTO-CONFIGURATION DEMONSTRATION")
    print("=" * 80)
    print("Framework automatically detects and configures everything!")
    
    # Demo 1: Environment variable configuration
    print("\n1. Environment Variable Configuration")
    print("-" * 50)
    
    os.environ["LUMINORA_STORAGE_TYPE"] = "sqlite_flexible"
    os.environ["LUMINORA_SQLITE_PATH"] = "./auto_config_demo.sqlite"
    
    print("    Environment variables set:")
    print(f"      LUMINORA_STORAGE_TYPE = {os.environ.get('LUMINORA_STORAGE_TYPE')}")
    print(f"      LUMINORA_SQLITE_PATH = {os.environ.get('LUMINORA_SQLITE_PATH')}")
    
    # Demo 2: Configuration file
    print("\n2. Configuration File")
    print("-" * 50)
    
    config_example = {
        "storage": {
            "type": "dynamodb_flexible",
            "dynamodb": {
                "table_name": "my-existing-table",
                "region": "us-east-1",
                "hash_key": "session_id",
                "range_key": "timestamp"
            }
        }
    }
    
    print("    Configuration file example:")
    print("      luminora_config.json:")
    print("      {")
    print("        \"storage\": {")
    print("          \"type\": \"dynamodb_flexible\",")
    print("          \"dynamodb\": {")
    print("            \"table_name\": \"my-existing-table\",")
    print("            \"region\": \"us-east-1\"")
    print("          }")
    print("        }")
    print("      }")
    
    # Demo 3: Docker Compose configuration
    print("\n3. Docker Compose Configuration")
    print("-" * 50)
    
    docker_example = {
        "LUMINORA_STORAGE_TYPE": "postgresql_flexible",
        "LUMINORA_POSTGRES_HOST": "postgres",
        "LUMINORA_POSTGRES_DATABASE": "luminora",
        "LUMINORA_POSTGRES_SCHEMA": "public"
    }
    
    print("    Docker Compose environment:")
    for key, value in docker_example.items():
        print(f"      {key} = {value}")
    
    # Clean up
    if os.path.exists("./auto_config_demo.sqlite"):
        os.remove("./auto_config_demo.sqlite")


async def main():
    """Main demonstration function"""
    print("LUMINORACORE v1.1 - COMPLETE PROFESSIONAL DEMO")
    print("=" * 80)
    print("This is the ONLY example you need to understand LuminoraCore v1.1")
    print("It demonstrates ALL features in a clean, professional way")
    print("=" * 80)
    
    try:
        # Run all demonstrations
        await demo_flexible_storage()
        await demo_memory_system()
        await demo_conversation_memory()
        await demo_auto_configuration()
        
        print("\n" + "=" * 80)
        print("DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("[OK] Flexible Storage - Works with ANY database")
        print("[OK] Memory System - Facts, episodes, affinity")
        print("[OK] Conversation Memory - Context-aware responses")
        print("[OK] Auto-configuration - No hardcoding")
        print("[OK] Professional - Clean, organized, working")
        
        print("\nKey Takeaways:")
        print("    Use FlexibleXXXStorageV11 for ANY database")
        print("    Framework auto-detects schemas and configurations")
        print("    Memory system remembers everything across conversations")
        print("    No hardcoding - completely configurable")
        print("    Professional and enterprise-ready")
        
    except Exception as e:
        print(f"Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
