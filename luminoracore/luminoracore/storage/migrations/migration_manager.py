"""
Migration Manager for LuminoraCore v1.1

Handles database schema migrations safely for Core tables.

NOTE: This is separate from SDK's session storage. Core manages its own
tables for personality-specific data (affinity, facts, episodes).
"""

import sqlite3
import hashlib
from pathlib import Path
from typing import List, Tuple, Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class MigrationError(Exception):
    """Exception raised for migration errors"""
    pass


class MigrationManager:
    """Manages database schema migrations for LuminoraCore Core"""
    
    def __init__(self, db_path: str):
        """
        Initialize migration manager
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self.migrations_dir = Path(__file__).parent / "versions"
        
        # Verify migrations directory exists
        if not self.migrations_dir.exists():
            raise MigrationError(f"Migrations directory not found: {self.migrations_dir}")
    
    def get_current_version(self) -> int:
        """
        Get current schema version from database
        
        Returns:
            Current version number (0 if table doesn't exist)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT MAX(version) FROM schema_migrations"
                )
                result = cursor.fetchone()
                version = result[0] if result[0] is not None else 0
                logger.info(f"Current schema version: {version}")
                return version
        except sqlite3.OperationalError:
            # Table doesn't exist yet (fresh database)
            logger.info("schema_migrations table not found - assuming version 0")
            return 0
        except Exception as e:
            logger.error(f"Error checking schema version: {e}")
            raise MigrationError(f"Failed to check schema version: {e}")
    
    def get_pending_migrations(self) -> List[Tuple[int, Path]]:
        """
        Get list of pending migrations to apply
        
        Returns:
            List of (version, sql_file_path) tuples
        """
        current_version = self.get_current_version()
        
        migrations = []
        sql_files = list(self.migrations_dir.glob("*.sql"))
        
        if not sql_files:
            logger.warning(f"No migration files found in {self.migrations_dir}")
        
        for sql_file in sorted(sql_files):
            try:
                # Extract version from filename: 001_name.sql -> 1
                version_str = sql_file.stem.split("_")[0]
                version = int(version_str)
                
                if version > current_version:
                    migrations.append((version, sql_file))
                    logger.debug(f"Found pending migration: {sql_file.name} (v{version})")
            except (ValueError, IndexError):
                logger.warning(f"Skipping invalid migration filename: {sql_file.name}")
                continue
        
        return sorted(migrations)
    
    def apply_migration(self, version: int, sql_file: Path, dry_run: bool = False) -> bool:
        """
        Apply a single migration
        
        Args:
            version: Migration version number
            sql_file: Path to SQL file
            dry_run: If True, show what would be done without applying
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"{'[DRY RUN] ' if dry_run else ''}Applying migration {version}: {sql_file.name}")
        
        try:
            # Read SQL file
            sql_content = sql_file.read_text(encoding='utf-8')
            
            # Calculate checksum for verification
            checksum = hashlib.sha256(sql_content.encode()).hexdigest()
            
            if dry_run:
                logger.info(f"[DRY RUN] Would execute SQL from {sql_file.name}")
                logger.info(f"[DRY RUN] Checksum: {checksum[:16]}...")
                return True
            
            # Apply migration
            with sqlite3.connect(self.db_path) as conn:
                # Enable foreign keys
                conn.execute("PRAGMA foreign_keys = ON")
                
                # Execute migration SQL
                logger.debug("Executing SQL script...")
                conn.executescript(sql_content)
                
                # Update checksum in migration record
                conn.execute(
                    "UPDATE schema_migrations SET checksum = ? WHERE version = ?",
                    (f"sha256:{checksum[:16]}", version)
                )
                
                conn.commit()
            
            logger.info(f"✅ Migration {version} applied successfully")
            return True
            
        except sqlite3.Error as e:
            logger.error(f"❌ Migration {version} failed (SQL error): {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Migration {version} failed: {e}")
            return False
    
    def migrate(self, target_version: int = None, dry_run: bool = False) -> bool:
        """
        Run all pending migrations up to target version
        
        Args:
            target_version: Version to migrate to (None = latest)
            dry_run: If True, show what would be done without applying
            
        Returns:
            True if all migrations successful
        """
        pending = self.get_pending_migrations()
        
        if not pending:
            logger.info("✅ Database is up to date (no pending migrations)")
            return True
        
        logger.info(f"Found {len(pending)} pending migration(s)")
        
        if dry_run:
            logger.info("[DRY RUN] Would apply the following migrations:")
            for version, sql_file in pending:
                if target_version and version > target_version:
                    logger.info(f"  [SKIP] v{version}: {sql_file.name} (beyond target)")
                else:
                    logger.info(f"  [APPLY] v{version}: {sql_file.name}")
            return True
        
        applied_count = 0
        for version, sql_file in pending:
            if target_version and version > target_version:
                logger.info(f"Stopping at target version {target_version}")
                break
            
            if not self.apply_migration(version, sql_file, dry_run=False):
                logger.error(f"Migration stopped at version {version} due to error")
                if applied_count > 0:
                    logger.warning(f"⚠️ {applied_count} migration(s) were applied before failure")
                return False
            
            applied_count += 1
        
        logger.info(f"✅ All {applied_count} migration(s) applied successfully")
        return True
    
    def rollback(self, target_version: int) -> bool:
        """
        Rollback migrations to target version
        
        Args:
            target_version: Version to rollback to
            
        Returns:
            True if rollback successful
        """
        current_version = self.get_current_version()
        
        if target_version >= current_version:
            logger.warning(f"Target version {target_version} >= current {current_version}, nothing to rollback")
            return True
        
        logger.warning(f"⚠️ Rolling back from v{current_version} to v{target_version}")
        logger.warning("⚠️ THIS WILL DELETE DATA - Make sure you have backups!")
        
        # For now, manual rollback (safety measure)
        logger.error("Automatic rollback not implemented - use manual SQL scripts")
        logger.info(f"See: rollback_{current_version:03d}.sql")
        return False
    
    def verify_tables(self) -> Dict[str, bool]:
        """
        Verify that all expected v1.1 tables exist
        
        Returns:
            Dict with table names and existence status
        """
        expected_tables = [
            'user_affinity',
            'user_facts',
            'episodes',
            'session_moods',
            'schema_migrations'
        ]
        
        results = {}
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                )
                existing_tables = {row[0] for row in cursor.fetchall()}
                
                for table in expected_tables:
                    results[table] = table in existing_tables
                
                logger.info(f"Table verification: {sum(results.values())}/{len(results)} tables exist")
        except Exception as e:
            logger.error(f"Error verifying tables: {e}")
            raise MigrationError(f"Table verification failed: {e}")
        
        return results
    
    def get_migration_history(self) -> List[Dict[str, Any]]:
        """
        Get history of applied migrations
        
        Returns:
            List of migration records
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    "SELECT version, name, applied_at, description FROM schema_migrations ORDER BY version"
                )
                
                history = []
                for row in cursor.fetchall():
                    history.append({
                        'version': row['version'],
                        'name': row['name'],
                        'applied_at': row['applied_at'],
                        'description': row['description'] if 'description' in row.keys() else None
                    })
                
                return history
        except sqlite3.OperationalError:
            # Table doesn't exist
            return []
        except Exception as e:
            logger.error(f"Error getting migration history: {e}")
            return []


# ============================================================================
# CLI INTERFACE (for manual testing)
# ============================================================================

def main():
    """Test migration manager from command line"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='LuminoraCore Migration Manager')
    parser.add_argument('db_path', help='Path to SQLite database')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done')
    parser.add_argument('--target', type=int, help='Target version')
    parser.add_argument('--history', action='store_true', help='Show migration history')
    
    args = parser.parse_args()
    
    try:
        manager = MigrationManager(args.db_path)
        
        if args.history:
            print("\n📜 Migration History:")
            history = manager.get_migration_history()
            if history:
                for record in history:
                    print(f"  v{record['version']}: {record['name']} (applied: {record['applied_at']})")
            else:
                print("  No migrations applied yet")
            sys.exit(0)
        
        print(f"\n📊 Current Status:")
        print(f"  Database: {args.db_path}")
        print(f"  Current version: {manager.get_current_version()}")
        print(f"  Pending migrations: {len(manager.get_pending_migrations())}")
        
        if args.dry_run:
            print("\n🔍 DRY RUN MODE - No changes will be made")
        
        # Run migrations
        success = manager.migrate(target_version=args.target, dry_run=args.dry_run)
        
        if success:
            if not args.dry_run:
                print("\n✅ Migration successful!")
                
                # Verify tables
                print("\n📊 Table Verification:")
                results = manager.verify_tables()
                for table, exists in sorted(results.items()):
                    status = "✅" if exists else "❌"
                    print(f"  {status} {table}")
                
                # Show history
                print("\n📜 Migration History:")
                history = manager.get_migration_history()
                for record in history:
                    print(f"  v{record['version']}: {record['name']}")
        else:
            print("\n❌ Migration failed!")
            sys.exit(1)
            
    except MigrationError as e:
        print(f"\n❌ Migration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

