#!/usr/bin/env python3
"""
Backup Before Migration Script
Creates complete backups before starting the restructure
"""

import os
import shutil
import datetime
from pathlib import Path

def create_backup():
    """Create complete backup of the project"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_before_migration_{timestamp}"
    
    print(f"🔄 Creating backup: {backup_dir}")
    
    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)
    
    # Directories to backup
    directories_to_backup = [
        "luminoracore",
        "luminoracore-sdk-python", 
        "luminoracore-cli",
        "examples",
        "tests"
    ]
    
    # Files to backup
    files_to_backup = [
        "README.md",
        "requirements.txt",
        "setup.py",
        "pyproject.toml"
    ]
    
    # Backup directories
    for directory in directories_to_backup:
        if os.path.exists(directory):
            print(f"📁 Backing up {directory}...")
            shutil.copytree(directory, os.path.join(backup_dir, directory))
            print(f"✅ {directory} backed up successfully")
        else:
            print(f"⚠️  {directory} not found, skipping")
    
    # Backup files
    for file in files_to_backup:
        if os.path.exists(file):
            print(f"📄 Backing up {file}...")
            shutil.copy2(file, os.path.join(backup_dir, file))
            print(f"✅ {file} backed up successfully")
        else:
            print(f"⚠️  {file} not found, skipping")
    
    # Create backup info file
    backup_info = f"""
Backup created: {datetime.datetime.now().isoformat()}
Purpose: Before migration restructure
Directories backed up: {len([d for d in directories_to_backup if os.path.exists(d)])}
Files backed up: {len([f for f in files_to_backup if os.path.exists(f)])}

To restore from backup:
1. Stop any running processes
2. Remove current directories: rm -rf luminoracore luminoracore-sdk-python luminoracore-cli
3. Copy from backup: cp -r {backup_dir}/* .
4. Test that everything works: python validate_migration.py
"""
    
    with open(os.path.join(backup_dir, "BACKUP_INFO.txt"), "w") as f:
        f.write(backup_info)
    
    print(f"\n✅ Backup completed: {backup_dir}")
    print(f"📋 Backup info saved to: {backup_dir}/BACKUP_INFO.txt")
    
    return backup_dir

def verify_backup(backup_dir):
    """Verify that backup is complete and valid"""
    print(f"\n🔍 Verifying backup: {backup_dir}")
    
    # Check that backup directory exists
    if not os.path.exists(backup_dir):
        print(f"❌ Backup directory not found: {backup_dir}")
        return False
    
    # Check that key directories are backed up
    key_directories = ["luminoracore", "luminoracore-sdk-python", "luminoracore-cli"]
    for directory in key_directories:
        backup_path = os.path.join(backup_dir, directory)
        if os.path.exists(backup_path):
            print(f"✅ {directory} found in backup")
        else:
            print(f"❌ {directory} missing from backup")
            return False
    
    # Check that key files are backed up
    key_files = ["README.md"]
    for file in key_files:
        backup_path = os.path.join(backup_dir, file)
        if os.path.exists(backup_path):
            print(f"✅ {file} found in backup")
        else:
            print(f"❌ {file} missing from backup")
            return False
    
    print("✅ Backup verification completed successfully")
    return True

def test_backup_restore(backup_dir):
    """Test that backup can be restored"""
    print(f"\n🧪 Testing backup restore: {backup_dir}")
    
    # Create test restore directory
    test_restore_dir = f"test_restore_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        # Copy backup to test directory
        shutil.copytree(backup_dir, test_restore_dir)
        print(f"✅ Backup copied to test directory: {test_restore_dir}")
        
        # Test that key files can be imported
        import sys
        sys.path.insert(0, os.path.join(test_restore_dir, "luminoracore-sdk-python"))
        
        try:
            from luminoracore_sdk import LuminoraCoreClient
            print("✅ SDK can be imported from backup")
        except ImportError as e:
            print(f"❌ SDK import failed: {e}")
            return False
        
        # Clean up test directory
        shutil.rmtree(test_restore_dir)
        print("✅ Test restore completed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Test restore failed: {e}")
        return False

def main():
    """Create backup and verify it"""
    print("🚀 Starting backup before migration...")
    print("=" * 50)
    
    # Create backup
    backup_dir = create_backup()
    
    # Verify backup
    if not verify_backup(backup_dir):
        print("❌ Backup verification failed!")
        return 1
    
    # Test backup restore
    if not test_backup_restore(backup_dir):
        print("❌ Backup restore test failed!")
        return 1
    
    print("\n🎉 Backup completed successfully!")
    print(f"📁 Backup location: {backup_dir}")
    print("🔒 You can now safely proceed with migration")
    print("📋 To restore from backup, see BACKUP_INFO.txt in backup directory")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
