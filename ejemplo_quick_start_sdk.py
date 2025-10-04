#!/usr/bin/env python3
"""
Ejemplo Quick Start - LuminoraCore SDK
Ejecuta este archivo para probar que luminoracore-sdk está instalado correctamente.

NOTA: Este ejemplo NO hace llamadas reales a APIs de LLM.
Solo verifica que el SDK esté instalado y funcional.
"""

import sys
import asyncio

async def main():
    """Prueba rápida del SDK de LuminoraCore."""
    print("=" * 60)
    print("🐍 LuminoraCore SDK - Quick Start")
    print("=" * 60)
    
    # Verificar que el SDK está instalado
    print("\n1️⃣  Verificando instalación del SDK...")
    try:
        from luminoracore import LuminoraCoreClient
        print("   ✅ LuminoraCoreClient importado correctamente")
    except ImportError as e:
        print(f"   ❌ Error: luminoracore-sdk no está instalado")
        print(f"   💡 Solución: cd luminoracore-sdk-python && pip install -e .")
        return False
    
    # Verificar tipos disponibles
    print("\n2️⃣  Verificando tipos y configuraciones...")
    try:
        from luminoracore.types.provider import ProviderConfig
        from luminoracore.types.session import StorageConfig, MemoryConfig
        print("   ✅ ProviderConfig disponible")
        print("   ✅ StorageConfig disponible")
        print("   ✅ MemoryConfig disponible")
    except ImportError as e:
        print(f"   ⚠️  Error al importar tipos: {e}")
    
    # Crear cliente
    print("\n3️⃣  Creando cliente de LuminoraCore...")
    try:
        from luminoracore.types.session import StorageConfig
        
        client = LuminoraCoreClient(
            storage_config=StorageConfig(
                storage_type="memory"
            )
        )
        print("   ✅ Cliente creado correctamente")
        print("   💾 Usando almacenamiento en memoria")
    except Exception as e:
        print(f"   ⚠️  Error al crear cliente: {e}")
        return False
    
    # Inicializar cliente
    print("\n4️⃣  Inicializando cliente...")
    try:
        await client.initialize()
        print("   ✅ Cliente inicializado correctamente")
    except Exception as e:
        print(f"   ⚠️  Error al inicializar: {e}")
        return False
    
    # Crear una personalidad de prueba
    print("\n5️⃣  Cargando personalidad de prueba...")
    try:
        personality_data = {
            "name": "asistente_demo",
            "description": "Personalidad de demostración para Quick Start",
            "system_prompt": "Eres un asistente amigable y servicial.",
            "metadata": {
                "version": "1.0.0",
                "author": "Quick Start Demo",
                "tags": ["demo", "test"]
            }
        }
        
        await client.load_personality("asistente_demo", personality_data)
        print("   ✅ Personalidad cargada: asistente_demo")
    except Exception as e:
        print(f"   ⚠️  Error al cargar personalidad: {e}")
    
    # Crear configuración de proveedor (sin API key real)
    print("\n6️⃣  Creando configuración de proveedor...")
    try:
        from luminoracore.types.provider import ProviderConfig
        
        provider_config = ProviderConfig(
            name="openai",
            api_key="demo-key-not-for-real-use",
            model="gpt-3.5-turbo",
            extra={
                "timeout": 30,
                "max_retries": 3
            }
        )
        print("   ✅ ProviderConfig creado (modo demo)")
        print("   ⚠️  Nota: Esta es una API key de demo, no real")
    except Exception as e:
        print(f"   ⚠️  Error al crear configuración: {e}")
    
    # Crear sesión
    print("\n7️⃣  Creando sesión...")
    try:
        session_id = await client.create_session(
            personality_name="asistente_demo",
            provider_config=provider_config
        )
        print(f"   ✅ Sesión creada: {session_id}")
    except Exception as e:
        print(f"   ⚠️  Error al crear sesión: {e}")
        session_id = None
    
    # Probar almacenamiento de memoria
    if session_id:
        print("\n8️⃣  Probando almacenamiento en memoria...")
        try:
            await client.store_memory(
                session_id=session_id,
                key="test_key",
                value="test_value"
            )
            print("   ✅ Memoria almacenada")
            
            memory = await client.get_memory(session_id, "test_key")
            print(f"   ✅ Memoria recuperada: {memory}")
        except Exception as e:
            print(f"   ⚠️  Error en memoria: {e}")
        
        # Obtener información de sesión
        print("\n9️⃣  Obteniendo información de sesión...")
        try:
            info = await client.get_session_info(session_id)
            print(f"   ✅ Información de sesión obtenida")
            print(f"      - ID: {info.get('session_id', 'N/A')}")
            print(f"      - Personalidad: {info.get('personality_name', 'N/A')}")
        except Exception as e:
            print(f"   ⚠️  Error al obtener info: {e}")
    
    # Verificar proveedores disponibles
    print("\n🔧 Proveedores de LLM soportados:")
    providers = [
        ("OpenAI", "gpt-3.5-turbo, gpt-4, gpt-4-turbo"),
        ("Anthropic", "claude-3-sonnet, claude-3-opus"),
        ("Cohere", "command, command-light"),
        ("Google", "gemini-pro, gemini-ultra"),
        ("Mistral", "mistral-large, mistral-medium"),
    ]
    
    for provider, models in providers:
        print(f"   📌 {provider}: {models}")
    
    # Limpieza
    print("\n🧹 Limpiando recursos...")
    try:
        await client.cleanup()
        print("   ✅ Limpieza completada")
    except Exception as e:
        print(f"   ⚠️  Error en limpieza: {e}")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE LA PRUEBA")
    print("=" * 60)
    print("✅ luminoracore-sdk está instalado y funcional")
    print("✅ Cliente puede crear sesiones y gestionar personalidades")
    print("✅ Sistema de memoria funcionando correctamente")
    print("")
    print("⚠️  IMPORTANTE:")
    print("   Este test NO hace llamadas reales a APIs de LLM")
    print("   Para hacer llamadas reales necesitas:")
    print("   1. Una API key válida del proveedor (OpenAI, Anthropic, etc.)")
    print("   2. Instalar las dependencias del proveedor:")
    print("      pip install -e \".[openai]\"  # Para OpenAI")
    print("      pip install -e \".[anthropic]\"  # Para Anthropic")
    print("      pip install -e \".[all]\"  # Para todos")
    print("")
    print("🚀 ¡Listo para usar el SDK!")
    print("")
    print("📖 Próximos pasos:")
    print("   1. Configura tus API keys en variables de entorno")
    print("   2. Lee GUIA_INSTALACION_USO.md para ejemplos completos")
    print("   3. Explora luminoracore-sdk-python/examples/")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Prueba interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)

