#!/usr/bin/env python3
"""
Test final para verificar que la corrección del backend funciona correctamente.
Este test simula exactamente el comportamiento del backend.
"""

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

class MockBaseClient:
    """Mock del base client que simula el comportamiento del backend"""
    
    def __init__(self):
        self.llm_provider = None
    
    async def send_message(self, session_id, message, personality_name, provider_config):
        """Simula el comportamiento del base client del backend"""
        
        # Verificar que el mensaje contiene contexto
        if "Contexto del usuario:" in message:
            # El framework está enviando contexto correctamente
            if "Carlos" in message and "desarrollador" in message:
                if "Como me llamo" in message or "Cual es mi nombre" in message:
                    return {"response": "Te llamas Carlos y eres desarrollador de Madrid."}
                else:
                    return {"response": f"Hola Carlos! Soy {personality_name}. ¿En qué puedo ayudarte?"}
            else:
                return {"response": f"Hola! Soy {personality_name}. ¿En qué puedo ayudarte?"}
        else:
            # Sin contexto - respuesta genérica
            return {"response": f"Hola! Soy {personality_name}. ¿En qué puedo ayudarte?"}

async def test_final_backend_fix():
    """Test final para verificar la corrección del backend"""
    
    print("=" * 80)
    print("TEST FINAL: Verificación de la corrección del backend")
    print("=" * 80)
    
    try:
        # 1. Inicialización del cliente (igual que el backend)
        print("1. Inicializando cliente (igual que el backend)...")
        
        # Crear storage con configuración exacta del backend
        dynamodb_storage = FlexibleDynamoDBStorageV11(
            table_name="luminora-sessions-v1-1",
            region_name="eu-west-1"
        )
        
        base_client = MockBaseClient()
        
        # Crear cliente v1.1 (igual que el backend)
        client_v11 = LuminoraCoreClientV11(
            base_client=base_client,
            storage_v11=dynamodb_storage
        )
        
        print("   [OK] Cliente inicializado correctamente")
        print()
        
        # 2. Test 1 - Mensaje inicial
        session_id_test = f"test_final_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        user_message_1 = "Hola, me llamo Carlos y soy desarrollador de Madrid. Trabajo en una empresa de tecnologia."
        personality_name = "Sakura"
        
        print(f"2. TEST 1 - Mensaje inicial:")
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
        
        # 3. Test 2 - Pregunta sobre información previa
        user_message_2 = "Como me llamo y donde trabajo?"
        
        print(f"3. TEST 2 - Pregunta sobre información previa:")
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
        
        # 4. Test 3 - Pregunta adicional
        user_message_3 = "Cual es mi nombre y a que me dedico?"
        
        print(f"4. TEST 3 - Pregunta adicional:")
        print(f"   Mensaje: '{user_message_3}'")
        
        result_3 = await client_v11.send_message_with_memory(
            session_id=session_id_test,
            user_message=user_message_3,
            personality_name=personality_name,
            provider_config=None
        )
        
        print(f"   Respuesta: {result_3.get('response')}")
        print(f"   Hechos en memoria: {result_3.get('memory_facts_count')}")
        print(f"   Nuevos hechos: {len(result_3.get('new_facts', []))}")
        print(f"   Contexto usado: {result_3.get('context_used')}")
        print()
        
        # 5. Verificación del resultado
        print("5. VERIFICACIÓN DEL RESULTADO:")
        print("=" * 50)
        
        # Verificar que la memoria contextual funciona
        memory_working = (
            result_1.get('memory_facts_count', 0) > 0 and
            result_2.get('memory_facts_count', 0) > 0 and
            result_3.get('memory_facts_count', 0) > 0
        )
        
        # Verificar que el contexto se usa
        context_working = (
            result_2.get('context_used', False) and
            result_3.get('context_used', False)
        )
        
        # Verificar que las respuestas son contextuales
        contextual_responses = (
            "Carlos" in result_2.get('response', '') and
            "Carlos" in result_3.get('response', '')
        )
        
        print(f"   [OK] Memoria contextual: {'FUNCIONA' if memory_working else 'FALLA'}")
        print(f"   [OK] Contexto usado: {'FUNCIONA' if context_working else 'FALLA'}")
        print(f"   [OK] Respuestas contextuales: {'FUNCIONA' if contextual_responses else 'FALLA'}")
        print()
        
        if memory_working and context_working and contextual_responses:
            print("[SUCCESS] ÉXITO: La corrección del backend funciona correctamente")
            print("   - La memoria contextual funciona")
            print("   - El contexto se usa correctamente")
            print("   - Las respuestas son contextuales")
            print("   - El framework está listo para el backend")
            return True
        else:
            print("[FAIL] FALLO: La corrección del backend NO funciona")
            print("   - Revisar los logs para identificar el problema")
            return False
        
    except Exception as e:
        print(f"[ERROR] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_final_backend_fix())
    
    if success:
        print("\n" + "=" * 80)
        print("RESULTADO FINAL: ÉXITO")
        print("El framework está corregido y listo para el backend")
        print("=" * 80)
    else:
        print("\n" + "=" * 80)
        print("RESULTADO FINAL: FALLO")
        print("El framework necesita más correcciones")
        print("=" * 80)
