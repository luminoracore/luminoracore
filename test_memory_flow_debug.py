#!/usr/bin/env python3
"""
DEBUG DEL FLUJO DE MEMORIA EN ConversationMemoryManager
Verificar por qué no usa los facts encontrados
"""

import asyncio
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore-sdk-python"))

async def test_memory_flow_debug():
    """Debug del flujo de memoria en ConversationMemoryManager"""
    print("=== DEBUG FLUJO DE MEMORIA ===")
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
        
        # TEST 1: Verificar conversation manager
        print("1. VERIFICANDO CONVERSATION MANAGER:")
        if hasattr(client, 'conversation_manager') and client.conversation_manager:
            print("   [OK] Conversation manager disponible")
            
            # Verificar método send_message_with_full_context directamente
            session_id = "debug_memory_session_123"
            user_id = session_id
            
            print(f"   Probando con session_id: {session_id}")
            print(f"   Probando con user_id: {user_id}")
            
            # Llamar directamente al método
            response = await client.conversation_manager.send_message_with_full_context(
                session_id=session_id,
                user_message="¿Qué sabes sobre mí?",
                user_id=user_id,
                personality_name="assistant"
            )
            
            print(f"   Response: {response.get('response', 'N/A')}")
            print(f"   Memory facts count: {response.get('memory_facts_count', 0)}")
            print(f"   Context used: {response.get('context_used', False)}")
            print(f"   User facts: {len(response.get('user_facts', []))}")
            
            # Mostrar user_facts si existen
            if response.get('user_facts'):
                print("   User facts encontrados:")
                for fact in response.get('user_facts', []):
                    print(f"     - {fact.get('key')}: {fact.get('value')}")
            else:
                print("   [PROBLEMA] No hay user_facts en la respuesta")
        
        else:
            print("   [ERROR] Conversation manager no disponible")
            return False
        
        # TEST 2: Verificar el flujo paso a paso
        print("\n2. VERIFICANDO FLUJO PASO A PASO:")
        
        # Paso 1: Get conversation history
        print("   Paso 1: Get conversation history")
        conversation_history = await client.conversation_manager._get_conversation_history(session_id)
        print(f"   Conversation history: {len(conversation_history)} items")
        
        # Paso 2: Get user facts
        print("   Paso 2: Get user facts")
        user_facts = await client.get_facts(user_id)
        print(f"   User facts: {len(user_facts)} items")
        for fact in user_facts[:3]:  # Mostrar solo los primeros 3
            print(f"     - {fact.get('key')}: {fact.get('value')}")
        
        # Paso 3: Get affinity
        print("   Paso 3: Get affinity")
        affinity = await client.get_affinity(user_id, "assistant")
        print(f"   Affinity: {affinity}")
        
        # Paso 4: Build context
        print("   Paso 4: Build context")
        try:
            context = await client.conversation_manager._build_llm_context(
                session_id=session_id,
                personality_name="assistant",
                conversation_history=conversation_history,
                user_facts=user_facts,
                affinity=affinity
            )
            print(f"   Context built: {len(context.get('messages', []))} messages")
            
            # Mostrar el contexto
            for i, message in enumerate(context.get('messages', [])):
                print(f"   Message {i+1}: {message.get('role', 'N/A')} - {str(message.get('content', ''))[:100]}...")
                
        except Exception as e:
            print(f"   [ERROR] Error building context: {e}")
            import traceback
            traceback.print_exc()
        
        # TEST 3: Verificar si el problema está en el filtrado
        print("\n3. VERIFICANDO FILTRADO DE FACTS:")
        
        # Verificar si hay facts de personal_info
        personal_facts = [fact for fact in user_facts if fact.get('category') == 'personal_info']
        print(f"   Personal info facts: {len(personal_facts)}")
        for fact in personal_facts:
            print(f"     - {fact.get('key')}: {fact.get('value')}")
        
        # Verificar si hay facts de preferences
        preference_facts = [fact for fact in user_facts if fact.get('category') == 'preferences']
        print(f"   Preference facts: {len(preference_facts)}")
        for fact in preference_facts:
            print(f"     - {fact.get('key')}: {fact.get('value')}")
        
        # RESULTADO FINAL
        print("\n" + "=" * 60)
        print("RESULTADO FINAL:")
        
        if len(user_facts) > 0:
            print("[OK] get_facts() encuentra facts")
            print("[INFO] El problema puede estar en el filtrado o uso de facts")
            print("[INFO] Verificar si los facts se usan en el contexto del LLM")
            return True
        else:
            print("[FAIL] get_facts() no encuentra facts")
            return False
        
        await base_client.cleanup()
        
    except Exception as e:
        print(f"[ERROR] ERROR CRITICO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_memory_flow_debug())
    if success:
        print("\n[OK] FLUJO DE MEMORIA VERIFICADO")
    else:
        print("\n[FAIL] FLUJO DE MEMORIA NO FUNCIONA")
    sys.exit(0 if success else 1)
