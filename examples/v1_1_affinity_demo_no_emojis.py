"""
LuminoraCore v1.1 - Affinity System Demo (Windows Compatible)

Demonstrates the complete affinity system with relationship progression.
"""

import asyncio
from luminoracore.core.relationship import AffinityManager, AffinityState, InteractionType


async def main():
    """Complete affinity system demonstration."""
    
    print("=" * 80)
    print("LuminoraCore v1.1 - Affinity System Demo")
    print("=" * 80)
    
    # ========================================
    # 1. AFFINITY MANAGER INITIALIZATION
    # ========================================
    
    print("\n1. AFFINITY MANAGER INITIALIZATION")
    print("-" * 80)
    
    # Initialize affinity manager
    affinity_manager = AffinityManager()
    print(f"Affinity manager initialized: {type(affinity_manager).__name__}")
    
    # Test user and personality
    user_id = "test_user_123"
    personality_name = "Assistant"
    
    print(f"User ID: {user_id}")
    print(f"Personality: {personality_name}")
    
    # ========================================
    # 2. INITIAL AFFINITY STATE
    # ========================================
    
    print("\n\n2. INITIAL AFFINITY STATE")
    print("-" * 80)
    
    try:
        # Get initial affinity state
        initial_affinity = await affinity_manager.get_affinity(user_id, personality_name)
        
        if initial_affinity:
            print("Initial affinity state found:")
            print(f"   Level: {initial_affinity.current_level}")
            print(f"   Points: {initial_affinity.affinity_points}")
            print(f"   Total interactions: {initial_affinity.total_interactions}")
            print(f"   Positive interactions: {initial_affinity.positive_interactions}")
        else:
            print("No initial affinity state found (new user)")
            
    except Exception as e:
        print(f"ERROR getting initial affinity: {e}")
    
    # ========================================
    # 3. INTERACTION SIMULATION
    # ========================================
    
    print("\n\n3. INTERACTION SIMULATION")
    print("-" * 80)
    
    # Simulate various interactions
    interactions = [
        (InteractionType.POSITIVE, "User thanked the assistant"),
        (InteractionType.POSITIVE, "User gave positive feedback"),
        (InteractionType.NEUTRAL, "User asked a question"),
        (InteractionType.POSITIVE, "User expressed satisfaction"),
        (InteractionType.NEGATIVE, "User expressed frustration"),
        (InteractionType.POSITIVE, "User apologized and thanked"),
        (InteractionType.NEUTRAL, "User asked for help"),
        (InteractionType.POSITIVE, "User completed a task successfully"),
    ]
    
    print("Simulating interactions...")
    
    for i, (interaction_type, description) in enumerate(interactions, 1):
        try:
            print(f"\n   Interaction {i}: {description}")
            print(f"   Type: {interaction_type.value}")
            
            # Process interaction
            result = await affinity_manager.process_interaction(
                user_id, personality_name, interaction_type
            )
            
            print(f"   Result: {result}")
            
            # Get updated affinity
            current_affinity = await affinity_manager.get_affinity(user_id, personality_name)
            if current_affinity:
                print(f"   Current level: {current_affinity.current_level}")
                print(f"   Current points: {current_affinity.affinity_points}")
            
        except Exception as e:
            print(f"   ERROR in interaction {i}: {e}")
    
    # ========================================
    # 4. AFFINITY PROGRESSION
    # ========================================
    
    print("\n\n4. AFFINITY PROGRESSION")
    print("-" * 80)
    
    try:
        # Get final affinity state
        final_affinity = await affinity_manager.get_affinity(user_id, personality_name)
        
        if final_affinity:
            print("Final affinity state:")
            print(f"   Level: {final_affinity.current_level}")
            print(f"   Points: {final_affinity.affinity_points}")
            print(f"   Total interactions: {final_affinity.total_interactions}")
            print(f"   Positive interactions: {final_affinity.positive_interactions}")
            print(f"   Negative interactions: {final_affinity.negative_interactions}")
            print(f"   Neutral interactions: {final_affinity.neutral_interactions}")
            
            # Calculate progression
            if initial_affinity:
                level_change = final_affinity.current_level - initial_affinity.current_level
                points_change = final_affinity.affinity_points - initial_affinity.affinity_points
                print(f"\nProgression:")
                print(f"   Level change: {level_change:+d}")
                print(f"   Points change: {points_change:+d}")
            else:
                print(f"\nProgression: New user started at level {final_affinity.current_level}")
                
        else:
            print("ERROR: No final affinity state found")
            
    except Exception as e:
        print(f"ERROR getting final affinity: {e}")
    
    # ========================================
    # 5. LEVEL THRESHOLDS
    # ========================================
    
    print("\n\n5. LEVEL THRESHOLDS")
    print("-" * 80)
    
    try:
        # Show level thresholds
        thresholds = affinity_manager.get_level_thresholds()
        print("Affinity level thresholds:")
        
        for level, threshold in thresholds.items():
            print(f"   Level {level}: {threshold} points")
            
    except Exception as e:
        print(f"ERROR getting level thresholds: {e}")
    
    # ========================================
    # 6. AFFINITY STATISTICS
    # ========================================
    
    print("\n\n6. AFFINITY STATISTICS")
    print("-" * 80)
    
    try:
        # Get affinity statistics
        stats = await affinity_manager.get_affinity_stats(user_id, personality_name)
        
        if stats:
            print("Affinity statistics:")
            print(f"   Average interaction score: {stats.get('average_score', 'N/A')}")
            print(f"   Interaction frequency: {stats.get('frequency', 'N/A')}")
            print(f"   Relationship strength: {stats.get('strength', 'N/A')}")
            print(f"   Trust level: {stats.get('trust_level', 'N/A')}")
        else:
            print("No affinity statistics available")
            
    except Exception as e:
        print(f"ERROR getting affinity statistics: {e}")
    
    # ========================================
    # 7. AFFINITY HISTORY
    # ========================================
    
    print("\n\n7. AFFINITY HISTORY")
    print("-" * 80)
    
    try:
        # Get affinity history
        history = await affinity_manager.get_affinity_history(user_id, personality_name)
        
        if history:
            print(f"Affinity history ({len(history)} entries):")
            for entry in history[-5:]:  # Show last 5 entries
                print(f"   {entry}")
        else:
            print("No affinity history available")
            
    except Exception as e:
        print(f"ERROR getting affinity history: {e}")
    
    # ========================================
    # 8. MULTIPLE PERSONALITIES
    # ========================================
    
    print("\n\n8. MULTIPLE PERSONALITIES")
    print("-" * 80)
    
    # Test with different personality
    other_personality = "Creative Assistant"
    
    try:
        print(f"Testing with personality: {other_personality}")
        
        # Process interaction with different personality
        result = await affinity_manager.process_interaction(
            user_id, other_personality, InteractionType.POSITIVE
        )
        
        print(f"Interaction result: {result}")
        
        # Get affinity for different personality
        other_affinity = await affinity_manager.get_affinity(user_id, other_personality)
        
        if other_affinity:
            print(f"Affinity with {other_personality}:")
            print(f"   Level: {other_affinity.current_level}")
            print(f"   Points: {other_affinity.affinity_points}")
        else:
            print(f"No affinity state found for {other_personality}")
            
    except Exception as e:
        print(f"ERROR with multiple personalities: {e}")
    
    print("\n" + "=" * 80)
    print("Affinity system demonstration completed!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
