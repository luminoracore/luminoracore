#!/usr/bin/env python3
"""
Quick v1.1 features example for LuminoraCore.

Demonstrates the new memory and relationship features in v1.1.
"""

import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

# v1.1 imports
from luminoracore.core.relationship.affinity import AffinityManager, AffinityState
from luminoracore.core.memory.fact_extractor import FactExtractor
from luminoracore.core.memory.episodic import EpisodicMemoryManager
from luminoracore.core.memory.classifier import MemoryClassifier


def main():
    """Demonstrate v1.1 features quickly."""
    print("LuminoraCore v1.1 - Quick Features Example")
    print("=" * 50)
    
    # ========================================
    # 1. AFFINITY SYSTEM
    # ========================================
    print("\n1. Affinity System")
    print("-" * 50)
    
    manager = AffinityManager()
    
    # Create user state
    state = AffinityState(
        user_id="demo_user",
        personality_name="alicia",
        affinity_points=0,
        current_level="stranger"
    )
    
    print(f"Initial: {state.current_level} (0 points)")
    
    # Simulate interactions
    for i in range(5):
        old_level = state.current_level
        state = manager.update_affinity_state(state, points_delta=5)
        
        if state.current_level != old_level:
            print(f"Level up! {old_level} -> {state.current_level}")
    
    print(f"Final: {state.current_level} ({state.affinity_points} points)")
    
    # ========================================
    # 2. FACT EXTRACTION
    # ========================================
    print("\n2. Fact Extraction (simple mode)")
    print("-" * 50)
    
    extractor = FactExtractor()
    
    # Extract facts (synchronous for demo)
    message = "I'm Diego, I'm 28 and work in IT"
    facts = extractor.extract_sync(
        user_id="demo_user",
        message=message
    )
    
    print(f"Extracted {len(facts)} fact(s) from:")
    print(f"  '{message}'")
    
    for fact in facts:
        print(f"  - {fact.key}: {fact.value}")
    
    # ========================================
    # 3. EPISODIC MEMORY
    # ========================================
    print("\n3. Episodic Memory")
    print("-" * 50)
    
    episode_mgr = EpisodicMemoryManager()
    
    # Create memorable episode
    episode = episode_mgr.create_episode(
        user_id="demo_user",
        episode_type="emotional_moment",
        title="Loss of pet",
        summary="User's dog passed away",
        sentiment="very_negative"
    )
    
    print(f"Episode: {episode.title}")
    print(f"  Type: {episode.episode_type}")
    print(f"  Importance: {episode.importance:.1f}/10")
    print(f"  Should store: {episode_mgr.should_store_episode(episode.importance)}")
    
    # ========================================
    # 4. MEMORY CLASSIFICATION
    # ========================================
    print("\n4. Memory Classification")
    print("-" * 50)
    
    classifier = MemoryClassifier()
    
    # Classify the fact
    if facts:
        classification = classifier.classify_fact(facts[0])
        print(f"Fact '{facts[0].key}' importance: {classification.importance_level}")
    
    # Classify the episode
    classification = classifier.classify_episode(episode)
    print(f"Episode '{episode.title}' importance: {classification.importance_level}")
    
    # ========================================
    # SUMMARY
    # ========================================
    print("\n" + "=" * 50)
    print("v1.1 Features Summary:")
    print(f"  - Affinity progressed from 0 to {state.affinity_points} points")
    print(f"  - Level changed from stranger to {state.current_level}")
    print(f"  - Extracted {len(facts)} facts")
    print(f"  - Created 1 episode (importance: {episode.importance:.1f}/10)")
    print("\nAll v1.1 features demonstrated successfully!")


if __name__ == "__main__":
    main()

