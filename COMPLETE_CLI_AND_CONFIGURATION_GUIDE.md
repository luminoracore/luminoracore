# 🔧 Complete CLI and Configuration Guide - LuminoraCore v1.1

**Complete guide for CLI commands, personality enrichment, sentiment analysis, and configuration**

---

## 🎭 **ENRICHED PERSONALITY (GENERATED JSON)**

### **📍 Where is the enriched personality JSON generated?**

The enriched personality JSON is generated in **`conversation_export.json`** in the `final_personality` section:

```json
{
  "final_personality": {
    "core_traits": {
      "professionalism": 1.0,
      "efficiency": 1.0,
      "empathy": 1.0,
      "directness": 0.736
    },
    "communication_style": {
      "formality": 0.4000000000000001,
      "warmth": 1.0,
      "humor": 0.9,
      "patience": 0.836
    }
  }
}
```

### **🔄 Personality Evolution (3 Recalculations):**

```json
{
  "personality_evolution": [
    {
      "message_count": 3,
      "affinity": 19,
      "relationship_level": "acquaintance",
      "personality_before": { /* initial personality */ },
      "personality_after": { /* personality after message 3 */ },
      "changes": {
        "professionalism": 0.019,
        "efficiency": 0.038,
        "empathy": 0.057,
        "directness": 0.019,
        "patience": 0.019
      }
    }
    // ... more recalculations
  ]
}
```

### **📁 Files Generated in Simulation:**

1. **`conversation_export.json`** - Complete JSON with:
   - `session_info`: Session information
   - `conversation`: The 10 complete messages
   - `personality_evolution`: 3 personality recalculations
   - `memory_classification`: Classified facts and episodes
   - `final_personality`: Final enriched personality

2. **`conversation_memory.db`** - SQLite database with:
   - `sessions` table: Session information
   - `conversations` table: Messages and context
   - `personality_evolution` table: Personality evolution
   - `memory_facts` table: Classified facts
   - `memory_episodes` table: Memorable episodes

---

## 📊 **SENTIMENT ANALYSIS AND CONFIGURATION**

### **⚙️ Where is sentiment analysis frequency configured?**

In the personality configuration file:

```json
{
  "memory_preferences": {
    "fact_retention": 0.9,
    "episodic_memory": 0.8,
    "preference_learning": 0.9,
    "goal_tracking": 0.8,
    "recalculation_frequency": 3,  // ← HERE: Every 3 messages
    "sentiment_analysis_frequency": 5  // ← HERE: Every 5 messages
  }
}
```

### **🧠 Complete Sentiment Analysis Configuration:**

```json
{
  "sentiment_config": {
    "enabled": true,
    "frequency": 5,  // Every 5 messages
    "provider": "deepseek",  // or "openai", "anthropic", etc.
    "analysis_types": [
      "emotional_tone",
      "user_satisfaction", 
      "relationship_health",
      "conversation_mood"
    ],
    "triggers": [
      "message_count_threshold",
      "affinity_change_detected",
      "negative_sentiment_detected",
      "relationship_level_change"
    ],
    "actions": {
      "on_negative_sentiment": "adjust_empathy_up",
      "on_positive_sentiment": "maintain_or_enhance_warmth",
      "on_neutral_sentiment": "increase_engagement"
    }
  }
}
```

### **📈 Sentiment Analysis Example:**

```json
{
  "sentiment_analysis": {
    "message_count": 5,
    "timestamp": "2025-10-16T22:47:39.064316",
    "analysis": {
      "overall_sentiment": 0.8,  // Positive
      "emotional_tone": "enthusiastic",
      "user_satisfaction": 0.85,
      "relationship_health": "improving",
      "conversation_mood": "collaborative"
    },
    "recommendations": [
      "maintain_current_warmth_level",
      "increase_technical_detail",
      "continue_direct_communication"
    ],
    "personality_adjustments": {
      "warmth": +0.1,
      "technical_depth": +0.05
    }
  }
}
```

### **🔧 CLI Command for Sentiment Analysis:**

```bash
# Analyze session sentiment (future command)
luminoracore sentiment analyze user_123        # Analyze sentiment
luminoracore sentiment history user_123        # Sentiment history
luminoracore sentiment dashboard user_123      # Sentiment dashboard
```

---

## 🖥️ **COMPLETE CLI COMMANDS**

### **📋 CLI Commands List v1.1 (REAL):**

```bash
# BASIC COMMANDS v1.0 (11 commands)
luminoracore validate <personality_file>     # Validate personality
luminoracore compile <personality_file>      # Compile personality  
luminoracore blend <file1> <file2>           # Blend personalities
luminoracore test <personality_file>         # Test personality
luminoracore create <template>               # Create new personality
luminoracore list                            # List personalities
luminoracore serve                           # Web server
luminoracore update <personality_file>       # Update personality
luminoracore init <project_name>             # Initialize project
luminoracore info <personality_file>         # Personality information

# NEW COMMANDS v1.1 (3 commands)
luminoracore migrate [db_path]               # Migrate database
luminoracore memory facts <session_id>       # Manage memory facts
luminoracore memory episodes <session_id>    # Manage episodes
luminoracore memory search <session_id>      # Search memory
luminoracore snapshot <session_id>           # Export snapshot
```

### **📖 CLI Commands Usage Guide:**

#### **🔧 Basic Commands:**

```bash
# 1. Validate personality
luminoracore validate luminoracore/luminoracore/personalities/dr_luna.json

# 2. Compile personality for OpenAI
luminoracore compile luminoracore/luminoracore/personalities/dr_luna.json --provider openai

# 3. Blend two personalities
luminoracore blend dr_luna.json victoria_sterling.json --output mixed_personality.json

# 4. Test personality
luminoracore test dr_luna.json --provider deepseek --api-key $DEEPSEEK_API_KEY

# 5. Analyze personality
luminoracore analyze dr_luna.json --detailed
```

#### **🆕 v1.1 Commands:**

```bash
# 1. Migrate database to v1.1
luminoracore migrate                          # Migrate with default configuration
luminoracore migrate custom.db                # Migrate specific database
luminoracore migrate --dry-run                # See what would be done without applying
luminoracore migrate --status                 # See migration status
luminoracore migrate --history                # See migration history

# 2. Manage session memory
luminoracore memory facts user_123            # List session facts
luminoracore memory facts user_123 --category personal_info  # Filter by category
luminoracore memory facts user_123 --format json            # JSON format
luminoracore memory episodes user_123         # List memorable episodes
luminoracore memory search user_123 "Carlos"  # Search in memory

# 3. Export complete snapshot
luminoracore snapshot user_123                # Export session snapshot
luminoracore snapshot user_123 --format json  # JSON format
luminoracore snapshot user_123 --format sqlite # SQLite format
```

### **📚 Command Help:**

```bash
# General help
luminoracore --help

# Specific command help
luminoracore validate --help
luminoracore migrate --help
luminoracore memory --help
luminoracore snapshot --help
```

---

## ⚙️ **ADVANCED CONFIGURATION**

### **🎯 Frequency Configuration:**

```json
{
  "luminora_config": {
    "personality_recalculation": {
      "frequency": 3,  // Every 3 messages
      "triggers": [
        "message_count",
        "affinity_change",
        "relationship_level_change"
      ]
    },
    "sentiment_analysis": {
      "frequency": 5,  // Every 5 messages
      "triggers": [
        "message_count",
        "negative_sentiment_detected",
        "conversation_quality_drop"
      ]
    },
    "memory_consolidation": {
      "frequency": 10,  // Every 10 messages
      "triggers": [
        "message_count",
        "memory_size_threshold",
        "conversation_end"
      ]
    }
  }
}
```

### **🔧 Environment Variables:**

```bash
# Frequency configuration
export LUMINORA_RECALCULATION_FREQUENCY=3
export LUMINORA_SENTIMENT_FREQUENCY=5
export LUMINORA_MEMORY_CONSOLIDATION_FREQUENCY=10

# Sentiment analysis configuration
export LUMINORA_SENTIMENT_PROVIDER=deepseek
export LUMINORA_SENTIMENT_MODEL=deepseek-chat
export LUMINORA_SENTIMENT_ENABLED=true

# Memory configuration
export LUMINORA_MEMORY_RETENTION_DAYS=30
export LUMINORA_MEMORY_MAX_FACTS=1000
export LUMINORA_MEMORY_MAX_EPISODES=500
```

---

## 🚀 **FUTURE COMMANDS (v1.2+)**

### **📋 Planned Commands (v1.2+):**

```bash
# Advanced analysis
luminoracore sentiment analyze <session_id>      # Analyze sentiment
luminoracore sentiment history <session_id>      # Sentiment history
luminoracore analytics dashboard <session_id>    # Analytics dashboard
luminoracore insights generate <session_id>      # Generate automatic insights

# Data management
luminoracore backup all-sessions                 # Complete backup
luminoracore restore from-backup <file>          # Restore backup
luminoracore sync cloud <provider>               # Sync with cloud
luminoracore export all-formats <session_id>     # Export all formats

# Development
luminoracore dev create-personality              # Interactive personality creation
luminoracore dev test-scenarios                  # Test scenarios
luminoracore dev benchmark                       # Performance benchmark
luminoracore dev validate-performance           # Validate performance

# Integration
luminoracore integrate webhook <url>             # Configure webhooks
luminoracore integrate api generate-keys         # Generate API keys
luminoracore integrate monitoring setup          # Configure monitoring
luminoracore integrate discord setup             # Configure Discord bot
luminoracore integrate telegram setup            # Configure Telegram bot

# Quality analysis
luminoracore quality check <personality_file>    # Verify quality
luminoracore quality optimize <personality_file> # Optimize personality
luminoracore quality compare <file1> <file2>     # Compare personalities
```

---

## 📊 **COMPLETE USAGE EXAMPLE**

### **🔧 Complete Configuration:**

```python
# config.py
PERSONALITY_CONFIG = {
    "name": "Victoria Sterling",
    "version": "1.1.0",
    "base_personality": {
        "core_traits": {
            "professionalism": 0.9,
            "efficiency": 0.8,
            "empathy": 0.7,
            "directness": 0.6
        }
    },
    "hierarchical_config": {
        "relationship_levels": {
            "stranger": {"affinity_threshold": 0},
            "acquaintance": {"affinity_threshold": 10},
            "friend": {"affinity_threshold": 25},
            "close_friend": {"affinity_threshold": 50}
        }
    },
    "memory_preferences": {
        "recalculation_frequency": 3,      # Every 3 messages
        "sentiment_analysis_frequency": 5,  # Every 5 messages
        "memory_consolidation_frequency": 10 # Every 10 messages
    },
    "sentiment_config": {
        "enabled": True,
        "provider": "deepseek",
        "frequency": 5,
        "analysis_types": [
            "emotional_tone",
            "user_satisfaction",
            "relationship_health"
        ]
    }
}
```

### **🖥️ CLI Commands Usage:**

```bash
# 1. Validate configuration
luminoracore validate victoria_sterling.json

# 2. Migrate to v1.1
luminoracore migrate --to-v1.1 --input victoria_sterling.json

# 3. Test with DeepSeek
luminoracore test victoria_sterling_v1_1.json --provider deepseek

# 4. Manage memory
luminoracore memory --session user_123 --action list

# 5. Export snapshot
luminoracore snapshot --export user_123 --format json
```

---

## 🎯 **COMPLETE SUMMARY OF ANSWERS**

### **📄 Enriched Personality JSON:**
✅ **Generated in**: `conversation_export.json` → `final_personality` section
✅ **Contains**: Complete personality evolution with 3 recalculations
✅ **Includes**: Facts, episodes, affinity and personality changes

### **📊 Sentiment Analysis:**
✅ **Configured in**: `memory_preferences.sentiment_analysis_frequency: 5`
✅ **Executes**: Every 5 messages (configurable)
✅ **Providers**: DeepSeek, OpenAI, Anthropic (configurable)
✅ **Commands**: `luminoracore sentiment analyze <session_id>` (future)

### **🖥️ CLI Commands:**
✅ **v1.0 Commands**: 10 basic commands (validate, compile, blend, test, create, list, serve, update, init, info)
✅ **v1.1 Commands**: 4 new commands (migrate, memory facts, memory episodes, memory search, snapshot)
✅ **Future Commands**: 15+ planned commands for v1.2+

### **⚙️ Configuration:**
✅ **Frequencies**: Configurable in JSON and environment variables
✅ **Providers**: DeepSeek, OpenAI, Anthropic, etc.
✅ **Customizable**: Every aspect is configurable
✅ **Database**: SQLite, PostgreSQL, Redis, MongoDB

### **📁 Generated Files:**
✅ **JSON**: `conversation_export.json` with all information
✅ **SQLite**: `conversation_memory.db` with table structure
✅ **Logs**: Detailed information of each process

### **🔄 Recalculation Process:**
✅ **Frequency**: Every 3 messages (configurable)
✅ **Triggers**: Affinity changes, relationship level, new facts
✅ **Algorithm**: Linear mapping + smooth transition
✅ **Export**: JSON, prompt, system prompt for LLMs

---

**🎊 LuminoraCore v1.1 has everything you need for intelligent personalities, sentiment analysis and advanced memory management!**
