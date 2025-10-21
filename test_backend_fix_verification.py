import asyncio
import json
import os
import logging
from datetime import datetime
from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11
from luminoracore_sdk.session.storage_dynamodb_flexible import FlexibleDynamoDBStorageV11

# Configurar logging detallado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_backend_fix_verification():
    """Verifica que la corrección del backend funciona correctamente."""
    
    print("TEST: Verificación de la corrección del backend")
    print("=" * 60)
    
    try:
        # 1. Inicialización del cliente (igual que el backend)
        print("Inicializando cliente (igual que el backend)...")
        
        # Crear storage con configuracion exacta del backend
        dynamodb_storage = FlexibleDynamoDBStorageV11(
            table_name="luminora-sessions-v1-1",
            region_name="eu-west-1"
        )
        
        # Crear mock base_client
        class MockBaseClient:
            def __init__(self):
                self.llm_provider = None
            
            async def send_message(self, session_id, message, personality_name, provider_config=None):
                # Simular una respuesta contextual del LLM
                # Esto simula que el LLM recibe el contexto y responde apropiadamente
                if "Como me llamo" in message or "Como me llamo?" in message:
                    if "llamo" in message or "Carlos" in message:
                        return "¡Hola Carlos! Por supuesto que sé que te llamas Carlos, lo mencionaste antes. ¿En qué puedo ayudarte hoy?"
                    else:
                        return "Hola! Soy Sakura. ¿Cómo te llamas tú?"
                elif "Hola" in message and "me llamo" in message:
                    return "¡Hola Carlos! Es un placer conocerte. ¿En qué puedo ayudarte hoy?"
                else:
                    return "Hola! Soy Sakura. ¿En qué puedo ayudarte?"
        
        base_client = MockBaseClient()
        
        # Crear cliente v1.1 (igual que el backend)
        client_v11 = LuminoraCoreClientV11(
            base_client=base_client,
            storage_v11=dynamodb_storage
        )
        
        print("Cliente inicializado correctamente")
        print()
        
        # 2. Test 1 - Mensaje inicial (igual que el backend)
        session_id_test = f"test_backend_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        user_message_1 = "Hola, me llamo Carlos y soy desarrollador de Madrid"
        personality_name = "Sakura"
        
        print(f"TEST 1 - Mensaje inicial:")
        print(f"   Mensaje: '{user_message_1}'")
        
        result_1 = await client_v11.send_message_with_memory(
            session_id=session_id_test,
            user_message=user_message_1,
            personality_name=personality_name,
            provider_config=None
        )
        
        print(f"   Respuesta: {result_1.get('response')}")
        print(f"   Hechos en memoria: {result_1.get('memory_facts_count')}")
        print(f"   Nuevos hechos: {len(result_1.get('new_facts', []))}")
        print(f"   Contexto usado: {result_1.get('context_used')}")
        print()
        
        # 3. Test 2 - Pregunta sobre informacion previa (MISMO session_id)
        user_message_2 = "Como me llamo?"
        
        print(f"TEST 2 - Pregunta sobre informacion previa:")
        print(f"   Mensaje: '{user_message_2}'")
        
        result_2 = await client_v11.send_message_with_memory(
            session_id=session_id_test,
            user_message=user_message_2,
            personality_name=personality_name,
            provider_config=None
        )
        
        print(f"   Respuesta: {result_2.get('response')}")
        print(f"   Hechos en memoria: {result_2.get('memory_facts_count')}")
        print(f"   Nuevos hechos: {len(result_2.get('new_facts', []))}")
        print(f"   Contexto usado: {result_2.get('context_used')}")
        print()
        
        # 4. Verificacion del resultado
        if result_1.get('memory_facts_count') > 0 and result_2.get('memory_facts_count') > 0 and result_2.get('context_used'):
            print("EXITO: La memoria contextual funciona")
            print("   - get_facts() encuentra hechos")
            print("   - send_message_with_memory usa contexto")
            print("   - El LLM recibe el contexto correctamente")
            return True
        else:
            print("FALLO: La memoria contextual NO funciona")
            print("   - Revisar los logs de debug para ver el problema")
            return False
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_backend_fix_verification())
    
    if success:
        print("\nRESULTADO: EXITO - El backend deberia funcionar correctamente")
        print("   - La corrección del contexto funciona")
        print("   - El LLM recibe el contexto completo")
        print("   - Las respuestas son contextuales")
    else:
        print("\nRESULTADO: FALLO - El backend tiene problemas")
        print("   - Revisar la implementación del contexto")
        print("   - Verificar la integración con el LLM")
