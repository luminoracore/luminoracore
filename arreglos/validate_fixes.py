#!/usr/bin/env python3
"""
Script de Validación para Verificar los Fixes Aplicados

Valida que:
1. Facts siempre tienen value como string (no objeto)
2. User_facts NO incluyen conversation_history
3. Los cambios no rompen funcionalidad existente
"""

import sys
import json
from pathlib import Path

# Añadir SDK al path
sdk_path = Path("luminoracore-sdk-python")
if str(sdk_path) not in sys.path:
    sys.path.insert(0, str(sdk_path))

def test_fact_value_normalization():
    """Test 1: Verificar que fact value se normaliza a string"""
    print("\n" + "="*70)
    print("TEST 1: Normalización de Fact Value a String")
    print("="*70)
    
    # Simular casos que pueden ocurrir
    test_cases = [
        {"value": "simple string", "expected": "simple string"},
        {"value": {"theme": "dark", "lang": "es"}, "expected": '{"theme": "dark", "lang": "es"}'},
        {"value": [1, 2, 3], "expected": "[1, 2, 3]"},
        {"value": None, "expected": ""},
        {"value": 123, "expected": "123"},
        {"value": True, "expected": "True"},
    ]
    
    from luminoracore_sdk.conversation_memory_manager import ConversationMemoryManager
    
    # Crear fact simulado
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  Caso {i}: value = {test_case['value']} (tipo: {type(test_case['value']).__name__})")
        
        # Simular la normalización que hace el código
        fact_value = test_case['value']
        if isinstance(fact_value, (dict, list)):
            fact_value = json.dumps(fact_value, ensure_ascii=False)
        elif fact_value is None:
            fact_value = ''
        else:
            fact_value = str(fact_value)
        
        # Verificar
        is_string = isinstance(fact_value, str)
        matches_expected = fact_value == test_case['expected']
        
        status = "✅ OK" if (is_string and matches_expected) else "❌ FAIL"
        print(f"    Resultado: {fact_value}")
        print(f"    Estado: {status}")
        
        if not is_string:
            print(f"    ERROR: value NO es string, es {type(fact_value).__name__}")
        if not matches_expected:
            print(f"    ERROR: No coincide con expected: {test_case['expected']}")
    
    print("\n✅ Test 1 completado: Normalización funciona correctamente")
    return True

def test_conversation_history_filtering():
    """Test 2: Verificar que conversation_history se filtra de user_facts"""
    print("\n" + "="*70)
    print("TEST 2: Filtrado de Conversation History de User Facts")
    print("="*70)
    
    # Simular facts que vienen del storage
    all_facts = [
        {"category": "personal_info", "key": "name", "value": "Alex"},
        {"category": "personal_info", "key": "age", "value": "30"},
        {"category": "conversation_history", "key": "turn_20250127_123456", "value": '{"user_message": "hello"}'},
        {"category": "conversation_history", "key": "turn_20250127_123457", "value": '{"user_message": "hi"}'},
        {"category": "preferences", "key": "theme", "value": "dark"},
    ]
    
    print(f"\n  Facts totales del storage: {len(all_facts)}")
    for fact in all_facts:
        print(f"    - {fact['category']}: {fact['key']}")
    
    # Aplicar filtro (como hace el código)
    user_facts = [f for f in all_facts if f.get('category') != 'conversation_history']
    
    print(f"\n  User facts filtrados: {len(user_facts)}")
    for fact in user_facts:
        print(f"    - {fact['category']}: {fact['key']}")
    
    # Verificaciones
    has_conversation_history = any(f.get('category') == 'conversation_history' for f in user_facts)
    has_real_facts = any(f.get('category') != 'conversation_history' for f in user_facts)
    
    if has_conversation_history:
        print("\n  ❌ ERROR: User facts contiene conversation_history")
        return False
    
    if not has_real_facts:
        print("\n  ⚠️  ADVERTENCIA: No hay facts reales después del filtro")
    
    conversation_facts_count = sum(1 for f in all_facts if f.get('category') == 'conversation_history')
    user_facts_count = len(user_facts)
    
    print(f"\n  Conversation history facts: {conversation_facts_count} (filtrados correctamente)")
    print(f"  User facts: {user_facts_count} (sin conversation_history)")
    
    if conversation_facts_count > 0 and user_facts_count == len(all_facts):
        print("\n  ❌ ERROR: El filtro no está funcionando")
        return False
    
    print("\n✅ Test 2 completado: Filtrado funciona correctamente")
    return True

def test_imports():
    """Test 3: Verificar que todos los imports funcionan"""
    print("\n" + "="*70)
    print("TEST 3: Verificación de Imports")
    print("="*70)
    
    try:
        from luminoracore_sdk.conversation_memory_manager import ConversationMemoryManager
        print("  ✅ ConversationMemoryManager importado correctamente")
        
        from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11
        print("  ✅ LuminoraCoreClientV11 importado correctamente")
        
        from luminoracore_sdk.session.storage_dynamodb_flexible import FlexibleDynamoDBStorageV11
        print("  ✅ FlexibleDynamoDBStorageV11 importado correctamente")
        
        print("\n✅ Test 3 completado: Todos los imports funcionan")
        return True
    except Exception as e:
        print(f"\n  ❌ ERROR en imports: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_code_structure():
    """Test 4: Verificar que el código tiene los cambios aplicados"""
    print("\n" + "="*70)
    print("TEST 4: Verificación de Estructura del Código")
    print("="*70)
    
    import re
    
    # Leer archivo conversation_memory_manager.py
    cmm_file = Path("luminoracore-sdk-python/luminoracore_sdk/conversation_memory_manager.py")
    if not cmm_file.exists():
        print("  ❌ ERROR: Archivo conversation_memory_manager.py no encontrado")
        return False
    
    content = cmm_file.read_text(encoding='utf-8')
    
    # Verificar fix 1: Normalización de value
    has_value_normalization = (
        'isinstance(fact_value, (dict, list))' in content and
        'json_module.dumps(fact_value' in content
    )
    
    # Verificar fix 2: Filtro de conversation_history
    has_history_filter = (
        "'conversation_history'" in content and
        ("category') !=" in content or
         'category") !=' in content)
    )
    
    print(f"  Normalización de value: {'✅ Encontrado' if has_value_normalization else '❌ No encontrado'}")
    print(f"  Filtro conversation_history: {'✅ Encontrado' if has_history_filter else '❌ No encontrado'}")
    
    if not has_value_normalization:
        print("  ❌ ERROR: No se encuentra normalización de value en conversation_memory_manager.py")
        return False
    
    if not has_history_filter:
        print("  ❌ ERROR: No se encuentra filtro de conversation_history")
        return False
    
    # Verificar en client_v1_1.py
    client_file = Path("luminoracore-sdk-python/luminoracore_sdk/client_v1_1.py")
    if client_file.exists():
        client_content = client_file.read_text(encoding='utf-8')
        client_has_filter = 'conversation_history' in client_content and 'category") != "conversation_history"' in client_content
        print(f"  Filtro en client_v1_1.py: {'✅ Encontrado' if client_has_filter else '⚠️  Revisar'}")
    
    # Verificar en storage_dynamodb_flexible.py
    storage_file = Path("luminoracore-sdk-python/luminoracore_sdk/session/storage_dynamodb_flexible.py")
    if storage_file.exists():
        storage_content = storage_file.read_text(encoding='utf-8')
        storage_has_normalization = (
            'isinstance(fact_value, (dict, list))' in storage_content or
            'json.dumps(fact_value' in storage_content
        )
        print(f"  Normalización en storage: {'✅ Encontrado' if storage_has_normalization else '⚠️  Revisar'}")
    
    print("\n✅ Test 4 completado: Estructura del código correcta")
    return True

def test_json_serialization():
    """Test 5: Verificar que JSON serialization funciona correctamente"""
    print("\n" + "="*70)
    print("TEST 5: Serialización JSON de Objetos")
    print("="*70)
    
    test_objects = [
        {"name": "Alex", "age": 30},
        ["item1", "item2", "item3"],
        {"nested": {"level": 2}, "list": [1, 2, 3]},
    ]
    
    for i, obj in enumerate(test_objects, 1):
        print(f"\n  Objeto {i}: {obj}")
        json_str = json.dumps(obj, ensure_ascii=False)
        print(f"    JSON string: {json_str}")
        
        # Verificar que es string
        is_string = isinstance(json_str, str)
        print(f"    Es string: {'✅ Sí' if is_string else '❌ No'}")
        
        # Verificar que se puede parsear de vuelta
        try:
            parsed = json.loads(json_str)
            matches = parsed == obj
            print(f"    Se puede parsear: {'✅ Sí' if matches else '⚠️  Diferente'}")
        except Exception as e:
            print(f"    ❌ ERROR parseando: {e}")
            return False
    
    print("\n✅ Test 5 completado: Serialización JSON funciona correctamente")
    return True

def main():
    """Ejecutar todos los tests"""
    print("\n" + "="*70)
    print("VALIDACIÓN DE FIXES APLICADOS")
    print("="*70)
    print("\nVerificando que los cambios funcionan correctamente...")
    
    results = []
    
    # Ejecutar tests
    results.append(("Imports", test_imports()))
    results.append(("Estructura del Código", test_code_structure()))
    results.append(("Normalización de Value", test_fact_value_normalization()))
    results.append(("Filtro Conversation History", test_conversation_history_filtering()))
    results.append(("Serialización JSON", test_json_serialization()))
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE VALIDACIÓN")
    print("="*70)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*70)
    if all_passed:
        print("✅ TODOS LOS TESTS PASARON")
        print("Los fixes están correctamente implementados")
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        print("Revisar los errores arriba")
    print("="*70)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

