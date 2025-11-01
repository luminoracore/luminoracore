#!/usr/bin/env python3
"""
Test para validar que las personalidades se cargan correctamente
"""

import sys
import json
from pathlib import Path

# Añadir SDK al path
sdk_path = Path("luminoracore-sdk-python")
if str(sdk_path) not in sys.path:
    sys.path.insert(0, str(sdk_path))

def test_load_personality_file():
    """Test 1: Verificar que se puede cargar un archivo JSON de personalidad"""
    print("\n" + "="*70)
    print("TEST 1: Carga de Archivo JSON de Personalidad")
    print("="*70)
    
    # Buscar archivo de personalidad
    personalities_dir = sdk_path / "luminoracore_sdk" / "personalities"
    
    print(f"\n  Buscando en: {personalities_dir}")
    
    if not personalities_dir.exists():
        print(f"  [FAIL] Directorio no existe: {personalities_dir}")
        return False
    
    # Listar archivos disponibles
    json_files = list(personalities_dir.glob("*.json"))
    print(f"  Archivos encontrados: {len(json_files)}")
    for f in json_files[:5]:  # Mostrar primeros 5
        print(f"    - {f.name}")
    
    # Intentar cargar grandma_hope.json
    grandma_file = personalities_dir / "grandma_hope.json"
    
    if not grandma_file.exists():
        print(f"\n  [FAIL] Archivo grandma_hope.json no encontrado")
        print(f"  Intentando con otro archivo...")
        if json_files:
            test_file = json_files[0]
            print(f"  Usando: {test_file.name}")
        else:
            return False
    else:
        test_file = grandma_file
    
    # Cargar y verificar JSON
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            personality_data = json.load(f)
        
        print(f"\n  [OK] Archivo cargado: {test_file.name}")
        
        # Verificar estructura
        has_persona = "persona" in personality_data
        has_core_traits = "core_traits" in personality_data
        has_linguistic = "linguistic_profile" in personality_data
        has_rules = "behavioral_rules" in personality_data
        
        print(f"  Estructura JSON:")
        print(f"    - persona: {has_persona}")
        print(f"    - core_traits: {has_core_traits}")
        print(f"    - linguistic_profile: {has_linguistic}")
        print(f"    - behavioral_rules: {has_rules}")
        
        if has_persona:
            persona = personality_data["persona"]
            print(f"\n  Persona encontrada:")
            print(f"    - name: {persona.get('name', 'N/A')}")
            print(f"    - description: {persona.get('description', 'N/A')[:60]}...")
        
        return has_persona or has_core_traits
        
    except Exception as e:
        print(f"\n  [FAIL] Error cargando JSON: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_personality_manager_methods():
    """Test 2: Verificar que los métodos del ConversationMemoryManager funcionan"""
    print("\n" + "="*70)
    print("TEST 2: Métodos de Carga de Personalidad")
    print("="*70)
    
    try:
        # Importar el manager
        from luminoracore_sdk.conversation_memory_manager import ConversationMemoryManager
        
        # Crear un mock client
        class MockClient:
            def __init__(self):
                self.base_client = None
        
        mock_client = MockClient()
        manager = ConversationMemoryManager(mock_client)
        
        print("\n  [OK] ConversationMemoryManager creado")
        
        # Verificar que los métodos existen
        has_load = hasattr(manager, '_load_personality_data')
        has_build = hasattr(manager, '_build_personality_prompt')
        
        print(f"  Métodos disponibles:")
        print(f"    - _load_personality_data: {has_load}")
        print(f"    - _build_personality_prompt: {has_build}")
        
        if not has_load or not has_build:
            print(f"\n  [FAIL] Métodos no encontrados")
            return False
        
        print(f"\n  [OK] Métodos encontrados")
        return True
        
    except Exception as e:
        print(f"\n  [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_load_personality_async():
    """Test 3: Probar carga asíncrona de personalidad"""
    print("\n" + "="*70)
    print("TEST 3: Carga Asíncrona de Personalidad")
    print("="*70)
    
    try:
        from luminoracore_sdk.conversation_memory_manager import ConversationMemoryManager
        
        # Crear un mock client con base_client que tiene personalities_dir
        class MockBaseClient:
            def __init__(self):
                sdk_dir = Path(__file__).parent.parent / "luminoracore-sdk-python" / "luminoracore_sdk"
                self.personalities_dir = str(sdk_dir / "personalities")
        
        class MockClient:
            def __init__(self):
                self.base_client = MockBaseClient()
        
        mock_client = MockClient()
        manager = ConversationMemoryManager(mock_client)
        
        # Probar con diferentes nombres
        test_names = ["Grandma Hope", "grandma_hope", "Dr. Luna", "dr_luna"]
        
        results = []
        for name in test_names:
            print(f"\n  Probando: '{name}'")
            try:
                personality_data = await manager._load_personality_data(name)
                if personality_data:
                    print(f"    [OK] Personalidad cargada")
                    print(f"    - Tiene persona: {'persona' in personality_data}")
                    print(f"    - Tiene core_traits: {'core_traits' in personality_data}")
                    print(f"    - Tiene linguistic_profile: {'linguistic_profile' in personality_data}")
                    results.append(True)
                else:
                    print(f"    [WARN] No se encontró archivo para: {name}")
                    results.append(False)
            except Exception as e:
                print(f"    [FAIL] Error: {e}")
                results.append(False)
        
        # Al menos una debería cargarse
        success_count = sum(results)
        print(f"\n  Resultado: {success_count}/{len(test_names)} personalidades cargadas")
        
        return success_count > 0
        
    except Exception as e:
        print(f"\n  [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_build_personality_prompt():
    """Test 4: Verificar construcción del prompt"""
    print("\n" + "="*70)
    print("TEST 4: Construcción del Prompt de Personalidad")
    print("="*70)
    
    try:
        from luminoracore_sdk.conversation_memory_manager import ConversationMemoryManager
        
        # Mock client
        class MockClient:
            pass
        
        manager = ConversationMemoryManager(MockClient())
        
        # Datos de prueba (similar a grandma_hope.json)
        test_personality_data = {
            "persona": {
                "name": "Grandma Hope",
                "description": "A warm and nurturing grandmother figure"
            },
            "core_traits": {
                "archetype": "caregiver",
                "temperament": "calm",
                "communication_style": "conversational"
            },
            "linguistic_profile": {
                "tone": ["warm", "friendly", "wise"],
                "vocabulary": ["dear", "sweetheart", "honey"],
                "fillers": ["oh my goodness", "bless your heart"],
                "syntax": "simple"
            },
            "behavioral_rules": [
                "Always speak with warmth",
                "Share wisdom through traditional sayings"
            ],
            "advanced_parameters": {
                "verbosity": 0.7,
                "formality": 0.3,
                "empathy": 0.9
            }
        }
        
        # Construir prompt
        prompt = manager._build_personality_prompt(test_personality_data, "Grandma Hope")
        
        print(f"\n  Prompt construido ({len(prompt)} caracteres):")
        print(f"  {prompt[:200]}...")
        
        # Verificar que contiene elementos esperados
        checks = [
            ("Grandma Hope" in prompt, "Nombre de personalidad"),
            ("warm" in prompt.lower() or "nurturing" in prompt.lower(), "Descripción"),
            ("caregiver" in prompt.lower(), "Archetype"),
            ("calm" in prompt.lower(), "Temperament"),
            ("dear" in prompt.lower() or "sweetheart" in prompt.lower(), "Vocabulario"),
            ("oh my goodness" in prompt.lower() or "bless your heart" in prompt.lower(), "Fillers"),
            ("Always speak" in prompt or "warmth" in prompt.lower(), "Behavioral rules"),
            ("0.7" in prompt or "0.3" in prompt, "Advanced parameters")
        ]
        
        print(f"\n  Verificaciones:")
        all_passed = True
        for passed, description in checks:
            status = "[OK]" if passed else "[FAIL]"
            print(f"    {status}: {description}")
            if not passed:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"\n  [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_full_integration():
    """Test 5: Integración completa - carga y construcción"""
    print("\n" + "="*70)
    print("TEST 5: Integración Completa")
    print("="*70)
    
    try:
        from luminoracore_sdk.conversation_memory_manager import ConversationMemoryManager
        
        # Mock client con base_client
        class MockBaseClient:
            def __init__(self):
                sdk_dir = Path(__file__).parent.parent / "luminoracore-sdk-python" / "luminoracore_sdk"
                self.personalities_dir = str(sdk_dir / "personalities")
        
        class MockClient:
            def __init__(self):
                self.base_client = MockBaseClient()
        
        mock_client = MockClient()
        manager = ConversationMemoryManager(mock_client)
        
        # Probar carga y construcción completa
        personality_name = "Grandma Hope"
        
        print(f"\n  Probando con: '{personality_name}'")
        
        # 1. Cargar datos
        personality_data = await manager._load_personality_data(personality_name)
        
        if not personality_data:
            print(f"  [WARN] No se pudo cargar personalidad, probando otros nombres...")
            # Intentar variaciones
            for variant in ["grandma_hope", "grandmahope"]:
                personality_data = await manager._load_personality_data(variant)
                if personality_data:
                    personality_name = variant
                    break
        
        if not personality_data:
            print(f"  [FAIL] No se pudo cargar ninguna personalidad")
            return False
        
        print(f"  [OK] Datos cargados")
        
        # 2. Construir prompt
        prompt = manager._build_personality_prompt(personality_data, personality_name)
        
        print(f"  [OK] Prompt construido ({len(prompt)} caracteres)")
        
        # 3. Verificar contenido
        required_elements = [
            personality_name.lower().replace(" ", "") in prompt.lower() or personality_name.lower() in prompt.lower(),
            len(prompt) > 50,  # Debe ser sustancial
            "\n" in prompt,  # Debe tener estructura
        ]
        
        all_passed = all(required_elements)
        
        print(f"\n  Verificaciones:")
        print(f"    [{'OK' if required_elements[0] else 'FAIL'}]: Nombre presente")
        print(f"    [{'OK' if required_elements[1] else 'FAIL'}]: Prompt sustancial")
        print(f"    [{'OK' if required_elements[2] else 'FAIL'}]: Estructura presente")
        
        # Mostrar una muestra del prompt
        print(f"\n  Muestra del prompt generado:")
        lines = prompt.split('\n')[:10]
        for line in lines:
            if line.strip():
                print(f"    {line[:70]}")
        
        return all_passed
        
    except Exception as e:
        print(f"\n  [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Ejecutar todos los tests"""
    print("\n" + "="*70)
    print("VALIDACION: Carga de Personalidades")
    print("="*70)
    
    import asyncio
    
    results = []
    
    # Test síncronos
    results.append(("Carga de archivo JSON", test_load_personality_file()))
    results.append(("Métodos del manager", test_personality_manager_methods()))
    results.append(("Construcción del prompt", test_build_personality_prompt()))
    
    # Test asíncronos
    results.append(("Carga asíncrona", asyncio.run(test_load_personality_async())))
    results.append(("Integración completa", asyncio.run(test_full_integration())))
    
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
        print("El fix de personalidades funciona correctamente")
    else:
        print("[FAIL] ALGUNOS TESTS FALLARON")
        print("Revisar los errores arriba")
    print("="*70)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

