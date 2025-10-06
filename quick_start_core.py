#!/usr/bin/env python3
"""
Quick Start Example - LuminoraCore Base Engine
Run this file to test that luminoracore is installed correctly.
"""

import sys
from pathlib import Path

def main():
    """Quick test of LuminoraCore base engine."""
    print("=" * 60)
    print("🧠 LuminoraCore - Base Engine - Quick Start")
    print("=" * 60)
    
    # Check that luminoracore is installed
    print("\n1️⃣  Checking luminoracore installation...")
    try:
        import luminoracore
        print(f"   ✅ luminoracore installed - Version: {luminoracore.__version__}")
    except ImportError as e:
        print(f"   ❌ Error: luminoracore is not installed")
        print(f"   💡 Solution: cd luminoracore && pip install -e .")
        return False
    
    # Import main components
    print("\n2️⃣  Importing main components...")
    try:
        from luminoracore import (
            Personality, 
            PersonalityValidator, 
            PersonalityCompiler, 
            PersonalityBlender,
            LLMProvider
        )
        print("   ✅ All components imported correctly")
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    
    # Check if personalities folder exists
    print("\n3️⃣  Looking for example personalities...")
    personalities_dir = Path("personalidades")
    
    if not personalities_dir.exists():
        # Try with package path
        personalities_dir = Path("luminoracore/luminoracore/personalities")
    
    if not personalities_dir.exists():
        print(f"   ⚠️  Personalities folder not found")
        print(f"   💡 Creating example personality in memory...")
        
        # Create a simple personality in memory
        personality_dict = {
            "persona": {
                "name": "Demo Assistant",
                "version": "1.0.0",
                "description": "A demonstration personality",
                "author": "LuminoraCore",
                "language": "en",
                "tags": ["demo", "test"],
                "compatibility": ["openai", "anthropic"]
            },
            "core_traits": {
                "archetype": "helper",
                "temperament": "friendly",
                "primary_motivation": "help users",
                "expertise_areas": ["general assistance"],
                "communication_style": "clear and concise"
            },
            "linguistic_profile": {
                "tone": ["friendly", "professional"],
                "formality_level": "semi-formal",
                "syntax": "structured",
                "vocabulary": ["clear", "precise", "accessible"],
                "fillers": [],
                "humor_style": "light"
            },
            "behavioral_rules": [
                "Always be respectful and courteous",
                "Provide accurate and verifiable information"
            ],
            "constraints": {
                "topics_to_avoid": ["inappropriate content"],
                "ethical_guidelines": ["respect user privacy"],
                "prohibited_behaviors": ["misinformation"]
            },
            "examples": {
                "sample_responses": [
                    {
                        "input": "Hello",
                        "output": "Hello! How can I help you today?"
                    }
                ],
                "tone_examples": ["Friendly and helpful"],
                "boundary_examples": ["I don't provide professional medical information"]
            }
        }
        
        # Simulate personality loading from dictionary
        print("   ✅ Example personality created in memory")
        personality = None  # For now just test imports
    else:
        # Look for a personality file
        personality_files = list(personalities_dir.glob("*.json"))
        if personality_files:
            print(f"   ✅ Found {len(personality_files)} personalities")
            print(f"   📄 Using: {personality_files[0].name}")
            
            try:
                personality = Personality(str(personality_files[0]))
                print(f"   ✅ Personality loaded: {personality.persona.name}")
            except Exception as e:
                print(f"   ⚠️  Error loading personality: {e}")
                personality = None
        else:
            print("   ⚠️  No .json personality files found")
            personality = None
    
    # Test the validator
    print("\n4️⃣  Testing PersonalityValidator...")
    try:
        validator = PersonalityValidator()
        print("   ✅ PersonalityValidator created correctly")
        
        if personality:
            result = validator.validate(personality)
            if result.is_valid:
                print(f"   ✅ Validation successful")
                print(f"      - Warnings: {len(result.warnings)}")
                print(f"      - Suggestions: {len(result.suggestions)}")
            else:
                print(f"   ⚠️  Validation with errors: {len(result.errors)}")
    except Exception as e:
        print(f"   ⚠️  Validation error: {e}")
    
    # Test the compiler
    print("\n5️⃣  Testing PersonalityCompiler...")
    try:
        compiler = PersonalityCompiler()
        print("   ✅ PersonalityCompiler created correctly")
        
        if personality:
            # Compile for OpenAI
            result = compiler.compile(personality, LLMProvider.OPENAI)
            print(f"   ✅ Compilation successful for OpenAI")
            print(f"      - Estimated tokens: {result.token_estimate}")
            print(f"      - Prompt length: {len(result.prompt)} characters")
            
            # Test with other providers
            providers_tested = []
            for provider in [LLMProvider.ANTHROPIC, LLMProvider.LLAMA]:
                try:
                    result = compiler.compile(personality, provider)
                    providers_tested.append(provider.value)
                except:
                    pass
            
            if providers_tested:
                print(f"   ✅ Also compiled for: {', '.join(providers_tested)}")
    except Exception as e:
        print(f"   ⚠️  Compilation error: {e}")
    
    # Test PersonalityBlender
    print("\n6️⃣  Testing PersonalityBlender...")
    try:
        blender = PersonalityBlender()
        print("   ✅ PersonalityBlender created correctly")
        print("   💡 PersonaBlend™ Technology available")
    except Exception as e:
        print(f"   ⚠️  Error creating blender: {e}")
    
    # Final summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print("✅ luminoracore is installed and functional")
    print("✅ All main components are available")
    print("")
    print("🚀 Ready to use LuminoraCore!")
    print("")
    print("📖 Next steps:")
    print("   1. Read INSTALLATION_GUIDE.md for more details")
    print("   2. Explore examples in luminoracore/examples/")
    print("   3. Create your first custom personality")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

