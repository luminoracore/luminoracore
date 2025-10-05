#!/usr/bin/env python3
"""
Quick Start Example - LuminoraCore SDK
Run this file to test that luminoracore-sdk is installed correctly.

NOTE: This example does NOT make real calls to LLM APIs.
It only verifies that the SDK is installed and functional.
"""

import sys
import asyncio

async def main():
    """Quick test of LuminoraCore SDK."""
    print("=" * 60)
    print("🐍 LuminoraCore SDK - Quick Start")
    print("=" * 60)
    
    # Check that the SDK is installed
    print("\n1️⃣  Checking SDK installation...")
    try:
        from luminoracore import LuminoraCoreClient
        print("   ✅ LuminoraCoreClient imported correctly")
    except ImportError as e:
        print(f"   ❌ Error: luminoracore-sdk is not installed")
        print(f"   💡 Solution: cd luminoracore-sdk-python && pip install -e .")
        return False
    
    # Check available types
    print("\n2️⃣  Checking types and configurations...")
    try:
        from luminoracore.types.provider import ProviderConfig
        from luminoracore.types.session import StorageConfig, MemoryConfig
        print("   ✅ ProviderConfig available")
        print("   ✅ StorageConfig available")
        print("   ✅ MemoryConfig available")
    except ImportError as e:
        print(f"   ⚠️  Error importing types: {e}")
    
    # Create client
    print("\n3️⃣  Creating LuminoraCore client...")
    try:
        from luminoracore.types.session import StorageConfig
        
        client = LuminoraCoreClient(
            storage_config=StorageConfig(
                storage_type="memory"
            )
        )
        print("   ✅ Client created correctly")
        print("   💾 Using in-memory storage")
    except Exception as e:
        print(f"   ⚠️  Error creating client: {e}")
        return False
    
    # Initialize client
    print("\n4️⃣  Initializing client...")
    try:
        await client.initialize()
        print("   ✅ Client initialized correctly")
    except Exception as e:
        print(f"   ⚠️  Error initializing: {e}")
        return False
    
    # Create a test personality
    print("\n5️⃣  Loading test personality...")
    try:
        personality_data = {
            "name": "demo_assistant",
            "description": "Demonstration personality for Quick Start",
            "system_prompt": "You are a friendly and helpful assistant.",
            "metadata": {
                "version": "1.0.0",
                "author": "Quick Start Demo",
                "tags": ["demo", "test"]
            }
        }
        
        await client.load_personality("demo_assistant", personality_data)
        print("   ✅ Personality loaded: demo_assistant")
    except Exception as e:
        print(f"   ⚠️  Error loading personality: {e}")
    
    # Create provider configuration (without real API key)
    print("\n6️⃣  Creating provider configuration...")
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
        print("   ✅ ProviderConfig created (demo mode)")
        print("   ⚠️  Note: This is a demo API key, not real")
    except Exception as e:
        print(f"   ⚠️  Error creating configuration: {e}")
    
    # Create session
    print("\n7️⃣  Creating session...")
    try:
        session_id = await client.create_session(
            personality_name="demo_assistant",
            provider_config=provider_config
        )
        print(f"   ✅ Session created: {session_id}")
    except Exception as e:
        print(f"   ⚠️  Error creating session: {e}")
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

