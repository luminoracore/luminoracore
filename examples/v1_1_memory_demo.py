"""
LuminoraCore v1.1 - Memory System Demo

Demonstrates fact extraction and episodic memory.
"""

import asyncio
from datetime import datetime
from luminoracore.core.memory.fact_extractor import Fact, FactExtractor
from luminoracore.core.memory.episodic import EpisodicMemoryManager, Episode
from luminoracore.core.memory.classifier import MemoryClassifier


async def main():
    print("🧠 LuminoraCore v1.1 - Memory System Demo\n")
    print("=" * 60)
    
    # Initialize components
    fact_extractor = FactExtractor()
    episode_manager = EpisodicMemoryManager()
    classifier = MemoryClassifier()
    
    # PART 1: Fact Extraction
    print("\n📋 PART 1: Fact Extraction")
    print("-" * 60)
    
    # Extract facts from a message (synchronous for demo)
    message = "I'm Diego, I'm 28 and work in IT. I love anime, especially Naruto!"
    facts = fact_extractor.extract_sync(user_id="demo_user", message=message)
    
    print(f"\nExtracted {len(facts)} fact(s) from:")
    print(f"  '{message}'")
    
    for fact in facts:
        print(f"\n  Fact: {fact.key} = {fact.value}")
        print(f"    Category: {fact.category}")
        print(f"    Confidence: {fact.confidence:.2f}")
        
        # Classify fact
        classification = classifier.classify_fact(fact)
        print(f"    Importance: {classification.importance_level}")
    
    # PART 2: Episodic Memory
    print("\n\n📖 PART 2: Episodic Memory")
    print("-" * 60)
    
    # Create memorable episodes
    episodes = [
        {
            "type": "emotional_moment",
            "title": "Loss of pet",
            "summary": "User shared sad news about their dog passing away",
            "sentiment": "very_negative"
        },
        {
            "type": "milestone",
            "title": "First conversation",
            "summary": "User and AI met for the first time",
            "sentiment": "positive"
        },
        {
            "type": "achievement",
            "title": "Job promotion",
            "summary": "User got promoted at work",
            "sentiment": "very_positive"
        }
    ]
    
    created_episodes = []
    
    for ep_data in episodes:
        episode = episode_manager.create_episode(
            user_id="demo_user",
            episode_type=ep_data["type"],
            title=ep_data["title"],
            summary=ep_data["summary"],
            sentiment=ep_data["sentiment"]
        )
        created_episodes.append(episode)
        
        print(f"\n  Episode: {episode.title}")
        print(f"    Type: {episode.episode_type}")
        print(f"    Importance: {episode.importance:.1f}/10")
        print(f"    Sentiment: {episode.sentiment}")
        
        # Check if should be stored
        should_store = episode_manager.should_store_episode(episode.importance)
        print(f"    Should store: {'✅ Yes' if should_store else '❌ No'}")
    
    # PART 3: Classification
    print("\n\n🏷️  PART 3: Memory Classification")
    print("-" * 60)
    
    # Get top episodes
    top_episodes = classifier.get_top_n_episodes(created_episodes, n=2)
    
    print(f"\nTop {len(top_episodes)} most important episodes:")
    for i, ep in enumerate(top_episodes, 1):
        print(f"\n  {i}. {ep.title}")
        print(f"     Current importance: {ep.get_current_importance():.1f}/10")
        print(f"     Type: {ep.episode_type}")
    
    print("\n" + "=" * 60)
    print("✅ Demo completed!")


if __name__ == "__main__":
    asyncio.run(main())

