#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Installation Verification Script - LuminoraCore
===============================================

This script verifies:
  1. Active virtual environment
  2. Base Engine (luminoracore)
  3. CLI (luminoracore-cli)
  4. SDK (luminoracore-sdk-python)
  5. Available providers (7 total)
  6. Optional dependencies
  7. Configured API Keys

IMPORTANT NOTE ABOUT API KEYS:
-------------------------------
API keys are configured as ENVIRONMENT VARIABLES, NOT in code files.

This is for security: you should never put API keys directly in your code.

How to configure an API key?

  Windows PowerShell:
    $env:DEEPSEEK_API_KEY="sk-your-api-key-here"
  
  Linux/Mac:
    export DEEPSEEK_API_KEY="sk-your-api-key-here"

API keys are only needed if you want to make REAL calls to LLMs.
For testing and development, the system works without them.

More information: INSTALLATION_GUIDE.md (section "API Key Configuration")
"""

import sys
import os

# Fix encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("=" * 70)
print("INSTALLATION VERIFICATION - LUMINORACORE")
print("=" * 70)
print()

# Verify virtual environment
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("✅ Virtual environment activated")
else:
    print("⚠️  WARNING: Not in a virtual environment")
    print("   Recommendation: Activate your venv before continuing")

print(f"   Python: {sys.version.split()[0]}")
print(f"   Path: {sys.executable}")
print()

tests = []
errors = []

# Test 1: Base Engine or SDK
print("1. BASE ENGINE / SDK (luminoracore)")
print("-" * 70)

# Try importing from standalone Base Engine
motor_base_ok = False
try:
    from luminoracore import Personality, PersonalityValidator, PersonalityCompiler
    from luminoracore.core.schema import LLMProvider
    import luminoracore
    version = getattr(luminoracore, '__version__', 'unknown')
    print(f"✅ Base Engine installed correctly (v{version})")
    print(f"   - Personality: OK")
    print(f"   - PersonalityValidator: OK")
    print(f"   - PersonalityCompiler: OK")
    print(f"   - LLMProvider: OK")
    motor_base_ok = True
except ImportError:
    # Try importing from SDK (which has its own system)
    try:
        from luminoracore_sdk import LuminoraCoreClient
        from luminoracore_sdk.providers import ProviderFactory
        import luminoracore
        version = getattr(luminoracore, '__version__', 'unknown')
        print(f"✅ SDK installed correctly (v{version})")
        print(f"   ℹ️  Using SDK (includes Base Engine functionality)")
        print(f"   - LuminoraCoreClient: OK")
        print(f"   - ProviderFactory: OK")
        motor_base_ok = True
    except ImportError as e:
        print(f"❌ ERROR: {e}")
        print("   Solution: cd luminoracore && pip install -e .")
        print("   Or: cd luminoracore-sdk-python && pip install -e '.[openai]'")
        errors.append("Base Engine/SDK not installed")

tests.append(motor_base_ok)
print()

# Test 2: CLI
print("2. CLI (luminoracore-cli)")
print("-" * 70)
try:
    import luminoracore_cli
    from luminoracore_cli import __version__ as cli_version
    print(f"✅ Installed correctly (v{cli_version})")
    
    # Verify command is available
    import subprocess
    result = subprocess.run(
        ['luminoracore', '--version'],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode == 0:
        print(f"   - Command 'luminoracore': OK")
    else:
        print(f"   ⚠️  Command 'luminoracore' not available in PATH")
    
    tests.append(True)
except ImportError as e:
    print(f"❌ ERROR: {e}")
    print("   Solution: cd luminoracore-cli && pip install -e .")
    tests.append(False)
    errors.append("CLI not installed")
except FileNotFoundError:
    print(f"⚠️  Package importable but command not found")
    print("   Reinstall: cd luminoracore-cli && pip install -e .")
    tests.append(True)
except Exception as e:
    print(f"⚠️  WARNING: {e}")
    tests.append(True)
print()

# Test 3: SDK (additional verification if not detected before)
print("3. SDK - COMPLETE VERIFICATION (luminoracore-sdk-python)")
print("-" * 70)
sdk_ok = False
try:
    from luminoracore_sdk import LuminoraCoreClient
    from luminoracore_sdk.types.provider import ProviderConfig
    print(f"✅ SDK fully functional")
    print(f"   - LuminoraCoreClient: OK")
    print(f"   - ProviderConfig: OK")
    
    # Verify StorageConfig (may be in different locations)
    try:
        from luminoracore.types.storage import StorageConfig
        print(f"   - StorageConfig: OK")
    except ImportError:
        try:
            from luminoracore.types.session import StorageConfig
            print(f"   - StorageConfig: OK")
        except ImportError:
            print(f"   ⚠️  StorageConfig: Not found (optional)")
    
    sdk_ok = True
except ImportError as e:
    print(f"❌ ERROR: {e}")
    print("   Solution: cd luminoracore-sdk-python && pip install -e '.[openai]'")
    errors.append("SDK not fully installed")

tests.append(sdk_ok)
print()

# Test 4: Providers
print("4. AVAILABLE PROVIDERS")
print("-" * 70)
providers_status = []
try:
    from luminoracore_sdk.providers import ProviderFactory
    
    # List of expected providers
    expected_providers = [
        "openai", "anthropic", "deepseek", "mistral", 
        "cohere", "google", "llama"
    ]
    
    for provider_name in expected_providers:
        try:
            from luminoracore_sdk.types.provider import ProviderConfig
            config = ProviderConfig(name=provider_name, api_key="test")
            provider = ProviderFactory.create_provider(config)
            print(f"  ✅ {provider_name.capitalize():12s} - {provider.__class__.__name__}")
            providers_status.append(True)
        except Exception as e:
            print(f"  ❌ {provider_name.capitalize():12s} - ERROR: {e}")
            providers_status.append(False)
    
    if all(providers_status):
        print(f"\n✅ All providers ({len(expected_providers)}) available")
    else:
        failed = len([p for p in providers_status if not p])
        print(f"\n⚠️  {failed} provider(s) with problems")
        
except ImportError as e:
    print(f"❌ ERROR: Cannot load providers: {e}")
print()

# Test 5: Optional dependencies
print("5. OPTIONAL DEPENDENCIES")
print("-" * 70)
optional_deps = {
    'openai': 'OpenAI API',
    'anthropic': 'Anthropic Claude API',
    'redis': 'Redis storage',
    'asyncpg': 'PostgreSQL storage',
    'motor': 'MongoDB storage',
}

for dep, desc in optional_deps.items():
    try:
        __import__(dep)
        print(f"  ✅ {dep:12s} - {desc}")
    except ImportError:
        print(f"  ⚪ {dep:12s} - {desc} (not installed)")

print()

# Test 6: Configuration
print("6. API KEYS CONFIGURATION")
print("-" * 70)
print("API keys are needed to make real calls to LLMs.")
print("They are configured as environment variables (NOT in code).")
print()

config_vars = {
    'OPENAI_API_KEY': 'https://platform.openai.com/api-keys',
    'ANTHROPIC_API_KEY': 'https://console.anthropic.com/',
    'DEEPSEEK_API_KEY': 'https://platform.deepseek.com/',
    'MISTRAL_API_KEY': 'https://console.mistral.ai/',
    'COHERE_API_KEY': 'https://dashboard.cohere.ai/',
    'GOOGLE_API_KEY': 'https://makersuite.google.com/app/apikey',
}

api_keys_found = 0
keys_no_configuradas = []

for var, url in config_vars.items():
    if os.getenv(var):
        print(f"  ✅ {var}")
        api_keys_found += 1
    else:
        print(f"  ⚪ {var} (not configured)")
        keys_no_configuradas.append((var, url))

if api_keys_found == 0:
    print("\n⚠️  No API keys configured")
    print("   To make real calls to LLMs, you need to configure at least one.")
    print()
    print("   📖 How to configure API keys?")
    print()
    print("   Windows PowerShell:")
    print("   $env:DEEPSEEK_API_KEY=\"sk-your-api-key-here\"")
    print()
    print("   Linux/Mac:")
    print("   export DEEPSEEK_API_KEY=\"sk-your-api-key-here\"")
    print()
    print("   📝 Where to get API keys:")
    for var, url in keys_no_configuradas:
        provider_name = var.replace('_API_KEY', '').title()
        print(f"   - {provider_name}: {url}")
elif api_keys_found < len(config_vars):
    print(f"\n✅ {api_keys_found} API key(s) configured")
    print()
    print("   💡 Tip: Configure more providers if you need them:")
    print()
    print("   Windows: $env:PROVIDER_API_KEY=\"your-key\"")
    print("   Linux/Mac: export PROVIDER_API_KEY=\"your-key\"")
else:
    print(f"\n✅ All API keys ({api_keys_found}) are configured!")

print()

# Final Summary
print("=" * 70)
print("SUMMARY")
print("=" * 70)

if all(tests):
    print("🎉 INSTALLATION COMPLETE AND CORRECT")
    print()
    print("Installed components:")
    if motor_base_ok:
        print("  ✅ Base Engine/SDK (luminoracore)")
    print("  ✅ CLI (luminoracore-cli)")
    if sdk_ok:
        print("  ✅ Complete SDK (with providers and client)")
    print()
    if api_keys_found == 0:
        print("⚠️  Note: You don't have API keys configured (yet)")
        print()
        print("This is fine to get started. You can:")
        print("  1. Explore the system without making real LLM calls")
        print("  2. View examples and documentation")
        print("  3. Configure API keys when you need them")
        print()
        print("📖 To configure API keys, check:")
        print("   INSTALLATION_GUIDE.md (section 'API Key Configuration')")
        print()
    print("Next steps:")
    print("  1. Read: QUICK_START.md")
    if sdk_ok and api_keys_found > 0:
        print("  2. Test: luminoracore test --provider deepseek")
        print("  3. Run examples: python ejemplo_quick_start_sdk.py")
    else:
        print("  2. Configure your API keys")
        print("  3. Test: luminoracore --help")
        print("  4. Run available examples")
else:
    print("⚠️  SOME COMPONENTS MISSING")
    print()
    print("Problems found:")
    for error in errors:
        print(f"  ❌ {error}")
    print()
    print("Check: INSTALLATION_GUIDE.md section 'Troubleshooting'")

print("=" * 70)
print()

# Exit code
sys.exit(0 if all(tests) else 1)

