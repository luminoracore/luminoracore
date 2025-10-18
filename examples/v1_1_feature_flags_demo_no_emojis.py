"""
LuminoraCore v1.1 - Feature Flags Deep Dive (Windows Compatible)

Demonstrates advanced use of Feature Flags for granular feature control.
"""

import json
from pathlib import Path
from luminoracore.core.config import FeatureFlagManager, get_features, is_enabled


def main():
    """Complete Feature Flags demonstration."""
    
    print("=" * 80)
    print("LuminoraCore v1.1 - Feature Flags Deep Dive")
    print("=" * 80)
    
    # ========================================
    # 1. PREDEFINED CONFIGURATIONS
    # ========================================
    
    print("\n1. PREDEFINED CONFIGURATIONS")
    print("-" * 80)
    
    # Load predefined configurations
    config_dir = Path("config")
    config_files = [
        "features_minimal.json",
        "features_development.json", 
        "features_production_safe.json"
    ]
    
    print("\nAvailable configurations:")
    for config_file in config_files:
        config_path = config_dir / config_file
        if config_path.exists():
            print(f"   + {config_file}")
        else:
            print(f"   - {config_file} (not found)")
    
    # ========================================
    # 2. FEATURE FLAG MANAGER
    # ========================================
    
    print("\n\n2. FEATURE FLAG MANAGER")
    print("-" * 80)
    
    # Initialize manager
    manager = FeatureFlagManager()
    print(f"Manager initialized: {type(manager).__name__}")
    
    # Get current features
    features = manager.get_features()
    print(f"Current features type: {type(features).__name__}")
    
    # ========================================
    # 3. FEATURE STATUS CHECKING
    # ========================================
    
    print("\n\n3. FEATURE STATUS CHECKING")
    print("-" * 80)
    
    # Check individual features
    feature_checks = [
        "episodic_memory",
        "mood_system", 
        "affinity_system",
        "personality_evolution",
        "advanced_sentiment",
        "hierarchical_personalities",
        "dynamic_compilation",
        "fact_extraction",
        "semantic_search",
        "session_export"
    ]
    
    print("\nFeature Status:")
    for feature in feature_checks:
        try:
            enabled = features.is_enabled(feature)
            status = "ENABLED" if enabled else "DISABLED"
            print(f"   {feature}: {status}")
        except Exception as e:
            print(f"   {feature}: ERROR - {e}")
    
    # ========================================
    # 4. LOADING CONFIGURATIONS
    # ========================================
    
    print("\n\n4. LOADING CONFIGURATIONS")
    print("-" * 80)
    
    # Try loading each configuration
    for config_file in config_files:
        config_path = config_dir / config_file
        if config_path.exists():
            try:
                print(f"\nLoading {config_file}:")
                loaded_features = manager.load_from_file(str(config_path))
                
                # Show some key features
                key_features = ["episodic_memory", "mood_system", "affinity_system"]
                for feature in key_features:
                    try:
                        enabled = loaded_features.is_enabled(feature)
                        status = "ENABLED" if enabled else "DISABLED"
                        print(f"   {feature}: {status}")
                    except Exception as e:
                        print(f"   {feature}: ERROR - {e}")
                        
            except Exception as e:
                print(f"   ERROR loading {config_file}: {e}")
        else:
            print(f"\n{config_file}: File not found")
    
    # ========================================
    # 5. FEATURE SUMMARY
    # ========================================
    
    print("\n\n5. FEATURE SUMMARY")
    print("-" * 80)
    
    try:
        summary = manager.get_summary()
        print(f"Summary type: {type(summary)}")
        print(f"Summary keys: {list(summary.keys()) if isinstance(summary, dict) else 'Not a dict'}")
        
        if isinstance(summary, dict):
            for key, value in summary.items():
                print(f"   {key}: {value}")
                
    except Exception as e:
        print(f"ERROR getting summary: {e}")
    
    # ========================================
    # 6. CONVENIENCE FUNCTIONS
    # ========================================
    
    print("\n\n6. CONVENIENCE FUNCTIONS")
    print("-" * 80)
    
    try:
        # Test convenience functions
        current_features = get_features()
        print(f"get_features() returned: {type(current_features).__name__}")
        
        # Test is_enabled function
        episodic_enabled = is_enabled("episodic_memory")
        print(f"is_enabled('episodic_memory'): {episodic_enabled}")
        
    except Exception as e:
        print(f"ERROR with convenience functions: {e}")
    
    # ========================================
    # 7. FEATURE CATEGORIES
    # ========================================
    
    print("\n\n7. FEATURE CATEGORIES")
    print("-" * 80)
    
    try:
        # Get enabled features by category
        enabled_features = features.get_enabled_features()
        print(f"Enabled features: {enabled_features}")
        
        # Get disabled features
        disabled_features = features.get_disabled_features()
        print(f"Disabled features: {disabled_features}")
        
    except Exception as e:
        print(f"ERROR with feature categories: {e}")
    
    print("\n" + "=" * 80)
    print("Feature Flags demonstration completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
