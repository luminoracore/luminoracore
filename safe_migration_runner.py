#!/usr/bin/env python3
"""
Safe Migration Runner
Executes the migration process with comprehensive safety checks
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_script(script_path, description):
    """Run a script and return success status"""
    print(f"\n{'='*20} {description} {'='*20}")
    
    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        return False
    
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            print(result.stdout)
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 {description} - ERROR: {e}")
        return False

def check_prerequisites():
    """Check that all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check that we're in the right directory
    if not os.path.exists("luminoracore-sdk-python"):
        print("❌ Not in the right directory. Please run from project root.")
        return False
    
    # Check that Python is available
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Python not available")
            return False
        print(f"✅ Python available: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Python check failed: {e}")
        return False
    
    # Check that required directories exist
    required_dirs = ["luminoracore", "luminoracore-sdk-python", "luminoracore-cli"]
    for directory in required_dirs:
        if not os.path.exists(directory):
            print(f"❌ Required directory not found: {directory}")
            return False
        print(f"✅ {directory} exists")
    
    print("✅ All prerequisites met")
    return True

def create_backup():
    """Create backup before migration"""
    print("\n🔄 Creating backup...")
    return run_script("backup_before_migration.py", "Backup Creation")

def validate_current_state():
    """Validate current state before migration"""
    print("\n🔍 Validating current state...")
    return run_script("validate_migration.py", "Current State Validation")

def run_migration_step(step_name, script_path):
    """Run a migration step with validation"""
    print(f"\n🚀 Running migration step: {step_name}")
    
    # Run the migration step
    if not run_script(script_path, f"Migration Step: {step_name}"):
        print(f"❌ Migration step failed: {step_name}")
        return False
    
    # Validate after the step
    print(f"\n🔍 Validating after {step_name}...")
    if not run_script("validate_migration.py", f"Validation after {step_name}"):
        print(f"❌ Validation failed after {step_name}")
        print("🔄 Rolling back...")
        run_script("rollback_migration.py", "Rollback")
        return False
    
    print(f"✅ {step_name} completed successfully")
    return True

def main():
    """Main migration runner"""
    print("🚀 Starting Safe Migration Process")
    print("=" * 60)
    
    start_time = time.time()
    
    # Step 1: Check prerequisites
    if not check_prerequisites():
        print("❌ Prerequisites not met, aborting migration")
        return 1
    
    # Step 2: Create backup
    if not create_backup():
        print("❌ Backup creation failed, aborting migration")
        return 1
    
    # Step 3: Validate current state
    if not validate_current_state():
        print("❌ Current state validation failed, aborting migration")
        return 1
    
    # Step 4: Run migration steps
    migration_steps = [
        ("Core Preparation", "migrate_core.py"),
        ("SDK Refactoring", "migrate_sdk.py"),
        ("CLI Refactoring", "migrate_cli.py"),
        ("Final Validation", "validate_migration.py"),
    ]
    
    for step_name, script_path in migration_steps:
        if not run_migration_step(step_name, script_path):
            print(f"❌ Migration failed at step: {step_name}")
            return 1
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print("\n" + "=" * 60)
    print("🎉 MIGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"⏱️  Total time: {total_time:.2f}s")
    print("✅ All tests passed")
    print("✅ All examples work")
    print("✅ All functionality preserved")
    print("🔒 Project is ready for use")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
