"""
LuminoraCore v1.1 - Affinity System Demo

Demonstrates relationship progression and level changes.
"""

import asyncio
from luminoracore.core.relationship.affinity import AffinityManager, AffinityState


async def main():
    print("🎭 LuminoraCore v1.1 - Affinity System Demo\n")
    print("=" * 60)
    
    # Initialize affinity manager
    manager = AffinityManager()
    
    # Create initial affinity state
    state = AffinityState(
        user_id="demo_user",
        personality_name="alicia",
        affinity_points=0,
        current_level="stranger"
    )
    
    print(f"\n📊 Initial State:")
    print(f"   Level: {state.current_level}")
    print(f"   Points: {state.affinity_points}/100")
    
    # Simulate interactions
    interactions = [
        ("positive", 2, "User gave compliment"),
        ("positive", 3, "Long conversation (150+ chars)"),
        ("positive", 2, "User shared personal info"),
        ("very_positive", 5, "User expressed gratitude"),
        ("positive", 2, "Another positive exchange")
    ]
    
    print(f"\n🔄 Simulating {len(interactions)} interactions...")
    
    for i, (interaction_type, delta, reason) in enumerate(interactions, 1):
        # Update affinity
        old_level = state.current_level
        state = manager.update_affinity_state(state, delta)
        
        print(f"\n   Interaction {i}: {reason}")
        print(f"   Type: {interaction_type} (+{delta} points)")
        print(f"   New points: {state.affinity_points}/100")
        
        # Check for level change
        if state.current_level != old_level:
            print(f"   ✨ LEVEL UP! {old_level} → {state.current_level}")
        
        # Show progress
        progress = manager.get_level_progress(state)
        print(f"   Progress in level: {progress['progress_in_level']*100:.1f}%")
        if progress['next_level']:
            print(f"   Points to next level: {progress['points_to_next_level']}")
    
    print(f"\n📊 Final State:")
    print(f"   Level: {state.current_level}")
    print(f"   Points: {state.affinity_points}/100")
    print(f"   Total messages: {state.total_messages}")
    print(f"   Positive interactions: {state.positive_interactions}")
    
    print("\n" + "=" * 60)
    print("✅ Demo completed!")


if __name__ == "__main__":
    asyncio.run(main())

