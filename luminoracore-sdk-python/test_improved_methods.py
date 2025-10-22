#!/usr/bin/env python3
"""
PRUEBAS COMPLETAS PARA LUMINORACORE SDK IMPROVED METHODS

Este archivo contiene pruebas completas para verificar que los métodos mejorados
funcionan correctamente y resuelven los problemas de validación y manejo de errores.
"""

import unittest
import logging
import sys
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

# Importar los métodos mejorados
from luminoracore_sdk_improved_methods import (
    ImprovedClientV11,
    ImprovedMemoryManagerV11,
    ImprovedFlexibleDynamoDBStorageV11,
    create_improved_storage,
    create_improved_memory_manager,
    create_improved_client_v11
)


class TestImprovedClientV11(unittest.TestCase):
    """Pruebas para el cliente v11 mejorado."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.base_client = Mock()
        self.storage_v11 = Mock()
        self.memory_v11 = Mock()
        
        self.client = ImprovedClientV11(
            base_client=self.base_client,
            storage_v11=self.storage_v11,
            memory_v11=self.memory_v11
        )
    
    def test_client_initialization(self):
        """Test: Inicialización del cliente mejorado."""
        print("\n🧪 Test: Inicialización del cliente mejorado")
        
        self.assertEqual(self.client.base_client, self.base_client)
        self.assertEqual(self.client.storage_v11, self.storage_v11)
        self.assertEqual(self.client.memory_v11, self.memory_v11)
        
        print("✅ Inicialización correcta")
    
    async def test_get_facts_success(self):
        """Test: get_facts exitoso."""
        print("\n🧪 Test: get_facts exitoso")
        
        # Mock de memory_v11
        self.memory_v11.get_facts = AsyncMock(return_value=[
            {"category": "personal_info", "key": "name", "value": "John"},
            {"category": "personal_info", "key": "age", "value": 25}
        ])
        
        # Ejecutar get_facts
        result = await self.client.get_facts("user123", category="personal_info")
        
        # Verificar resultado
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["key"], "name")
        self.assertEqual(result[1]["key"], "age")
        
        print("✅ get_facts exitoso")
    
    async def test_get_facts_no_memory_v11(self):
        """Test: get_facts sin memory_v11."""
        print("\n🧪 Test: get_facts sin memory_v11")
        
        # Cliente sin memory_v11
        client = ImprovedClientV11(base_client=self.base_client, storage_v11=self.storage_v11)
        
        # Ejecutar get_facts
        result = await client.get_facts("user123")
        
        # Verificar resultado
        self.assertIsInstance(result, dict)
        self.assertFalse(result["success"])
        self.assertIn("Memory v1.1 no está configurado", result["error"])
        
        print("✅ get_facts sin memory_v11")
    
    async def test_get_facts_no_storage_v11(self):
        """Test: get_facts sin storage_v11."""
        print("\n🧪 Test: get_facts sin storage_v11")
        
        # Cliente sin storage_v11
        client = ImprovedClientV11(base_client=self.base_client, memory_v11=self.memory_v11)
        
        # Ejecutar get_facts
        result = await client.get_facts("user123")
        
        # Verificar resultado
        self.assertIsInstance(result, dict)
        self.assertFalse(result["success"])
        self.assertIn("Storage v1.1 no está configurado", result["error"])
        
        print("✅ get_facts sin storage_v11")
    
    async def test_get_facts_memory_error(self):
        """Test: get_facts con error en memory_v11."""
        print("\n🧪 Test: get_facts con error en memory_v11")
        
        # Mock de memory_v11 que devuelve error
        self.memory_v11.get_facts = AsyncMock(return_value={
            "success": False,
            "error": "Memory error",
            "error_type": "MemoryError"
        })
        
        # Ejecutar get_facts
        result = await self.client.get_facts("user123")
        
        # Verificar resultado
        self.assertIsInstance(result, dict)
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Memory error")
        
        print("✅ get_facts con error en memory_v11")


class TestImprovedMemoryManagerV11(unittest.TestCase):
    """Pruebas para el memory manager v11 mejorado."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.storage_v11 = Mock()
        self.vector_store = Mock()
        
        self.memory_manager = ImprovedMemoryManagerV11(
            storage_v11=self.storage_v11,
            vector_store=self.vector_store
        )
    
    def test_memory_manager_initialization(self):
        """Test: Inicialización del memory manager mejorado."""
        print("\n🧪 Test: Inicialización del memory manager mejorado")
        
        self.assertEqual(self.memory_manager.storage, self.storage_v11)
        self.assertEqual(self.memory_manager.vector_store, self.vector_store)
        
        print("✅ Inicialización correcta")
    
    async def test_get_facts_success(self):
        """Test: get_facts exitoso."""
        print("\n🧪 Test: get_facts exitoso")
        
        # Mock de storage
        self.storage_v11.get_facts = AsyncMock(return_value=[
            {"category": "personal_info", "key": "name", "value": "John"},
            {"category": "personal_info", "key": "age", "value": 25}
        ])
        
        # Ejecutar get_facts
        result = await self.memory_manager.get_facts("user123", options={"category": "personal_info"})
        
        # Verificar resultado
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["key"], "name")
        self.assertEqual(result[1]["key"], "age")
        
        print("✅ get_facts exitoso")
    
    async def test_get_facts_no_storage(self):
        """Test: get_facts sin storage."""
        print("\n🧪 Test: get_facts sin storage")
        
        # Memory manager sin storage
        memory_manager = ImprovedMemoryManagerV11()
        
        # Ejecutar get_facts
        result = await memory_manager.get_facts("user123")
        
        # Verificar resultado
        self.assertIsInstance(result, dict)
        self.assertFalse(result["success"])
        self.assertIn("Storage no está configurado", result["error"])
        
        print("✅ get_facts sin storage")
    
    async def test_get_facts_with_filters(self):
        """Test: get_facts con filtros."""
        print("\n🧪 Test: get_facts con filtros")
        
        # Mock de storage
        self.storage_v11.get_facts = AsyncMock(return_value=[
            {"category": "personal_info", "key": "name", "value": "John", "is_active": True},
            {"category": "personal_info", "key": "age", "value": 25, "is_active": False},
            {"category": "personal_info", "key": "city", "value": "Madrid", "is_active": True}
        ])
        
        # Ejecutar get_facts con filtros
        options = {
            "category": "personal_info",
            "include_inactive": False,
            "max_results": 2
        }
        result = await self.memory_manager.get_facts("user123", options=options)
        
        # Verificar resultado
        self.assertEqual(len(result), 2)  # Solo 2 resultados por max_results
        self.assertTrue(all(fact.get("is_active", True) for fact in result))  # Solo activos
        
        print("✅ get_facts con filtros")


class TestImprovedFlexibleDynamoDBStorageV11(unittest.TestCase):
    """Pruebas para el storage DynamoDB mejorado."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.table_name = "test-table"
        self.region_name = "eu-west-1"
    
    @patch('boto3.resource')
    @patch('boto3.client')
    def test_storage_initialization_success(self, mock_boto3_client, mock_boto3_resource):
        """Test: Inicialización exitosa del storage."""
        print("\n🧪 Test: Inicialización exitosa del storage")
        
        # Mock de DynamoDB
        mock_table = Mock()
        mock_table.table_name = self.table_name
        mock_table.table_status = "ACTIVE"
        
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
        
        # Crear storage
        storage = ImprovedFlexibleDynamoDBStorageV11(
            table_name=self.table_name,
            region_name=self.region_name
        )
        
        # Verificar inicialización
        self.assertTrue(storage._initialized)
        self.assertEqual(storage.table_name, self.table_name)
        self.assertEqual(storage.region_name, self.region_name)
        
        print("✅ Inicialización exitosa del storage")
    
    @patch('boto3.resource')
    @patch('boto3.client')
    def test_storage_initialization_failure(self, mock_boto3_client, mock_boto3_resource):
        """Test: Inicialización fallida del storage."""
        print("\n🧪 Test: Inicialización fallida del storage")
        
        # Mock que falla
        mock_boto3_resource.side_effect = Exception("AWS credentials not found")
        
        # Crear storage
        storage = ImprovedFlexibleDynamoDBStorageV11(
            table_name=self.table_name,
            region_name=self.region_name
        )
        
        # Verificar que no está inicializado
        self.assertFalse(storage._initialized)
        self.assertIsNotNone(storage._initialization_error)
        
        print("✅ Inicialización fallida del storage")
    
    @patch('boto3.resource')
    @patch('boto3.client')
    async def test_get_facts_success(self, mock_boto3_client, mock_boto3_resource):
        """Test: get_facts exitoso."""
        print("\n🧪 Test: get_facts exitoso")
        
        # Mock de DynamoDB
        mock_table = Mock()
        mock_table.table_name = self.table_name
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
        
        # Crear storage
        storage = ImprovedFlexibleDynamoDBStorageV11(
            table_name=self.table_name,
            region_name=self.region_name
        )
        
        # Ejecutar get_facts
        result = await storage.get_facts("user123")
        
        # Verificar resultado
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["key"], "name")
        self.assertEqual(result[0]["value"], "John")
        
        print("✅ get_facts exitoso")
    
    @patch('boto3.resource')
    @patch('boto3.client')
    async def test_get_facts_not_initialized(self, mock_boto3_client, mock_boto3_resource):
        """Test: get_facts sin inicializar."""
        print("\n🧪 Test: get_facts sin inicializar")
        
        # Mock que falla
        mock_boto3_resource.side_effect = Exception("AWS credentials not found")
        
        # Crear storage
        storage = ImprovedFlexibleDynamoDBStorageV11(
            table_name=self.table_name,
            region_name=self.region_name
        )
        
        # Ejecutar get_facts
        with self.assertRaises(Exception):
            await storage.get_facts("user123")
        
        print("✅ get_facts sin inicializar")


class TestConvenienceFunctions(unittest.TestCase):
    """Pruebas para las funciones de conveniencia."""
    
    def test_create_improved_storage(self):
        """Test: Función de conveniencia para crear storage."""
        print("\n🧪 Test: Función de conveniencia para crear storage")
        
        with patch('luminoracore_sdk_improved_methodii.ImprovedFlexibleDynamoDBStorageV11') as mock_storage_class:
            mock_storage = Mock()
            mock_storage_class.return_value = mock_storage
            
            # Ejecutar función de conveniencia
            result = create_improved_storage("test-table", "eu-west-1")
            
            # Verificar resultado
            self.assertEqual(result, mock_storage)
            mock_storage_class.assert_called_once_with("test-table", "eu-west-1")
        
        print("✅ Función de conveniencia para crear storage")
    
    def test_create_improved_memory_manager(self):
        """Test: Función de conveniencia para crear memory manager."""
        print("\n🧪 Test: Función de conveniencia para crear memory manager")
        
        mock_storage = Mock()
        mock_vector_store = Mock()
        
        # Ejecutar función de conveniencia
        result = create_improved_memory_manager(mock_storage, mock_vector_store)
        
        # Verificar resultado
        self.assertIsInstance(result, ImprovedMemoryManagerV11)
        self.assertEqual(result.storage, mock_storage)
        self.assertEqual(result.vector_store, mock_vector_store)
        
        print("✅ Función de conveniencia para crear memory manager")
    
    def test_create_improved_client_v11(self):
        """Test: Función de conveniencia para crear client v11."""
        print("\n🧪 Test: Función de conveniencia para crear client v11")
        
        mock_base_client = Mock()
        mock_storage = Mock()
        mock_memory = Mock()
        
        # Ejecutar función de conveniencia
        result = create_improved_client_v11(mock_base_client, mock_storage, mock_memory)
        
        # Verificar resultado
        self.assertIsInstance(result, ImprovedClientV11)
        self.assertEqual(result.base_client, mock_base_client)
        self.assertEqual(result.storage_v11, mock_storage)
        self.assertEqual(result.memory_v11, mock_memory)
        
        print("✅ Función de conveniencia para crear client v11")


class TestIntegrationScenarios(unittest.TestCase):
    """Pruebas de integración con escenarios reales."""
    
    async def test_complete_flow_success(self):
        """Test: Flujo completo exitoso."""
        print("\n🧪 Test: Flujo completo exitoso")
        
        # Mock de storage
        mock_storage = Mock()
        mock_storage.get_facts = AsyncMock(return_value=[
            {"category": "personal_info", "key": "name", "value": "John"},
            {"category": "personal_info", "key": "age", "value": 25}
        ])
        
        # Mock de memory manager
        mock_memory = Mock()
        mock_memory.get_facts = AsyncMock(return_value=[
            {"category": "personal_info", "key": "name", "value": "John"},
            {"category": "personal_info", "key": "age", "value": 25}
        ])
        
        # Mock de base client
        mock_base_client = Mock()
        
        # Crear client mejorado
        client = ImprovedClientV11(
            base_client=mock_base_client,
            storage_v11=mock_storage,
            memory_v11=mock_memory
        )
        
        # Ejecutar flujo completo
        result = await client.get_facts("user123", category="personal_info")
        
        # Verificar resultado
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["key"], "name")
        self.assertEqual(result[1]["key"], "age")
        
        print("✅ Flujo completo exitoso")
    
    async def test_complete_flow_with_errors(self):
        """Test: Flujo completo con errores."""
        print("\n🧪 Test: Flujo completo con errores")
        
        # Mock de storage
        mock_storage = Mock()
        mock_storage.get_facts = AsyncMock(return_value={
            "success": False,
            "error": "Storage error",
            "error_type": "StorageError"
        })
        
        # Mock de memory manager
        mock_memory = Mock()
        mock_memory.get_facts = AsyncMock(return_value={
            "success": False,
            "error": "Storage error",
            "error_type": "StorageError"
        })
        
        # Mock de base client
        mock_base_client = Mock()
        
        # Crear client mejorado
        client = ImprovedClientV11(
            base_client=mock_base_client,
            storage_v11=mock_storage,
            memory_v11=mock_memory
        )
        
        # Ejecutar flujo completo
        result = await client.get_facts("user123")
        
        # Verificar resultado
        self.assertIsInstance(result, dict)
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Storage error")
        
        print("✅ Flujo completo con errores")


def run_async_test(test_func):
    """Ejecutar test asíncrono."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(test_func())
    finally:
        loop.close()


def run_all_tests():
    """Ejecutar todas las pruebas."""
    print("🚀 INICIANDO PRUEBAS COMPLETAS DE LUMINORACORE SDK IMPROVED METHODS")
    print("=" * 80)
    
    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las pruebas
    suite.addTests(loader.loadTestsFromTestCase(TestImprovedClientV11))
    suite.addTests(loader.loadTestsFromTestCase(TestImprovedMemoryManagerV11))
    suite.addTests(loader.loadTestsFromTestCase(TestImprovedFlexibleDynamoDBStorageV11))
    suite.addTests(loader.loadTestsFromTestCase(TestConvenienceFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationScenarios))
    
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
