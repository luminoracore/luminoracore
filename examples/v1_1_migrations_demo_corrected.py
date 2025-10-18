"""
LuminoraCore v1.1 - Database Migrations Demo (Corrected)

Demonstrates the actual MigrationManager methods available.
"""

import os
from luminoracore.storage.migrations import MigrationManager, MigrationError


def main():
    """Corrected migrations demonstration."""
    
    print("=" * 80)
    print("LuminoraCore v1.1 - Database Migrations Demo (Corrected)")
    print("=" * 80)
    
    # ========================================
    # 1. MIGRATION MANAGER INITIALIZATION
    # ========================================
    
    print("\n1. MIGRATION MANAGER INITIALIZATION")
    print("-" * 80)
    
    # Create test database path
    test_db = "test_migrations_corrected.db"
    
    try:
        # Initialize migration manager
        migration_manager = MigrationManager(test_db)
        print(f"Migration manager initialized with database: {test_db}")
        
        # Check if migrations directory exists
        migrations_dir = migration_manager.migrations_dir
        print(f"Migrations directory: {migrations_dir}")
        print(f"Directory exists: {migrations_dir.exists()}")
        
    except Exception as e:
        print(f"ERROR initializing migration manager: {e}")
        return
    
    # ========================================
    # 2. CURRENT VERSION CHECK
    # ========================================
    
    print("\n\n2. CURRENT VERSION CHECK")
    print("-" * 80)
    
    try:
        current_version = migration_manager.get_current_version()
        print(f"Current database version: {current_version}")
        
        if current_version == 0:
            print("   Database is fresh (no migrations applied)")
        else:
            print(f"   Database has {current_version} migrations applied")
            
    except Exception as e:
        print(f"ERROR checking current version: {e}")
    
    # ========================================
    # 3. PENDING MIGRATIONS
    # ========================================
    
    print("\n\n3. PENDING MIGRATIONS")
    print("-" * 80)
    
    try:
        pending_migrations = migration_manager.get_pending_migrations()
        print(f"Pending migrations count: {len(pending_migrations)}")
        
        if pending_migrations:
            print("\nPending migrations:")
            for version, migration_path in pending_migrations:
                print(f"   Version {version}: {migration_path.name}")
        else:
            print("   No pending migrations")
            
    except Exception as e:
        print(f"ERROR getting pending migrations: {e}")
    
    # ========================================
    # 4. DRY RUN MIGRATIONS
    # ========================================
    
    print("\n\n4. DRY RUN MIGRATIONS")
    print("-" * 80)
    
    try:
        print("Performing dry run migration...")
        dry_run_result = migration_manager.migrate(dry_run=True)
        print(f"Dry run result: {dry_run_result}")
        
    except Exception as e:
        print(f"ERROR in dry run migration: {e}")
    
    # ========================================
    # 5. APPLY MIGRATIONS (if any pending)
    # ========================================
    
    print("\n\n5. APPLY MIGRATIONS")
    print("-" * 80)
    
    try:
        pending_migrations = migration_manager.get_pending_migrations()
        
        if pending_migrations:
            print(f"Applying {len(pending_migrations)} pending migrations...")
            result = migration_manager.migrate()
            print(f"Migration result: {result}")
            
            # Check new version
            new_version = migration_manager.get_current_version()
            print(f"New database version: {new_version}")
            
        else:
            print("No pending migrations to apply")
            
    except Exception as e:
        print(f"ERROR applying migrations: {e}")
    
    # ========================================
    # 6. VERIFY TABLES
    # ========================================
    
    print("\n\n6. VERIFY TABLES")
    print("-" * 80)
    
    try:
        table_results = migration_manager.verify_tables()
        print("Table verification results:")
        
        for table, exists in table_results.items():
            status = "EXISTS" if exists else "MISSING"
            print(f"   {table}: {status}")
            
    except Exception as e:
        print(f"ERROR verifying tables: {e}")
    
    # ========================================
    # 7. MIGRATION HISTORY
    # ========================================
    
    print("\n\n7. MIGRATION HISTORY")
    print("-" * 80)
    
    try:
        history = migration_manager.get_migration_history()
        print(f"Migration history count: {len(history)}")
        
        if history:
            print("\nMigration history:")
            for record in history:
                print(f"   Version {record['version']}: {record['name']}")
                print(f"     Applied at: {record['applied_at']}")
                if record.get('description'):
                    print(f"     Description: {record['description']}")
        else:
            print("   No migration history available")
            
    except Exception as e:
        print(f"ERROR getting migration history: {e}")
    
    # ========================================
    # 8. ROLLBACK DEMONSTRATION
    # ========================================
    
    print("\n\n8. ROLLBACK DEMONSTRATION")
    print("-" * 80)
    
    try:
        current_version = migration_manager.get_current_version()
        
        if current_version > 0:
            print(f"Current version: {current_version}")
            print("Attempting rollback...")
            
            # Note: rollback is not fully implemented for safety
            rollback_result = migration_manager.rollback(target_version=0)
            print(f"Rollback result: {rollback_result}")
            
        else:
            print("No migrations to rollback")
            
    except Exception as e:
        print(f"ERROR in rollback: {e}")
    
    # ========================================
    # 9. CLEANUP
    # ========================================
    
    print("\n\n9. CLEANUP")
    print("-" * 80)
    
    try:
        # Clean up test database
        if os.path.exists(test_db):
            os.remove(test_db)
            print(f"Test database {test_db} removed")
        else:
            print(f"Test database {test_db} not found")
            
    except Exception as e:
        print(f"ERROR during cleanup: {e}")
    
    print("\n" + "=" * 80)
    print("Database migrations demonstration completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
