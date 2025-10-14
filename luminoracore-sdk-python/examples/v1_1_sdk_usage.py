"""
LuminoraCore SDK v1.1 - Complete Usage Example

Demonstrates all v1.1 features through the SDK.
"""

import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
from luminoracore_sdk.types.provider import ProviderConfig
from luminoracore_sdk.types.session import StorageConfig


async def main():
    """Demonstrate v1.1 SDK features."""
    print("LuminoraCore SDK v1.1 - Complete Usage Example")
    print("=" * 60)
    
    # ========================================
    # 1. INITIALIZE CLIENT WITH v1.1
    # ========================================
    print("\n1. Initializing SDK with v1.1 extensions...")
    
    # Create base client
    base_client = LuminoraCoreClient(
        storage_config=StorageConfig(storage_type="memory")
    )
    await base_client.initialize()
    
    # Create v1.1 storage
    storage_v11 = InMemoryStorageV11()
    
    # Create v1.1 client extension
    client_v11 = LuminoraCoreClientV11(base_client, storage_v11=storage_v11)
    
    print("  [OK] SDK initialized with v1.1 extensions")
    
    # ========================================
    # 2. AFFINITY MANAGEMENT
    # ========================================
    print("\n2. Affinity Management...")
    
    user_id = "demo_user"
    personality_name = "alicia"
    
    # Initial affinity
    initial_affinity = await client_v11.get_affinity(user_id, personality_name)
    print(f"  Initial affinity: {initial_affinity}")
    
    # Update affinity (positive interaction)
    print("  Simulating positive interaction...")
    updated = await client_v11.update_affinity(
        user_id=user_id,
        personality_name=personality_name,
        points_delta=5,
        interaction_type="positive"
    )
    
    print(f"  [OK] Affinity updated: {updated['affinity_points']} points")
    print(f"       Current level: {updated['current_level']}")
    
    # Update affinity multiple times
    for i in range(3):
        await client_v11.update_affinity(
            user_id=user_id,
            personality_name=personality_name,
            points_delta=8,
            interaction_type="very_positive"
        )
    
    final_affinity = await client_v11.get_affinity(user_id, personality_name)
    print(f"  [OK] Final affinity: {final_affinity['affinity_points']} points")
    print(f"       Final level: {final_affinity['current_level']}")
    
    # ========================================
    # 3. FACT MANAGEMENT
    # ========================================
    print("\n3. Fact Management...")
    
    # Save facts (would normally be extracted automatically)
    print("  Saving user facts...")
    await storage_v11.save_fact(
        user_id=user_id,
        category="personal_info",
        key="name",
        value="Diego",
        confidence=0.99
    )
    
    await storage_v11.save_fact(
        user_id=user_id,
        category="preferences",
        key="favorite_anime",
        value="Naruto",
        confidence=0.9
    )
    
    await storage_v11.save_fact(
        user_id=user_id,
        category="work",
        key="profession",
        value="Software Developer",
        confidence=0.95
    )
    
    # Retrieve facts
    all_facts = await client_v11.get_facts(user_id)
    print(f"  [OK] Total facts stored: {len(all_facts)}")
    
    # Retrieve by category
    personal_facts = await client_v11.get_facts(user_id, category="personal_info")
    print(f"  [OK] Personal info facts: {len(personal_facts)}")
    
    for fact in personal_facts:
        print(f"       - {fact['key']}: {fact['value']} (confidence: {fact['confidence']:.2f})")
    
    # ========================================
    # 4. EPISODIC MEMORY
    # ========================================
    print("\n4. Episodic Memory...")
    
    # Save episodes
    print("  Creating memorable episodes...")
    
    await storage_v11.save_episode(
        user_id=user_id,
        episode_type="milestone",
        title="First conversation",
        summary="User and AI met for the first time",
        importance=7.0,
        sentiment="positive",
        tags=["first", "milestone"]
    )
    
    await storage_v11.save_episode(
        user_id=user_id,
        episode_type="emotional_moment",
        title="Shared personal story",
        summary="User opened up about difficult childhood",
        importance=9.5,
        sentiment="very_negative",
        tags=["personal", "emotional"]
    )
    
    await storage_v11.save_episode(
        user_id=user_id,
        episode_type="achievement",
        title="Job promotion",
        summary="User got promoted at work",
        importance=8.0,
        sentiment="very_positive",
        tags=["work", "success"]
    )
    
    # Retrieve episodes
    all_episodes = await client_v11.get_episodes(user_id)
    print(f"  [OK] Total episodes: {len(all_episodes)}")
    
    # Get only important episodes
    important_episodes = await client_v11.get_episodes(
        user_id=user_id,
        min_importance=7.5
    )
    print(f"  [OK] Important episodes (>7.5): {len(important_episodes)}")
    
    for episode in important_episodes:
        print(f"       - {episode['title']} (importance: {episode['importance']}/10)")
    
    # ========================================
    # 5. MEMORY CONTEXT FOR QUERIES
    # ========================================
    print("\n5. Getting Context for Query...")
    
    # This would be used before generating a response
    query = "Tell me what you remember about me"
    
    # Get relevant context
    from luminoracore_sdk.session.memory_v1_1 import MemoryManagerV11
    memory_v11 = MemoryManagerV11(storage_v11=storage_v11)
    
    context = await memory_v11.get_context_for_query(
        user_id=user_id,
        query=query,
        max_facts=5,
        max_episodes=3
    )
    
    print(f"  [OK] Context retrieved:")
    print(f"       Facts: {len(context['facts'])}")
    print(f"       Episodes: {len(context['episodes'])}")
    print(f"       Search results: {len(context['search_results'])}")
    
    # ========================================
    # 6. SNAPSHOT EXPORT (PLACEHOLDER)
    # ========================================
    print("\n6. Snapshot Operations...")
    
    session_id = "demo_session_123"
    
    # Export snapshot
    print("  Exporting personality snapshot...")
    snapshot = await client_v11.export_snapshot(session_id)
    
    print(f"  [OK] Snapshot exported")
    print(f"       Template: {snapshot['_snapshot_info']['template_name']}")
    print(f"       Created: {snapshot['_snapshot_info']['created_at']}")
    
    # ========================================
    # 7. ANALYTICS (PLACEHOLDER)
    # ========================================
    print("\n7. Session Analytics...")
    
    analytics = await client_v11.get_session_analytics(session_id)
    print(f"  [OK] Analytics retrieved:")
    print(f"       Total messages: {analytics['total_messages']}")
    print(f"       Facts learned: {analytics['facts_learned']}")
    print(f"       Episodes created: {analytics['episodes_created']}")
    
    # ========================================
    # SUMMARY
    # ========================================
    print("\n" + "=" * 60)
    print("✓ SDK v1.1 Features Summary:")
    print(f"  - Affinity: {final_affinity['affinity_points']} points ({final_affinity['current_level']})")
    print(f"  - Facts stored: {len(all_facts)}")
    print(f"  - Episodes created: {len(all_episodes)}")
    print(f"  - Important episodes: {len(important_episodes)}")
    print("\n✓ All v1.1 SDK features demonstrated successfully!")
    
    # Cleanup
    await base_client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())

