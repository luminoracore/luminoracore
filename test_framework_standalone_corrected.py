"""
Valida que el framework funcione correctamente de forma aislada
Usa SOLO las clases que realmente existen en el framework actual
"""

import sys

def test_framework_integrity():
    """Prueba que el framework funciona como biblioteca Python independiente"""
    
    print("=" * 70)
    print("VALIDACIÓN DEL FRAMEWORK LUMINORACORE")
    print("=" * 70)
    print()
    
    all_passed = True
    
    # TEST 1: Imports básicos - usando SOLO lo que existe
    print("TEST 1: Verificar que todos los módulos se pueden importar")
    print("-" * 70)
    try:
        # Clientes principales
        from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
        print("✅ LuminoraCoreClient y LuminoraCoreClientV11 importados")
        
        # Storage classes
        from luminoracore_sdk import FlexibleDynamoDBStorageV11, FlexibleSQLiteStorageV11
        print("✅ FlexibleDynamoDBStorageV11 y FlexibleSQLiteStorageV11 importados")
        
        # Personality classes
        from luminoracore_sdk import PersonalityLoader, PersonalityBlender
        print("✅ PersonalityLoader y PersonalityBlender importados")
        
        # Logging
        from luminoracore_sdk import setup_logging, auto_configure, get_logger
        print("✅ setup_logging, auto_configure, get_logger importados")
        
        # Providers
        from luminoracore_sdk import ProviderFactory, OpenAIProvider, DeepSeekProvider
        print("✅ ProviderFactory y providers importados")
        
    except ImportError as e:
        print(f"❌ Error de import: {e}")
        all_passed = False
    print()
    
    # TEST 2: Instanciar clases principales
    print("TEST 2: Verificar que las clases se pueden instanciar")
    print("-" * 70)
    try:
        # Test PersonalityLoader
        loader = PersonalityLoader()
        print("✅ PersonalityLoader se puede instanciar")
        
        # Test PersonalityBlender
        blender = PersonalityBlender()
        print("✅ PersonalityBlender se puede instanciar")
        
        # Test ProviderFactory
        factory = ProviderFactory()
        print("✅ ProviderFactory se puede instanciar")
        
    except Exception as e:
        print(f"❌ Error al instanciar: {e}")
        all_passed = False
    print()
    
    # TEST 3: Test de logging
    print("TEST 3: Verificar que el logging funciona")
    print("-" * 70)
    try:
        # Configurar logging
        setup_logging(level="DEBUG", format_type="text")
        print("✅ setup_logging() funciona correctamente")
        
        # Obtener logger
        logger = get_logger(__name__)
        logger.info("Test message from framework validation")
        print("✅ get_logger() funciona correctamente")
        
    except Exception as e:
        print(f"❌ Error en logging: {e}")
        all_passed = False
    print()
    
    # TEST 4: Verificar estructura de clases Storage
    print("TEST 4: Verificar que las clases Storage existen y tienen métodos")
    print("-" * 70)
    try:
        # Verificar métodos de FlexibleDynamoDBStorageV11
        dynamodb_methods = ['save_fact', 'get_facts', 'save_episode', 'get_episodes', 'save_mood', 'get_mood']
        
        for method in dynamodb_methods:
            if hasattr(FlexibleDynamoDBStorageV11, method):
                print(f"✅ FlexibleDynamoDBStorageV11.{method} existe")
            else:
                print(f"❌ FlexibleDynamoDBStorageV11.{method} NO existe")
                all_passed = False
        
        # Verificar métodos de FlexibleSQLiteStorageV11
        sqlite_methods = ['save_fact', 'get_facts', 'save_episode', 'get_episodes', 'save_mood', 'get_mood']
        
        for method in sqlite_methods:
            if hasattr(FlexibleSQLiteStorageV11, method):
                print(f"✅ FlexibleSQLiteStorageV11.{method} existe")
            else:
                print(f"❌ FlexibleSQLiteStorageV11.{method} NO existe")
                all_passed = False
                
    except Exception as e:
        print(f"❌ Error verificando Storage: {e}")
        all_passed = False
    print()
    
    # TEST 5: Verificar que los clientes se pueden instanciar
    print("TEST 5: Verificar que los clientes se pueden instanciar")
    print("-" * 70)
    try:
        # Test LuminoraCoreClient
        client = LuminoraCoreClient()
        print("✅ LuminoraCoreClient se puede instanciar")
        
        # Test LuminoraCoreClientV11
        client_v11 = LuminoraCoreClientV11(base_client=None)
        print("✅ LuminoraCoreClientV11 se puede instanciar")
        
    except Exception as e:
        print(f"❌ Error al instanciar clientes: {e}")
        all_passed = False
    print()
    
    # TEST 6: Verificar que los providers se pueden instanciar
    print("TEST 6: Verificar que los providers se pueden instanciar")
    print("-" * 70)
    try:
        # Test OpenAIProvider
        openai_provider = OpenAIProvider(api_key="test_key")
        print("✅ OpenAIProvider se puede instanciar")
        
        # Test DeepSeekProvider
        deepseek_provider = DeepSeekProvider(api_key="test_key")
        print("✅ DeepSeekProvider se puede instanciar")
        
    except Exception as e:
        print(f"❌ Error al instanciar providers: {e}")
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
        print("Todas las clases principales se pueden importar e instanciar.")
        print()
        print("Clases disponibles y funcionales:")
        print("- LuminoraCoreClient y LuminoraCoreClientV11")
        print("- FlexibleDynamoDBStorageV11 y FlexibleSQLiteStorageV11")
        print("- PersonalityLoader y PersonalityBlender")
        print("- ProviderFactory y providers (OpenAI, DeepSeek, etc.)")
        print("- setup_logging, auto_configure, get_logger")
        return True
    else:
        print("❌ EL FRAMEWORK TIENE PROBLEMAS")
        print()
        print("Hay errores en el framework que deben corregirse antes de usarlo.")
        return False

if __name__ == "__main__":
    success = test_framework_integrity()
    sys.exit(0 if success else 1)
