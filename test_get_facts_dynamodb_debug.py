#!/usr/bin/env python3
"""
DEBUG ESPECIFICO DEL BUG EN get_facts() CON DYNAMODB
Verificar exactamente qué está pasando en la consulta
"""

import asyncio
import sys
import json
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore-sdk-python"))

async def test_get_facts_debug():
    """Debug específico del problema en get_facts()"""
    print("=== DEBUG ESPECIFICO get_facts() DYNAMODB ===")
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
        
        print("1. CONFIGURACION DE STORAGE:")
        print(f"   Table: {storage.table_name}")
        print(f"   Hash Key: {storage.hash_key_name}")
        print(f"   Range Key: {storage.range_key_name}")
        print(f"   GSI Name: {storage.gsi_name}")
        print(f"   GSI Hash: {storage.gsi_hash_key}")
        print(f"   GSI Range: {storage.gsi_range_key}")
        
        # TEST 1: Guardar facts específicos
        print("\n2. GUARDANDO FACTS ESPECIFICOS:")
        user_id = "debug_test_user_123"
        
        await client.save_fact(user_id, "personal_info", "name", "Carlos", confidence=0.9)
        await client.save_fact(user_id, "preferences", "language", "Python", confidence=0.8)
        await client.save_fact(user_id, "hobbies", "sport", "Football", confidence=0.7)
        
        print(f"   Facts guardados para user_id: {user_id}")
        
        # TEST 2: Verificar datos en DynamoDB directamente
        print("\n3. VERIFICANDO DATOS EN DYNAMODB:")
        try:
            import boto3
            dynamodb = boto3.client('dynamodb', region_name='us-east-1')
            
            # Scan para ver todos los items
            response = dynamodb.scan(TableName=storage.table_name)
            items = response.get('Items', [])
            
            print(f"   Total items en tabla: {len(items)}")
            
            # Buscar items específicos de nuestro user_id
            user_items = []
            for item in items:
                if 'user_id' in item and item['user_id'].get('S') == user_id:
                    user_items.append(item)
            
            print(f"   Items para user_id {user_id}: {len(user_items)}")
            
            for item in user_items:
                print(f"   Item: {item.get('PK', {}).get('S', 'N/A')} | {item.get('SK', {}).get('S', 'N/A')}")
                print(f"   Category: {item.get('category', {}).get('S', 'N/A')}")
                print(f"   Key: {item.get('key', {}).get('S', 'N/A')}")
                print(f"   Value: {item.get('value', {}).get('S', 'N/A')}")
                print("   ---")
                
        except Exception as e:
            print(f"   [ERROR] No se puede verificar DynamoDB directamente: {e}")
        
        # TEST 3: Probar get_facts() directamente
        print("\n4. PROBANDO get_facts() DIRECTAMENTE:")
        facts = await client.get_facts(user_id)
        
        print(f"   Facts encontrados: {len(facts)}")
        for i, fact in enumerate(facts):
            print(f"   Fact {i+1}: {fact}")
        
        # TEST 4: Probar con diferentes parámetros
        print("\n5. PROBANDO CON DIFERENTES PARAMETROS:")
        
        # Sin categoría
        facts_all = await client.get_facts(user_id)
        print(f"   Facts (sin categoría): {len(facts_all)}")
        
        # Con categoría específica
        facts_personal = await client.get_facts(user_id, "personal_info")
        print(f"   Facts (personal_info): {len(facts_personal)}")
        
        # TEST 5: Verificar método interno del storage
        print("\n6. VERIFICANDO METODO INTERNO DEL STORAGE:")
        try:
            # Llamar directamente al método del storage
            storage_facts = await storage.get_facts(user_id)
            print(f"   Storage facts directos: {len(storage_facts)}")
            for fact in storage_facts:
                print(f"   Storage Fact: {fact}")
        except Exception as e:
            print(f"   [ERROR] Error en storage directo: {e}")
            import traceback
            traceback.print_exc()
        
        # RESULTADO FINAL
        print("\n" + "=" * 60)
        print("RESULTADO FINAL:")
        
        if len(facts) >= 3:
            print("[OK] get_facts() FUNCIONA CORRECTAMENTE")
            print("[OK] El framework SÍ está bien")
            return True
        else:
            print("[FAIL] get_facts() NO FUNCIONA")
            print("[FAIL] El framework NO está bien")
            print(f"[FAIL] Facts encontrados: {len(facts)}, Esperados: 3")
            return False
        
        await base_client.cleanup()
        
    except Exception as e:
        print(f"[ERROR] ERROR CRITICO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_get_facts_debug())
    if success:
        print("\n[OK] get_facts() VERIFICADO - REALMENTE FUNCIONA")
    else:
        print("\n[FAIL] get_facts() NO FUNCIONA - HAY BUG REAL")
    sys.exit(0 if success else 1)
