#!/usr/bin/env python3
"""
Basic usage example for LuminoraCore.
"""

import sys
from pathlib import Path

# Add the parent directory to the path to import luminoracore
sys.path.insert(0, str(Path(__file__).parent.parent))

from luminoracore import Personality, PersonalityValidator, PersonalityCompiler, LLMProvider, find_personality_file


def main():
    """Demonstrate basic LuminoraCore usage."""
    print("LuminoraCore Basic Usage Example")
    print("=" * 50)
    
    # Load a personality
    print("\n1. Loading a personality...")
    try:
        # Use find_personality_file for robust path resolution
        personality_path = find_personality_file("Dr. Luna") or Path(__file__).parent.parent / "luminoracore" / "personalities" / "dr_luna.json"
        personality = Personality(personality_path)
        print(f"[OK] Loaded personality: {personality.persona.name}")
        print(f"  Description: {personality.persona.description}")
        print(f"  Archetype: {personality.core_traits.archetype}")
        print(f"  Temperament: {personality.core_traits.temperament}")
    except Exception as e:
        print(f"[ERROR] Failed to load personality: {e}")
        return
    
    # Validate the personality
    print("\n2. Validating personality...")
    try:
        validator = PersonalityValidator()
        result = validator.validate(personality)
        
        if result.is_valid:
            print("[OK] Personality validation passed")
            if result.warnings:
                print(f"  Warnings: {len(result.warnings)}")
            if result.suggestions:
                print(f"  Suggestions: {len(result.suggestions)}")
        else:
            print("[ERROR] Personality validation failed")
            for error in result.errors:
                print(f"  Error: {error}")
            return
    except Exception as e:
        print(f"[ERROR] Validation failed: {e}")
        return
    
    # Compile for different providers
    print("\n3. Compiling for different providers...")
    try:
        compiler = PersonalityCompiler()
        
        # Test compilation for OpenAI
        openai_result = compiler.compile(personality, LLMProvider.OPENAI)
        print(f"[OK] OpenAI compilation successful")
        print(f"  Token estimate: {openai_result.token_estimate}")
        print(f"  Format: {openai_result.metadata['format']}")
        
        # Test compilation for Anthropic
        anthropic_result = compiler.compile(personality, LLMProvider.ANTHROPIC)
        print(f"[OK] Anthropic compilation successful")
        print(f"  Token estimate: {anthropic_result.token_estimate}")
        print(f"  Format: {anthropic_result.metadata['format']}")
        
        # Test compilation for Llama
        llama_result = compiler.compile(personality, LLMProvider.LLAMA)
        print(f"[OK] Llama compilation successful")
        print(f"  Token estimate: {llama_result.token_estimate}")
        print(f"  Format: {llama_result.metadata['format']}")
        
    except Exception as e:
        print(f"[ERROR] Compilation failed: {e}")
        return
    
    # Display personality information
    print("\n4. Personality Information:")
    print(f"  Name: {personality.persona.name}")
    print(f"  Version: {personality.persona.version}")
    print(f"  Author: {personality.persona.author}")
    print(f"  Language: {personality.persona.language}")
    print(f"  Tags: {', '.join(personality.persona.tags)}")
    print(f"  Compatibility: {', '.join(personality.persona.compatibility)}")
    
    # Display linguistic profile
    print("\n5. Linguistic Profile:")
    print(f"  Tone: {', '.join(personality.linguistic_profile.tone)}")
    print(f"  Syntax: {personality.linguistic_profile.syntax}")
    print(f"  Vocabulary: {', '.join(personality.linguistic_profile.vocabulary[:5])}...")
    if personality.linguistic_profile.fillers:
        print(f"  Fillers: {', '.join(personality.linguistic_profile.fillers[:3])}...")
    
    # Display behavioral rules
    print("\n6. Behavioral Rules:")
    for i, rule in enumerate(personality.behavioral_rules[:3], 1):
        print(f"  {i}. {rule}")
    
    # Display examples
    if personality.examples and personality.examples.sample_responses:
        print("\n7. Example Interactions:")
        for i, example in enumerate(personality.examples.sample_responses[:2], 1):
            print(f"  Example {i}:")
            print(f"    Input: {example.input}")
            print(f"    Output: {example.output}")
    
    print("\nBasic usage example completed successfully!")


if __name__ == "__main__":
    main()
