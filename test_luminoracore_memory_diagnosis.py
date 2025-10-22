#!/usr/bin/env python3
"""
DIAGNÓSTICO COMPLETO: LuminoraCore v1.1 - Sistema de Memoria con DynamoDB
==========================================================================

Este script realiza un diagnóstico exhaustivo del sistema de memoria de
LuminoraCore v1.1 para determinar si realmente hay un bug o si es un
problema de configuración.

Tests que realiza:
1. ✅ Verificar conexión con DynamoDB
2. ✅ Guardar un fact en DynamoDB
3. ✅ Recuperar el fact guardado
4. ✅ Verificar que get_facts() funciona correctamente
5. ✅ Test completo end-to-end de memoria contextual
"""

import asyncio
import sys
import os
from datetime import datetime
import boto3
from decimal import Decimal

# Configuración de colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


async def test_1_dynamodb_connection():
    """Test 1: Verificar conexión básica con DynamoDB"""
    print_header("TEST 1: Conexión con DynamoDB")
    
    try:
        # Obtener configuración
        table_name = os.getenv("DYNAMODB_TABLE_NAME", "luminoracore-sessions")
        region = os.getenv("AWS_REGION", "eu-west-1")
        
        print_info(f"Tabla: {table_name}")
        print_info(f"Región: {region}")
        
        # Intentar conectar
        dynamodb = boto3.resource('dynamodb', region_name=region)
        table = dynamodb.Table(table_name)
        
        # Verificar que la tabla existe
        table.load()
        
        print_success(f"Conexión exitosa con tabla '{table_name}'")
        print_info(f"Estado de la tabla: {table.table_status}")
        print_info(f"Items estimados: {table.item_count}")
        
        # Obtener esquema de la tabla
        key_schema = table.key_schema
        hash_key = None
        range_key = None
        
        for key in key_schema:
            if key['KeyType'] == 'HASH':
                hash_key = key['AttributeName']
            elif key['KeyType'] == 'RANGE':
                range_key = key['AttributeName']
        
        print_info(f"Hash Key: {hash_key}")
        print_info(f"Range Key: {range_key}")
        
        return True, table, hash_key, range_key
        
    except Exception as e:
        print_error(f"Error al conectar con DynamoDB: {e}")
        return False, None, None, None


async def test_2_save_fact_directly(table, hash_key, range_key):
    """Test 2: Guardar un fact directamente en DynamoDB"""
    print_header("TEST 2: Guardar Fact Directamente en DynamoDB")
    
    if not table:
        print_error("No se pudo conectar a la tabla")
        return False
    
    try:
        # Crear un fact de prueba
        test_user_id = "test_diagnosis_user"
        test_fact = {
            hash_key: f"{test_user_id}_test_session",
            range_key: f"FACT#{datetime.now().isoformat()}",
            'user_id': test_user_id,
            'category': 'test_info',
            'key': 'test_name',
            'value': 'TestUser',
            'confidence': Decimal('1.0'),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        print_info(f"Guardando fact de prueba para user_id: {test_user_id}")
        print_info(f"Fact: category=test_info, key=test_name, value=TestUser")
        
        # Guardar en DynamoDB
        table.put_item(Item=test_fact)
        
        print_success("Fact guardado exitosamente en DynamoDB")
        
        # Verificar que se guardó
        response = table.scan(
            FilterExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': test_user_id}
        )
        
        items_found = response.get('Items', [])
        print_info(f"Items encontrados para {test_user_id}: {len(items_found)}")
        
        if items_found:
            print_success(f"Verificación: El fact se guardó correctamente")
            return True, test_user_id
        else:
            print_error("Verificación: El fact NO se encontró después de guardarlo")
            return False, test_user_id
            
    except Exception as e:
        print_error(f"Error al guardar fact: {e}")
        return False, None


async def test_3_get_facts_directly(table, test_user_id, range_key):
    """Test 3: Recuperar facts directamente de DynamoDB usando SCAN"""
    print_header("TEST 3: Recuperar Facts con SCAN (método del framework)")
    
    if not table or not test_user_id:
        print_error("No se pudo completar el test anterior")
        return False
    
    try:
        print_info(f"Buscando facts para user_id: {test_user_id}")
        print_info(f"Usando FilterExpression con begins_with en range_key")
        
        # Usar el mismo método que usa FlexibleDynamoDBStorageV11.get_facts()
        response = table.scan(
            FilterExpression='user_id = :user_id AND begins_with(#range_key, :fact_prefix)',
            ExpressionAttributeNames={
                '#range_key': range_key
            },
            ExpressionAttributeValues={
                ':user_id': test_user_id,
                ':fact_prefix': 'FACT#'
            }
        )
        
        items = response.get('Items', [])
        print_info(f"Items retornados por SCAN: {len(items)}")
        
        if items:
            print_success(f"SCAN encontró {len(items)} fact(s)")
            for i, item in enumerate(items):
                print_info(f"  Fact {i+1}: category={item.get('category')}, key={item.get('key')}, value={item.get('value')}")
            return True
        else:
            print_error("SCAN NO encontró ningún fact")
            print_warning("Esto indica que el problema está en la FilterExpression o en el range_key")
            
            # Debug: intentar un scan sin filtros
            print_info("Intentando SCAN sin filtros para ver qué hay en la tabla...")
            response_all = table.scan(
                FilterExpression='user_id = :user_id',
                ExpressionAttributeValues={':user_id': test_user_id}
            )
            all_items = response_all.get('Items', [])
            print_info(f"Items totales para el usuario (sin filtro de FACT#): {len(all_items)}")
            
            if all_items:
                print_warning("Hay items pero no coinciden con el filtro begins_with(FACT#)")
                for item in all_items:
                    print_info(f"  Range key encontrado: {item.get(range_key)}")
            
            return False
            
    except Exception as e:
        print_error(f"Error al recuperar facts: {e}")
        return False


async def test_4_framework_get_facts():
    """Test 4: Usar get_facts() del framework LuminoraCore"""
    print_header("TEST 4: get_facts() del Framework LuminoraCore")
    
    try:
        # Importar el SDK
        from luminoracore_sdk.session.storage_dynamodb_flexible import FlexibleDynamoDBStorageV11
        
        table_name = os.getenv("DYNAMODB_TABLE_NAME", "luminoracore-sessions")
        region = os.getenv("AWS_REGION", "eu-west-1")
        
        print_info(f"Inicializando FlexibleDynamoDBStorageV11")
        print_info(f"Tabla: {table_name}")
        
        # Crear storage
        storage = FlexibleDynamoDBStorageV11(
            table_name=table_name,
            region_name=region
        )
        
        print_success("Storage inicializado correctamente")
        
        # Usar el user_id del test anterior
        test_user_id = "test_diagnosis_user"
        
        print_info(f"Llamando a storage.get_facts('{test_user_id}')")
        
        # Llamar a get_facts
        facts = await storage.get_facts(test_user_id)
        
        print_info(f"get_facts() retornó: {len(facts)} facts")
        
        if facts:
            print_success(f"get_facts() FUNCIONA CORRECTAMENTE - Recuperó {len(facts)} fact(s)")
            for i, fact in enumerate(facts):
                print_info(f"  Fact {i+1}: category={fact.get('category')}, key={fact.get('key')}, value={fact.get('value')}")
            return True
        else:
            print_error("get_facts() retornó lista vacía []")
            print_warning("El framework NO puede recuperar los facts que guardó")
            return False
            
    except Exception as e:
        print_error(f"Error en test del framework: {e}")
        import traceback
        print(traceback.format_exc())
        return False


async def test_5_end_to_end_memory():
    """Test 5: Test completo end-to-end del sistema de memoria"""
    print_header("TEST 5: Test End-to-End del Sistema de Memoria")
    
    try:
        from luminoracore_sdk import LuminoraCoreClientV11
        from luminoracore_sdk.session.storage_dynamodb_flexible import FlexibleDynamoDBStorageV11
        
        table_name = os.getenv("DYNAMODB_TABLE_NAME", "luminoracore-sessions")
        region = os.getenv("AWS_REGION", "eu-west-1")
        
        # Crear cliente
        storage = FlexibleDynamoDBStorageV11(
            table_name=table_name,
            region_name=region
        )
        
        # Crear cliente sin base_client (solo para test de memoria)
        client = LuminoraCoreClientV11(
            base_client=None,
            storage_v11=storage
        )
        
        test_user_id = "test_e2e_user"
        
        print_info("1. Guardando un fact...")
        await client.save_fact(
            user_id=test_user_id,
            category="personal_info",
            key="name",
            value="Carlos E2E"
        )
        print_success("Fact guardado")
        
        print_info("2. Recuperando facts...")
        facts = await client.get_facts(test_user_id)
        
        print_info(f"Facts recuperados: {len(facts)}")
        
        if facts:
            print_success("TEST END-TO-END EXITOSO")
            print_success("El sistema de memoria funciona correctamente")
            for fact in facts:
                print_info(f"  - {fact.get('key')}: {fact.get('value')}")
            return True
        else:
            print_error("TEST END-TO-END FALLIDO")
            print_error("El sistema NO puede recuperar los facts que guarda")
            return False
            
    except Exception as e:
        print_error(f"Error en test end-to-end: {e}")
        import traceback
        print(traceback.format_exc())
        return False


async def run_all_tests():
    """Ejecutar todos los tests de diagnóstico"""
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║  LUMINORACORE v1.1 - DIAGNÓSTICO COMPLETO DE SISTEMA DE MEMORIA  ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    results = {}
    
    # Test 1: Conexión
    success, table, hash_key, range_key = await test_1_dynamodb_connection()
    results['connection'] = success
    
    if not success:
        print_error("\nDIAGNÓSTICO ABORTADO: No se pudo conectar con DynamoDB")
        return False
    
    # Test 2: Guardar fact
    success, test_user_id = await test_2_save_fact_directly(table, hash_key, range_key)
    results['save_fact'] = success
    
    # Test 3: Recuperar fact con SCAN
    success = await test_3_get_facts_directly(table, test_user_id, range_key)
    results['get_facts_scan'] = success
    
    # Test 4: get_facts() del framework
    success = await test_4_framework_get_facts()
    results['framework_get_facts'] = success
    
    # Test 5: End-to-end
    success = await test_5_end_to_end_memory()
    results['end_to_end'] = success
    
    # Resumen final
    print_header("RESUMEN DE DIAGNÓSTICO")
    
    print(f"\n{Colors.BOLD}Resultados:{Colors.END}")
    for test_name, passed in results.items():
        status = f"{Colors.GREEN}✅ PASS{Colors.END}" if passed else f"{Colors.RED}❌ FAIL{Colors.END}"
        print(f"  {test_name}: {status}")
    
    all_passed = all(results.values())
    
    print(f"\n{Colors.BOLD}Conclusión:{Colors.END}")
    if all_passed:
        print_success("TODOS LOS TESTS PASARON")
        print_success("El sistema de memoria de LuminoraCore v1.1 funciona correctamente")
        print_info("No hay bug en el framework - la memoria funciona como debe")
    else:
        print_error("ALGUNOS TESTS FALLARON")
        print_warning("Revisar los tests que fallaron para identificar el problema")
        
        if not results.get('framework_get_facts'):
            print_warning("El problema está en el método get_facts() del framework")
        if not results.get('get_facts_scan'):
            print_warning("El problema está en la FilterExpression del SCAN")
    
    return all_passed


if __name__ == "__main__":
    print(f"\n{Colors.BOLD}Ejecutando diagnóstico...{Colors.END}\n")
    
    try:
        result = asyncio.run(run_all_tests())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Diagnóstico interrumpido por el usuario{Colors.END}\n")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nError fatal en diagnóstico: {e}")
        import traceback
        print(traceback.format_exc())
        sys.exit(1)
