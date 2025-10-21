#!/usr/bin/env python3
"""
VERIFICACIÓN REAL Y EXHAUSTIVA DEL FRAMEWORK
NO DECIR QUE ESTÁ BIEN SIN VERIFICAR REALMENTE
"""

import asyncio
import sys
import json
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore-sdk-python"))

async def test_real_verification():
    """Verificación REAL del framework"""
    print("=== VERIFICACION REAL DEL FRAMEWORK ===")
    print("NO DECIR QUE ESTA BIEN SIN VERIFICAR")
    print("=" * 60)
    
    try:
        from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
        from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
        
        # Initialize
        base_client = LuminoraCoreClient()
        await base_client.initialize()
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(base_client, storage_v11=storage)
        
        # TEST 1: Crear sesión y guardar datos
        print("\n1. CREAR SESION Y GUARDAR DATOS:")
        session_id = await client.create_session(
            user_id="test_real_user",
            personality_name="alicia"
        )
        print(f"   Session ID: {session_id}")
        
        # Guardar facts
        await client.save_fact("test_real_user", "personal_info", "name", "Carlos", confidence=0.9)
        await client.save_fact("test_real_user", "preferences", "language", "Python", confidence=0.8)
        
        # Verificar que se guardaron
        facts = await client.get_facts("test_real_user")
        print(f"   Facts guardados: {len(facts)}")
        for fact in facts:
            if fact.get('key') in ['name', 'language']:
                print(f"     - {fact.get('key')}: {fact.get('value')}")
        
        # TEST 2: Enviar mensaje SIN user_id explícito (debe usar session_id)
        print("\n2. ENVIAR MENSAJE SIN USER_ID EXPLICITO:")
        result1 = await client.send_message_with_memory(
            session_id=session_id,
            user_message="What do you remember about me?",
            personality_name="alicia"
        )
        
        print(f"   Success: {result1.get('success', False)}")
        print(f"   Context used: {result1.get('context_used', False)}")
        print(f"   Response: {result1.get('response', 'No response')[:150]}...")
        
        # TEST 3: Enviar mensaje CON user_id explícito
        print("\n3. ENVIAR MENSAJE CON USER_ID EXPLICITO:")
        result2 = await client.send_message_with_memory(
            session_id=session_id,
            user_message="Tell me about my preferences",
            user_id="test_real_user",
            personality_name="alicia"
        )
        
        print(f"   Success: {result2.get('success', False)}")
        print(f"   Context used: {result2.get('context_used', False)}")
        print(f"   Response: {result2.get('response', 'No response')[:150]}...")
        
        # TEST 4: Verificar que la memoria se está usando
        print("\n4. VERIFICACION DE MEMORIA:")
        memory_used_1 = result1.get('context_used', False)
        memory_used_2 = result2.get('context_used', False)
        
        print(f"   Test 1 (sin user_id): Memory used = {memory_used_1}")
        print(f"   Test 2 (con user_id): Memory used = {memory_used_2}")
        
        # TEST 5: Verificar que los facts se están consultando correctamente
        print("\n5. VERIFICACION DE CONSULTA DE FACTS:")
        facts_after = await client.get_facts("test_real_user")
        print(f"   Facts después de conversación: {len(facts_after)}")
        
        # TEST 6: Verificar afinidad
        print("\n6. VERIFICACION DE AFINIDAD:")
        affinity = await client.get_affinity("test_real_user", "alicia")
        print(f"   Affinity: {affinity.get('current_level', 'unknown')} - {affinity.get('affinity_points', 0)} puntos")
        
        # RESULTADO FINAL
        print("\n" + "=" * 60)
        print("RESULTADO FINAL:")
        
        if memory_used_1 and memory_used_2:
            print("[OK] MEMORIA CONTEXTUAL FUNCIONANDO")
            print("[OK] El framework SÍ está bien")
        else:
            print("[FAIL] MEMORIA CONTEXTUAL NO FUNCIONA")
            print("[FAIL] El framework NO está bien")
            return False
        
        await base_client.cleanup()
        return True
        
    except Exception as e:
        print(f"[ERROR] ERROR CRITICO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_real_verification())
    if success:
        print("\n[OK] FRAMEWORK VERIFICADO - REALMENTE FUNCIONA")
    else:
        print("\n[FAIL] FRAMEWORK NO FUNCIONA - NO DECIR QUE ESTA BIEN")
    sys.exit(0 if success else 1)
