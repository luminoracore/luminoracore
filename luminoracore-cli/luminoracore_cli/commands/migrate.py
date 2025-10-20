"""
Migrate command for LuminoraCore CLI

Runs database migrations for v1.1 tables.
"""

import click
import sys
from pathlib import Path

# Import Core migration manager
try:
    # Add luminoracore to path
    core_path = Path(__file__).parent.parent.parent.parent / "luminoracore"
    if core_path.exists():
        sys.path.insert(0, str(core_path))
    
    from luminoracore.storage.migrations.migration_manager import MigrationManager, MigrationError
except ImportError as e:
    click.echo(f"Error: Cannot import MigrationManager: {e}", err=True)
    MigrationManager = None
    MigrationError = Exception


@click.command()
@click.argument('db_path', type=click.Path(), required=True)
@click.option('--dry-run', is_flag=True, help='Show what would be done without applying')
@click.option('--target', type=int, help='Target version to migrate to')
@click.option('--status', is_flag=True, help='Show migration status')
@click.option('--history', is_flag=True, help='Show migration history')
def migrate(db_path, dry_run, target, status, history):
    """
    Run database migrations for v1.1
    
    Examples:
        luminora-cli migrate                    # Run all pending migrations
        luminora-cli migrate --dry-run          # Preview migrations
        luminora-cli migrate --target 1         # Migrate to specific version
        luminora-cli migrate --status           # Show current status
        luminora-cli migrate --history          # Show migration history
    """
    if not MigrationManager:
        click.echo("❌ Error: MigrationManager not available", err=True)
        click.echo("   Make sure luminoracore package is installed", err=True)
        sys.exit(1)
    
    try:
        manager = MigrationManager(db_path)
        
        # Show status
        if status:
            current_version = manager.get_current_version()
            pending = manager.get_pending_migrations()
            
            click.echo("\n📊 Migration Status:")
            click.echo(f"  Database: {db_path}")
            click.echo(f"  Current version: {current_version}")
            click.echo(f"  Pending migrations: {len(pending)}")
            
            if pending:
                click.echo("\n  Pending:")
                for version, sql_file in pending:
                    click.echo(f"    - v{version}: {sql_file.name}")
            
            sys.exit(0)
        
        # Show history
        if history:
            hist = manager.get_migration_history()
            
            click.echo("\n📜 Migration History:")
            if hist:
                for record in hist:
                    click.echo(f"  v{record['version']}: {record['name']}")
                    click.echo(f"    Applied: {record['applied_at']}")
                    if record.get('description'):
                        click.echo(f"    Description: {record['description']}")
            else:
                click.echo("  No migrations applied yet")
            
            sys.exit(0)
        
        # Run migrations
        if dry_run:
            click.echo("\n🔍 DRY RUN MODE - No changes will be made\n")
        
        success = manager.migrate(target_version=target, dry_run=dry_run)
        
        if success:
            if not dry_run:
                click.echo("\n✅ Migration successful!")
                
                # Verify tables
                click.echo("\n📊 Table Verification:")
                results = manager.verify_tables()
                for table, exists in sorted(results.items()):
                    status_icon = "✅" if exists else "❌"
                    click.echo(f"  {status_icon} {table}")
                
                # Show history
                click.echo("\n📜 Applied Migrations:")
                hist = manager.get_migration_history()
                for record in hist:
                    click.echo(f"  v{record['version']}: {record['name']}")
        else:
            click.echo("\n❌ Migration failed!", err=True)
            sys.exit(1)
    
    except MigrationError as e:
        click.echo(f"\n❌ Migration error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"\n❌ Unexpected error: {e}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    migrate()

