#!/usr/bin/env python3
"""
DEBUG COMPLETO DEL FLUJO send_message_with_memory()
Verificar exactamente dónde falla la memoria contextual
"""

import asyncio
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore-sdk-python"))

async def test_send_message_memory_debug():
    """Debug completo del flujo de memoria contextual"""
    print("=== DEBUG COMPLETO send_message_with_memory() ===")
    print("=" * 60)
    
    try:
        from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
        from luminoracore_sdk.session.storage_v1_1 import FlexibleDynamoDBStorageV11
        
        # Initialize
        base_client = LuminoraCoreClient()
        await base_client.initialize()
        
        # Usar tabla existente
        storage = FlexibleDynamoDBStorageV11(
            table_name="demo-luminora-sessions",
            region_name="us-east-1",
            hash_key_name="PK",
            range_key_name="SK"
        )
        client = LuminoraCoreClientV11(base_client, storage_v11=storage)
        
        # TEST 1: Primera conversación - guardar facts
        print("1. PRIMERA CONVERSACION - GUARDANDO FACTS:")
        session_id = "debug_memory_session_123"
        user_id = session_id  # Usar session_id como user_id
        
        # Simular primera conversación
        response1 = await client.send_message_with_memory(
            session_id=session_id,
            user_message="Hola, me llamo Carlos y me gusta programar en Python",
            user_id=user_id,
            personality_name="assistant"
        )
        
        print(f"   Response 1 success: {response1.get('success', False)}")
        print(f"   Response 1: {response1.get('response', 'N/A')[:100]}...")
        print(f"   New facts: {len(response1.get('new_facts', []))}")
        for fact in response1.get('new_facts', []):
            print(f"   New Fact: {fact}")
        
        # TEST 2: Verificar facts guardados
        print("\n2. VERIFICANDO FACTS GUARDADOS:")
        facts = await client.get_facts(user_id)
        print(f"   Facts encontrados: {len(facts)}")
        for fact in facts:
            print(f"   Fact: {fact.get('key')} = {fact.get('value')}")
        
        # TEST 3: Segunda conversación - debería usar memoria
        print("\n3. SEGUNDA CONVERSACION - DEBERIA USAR MEMORIA:")
        response2 = await client.send_message_with_memory(
            session_id=session_id,
            user_message="¿Cómo me llamo y qué me gusta?",
            user_id=user_id,
            personality_name="assistant"
        )
        
        print(f"   Response 2 success: {response2.get('success', False)}")
        print(f"   Response 2: {response2.get('response', 'N/A')}")
        print(f"   Memory facts count: {response2.get('memory_facts_count', 0)}")
        print(f"   Context used: {response2.get('context_used', False)}")
        print(f"   User facts: {len(response2.get('user_facts', []))}")
        
        # TEST 4: Verificar flujo interno
        print("\n4. VERIFICANDO FLUJO INTERNO:")
        
        # Verificar conversation manager
        if hasattr(client, 'conversation_manager') and client.conversation_manager:
            print("   [OK] Conversation manager disponible")
            
            # Verificar método send_message_with_full_context
            try:
                response3 = await client.conversation_manager.send_message_with_full_context(
                    session_id=session_id,
                    user_message="¿Qué sabes sobre mí?",
                    user_id=user_id,
                    personality_name="assistant"
                )
                
                print(f"   Response 3 (directo): {response3.get('response', 'N/A')[:100]}...")
                print(f"   Memory facts (directo): {len(response3.get('user_facts', []))}")
                
            except Exception as e:
                print(f"   [ERROR] Error en conversation manager: {e}")
        else:
            print("   [ERROR] Conversation manager no disponible")
        
        # TEST 5: Verificar affinity
        print("\n5. VERIFICANDO AFFINITY:")
        affinity = await client.get_affinity(user_id, "assistant")
        print(f"   Affinity: {affinity}")
        
        # RESULTADO FINAL
        print("\n" + "=" * 60)
        print("RESULTADO FINAL:")
        
        # Verificar si la segunda respuesta usa memoria
        if response2.get('memory_facts_count', 0) > 0:
            print("[OK] Memoria contextual FUNCIONA")
            print("[OK] El framework SÍ está bien")
            return True
        else:
            print("[FAIL] Memoria contextual NO FUNCIONA")
            print("[FAIL] El framework NO está bien")
            print(f"[FAIL] Memory facts count: {response2.get('memory_facts_count', 0)}")
            return False
        
        await base_client.cleanup()
        
    except Exception as e:
        print(f"[ERROR] ERROR CRITICO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_send_message_memory_debug())
    if success:
        print("\n[OK] MEMORIA CONTEXTUAL VERIFICADA - REALMENTE FUNCIONA")
    else:
        print("\n[FAIL] MEMORIA CONTEXTUAL NO FUNCIONA - HAY BUG REAL")
    sys.exit(0 if success else 1)
