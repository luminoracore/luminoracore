"""
LuminoraCore v1.1 - Affinity System Demo (Corrected)

Demonstrates the actual AffinityManager methods available.
"""

import asyncio
from luminoracore.core.relationship import AffinityManager, AffinityState


def main():
    """Corrected affinity system demonstration."""
    
    print("=" * 80)
    print("LuminoraCore v1.1 - Affinity System Demo (Corrected)")
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
    # 2. AFFINITY STATE CREATION
    # ========================================
    
    print("\n\n2. AFFINITY STATE CREATION")
    print("-" * 80)
    
    try:
        # Create initial affinity state
        initial_state = AffinityState(
            user_id=user_id,
            personality_name=personality_name,
            affinity_points=0,
            current_level="stranger"
        )
        
        print("Initial affinity state created:")
        print(f"   User ID: {initial_state.user_id}")
        print(f"   Personality: {initial_state.personality_name}")
        print(f"   Points: {initial_state.affinity_points}")
        print(f"   Level: {initial_state.current_level}")
        print(f"   Total messages: {initial_state.total_messages}")
        
    except Exception as e:
        print(f"ERROR creating affinity state: {e}")
        return
    
    # ========================================
    # 3. POINTS CALCULATION
    # ========================================
    
    print("\n\n3. POINTS CALCULATION")
    print("-" * 80)
    
    # Test different interaction types
    interaction_types = [
        "very_positive",
        "positive", 
        "neutral",
        "negative",
        "very_negative"
    ]
    
    print("Testing points calculation for different interaction types:")
    
    for interaction_type in interaction_types:
        try:
            points_delta = affinity_manager.calculate_points_delta(interaction_type)
            print(f"   {interaction_type}: {points_delta:+d} points")
            
        except Exception as e:
            print(f"   {interaction_type}: ERROR - {e}")
    
    # Test with message length
    print("\nTesting points calculation with message length:")
    
    try:
        # Short message
        short_points = affinity_manager.calculate_points_delta("positive", message_length=50)
        print(f"   Short message (50 chars): {short_points:+d} points")
        
        # Long message
        long_points = affinity_manager.calculate_points_delta("positive", message_length=150)
        print(f"   Long message (150 chars): {long_points:+d} points")
        
    except Exception as e:
        print(f"ERROR with message length calculation: {e}")
    
    # ========================================
    # 4. LEVEL DETERMINATION
    # ========================================
    
    print("\n\n4. LEVEL DETERMINATION")
    print("-" * 80)
    
    # Test different point values
    test_points = [0, 15, 30, 50, 70, 90, 100]
    
    print("Testing level determination:")
    
    for points in test_points:
        try:
            level = affinity_manager.determine_level(points)
            print(f"   {points:3d} points: {level}")
            
        except Exception as e:
            print(f"   {points:3d} points: ERROR - {e}")
    
    # ========================================
    # 5. AFFINITY STATE UPDATES
    # ========================================
    
    print("\n\n5. AFFINITY STATE UPDATES")
    print("-" * 80)
    
    # Simulate interactions
    interactions = [
        ("positive", 2),
        ("positive", 2), 
        ("neutral", 1),
        ("positive", 2),
        ("negative", -2),
        ("positive", 2),
        ("neutral", 1),
        ("very_positive", 5),
    ]
    
    print("Simulating interactions:")
    
    current_state = initial_state
    
    for i, (interaction_type, expected_delta) in enumerate(interactions, 1):
        try:
            print(f"\n   Interaction {i}: {interaction_type}")
            
            # Calculate points delta
            points_delta = affinity_manager.calculate_points_delta(interaction_type)
            print(f"   Points delta: {points_delta:+d}")
            
            # Update state
            old_level = current_state.current_level
            old_points = current_state.affinity_points
            
            current_state = affinity_manager.update_affinity_state(current_state, points_delta)
            
            print(f"   Points: {old_points} → {current_state.affinity_points}")
            print(f"   Level: {old_level} → {current_state.current_level}")
            print(f"   Total messages: {current_state.total_messages}")
            
            if old_level != current_state.current_level:
                print(f"   *** LEVEL UP! ***")
            
        except Exception as e:
            print(f"   ERROR in interaction {i}: {e}")
    
    # ========================================
    # 6. LEVEL PROGRESS
    # ========================================
    
    print("\n\n6. LEVEL PROGRESS")
    print("-" * 80)
    
    try:
        progress = affinity_manager.get_level_progress(current_state)
        
        print("Current level progress:")
        print(f"   Current level: {progress['current_level']}")
        print(f"   Points: {progress['points']}")
        print(f"   Progress in level: {progress['progress_in_level']:.1%}")
        print(f"   Points to next level: {progress['points_to_next_level']}")
        print(f"   Next level: {progress['next_level']}")
        
    except Exception as e:
        print(f"ERROR getting level progress: {e}")
    
    # ========================================
    # 7. CUSTOM LEVEL DEFINITIONS
    # ========================================
    
    print("\n\n7. CUSTOM LEVEL DEFINITIONS")
    print("-" * 80)
    
    # Test with custom level definitions
    custom_levels = [
        {"name": "beginner", "min": 0, "max": 25},
        {"name": "intermediate", "min": 26, "max": 50},
        {"name": "advanced", "min": 51, "max": 75},
        {"name": "expert", "min": 76, "max": 100}
    ]
    
    try:
        print("Testing with custom level definitions:")
        
        for points in [20, 40, 60, 80]:
            level = affinity_manager.determine_level(points, custom_levels)
            print(f"   {points} points: {level}")
        
        # Test progress with custom levels
        custom_state = AffinityState(
            user_id="custom_user",
            personality_name="Custom Assistant",
            affinity_points=65,
            current_level="advanced"
        )
        
        custom_progress = affinity_manager.get_level_progress(custom_state, custom_levels)
        
        print(f"\nCustom level progress:")
        print(f"   Current level: {custom_progress['current_level']}")
        print(f"   Points: {custom_progress['points']}")
        print(f"   Progress in level: {custom_progress['progress_in_level']:.1%}")
        print(f"   Next level: {custom_progress['next_level']}")
        
    except Exception as e:
        print(f"ERROR with custom level definitions: {e}")
    
    # ========================================
    # 8. EDGE CASES
    # ========================================
    
    print("\n\n8. EDGE CASES")
    print("-" * 80)
    
    try:
        # Test boundary conditions
        boundary_state = AffinityState(
            user_id="boundary_user",
            personality_name="Boundary Assistant",
            affinity_points=0,
            current_level="stranger"
        )
        
        print("Testing boundary conditions:")
        
        # Test negative points (should be clamped)
        negative_state = affinity_manager.update_affinity_state(boundary_state, -50)
        print(f"   Negative delta (-50): {negative_state.affinity_points} points")
        
        # Test excessive positive points (should be clamped)
        positive_state = affinity_manager.update_affinity_state(boundary_state, 150)
        print(f"   Positive delta (+150): {positive_state.affinity_points} points")
        
        # Test invalid affinity state creation
        try:
            invalid_state = AffinityState(
                user_id="invalid_user",
                personality_name="Invalid Assistant",
                affinity_points=150  # Invalid: > 100
            )
            print("   Invalid state creation: ERROR - should have failed")
        except ValueError as e:
            print(f"   Invalid state creation: Correctly rejected - {e}")
        
    except Exception as e:
        print(f"ERROR with edge cases: {e}")
    
    print("\n" + "=" * 80)
    print("Affinity system demonstration completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
