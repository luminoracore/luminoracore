"""
LuminoraCore v1.1 - Memory System Demo (Simplified)

Demonstrates fact and episode management using the SDK v1.1.
"""

import asyncio
from luminoracore_sdk import (
    LuminoraCoreClient,
    LuminoraCoreClientV11,
    InMemoryStorageV11
)


async def main():
    print("LuminoraCore v1.1 - Memory System Demo (Simplified)")
    print("=" * 60)
    
    # Initialize client with in-memory storage
    client = LuminoraCoreClient()
    await client.initialize()
    
    storage = InMemoryStorageV11()
    client_v11 = LuminoraCoreClientV11(client, storage_v11=storage)
    
    user_id = "demo_user"
    
    print(f"\nUser: {user_id}")
    
    # PART 1: Fact Management
    print("\n1. Fact Management")
    print("-" * 30)
    
    # Save facts
    facts_to_save = [
        ("personal_info", "name", "Diego", 0.95),
        ("personal_info", "age", 28, 0.9),
        ("preferences", "language", "Python", 0.85),
        ("preferences", "framework", "FastAPI", 0.8),
        ("hobbies", "anime", "Naruto", 0.9)
    ]
    
    print(f"Saving {len(facts_to_save)} facts...")
    for category, key, value, confidence in facts_to_save:
        await client_v11.save_fact(user_id, category, key, value, confidence=confidence)
        print(f"   + {category}:{key} = {value} (conf: {confidence})")
    
    # Retrieve facts
    all_facts = await client_v11.get_facts(user_id)
    personal_facts = await client_v11.get_facts(user_id, category="personal_info")
    
    print(f"\nRetrieved {len(all_facts)} total facts")
    print(f"Retrieved {len(personal_facts)} personal facts")
    
    # PART 2: Episode Management
    print("\n\n2. Episode Management")
    print("-" * 30)
    
    # Save episodes
    episodes_to_save = [
        ("milestone", "First API created", "Successfully created first REST API", 8.5, "positive"),
        ("achievement", "Database integration", "Integrated SQLite with proper migrations", 7.8, "positive"),
        ("emotional_moment", "Project completion", "Completed major project milestone", 9.0, "very_positive"),
        ("learning", "New technology", "Learned FastAPI framework", 6.5, "positive")
    ]
    
    print(f"Saving {len(episodes_to_save)} episodes...")
    for episode_type, title, summary, importance, sentiment in episodes_to_save:
        await client_v11.save_episode(
            user_id, episode_type, title, summary, importance, sentiment
        )
        print(f"   + {episode_type}: {title} (importance: {importance})")
    
    # Retrieve episodes
    all_episodes = await client_v11.get_episodes(user_id)
    important_episodes = await client_v11.get_episodes(user_id, min_importance=8.0)
    
    print(f"\nRetrieved {len(all_episodes)} total episodes")
    print(f"Retrieved {len(important_episodes)} important episodes (>= 8.0)")
    
    # PART 3: Memory Statistics
    print("\n\n3. Memory Statistics")
    print("-" * 30)
    
    memory_stats = await client_v11.get_memory_stats(user_id)
    
    print(f"Total Facts: {memory_stats['total_facts']}")
    print(f"Total Episodes: {memory_stats['total_episodes']}")
    print(f"Fact Categories: {memory_stats.get('fact_categories', {})}")
    print(f"Episode Types: {memory_stats.get('episode_types', {})}")
    
    if memory_stats.get('most_important_episode'):
        episode = memory_stats['most_important_episode']
        print(f"Most Important Episode: {episode['title']} (importance: {episode['importance']})")
    
    # PART 4: Search and Retrieval
    print("\n\n4. Search and Retrieval")
    print("-" * 30)
    
    # Search memories
    search_results = await client_v11.search_memories(user_id, "Python programming", top_k=3)
    print(f"Search results for 'Python programming': {len(search_results)} results")
    
    for i, result in enumerate(search_results, 1):
        print(f"   {i}. {result.get('content', 'N/A')[:50]}... (score: {result.get('score', 0):.2f})")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    
    await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
