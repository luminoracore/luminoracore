"""
Test Step 1: Database Migration System

Validates that v1.1 tables are created correctly without breaking v1.0
"""

import pytest
import sqlite3
import tempfile
import os
from pathlib import Path

# Add parent to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from luminoracore.storage.migrations.migration_manager import MigrationManager, MigrationError


class TestMigrationManager:
    """Test migration manager basic functionality"""
    
    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing"""
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        yield path
        # Cleanup - Windows-safe
        try:
            if os.path.exists(path):
                # Give SQLite time to release the file
                import time
                time.sleep(0.1)
                os.unlink(path)
        except PermissionError:
            # File still locked, will be cleaned by OS
            pass
    
    def test_manager_initialization(self, temp_db):
        """Test that manager initializes correctly"""
        manager = MigrationManager(temp_db)
        assert manager.db_path == temp_db
        assert manager.migrations_dir.exists()
    
    def test_get_current_version_fresh_db(self, temp_db):
        """Test getting version from fresh database"""
        manager = MigrationManager(temp_db)
        version = manager.get_current_version()
        assert version == 0  # Fresh DB should be version 0
    
    def test_get_pending_migrations(self, temp_db):
        """Test getting list of pending migrations"""
        manager = MigrationManager(temp_db)
        pending = manager.get_pending_migrations()
        
        # Should have at least migration 001
        assert len(pending) >= 1
        assert pending[0][0] == 1  # First migration is version 1
        assert pending[0][1].name == "001_v1_1_base_tables.sql"


class TestMigrationExecution:
    """Test actual migration execution"""
    
    @pytest.fixture
    def temp_db(self):
        """Create temporary database"""
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        yield path
        try:
            if os.path.exists(path):
                import time
                time.sleep(0.1)
                os.unlink(path)
        except PermissionError:
            pass
    
    def test_migration_creates_tables(self, temp_db):
        """Test that migration creates all expected tables"""
        manager = MigrationManager(temp_db)
        
        # Run migration
        success = manager.migrate()
        assert success == True
        
        # Verify tables exist
        results = manager.verify_tables()
        
        assert results['user_affinity'] == True
        assert results['user_facts'] == True
        assert results['episodes'] == True
        assert results['session_moods'] == True
        assert results['schema_migrations'] == True
    
    def test_migration_is_idempotent(self, temp_db):
        """Test that running migration twice doesn't break anything"""
        manager = MigrationManager(temp_db)
        
        # Run first time
        assert manager.migrate() == True
        
        # Run second time (should be no-op)
        assert manager.migrate() == True
        
        # Version should still be 1
        assert manager.get_current_version() == 1
    
    def test_dry_run_mode(self, temp_db):
        """Test dry run mode doesn't modify database"""
        manager = MigrationManager(temp_db)
        
        # Run in dry-run mode
        success = manager.migrate(dry_run=True)
        assert success == True
        
        # Version should still be 0 (nothing applied)
        assert manager.get_current_version() == 0
        
        # Tables should NOT exist
        results = manager.verify_tables()
        assert results['user_affinity'] == False


class TestTableConstraints:
    """Test database table constraints"""
    
    @pytest.fixture
    def migrated_db(self):
        """Create and migrate a temporary database"""
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        
        # Apply migration
        manager = MigrationManager(path)
        manager.migrate()
        
        yield path
        
        try:
            if os.path.exists(path):
                import time
                time.sleep(0.1)
                os.unlink(path)
        except PermissionError:
            pass
    
    def test_user_affinity_constraints(self, migrated_db):
        """Test user_affinity table constraints"""
        with sqlite3.connect(migrated_db) as conn:
            # Valid insert
            conn.execute(
                "INSERT INTO user_affinity (user_id, personality_name, affinity_points) "
                "VALUES ('user1', 'alicia', 50)"
            )
            conn.commit()
            
            # Test UNIQUE constraint (duplicate)
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO user_affinity (user_id, personality_name, affinity_points) "
                    "VALUES ('user1', 'alicia', 60)"
                )
            
            # Test CHECK constraint (affinity_points must be 0-100)
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO user_affinity (user_id, personality_name, affinity_points) "
                    "VALUES ('user2', 'alicia', 150)"
                )
            
            # Test CHECK constraint (negative affinity)
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO user_affinity (user_id, personality_name, affinity_points) "
                    "VALUES ('user3', 'alicia', -10)"
                )
    
    def test_user_facts_categories(self, migrated_db):
        """Test that user_facts only accepts valid categories"""
        with sqlite3.connect(migrated_db) as conn:
            # Valid category
            conn.execute(
                "INSERT INTO user_facts (user_id, category, fact_key, fact_value) "
                "VALUES ('user1', 'personal_info', 'name', '\"Diego\"')"
            )
            conn.commit()
            
            # Invalid category
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO user_facts (user_id, category, fact_key, fact_value) "
                    "VALUES ('user1', 'invalid_category', 'test', '\"value\"')"
                )
    
    def test_episodes_importance_range(self, migrated_db):
        """Test that episodes importance is constrained to 0-10"""
        with sqlite3.connect(migrated_db) as conn:
            # Valid importance
            conn.execute(
                "INSERT INTO episodes (user_id, episode_type, title, summary, importance, sentiment, timestamp) "
                "VALUES ('user1', 'emotional_moment', 'Test Episode', 'Summary', 5.0, 'positive', '2025-10-14 12:00:00')"
            )
            conn.commit()
            
            # Invalid importance (> 10)
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO episodes (user_id, episode_type, title, summary, importance, sentiment, timestamp) "
                    "VALUES ('user1', 'emotional_moment', 'Test', 'Summary', 15.0, 'positive', '2025-10-14 12:00:00')"
                )
            
            # Invalid importance (negative)
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO episodes (user_id, episode_type, title, summary, importance, sentiment, timestamp) "
                    "VALUES ('user1', 'emotional_moment', 'Test', 'Summary', -1.0, 'positive', '2025-10-14 12:00:00')"
                )
    
    def test_episode_types(self, migrated_db):
        """Test that episodes only accept valid types"""
        with sqlite3.connect(migrated_db) as conn:
            # Valid type
            conn.execute(
                "INSERT INTO episodes (user_id, episode_type, title, summary, importance, sentiment, timestamp) "
                "VALUES ('user1', 'milestone', 'Test', 'Summary', 5.0, 'positive', '2025-10-14 12:00:00')"
            )
            conn.commit()
            
            # Invalid type
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO episodes (user_id, episode_type, title, summary, importance, sentiment, timestamp) "
                    "VALUES ('user1', 'invalid_type', 'Test', 'Summary', 5.0, 'positive', '2025-10-14 12:00:00')"
                )
    
    def test_session_moods_constraints(self, migrated_db):
        """Test session_moods table constraints"""
        with sqlite3.connect(migrated_db) as conn:
            # Valid insert
            conn.execute(
                "INSERT INTO session_moods (session_id, user_id, current_mood, mood_intensity) "
                "VALUES ('session1', 'user1', 'happy', 0.8)"
            )
            conn.commit()
            
            # Test PRIMARY KEY constraint
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO session_moods (session_id, user_id, current_mood) "
                    "VALUES ('session1', 'user1', 'sad')"
                )
            
            # Test mood_intensity range
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO session_moods (session_id, user_id, mood_intensity) "
                    "VALUES ('session2', 'user1', 1.5)"
                )


class TestBackwardCompatibility:
    """Test that migrations don't break existing v1.0 tables"""
    
    @pytest.fixture
    def db_with_v1_tables(self):
        """Create database with v1.0-style tables"""
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        
        # Create v1.0 tables (simulate existing database)
        with sqlite3.connect(path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    role TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
        
        yield path
        
        try:
            if os.path.exists(path):
                import time
                time.sleep(0.1)
                os.unlink(path)
        except PermissionError:
            pass
    
    def test_migration_preserves_v1_tables(self, db_with_v1_tables):
        """Test that v1.1 migration doesn't modify v1.0 tables"""
        # Get v1.0 table schemas before migration
        with sqlite3.connect(db_with_v1_tables) as conn:
            cursor = conn.execute("SELECT sql FROM sqlite_master WHERE name='sessions'")
            v1_sessions_schema = cursor.fetchone()[0]
            
            cursor = conn.execute("SELECT sql FROM sqlite_master WHERE name='messages'")
            v1_messages_schema = cursor.fetchone()[0]
        
        # Run v1.1 migration
        manager = MigrationManager(db_with_v1_tables)
        assert manager.migrate() == True
        
        # Verify v1.0 schemas are unchanged
        with sqlite3.connect(db_with_v1_tables) as conn:
            cursor = conn.execute("SELECT sql FROM sqlite_master WHERE name='sessions'")
            assert cursor.fetchone()[0] == v1_sessions_schema
            
            cursor = conn.execute("SELECT sql FROM sqlite_master WHERE name='messages'")
            assert cursor.fetchone()[0] == v1_messages_schema
        
        # Verify v1.1 tables were added
        results = manager.verify_tables()
        assert all(results.values())  # All v1.1 tables should exist
    
    def test_existing_data_preserved(self, db_with_v1_tables):
        """Test that existing data is preserved during migration"""
        # Insert test data
        with sqlite3.connect(db_with_v1_tables) as conn:
            conn.execute(
                "INSERT INTO sessions (id, user_id) VALUES ('session1', 'user1')"
            )
            conn.execute(
                "INSERT INTO messages (id, session_id, content, role) "
                "VALUES ('msg1', 'session1', 'Hello', 'user')"
            )
            conn.commit()
        
        # Run migration
        manager = MigrationManager(db_with_v1_tables)
        assert manager.migrate() == True
        
        # Verify data still exists
        with sqlite3.connect(db_with_v1_tables) as conn:
            cursor = conn.execute("SELECT * FROM sessions WHERE id='session1'")
            assert cursor.fetchone() is not None
            
            cursor = conn.execute("SELECT * FROM messages WHERE id='msg1'")
            assert cursor.fetchone() is not None


class TestMigrationHistory:
    """Test migration history tracking"""
    
    @pytest.fixture
    def temp_db(self):
        """Create temporary database"""
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        yield path
        try:
            if os.path.exists(path):
                import time
                time.sleep(0.1)
                os.unlink(path)
        except PermissionError:
            pass
    
    def test_migration_history_tracking(self, temp_db):
        """Test that migrations are tracked in history"""
        manager = MigrationManager(temp_db)
        
        # Initially no history
        history = manager.get_migration_history()
        assert len(history) == 0
        
        # Apply migration
        manager.migrate()
        
        # Now should have history
        history = manager.get_migration_history()
        assert len(history) == 1
        assert history[0]['version'] == 1
        assert history[0]['name'] == '001_v1_1_base_tables'


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

