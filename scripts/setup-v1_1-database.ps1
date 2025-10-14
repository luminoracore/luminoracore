# Setup LuminoraCore v1.1 Database
# PowerShell version for Windows

param(
    [string]$DbPath = "luminora.db"
)

$ErrorActionPreference = "Stop"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "LuminoraCore v1.1 Database Setup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

Write-Host "`nDatabase path: $DbPath" -ForegroundColor Yellow

# Check if Core is installed
try {
    python -c "import luminoracore" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "luminoracore not installed"
    }
}
catch {
    Write-Host "`n✗ Error: luminoracore not installed" -ForegroundColor Red
    Write-Host "Install: cd luminoracore; pip install -e ." -ForegroundColor Yellow
    exit 1
}

Write-Host "`nRunning v1.1 migrations..." -ForegroundColor Yellow

# Run migrations using Python
$pythonScript = @"
import sys
from pathlib import Path

# Import migration manager
try:
    from luminoracore.storage.migrations.migration_manager import MigrationManager, MigrationError
except ImportError as e:
    print(f'Error importing MigrationManager: {e}')
    sys.exit(1)

# Run migrations
try:
    manager = MigrationManager('$DbPath')
    
    # Get pending
    current = manager.get_current_version()
    pending = manager.get_pending_migrations()
    
    print(f'Current version: {current}')
    print(f'Pending migrations: {len(pending)}')
    
    if pending:
        print('\nApplying migrations...')
        for version, sql_file in pending:
            print(f'  - v{version}: {sql_file.name}')
        
        success = manager.migrate()
        
        if success:
            print('\n✓ Migrations applied successfully')
            
            # Verify tables
            results = manager.verify_tables()
            print('\nTable verification:')
            for table, exists in sorted(results.items()):
                status = '✓' if exists else '✗'
                print(f'  {status} {table}')
        else:
            print('\n✗ Migration failed')
            sys.exit(1)
    else:
        print('\n✓ Database is up to date')
    
except MigrationError as e:
    print(f'\n✗ Migration error: {e}')
    sys.exit(1)
except Exception as e:
    print(f'\n✗ Unexpected error: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"@

python -c $pythonScript

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n======================================" -ForegroundColor Cyan
    Write-Host "Database setup complete!" -ForegroundColor Green
    Write-Host "======================================" -ForegroundColor Cyan
    
    Write-Host "`nNext steps:" -ForegroundColor Blue
    Write-Host "  1. Enable features: Edit config/features.json" -ForegroundColor White
    Write-Host "  2. Test: python examples/v1_1_quick_example.py" -ForegroundColor White
    Write-Host "  3. Use CLI: luminora-cli migrate --status" -ForegroundColor White
}
else {
    Write-Host "`nDatabase setup failed" -ForegroundColor Red
    exit 1
}

