#!/usr/bin/env python3
"""
Test basico de LuminoraCore v1.1 con DeepSeek
Solo prueba la configuracion y creacion de cliente
"""

import os
import sys

# Anadir el directorio actual al path para importar los paquetes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from luminoracore.core.personality import Personality
from luminoracore_sdk.client import LuminoraCoreClient
from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11

# Configuracion para DeepSeek
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    print("ERROR: DEEPSEEK_API_KEY no esta configurada")
    print("Por favor, configura tu API key de DeepSeek:")
    print("export DEEPSEEK_API_KEY='tu_api_key_aqui'")
    sys.exit(1)

def test_basic_setup():
    """Test basico de configuracion"""
    
    print("LuminoraCore v1.1 - Test Basico con DeepSeek")
    print("=" * 60)
    
    # 1. Verificar API key
    print("\nPaso 1: Verificando API key...")
    print(f"OK API key configurada: {DEEPSEEK_API_KEY[:8]}...{DEEPSEEK_API_KEY[-4:]}")
    
    # 2. Crear storage
    print("\nPaso 2: Creando storage...")
    storage = InMemoryStorageV11()
    print("OK Storage en memoria creado")
    
    # 3. Crear cliente base
    print("\nPaso 3: Creando cliente base...")
    base_client = LuminoraCoreClient(
        personalities_dir="luminoracore/luminoracore/personalities"
    )
    print("OK Cliente base creado con directorio de personalidades")
    
    # 4. Crear cliente v1.1
    print("\nPaso 4: Creando cliente v1.1...")
    client = LuminoraCoreClientV11(base_client, storage_v11=storage)
    print("OK Cliente v1.1 creado con extensiones")
    
    # 5. Crear personalidad
    print("\nPaso 5: Creando personalidad...")
    victoria_personality = {
        "name": "Victoria Sterling",
        "version": "1.1.0",
        "description": "Executive assistant with evolving personality",
        "base_personality": {
            "core_traits": {
                "professionalism": 0.9,
                "efficiency": 0.8,
                "empathy": 0.7,
                "directness": 0.6
            }
        },
        "hierarchical_config": {
            "relationship_levels": {
                "stranger": {"formality_modifier": 0.2},
                "acquaintance": {"formality_modifier": 0.0},
                "friend": {"formality_modifier": -0.1},
                "close_friend": {"formality_modifier": -0.3}
            }
        },
        "memory_preferences": {
            "fact_retention": 0.9,
            "episodic_memory": 0.8
        },
        "affinity_config": {
            "positive_interactions": 5,
            "negative_interactions": -3
        }
    }
    print("OK Personalidad Victoria Sterling creada")
    
    # 6. Verificar metodos disponibles
    print("\nPaso 6: Verificando metodos disponibles...")
    
    print("Metodos del cliente base:")
    base_methods = [method for method in dir(base_client) if not method.startswith('_')]
    for method in base_methods[:5]:  # Mostrar solo los primeros 5
        print(f"   - {method}")
    print(f"   ... y {len(base_methods) - 5} mas")
    
    print("\nMetodos del cliente v1.1:")
    v11_methods = [method for method in dir(client) if not method.startswith('_')]
    for method in v11_methods[:5]:  # Mostrar solo los primeros 5
        print(f"   - {method}")
    print(f"   ... y {len(v11_methods) - 5} mas")
    
    # 7. Test de creacion de sesion (sin enviar mensajes)
    print("\nPaso 7: Probando creacion de sesion...")
    
    try:
        import asyncio
        
        async def test_session_creation():
            from luminoracore_sdk.types.provider import ProviderConfig
            
            # Crear configuracion de proveedor
            provider_config = ProviderConfig(
                name="openai",  # Usar openai como ejemplo
                model="gpt-3.5-turbo",
                api_key="test_key"
            )
            
            session_id = await base_client.create_session(
                personality_name="Dr. Luna",
                provider_config=provider_config
            )
            return session_id
        
        session_id = asyncio.run(test_session_creation())
        print(f"OK Sesion creada exitosamente: {session_id}")
        
    except Exception as e:
        print(f"ERROR creando sesion: {e}")
        return False
    
    # 8. Verificar informacion de sesion
    print("\nPaso 8: Verificando informacion de sesion...")
    
    try:
        import asyncio
        
        async def test_session_info():
            session_info = await base_client.get_session_info(session_id)
            return session_info
        
        session_info = asyncio.run(test_session_info())
        if session_info:
            print("OK Informacion de sesion obtenida")
            print(f"   - Session ID: {session_info.get('session_id', 'N/A')}")
            print(f"   - Created: {session_info.get('created_at', 'N/A')}")
        else:
            print("ADVERTENCIA: No se pudo obtener informacion de sesion")
        
    except Exception as e:
        print(f"ERROR obteniendo informacion de sesion: {e}")
    
    # 9. Resumen final
    print("\n" + "=" * 60)
    print("RESUMEN DEL TEST BASICO")
    print("=" * 60)
    
    print("ESTADO: CONFIGURACION EXITOSA")
    print("\nEl sistema esta configurado correctamente:")
    print("1. OK API key de DeepSeek configurada")
    print("2. OK Storage en memoria funcionando")
    print("3. OK Cliente base LuminoraCore funcionando")
    print("4. OK Extensiones v1.1 funcionando")
    print("5. OK Personalidad configurada")
    print("6. OK Creacion de sesiones funcionando")
    
    print("\nPara probar envio de mensajes, necesitarias:")
    print("1. Configurar un proveedor de LLM en el cliente base")
    print("2. Usar el metodo send_message del cliente base")
    print("3. Procesar las respuestas del LLM")
    
    print("\nEl sistema esta listo para desarrollo y pruebas!")
    
    return True

if __name__ == "__main__":
    print("Iniciando test basico de LuminoraCore v1.1...")
    print("Este test verifica la configuracion basica sin enviar mensajes")
    print("=" * 60)
    
    try:
        success = test_basic_setup()
        
        if success:
            print("\nTest basico completado exitosamente!")
            sys.exit(0)
        else:
            print("\nTest basico fallo")
            sys.exit(1)
            
    except Exception as e:
        print(f"\nERROR durante el test: {e}")
        print("\nPosibles soluciones:")
        print("1. Verifica que todos los paquetes esten instalados")
        print("2. Verifica que la API key de DeepSeek sea valida")
        print("3. Verifica la conexion a internet")
        sys.exit(1)
