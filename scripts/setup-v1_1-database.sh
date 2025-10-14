#!/bin/bash

# Setup LuminoraCore v1.1 Database
# Creates and migrates v1.1 tables

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}LuminoraCore v1.1 Database Setup${NC}"
echo "========================================"

# Default database path
DB_PATH="${1:-luminora.db}"

echo -e "\n${YELLOW}Database path:${NC} $DB_PATH"

# Check if Core is installed
if ! python -c "import luminoracore" 2>/dev/null; then
    echo -e "${RED}Error: luminoracore not installed${NC}"
    echo "Install: cd luminoracore && pip install -e ."
    exit 1
fi

# Run migrations
echo -e "\n${YELLOW}Running v1.1 migrations...${NC}"

python << EOF
import sys
from pathlib import Path

# Import migration manager
try:
    from luminoracore.storage.migrations.migration_manager import MigrationManager, MigrationError
except ImportError as e:
    print(f"Error importing MigrationManager: {e}")
    sys.exit(1)

# Run migrations
try:
    manager = MigrationManager("$DB_PATH")
    
    # Get pending
    current = manager.get_current_version()
    pending = manager.get_pending_migrations()
    
    print(f"Current version: {current}")
    print(f"Pending migrations: {len(pending)}")
    
    if pending:
        print("\nApplying migrations...")
        for version, sql_file in pending:
            print(f"  - v{version}: {sql_file.name}")
        
        success = manager.migrate()
        
        if success:
            print("\n✓ Migrations applied successfully")
            
            # Verify tables
            results = manager.verify_tables()
            print("\nTable verification:")
            for table, exists in sorted(results.items()):
                status = "✓" if exists else "✗"
                print(f"  {status} {table}")
        else:
            print("\n✗ Migration failed")
            sys.exit(1)
    else:
        print("\n✓ Database is up to date")
    
except MigrationError as e:
    print(f"\n✗ Migration error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\n✗ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}Database setup complete!${NC}"
    echo -e "\n${BLUE}Next steps:${NC}"
    echo "  1. Enable features: Edit config/features.json"
    echo "  2. Test: python examples/v1_1_quick_example.py"
    echo "  3. Use CLI: luminora-cli migrate --status"
else
    echo -e "\n${RED}Database setup failed${NC}"
    exit 1
fi

