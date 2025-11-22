#!/usr/bin/env python3
"""
Performance demonstration for LuminoraCore with caching and optimizations.
"""

import sys
import time
from pathlib import Path

# Add the parent directory to the path to import luminoracore
sys.path.insert(0, str(Path(__file__).parent.parent))

from luminoracore import Personality, PersonalityCompiler, LLMProvider, PersonalityValidator

def demonstrate_caching_performance():
    """Demonstrate the performance benefits of caching."""
    print("LuminoraCore Performance Demo")
    print("=" * 50)
    
    # Load a personality
    personality_path = Path(__file__).parent.parent / "luminoracore" / "personalities" / "dr_luna.json"
    personality = Personality(personality_path)
    
    # Create compiler with cache
    compiler = PersonalityCompiler(cache_size=64)
    
    # Test compilation without cache (first run)
    print("\nTesting compilation performance...")
    
    providers = [
        LLMProvider.OPENAI,
        LLMProvider.ANTHROPIC,
        LLMProvider.GOOGLE,
        LLMProvider.COHERE
    ]
    
    # First compilation (cache miss)
    start_time = time.time()
    for provider in providers:
        result = compiler.compile(personality, provider)
        print(f"  {provider.value}: {result.token_estimate} tokens")
    first_run_time = time.time() - start_time
    
    # Second compilation (cache hit)
    start_time = time.time()
    for provider in providers:
        result = compiler.compile(personality, provider)
        print(f"  {provider.value}: {result.token_estimate} tokens (cached)")
    second_run_time = time.time() - start_time
    
    # Show cache statistics
    stats = compiler.get_cache_stats()
    print(f"\nCache Statistics:")
    print(f"  Cache hits: {stats['cache_hits']}")
    print(f"  Cache misses: {stats['cache_misses']}")
    print(f"  Hit rate: {stats['hit_rate']}%")
    print(f"  Cache size: {stats['cache_size']}/{stats['max_cache_size']}")
    
    # Performance improvement
    if first_run_time > 0:
        improvement = ((first_run_time - second_run_time) / first_run_time) * 100
        print(f"\nPerformance Improvement: {improvement:.1f}%")
    else:
        improvement = 0
        print(f"\nPerformance Improvement: {improvement:.1f}% (cached)")
    print(f"  First run: {first_run_time:.3f}s")
    print(f"  Second run: {second_run_time:.3f}s")

def demonstrate_validation_performance():
    """Demonstrate performance validation features."""
    print("\nPerformance Validation Demo")
    print("=" * 50)
    
    # Create validator with performance checks enabled
    validator = PersonalityValidator(enable_performance_checks=True)
    
    # Load personality
    personality_path = Path(__file__).parent.parent / "luminoracore" / "personalities" / "dr_luna.json"
    
    # Validate with performance checks
    result = validator.validate(personality_path)
    
    print(f"Validation Result: {'[OK] Valid' if result.is_valid else '[ERROR] Invalid'}")
    
    if result.warnings:
        print(f"\nWarnings ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"  • {warning}")
    
    if result.suggestions:
        print(f"\nSuggestions ({len(result.suggestions)}):")
        for suggestion in result.suggestions:
            print(f"  • {suggestion}")

def demonstrate_compilation_all_providers():
    """Demonstrate compilation for all providers with performance metrics."""
    print("\nMulti-Provider Compilation Demo")
    print("=" * 50)
    
    personality_path = Path(__file__).parent.parent / "luminoracore" / "personalities" / "dr_luna.json"
    personality = Personality(personality_path)
    
    compiler = PersonalityCompiler(cache_size=128)
    
    # Compile for all providers
    start_time = time.time()
    results = compiler.compile_all_providers(personality)
    total_time = time.time() - start_time
    
    print(f"Compiled for {len(results)} providers in {total_time:.3f}s")
    print(f"Average time per provider: {total_time/len(results):.3f}s")
    
    for provider, result in results.items():
        print(f"  {provider.value}: {result.token_estimate} tokens")
    
    # Show final cache stats
    stats = compiler.get_cache_stats()
    print(f"\nFinal cache hit rate: {stats['hit_rate']}%")

if __name__ == "__main__":
    try:
        demonstrate_caching_performance()
        demonstrate_validation_performance()
        demonstrate_compilation_all_providers()
        
        print("\nPerformance demo completed successfully!")
        
    except Exception as e:
        print(f"\n[ERROR] Demo failed: {e}")
        import traceback
        traceback.print_exc()
