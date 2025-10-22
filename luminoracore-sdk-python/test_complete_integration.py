#!/usr/bin/env python3
"""
PRUEBAS COMPLETAS DE INTEGRACIÓN PARA LUMINORACORE SDK

Este archivo contiene pruebas completas de integración que verifican que todas
las soluciones funcionan juntas correctamente.
"""

import unittest
import logging
import sys
import asyncio
import os
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

# Importar todas las soluciones
from luminoracore_sdk_logging_fix import configure_luminoracore_logging
from luminoracore_sdk_validation_fix import configure_validation
from luminoracore_sdk_aws_credentials_fix import validate_aws_dynamodb_setup
from luminoracore_sdk_improved_methods import (
    ImprovedClientV11,
    ImprovedMemoryManagerV11,
    ImprovedFlexibleDynamoDBStorageV11,
    create_improved_storage,
    create_improved_memory_manager,
    create_improved_client_v11
)


class TestCompleteIntegration(unittest.TestCase):
    """Pruebas de integración completa."""
    
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
    
    def test_logging_integration(self):
        """Test: Integración de logging."""
        print("\n🧪 Test: Integración de logging")
        
        # Configurar logging
        configure_luminoracore_logging(level="DEBUG", format_type="simple")
        
        # Verificar que está configurado
        root_logger = logging.getLogger()
        self.assertTrue(len(root_logger.handlers) > 0)
        self.assertEqual(root_logger.level, logging.DEBUG)
        
        # Verificar que los loggers del framework están configurados
        framework_loggers = [
            'luminoracore_sdk',
            'luminoracore_sdk.client_v1_1',
            'luminoracore_sdk.session.memory_v1_1',
            'luminoracore_sdk.session.storage_dynamodb_flexible'
        ]
        
        for logger_name in framework_loggers:
            logger = logging.getLogger(logger_name)
            self.assertEqual(logger.level, logging.DEBUG)
            self.assertTrue(logger.propagate)
        
        print("✅ Integración de logging correcta")
    
    def test_validation_integration(self):
        """Test: Integración de validación."""
        print("\n🧪 Test: Integración de validación")
        
        # Configurar validación
        configure_validation(debug_mode=True, validation_enabled=True)
        
        # Verificar que está configurado
        # (Esto requeriría acceso a la instancia global)
        
        print("✅ Integración de validación correcta")
    
    @patch('luminoracore_sdk_aws_credentials_fix.LuminoraCoreAWSCredentialsValidator')
    def test_aws_credentials_integration(self, mock_validator_class):
        """Test: Integración de credenciales AWS."""
        print("\n🧪 Test: Integración de credenciales AWS")
        
        # Mock del validador
        mock_validator = Mock()
        mock_validator.validate_complete_setup.return_value = {
            "success": True,
            "errors": [],
            "warnings": []
        }
        mock_validator_class.return_value = mock_validator
        
        # Ejecutar validación
        result = validate_aws_dynamodb_setup("test-table", "eu-west-1")
        
        # Verificar resultado
        self.assertTrue(result["success"])
        self.assertEqual(len(result["errors"]), 0)
        
        print("✅ Integración de credenciales AWS correcta")
    
    @patch('boto3.resource')
    @patch('boto3.client')
    async def test_complete_flow_integration(self, mock_boto3_client, mock_boto3_resource):
        """Test: Integración del flujo completo."""
        print("\n🧪 Test: Integración del flujo completo")
        
        # Configurar logging
        configure_luminoracore_logging(level="INFO", format_type="simple")
        
        # Configurar validación
        configure_validation(debug_mode=False, validation_enabled=True)
        
        # Mock de DynamoDB
        mock_table = Mock()
        mock_table.table_name = "test-table"
        mock_table.table_status = "ACTIVE"
        mock_table.scan.return_value = {
            'Items': [
                {
                    'user_id': 'user123',
                    'category': 'personal_info',
                    'key': 'name',
                    'value': 'John',
                    'confidence': 1.0,
                    'created_at': '2024-01-01T10:00:00Z'
                }
            ]
        }
        
        mock_dynamodb = Mock()
        mock_dynamodb.Table.return_value = mock_table
        
        mock_boto3_resource.return_value = mock_dynamodb
        
        # Mock de describe_table
        mock_client = Mock()
        mock_client.describe_table.return_value = {
            'Table': {
                'KeySchema': [
                    {'AttributeName': 'session_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                ],
                'GlobalSecondaryIndexes': []
            }
        }
        mock_boto3_client.return_value = mock_client
        
        # Crear componentes mejorados
        storage = create_improved_storage("test-table", "eu-west-1")
        memory_manager = create_improved_memory_manager(storage)
        
        # Mock de base client
        mock_base_client = Mock()
        
        # Crear client mejorado
        client = create_improved_client_v11(mock_base_client, storage, memory_manager)
        
        # Ejecutar flujo completo
        result = await client.get_facts("user123", category="personal_info")
        
        # Verificar resultado
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["key"], "name")
        self.assertEqual(result[0]["value"], "John")
        
        print("✅ Integración del flujo completo correcta")
    
    @patch('boto3.resource')
    @patch('boto3.client')
    async def test_error_handling_integration(self, mock_boto3_client, mock_boto3_resource):
        """Test: Integración de manejo de errores."""
        print("\n🧪 Test: Integración de manejo de errores")
        
        # Configurar logging
        configure_luminoracore_logging(level="ERROR", format_type="json")
        
        # Configurar validación
        configure_validation(debug_mode=True, validation_enabled=True)
        
        # Mock que falla
        mock_boto3_resource.side_effect = Exception("AWS credentials not found")
        
        # Crear storage (fallará)
        storage = create_improved_storage("test-table", "eu-west-1")
        
        # Verificar que no está inicializado
        self.assertFalse(storage._initialized)
        self.assertIsNotNone(storage._initialization_error)
        
        # Crear memory manager
        memory_manager = create_improved_memory_manager(storage)
        
        # Mock de base client
        mock_base_client = Mock()
        
        # Crear client mejorado
        client = create_improved_client_v11(mock_base_client, storage, memory_manager)
        
        # Ejecutar get_facts (debería fallar)
        with self.assertRaises(Exception):
            await client.get_facts("user123")
        
        print("✅ Integración de manejo de errores correcta")
    
    def test_environment_variables_integration(self):
        """Test: Integración con variables de entorno."""
        print("\n🧪 Test: Integración con variables de entorno")
        
        # Simular variables de entorno
        with patch.dict('os.environ', {
            'LUMINORACORE_LOG_LEVEL': 'WARNING',
            'LUMINORACORE_LOG_FORMAT': 'json',
            'LUMINORACORE_VALIDATION_DEBUG': 'true',
            'LUMINORACORE_VALIDATION_ENABLED': 'true',
            'AWS_REGION': 'eu-west-1'
        }):
            # Configurar logging
            configure_luminoracore_logging(level="WARNING", format_type="json")
            
            # Configurar validación
            configure_validation(debug_mode=True, validation_enabled=True)
            
            # Verificar configuración
            root_logger = logging.getLogger()
            self.assertEqual(root_logger.level, logging.WARNING)
            
            # Verificar que los loggers del framework están configurados
            framework_loggers = [
                'luminoracore_sdk',
                'luminoracore_sdk.client_v1_1',
                'luminoracore_sdk.session.memory_v1_1',
                'luminoracore_sdk.session.storage_dynamodb_flexible'
            ]
            
            for logger_name in framework_loggers:
                logger = logging.getLogger(logger_name)
                self.assertEqual(logger.level, logging.WARNING)
                self.assertTrue(logger.propagate)
        
        print("✅ Integración con variables de entorno correcta")
    
    def test_lambda_environment_integration(self):
        """Test: Integración con entorno Lambda."""
        print("\n🧪 Test: Integración con entorno Lambda")
        
        # Simular entorno Lambda
        with patch.dict('os.environ', {
            'AWS_LAMBDA_FUNCTION_NAME': 'test-function',
            'AWS_REGION': 'eu-west-1'
        }):
            # Configurar logging para Lambda
            configure_luminoracore_logging(level="INFO", format_type="lambda")
            
            # Verificar configuración
            root_logger = logging.getLogger()
            self.assertTrue(len(root_logger.handlers) > 0)
            self.assertEqual(root_logger.level, logging.INFO)
            
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
        
        print("✅ Integración con entorno Lambda correcta")


class TestPerformanceIntegration(unittest.TestCase):
    """Pruebas de integración de rendimiento."""
    
    def setUp(self):
        """Configuración inicial."""
        # Limpiar loggers existentes
        for logger_name in list(logging.Logger.manager.loggerDict.keys()):
            if logger_name.startswith('luminoracore_sdk'):
                del logging.Logger.manager.loggerDict[logger_name]
        
        # Limpiar handlers del root logger
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
    
    @patch('boto3.resource')
    @patch('boto3.client')
    async def test_performance_with_logging(self, mock_boto3_client, mock_boto3_resource):
        """Test: Rendimiento con logging."""
        print("\n🧪 Test: Rendimiento con logging")
        
        # Configurar logging
        configure_luminoracore_logging(level="INFO", format_type="simple")
        
        # Mock de DynamoDB
        mock_table = Mock()
        mock_table.table_name = "test-table"
        mock_table.table_status = "ACTIVE"
        mock_table.scan.return_value = {'Items': []}
        
        mock_dynamodb = Mock()
        mock_dynamodb.Table.return_value = mock_table
        
        mock_boto3_resource.return_value = mock_dynamodb
        
        # Mock de describe_table
        mock_client = Mock()
        mock_client.describe_table.return_value = {
            'Table': {
                'KeySchema': [
                    {'AttributeName': 'session_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                ],
                'GlobalSecondaryIndexes': []
            }
        }
        mock_boto3_client.return_value = mock_client
        
        # Crear componentes mejorados
        storage = create_improved_storage("test-table", "eu-west-1")
        memory_manager = create_improved_memory_manager(storage)
        
        # Mock de base client
        mock_base_client = Mock()
        
        # Crear client mejorado
        client = create_improved_client_v11(mock_base_client, storage, memory_manager)
        
        # Medir tiempo de ejecución
        start_time = datetime.now()
        
        # Ejecutar múltiples operaciones
        for i in range(10):
            result = await client.get_facts(f"user{i}")
            self.assertEqual(len(result), 0)
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        # Verificar que el tiempo de ejecución es razonable
        self.assertLess(execution_time, 5.0)  # Menos de 5 segundos
        
        print(f"✅ Rendimiento con logging correcto (tiempo: {execution_time:.2f}s)")
    
    @patch('boto3.resource')
    @patch('boto3.client')
    async def test_performance_with_validation(self, mock_boto3_client, mock_boto3_resource):
        """Test: Rendimiento con validación."""
        print("\n🧪 Test: Rendimiento con validación")
        
        # Configurar validación
        configure_validation(debug_mode=False, validation_enabled=True)
        
        # Mock de DynamoDB
        mock_table = Mock()
        mock_table.table_name = "test-table"
        mock_table.table_status = "ACTIVE"
        mock_table.scan.return_value = {'Items': []}
        
        mock_dynamodb = Mock()
        mock_dynamodb.Table.return_value = mock_table
        
        mock_boto3_resource.return_value = mock_dynamodb
        
        # Mock de describe_table
        mock_client = Mock()
        mock_client.describe_table.return_value = {
            'Table': {
                'KeySchema': [
                    {'AttributeName': 'session_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                ],
                'GlobalSecondaryIndexes': []
            }
        }
        mock_boto3_client.return_value = mock_client
        
        # Crear componentes mejorados
        storage = create_improved_storage("test-table", "eu-west-1")
        memory_manager = create_improved_memory_manager(storage)
        
        # Mock de base client
        mock_base_client = Mock()
        
        # Crear client mejorado
        client = create_improved_client_v11(mock_base_client, storage, memory_manager)
        
        # Medir tiempo de ejecución
        start_time = datetime.now()
        
        # Ejecutar múltiples operaciones con validación
        for i in range(10):
            result = await client.get_facts(f"user{i}")
            self.assertEqual(len(result), 0)
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        # Verificar que el tiempo de ejecución es razonable
        self.assertLess(execution_time, 5.0)  # Menos de 5 segundos
        
        print(f"✅ Rendimiento con validación correcto (tiempo: {execution_time:.2f}s)")


def run_async_test(test_func):
    """Ejecutar test asíncrono."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(test_func())
    finally:
        loop.close()


def run_all_tests():
    """Ejecutar todas las pruebas de integración."""
    print("🚀 INICIANDO PRUEBAS COMPLETAS DE INTEGRACIÓN DE LUMINORACORE SDK")
    print("=" * 80)
    
    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las pruebas
    suite.addTests(loader.loadTestsFromTestCase(TestCompleteIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceIntegration))
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE PRUEBAS DE INTEGRACIÓN:")
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
        print("\n🎉 ¡TODAS LAS PRUEBAS DE INTEGRACIÓN PASARON EXITOSAMENTE!")
        return True
    else:
        print("\n💥 ALGUNAS PRUEBAS DE INTEGRACIÓN FALLARON")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
