"""
LuminoraCore v1.1 - Dynamic Personality Demo (Simplified)

Demonstrates personality adaptation using the SDK v1.1.
"""

import asyncio
from luminoracore_sdk import (
    LuminoraCoreClient,
    LuminoraCoreClientV11,
    InMemoryStorageV11
)


async def main():
    print("LuminoraCore v1.1 - Dynamic Personality Demo (Simplified)")
    print("=" * 60)
    
    # Initialize client with in-memory storage
    client = LuminoraCoreClient()
    await client.initialize()
    
    storage = InMemoryStorageV11()
    client_v11 = LuminoraCoreClientV11(client, storage_v11=storage)
    
    user_id = "demo_user"
    personality_name = "alicia"
    
    print(f"\nPersonality: {personality_name}")
    print(f"User: {user_id}")
    
    # Simulate different affinity levels
    affinity_levels = [
        (5, "stranger"),
        (30, "acquaintance"),
        (50, "friend"),
        (70, "close_friend"),
        (90, "best_friend")
    ]
    
    print(f"\nSimulating personality adaptation at different affinity levels...")
    
    for affinity_points, expected_level in affinity_levels:
        print(f"\n--- Affinity: {affinity_points}/100 ({expected_level}) ---")
        
        # Update affinity state
        await client_v11.update_affinity(
            user_id, personality_name, affinity_points, "positive"
        )
        
        # Simulate personality evolution
        session_id = f"{user_id}_session_{affinity_points}"
        evolution_result = await client_v11.evolve_personality(
            session_id, user_id, personality_name
        )
        
        print(f"   Evolution Analysis:")
        print(f"   - Changes Detected: {evolution_result['changes_detected']}")
        print(f"   - Confidence Score: {evolution_result['confidence_score']:.2f}")
        print(f"   - Triggers: {evolution_result['evolution_triggers']}")
        
        if evolution_result['changes_detected']:
            print(f"   - Personality Updates: {evolution_result['personality_updates']}")
            for change in evolution_result.get('changes', []):
                print(f"     * {change['trait_name']}: {change['old_value']:.2f} -> {change['new_value']:.2f}")
                print(f"       Reason: {change['change_reason']}")
        
        # Show personality adaptation effect
        if expected_level == "stranger":
            print(f"   Effect: Formal, reserved, professional communication")
        elif expected_level == "acquaintance":
            print(f"   Effect: Friendly but still somewhat formal")
        elif expected_level == "friend":
            print(f"   Effect: Casual, friendly, comfortable conversation")
        elif expected_level == "close_friend":
            print(f"   Effect: Very casual, playful, intimate communication")
        elif expected_level == "best_friend":
            print(f"   Effect: Extremely casual, inside jokes, deep understanding")
    
    # Get final affinity state
    final_affinity = await client_v11.get_affinity(user_id, personality_name)
    
    print(f"\nFinal Affinity State:")
    print(f"   Level: {final_affinity['current_level'] if final_affinity else 'unknown'}")
    print(f"   Points: {final_affinity['affinity_points'] if final_affinity else 0}/100")
    
    # Demonstrate session export (simplified)
    print(f"\nSession Export Demo:")
    print(f"   Note: Full session export requires SQLite or persistent storage")
    print(f"   Current implementation uses InMemoryStorageV11")
    print(f"   For full features, use SQLiteStorageV11 or other persistent storage")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    
    await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
