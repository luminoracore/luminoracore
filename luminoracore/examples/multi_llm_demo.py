#!/usr/bin/env python3
"""
Multi-LLM compilation demonstration for LuminoraCore.
"""

import sys
from pathlib import Path

# Add the parent directory to the path to import luminoracore
sys.path.insert(0, str(Path(__file__).parent.parent))

from luminoracore import Personality, PersonalityCompiler, LLMProvider


def demonstrate_multi_llm_compilation():
    """Demonstrate compilation for multiple LLM providers."""
    print("LuminoraCore Multi-LLM Compilation Example")
    print("=" * 60)
    
    # Load a personality
    print("\n1. Loading personality...")
    try:
        personality = Personality("luminoracore/luminoracore/personalities/dr_luna.json")
        print(f"✓ Loaded: {personality.persona.name}")
        print(f"  Archetype: {personality.core_traits.archetype}")
        print(f"  Compatibility: {', '.join(personality.persona.compatibility)}")
    except Exception as e:
        print(f"✗ Failed to load personality: {e}")
        return
    
    # Create compiler
    compiler = PersonalityCompiler()
    
    # Compile for all providers
    print("\n2. Compiling for all providers...")
    providers = [
        LLMProvider.OPENAI,
        LLMProvider.ANTHROPIC,
        LLMProvider.LLAMA,
        LLMProvider.MISTRAL,
        LLMProvider.COHERE,
        LLMProvider.GOOGLE,
        LLMProvider.UNIVERSAL
    ]
    
    results = {}
    for provider in providers:
        try:
            result = compiler.compile(personality, provider)
            results[provider] = result
            print(f"✓ {provider.value}: {result.token_estimate} tokens, {result.metadata['format']} format")
        except Exception as e:
            print(f"✗ {provider.value}: Failed - {e}")
    
    # Show detailed comparison
    print("\n3. Detailed Provider Comparison:")
    print("=" * 60)
    
    for provider, result in results.items():
        print(f"\n🔧 {provider.value.upper()}:")
        print(f"   Token estimate: {result.token_estimate}")
        print(f"   Format: {result.metadata['format']}")
        print(f"   Model: {result.metadata.get('model', 'N/A')}")
        print(f"   Temperature: {result.metadata.get('temperature', 'N/A')}")
        
        # Show prompt structure
        if isinstance(result.prompt, dict):
            print(f"   Prompt structure:")
            for key in result.prompt.keys():
                print(f"     • {key}")
        else:
            # Show text prompt snippet
            prompt_text = str(result.prompt)
            snippet = prompt_text[:200] + "..." if len(prompt_text) > 200 else prompt_text
            print(f"   Prompt snippet: {snippet}")
    
    # Show format differences
    print("\n4. Format Differences:")
    print("=" * 60)
    
    # OpenAI format
    if LLMProvider.OPENAI in results:
        openai_result = results[LLMProvider.OPENAI]
        print(f"\n📝 OpenAI Format (Messages):")
        if isinstance(openai_result.prompt, dict) and 'messages' in openai_result.prompt:
            messages = openai_result.prompt['messages']
            print(f"   Messages count: {len(messages)}")
            for i, msg in enumerate(messages):
                print(f"   Message {i+1}: role='{msg['role']}', content_length={len(msg['content'])}")
    
    # Anthropic format
    if LLMProvider.ANTHROPIC in results:
        anthropic_result = results[LLMProvider.ANTHROPIC]
        print(f"\n📝 Anthropic Format (XML):")
        if isinstance(anthropic_result.prompt, str):
            lines = anthropic_result.prompt.split('\n')
            print(f"   Lines: {len(lines)}")
            print(f"   Contains <system>: {'<system>' in anthropic_result.prompt}")
            print(f"   Contains <human>: {'<human>' in anthropic_result.prompt}")
            print(f"   Contains <assistant>: {'<assistant>' in anthropic_result.prompt}")
    
    # Llama format
    if LLMProvider.LLAMA in results:
        llama_result = results[LLMProvider.LLAMA]
        print(f"\n📝 Llama Format (Text):")
        if isinstance(llama_result.prompt, str):
            lines = llama_result.prompt.split('\n')
            print(f"   Lines: {len(lines)}")
            print(f"   Contains '### System:': {'### System:' in llama_result.prompt}")
            print(f"   Contains '### Human:': {'### Human:' in llama_result.prompt}")
            print(f"   Contains '### Assistant:': {'### Assistant:' in llama_result.prompt}")
    
    # Universal format
    if LLMProvider.UNIVERSAL in results:
        universal_result = results[LLMProvider.UNIVERSAL]
        print(f"\n📝 Universal Format (Portable):")
        if isinstance(universal_result.prompt, dict):
            print(f"   Keys: {list(universal_result.prompt.keys())}")
            if 'personality_info' in universal_result.prompt:
                info = universal_result.prompt['personality_info']
                print(f"   Personality info: {list(info.keys())}")
            if 'settings' in universal_result.prompt:
                settings = universal_result.prompt['settings']
                print(f"   Settings: {list(settings.keys())}")
    
    # Show token usage comparison
    print("\n5. Token Usage Comparison:")
    print("=" * 60)
    
    token_counts = [(provider.value, result.token_estimate) for provider, result in results.items()]
    token_counts.sort(key=lambda x: x[1], reverse=True)
    
    print("   Provider | Tokens | Efficiency")
    print("   ---------|--------|----------")
    for provider, tokens in token_counts:
        efficiency = "High" if tokens < 2000 else "Medium" if tokens < 4000 else "Low"
        print(f"   {provider:8} | {tokens:6} | {efficiency}")
    
    # Show compatibility check
    print("\n6. Compatibility Check:")
    print("=" * 60)
    
    for provider in providers:
        compatible = personality.is_compatible_with(provider.value)
        status = "✓ Compatible" if compatible else "✗ Not compatible"
        print(f"   {provider.value:12}: {status}")
    
    print(f"\n🎉 Multi-LLM compilation example completed!")
    print(f"   Successfully compiled for {len(results)} providers")


if __name__ == "__main__":
    demonstrate_multi_llm_compilation()
