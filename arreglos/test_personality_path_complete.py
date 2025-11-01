#!/usr/bin/env python3
"""
Test completo para validar que las personalidades se encuentran correctamente
en el CORE y en el SDK, tanto en desarrollo como en Lambda Layer
"""

import sys
import json
from pathlib import Path

# Añadir paths
sdk_path = Path("luminoracore-sdk-python")
core_path = Path("luminoracore")

if str(sdk_path) not in sys.path:
    sys.path.insert(0, str(sdk_path))
if str(core_path) not in sys.path:
    sys.path.insert(0, str(core_path))

def test_core_find_personality():
    """Test 1: Verificar que el CORE puede encontrar personalidades"""
    print("\n" + "="*70)
    print("TEST 1: CORE - find_personality_file()")
    print("="*70)
    
    try:
        from luminoracore import find_personality_file
        
        test_names = ["Grandma Hope", "Dr. Luna", "grandma_hope", "dr_luna"]
        
        results = []
        for name in test_names:
            print(f"\n  Probando: '{name}'")
            file_path = find_personality_file(name)
            
            if file_path:
                print(f"    [OK] Archivo encontrado: {file_path.name}")
                # Verificar que es un archivo válido
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    has_persona = "persona" in data
                    print(f"    - Tiene persona: {has_persona}")
                    results.append(True)
                except Exception as e:
                    print(f"    [FAIL] Error leyendo archivo: {e}")
                    results.append(False)
            else:
                print(f"    [WARN] No se encontró archivo")
                results.append(False)
        
        success_count = sum(results)
        print(f"\n  Resultado: {success_count}/{len(test_names)} personalidades encontradas")
        return success_count > 0
        
    except ImportError as e:
        print(f"\n  [FAIL] No se puede importar find_personality_file: {e}")
        return False
    except Exception as e:
        print(f"\n  [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sdk_load_personality():
    """Test 2: Verificar que el SDK puede cargar personalidades"""
    print("\n" + "="*70)
    print("TEST 2: SDK - _load_personality_data()")
    print("="*70)
    
    try:
        from luminoracore_sdk.conversation_memory_manager import ConversationMemoryManager
        
        # Mock client
        class MockClient:
            pass
        
        manager = ConversationMemoryManager(MockClient())
        
        import asyncio
        async def test():
            test_names = ["Grandma Hope", "Dr. Luna"]
            results = []
            
            for name in test_names:
                print(f"\n  Probando: '{name}'")
                try:
                    data = await manager._load_personality_data(name)
                    if data:
                        print(f"    [OK] Datos cargados")
                        print(f"    - Tiene persona: {'persona' in data}")
                        print(f"    - Tiene core_traits: {'core_traits' in data}")
                        results.append(True)
                    else:
                        print(f"    [WARN] No se encontraron datos")
                        results.append(False)
                except Exception as e:
                    print(f"    [FAIL] Error: {e}")
                    results.append(False)
            
            return results
        
        results = asyncio.run(test())
        success_count = sum(results)
        print(f"\n  Resultado: {success_count}/{len(results)} personalidades cargadas")
        return success_count > 0
        
    except Exception as e:
        print(f"\n  [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_path_calculation_core():
    """Test 3: Verificar cálculo de path en el CORE"""
    print("\n" + "="*70)
    print("TEST 3: Path Calculation - CORE")
    print("="*70)
    
    try:
        from luminoracore.core.personality import find_personality_file
        from pathlib import Path
        
        # Simular __file__ en el core
        core_file = core_path / "luminoracore" / "core" / "personality.py"
        
        if not core_file.exists():
            print(f"  [WARN] Archivo core no encontrado: {core_file}")
            print(f"  Probando con find_personality_file directamente...")
        else:
            print(f"  Archivo core: {core_file}")
            calculated_parent = core_file.parent.parent  # luminoracore directory
            calculated_personalities = calculated_parent / "personalities"
            
            print(f"  __file__.parent.parent: {calculated_parent}")
            print(f"  personalities_dir: {calculated_personalities}")
            
            if calculated_personalities.exists():
                json_files = list(calculated_personalities.glob("*.json"))
                print(f"  [OK] Directorio existe con {len(json_files)} archivos JSON")
                return True
            else:
                print(f"  [FAIL] Directorio no existe")
                return False
        
        # Test directo
        file_path = find_personality_file("Grandma Hope")
        if file_path:
            print(f"  [OK] find_personality_file funciona: {file_path}")
            return True
        else:
            print(f"  [FAIL] find_personality_file no encontró archivo")
            return False
        
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_path_calculation_sdk():
    """Test 4: Verificar cálculo de path en el SDK"""
    print("\n" + "="*70)
    print("TEST 4: Path Calculation - SDK")
    print("="*70)
    
    try:
        from pathlib import Path
        
        # Simular __file__ en el SDK
        sdk_file = sdk_path / "luminoracore_sdk" / "conversation_memory_manager.py"
        
        if not sdk_file.exists():
            print(f"  [WARN] Archivo SDK no encontrado: {sdk_file}")
            return False
        
        print(f"  Archivo SDK: {sdk_file}")
        calculated_parent = sdk_file.parent  # luminoracore_sdk directory
        calculated_personalities = calculated_parent / "personalities"
        
        print(f"  __file__.parent: {calculated_parent}")
        print(f"  personalities_dir: {calculated_personalities}")
        
        if calculated_personalities.exists():
            json_files = list(calculated_personalities.glob("*.json"))
            print(f"  [OK] Directorio existe con {len(json_files)} archivos JSON")
            return True
        else:
            print(f"  [FAIL] Directorio no existe")
            return False
        
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_lambda_layer_simulation():
    """Test 5: Simular estructura de Lambda Layer"""
    print("\n" + "="*70)
    print("TEST 5: Simulación Lambda Layer")
    print("="*70)
    
    try:
        from pathlib import Path
        
        # Simular estructura Lambda
        lambda_core_file = Path("/opt/python/luminoracore/core/personality.py")
        lambda_sdk_file = Path("/opt/python/luminoracore_sdk/conversation_memory_manager.py")
        
        print("\n  [1] Estructura CORE en Lambda:")
        print(f"    __file__: {lambda_core_file}")
        core_parent = lambda_core_file.parent.parent  # /opt/python/luminoracore
        core_personalities = core_parent / "personalities"
        print(f"    __file__.parent.parent: {core_parent}")
        print(f"    personalities_dir: {core_personalities}")
        
        # Verificar que el path es correcto (aunque no exista en nuestra máquina)
        expected_core = "/opt/python/luminoracore/personalities"
        actual_core = str(core_personalities)
        if actual_core == expected_core or actual_core.replace("\\", "/") == expected_core:
            print(f"    [OK] Path CORE correcto")
            core_ok = True
        else:
            print(f"    [FAIL] Path CORE incorrecto. Esperado: {expected_core}, Obtenido: {actual_core}")
            core_ok = False
        
        print("\n  [2] Estructura SDK en Lambda:")
        print(f"    __file__: {lambda_sdk_file}")
        sdk_parent = lambda_sdk_file.parent  # /opt/python/luminoracore_sdk
        sdk_personalities = sdk_parent / "personalities"
        print(f"    __file__.parent: {sdk_parent}")
        print(f"    personalities_dir: {sdk_personalities}")
        
        # Verificar que el path es correcto
        expected_sdk = "/opt/python/luminoracore_sdk/personalities"
        actual_sdk = str(sdk_personalities)
        if actual_sdk == expected_sdk or actual_sdk.replace("\\", "/") == expected_sdk:
            print(f"    [OK] Path SDK correcto")
            sdk_ok = True
        else:
            print(f"    [FAIL] Path SDK incorrecto. Esperado: {expected_sdk}, Obtenido: {actual_sdk}")
            sdk_ok = False
        
        return core_ok and sdk_ok
        
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration_complete():
    """Test 6: Integración completa - SDK usando core y propio directorio"""
    print("\n" + "="*70)
    print("TEST 6: Integración Completa")
    print("="*70)
    
    try:
        from luminoracore_sdk.conversation_memory_manager import ConversationMemoryManager
        
        # Mock client
        class MockClient:
            pass
        
        manager = ConversationMemoryManager(MockClient())
        
        import asyncio
        async def test():
            # Probar que el SDK puede cargar personalidades
            personality_name = "Grandma Hope"
            print(f"\n  Probando carga de: '{personality_name}'")
            
            data = await manager._load_personality_data(personality_name)
            
            if data:
                print(f"  [OK] Datos cargados exitosamente")
                
                # Verificar estructura
                checks = [
                    ("persona" in data, "Tiene persona"),
                    ("core_traits" in data, "Tiene core_traits"),
                    ("linguistic_profile" in data, "Tiene linguistic_profile"),
                    ("behavioral_rules" in data, "Tiene behavioral_rules"),
                ]
                
                print(f"\n  Estructura del JSON:")
                all_ok = True
                for passed, description in checks:
                    status = "[OK]" if passed else "[FAIL]"
                    print(f"    {status}: {description}")
                    if not passed:
                        all_ok = False
                
                # Verificar que se puede construir el prompt
                if all_ok:
                    prompt = manager._build_personality_prompt(data, personality_name)
                    if prompt and len(prompt) > 50:
                        print(f"\n  [OK] Prompt construido ({len(prompt)} caracteres)")
                        print(f"  Muestra: {prompt[:100]}...")
                        return True
                    else:
                        print(f"\n  [FAIL] Prompt no se construyó correctamente")
                        return False
                else:
                    return False
            else:
                print(f"  [FAIL] No se pudieron cargar los datos")
                return False
        
        result = asyncio.run(test())
        return result
        
    except Exception as e:
        print(f"\n  [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Ejecutar todos los tests"""
    print("\n" + "="*70)
    print("VALIDACION COMPLETA: Personalidades CORE y SDK")
    print("="*70)
    
    results = []
    
    results.append(("CORE - find_personality_file", test_core_find_personality()))
    results.append(("SDK - _load_personality_data", test_sdk_load_personality()))
    results.append(("Path Calculation CORE", test_path_calculation_core()))
    results.append(("Path Calculation SDK", test_path_calculation_sdk()))
    results.append(("Simulación Lambda Layer", test_lambda_layer_simulation()))
    results.append(("Integración Completa", test_integration_complete()))
    
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
        print("Todo está funcionando correctamente")
    else:
        print("[FAIL] ALGUNOS TESTS FALLARON")
        print("Revisar los errores arriba")
    print("="*70)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

