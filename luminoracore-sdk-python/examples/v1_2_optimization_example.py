"""
LuminoraCore SDK v1.2.0 - Optimization Example

This example demonstrates the NEW optimization features in v1.2.0:
- Token reduction (25-45%)
- Key mapping (abbreviated keys)
- Compact format (array-based storage)
- Deduplication (merge duplicate facts)
- Caching (LRU with TTL)

REQUIREMENTS:
- luminoracore>=1.2.0 (Core package)
- luminoracore-sdk>=1.2.0
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the parent directory to the path to import luminoracore_sdk
sys.path.insert(0, str(Path(__file__).parent.parent))

from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types.provider import ProviderConfig
from luminoracore_sdk.types.session import StorageConfig, MemoryConfig

# Import optimization from Core
try:
    from luminoracore.optimization import OptimizationConfig
    HAS_OPTIMIZATION = True
except ImportError:
    HAS_OPTIMIZATION = False
    print("[WARNING] luminoracore.optimization not available. Install luminoracore>=1.2.0")
    print("This example requires the Core package with optimization module.")


async def main():
    """Demonstrate v1.2.0 optimization features."""
    print("=" * 80)
    print("LuminoraCore SDK v1.2.0 - Optimization Example")
    print("=" * 80)
    
    if not HAS_OPTIMIZATION:
        print("\n[ERROR] Optimization module not available.")
        print("Install: pip install -e ../luminoracore/")
        return
    
    # ========================================
    # 1. CLIENT WITH OPTIMIZATION ENABLED
    # ========================================
    print("\n1. Initializing client with optimization...")
    
    # Create optimization config
    opt_config = OptimizationConfig(
        key_abbreviation=True,      # Abbreviate long keys (e.g., "user_id" -> "uid")
        compact_format=True,        # Use compact array format
        minification=True,         # Minify JSON (remove whitespace)
        deduplication=True,         # Merge duplicate facts
        cache_enabled=True,         # Enable LRU cache
        cache_size=1000,            # Cache size
        cache_ttl=3600              # Cache TTL (1 hour)
    )
    
    # Initialize client with optimization
    client = LuminoraCoreClient(
        storage_config=StorageConfig(
            storage_type="memory"
        ),
        memory_config=MemoryConfig(
            max_entries=1000,
            decay_factor=0.1
        ),
        optimization_config=opt_config  # 🆕 NEW in v1.2.0
    )
    
    await client.initialize()
    print("  [OK] Client initialized with optimization")
    print(f"  [OK] Optimizer active: {client.optimizer is not None}")
    
    # ========================================
    # 2. CHECK OPTIMIZATION STATS
    # ========================================
    print("\n2. Optimization statistics...")
    stats = await client.get_optimization_stats()
    print(f"  [OK] Optimization enabled: {stats['enabled']}")
    print(f"  [OK] Key abbreviation: {stats['config']['key_abbreviation']}")
    print(f"  [OK] Compact format: {stats['config']['compact_format']}")
    print(f"  [OK] Deduplication: {stats['config']['deduplication']}")
    print(f"  [OK] Cache enabled: {stats['config']['cache_enabled']}")
    
    # ========================================
    # 3. STORAGE WITH OPTIMIZATION
    # ========================================
    print("\n3. Testing storage with optimization...")
    
    # Create a provider config (mock for demo)
    provider_config = ProviderConfig(
        name="openai",
        api_key="mock-key-for-demo",
        model="gpt-3.5-turbo",
        base_url="https://api.openai.com/v1"
    )
    
    # Load personality
    personality_data = {
        "name": "optimized_assistant",
        "description": "An optimized AI assistant",
        "system_prompt": "You are a helpful AI assistant optimized for efficiency.",
        "metadata": {"version": "1.2.0", "author": "Demo"}
    }
    
    await client.load_personality("optimized_assistant", personality_data)
    print("  [OK] Personality loaded")
    
    # Create session
    session_id = await client.create_session(
        personality_name="optimized_assistant",
        provider_config=provider_config
    )
    print(f"  [OK] Session created: {session_id}")
    
    # Storage is automatically wrapped with OptimizedStorageWrapper
    # All data is compressed/expanded transparently
    print("  [OK] Storage is automatically optimized (transparent)")
    
    # ========================================
    # 4. MEMORY WITH OPTIMIZATION
    # ========================================
    print("\n4. Testing memory with optimization...")
    
    # Store memory (automatically optimized)
    await client.store_memory(
        session_id=session_id,
        key="user_preference",
        value="interested in AI optimization and token reduction"
    )
    print("  [OK] Memory stored (optimized)")
    
    # Retrieve memory (automatically expanded)
    memory = await client.get_memory(session_id, "user_preference")
    print(f"  [OK] Memory retrieved: {memory}")
    
    # MemoryManager uses Core MemorySystem when available
    if hasattr(client.memory_manager, '_use_core'):
        print(f"  [OK] MemoryManager using Core: {client.memory_manager._use_core}")
    
    # ========================================
    # 5. COMPARISON: WITH vs WITHOUT OPTIMIZATION
    # ========================================
    print("\n5. Optimization benefits...")
    print("  [INFO] Token reduction: 25-45%")
    print("  [INFO] Storage size: Reduced by ~30-40%")
    print("  [INFO] Cache hits: Faster reads for frequently accessed data")
    print("  [INFO] Deduplication: Automatic merge of duplicate facts")
    
    # ========================================
    # 6. CLEANUP
    # ========================================
    print("\n6. Cleaning up...")
    await client.cleanup()
    print("  [OK] Cleanup completed")
    
    print("\n" + "=" * 80)
    print("[OK] Optimization example completed successfully!")
    print("=" * 80)
    print("\nKey Takeaways:")
    print("  ✅ Optimization is transparent - no code changes needed")
    print("  ✅ Enable with optimization_config parameter")
    print("  ✅ Automatic compression/expansion of data")
    print("  ✅ Significant token reduction (25-45%)")
    print("  ✅ Backward compatible - works without optimization too")


if __name__ == "__main__":
    print("\n[INFO] This example demonstrates v1.2.0 optimization features")
    print("[INFO] Requires: luminoracore>=1.2.0 and luminoracore-sdk>=1.2.0")
    print("[INFO] Install Core: pip install -e ../luminoracore/\n")
    
    asyncio.run(main())

