#!/usr/bin/env python3
"""
DEBUG DIRECTO DEL PROBLEMA EN get_facts()
Verificar exactamente qué retorna get_facts() en el contexto real
"""

import asyncio
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore-sdk-python"))

async def test_get_facts_direct_debug():
    """Debug directo del problema en get_facts()"""
    print("=== DEBUG DIRECTO get_facts() ===")
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
        
        # TEST 1: Verificar facts existentes
        print("1. VERIFICANDO FACTS EXISTENTES:")
        all_facts = await client.get_facts("debug_memory_session_123")
        print(f"   Facts para debug_memory_session_123: {len(all_facts)}")
        for fact in all_facts:
            print(f"   Fact: {fact.get('key')} = {fact.get('value')}")
        
        # TEST 2: Probar con diferentes user_ids
        print("\n2. PROBANDO CON DIFERENTES USER_IDS:")
        
        # Probar con el user_id exacto
        facts_exact = await client.get_facts("debug_memory_session_123")
        print(f"   Facts con user_id exacto: {len(facts_exact)}")
        
        # Probar con session_id
        facts_session = await client.get_facts("debug_memory_session_123")
        print(f"   Facts con session_id: {len(facts_session)}")
        
        # TEST 3: Verificar storage directo
        print("\n3. VERIFICANDO STORAGE DIRECTO:")
        try:
            storage_facts = await storage.get_facts("debug_memory_session_123")
            print(f"   Storage facts directos: {len(storage_facts)}")
            for fact in storage_facts:
                print(f"   Storage Fact: {fact}")
        except Exception as e:
            print(f"   [ERROR] Error en storage directo: {e}")
            import traceback
            traceback.print_exc()
        
        # TEST 4: Verificar datos en DynamoDB
        print("\n4. VERIFICANDO DATOS EN DYNAMODB:")
        try:
            import boto3
            dynamodb = boto3.client('dynamodb', region_name='us-east-1')
            
            # Scan para ver todos los items
            response = dynamodb.scan(TableName=storage.table_name)
            items = response.get('Items', [])
            
            print(f"   Total items en tabla: {len(items)}")
            
            # Buscar items específicos
            user_items = []
            for item in items:
                if 'user_id' in item and item['user_id'].get('S') == "debug_memory_session_123":
                    user_items.append(item)
            
            print(f"   Items para debug_memory_session_123: {len(user_items)}")
            
            for item in user_items:
                print(f"   Item: {item.get('PK', {}).get('S', 'N/A')} | {item.get('SK', {}).get('S', 'N/A')}")
                print(f"   User ID: {item.get('user_id', {}).get('S', 'N/A')}")
                print(f"   Category: {item.get('category', {}).get('S', 'N/A')}")
                print(f"   Key: {item.get('key', {}).get('S', 'N/A')}")
                print(f"   Value: {item.get('value', {}).get('S', 'N/A')}")
                print("   ---")
                
        except Exception as e:
            print(f"   [ERROR] No se puede verificar DynamoDB: {e}")
        
        # TEST 5: Probar con user_id diferente
        print("\n5. PROBANDO CON USER_ID DIFERENTE:")
        
        # Crear nuevo user_id
        new_user_id = "test_new_user_456"
        await client.save_fact(new_user_id, "test_category", "test_key", "test_value", confidence=0.9)
        
        new_facts = await client.get_facts(new_user_id)
        print(f"   Facts para nuevo user_id: {len(new_facts)}")
        for fact in new_facts:
            print(f"   New Fact: {fact.get('key')} = {fact.get('value')}")
        
        # RESULTADO FINAL
        print("\n" + "=" * 60)
        print("RESULTADO FINAL:")
        
        if len(all_facts) > 0:
            print("[OK] get_facts() SÍ encuentra facts")
            print("[OK] El problema NO está en get_facts()")
            print("[INFO] El problema debe estar en el flujo de send_message_with_memory()")
            return True
        else:
            print("[FAIL] get_facts() NO encuentra facts")
            print("[FAIL] El problema SÍ está en get_facts()")
            return False
        
        await base_client.cleanup()
        
    except Exception as e:
        print(f"[ERROR] ERROR CRITICO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_get_facts_direct_debug())
    if success:
        print("\n[OK] get_facts() VERIFICADO - FUNCIONA")
    else:
        print("\n[FAIL] get_facts() NO FUNCIONA - HAY BUG REAL")
    sys.exit(0 if success else 1)
