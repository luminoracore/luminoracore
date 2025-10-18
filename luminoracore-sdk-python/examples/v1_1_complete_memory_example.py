"""
LuminoraCore v1.1 - Complete Memory Management Example

This example demonstrates the COMPLETE memory system with both read and write operations:
✅ Save facts and episodes
✅ Retrieve facts and episodes  
✅ Delete facts
✅ Get memory statistics
✅ Manage affinity relationships

REAL USE CASE:
A customer support chatbot that:
1. Learns about users automatically
2. Stores memorable interactions
3. Tracks relationship progression
4. Provides memory analytics
"""

import asyncio
import json
from datetime import datetime

# SDK imports
from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
from luminoracore_sdk.types.provider import ProviderConfig
from luminoracore_sdk.types.session import StorageConfig

# Mock base client for demonstration
class MockBaseClient:
    """Mock base client for demonstration"""
    def __init__(self):
        self.sessions = {}

async def main():
    """Complete memory management demonstration."""
    
    print("=" * 80)
    print("🧠 LuminoraCore v1.1 - COMPLETE MEMORY MANAGEMENT")
    print("=" * 80)
    print("\nThis example demonstrates the COMPLETE memory system:")
    print("✅ Save facts and episodes")
    print("✅ Retrieve facts and episodes")
    print("✅ Delete facts")
    print("✅ Get memory statistics")
    print("✅ Manage affinity relationships\n")
    
    # ========================================
    # 1. SETUP
    # ========================================
    print("\n" + "=" * 80)
    print("STEP 1: SETUP")
    print("=" * 80)
    
    # Initialize storage
    storage_v11 = InMemoryStorageV11()
    print("✅ Storage initialized: InMemoryStorageV11")
    
    # Initialize base client (mock)
    base_client = MockBaseClient()
    print("✅ Base client initialized: MockBaseClient")
    
    # Initialize v1.1 client
    client_v11 = LuminoraCoreClientV11(base_client, storage_v11=storage_v11)
    print("✅ v1.1 client initialized: LuminoraCoreClientV11")
    
    # Test user and personality
    user_id = "user_carlos_123"
    personality_name = "dr_luna"
    
    print(f"\n👤 Test user: {user_id}")
    print(f"🎭 Test personality: {personality_name}")
    
    # ========================================
    # 2. SAVE FACTS (WRITE OPERATIONS)
    # ========================================
    print("\n" + "=" * 80)
    print("STEP 2: SAVE FACTS (WRITE OPERATIONS)")
    print("=" * 80)
    
    # Save personal information
    print("\n📝 Saving personal information...")
    await client_v11.save_fact(
        user_id=user_id,
        category="personal_info",
        key="name",
        value="Carlos",
        confidence=0.95,
        source="user_input"
    )
    print("✅ Fact saved: name = Carlos")
    
    await client_v11.save_fact(
        user_id=user_id,
        category="personal_info",
        key="age",
        value=28,
        confidence=0.9,
        source="user_input"
    )
    print("✅ Fact saved: age = 28")
    
    await client_v11.save_fact(
        user_id=user_id,
        category="personal_info",
        key="profession",
        value="Software Developer",
        confidence=0.95,
        source="user_input"
    )
    print("✅ Fact saved: profession = Software Developer")
    
    # Save preferences
    print("\n🎯 Saving preferences...")
    await client_v11.save_fact(
        user_id=user_id,
        category="preferences",
        key="programming_language",
        value="Python",
        confidence=0.9,
        source="conversation"
    )
    print("✅ Fact saved: programming_language = Python")
    
    await client_v11.save_fact(
        user_id=user_id,
        category="preferences",
        key="hobby",
        value="Playing guitar",
        confidence=0.85,
        source="conversation"
    )
    print("✅ Fact saved: hobby = Playing guitar")
    
    # Save work information
    print("\n💼 Saving work information...")
    await client_v11.save_fact(
        user_id=user_id,
        category="work",
        key="company",
        value="TechStartup Inc",
        confidence=0.9,
        source="user_input"
    )
    print("✅ Fact saved: company = TechStartup Inc")
    
    await client_v11.save_fact(
        user_id=user_id,
        category="work",
        key="project",
        value="AI Chatbot Implementation",
        confidence=0.95,
        source="conversation"
    )
    print("✅ Fact saved: project = AI Chatbot Implementation")
    
    # ========================================
    # 3. SAVE EPISODES (WRITE OPERATIONS)
    # ========================================
    print("\n" + "=" * 80)
    print("STEP 3: SAVE EPISODES (WRITE OPERATIONS)")
    print("=" * 80)
    
    # Save memorable episodes
    print("\n🎬 Saving memorable episodes...")
    await client_v11.save_episode(
        user_id=user_id,
        episode_type="milestone",
        title="First conversation",
        summary="Carlos introduced himself and shared his background as a software developer",
        importance=7.5,
        sentiment="positive",
        context="initial_meeting"
    )
    print("✅ Episode saved: First conversation")
    
    await client_v11.save_episode(
        user_id=user_id,
        episode_type="emotional_moment",
        title="Shared passion for music",
        summary="Carlos mentioned he plays guitar and we bonded over music",
        importance=8.0,
        sentiment="very_positive",
        context="personal_connection"
    )
    print("✅ Episode saved: Shared passion for music")
    
    await client_v11.save_episode(
        user_id=user_id,
        episode_type="goal_achievement",
        title="Project discussion",
        summary="Carlos explained his AI chatbot project and we discussed implementation details",
        importance=9.0,
        sentiment="positive",
        context="work_collaboration"
    )
    print("✅ Episode saved: Project discussion")
    
    await client_v11.save_episode(
        user_id=user_id,
        episode_type="routine",
        title="Daily check-in",
        summary="Regular conversation about progress and next steps",
        importance=4.0,
        sentiment="neutral",
        context="routine_interaction"
    )
    print("✅ Episode saved: Daily check-in")
    
    # ========================================
    # 4. UPDATE AFFINITY (WRITE OPERATIONS)
    # ========================================
    print("\n" + "=" * 80)
    print("STEP 4: UPDATE AFFINITY (WRITE OPERATIONS)")
    print("=" * 80)
    
    # Update affinity based on interactions
    print("\n💝 Updating affinity relationships...")
    
    # Initial interaction
    affinity = await client_v11.update_affinity(
        user_id=user_id,
        personality_name=personality_name,
        points_delta=5,
        interaction_type="first_meeting"
    )
    print(f"✅ Affinity updated: {affinity['affinity_points']} points ({affinity['current_level']})")
    
    # Positive interactions
    affinity = await client_v11.update_affinity(
        user_id=user_id,
        personality_name=personality_name,
        points_delta=8,
        interaction_type="shared_interest"
    )
    print(f"✅ Affinity updated: {affinity['affinity_points']} points ({affinity['current_level']})")
    
    # More positive interactions
    affinity = await client_v11.update_affinity(
        user_id=user_id,
        personality_name=personality_name,
        points_delta=10,
        interaction_type="deep_conversation"
    )
    print(f"✅ Affinity updated: {affinity['affinity_points']} points ({affinity['current_level']})")
    
    # ========================================
    # 5. RETRIEVE DATA (READ OPERATIONS)
    # ========================================
    print("\n" + "=" * 80)
    print("STEP 5: RETRIEVE DATA (READ OPERATIONS)")
    print("=" * 80)
    
    # Get all facts
    print("\n📖 Retrieving all facts...")
    all_facts = await client_v11.get_facts(user_id)
    print(f"✅ Retrieved {len(all_facts)} facts:")
    for fact in all_facts:
        print(f"   - {fact['category']}:{fact['key']} = {fact['value']} (confidence: {fact.get('confidence', 'N/A')})")
    
    # Get facts by category
    print("\n📖 Retrieving personal info facts...")
    personal_facts = await client_v11.get_facts(user_id, category="personal_info")
    print(f"✅ Retrieved {len(personal_facts)} personal info facts:")
    for fact in personal_facts:
        print(f"   - {fact['key']}: {fact['value']}")
    
    # Get all episodes
    print("\n🎬 Retrieving all episodes...")
    all_episodes = await client_v11.get_episodes(user_id)
    print(f"✅ Retrieved {len(all_episodes)} episodes:")
    for episode in all_episodes:
        print(f"   - {episode['episode_type']}: {episode['title']} (importance: {episode['importance']}/10)")
    
    # Get important episodes only
    print("\n🎬 Retrieving important episodes (importance >= 7.0)...")
    important_episodes = await client_v11.get_episodes(user_id, min_importance=7.0)
    print(f"✅ Retrieved {len(important_episodes)} important episodes:")
    for episode in important_episodes:
        print(f"   - {episode['episode_type']}: {episode['title']} (importance: {episode['importance']}/10)")
    
    # Get current affinity
    print("\n💝 Retrieving current affinity...")
    current_affinity = await client_v11.get_affinity(user_id, personality_name)
    print(f"✅ Current affinity: {current_affinity['affinity_points']} points ({current_affinity['current_level']})")
    
    # ========================================
    # 6. MEMORY STATISTICS
    # ========================================
    print("\n" + "=" * 80)
    print("STEP 6: MEMORY STATISTICS")
    print("=" * 80)
    
    # Get memory statistics
    print("\n📊 Getting memory statistics...")
    stats = await client_v11.get_memory_stats(user_id)
    
    print("✅ Memory Statistics:")
    print(f"   - Total facts: {stats['total_facts']}")
    print(f"   - Total episodes: {stats['total_episodes']}")
    print(f"   - Fact categories: {stats['fact_categories']}")
    print(f"   - Episode types: {stats['episode_types']}")
    
    if stats['most_important_episode']:
        most_important = stats['most_important_episode']
        print(f"   - Most important episode: {most_important['title']} (importance: {most_important['importance']}/10)")
    
    # ========================================
    # 7. DELETE OPERATIONS
    # ========================================
    print("\n" + "=" * 80)
    print("STEP 7: DELETE OPERATIONS")
    print("=" * 80)
    
    # Delete a fact
    print("\n🗑️ Deleting a fact...")
    deleted = await client_v11.delete_fact(user_id, "preferences", "hobby")
    print(f"✅ Fact deleted: preferences:hobby (result: {deleted})")
    
    # Verify deletion
    print("\n📖 Verifying deletion...")
    remaining_facts = await client_v11.get_facts(user_id, category="preferences")
    print(f"✅ Remaining preference facts: {len(remaining_facts)}")
    for fact in remaining_facts:
        print(f"   - {fact['key']}: {fact['value']}")
    
    # ========================================
    # 8. FINAL SUMMARY
    # ========================================
    print("\n" + "=" * 80)
    print("STEP 8: FINAL SUMMARY")
    print("=" * 80)
    
    # Final statistics
    final_stats = await client_v11.get_memory_stats(user_id)
    final_affinity = await client_v11.get_affinity(user_id, personality_name)
    
    print("\n🎉 FINAL RESULTS:")
    print(f"✅ Total facts stored: {final_stats['total_facts']}")
    print(f"✅ Total episodes stored: {final_stats['total_episodes']}")
    print(f"✅ Final affinity: {final_affinity['affinity_points']} points ({final_affinity['current_level']})")
    print(f"✅ Fact categories: {list(final_stats['fact_categories'].keys())}")
    print(f"✅ Episode types: {list(final_stats['episode_types'].keys())}")
    
    print("\n🚀 COMPLETE MEMORY SYSTEM DEMONSTRATED!")
    print("✅ Write operations: save_fact, save_episode, update_affinity")
    print("✅ Read operations: get_facts, get_episodes, get_affinity")
    print("✅ Delete operations: delete_fact")
    print("✅ Analytics operations: get_memory_stats")
    print("\n💡 The SDK v1.1 now has COMPLETE memory management capabilities!")

if __name__ == "__main__":
    asyncio.run(main())
