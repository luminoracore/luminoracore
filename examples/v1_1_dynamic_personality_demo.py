"""
LuminoraCore v1.1 - Dynamic Personality Compilation Demo

Demonstrates how personality changes based on affinity level.
"""

import asyncio
from luminoracore.core.personality_v1_1 import PersonalityV11Extensions
from luminoracore.core.compiler_v1_1 import DynamicPersonalityCompiler


async def main():
    print("🎭 LuminoraCore v1.1 - Dynamic Personality Demo\n")
    print("=" * 60)
    
    # Sample personality with hierarchical levels
    personality_dict = {
        "persona": {
            "name": "Alicia",
            "tagline": "Your adaptive AI companion"
        },
        "advanced_parameters": {
            "empathy": 0.9,
            "formality": 0.3,
            "humor": 0.6
        },
        "hierarchical_config": {
            "enabled": True,
            "relationship_levels": [
                {
                    "name": "stranger",
                    "affinity_range": [0, 20],
                    "description": "Initial interactions, formal and cautious",
                    "modifiers": {
                        "advanced_parameters": {
                            "formality": 0.3,  # More formal
                            "humor": -0.2  # Less humor
                        }
                    }
                },
                {
                    "name": "friend",
                    "affinity_range": [41, 60],
                    "description": "Comfortable, more casual",
                    "modifiers": {
                        "advanced_parameters": {
                            "formality": -0.2,  # Less formal
                            "humor": 0.2  # More humor
                        }
                    }
                },
                {
                    "name": "close_friend",
                    "affinity_range": [61, 80],
                    "description": "Very comfortable, playful",
                    "modifiers": {
                        "advanced_parameters": {
                            "formality": -0.3,  # Much less formal
                            "humor": 0.3  # Much more humor
                        }
                    }
                }
            ]
        }
    }
    
    # Parse v1.1 extensions
    extensions = PersonalityV11Extensions.from_personality_dict(personality_dict)
    
    print("\n📊 Personality Configuration:")
    print(f"   Name: {personality_dict['persona']['name']}")
    print(f"   Hierarchical: {extensions.has_hierarchical()}")
    print(f"   Levels: {len(extensions.hierarchical_config.relationship_levels)}")
    
    # Create compiler
    compiler = DynamicPersonalityCompiler(personality_dict, extensions)
    
    # Compile at different affinity levels
    affinity_levels = [
        (5, "stranger"),
        (50, "friend"),
        (70, "close_friend")
    ]
    
    print("\n🔄 Compiling personality at different affinity levels:")
    print("=" * 60)
    
    base_empathy = personality_dict["advanced_parameters"]["empathy"]
    base_formality = personality_dict["advanced_parameters"]["formality"]
    base_humor = personality_dict["advanced_parameters"]["humor"]
    
    print(f"\n📌 Base Parameters:")
    print(f"   Empathy: {base_empathy}")
    print(f"   Formality: {base_formality}")
    print(f"   Humor: {base_humor}")
    
    for affinity, expected_level in affinity_levels:
        print(f"\n🎯 Affinity: {affinity}/100 ({expected_level})")
        print("-" * 60)
        
        # Compile personality
        compiled = compiler.compile(affinity_points=affinity)
        
        # Show modified parameters
        params = compiled["advanced_parameters"]
        print(f"   Empathy: {params['empathy']:.2f} (Δ {params['empathy']-base_empathy:+.2f})")
        print(f"   Formality: {params['formality']:.2f} (Δ {params['formality']-base_formality:+.2f})")
        print(f"   Humor: {params['humor']:.2f} (Δ {params['humor']-base_humor:+.2f})")
        
        # Show effect
        if expected_level == "stranger":
            print("\n   Effect: More formal, reserved, professional")
        elif expected_level == "friend":
            print("\n   Effect: Casual, friendly, comfortable")
        elif expected_level == "close_friend":
            print("\n   Effect: Very casual, playful, intimate")
    
    print("\n" + "=" * 60)
    print("✅ Demo completed!")


if __name__ == "__main__":
    asyncio.run(main())

