#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script temporal para verificar imports después del refactoring.
"""
import sys

print("Probando imports...")
print("")

# Motor Base (luminoracore)
try:
    from luminoracore import Personality, PersonalityValidator, PersonalityCompiler
    print("[OK] Motor Base (luminoracore):")
    print("   - Personality")
    print("   - PersonalityValidator")
    print("   - PersonalityCompiler")
    print("")
except ImportError as e:
    print(f"[ERROR] Motor Base: {e}")
    print("")
    
    # Diagnostico adicional
    print("Diagnostico:")
    try:
        import luminoracore
        print(f"  luminoracore location: {luminoracore.__file__}")
        print(f"  luminoracore dir: {dir(luminoracore)}")
    except Exception as diag_e:
        print(f"  No se puede diagnosticar: {diag_e}")
    print("")
    exit(1)

# SDK (luminoracore_sdk)  
try:
    from luminoracore_sdk import LuminoraCoreClient
    from luminoracore_sdk.types import ProviderConfig
    print("[OK] SDK (luminoracore_sdk):")
    print("   - LuminoraCoreClient")
    print("   - ProviderConfig")
    print("")
except ImportError as e:
    print(f"[ERROR] SDK: {e}")
    print("")
    exit(1)

print("=" * 70)
print("REFACTORING EXITOSO - Namespaces separados funcionando!")
print("=" * 70)

