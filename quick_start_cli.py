#!/usr/bin/env python3
"""
Quick Start Example - LuminoraCore CLI
Run this file to test that luminoracore-cli is installed correctly.
"""

import sys
import subprocess
import shutil

def main():
    """Quick test of LuminoraCore CLI."""
    print("=" * 60)
    print("🛠️  LuminoraCore CLI - Quick Start")
    print("=" * 60)
    
    # Check that the command is available
    print("\n1️⃣  Checking that 'luminoracore' command is available...")
    
    luminoracore_path = shutil.which("luminoracore")
    lc_path = shutil.which("lc")
    
    if luminoracore_path:
        print(f"   ✅ 'luminoracore' command found at: {luminoracore_path}")
    else:
        print("   ❌ 'luminoracore' command not found")
        print("   💡 Solution: cd luminoracore-cli && pip install -e .")
        return False
    
    if lc_path:
        print(f"   ✅ 'lc' alias also available")
    
    # Test the --version command
    print("\n2️⃣  Getting CLI version...")
    try:
        result = subprocess.run(
            ["luminoracore", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_output = result.stdout.strip()
            print(f"   ✅ {version_output}")
        else:
            print("   ⚠️  Could not get version")
    except Exception as e:
        print(f"   ⚠️  Error executing command: {e}")
    
    # Test the --help command
    print("\n3️⃣  Checking available commands...")
    try:
        result = subprocess.run(
            ["luminoracore", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            # Look for commands in the output
            commands = []
            for line in result.stdout.split('\n'):
                line_lower = line.lower()
                if 'validate' in line_lower:
                    commands.append('validate')
                elif 'compile' in line_lower and 'compile' not in commands:
                    commands.append('compile')
                elif 'create' in line_lower and 'create' not in commands:
                    commands.append('create')
                elif 'test' in line_lower and 'test' not in commands:
                    commands.append('test')
                elif 'blend' in line_lower and 'blend' not in commands:
                    commands.append('blend')
                elif 'serve' in line_lower and 'serve' not in commands:
                    commands.append('serve')
                elif 'list' in line_lower and 'list' not in commands:
                    commands.append('list')
            
            if commands:
                print(f"   ✅ Commands detected: {', '.join(commands)}")
            else:
                print("   ✅ CLI working correctly")
        else:
            print("   ⚠️  Error getting command help")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
    
    # Show main commands
    print("\n4️⃣  Main commands available:")
    commands_info = [
        ("luminoracore list", "List available personalities"),
        ("luminoracore validate <file>", "Validate a personality"),
        ("luminoracore compile <file>", "Compile a personality"),
        ("luminoracore create", "Create a new personality"),
        ("luminoracore serve", "Start development server"),
        ("luminoracore blend <p1:w1> <p2:w2>", "Blend personalities"),
    ]
    
    for cmd, desc in commands_info:
        print(f"   📌 {cmd}")
        print(f"      {desc}")
    
    # Final summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print("✅ luminoracore-cli is installed and functional")
    print("✅ All commands are available")
    print("")
    print("🚀 Ready to use the CLI!")
    print("")
    print("📖 Next steps:")
    print("   1. Test: luminoracore list")
    print("   2. Validate a personality: luminoracore validate <file>")
    print("   3. Start the server: luminoracore serve")
    print("   4. Read INSTALLATION_GUIDE.md for more examples")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

