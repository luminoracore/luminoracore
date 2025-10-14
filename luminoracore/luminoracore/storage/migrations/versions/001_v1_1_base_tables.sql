-- ============================================================================
-- LuminoraCore v1.1 - Base Tables Migration
-- VERSION: 001
-- DESCRIPTION: Add v1.1 tables for Core (affinity, facts, episodes, moods)
-- NOTES: These are CORE tables, separate from SDK session tables
-- ROLLBACK: See rollback section at bottom
-- ============================================================================

-- ============================================================================
-- AFFINITY TABLE (Relationship progression)
-- ============================================================================

CREATE TABLE IF NOT EXISTS user_affinity (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT NOT NULL,
    personality_name TEXT NOT NULL,
    affinity_points INTEGER DEFAULT 0 CHECK(affinity_points >= 0 AND affinity_points <= 100),
    current_level TEXT DEFAULT 'stranger',
    total_messages INTEGER DEFAULT 0,
    positive_interactions INTEGER DEFAULT 0,
    negative_interactions INTEGER DEFAULT 0,
    last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, personality_name)
);

CREATE INDEX IF NOT EXISTS idx_affinity_user_id ON user_affinity(user_id);
CREATE INDEX IF NOT EXISTS idx_affinity_personality ON user_affinity(personality_name);
CREATE INDEX IF NOT EXISTS idx_affinity_last_interaction ON user_affinity(last_interaction);

-- ============================================================================
-- FACTS TABLE (Learned facts about users)
-- ============================================================================

CREATE TABLE IF NOT EXISTS user_facts (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT NOT NULL,
    session_id TEXT,
    category TEXT NOT NULL CHECK(category IN (
        'personal_info', 'preferences', 'relationships', 
        'hobbies', 'goals', 'health', 'work', 'events', 'other'
    )),
    fact_key TEXT NOT NULL,
    fact_value TEXT NOT NULL,
    confidence REAL DEFAULT 1.0 CHECK(confidence >= 0.0 AND confidence <= 1.0),
    source_message_id TEXT,
    first_mentioned TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mention_count INTEGER DEFAULT 1,
    tags TEXT,
    context TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, category, fact_key)
);

CREATE INDEX IF NOT EXISTS idx_facts_user_id ON user_facts(user_id);
CREATE INDEX IF NOT EXISTS idx_facts_category ON user_facts(category);
CREATE INDEX IF NOT EXISTS idx_facts_session ON user_facts(session_id);
CREATE INDEX IF NOT EXISTS idx_facts_active ON user_facts(is_active);

-- ============================================================================
-- EPISODES TABLE (Memorable moments)
-- ============================================================================

CREATE TABLE IF NOT EXISTS episodes (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT NOT NULL,
    session_id TEXT,
    episode_type TEXT NOT NULL CHECK(episode_type IN (
        'emotional_moment', 'milestone', 'confession', 
        'conflict', 'achievement', 'bonding', 'routine'
    )),
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    importance REAL NOT NULL CHECK(importance >= 0.0 AND importance <= 10.0),
    sentiment TEXT NOT NULL CHECK(sentiment IN (
        'very_positive', 'positive', 'neutral', 'negative', 'very_negative'
    )),
    tags TEXT,
    context_messages TEXT,
    timestamp TIMESTAMP NOT NULL,
    temporal_decay REAL DEFAULT 1.0 CHECK(temporal_decay >= 0.0 AND temporal_decay <= 1.0),
    related_facts TEXT,
    related_episodes TEXT,
    metadata TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_episodes_user_id ON episodes(user_id);
CREATE INDEX IF NOT EXISTS idx_episodes_importance ON episodes(importance);
CREATE INDEX IF NOT EXISTS idx_episodes_timestamp ON episodes(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_episodes_type ON episodes(episode_type);
CREATE INDEX IF NOT EXISTS idx_episodes_session ON episodes(session_id);

-- ============================================================================
-- SESSION MOODS TABLE (Emotional states per session)
-- ============================================================================

CREATE TABLE IF NOT EXISTS session_moods (
    session_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    current_mood TEXT DEFAULT 'neutral',
    mood_intensity REAL DEFAULT 1.0 CHECK(mood_intensity >= 0.0 AND mood_intensity <= 1.0),
    mood_started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mood_history TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_moods_user_id ON session_moods(user_id);
CREATE INDEX IF NOT EXISTS idx_moods_current_mood ON session_moods(current_mood);

-- ============================================================================
-- MIGRATION TRACKING (Meta table)
-- ============================================================================

CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    checksum TEXT,
    description TEXT
);

-- Record this migration
INSERT OR IGNORE INTO schema_migrations (version, name, description, checksum) 
VALUES (
    1, 
    '001_v1_1_base_tables', 
    'Base tables for LuminoraCore v1.1: affinity, facts, episodes, moods',
    'sha256:placeholder'
);

-- ============================================================================
-- VERIFICATION QUERIES (Run after migration to verify)
-- ============================================================================

-- Verify all tables exist
-- SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;

-- Expected tables:
-- - episodes
-- - schema_migrations
-- - session_moods
-- - user_affinity
-- - user_facts

-- Verify indexes
-- SELECT name FROM sqlite_master WHERE type='index' ORDER BY name;

-- ============================================================================
-- ROLLBACK SCRIPT (If needed)
-- ============================================================================

-- To rollback this migration, run:
-- DROP TABLE IF EXISTS session_moods;
-- DROP TABLE IF EXISTS episodes;
-- DROP TABLE IF EXISTS user_facts;
-- DROP TABLE IF EXISTS user_affinity;
-- DELETE FROM schema_migrations WHERE version = 1;

