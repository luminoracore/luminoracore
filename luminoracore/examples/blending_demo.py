#!/usr/bin/env python3
"""
Personality blending demonstration for LuminoraCore.
"""

import sys
from pathlib import Path

# Add the parent directory to the path to import luminoracore
sys.path.insert(0, str(Path(__file__).parent.parent))

from luminoracore import Personality, PersonaBlend


def demonstrate_personality_blending():
    """Demonstrate blending different personalities."""
    print("🎨 LuminoraCore Personality Blending Example")
    print("=" * 60)
    
    # Load personalities for blending
    print("\n1. Loading personalities for blending...")
    personalities = {}
    personality_files = [
        "personalities/dr_luna.json",
        "personalities/captain_hook.json",
        "personalities/grandma_hope.json"
    ]
    
    for file_path in personality_files:
        try:
            personality = Personality(file_path)
            personalities[personality.persona.name] = personality
            print(f"✓ Loaded: {personality.persona.name}")
            print(f"  Archetype: {personality.core_traits.archetype}")
            print(f"  Temperament: {personality.core_traits.temperament}")
        except Exception as e:
            print(f"✗ Failed to load {file_path}: {e}")
    
    if len(personalities) < 2:
        print("✗ Need at least 2 personalities for blending")
        return
    
    # Create blender
    blender = PersonaBlend()
    
    # Test different blending strategies
    print("\n2. Testing different blending strategies...")
    
    # Strategy 1: Weighted Average (equal weights)
    print("\n🎯 Strategy 1: Weighted Average (equal weights)")
    try:
        personality_list = list(personalities.values())
        weights = {name: 1.0 for name in personalities.keys()}
        
        result1 = blender.blend(personality_list, weights, strategy="weighted_average")
        blended1 = result1.blended_personality
        
        print(f"✓ Blended personality: {blended1.persona.name}")
        print(f"  Archetype: {blended1.core_traits.archetype}")
        print(f"  Temperament: {blended1.core_traits.temperament}")
        print(f"  Communication: {blended1.core_traits.communication_style}")
        print(f"  Tone: {', '.join(blended1.linguistic_profile.tone[:3])}")
        print(f"  Vocabulary: {', '.join(blended1.linguistic_profile.vocabulary[:5])}")
        
    except Exception as e:
        print(f"✗ Blending failed: {e}")
    
    # Strategy 2: Dominant (Dr. Luna dominant)
    print("\n🎯 Strategy 2: Dominant (Dr. Luna dominant)")
    try:
        weights = {
            "Dr. Luna": 0.7,
            "Captain Hook Digital": 0.2,
            "Grandma Hope": 0.1
        }
        
        result2 = blender.blend(personality_list, weights, strategy="dominant")
        blended2 = result2.blended_personality
        
        print(f"✓ Blended personality: {blended2.persona.name}")
        print(f"  Archetype: {blended2.core_traits.archetype}")
        print(f"  Temperament: {blended2.core_traits.temperament}")
        print(f"  Communication: {blended2.core_traits.communication_style}")
        print(f"  Tone: {', '.join(blended2.linguistic_profile.tone[:3])}")
        print(f"  Vocabulary: {', '.join(blended2.linguistic_profile.vocabulary[:5])}")
        
    except Exception as e:
        print(f"✗ Blending failed: {e}")
    
    # Strategy 3: Hybrid
    print("\n🎯 Strategy 3: Hybrid")
    try:
        weights = {name: 1.0 for name in personalities.keys()}
        
        result3 = blender.blend(personality_list, weights, strategy="hybrid")
        blended3 = result3.blended_personality
        
        print(f"✓ Blended personality: {blended3.persona.name}")
        print(f"  Archetype: {blended3.core_traits.archetype}")
        print(f"  Temperament: {blended3.core_traits.temperament}")
        print(f"  Communication: {blended3.core_traits.communication_style}")
        print(f"  Tone: {', '.join(blended3.linguistic_profile.tone[:3])}")
        print(f"  Vocabulary: {', '.join(blended3.linguistic_profile.vocabulary[:5])}")
        
    except Exception as e:
        print(f"✗ Blending failed: {e}")
    
    # Show blending details
    print("\n3. Blending Details:")
    print("=" * 60)
    
    if 'result1' in locals():
        print(f"\n📊 Weighted Average Blend:")
        print(f"   Source personalities: {', '.join(result1.blend_info['source_personalities'])}")
        print(f"   Weights: {result1.blend_info['weights']}")
        print(f"   Strategy: {result1.blend_info['strategy']}")
    
    if 'result2' in locals():
        print(f"\n📊 Dominant Blend:")
        print(f"   Source personalities: {', '.join(result2.blend_info['source_personalities'])}")
        print(f"   Weights: {result2.blend_info['weights']}")
        print(f"   Strategy: {result2.blend_info['strategy']}")
    
    # Show advanced parameters comparison
    print("\n4. Advanced Parameters Comparison:")
    print("=" * 60)
    
    for name, personality in personalities.items():
        if personality.advanced_parameters:
            params = personality.advanced_parameters
            print(f"\n🔧 {name}:")
            print(f"   Verbosity: {params.verbosity}")
            print(f"   Formality: {params.formality}")
            print(f"   Humor: {params.humor}")
            print(f"   Empathy: {params.empathy}")
            print(f"   Creativity: {params.creativity}")
            print(f"   Directness: {params.directness}")
    
    # Show blended parameters
    if 'result1' in locals() and result1.blended_personality.advanced_parameters:
        params = result1.blended_personality.advanced_parameters
        print(f"\n🔧 Blended (Weighted Average):")
        print(f"   Verbosity: {params.verbosity}")
        print(f"   Formality: {params.formality}")
        print(f"   Humor: {params.humor}")
        print(f"   Empathy: {params.empathy}")
        print(f"   Creativity: {params.creativity}")
        print(f"   Directness: {params.directness}")
    
    print(f"\n🎉 Personality blending example completed!")
    print(f"   Successfully blended {len(personalities)} personalities")


if __name__ == "__main__":
    demonstrate_personality_blending()
