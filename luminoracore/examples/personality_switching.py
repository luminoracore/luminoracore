#!/usr/bin/env python3
"""
Personality switching example for LuminoraCore.
"""

import sys
from pathlib import Path

# Add the parent directory to the path to import luminoracore
sys.path.insert(0, str(Path(__file__).parent.parent))

from luminoracore import Personality, PersonalityCompiler, LLMProvider


def demonstrate_personality_switching():
    """Demonstrate switching between different personalities."""
    print("🔄 LuminoraCore Personality Switching Example")
    print("=" * 60)
    
    # Load multiple personalities
    personalities = {}
    personality_files = [
        "luminoracore/luminoracore/personalities/dr_luna.json",
        "luminoracore/luminoracore/personalities/captain_hook.json", 
        "luminoracore/luminoracore/personalities/grandma_hope.json",
        "luminoracore/luminoracore/personalities/marcus_sarcastic.json"
    ]
    
    print("\n1. Loading personalities...")
    for file_path in personality_files:
        try:
            personality = Personality(file_path)
            personalities[personality.persona.name] = personality
            print(f"✓ Loaded: {personality.persona.name} ({personality.core_traits.archetype})")
        except Exception as e:
            print(f"✗ Failed to load {file_path}: {e}")
    
    if not personalities:
        print("✗ No personalities loaded successfully")
        return
    
    # Compile each personality for OpenAI
    print("\n2. Compiling personalities for OpenAI...")
    compiler = PersonalityCompiler()
    compiled_personalities = {}
    
    for name, personality in personalities.items():
        try:
            result = compiler.compile(personality, LLMProvider.OPENAI)
            compiled_personalities[name] = result
            print(f"✓ Compiled: {name} ({result.token_estimate} tokens)")
        except Exception as e:
            print(f"✗ Failed to compile {name}: {e}")
    
    # Demonstrate different responses to the same question
    test_question = "Can you help me understand how photosynthesis works?"
    
    print(f"\n3. Testing responses to: '{test_question}'")
    print("=" * 60)
    
    for name, personality in personalities.items():
        print(f"\n🎭 {name} ({personality.core_traits.archetype}):")
        print(f"   Temperament: {personality.core_traits.temperament}")
        print(f"   Communication: {personality.core_traits.communication_style}")
        
        # Show trigger response for greeting
        if personality.trigger_responses and personality.trigger_responses.on_greeting:
            print(f"   Greeting: {personality.trigger_responses.on_greeting[0]}")
        
        # Show vocabulary
        print(f"   Vocabulary: {', '.join(personality.linguistic_profile.vocabulary[:3])}")
        
        # Show behavioral rule
        if personality.behavioral_rules:
            print(f"   Behavior: {personality.behavioral_rules[0]}")
    
    # Show compilation differences
    print(f"\n4. Compilation Differences:")
    print("=" * 60)
    
    for name, result in compiled_personalities.items():
        print(f"\n📝 {name}:")
        print(f"   Token estimate: {result.token_estimate}")
        print(f"   Temperature: {result.metadata.get('temperature', 'N/A')}")
        
        # Show a snippet of the compiled prompt
        if isinstance(result.prompt, dict) and 'messages' in result.prompt:
            content = result.prompt['messages'][0]['content']
            snippet = content[:200] + "..." if len(content) > 200 else content
            print(f"   Prompt snippet: {snippet}")
    
    print(f"\n🎉 Personality switching example completed!")
    print(f"   Loaded {len(personalities)} personalities")
    print(f"   Compiled {len(compiled_personalities)} prompts")


if __name__ == "__main__":
    demonstrate_personality_switching()
