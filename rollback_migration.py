#!/usr/bin/env python3
"""
Rollback Migration Script
Automatically rolls back to the last working state if migration fails
"""

import os
import shutil
import glob
from pathlib import Path

def find_latest_backup():
    """Find the latest backup directory"""
    backup_pattern = "backup_before_migration_*"
    backup_dirs = glob.glob(backup_pattern)
    
    if not backup_dirs:
        print("❌ No backup directories found!")
        return None
    
    # Sort by modification time (newest first)
    backup_dirs.sort(key=os.path.getmtime, reverse=True)
    latest_backup = backup_dirs[0]
    
    print(f"📁 Found latest backup: {latest_backup}")
    return latest_backup

def rollback_from_backup(backup_dir):
    """Rollback from backup directory"""
    print(f"🔄 Rolling back from: {backup_dir}")
    
    if not os.path.exists(backup_dir):
        print(f"❌ Backup directory not found: {backup_dir}")
        return False
    
    # Directories to restore
    directories_to_restore = [
        "luminoracore",
        "luminoracore-sdk-python", 
        "luminoracore-cli",
        "examples",
        "tests"
    ]
    
    # Files to restore
    files_to_restore = [
        "README.md",
        "requirements.txt",
        "setup.py",
        "pyproject.toml"
    ]
    
    # Remove current directories if they exist
    for directory in directories_to_restore:
        if os.path.exists(directory):
            print(f"🗑️  Removing current {directory}...")
            shutil.rmtree(directory)
            print(f"✅ {directory} removed")
    
    # Restore directories
    for directory in directories_to_restore:
        backup_path = os.path.join(backup_dir, directory)
        if os.path.exists(backup_path):
            print(f"📁 Restoring {directory}...")
            shutil.copytree(backup_path, directory)
            print(f"✅ {directory} restored")
        else:
            print(f"⚠️  {directory} not found in backup, skipping")
    
    # Restore files
    for file in files_to_restore:
        backup_path = os.path.join(backup_dir, file)
        if os.path.exists(backup_path):
            print(f"📄 Restoring {file}...")
            shutil.copy2(backup_path, file)
            print(f"✅ {file} restored")
        else:
            print(f"⚠️  {file} not found in backup, skipping")
    
    return True

def verify_rollback():
    """Verify that rollback was successful"""
    print("\n🔍 Verifying rollback...")
    
    # Check that key directories exist
    key_directories = ["luminoracore", "luminoracore-sdk-python", "luminoracore-cli"]
    for directory in key_directories:
        if os.path.exists(directory):
            print(f"✅ {directory} exists")
        else:
            print(f"❌ {directory} missing")
            return False
    
    # Check that key files exist
    key_files = ["README.md"]
    for file in key_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            return False
    
    # Test that SDK can be imported
    try:
        import sys
        sys.path.insert(0, "luminoracore-sdk-python")
        from luminoracore_sdk import LuminoraCoreClient
        print("✅ SDK can be imported")
    except ImportError as e:
        print(f"❌ SDK import failed: {e}")
        return False
    
    print("✅ Rollback verification completed successfully")
    return True

def test_functionality():
    """Test that functionality works after rollback"""
    print("\n🧪 Testing functionality after rollback...")
    
    try:
        # Test basic imports
        import sys
        sys.path.insert(0, "luminoracore-sdk-python")
        from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
        from luminoracore_sdk.session import InMemoryStorageV11
        
        # Test client creation
        client = LuminoraCoreClient()
        storage = InMemoryStorageV11()
        client_v11 = LuminoraCoreClientV11(client, storage_v11=storage)
        
        print("✅ Basic functionality works")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def main():
    """Main rollback function"""
    print("🚀 Starting rollback...")
    print("=" * 50)
    
    # Find latest backup
    backup_dir = find_latest_backup()
    if not backup_dir:
        print("❌ No backup found, cannot rollback!")
        return 1
    
    # Rollback from backup
    if not rollback_from_backup(backup_dir):
        print("❌ Rollback failed!")
        return 1
    
    # Verify rollback
    if not verify_rollback():
        print("❌ Rollback verification failed!")
        return 1
    
    # Test functionality
    if not test_functionality():
        print("❌ Functionality test failed!")
        return 1
    
    print("\n🎉 Rollback completed successfully!")
    print("🔒 Project has been restored to the last working state")
    print("📋 You can now continue with development")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
