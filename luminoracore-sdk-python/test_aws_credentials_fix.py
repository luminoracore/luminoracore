#!/usr/bin/env python3
"""
PRUEBAS COMPLETAS PARA LUMINORACORE SDK AWS CREDENTIALS FIX

Este archivo contiene pruebas completas para verificar que el sistema de validación
de credenciales AWS funciona correctamente.
"""

import unittest
import logging
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Importar el sistema de validación de credenciales AWS
from luminoracore_sdk_aws_credentials_fix import (
    LuminoraCoreAWSCredentialsValidator,
    AWSCredentialsError,
    DynamoDBPermissionsError,
    DynamoDBTableError,
    validate_aws_dynamodb_setup,
    get_validation_summary
)


class TestLuminoraCoreAWSCredentialsValidator(unittest.TestCase):
    """Pruebas para el validador de credenciales AWS."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.validator = LuminoraCoreAWSCredentialsValidator(region_name="eu-west-1")
    
    def test_validator_initialization(self):
        """Test: Inicialización del validador."""
        print("\n🧪 Test: Inicialización del validador")
        
        self.assertEqual(self.validator.region_name, "eu-west-1")
        self.assertIsNone(self.validator.session)
        self.assertIsNone(self.validator.sts_client)
        self.assertIsNone(self.validator.dynamodb_client)
        
        print("✅ Inicialización correcta")
    
    def test_auto_detect_region(self):
        """Test: Auto-detección de región."""
        print("\n🧪 Test: Auto-detección de región")
        
        # Test con región en variable de entorno
        with patch.dict('os.environ', {'AWS_REGION': 'us-east-1'}):
            validator = LuminoraCoreAWSCredentialsValidator()
            self.assertEqual(validator.region_name, "us-east-1")
        
        # Test con AWS_DEFAULT_REGION
        with patch.dict('os.environ', {'AWS_DEFAULT_REGION': 'us-west-2'}):
            validator = LuminoraCoreAWSCredentialsValidator()
            self.assertEqual(validator.region_name, "us-west-2")
        
        # Test con LUMINORACORE_AWS_REGION
        with patch.dict('os.environ', {'LUMINORACORE_AWS_REGION': 'ap-southeast-1'}):
            validator = LuminoraCoreAWSCredentialsValidator()
            self.assertEqual(validator.region_name, "ap-southeast-1")
        
        # Test sin variables de entorno (fallback)
        with patch.dict('os.environ', {}, clear=True):
            validator = LuminoraCoreAWSCredentialsValidator()
            self.assertEqual(validator.region_name, "eu-west-1")
        
        print("✅ Auto-detección de región correcta")
    
    @patch('boto3.Session')
    @patch('boto3.client')
    def test_validate_aws_credentials_success(self, mock_boto3_client, mock_boto3_session):
        """Test: Validación exitosa de credenciales AWS."""
        print("\n🧪 Test: Validación exitosa de credenciales AWS")
        
        # Mock de sesión y credenciales
        mock_credentials = Mock()
        mock_credentials.access_key = "test_access_key"
        mock_credentials.secret_key = "test_secret_key"
        
        mock_session = Mock()
        mock_session.get_credentials.return_value = mock_credentials
        mock_boto3_session.return_value = mock_session
        
        # Mock de STS client
        mock_sts_client = Mock()
        mock_sts_client.get_caller_identity.return_value = {
            "Account": "123456789012",
            "Arn": "arn:aws:iam::123456789012:user/test-user"
        }
        mock_boto3_client.return_value = mock_sts_client
        
        # Ejecutar validación
        result = self.validator.validate_aws_credentials()
        
        # Verificar resultado
        self.assertTrue(result["valid"])
        self.assertEqual(result["account_id"], "123456789012")
        self.assertEqual(result["user_arn"], "arn:aws:iam::123456789012:user/test-user")
        self.assertEqual(len(result["errors"]), 0)
        
        print("✅ Validación exitosa de credenciales AWS")
    
    @patch('boto3.Session')
    def test_validate_aws_credentials_no_credentials(self, mock_boto3_session):
        """Test: Validación de credenciales sin credenciales."""
        print("\n🧪 Test: Validación de credenciales sin credenciales")
        
        # Mock de sesión sin credenciales
        mock_session = Mock()
        mock_session.get_credentials.return_value = None
        mock_boto3_session.return_value = mock_session
        
        # Ejecutar validación
        result = self.validator.validate_aws_credentials()
        
        # Verificar resultado
        self.assertFalse(result["valid"])
        self.assertIn("No se encontraron credenciales AWS", result["errors"])
        
        print("✅ Validación de credenciales sin credenciales")
    
    @patch('boto3.Session')
    @patch('boto3.client')
    def test_validate_aws_credentials_invalid_credentials(self, mock_boto3_client, mock_boto3_session):
        """Test: Validación de credenciales inválidas."""
        print("\n🧪 Test: Validación de credenciales inválidas")
        
        # Mock de sesión con credenciales
        mock_credentials = Mock()
        mock_session = Mock()
        mock_session.get_credentials.return_value = mock_credentials
        mock_boto3_session.return_value = mock_session
        
        # Mock de STS client que falla
        mock_sts_client = Mock()
        mock_sts_client.get_caller_identity.side_effect = Exception("InvalidAccessKeyId")
        mock_boto3_client.return_value = mock_sts_client
        
        # Ejecutar validación
        result = self.validator.validate_aws_credentials()
        
        # Verificar resultado
        self.assertFalse(result["valid"])
        self.assertIn("InvalidAccessKeyId", result["errors"])
        
        print("✅ Validación de credenciales inválidas")
    
    @patch('boto3.client')
    def test_validate_table_exists_success(self, mock_boto3_client):
        """Test: Validación exitosa de existencia de tabla."""
        print("\n🧪 Test: Validación exitosa de existencia de tabla")
        
        # Mock de DynamoDB client
        mock_dynamodb_client = Mock()
        mock_dynamodb_client.describe_table.return_value = {
            'Table': {
                'TableStatus': 'ACTIVE',
                'TableArn': 'arn:aws:dynamodb:eu-west-1:123456789012:table/test-table'
            }
        }
        mock_boto3_client.return_value = mock_dynamodb_client
        self.validator.dynamodb_client = mock_dynamodb_client
        
        # Ejecutar validación
        result = self.validator.validate_table_exists("test-table")
        
        # Verificar resultado
        self.assertTrue(result["valid"])
        self.assertEqual(result["table_status"], "ACTIVE")
        self.assertIn("test-table", result["table_arn"])
        self.assertEqual(len(result["errors"]), 0)
        
        print("✅ Validación exitosa de existencia de tabla")
    
    @patch('boto3.client')
    def test_validate_table_exists_not_found(self, mock_boto3_client):
        """Test: Validación de tabla no encontrada."""
        print("\n🧪 Test: Validación de tabla no encontrada")
        
        # Mock de DynamoDB client
        mock_dynamodb_client = Mock()
        mock_dynamodb_client.describe_table.side_effect = Exception("ResourceNotFoundException")
        mock_boto3_client.return_value = mock_dynamodb_client
        self.validator.dynamodb_client = mock_dynamodb_client
        
        # Ejecutar validación
        result = self.validator.validate_table_exists("nonexistent-table")
        
        # Verificar resultado
        self.assertFalse(result["valid"])
        self.assertIn("nonexistent-table no encontrada", result["errors"])
        
        print("✅ Validación de tabla no encontrada")
    
    @patch('boto3.client')
    def test_validate_table_exists_inactive(self, mock_boto3_client):
        """Test: Validación de tabla inactiva."""
        print("\n🧪 Test: Validación de tabla inactiva")
        
        # Mock de DynamoDB client
        mock_dynamodb_client = Mock()
        mock_dynamodb_client.describe_table.return_value = {
            'Table': {
                'TableStatus': 'CREATING',
                'TableArn': 'arn:aws:dynamodb:eu-west-1:123456789012:table/test-table'
            }
        }
        mock_boto3_client.return_value = mock_dynamodb_client
        self.validator.dynamodb_client = mock_dynamodb_client
        
        # Ejecutar validación
        result = self.validator.validate_table_exists("test-table")
        
        # Verificar resultado
        self.assertFalse(result["valid"])
        self.assertIn("no está activa: CREATING", result["errors"])
        
        print("✅ Validación de tabla inactiva")
    
    @patch('boto3.client')
    def test_validate_table_schema(self, mock_boto3_client):
        """Test: Validación de esquema de tabla."""
        print("\n🧪 Test: Validación de esquema de tabla")
        
        # Mock de DynamoDB client
        mock_dynamodb_client = Mock()
        mock_dynamodb_client.describe_table.return_value = {
            'Table': {
                'KeySchema': [
                    {'AttributeName': 'PK', 'KeyType': 'HASH'},
                    {'AttributeName': 'SK', 'KeyType': 'RANGE'}
                ],
                'GlobalSecondaryIndexes': [
                    {
                        'IndexName': 'GSI1',
                        'KeySchema': [
                            {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},
                            {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}
                        ]
                    }
                ]
            }
        }
        mock_boto3_client.return_value = mock_dynamodb_client
        self.validator.dynamodb_client = mock_dynamodb_client
        
        # Ejecutar validación
        result = self.validator.validate_table_schema("test-table")
        
        # Verificar resultado
        self.assertTrue(result["valid"])
        self.assertEqual(result["hash_key"], "PK")
        self.assertEqual(result["range_key"], "SK")
        self.assertEqual(result["gsi_count"], 1)
        
        print("✅ Validación de esquema de tabla")
    
    @patch('boto3.client')
    def test_validate_dynamodb_permissions(self, mock_boto3_client):
        """Test: Validación de permisos DynamoDB."""
        print("\n🧪 Test: Validación de permisos DynamoDB")
        
        # Mock de DynamoDB client
        mock_dynamodb_client = Mock()
        mock_dynamodb_client.describe_table.return_value = {
            'Table': {
                'TableStatus': 'ACTIVE',
                'TableArn': 'arn:aws:dynamodb:eu-west-1:123456789012:table/test-table'
            }
        }
        mock_dynamodb_client.scan.return_value = {'Items': []}
        mock_dynamodb_client.get_item.return_value = {}
        mock_boto3_client.return_value = mock_dynamodb_client
        self.validator.dynamodb_client = mock_dynamodb_client
        
        # Ejecutar validación
        result = self.validator.validate_dynamodb_permissions("test-table", [
            "dynamodb:DescribeTable",
            "dynamodb:GetItem",
            "dynamodb:Scan"
        ])
        
        # Verificar resultado
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["tested_permissions"]), 3)
        
        print("✅ Validación de permisos DynamoDB")
    
    @patch('boto3.client')
    def test_validate_dynamodb_permissions_insufficient(self, mock_boto3_client):
        """Test: Validación de permisos DynamoDB insuficientes."""
        print("\n🧪 Test: Validación de permisos DynamoDB insuficientes")
        
        # Mock de DynamoDB client que falla en algunos permisos
        mock_dynamodb_client = Mock()
        mock_dynamodb_client.describe_table.return_value = {
            'Table': {
                'TableStatus': 'ACTIVE',
                'TableArn': 'arn:aws:dynamodb:eu-west-1:123456789012:table/test-table'
            }
        }
        mock_dynamodb_client.scan.side_effect = Exception("AccessDenied")
        mock_dynamodb_client.get_item.return_value = {}
        mock_boto3_client.return_value = mock_dynamodb_client
        self.validator.dynamodb_client = mock_dynamodb_client
        
        # Ejecutar validación
        result = self.validator.validate_dynamodb_permissions("test-table", [
            "dynamodb:DescribeTable",
            "dynamodb:Scan"
        ])
        
        # Verificar resultado
        self.assertFalse(result["valid"])
        self.assertIn("AccessDenied", result["errors"])
        
        print("✅ Validación de permisos DynamoDB insuficientes")
    
    @patch('boto3.client')
    def test_test_basic_operations(self, mock_boto3_client):
        """Test: Prueba de operaciones básicas."""
        print("\n🧪 Test: Prueba de operaciones básicas")
        
        # Mock de DynamoDB client
        mock_dynamodb_client = Mock()
        mock_dynamodb_client.scan.return_value = {'Items': []}
        mock_boto3_client.return_value = mock_dynamodb_client
        self.validator.dynamodb_client = mock_dynamodb_client
        
        # Ejecutar prueba
        result = self.validator.test_basic_operations("test-table")
        
        # Verificar resultado
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["operations_tested"]), 1)
        
        print("✅ Prueba de operaciones básicas")
    
    def test_validate_complete_setup(self):
        """Test: Validación completa de configuración."""
        print("\n🧪 Test: Validación completa de configuración")
        
        # Mock de todos los métodos
        with patch.object(self.validator, 'validate_aws_credentials') as mock_creds, \
             patch.object(self.validator, 'validate_dynamodb_permissions') as mock_perms, \
             patch.object(self.validator, 'validate_table_exists') as mock_table, \
             patch.object(self.validator, 'validate_table_schema') as mock_schema, \
             patch.object(self.validator, 'test_basic_operations') as mock_ops:
            
            # Configurar mocks para éxito
            mock_creds.return_value = {"valid": True, "errors": []}
            mock_perms.return_value = {"valid": True, "errors": []}
            mock_table.return_value = {"valid": True, "errors": []}
            mock_schema.return_value = {"valid": True, "warnings": []}
            mock_ops.return_value = {"valid": True, "errors": []}
            
            # Ejecutar validación completa
            result = self.validator.validate_complete_setup("test-table")
            
            # Verificar resultado
            self.assertTrue(result["success"])
            self.assertEqual(len(result["errors"]), 0)
            self.assertIn("aws_credentials", result["checks"])
            self.assertIn("dynamodb_permissions", result["checks"])
            self.assertIn("table_exists", result["checks"])
            self.assertIn("table_schema", result["checks"])
            self.assertIn("basic_operations", result["checks"])
            
        print("✅ Validación completa de configuración")
    
    def test_validate_complete_setup_with_errors(self):
        """Test: Validación completa con errores."""
        print("\n🧪 Test: Validación completa con errores")
        
        # Mock de todos los métodos
        with patch.object(self.validator, 'validate_aws_credentials') as mock_creds, \
             patch.object(self.validator, 'validate_dynamodb_permissions') as mock_perms, \
             patch.object(self.validator, 'validate_table_exists') as mock_table, \
             patch.object(self.validator, 'validate_table_schema') as mock_schema, \
             patch.object(self.validator, 'test_basic_operations') as mock_ops:
            
            # Configurar mocks con errores
            mock_creds.return_value = {"valid": False, "errors": ["No credentials found"]}
            mock_perms.return_value = {"valid": False, "errors": ["Access denied"]}
            mock_table.return_value = {"valid": False, "errors": ["Table not found"]}
            mock_schema.return_value = {"valid": True, "warnings": []}
            mock_ops.return_value = {"valid": True, "errors": []}
            
            # Ejecutar validación completa
            result = self.validator.validate_complete_setup("test-table")
            
            # Verificar resultado
            self.assertFalse(result["success"])
            self.assertGreater(len(result["errors"]), 0)
            
        print("✅ Validación completa con errores")
    
    def test_get_validation_summary(self):
        """Test: Obtención de resumen de validación."""
        print("\n🧪 Test: Obtención de resumen de validación")
        
        # Configurar resultados de validación
        self.validator._validation_results = {
            "success": True,
            "timestamp": "2024-01-01T10:00:00Z",
            "region": "eu-west-1",
            "table_name": "test-table",
            "errors": [],
            "warnings": ["Table without GSI"],
            "recommendations": ["Consider adding GSI for better performance"]
        }
        
        # Obtener resumen
        summary = self.validator.get_validation_summary()
        
        # Verificar resumen
        self.assertIn("ÉXITO", summary)
        self.assertIn("eu-west-1", summary)
        self.assertIn("test-table", summary)
        self.assertIn("Table without GSI", summary)
        
        print("✅ Obtención de resumen de validación")


class TestConvenienceFunctions(unittest.TestCase):
    """Pruebas para las funciones de conveniencia."""
    
    @patch('luminoracore_sdk_aws_credentials_fix.LuminoraCoreAWSCredentialsValidator')
    def test_validate_aws_dynamodb_setup(self, mock_validator_class):
        """Test: Función de conveniencia para validación."""
        print("\n🧪 Test: Función de conveniencia para validación")
        
        # Mock del validador
        mock_validator = Mock()
        mock_validator.validate_complete_setup.return_value = {
            "success": True,
            "errors": [],
            "warnings": []
        }
        mock_validator_class.return_value = mock_validator
        
        # Ejecutar función de conveniencia
        result = validate_aws_dynamodb_setup("test-table", "eu-west-1")
        
        # Verificar resultado
        self.assertTrue(result["success"])
        mock_validator.validate_complete_setup.assert_called_once_with("test-table", None)
        
        print("✅ Función de conveniencia para validación")
    
    @patch('luminoracore_sdk_aws_credentials_fix.LuminoraCoreAWSCredentialsValidator')
    def test_get_validation_summary(self, mock_validator_class):
        """Test: Función de conveniencia para resumen."""
        print("\n🧪 Test: Función de conveniencia para resumen")
        
        # Mock del validador
        mock_validator = Mock()
        mock_validator.validate_complete_setup.return_value = {
            "success": True,
            "errors": [],
            "warnings": []
        }
        mock_validator.get_validation_summary.return_value = "Validation summary"
        mock_validator_class.return_value = mock_validator
        
        # Ejecutar función de conveniencia
        summary = get_validation_summary("test-table", "eu-west-1")
        
        # Verificar resultado
        self.assertEqual(summary, "Validation summary")
        
        print("✅ Función de conveniencia para resumen")


def run_all_tests():
    """Ejecutar todas las pruebas."""
    print("🚀 INICIANDO PRUEBAS COMPLETAS DE LUMINORACORE SDK AWS CREDENTIALS FIX")
    print("=" * 80)
    
    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las pruebas
    suite.addTests(loader.loadTestsFromTestCase(TestLuminoraCoreAWSCredentialsValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestConvenienceFunctions))
    
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
