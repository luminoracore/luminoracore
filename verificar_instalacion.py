#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Verificación de Instalación - LuminoraCore
Verifica que todos los componentes estén instalados correctamente.
"""

import sys
import os

# Fix encoding para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("=" * 70)
print("VERIFICACION DE INSTALACION - LUMINORACORE")
print("=" * 70)
print()

# Verificar entorno virtual
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("✅ Entorno virtual activado")
else:
    print("⚠️  WARNING: No estas en un entorno virtual")
    print("   Recomendacion: Activa tu venv antes de continuar")

print(f"   Python: {sys.version.split()[0]}")
print(f"   Path: {sys.executable}")
print()

tests = []
errors = []

# Test 1: Motor Base
print("1. MOTOR BASE (luminoracore)")
print("-" * 70)
try:
    from luminoracore import Personality, PersonalityValidator, PersonalityCompiler
    from luminoracore.core.schema import LLMProvider
    import luminoracore
    version = getattr(luminoracore, '__version__', 'unknown')
    print(f"✅ Instalado correctamente (v{version})")
    print(f"   - Personality: OK")
    print(f"   - PersonalityValidator: OK")
    print(f"   - PersonalityCompiler: OK")
    print(f"   - LLMProvider: OK")
    tests.append(True)
except ImportError as e:
    print(f"❌ ERROR: {e}")
    print("   Solucion: cd luminoracore && pip install -e .")
    tests.append(False)
    errors.append("Motor Base no instalado")
print()

# Test 2: CLI
print("2. CLI (luminoracore-cli)")
print("-" * 70)
try:
    import luminoracore_cli
    from luminoracore_cli import __version__ as cli_version
    print(f"✅ Instalado correctamente (v{cli_version})")
    
    # Verificar que el comando está disponible
    import subprocess
    result = subprocess.run(
        ['luminoracore', '--version'],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode == 0:
        print(f"   - Comando 'luminoracore': OK")
    else:
        print(f"   ⚠️  Comando 'luminoracore' no disponible en PATH")
    
    tests.append(True)
except ImportError as e:
    print(f"❌ ERROR: {e}")
    print("   Solucion: cd luminoracore-cli && pip install -e .")
    tests.append(False)
    errors.append("CLI no instalado")
except FileNotFoundError:
    print(f"⚠️  Paquete importable pero comando no encontrado")
    print("   Reinstala: cd luminoracore-cli && pip install -e .")
    tests.append(True)
except Exception as e:
    print(f"⚠️  WARNING: {e}")
    tests.append(True)
print()

# Test 3: SDK
print("3. SDK (luminoracore-sdk-python)")
print("-" * 70)
try:
    from luminoracore import LuminoraCoreClient
    from luminoracore.types.provider import ProviderConfig
    from luminoracore.types.storage import StorageConfig
    print(f"✅ Instalado correctamente")
    print(f"   - LuminoraCoreClient: OK")
    print(f"   - ProviderConfig: OK")
    print(f"   - StorageConfig: OK")
    tests.append(True)
except ImportError as e:
    print(f"❌ ERROR: {e}")
    print("   Solucion: cd luminoracore-sdk-python && pip install -e '.[openai]'")
    tests.append(False)
    errors.append("SDK no instalado")
print()

# Test 4: Providers
print("4. PROVIDERS DISPONIBLES")
print("-" * 70)
providers_status = []
try:
    from luminoracore.providers import ProviderFactory
    
    # Lista de providers esperados
    expected_providers = [
        "openai", "anthropic", "deepseek", "mistral", 
        "cohere", "google", "llama"
    ]
    
    for provider_name in expected_providers:
        try:
            from luminoracore.types.provider import ProviderConfig
            config = ProviderConfig(name=provider_name, api_key="test")
            provider = ProviderFactory.create_provider(config)
            print(f"  ✅ {provider_name.capitalize():12s} - {provider.__class__.__name__}")
            providers_status.append(True)
        except Exception as e:
            print(f"  ❌ {provider_name.capitalize():12s} - ERROR: {e}")
            providers_status.append(False)
    
    if all(providers_status):
        print(f"\n✅ Todos los providers ({len(expected_providers)}) disponibles")
    else:
        failed = len([p for p in providers_status if not p])
        print(f"\n⚠️  {failed} provider(s) con problemas")
        
except ImportError as e:
    print(f"❌ ERROR: No se pueden cargar providers: {e}")
print()

# Test 5: Dependencias opcionales
print("5. DEPENDENCIAS OPCIONALES")
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
        print(f"  ⚪ {dep:12s} - {desc} (no instalado)")

print()

# Test 6: Configuración
print("6. CONFIGURACION")
print("-" * 70)
config_vars = [
    'OPENAI_API_KEY',
    'ANTHROPIC_API_KEY',
    'DEEPSEEK_API_KEY',
    'MISTRAL_API_KEY',
    'COHERE_API_KEY',
    'GOOGLE_API_KEY',
]

api_keys_found = 0
for var in config_vars:
    if os.getenv(var):
        print(f"  ✅ {var}")
        api_keys_found += 1
    else:
        print(f"  ⚪ {var} (no configurada)")

if api_keys_found == 0:
    print("\n⚠️  Ninguna API key configurada")
    print("   Las necesitaras para usar los providers")
else:
    print(f"\n✅ {api_keys_found} API key(s) configurada(s)")

print()

# Resumen Final
print("=" * 70)
print("RESUMEN")
print("=" * 70)

if all(tests):
    print("🎉 INSTALACION COMPLETA Y CORRECTA")
    print()
    print("Todos los componentes principales instalados:")
    print("  ✅ Motor Base (luminoracore)")
    print("  ✅ CLI (luminoracore-cli)")
    print("  ✅ SDK (luminoracore-sdk)")
    print()
    print("Siguientes pasos:")
    print("  1. Configura tus API keys (variables de entorno)")
    print("  2. Lee: INICIO_RAPIDO.md")
    print("  3. Prueba: luminoracore --help")
    print("  4. Ejecuta ejemplos: python ejemplo_quick_start_core.py")
else:
    print("⚠️  ALGUNOS COMPONENTES FALTAN")
    print()
    print("Problemas encontrados:")
    for error in errors:
        print(f"  ❌ {error}")
    print()
    print("Consulta: GUIA_INSTALACION_USO.md seccion 'Solucion de Problemas'")

print("=" * 70)
print()

# Exit code
sys.exit(0 if all(tests) else 1)

