"""
LuminoraCore v1.1 - Affinity System Demo (Simplified)

Demonstrates relationship progression using the SDK v1.1.
"""

import asyncio
from luminoracore_sdk import (
    LuminoraCoreClient,
    LuminoraCoreClientV11,
    InMemoryStorageV11
)


async def main():
    print("LuminoraCore v1.1 - Affinity System Demo (Simplified)")
    print("=" * 60)
    
    # Initialize client with in-memory storage
    client = LuminoraCoreClient()
    await client.initialize()
    
    storage = InMemoryStorageV11()
    client_v11 = LuminoraCoreClientV11(client, storage_v11=storage)
    
    user_id = "demo_user"
    personality_name = "alicia"
    
    print(f"\nInitial State:")
    print(f"   User: {user_id}")
    print(f"   Personality: {personality_name}")
    print(f"   Level: stranger")
    print(f"   Points: 0/100")
    
    # Simulate interactions
    interactions = [
        ("positive", 3, "User gave compliment"),
        ("positive", 2, "Long conversation"),
        ("very_positive", 5, "User expressed gratitude"),
        ("positive", 2, "Another positive exchange")
    ]
    
    print(f"\nSimulating {len(interactions)} interactions...")
    
    total_points = 0
    for i, (interaction_type, delta, reason) in enumerate(interactions, 1):
        total_points += delta
        
        # Determine level based on points
        if total_points <= 20:
            level = "stranger"
        elif total_points <= 40:
            level = "acquaintance"
        elif total_points <= 60:
            level = "friend"
        elif total_points <= 80:
            level = "close_friend"
        else:
            level = "best_friend"
        
        print(f"\n   Interaction {i}: {reason}")
        print(f"   Type: {interaction_type} (+{delta} points)")
        print(f"   Total points: {total_points}/100")
        print(f"   Current level: {level}")
        
        # Update affinity data
        await client_v11.update_affinity(
            user_id, personality_name, delta, interaction_type
        )
    
    # Get final affinity
    affinity = await client_v11.get_affinity(user_id, personality_name)
    
    print(f"\nFinal State:")
    print(f"   Level: {affinity.get('current_level', 'unknown') if affinity else 'unknown'}")
    print(f"   Points: {affinity.get('affinity_points', 0) if affinity else 0}/100")
    print(f"   Total interactions: {affinity.get('total_interactions', 0) if affinity else 0}")
    print(f"   Positive interactions: {affinity.get('positive_interactions', 0) if affinity else 0}")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    
    await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
