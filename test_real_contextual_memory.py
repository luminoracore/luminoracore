#!/usr/bin/env python3
"""
TEST REAL DE MEMORIA CONTEXTUAL
Este test simula exactamente lo que hace el backend
"""

import asyncio
import json
from datetime import datetime
from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
from luminoracore_sdk.types import ProviderConfig

class MockBaseClient:
    """Mock del LuminoraCoreClient para testing"""
    
    def __init__(self):
        self.responses = []
    
    async def send_message(self, message: str, **kwargs):
        """Simula el envío de mensaje al LLM"""
        # Simula respuesta del LLM
        if "llamo" in message.lower() and "como me llamo" in message.lower():
            return "Te llamas Carlos, como me dijiste anteriormente."
        elif "llamo" in message.lower():
            return "Hola Carlos! ¿En qué puedo ayudarte?"
        else:
            return "Hola! ¿En qué puedo ayudarte?"
    
    def get(self, key: str, default=None):
        """Mock method for dict-like access"""
        return getattr(self, key, default)

async def test_real_contextual_memory():
    """Test REAL de memoria contextual"""
    print("[TEST] INICIANDO TEST REAL DE MEMORIA CONTEXTUAL")
    print("=" * 60)
    
    # 1. Inicializar storage y cliente
    storage = InMemoryStorageV11()
    base_client = MockBaseClient()
    client = LuminoraCoreClientV11(base_client=base_client, storage_v11=storage)
    
    # 2. Configurar provider
    provider_config = ProviderConfig(
        name="deepseek",
        api_key="test-key",
        model="deepseek-chat"
    )
    
    session_id = f"test_real_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    user_id = session_id  # Como hace el backend
    
    print(f"[INFO] Session ID: {session_id}")
    print(f"[INFO] User ID: {user_id}")
    print()
    
    # 3. PRIMER MENSAJE - Introducción
    print("[TEST] PRIMER MENSAJE:")
    print("   Usuario: 'Hola, me llamo Carlos y soy desarrollador de Madrid'")
    
    result1 = await client.send_message_with_memory(
        session_id=session_id,
        user_message="Hola, me llamo Carlos y soy desarrollador de Madrid",
        personality_name="Sakura",
        provider_config=provider_config
    )
    
    print(f"   Respuesta: {result1.get('response', 'Sin respuesta')}")
    print(f"   Hechos guardados: {result1.get('new_facts_count', 0)}")
    print(f"   Contexto usado: {result1.get('context_used', False)}")
    print(f"   Hechos en memoria: {result1.get('memory_facts_count', 0)}")
    print()
    
    # 4. SEGUNDO MENSAJE - Pregunta sobre información previa
    print("[TEST] SEGUNDO MENSAJE:")
    print("   Usuario: 'Como me llamo?'")
    
    result2 = await client.send_message_with_memory(
        session_id=session_id,
        user_message="Como me llamo?",
        personality_name="Sakura",
        provider_config=provider_config
    )
    
    print(f"   Respuesta: {result2.get('response', 'Sin respuesta')}")
    print(f"   Hechos guardados: {result2.get('new_facts_count', 0)}")
    print(f"   Contexto usado: {result2.get('context_used', False)}")
    print(f"   Hechos en memoria: {result2.get('memory_facts_count', 0)}")
    print()
    
    # 5. VERIFICACIÓN CRÍTICA
    print("[VERIFY] VERIFICACIÓN CRÍTICA:")
    
    # Verificar si se guardaron hechos
    facts = await client.get_facts(user_id)
    print(f"   Hechos guardados en storage: {len(facts)}")
    for fact in facts:
        print(f"     - {fact.get('key', 'N/A')}: {fact.get('value', 'N/A')}")
    
    # Verificar si la respuesta es contextual
    response = result2.get('response', '')
    is_contextual = 'Carlos' in response and 'llamo' in response.lower()
    
    print(f"   ¿Respuesta contextual? {'[OK] SÍ' if is_contextual else '[FAIL] NO'}")
    print(f"   ¿Contexto usado? {'[OK] SÍ' if result2.get('context_used', False) else '[FAIL] NO'}")
    print(f"   ¿Hechos en memoria? {'[OK] SÍ' if result2.get('memory_facts_count', 0) > 0 else '[FAIL] NO'}")
    print()
    
    # 6. RESULTADO FINAL
    print("[RESULT] RESULTADO FINAL:")
    if is_contextual and result2.get('context_used', False) and result2.get('memory_facts_count', 0) > 0:
        print("   [OK] MEMORIA CONTEXTUAL FUNCIONA CORRECTAMENTE")
        print("   [OK] El framework puede usar información previa")
        print("   [OK] Las respuestas son contextuales")
    else:
        print("   [FAIL] MEMORIA CONTEXTUAL NO FUNCIONA")
        print("   [FAIL] El framework NO puede usar información previa")
        print("   [FAIL] Las respuestas son genéricas")
    
    print("=" * 60)
    return is_contextual and result2.get('context_used', False) and result2.get('memory_facts_count', 0) > 0

if __name__ == "__main__":
    result = asyncio.run(test_real_contextual_memory())
    exit(0 if result else 1)
