"""
LuminoraCore v1.1 - Complete Workflow Example

This example demonstrates a complete production workflow using ALL 
v1.1 features integrated:

✅ Feature Flags - Dynamic feature control
✅ Database Migrations - Schema management
✅ Affinity System - Relationship tracking
✅ Fact Extraction - Automatic learning
✅ Episodic Memory - Memorable moments
✅ Hierarchical Personalities - Adaptive personality
✅ Dynamic Compilation - Real-time compilation
✅ Snapshot Export/Import - Backup and restoration

REAL USE CASE:
An educational chatbot that:
1. Configures feature flags for production
2. Runs database migrations
3. Creates session with v1.1 personality
4. Interacts with user and learns
5. Adapts personality based on affinity
6. Exports snapshot at the end
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime

# Core imports
from luminoracore.core.config import FeatureFlagManager, get_features, is_enabled
from luminoracore.storage.migration_manager import MigrationManager, Migration
from luminoracore.core.relationship.affinity import AffinityManager, AffinityState
from luminoracore.core.memory.fact_extractor import FactExtractor
from luminoracore.core.memory.episodic import EpisodicMemoryManager
from luminoracore.core.memory.classifier import MemoryClassifier
from luminoracore.core.personality_v1_1 import PersonalityV11Extensions
from luminoracore.core.compiler_v1_1 import DynamicPersonalityCompiler


async def main():
    """Complete v1.1 production workflow."""
    
    print("=" * 80)
    print("🚀 LuminoraCore v1.1 - COMPLETE PRODUCTION WORKFLOW")
    print("=" * 80)
    print("\nThis example demonstrates all v1.1 features integrated")
    print("Use case: Educational chatbot with memory and adaptive personality\n")
    
    # ========================================
    # STEP 1: CONFIGURE FEATURE FLAGS
    # ========================================
    print("\n" + "=" * 80)
    print("STEP 1: FEATURE FLAGS CONFIGURATION")
    print("=" * 80)
    
    print("\n📋 Loading production feature configuration...")
    
    # Simulate configuration file
    feature_config = {
        "episodic_memory": True,
        "semantic_search": False,  # Disabled in production
        "fact_extraction": True,
        "hierarchical_personality": True,
        "mood_system": False,  # Not yet implemented
        "affinity_system": True,
        "conversation_analytics": True,
        "snapshot_export": True
    }
    
    # Load features
    FeatureFlagManager.load_from_dict(feature_config)
    features = get_features()
    
    print("\n✅ Enabled features:")
    for feature, enabled in feature_config.items():
        status = "✅ ON" if enabled else "❌ OFF"
        print(f"   {status}  {feature}")
    
    print(f"\n💡 Feature flags in memory: {len(feature_config)} features configured")
    
    # ========================================
    # STEP 2: DATABASE MIGRATIONS
    # ========================================
    print("\n" + "=" * 80)
    print("STEP 2: DATABASE MIGRATIONS MANAGEMENT")
    print("=" * 80)
    
    print("\n🗄️  Checking migration status...")
    
    # Simulate migration manager (in production would use real storage)
    class MockStorage:
        def __init__(self):
            self.applied_migrations = ["001_initial", "002_affinity", "003_facts"]
        
        def get_applied_migrations(self):
            return self.applied_migrations
    
    storage = MockStorage()
    
    # Check applied migrations
    applied = storage.get_applied_migrations()
    print(f"\n✅ Applied migrations: {len(applied)}")
    for migration in applied:
        print(f"   ✓ {migration}")
    
    # Available migrations
    all_migrations = [
        "001_initial",
        "002_affinity", 
        "003_facts",
        "004_episodes",
        "005_moods"
    ]
    
    pending = [m for m in all_migrations if m not in applied]
    
    if pending:
        print(f"\n⚠️  Pending migrations: {len(pending)}")
        for migration in pending:
            print(f"   ⏳ {migration}")
        print("\n   In production you would run: luminora-cli migrate up")
    else:
        print("\n✅ All migrations are applied")
    
    print(f"\n💡 Database ready for v1.1")
    
    # ========================================
    # STEP 3: INITIALIZE v1.1 PERSONALITY
    # ========================================
    print("\n" + "=" * 80)
    print("STEP 3: INITIALIZE ADAPTIVE PERSONALITY")
    print("=" * 80)
    
    print("\n🎭 Loading Dr. Luna v1.1 personality...")
    
    # Load personality with hierarchical configuration
    personality_dict = {
        "persona": {
            "name": "Dr. Luna",
            "tagline": "Your enthusiastic science companion",
            "version": "1.1.0"
        },
        "core_traits": {
            "archetype": "scientist",
            "temperament": "energetic"
        },
        "advanced_parameters": {
            "verbosity": 0.9,
            "formality": 0.4,
            "humor": 0.6,
            "empathy": 0.8
        },
        "hierarchical_config": {
            "enabled": True,
            "relationship_levels": [
                {
                    "name": "stranger",
                    "affinity_range": [0, 20],
                    "description": "Formal and professional",
                    "modifiers": {
                        "advanced_parameters": {
                            "formality": 0.3,
                            "verbosity": -0.1
                        }
                    }
                },
                {
                    "name": "friend",
                    "affinity_range": [41, 60],
                    "description": "Casual and enthusiastic",
                    "modifiers": {
                        "advanced_parameters": {
                            "formality": -0.2,
                            "humor": 0.2
                        }
                    }
                },
                {
                    "name": "close_friend",
                    "affinity_range": [61, 100],
                    "description": "Very casual and playful",
                    "modifiers": {
                        "advanced_parameters": {
                            "formality": -0.3,
                            "humor": 0.3
                        }
                    }
                }
            ]
        },
        "memory_preferences": {
            "fact_categories": ["personal_info", "preferences", "goals", "hobbies"],
            "episode_types": ["milestone", "achievement", "emotional_moment"],
            "importance_threshold": 6.0
        },
        "affinity_config": {
            "interaction_types": {
                "positive": 3,
                "very_positive": 5,
                "question_about_science": 2,
                "shared_enthusiasm": 4
            }
        }
    }
    
    # Parse v1.1 extensions
    extensions = PersonalityV11Extensions.from_personality_dict(personality_dict)
    
    print(f"   ✓ Personality loaded: {personality_dict['persona']['name']}")
    print(f"   ✓ Version: {personality_dict['persona']['version']}")
    print(f"   ✓ Hierarchical levels: {len(extensions.hierarchical_config.relationship_levels)}")
    print(f"   ✓ Fact categories: {len(personality_dict['memory_preferences']['fact_categories'])}")
    
    # ========================================
    # STEP 4: SIMULATE USER CONVERSATION
    # ========================================
    print("\n" + "=" * 80)
    print("STEP 4: CONVERSATION WITH MEMORY AND AFFINITY TRACKING")
    print("=" * 80)
    
    # Initialize v1.1 components
    affinity_mgr = AffinityManager()
    fact_extractor = FactExtractor()
    episode_mgr = EpisodicMemoryManager()
    classifier = MemoryClassifier()
    compiler = DynamicPersonalityCompiler(personality_dict, extensions)
    
    # Create initial user state
    user_id = "student_alice"
    affinity_state = AffinityState(
        user_id=user_id,
        personality_name="dr_luna",
        affinity_points=0,
        current_level="stranger"
    )
    
    print(f"\n👤 User: {user_id}")
    print(f"   Initial state: {affinity_state.current_level} (0 points)\n")
    
    # Simulate conversation
    conversation = [
        {
            "turn": 1,
            "message": "Hello! I'm Alice, I'm 19 and studying biology.",
            "interaction_type": "positive",
            "points": 3,
            "extract_facts": True
        },
        {
            "turn": 2,
            "message": "I'm really interested in marine biology, especially coral reefs!",
            "interaction_type": "shared_enthusiasm",
            "points": 4,
            "extract_facts": True
        },
        {
            "turn": 3,
            "message": "Can you explain how photosynthesis works in coral?",
            "interaction_type": "question_about_science",
            "points": 2,
            "extract_facts": False
        },
        {
            "turn": 4,
            "message": "Wow, that's amazing! I just got accepted to a marine research program!",
            "interaction_type": "very_positive",
            "points": 5,
            "extract_facts": False,
            "create_episode": True,
            "episode_data": {
                "type": "achievement",
                "title": "Accepted to marine research program",
                "summary": "Student got accepted to prestigious program",
                "sentiment": "very_positive"
            }
        }
    ]
    
    all_facts = []
    all_episodes = []
    
    for conv in conversation:
        print(f"\n{'─' * 80}")
        print(f"TURN {conv['turn']}")
        print(f"{'─' * 80}")
        
        print(f"\n💬 User: \"{conv['message']}\"")
        
        # 1. Check feature flags before using features
        if is_enabled("fact_extraction") and conv.get("extract_facts"):
            print("\n   📋 [Feature: fact_extraction ENABLED]")
            facts = fact_extractor.extract_sync(user_id=user_id, message=conv['message'])
            if facts:
                all_facts.extend(facts)
                print(f"   ✓ Extracted {len(facts)} facts:")
                for fact in facts:
                    print(f"      • {fact.category}: {fact.key} = {fact.value} (conf: {fact.confidence:.2f})")
        
        # 2. Create episode if memorable
        if is_enabled("episodic_memory") and conv.get("create_episode"):
            print("\n   📖 [Feature: episodic_memory ENABLED]")
            episode = episode_mgr.create_episode(
                user_id=user_id,
                episode_type=conv['episode_data']['type'],
                title=conv['episode_data']['title'],
                summary=conv['episode_data']['summary'],
                sentiment=conv['episode_data']['sentiment']
            )
            all_episodes.append(episode)
            print(f"   ✓ Episode created: '{episode.title}'")
            print(f"      Importance: {episode.importance:.1f}/10")
        
        # 3. Update affinity
        if is_enabled("affinity_system"):
            print(f"\n   💝 [Feature: affinity_system ENABLED]")
            old_level = affinity_state.current_level
            affinity_state = affinity_mgr.update_affinity_state(
                affinity_state, 
                points_delta=conv['points']
            )
            
            print(f"   ✓ Affinity updated: +{conv['points']} points")
            print(f"      Total: {affinity_state.affinity_points}/100")
            
            if affinity_state.current_level != old_level:
                print(f"      ✨ LEVEL UP! {old_level} → {affinity_state.current_level}")
        
        # 4. Compile personality dynamically
        if is_enabled("hierarchical_personality"):
            print(f"\n   🎭 [Feature: hierarchical_personality ENABLED]")
            compiled = compiler.compile(affinity_points=affinity_state.affinity_points)
            params = compiled["advanced_parameters"]
            print(f"   ✓ Personality compiled for level: {affinity_state.current_level}")
            print(f"      Formality: {params['formality']:.2f}")
            print(f"      Humor: {params['humor']:.2f}")
            print(f"      Verbosity: {params['verbosity']:.2f}")
    
    # ========================================
    # STEP 5: MEMORY ANALYSIS
    # ========================================
    print("\n" + "=" * 80)
    print("STEP 5: MEMORY ANALYSIS AND CLASSIFICATION")
    print("=" * 80)
    
    # Classify facts by importance
    print("\n🏷️  Classification of learned facts:")
    for fact in all_facts:
        classification = classifier.classify_fact(fact)
        print(f"   • {fact.key}: {classification.importance_level} importance")
    
    # Top episodes
    if all_episodes:
        print("\n📖 Memorable episodes:")
        top_episodes = classifier.get_top_n_episodes(all_episodes, n=3)
        for i, ep in enumerate(top_episodes, 1):
            print(f"   {i}. {ep.title}")
            print(f"      Importance: {ep.importance:.1f}/10")
            print(f"      Type: {ep.episode_type}")
    
    # ========================================
    # STEP 6: CONTEXT FOR NEXT RESPONSE
    # ========================================
    print("\n" + "=" * 80)
    print("STEP 6: GENERATE CONTEXT FOR NEXT RESPONSE")
    print("=" * 80)
    
    print("\n🧠 Building context based on memory...")
    
    # Compile relevant context
    context = {
        "user_id": user_id,
        "affinity": {
            "points": affinity_state.affinity_points,
            "level": affinity_state.current_level
        },
        "facts": [
            {
                "category": f.category,
                "key": f.key,
                "value": f.value,
                "confidence": f.confidence
            }
            for f in all_facts
        ],
        "episodes": [
            {
                "title": ep.title,
                "type": ep.episode_type,
                "importance": ep.importance
            }
            for ep in all_episodes
        ]
    }
    
    print(f"\n   ✓ Context generated:")
    print(f"      Relationship level: {context['affinity']['level']}")
    print(f"      Affinity points: {context['affinity']['points']}/100")
    print(f"      Known facts: {len(context['facts'])}")
    print(f"      Memorable episodes: {len(context['episodes'])}")
    
    # Show what we remember
    if context['facts']:
        print(f"\n   📋 We remember about {user_id}:")
        for fact in context['facts']:
            print(f"      • {fact['key']}: {fact['value']}")
    
    # ========================================
    # STEP 7: SNAPSHOT EXPORT
    # ========================================
    print("\n" + "=" * 80)
    print("STEP 7: EXPORT STATE SNAPSHOT")
    print("=" * 80)
    
    if is_enabled("snapshot_export"):
        print("\n📸 [Feature: snapshot_export ENABLED]")
        print("\n💾 Creating complete state snapshot...")
        
        # Create snapshot
        snapshot = {
            "_snapshot_info": {
                "version": "1.1.0",
                "created_at": datetime.utcnow().isoformat(),
                "user_id": user_id,
                "personality_name": "dr_luna"
            },
            "affinity_state": {
                "affinity_points": affinity_state.affinity_points,
                "current_level": affinity_state.current_level,
                "total_messages": affinity_state.total_messages,
                "positive_interactions": affinity_state.positive_interactions
            },
            "facts": context['facts'],
            "episodes": context['episodes'],
            "personality_template": personality_dict
        }
        
        # Save snapshot
        snapshot_file = f"session_snapshot_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        # In production you would save this
        # with open(snapshot_file, 'w') as f:
        #     json.dump(snapshot, f, indent=2)
        
        print(f"   ✓ Snapshot created: {snapshot_file}")
        print(f"      Size: ~{len(json.dumps(snapshot))} bytes")
        print(f"      Includes: affinity, {len(context['facts'])} facts, {len(context['episodes'])} episodes")
        
        print(f"\n   💡 To restore: luminora-cli snapshot restore --input {snapshot_file}")
    else:
        print("\n❌ [Feature: snapshot_export DISABLED]")
        print("   Snapshots not available in this configuration")
    
    # ========================================
    # STEP 8: ANALYTICS AND STATISTICS
    # ========================================
    print("\n" + "=" * 80)
    print("STEP 8: SESSION ANALYTICS AND STATISTICS")
    print("=" * 80)
    
    if is_enabled("conversation_analytics"):
        print("\n📊 [Feature: conversation_analytics ENABLED]")
        print("\n📈 Session statistics:")
        
        analytics = {
            "session_id": f"session_{user_id}",
            "total_messages": len(conversation),
            "facts_learned": len(all_facts),
            "episodes_created": len(all_episodes),
            "affinity_progression": {
                "initial": 0,
                "final": affinity_state.affinity_points,
                "delta": affinity_state.affinity_points
            },
            "level_progression": {
                "initial": "stranger",
                "final": affinity_state.current_level
            },
            "memory_usage": {
                "facts": len(all_facts),
                "episodes": len(all_episodes),
                "total_memories": len(all_facts) + len(all_episodes)
            }
        }
        
        print(f"\n   📊 General metrics:")
        print(f"      Total messages: {analytics['total_messages']}")
        print(f"      Facts learned: {analytics['facts_learned']}")
        print(f"      Episodes created: {analytics['episodes_created']}")
        
        print(f"\n   💝 Affinity progression:")
        print(f"      Initial: {analytics['affinity_progression']['initial']} points")
        print(f"      Final: {analytics['affinity_progression']['final']} points")
        print(f"      Increase: +{analytics['affinity_progression']['delta']} points")
        
        print(f"\n   🎭 Level progression:")
        print(f"      Initial: {analytics['level_progression']['initial']}")
        print(f"      Final: {analytics['level_progression']['final']}")
        
        print(f"\n   🧠 Memory usage:")
        print(f"      Total memories: {analytics['memory_usage']['total_memories']}")
    
    # ========================================
    # STEP 9: SUMMARY AND RECOMMENDATIONS
    # ========================================
    print("\n" + "=" * 80)
    print("STEP 9: SUMMARY AND NEXT STEPS")
    print("=" * 80)
    
    print("\n✅ WORKFLOW COMPLETED SUCCESSFULLY")
    print("\n🎯 v1.1 Features demonstrated:")
    
    features_used = [
        ("Feature Flags", "✅", "Dynamic feature configuration"),
        ("Database Migrations", "✅", "DB schema management"),
        ("Affinity System", "✅", f"Progression from 0 → {affinity_state.affinity_points} points"),
        ("Hierarchical Personality", "✅", f"Current level: {affinity_state.current_level}"),
        ("Fact Extraction", "✅", f"{len(all_facts)} facts learned"),
        ("Episodic Memory", "✅", f"{len(all_episodes)} episodes saved"),
        ("Dynamic Compilation", "✅", "Personality adapted in real-time"),
        ("Snapshot Export", "✅", "Complete state exportable")
    ]
    
    for feature, status, detail in features_used:
        print(f"\n   {status} {feature}")
        print(f"       {detail}")
    
    # Recommendations for next steps
    print("\n\n📚 RECOMMENDED NEXT STEPS:")
    print("\n   For development:")
    print("   1. Enable more features in config/features_development.json")
    print("   2. Test with real database (SQLite/PostgreSQL)")
    print("   3. Integrate with real LLM provider")
    
    print("\n   For production:")
    print("   1. Use config/features_production_safe.json")
    print("   2. Configure Redis/PostgreSQL for storage")
    print("   3. Implement automatic snapshot backups")
    print("   4. Monitor analytics in real-time")
    
    print("\n   To extend:")
    print("   1. Create more v1.1 personalities (see dr_luna_v1_1.json)")
    print("   2. Customize affinity_config per use case")
    print("   3. Adjust importance_threshold as needed")
    
    # ========================================
    # EQUIVALENT CLI COMMANDS
    # ========================================
    print("\n" + "=" * 80)
    print("EQUIVALENT CLI COMMANDS")
    print("=" * 80)
    
    print("\n🔧 To do the same with CLI:")
    print("\n   # Feature flags")
    print("   export LUMINORA_FEATURES_CONFIG=config/features_production_safe.json")
    print("\n   # Migrations")
    print("   luminora-cli migrate --status")
    print("   luminora-cli migrate up")
    print("\n   # Memory queries")
    print(f"   luminora-cli memory facts --session-id {user_id}")
    print(f"   luminora-cli memory episodes --session-id {user_id} --min-importance 7.0")
    print("\n   # Snapshot")
    print(f"   luminora-cli snapshot create --session-id {user_id} --output backup.json")
    print(f"   luminora-cli snapshot restore --input backup.json")
    
    # ========================================
    # END
    # ========================================
    print("\n" + "=" * 80)
    print("🎉 v1.1 WORKFLOW COMPLETED")
    print("=" * 80)
    
    print(f"\n✨ Final state:")
    print(f"   User: {user_id}")
    print(f"   Level: {affinity_state.current_level}")
    print(f"   Affinity: {affinity_state.affinity_points}/100")
    print(f"   Messages: {len(conversation)}")
    print(f"   Facts: {len(all_facts)}")
    print(f"   Episodes: {len(all_episodes)}")
    
    print(f"\n🚀 This example demonstrates a REAL production use case")
    print(f"   with ALL v1.1 features integrated.\n")
    
    print("=" * 80)


if __name__ == "__main__":
    print("\n🎓 EDUCATIONAL CHATBOT - Complete v1.1 Production Workflow")
    print("This example simulates a complete educational chatbot with all v1.1 features\n")
    
    asyncio.run(main())
