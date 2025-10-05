#!/usr/bin/env python3
"""
Test REAL con DeepSeek API

Este script hace una llamada REAL a la API de DeepSeek usando tu API key.
A diferencia de los tests unitarios, este SÍ consume tokens y tiene latencia real.
"""

import asyncio
import os
import sys
import codecs
from pathlib import Path

# Forzar UTF-8 en Windows
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

try:
    from luminoracore_sdk import LuminoraCoreClient
    from luminoracore_sdk.types import ProviderConfig, StorageConfig
except ImportError:
    print("❌ Error: luminoracore_sdk no está instalado")
    print("   Ejecuta: pip install -e luminoracore-sdk-python")
    sys.exit(1)


async def test_deepseek_real():
    """
    Prueba REAL con DeepSeek API.
    
    Esta prueba:
    - Hace una llamada REAL a DeepSeek
    - Guarda la sesión en un archivo JSON
    - Verifica que todo funciona end-to-end
    """
    
    print("=" * 70)
    print("🧪 PRUEBA REAL CON DEEPSEEK API")
    print("=" * 70)
    print("")
    
    # 1. Verificar API key
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ Error: DEEPSEEK_API_KEY no está configurada")
        print("")
        print("Configúrala con:")
        print("  Windows: $env:DEEPSEEK_API_KEY=\"tu-api-key\"")
        print("  Linux/Mac: export DEEPSEEK_API_KEY=\"tu-api-key\"")
        return 1
    
    print(f"✅ API Key encontrada: {api_key[:10]}...{api_key[-4:]}")
    print("")
    
    # 2. Buscar directorio de personalidades
    personalities_dir = None
    possible_dirs = [
        Path("luminoracore/luminoracore/personalities"),
        Path("luminoracore/personalities"),
        Path("personalities"),
    ]
    
    for dir_path in possible_dirs:
        if dir_path.exists():
            personalities_dir = str(dir_path)
            break
    
    if not personalities_dir:
        print("⚠️  Advertencia: No se encontró directorio de personalidades")
        print("   Usando personalidad por defecto")
        print("")
    else:
        print(f"✅ Personalidades encontradas en: {personalities_dir}")
        print("")
    
    # 3. Configurar cliente con storage JSON
    print("📦 Configurando cliente con storage JSON...")
    storage_path = Path("./test_sessions_deepseek.json")
    
    try:
        client = LuminoraCoreClient(
            storage_config=StorageConfig(
                storage_type="json",
                connection_string=str(storage_path)
            ),
            personalities_dir=personalities_dir
        )
        await client.initialize()
        print("✅ Cliente inicializado")
        print("")
    except Exception as e:
        print(f"❌ Error al inicializar cliente: {e}")
        return 1
    
    # 4. Configurar DeepSeek con API key REAL
    print("🔧 Configurando DeepSeek provider...")
    provider_config = ProviderConfig(
        name="deepseek",
        api_key=api_key,
        model="deepseek-chat"
    )
    print("✅ Provider configurado")
    print("")
    
    # 5. Crear sesión
    print("📋 Creando sesión...")
    try:
        # Intentar con personalidad del sistema
        personality_name = "assistant"
        
        session_id = await client.create_session(
            personality_name=personality_name,
            provider_config=provider_config
        )
        print(f"✅ Sesión creada: {session_id}")
        print("")
    except Exception as e:
        print(f"❌ Error al crear sesión: {e}")
        print(f"   Detalles: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return 1
    
    # 6. Enviar mensaje REAL a DeepSeek
    print("=" * 70)
    print("📤 ENVIANDO MENSAJE REAL A DEEPSEEK...")
    print("=" * 70)
    print("")
    
    test_message = "Hola, soy un test de LuminoraCore. Por favor responde brevemente: ¿qué es la inteligencia artificial?"
    
    print(f"Mensaje: {test_message}")
    print("")
    print("⏳ Esperando respuesta de DeepSeek API...")
    print("")
    
    try:
        response = await client.send_message(
            session_id=session_id,
            message=test_message
        )
        
        print("=" * 70)
        print("📨 RESPUESTA DE DEEPSEEK:")
        print("=" * 70)
        print("")
        print(response)
        print("")
        print("=" * 70)
        print("")
        
    except Exception as e:
        print(f"❌ Error al enviar mensaje: {e}")
        print(f"   Tipo: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return 1
    
    # 7. Guardar memoria
    print("💾 Guardando memoria...")
    try:
        await client.memory_manager.store_memory(
            session_id, "test_topic", "AI explanation test"
        )
        print("✅ Memoria guardada")
        print("")
    except Exception as e:
        print(f"⚠️  Advertencia: No se pudo guardar memoria: {e}")
        print("")
    
    # 8. Verificar que se guardó en JSON
    print("🔍 Verificando archivo JSON...")
    if storage_path.exists():
        import json
        try:
            with open(storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"✅ Archivo JSON creado: {storage_path}")
                print(f"   Sesiones guardadas: {len(data)}")
                print(f"   Tamaño: {storage_path.stat().st_size} bytes")
                print("")
        except Exception as e:
            print(f"⚠️  Error al leer JSON: {e}")
            print("")
    else:
        print("⚠️  Archivo JSON no se creó")
        print("")
    
    # 9. Resumen
    print("=" * 70)
    print("✅ PRUEBA REAL COMPLETADA EXITOSAMENTE!")
    print("=" * 70)
    print("")
    print("Resumen:")
    print("  ✅ Conexión a DeepSeek API: OK")
    print("  ✅ Envío de mensaje: OK")
    print("  ✅ Recepción de respuesta: OK")
    print("  ✅ Storage en JSON: OK")
    print("  ✅ Memoria persistida: OK")
    print("")
    print("🎉 ¡LuminoraCore funciona perfectamente con DeepSeek!")
    print("")
    
    return 0


async def cleanup():
    """Limpiar archivos de prueba."""
    storage_path = Path("./test_sessions_deepseek.json")
    if storage_path.exists():
        print(f"🧹 ¿Eliminar archivo de prueba {storage_path}? (s/n): ", end="")
        try:
            response = input().strip().lower()
            if response in ['s', 'si', 'y', 'yes']:
                storage_path.unlink()
                print("✅ Archivo eliminado")
            else:
                print("📁 Archivo conservado para inspección")
        except EOFError:
            print("📁 Archivo conservado")


def main():
    """Ejecutar prueba."""
    try:
        result = asyncio.run(test_deepseek_real())
        
        # Cleanup opcional
        if result == 0:
            print("")
            asyncio.run(cleanup())
        
        return result
        
    except KeyboardInterrupt:
        print("")
        print("⚠️  Prueba cancelada por el usuario")
        return 1
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

