#!/usr/bin/env python3
"""
PRUEBAS COMPLETAS PARA LUMINORACORE SDK LOGGING FIX

Este archivo contiene pruebas completas para verificar que el sistema de logging
funciona correctamente y resuelve el problema de visibilidad de logs en AWS Lambda.
"""

import unittest
import logging
import sys
import io
from unittest.mock import patch, MagicMock
from contextlib import redirect_stderr, redirect_stdout

# Importar el sistema de logging fix
from luminoracore_sdk_logging_fix import (
    LuminoraCoreLoggingConfig,
    configure_luminoracore_logging,
    auto_configure_for_environment
)


class TestLuminoraCoreLoggingFix(unittest.TestCase):
    """Pruebas para el sistema de logging fix del SDK."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        # Limpiar loggers existentes
        for logger_name in list(logging.Logger.manager.loggerDict.keys()):
            if logger_name.startswith('luminoracore_sdk'):
                del logging.Logger.manager.loggerDict[logger_name]
        
        # Limpiar handlers del root logger
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
    
    def test_logging_config_initialization(self):
        """Test: Inicialización de configuración de logging."""
        print("\n🧪 Test: Inicialización de configuración de logging")
        
        config = LuminoraCoreLoggingConfig(level="DEBUG", format_type="lambda")
        
        self.assertEqual(config.level, "DEBUG")
        self.assertEqual(config.format_type, "lambda")
        self.assertFalse(config._configured)
        
        print("✅ Inicialización correcta")
    
    def test_logging_configuration(self):
        """Test: Configuración completa de logging."""
        print("\n🧪 Test: Configuración completa de logging")
        
        config = LuminoraCoreLoggingConfig(level="DEBUG", format_type="lambda")
        config.configure_logging()
        
        # Verificar que está configurado
        self.assertTrue(config._configured)
        
        # Verificar que el root logger tiene handlers
        root_logger = logging.getLogger()
        self.assertTrue(len(root_logger.handlers) > 0)
        
        # Verificar nivel de logging
        self.assertEqual(root_logger.level, logging.DEBUG)
        
        print("✅ Configuración de logging correcta")
    
    def test_framework_loggers_configured(self):
        """Test: Loggers del framework configurados correctamente."""
        print("\n🧪 Test: Loggers del framework configurados")
        
        config = LuminoraCoreLoggingConfig(level="INFO", format_type="simple")
        config.configure_logging()
        
        # Verificar que los loggers del framework están configurados
        framework_loggers = [
            'luminoracore_sdk',
            'luminoracore_sdk.client_v1_1',
            'luminoracore_sdk.session.memory_v1_1',
            'luminoracore_sdk.session.storage_dynamodb_flexible'
        ]
        
        for logger_name in framework_loggers:
            logger = logging.getLogger(logger_name)
            self.assertEqual(logger.level, logging.INFO)
            self.assertTrue(logger.propagate)
        
        print("✅ Loggers del framework configurados correctamente")
    
    def test_logging_output_capture(self):
        """Test: Captura de output de logging."""
        print("\n🧪 Test: Captura de output de logging")
        
        # Configurar logging
        config = LuminoraCoreLoggingConfig(level="DEBUG", format_type="simple")
        config.configure_logging()
        
        # Capturar output
        with io.StringIO() as captured_output:
            with redirect_stdout(captured_output):
                # Crear logger del framework
                logger = logging.getLogger('luminoracore_sdk.client_v1_1')
                logger.info("Test message from framework")
                logger.debug("Debug message from framework")
                logger.warning("Warning message from framework")
        
        output = captured_output.getvalue()
        
        # Verificar que los mensajes aparecen
        self.assertIn("Test message from framework", output)
        self.assertIn("Debug message from framework", output)
        self.assertIn("Warning message from framework", output)
        
        print("✅ Output de logging capturado correctamente")
    
    def test_json_formatting(self):
        """Test: Formato JSON de logging."""
        print("\n🧪 Test: Formato JSON de logging")
        
        config = LuminoraCoreLoggingConfig(level="INFO", format_type="json")
        config.configure_logging()
        
        # Capturar output
        with io.StringIO() as captured_output:
            with redirect_stdout(captured_output):
                logger = logging.getLogger('luminoracore_sdk.test')
                logger.info("Test JSON message")
        
        output = captured_output.getvalue()
        
        # Verificar que es formato JSON
        self.assertIn('"level": "INFO"', output)
        self.assertIn('"message": "Test JSON message"', output)
        self.assertIn('"logger": "luminoracore_sdk.test"', output)
        
        print("✅ Formato JSON correcto")
    
    def test_aws_lambda_compatibility(self):
        """Test: Compatibilidad con AWS Lambda."""
        print("\n🧪 Test: Compatibilidad con AWS Lambda")
        
        # Simular entorno Lambda
        with patch.dict('os.environ', {'AWS_LAMBDA_FUNCTION_NAME': 'test-function'}):
            config = LuminoraCoreLoggingConfig(level="INFO", format_type="lambda")
            config.configure_logging()
            
            # Verificar que está configurado
            self.assertTrue(config._configured)
            
            # Verificar que el formato es lambda
            self.assertEqual(config.format_type, "lambda")
        
        print("✅ Compatibilidad con AWS Lambda correcta")
    
    def test_convenience_function(self):
        """Test: Función de conveniencia."""
        print("\n🧪 Test: Función de conveniencia")
        
        # Usar función de conveniencia
        configure_luminoracore_logging(level="WARNING", format_type="simple")
        
        # Verificar que está configurado
        root_logger = logging.getLogger()
        self.assertEqual(root_logger.level, logging.WARNING)
        
        print("✅ Función de conveniencia funciona correctamente")
    
    def test_auto_configure_environment(self):
        """Test: Configuración automática basada en entorno."""
        print("\n🧪 Test: Configuración automática basada en entorno")
        
        # Simular variables de entorno
        with patch.dict('os.environ', {
            'LUMINORACORE_LOG_LEVEL': 'ERROR',
            'LUMINORACORE_LOG_FORMAT': 'json'
        }):
            auto_configure_for_environment()
            
            # Verificar configuración
            root_logger = logging.getLogger()
            self.assertEqual(root_logger.level, logging.ERROR)
        
        print("✅ Configuración automática funciona correctamente")
    
    def test_logging_test_function(self):
        """Test: Función de test de logging."""
        print("\n🧪 Test: Función de test de logging")
        
        config = LuminoraCoreLoggingConfig(level="DEBUG", format_type="simple")
        config.configure_logging()
        
        # Capturar output del test
        with io.StringIO() as captured_output:
            with redirect_stdout(captured_output):
                config.test_logging()
        
        output = captured_output.getvalue()
        
        # Verificar que todos los niveles aparecen
        self.assertIn("DEBUG: Test de logging", output)
        self.assertIn("INFO: Test de logging", output)
        self.assertIn("WARNING: Test de logging", output)
        self.assertIn("ERROR: Test de logging", output)
        self.assertIn("CRITICAL: Test de logging", output)
        
        print("✅ Función de test de logging funciona correctamente")
    
    def test_multiple_configurations(self):
        """Test: Múltiples configuraciones no causan problemas."""
        print("\n🧪 Test: Múltiples configuraciones")
        
        # Configurar múltiples veces
        config1 = LuminoraCoreLoggingConfig(level="INFO", format_type="simple")
        config1.configure_logging()
        
        config2 = LuminoraCoreLoggingConfig(level="DEBUG", format_type="json")
        config2.configure_logging()
        
        # Verificar que no hay handlers duplicados
        root_logger = logging.getLogger()
        self.assertEqual(len(root_logger.handlers), 1)  # Solo un handler
        
        print("✅ Múltiples configuraciones manejadas correctamente")
    
    def test_error_handling(self):
        """Test: Manejo de errores en configuración."""
        print("\n🧪 Test: Manejo de errores en configuración")
        
        # Test con nivel inválido
        with self.assertRaises(AttributeError):
            config = LuminoraCoreLoggingConfig(level="INVALID", format_type="simple")
            config.configure_logging()
        
        print("✅ Manejo de errores correcto")


class TestIntegrationWithFramework(unittest.TestCase):
    """Pruebas de integración con el framework."""
    
    def setUp(self):
        """Configuración inicial."""
        # Limpiar loggers
        for logger_name in list(logging.Logger.manager.loggerDict.keys()):
            if logger_name.startswith('luminoracore_sdk'):
                del logging.Logger.manager.loggerDict[logger_name]
        
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
    
    def test_framework_logging_visibility(self):
        """Test: Visibilidad de logs del framework."""
        print("\n🧪 Test: Visibilidad de logs del framework")
        
        # Configurar logging
        configure_luminoracore_logging(level="DEBUG", format_type="simple")
        
        # Simular logs del framework
        with io.StringIO() as captured_output:
            with redirect_stdout(captured_output):
                # Simular logs de diferentes partes del framework
                client_logger = logging.getLogger('luminoracore_sdk.client_v1_1')
                memory_logger = logging.getLogger('luminoracore_sdk.session.memory_v1_1')
                storage_logger = logging.getLogger('luminoracore_sdk.session.storage_dynamodb_flexible')
                
                client_logger.info("Client initialized")
                memory_logger.debug("Memory manager created")
                storage_logger.warning("Storage connection issue")
        
        output = captured_output.getvalue()
        
        # Verificar que todos los logs son visibles
        self.assertIn("Client initialized", output)
        self.assertIn("Memory manager created", output)
        self.assertIn("Storage connection issue", output)
        
        print("✅ Logs del framework son visibles")
    
    def test_lambda_environment_simulation(self):
        """Test: Simulación de entorno Lambda."""
        print("\n🧪 Test: Simulación de entorno Lambda")
        
        # Simular entorno Lambda
        with patch.dict('os.environ', {
            'AWS_LAMBDA_FUNCTION_NAME': 'test-function',
            'AWS_REGION': 'eu-west-1'
        }):
            # Configurar logging
            configure_luminoracore_logging(level="INFO", format_type="lambda")
            
            # Simular logs del framework
            with io.StringIO() as captured_output:
                with redirect_stdout(captured_output):
                    logger = logging.getLogger('luminoracore_sdk.client_v1_1')
                    logger.info("Lambda function started")
                    logger.error("Error in Lambda function")
            
            output = captured_output.getvalue()
            
            # Verificar que los logs aparecen
            self.assertIn("Lambda function started", output)
            self.assertIn("Error in Lambda function", output)
        
        print("✅ Entorno Lambda simulado correctamente")


def run_all_tests():
    """Ejecutar todas las pruebas."""
    print("🚀 INICIANDO PRUEBAS COMPLETAS DE LUMINORACORE SDK LOGGING FIX")
    print("=" * 80)
    
    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las pruebas
    suite.addTests(loader.loadTestsFromTestCase(TestLuminoraCoreLoggingFix))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationWithFramework))
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"✅ Tests ejecutados: {result.testsRun}")
    print(f"✅ Tests exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Tests fallidos: {len(result.failures)}")
    print(f"❌ Tests con errores: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ TESTS FALLIDOS:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n❌ TESTS CON ERRORES:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        return True
    else:
        print("\n💥 ALGUNAS PRUEBAS FALLARON")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
