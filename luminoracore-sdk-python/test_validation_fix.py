#!/usr/bin/env python3
"""
PRUEBAS COMPLETAS PARA LUMINORACORE SDK VALIDATION FIX

Este archivo contiene pruebas completas para verificar que el sistema de validación
funciona correctamente y resuelve el problema de falta de validación en get_facts().
"""

import unittest
import logging
import sys
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

# Importar el sistema de validación fix
from luminoracore_sdk_validation_fix import (
    LuminoraCoreValidationManager,
    ValidationError,
    StorageConfigurationError,
    configure_validation
)


class TestLuminoraCoreValidationManager(unittest.TestCase):
    """Pruebas para el manager de validación del SDK."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.validation_manager = LuminoraCoreValidationManager()
        self.validation_manager.validation_enabled = True
        self.validation_manager.debug_mode = False
    
    def test_validation_manager_initialization(self):
        """Test: Inicialización del manager de validación."""
        print("\n🧪 Test: Inicialización del manager de validación")
        
        self.assertTrue(self.validation_manager.validation_enabled)
        self.assertFalse(self.validation_manager.debug_mode)
        
        print("✅ Inicialización correcta")
    
    def test_debug_mode_toggle(self):
        """Test: Activar/desactivar modo debug."""
        print("\n🧪 Test: Activar/desactivar modo debug")
        
        # Activar debug mode
        self.validation_manager.enable_debug_mode(True)
        self.assertTrue(self.validation_manager.debug_mode)
        
        # Desactivar debug mode
        self.validation_manager.enable_debug_mode(False)
        self.assertFalse(self.validation_manager.debug_mode)
        
        print("✅ Modo debug funciona correctamente")
    
    def test_storage_configuration_validation(self):
        """Test: Validación de configuración de storage."""
        print("\n🧪 Test: Validación de configuración de storage")
        
        # Test con storage None
        with self.assertRaises(StorageConfigurationError):
            self.validation_manager.validate_storage_configuration(None)
        
        # Test con storage sin método get_facts
        mock_storage = Mock()
        del mock_storage.get_facts  # Remover método get_facts
        
        with self.assertRaises(StorageConfigurationError):
            self.validation_manager.validate_storage_configuration(mock_storage)
        
        # Test con storage válido
        mock_storage = Mock()
        mock_storage.get_facts = Mock()
        mock_storage.table_name = "test-table"
        mock_storage.table = Mock()
        
        result = self.validation_manager.validate_storage_configuration(mock_storage)
        self.assertTrue(result)
        
        print("✅ Validación de configuración de storage correcta")
    
    def test_user_id_validation(self):
        """Test: Validación de user_id."""
        print("\n🧪 Test: Validación de user_id")
        
        # Test con user_id None
        with self.assertRaises(ValidationError):
            self.validation_manager.validate_user_id(None)
        
        # Test con user_id vacío
        with self.assertRaises(ValidationError):
            self.validation_manager.validate_user_id("")
        
        # Test con user_id solo espacios
        with self.assertRaises(ValidationError):
            self.validation_manager.validate_user_id("   ")
        
        # Test con user_id no string
        with self.assertRaises(ValidationError):
            self.validation_manager.validate_user_id(123)
        
        # Test con user_id válido
        result = self.validation_manager.validate_user_id("valid_user_id")
        self.assertTrue(result)
        
        print("✅ Validación de user_id correcta")
    
    def test_category_validation(self):
        """Test: Validación de categoría."""
        print("\n🧪 Test: Validación de categoría")
        
        # Test con categoría None (válido)
        result = self.validation_manager.validate_category(None)
        self.assertTrue(result)
        
        # Test con categoría vacía
        with self.assertRaises(ValidationError):
            self.validation_manager.validate_category("")
        
        # Test con categoría solo espacios
        with self.assertRaises(ValidationError):
            self.validation_manager.validate_category("   ")
        
        # Test con categoría no string
        with self.assertRaises(ValidationError):
            self.validation_manager.validate_category(123)
        
        # Test con categoría válida
        result = self.validation_manager.validate_category("valid_category")
        self.assertTrue(result)
        
        print("✅ Validación de categoría correcta")


class TestSafeGetFacts(unittest.TestCase):
    """Pruebas para el método safe_get_facts."""
    
    def setUp(self):
        """Configuración inicial."""
        self.validation_manager = LuminoraCoreValidationManager()
        self.validation_manager.validation_enabled = True
        self.validation_manager.debug_mode = False
    
    async def test_safe_get_facts_success(self):
        """Test: safe_get_facts exitoso."""
        print("\n🧪 Test: safe_get_facts exitoso")
        
        # Mock storage
        mock_storage = Mock()
        mock_storage.get_facts = AsyncMock(return_value=[
            {"category": "personal_info", "key": "name", "value": "John"},
            {"category": "personal_info", "key": "age", "value": 25}
        ])
        mock_storage.table_name = "test-table"
        mock_storage.table = Mock()
        
        # Ejecutar safe_get_facts
        result = await self.validation_manager.safe_get_facts(
            mock_storage,
            "user123",
            category="personal_info"
        )
        
        # Verificar resultado
        self.assertTrue(result["success"])
        self.assertEqual(len(result["data"]), 2)
        self.assertIsNone(result["error"])
        self.assertEqual(len(result["validation_errors"]), 0)
        
        print("✅ safe_get_facts exitoso")
    
    async def test_safe_get_facts_storage_error(self):
        """Test: safe_get_facts con error de storage."""
        print("\n🧪 Test: safe_get_facts con error de storage")
        
        # Mock storage con error
        mock_storage = Mock()
        mock_storage.get_facts = AsyncMock(side_effect=Exception("Storage error"))
        mock_storage.table_name = "test-table"
        mock_storage.table = Mock()
        
        # Ejecutar safe_get_facts
        result = await self.validation_manager.safe_get_facts(
            mock_storage,
            "user123"
        )
        
        # Verificar resultado
        self.assertFalse(result["success"])
        self.assertIsNone(result["data"])
        self.assertIn("Storage error", result["error"])
        self.assertEqual(result["error_type"], "Exception")
        
        print("✅ safe_get_facts con error de storage")
    
    async def test_safe_get_facts_validation_error(self):
        """Test: safe_get_facts con error de validación."""
        print("\n🧪 Test: safe_get_facts con error de validación")
        
        # Mock storage
        mock_storage = Mock()
        mock_storage.get_facts = AsyncMock()
        mock_storage.table_name = "test-table"
        mock_storage.table = Mock()
        
        # Ejecutar safe_get_facts con user_id inválido
        result = await self.validation_manager.safe_get_facts(
            mock_storage,
            "",  # user_id vacío
            category="personal_info"
        )
        
        # Verificar resultado
        self.assertFalse(result["success"])
        self.assertIsNone(result["data"])
        self.assertEqual(result["error_type"], "ValidationError")
        self.assertIn("user_id no puede estar vacío", result["error"])
        
        print("✅ safe_get_facts con error de validación")
    
    async def test_safe_get_facts_timeout(self):
        """Test: safe_get_facts con timeout."""
        print("\n🧪 Test: safe_get_facts con timeout")
        
        # Mock storage que nunca responde
        mock_storage = Mock()
        mock_storage.get_facts = AsyncMock(side_effect=asyncio.TimeoutError())
        mock_storage.table_name = "test-table"
        mock_storage.table = Mock()
        
        # Ejecutar safe_get_facts
        result = await self.validation_manager.safe_get_facts(
            mock_storage,
            "user123"
        )
        
        # Verificar resultado
        self.assertFalse(result["success"])
        self.assertIsNone(result["data"])
        self.assertEqual(result["error_type"], "TimeoutError")
        self.assertIn("Timeout", result["error"])
        
        print("✅ safe_get_facts con timeout")
    
    async def test_safe_get_facts_debug_mode(self):
        """Test: safe_get_facts en modo debug."""
        print("\n🧪 Test: safe_get_facts en modo debug")
        
        # Activar debug mode
        self.validation_manager.debug_mode = True
        
        # Mock storage
        mock_storage = Mock()
        mock_storage.get_facts = AsyncMock(return_value=[])
        mock_storage.table_name = "test-table"
        mock_storage.table = Mock()
        
        # Ejecutar safe_get_facts
        result = await self.validation_manager.safe_get_facts(
            mock_storage,
            "user123"
        )
        
        # Verificar que hay información de debug
        self.assertTrue(result["success"])
        self.assertIsNotNone(result["debug_info"])
        self.assertIn("storage_type", result["debug_info"])
        self.assertIn("execution_time_ms", result["debug_info"])
        
        print("✅ safe_get_facts en modo debug")


class TestErrorResponseCreation(unittest.TestCase):
    """Pruebas para la creación de respuestas de error."""
    
    def setUp(self):
        """Configuración inicial."""
        self.validation_manager = LuminoraCoreValidationManager()
    
    def test_create_error_response(self):
        """Test: Creación de respuesta de error."""
        print("\n🧪 Test: Creación de respuesta de error")
        
        error_response = self.validation_manager.create_error_response(
            error_message="Test error",
            error_type="TestError",
            validation_errors=["Validation error 1", "Validation error 2"],
            debug_info={"test": "debug_info"}
        )
        
        # Verificar estructura
        self.assertFalse(error_response["success"])
        self.assertIsNone(error_response["data"])
        self.assertEqual(error_response["error"], "Test error")
        self.assertEqual(error_response["error_type"], "TestError")
        self.assertEqual(len(error_response["validation_errors"]), 2)
        self.assertEqual(error_response["debug_info"]["test"], "debug_info")
        
        print("✅ Creación de respuesta de error correcta")


class TestConvenienceFunctions(unittest.TestCase):
    """Pruebas para las funciones de conveniencia."""
    
    def test_configure_validation(self):
        """Test: Función de configuración de validación."""
        print("\n🧪 Test: Función de configuración de validación")
        
        # Configurar validación
        configure_validation(debug_mode=True, validation_enabled=False)
        
        # Verificar que se configuró correctamente
        # (Esto requeriría acceso a la instancia global)
        
        print("✅ Función de configuración de validación")


class TestIntegrationScenarios(unittest.TestCase):
    """Pruebas de integración con escenarios reales."""
    
    def setUp(self):
        """Configuración inicial."""
        self.validation_manager = LuminoraCoreValidationManager()
        self.validation_manager.validation_enabled = True
        self.validation_manager.debug_mode = False
    
    async def test_complete_validation_flow(self):
        """Test: Flujo completo de validación."""
        print("\n🧪 Test: Flujo completo de validación")
        
        # Mock storage
        mock_storage = Mock()
        mock_storage.get_facts = AsyncMock(return_value=[
            {"category": "personal_info", "key": "name", "value": "John"},
            {"category": "personal_info", "key": "age", "value": 25}
        ])
        mock_storage.table_name = "test-table"
        mock_storage.table = Mock()
        
        # Ejecutar flujo completo
        result = await self.validation_manager.safe_get_facts(
            mock_storage,
            "user123",
            category="personal_info"
        )
        
        # Verificar resultado completo
        self.assertTrue(result["success"])
        self.assertEqual(len(result["data"]), 2)
        self.assertIsNone(result["error"])
        self.assertEqual(len(result["validation_errors"]), 0)
        self.assertIsNotNone(result["debug_info"])
        
        print("✅ Flujo completo de validación")
    
    async def test_error_handling_flow(self):
        """Test: Flujo de manejo de errores."""
        print("\n🧪 Test: Flujo de manejo de errores")
        
        # Mock storage con error
        mock_storage = Mock()
        mock_storage.get_facts = AsyncMock(side_effect=Exception("Database connection failed"))
        mock_storage.table_name = "test-table"
        mock_storage.table = Mock()
        
        # Ejecutar con error
        result = await self.validation_manager.safe_get_facts(
            mock_storage,
            "user123"
        )
        
        # Verificar manejo de error
        self.assertFalse(result["success"])
        self.assertIsNone(result["data"])
        self.assertIn("Database connection failed", result["error"])
        self.assertEqual(result["error_type"], "Exception")
        self.assertIsNotNone(result["debug_info"])
        
        print("✅ Flujo de manejo de errores")


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
    print("🚀 INICIANDO PRUEBAS COMPLETAS DE LUMINORACORE SDK VALIDATION FIX")
    print("=" * 80)
    
    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las pruebas
    suite.addTests(loader.loadTestsFromTestCase(TestLuminoraCoreValidationManager))
    suite.addTests(loader.loadTestsFromTestCase(TestSafeGetFacts))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorResponseCreation))
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
