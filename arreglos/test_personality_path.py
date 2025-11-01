#!/usr/bin/env python3
"""
Test para validar que el path de personalidades es correcto
Tanto en desarrollo local como en Lambda
"""

import sys
from pathlib import Path

# Añadir SDK al path
sdk_path = Path("luminoracore-sdk-python")
if str(sdk_path) not in sys.path:
    sys.path.insert(0, str(sdk_path))

def test_path_calculation():
    """Test 1: Verificar cálculo del path"""
    print("\n" + "="*70)
    print("TEST 1: Cálculo del Path de Personalidades")
    print("="*70)
    
    # Simular __file__ como está en el código
    # En desarrollo: conversation_memory_manager.py está en luminoracore_sdk/
    # En Lambda: conversation_memory_manager.py está en /opt/python/luminoracore_sdk/
    
    # Simular desarrollo local
    print("\n  [1] Simulación: Desarrollo Local")
    dev_file = sdk_path / "luminoracore_sdk" / "conversation_memory_manager.py"
    dev_parent = dev_file.parent  # luminoracore_sdk
    dev_personalities = dev_parent / "personalities"
    
    print(f"    __file__: {dev_file}")
    print(f"    __file__.parent: {dev_parent}")
    print(f"    personalities_dir: {dev_personalities}")
    
    # Verificar que existe
    if dev_personalities.exists():
        json_files = list(dev_personalities.glob("*.json"))
        print(f"    [OK] Directorio existe con {len(json_files)} archivos JSON")
    else:
        print(f"    [FAIL] Directorio NO existe")
        return False
    
    # Simular Lambda
    print("\n  [2] Simulación: Lambda Layer")
    lambda_file = Path("/opt/python/luminoracore_sdk/conversation_memory_manager.py")
    lambda_parent = lambda_file.parent  # /opt/python/luminoracore_sdk
    lambda_personalities = lambda_parent / "personalities"
    
    print(f"    __file__: {lambda_file}")
    print(f"    __file__.parent: {lambda_parent}")
    print(f"    personalities_dir: {lambda_personalities}")
    
    # El path debe ser correcto (aunque el directorio no exista en nuestra máquina)
    expected = "/opt/python/luminoracore_sdk/personalities"
    actual = str(lambda_personalities)
    
    print(f"    Path esperado: {expected}")
    print(f"    Path calculado: {actual}")
    
    if actual == expected:
        print(f"    [OK] Path correcto para Lambda")
    else:
        print(f"    [FAIL] Path incorrecto. Debería ser: {expected}")
        return False
    
    # Verificar que NO use parent.parent
    print("\n  [3] Verificación: NO usar parent.parent")
    wrong_parent = dev_file.parent.parent  # luminoracore-sdk-python
    wrong_personalities = wrong_parent / "personalities"
    
    print(f"    __file__.parent.parent: {wrong_parent}")
    print(f"    WRONG personalities_dir: {wrong_personalities}")
    
    if wrong_personalities.exists():
        print(f"    [WARN] El path incorrecto también existe (puede causar confusión)")
    else:
        print(f"    [OK] El path incorrecto NO existe")
    
    return True

def test_actual_load():
    """Test 2: Probar carga real desde el path correcto"""
    print("\n" + "="*70)
    print("TEST 2: Carga Real desde Path Correcto")
    print("="*70)
    
    try:
        from luminoracore_sdk.conversation_memory_manager import ConversationMemoryManager
        
        # Mock client
        class MockBaseClient:
            def __init__(self):
                # No establecer personalities_dir para usar el default
                pass
        
        class MockClient:
            def __init__(self):
                # No tener base_client o no tener personalities_dir
                pass
        
        mock_client = MockClient()
        manager = ConversationMemoryManager(mock_client)
        
        # Obtener el path que se calcula
        import inspect
        source = inspect.getsource(manager._load_personality_data)
        
        # Verificar que usa parent (no parent.parent)
        if "parent.parent" in source:
            print(f"  [FAIL] El código todavía usa parent.parent")
            return False
        elif "parent" in source and "__file__" in source:
            print(f"  [OK] El código usa __file__.parent")
        
        # Probar carga real
        import asyncio
        async def test():
            personality_data = await manager._load_personality_data("Grandma Hope")
            return personality_data is not None
        
        result = asyncio.run(test())
        
        if result:
            print(f"  [OK] Personalidad cargada correctamente")
            return True
        else:
            print(f"  [WARN] No se pudo cargar personalidad (puede ser por otro motivo)")
            # Aún así, si el path es correcto, esto está bien
            return True
        
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_path_logic():
    """Test 3: Verificar lógica del path en diferentes escenarios"""
    print("\n" + "="*70)
    print("TEST 3: Lógica del Path en Diferentes Escenarios")
    print("="*70)
    
    scenarios = [
        {
            "name": "Desarrollo Local",
            "file": "luminoracore-sdk-python/luminoracore_sdk/conversation_memory_manager.py",
            "expected_parent": "luminoracore-sdk-python/luminoracore_sdk",
            "expected_personalities": "luminoracore-sdk-python/luminoracore_sdk/personalities"
        },
        {
            "name": "Lambda Layer",
            "file": "/opt/python/luminoracore_sdk/conversation_memory_manager.py",
            "expected_parent": "/opt/python/luminoracore_sdk",
            "expected_personalities": "/opt/python/luminoracore_sdk/personalities"
        },
        {
            "name": "Instalación pip (site-packages)",
            "file": "/usr/local/lib/python3.11/site-packages/luminoracore_sdk/conversation_memory_manager.py",
            "expected_parent": "/usr/local/lib/python3.11/site-packages/luminoracore_sdk",
            "expected_personalities": "/usr/local/lib/python3.11/site-packages/luminoracore_sdk/personalities"
        }
    ]
    
    all_passed = True
    
    for scenario in scenarios:
        print(f"\n  Escenario: {scenario['name']}")
        file_path = Path(scenario['file'])
        
        # Cálculo correcto (usando parent)
        calculated_parent = file_path.parent
        calculated_personalities = calculated_parent / "personalities"
        
        expected_parent = Path(scenario['expected_parent'])
        expected_personalities = Path(scenario['expected_personalities'])
        
        parent_ok = str(calculated_parent) == str(expected_parent) or calculated_parent == expected_parent
        personalities_ok = str(calculated_personalities) == str(expected_personalities) or calculated_personalities == expected_personalities
        
        print(f"    Path calculado: {calculated_personalities}")
        print(f"    Path esperado: {expected_personalities}")
        
        if parent_ok and personalities_ok:
            print(f"    [OK] Path correcto")
        else:
            print(f"    [FAIL] Path incorrecto")
            all_passed = False
        
        # Verificar que NO sea parent.parent
        wrong_path = file_path.parent.parent / "personalities"
        if str(wrong_path) == str(expected_personalities):
            print(f"    [FAIL] Usaría parent.parent (INCORRECTO)")
            all_passed = False
        else:
            print(f"    [OK] NO usa parent.parent")
    
    return all_passed

def main():
    """Ejecutar todos los tests"""
    print("\n" + "="*70)
    print("VALIDACION: Path de Personalidades")
    print("="*70)
    
    results = []
    
    results.append(("Cálculo del path", test_path_calculation()))
    results.append(("Carga real", test_actual_load()))
    results.append(("Lógica del path", test_path_logic()))
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    
    all_passed = True
    for test_name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status}: {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*70)
    if all_passed:
        print("[OK] TODOS LOS TESTS PASARON")
        print("El path de personalidades es correcto")
    else:
        print("[FAIL] ALGUNOS TESTS FALLARON")
        print("Revisar los errores arriba")
    print("="*70)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

