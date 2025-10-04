#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Verificación de Instalación - LuminoraCore
====================================================

Este script verifica:
  1. Entorno virtual activo
  2. Motor Base (luminoracore)
  3. CLI (luminoracore-cli)
  4. SDK (luminoracore-sdk-python)
  5. Providers disponibles (7 en total)
  6. Dependencias opcionales
  7. API Keys configuradas

NOTA IMPORTANTE SOBRE API KEYS:
-------------------------------
Las API keys se configuran como VARIABLES DE ENTORNO, NO en archivos de código.

Esto es por seguridad: nunca debes poner API keys directamente en tu código.

¿Cómo configurar una API key?

  Windows PowerShell:
    $env:DEEPSEEK_API_KEY="sk-tu-api-key-aqui"
  
  Linux/Mac:
    export DEEPSEEK_API_KEY="sk-tu-api-key-aqui"

Las API keys son necesarias solo si quieres hacer llamadas REALES a los LLMs.
Para testing y desarrollo, el sistema funciona sin ellas.

Más información: GUIA_INSTALACION_USO.md (sección "Configurar API Keys")
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

# Test 1: Motor Base o SDK
print("1. MOTOR BASE / SDK (luminoracore)")
print("-" * 70)

# Intentar importar desde Motor Base standalone
motor_base_ok = False
try:
    from luminoracore import Personality, PersonalityValidator, PersonalityCompiler
    from luminoracore.core.schema import LLMProvider
    import luminoracore
    version = getattr(luminoracore, '__version__', 'unknown')
    print(f"✅ Motor Base instalado correctamente (v{version})")
    print(f"   - Personality: OK")
    print(f"   - PersonalityValidator: OK")
    print(f"   - PersonalityCompiler: OK")
    print(f"   - LLMProvider: OK")
    motor_base_ok = True
except ImportError:
    # Intentar importar desde SDK (que tiene su propio sistema)
    try:
        from luminoracore import LuminoraCoreClient
        from luminoracore.providers import ProviderFactory
        import luminoracore
        version = getattr(luminoracore, '__version__', 'unknown')
        print(f"✅ SDK instalado correctamente (v{version})")
        print(f"   ℹ️  Usando SDK (incluye funcionalidad del Motor Base)")
        print(f"   - LuminoraCoreClient: OK")
        print(f"   - ProviderFactory: OK")
        motor_base_ok = True
    except ImportError as e:
        print(f"❌ ERROR: {e}")
        print("   Solucion: cd luminoracore && pip install -e .")
        print("   O: cd luminoracore-sdk-python && pip install -e '.[openai]'")
        errors.append("Motor Base/SDK no instalado")

tests.append(motor_base_ok)
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

# Test 3: SDK (verificación adicional si no se detectó antes)
print("3. SDK - VERIFICACION COMPLETA (luminoracore-sdk-python)")
print("-" * 70)
sdk_ok = False
try:
    from luminoracore import LuminoraCoreClient
    from luminoracore.types.provider import ProviderConfig
    print(f"✅ SDK completamente funcional")
    print(f"   - LuminoraCoreClient: OK")
    print(f"   - ProviderConfig: OK")
    
    # Verificar StorageConfig (puede estar en diferentes lugares)
    try:
        from luminoracore.types.storage import StorageConfig
        print(f"   - StorageConfig: OK")
    except ImportError:
        try:
            from luminoracore.types.session import StorageConfig
            print(f"   - StorageConfig: OK")
        except ImportError:
            print(f"   ⚠️  StorageConfig: No encontrado (opcional)")
    
    sdk_ok = True
except ImportError as e:
    print(f"❌ ERROR: {e}")
    print("   Solucion: cd luminoracore-sdk-python && pip install -e '.[openai]'")
    errors.append("SDK no instalado completamente")

tests.append(sdk_ok)
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
print("6. CONFIGURACION DE API KEYS")
print("-" * 70)
print("Las API keys son necesarias para hacer llamadas reales a los LLMs.")
print("Se configuran como variables de entorno (NO en el código).")
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
        print(f"  ⚪ {var} (no configurada)")
        keys_no_configuradas.append((var, url))

if api_keys_found == 0:
    print("\n⚠️  Ninguna API key configurada")
    print("   Para hacer llamadas reales a LLMs, necesitas configurar al menos una.")
    print()
    print("   📖 ¿Cómo configurar API keys?")
    print()
    print("   Windows PowerShell:")
    print("   $env:DEEPSEEK_API_KEY=\"sk-tu-api-key-aqui\"")
    print()
    print("   Linux/Mac:")
    print("   export DEEPSEEK_API_KEY=\"sk-tu-api-key-aqui\"")
    print()
    print("   📝 Donde obtener API keys:")
    for var, url in keys_no_configuradas:
        provider_name = var.replace('_API_KEY', '').title()
        print(f"   - {provider_name}: {url}")
elif api_keys_found < len(config_vars):
    print(f"\n✅ {api_keys_found} API key(s) configurada(s)")
    print()
    print("   💡 Tip: Configura más providers si los necesitas:")
    print()
    print("   Windows: $env:PROVIDER_API_KEY=\"tu-key\"")
    print("   Linux/Mac: export PROVIDER_API_KEY=\"tu-key\"")
else:
    print(f"\n✅ Todas las API keys ({api_keys_found}) están configuradas!")

print()

# Resumen Final
print("=" * 70)
print("RESUMEN")
print("=" * 70)

if all(tests):
    print("🎉 INSTALACION COMPLETA Y CORRECTA")
    print()
    print("Componentes instalados:")
    if motor_base_ok:
        print("  ✅ Motor Base/SDK (luminoracore)")
    print("  ✅ CLI (luminoracore-cli)")
    if sdk_ok:
        print("  ✅ SDK completo (con providers y cliente)")
    print()
    if api_keys_found == 0:
        print("⚠️  Nota: No tienes API keys configuradas (aún)")
        print()
        print("Esto está bien para empezar. Puedes:")
        print("  1. Explorar el sistema sin hacer llamadas a LLMs reales")
        print("  2. Ver ejemplos y documentación")
        print("  3. Configurar API keys cuando las necesites")
        print()
        print("📖 Para configurar API keys, consulta:")
        print("   GUIA_INSTALACION_USO.md (sección 'Configurar API Keys')")
        print()
    print("Siguientes pasos:")
    print("  1. Lee: INICIO_RAPIDO.md")
    if sdk_ok and api_keys_found > 0:
        print("  2. Prueba: luminoracore test --provider deepseek")
        print("  3. Ejecuta ejemplos: python ejemplo_quick_start_sdk.py")
    else:
        print("  2. Configura tus API keys")
        print("  3. Prueba: luminoracore --help")
        print("  4. Ejecuta ejemplos disponibles")
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

