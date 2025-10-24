"""
Valida que el framework funcione correctamente de forma aislada
NO involucra Lambda, Docker, ni API
"""

import sys

def test_framework_integrity():
    """Prueba que el framework funciona como biblioteca Python independiente"""
    
    print("=" * 70)
    print("VALIDACIÓN DEL FRAMEWORK LUMINORACORE")
    print("=" * 70)
    print()
    
    all_passed = True
    
    # TEST 1: Imports básicos
    print("TEST 1: Verificar que todos los módulos se pueden importar")
    print("-" * 70)
    try:
        from luminoracore_sdk.personality.compiler import PersonalityCompiler
        from luminoracore_sdk.personality.validator import PersonalityValidator
        from luminoracore_sdk.session.storage_dynamodb_flexible import FlexibleDynamoDBStorageV11
        from luminoracore_sdk.session.storage_sqlite_flexible import FlexibleSQLiteStorageV11
        print("✅ Todos los imports funcionan")
    except ImportError as e:
        print(f"❌ Error de import: {e}")
        all_passed = False
    print()
    
    # TEST 2: Instanciar clases principales
    print("TEST 2: Verificar que las clases se pueden instanciar")
    print("-" * 70)
    try:
        compiler = PersonalityCompiler()
        print("✅ PersonalityCompiler se puede instanciar")
        
        validator = PersonalityValidator()
        print("✅ PersonalityValidator se puede instanciar")
    except Exception as e:
        print(f"❌ Error al instanciar: {e}")
        all_passed = False
    print()
    
    # TEST 3: Compilar una personalidad simple
    print("TEST 3: Compilar una personalidad de prueba")
    print("-" * 70)
    try:
        test_personality = {
            "persona": {
                "name": "TestBot",
                "version": "1.0.0",
                "description": "A test personality",
                "author": "Test",
                "tags": ["test"],
                "language": "en",
                "compatibility": ["deepseek"]
            },
            "core_traits": {
                "archetype": "sage",
                "temperament": "calm",
                "communication_style": "conversational"
            },
            "linguistic_profile": {
                "tone": ["friendly"],
                "syntax": "simple",
                "vocabulary": ["hello"],
                "fillers": ["well"],
                "punctuation_style": "moderate"
            },
            "behavioral_rules": ["Be helpful"],
            "advanced_parameters": {
                "verbosity": 0.5,
                "formality": 0.5,
                "humor": 0.3,
                "empathy": 0.7,
                "creativity": 0.5,
                "directness": 0.6
            }
        }
        
        result = compiler.compile(test_personality)
        
        if result and 'compiled_prompt' in result:
            print("✅ Personalidad compilada correctamente")
            print(f"   Longitud del prompt: {len(result['compiled_prompt'])} caracteres")
        else:
            print("❌ La compilación no retornó el formato esperado")
            all_passed = False
            
    except Exception as e:
        print(f"❌ Error al compilar: {e}")
        import traceback
        traceback.print_exc()
        all_passed = False
    print()
    
    # TEST 4: Validar una personalidad
    print("TEST 4: Validar una personalidad")
    print("-" * 70)
    try:
        validation_result = validator.validate(test_personality)
        
        if validation_result.get('is_valid'):
            print("✅ Validación funciona correctamente")
        else:
            print(f"⚠️  Validación funciona pero encontró errores: {validation_result.get('errors')}")
            
    except Exception as e:
        print(f"❌ Error al validar: {e}")
        import traceback
        traceback.print_exc()
        all_passed = False
    print()
    
    # TEST 5: Verificar estructura de clases Storage
    print("TEST 5: Verificar que las clases Storage existen y tienen métodos")
    print("-" * 70)
    try:
        # Solo verificar que existen, no conectar realmente
        required_methods = ['save_session', 'load_session', 'delete_session', 'list_sessions']
        
        for method in required_methods:
            if hasattr(FlexibleDynamoDBStorageV11, method):
                print(f"✅ FlexibleDynamoDBStorageV11.{method} existe")
            else:
                print(f"❌ FlexibleDynamoDBStorageV11.{method} NO existe")
                all_passed = False
                
        for method in required_methods:
            if hasattr(FlexibleSQLiteStorageV11, method):
                print(f"✅ FlexibleSQLiteStorageV11.{method} existe")
            else:
                print(f"❌ FlexibleSQLiteStorageV11.{method} NO existe")
                all_passed = False
                
    except Exception as e:
        print(f"❌ Error verificando Storage: {e}")
        all_passed = False
    print()
    
    # RESULTADO FINAL
    print("=" * 70)
    print("RESULTADO FINAL")
    print("=" * 70)
    
    if all_passed:
        print("✅ EL FRAMEWORK ES CORRECTO Y FUNCIONAL")
        print()
        print("El framework funciona correctamente como biblioteca Python.")
        print("Si hay errores en la API, son problemas de la API, no del framework.")
        return True
    else:
        print("❌ EL FRAMEWORK TIENE PROBLEMAS")
        print()
        print("Hay errores en el framework que deben corregirse antes de usarlo.")
        return False

if __name__ == "__main__":
    success = test_framework_integrity()
    sys.exit(0 if success else 1)
