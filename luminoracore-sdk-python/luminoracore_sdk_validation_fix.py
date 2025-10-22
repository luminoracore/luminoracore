"""
SOLUCIÓN PARA PROBLEMA #2: FALTA DE VALIDACIÓN EN get_facts()

Este archivo resuelve el problema crítico donde el método get_facts() en TODAS las capas 
(Client → MemoryManager → Storage) no tiene validación ni manejo de errores adecuado.

PROBLEMA ORIGINAL:
- get_facts() no valida que storage_v11 esté correctamente inicializado
- No hay try-catch en ninguna capa para capturar excepciones
- No hay logs de error cuando algo falla
- Se devuelve [] silenciosamente sin indicar QUÉ falló

FLUJO PROBLEMÁTICO ACTUAL:
1. ClientV11.get_facts() - Solo warning, devuelve []
2. MemoryManagerV11.get_facts() - Solo warning, devuelve []
3. FlexibleDynamoDBStorageV11.get_facts() - Sin try-catch, excepción se propaga

SOLUCIÓN:
- Validación robusta en todas las capas
- Manejo de errores con logging detallado
- Respuestas informativas en lugar de [] silencioso
- Validación de configuración de AWS y DynamoDB
"""

import logging
import asyncio
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
import traceback


logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Excepción personalizada para errores de validación."""
    pass


class StorageConfigurationError(Exception):
    """Excepción para errores de configuración de storage."""
    pass


class LuminoraCoreValidationManager:
    """
    Manager de validación para LuminoraCore SDK que proporciona validación robusta
    y manejo de errores para todas las operaciones del framework.
    """
    
    def __init__(self):
        self.validation_enabled = True
        self.debug_mode = False
    
    def enable_debug_mode(self, enabled: bool = True):
        """Habilitar modo debug para logging detallado."""
        self.debug_mode = enabled
        if enabled:
            logger.info("Modo debug habilitado para validación")
    
    def validate_storage_configuration(self, storage_v11) -> bool:
        """
        Validar que la configuración de storage esté correcta.
        
        Args:
            storage_v11: Instancia de storage v1.1
            
        Returns:
            True si la configuración es válida
            
        Raises:
            StorageConfigurationError: Si la configuración es inválida
        """
        if not self.validation_enabled:
            return True
        
        if not storage_v11:
            error_msg = "Storage v1.1 no está configurado"
            logger.error(error_msg)
            raise StorageConfigurationError(error_msg)
        
        # Validar que sea una instancia de storage válida
        if not hasattr(storage_v11, 'get_facts'):
            error_msg = f"Storage v1.1 no tiene método get_facts(): {type(storage_v11)}"
            logger.error(error_msg)
            raise StorageConfigurationError(error_msg)
        
        # Validar configuración específica para DynamoDB
        if hasattr(storage_v11, 'table_name'):
            if not storage_v11.table_name:
                error_msg = "DynamoDB table_name no está configurado"
                logger.error(error_msg)
                raise StorageConfigurationError(error_msg)
            
            if not hasattr(storage_v11, 'table') or not storage_v11.table:
                error_msg = "DynamoDB table no está inicializado correctamente"
                logger.error(error_msg)
                raise StorageConfigurationError(error_msg)
        
        if self.debug_mode:
            logger.debug(f"Configuración de storage válida: {type(storage_v11)}")
        
        return True
    
    def validate_user_id(self, user_id: str) -> bool:
        """
        Validar que el user_id sea válido.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            True si el user_id es válido
            
        Raises:
            ValidationError: Si el user_id es inválido
        """
        if not self.validation_enabled:
            return True
        
        if not user_id:
            error_msg = "user_id no puede estar vacío"
            logger.error(error_msg)
            raise ValidationError(error_msg)
        
        if not isinstance(user_id, str):
            error_msg = f"user_id debe ser string, recibido: {type(user_id)}"
            logger.error(error_msg)
            raise ValidationError(error_msg)
        
        if len(user_id.strip()) == 0:
            error_msg = "user_id no puede ser solo espacios en blanco"
            logger.error(error_msg)
            raise ValidationError(error_msg)
        
        if self.debug_mode:
            logger.debug(f"user_id válido: {user_id}")
        
        return True
    
    def validate_category(self, category: Optional[str]) -> bool:
        """
        Validar que la categoría sea válida si se proporciona.
        
        Args:
            category: Categoría opcional
            
        Returns:
            True si la categoría es válida
            
        Raises:
            ValidationError: Si la categoría es inválida
        """
        if not self.validation_enabled:
            return True
        
        if category is not None:
            if not isinstance(category, str):
                error_msg = f"category debe ser string o None, recibido: {type(category)}"
                logger.error(error_msg)
                raise ValidationError(error_msg)
            
            if len(category.strip()) == 0:
                error_msg = "category no puede ser solo espacios en blanco"
                logger.error(error_msg)
                raise ValidationError(error_msg)
        
        if self.debug_mode and category:
            logger.debug(f"category válida: {category}")
        
        return True
    
    async def safe_get_facts(
        self,
        storage_v11,
        user_id: str,
        category: Optional[str] = None,
        operation_context: str = "get_facts"
    ) -> Dict[str, Any]:
        """
        Versión segura de get_facts() con validación completa y manejo de errores.
        
        Args:
            storage_v11: Instancia de storage v1.1
            user_id: ID del usuario
            category: Categoría opcional
            operation_context: Contexto de la operación para logging
            
        Returns:
            Dict con resultado de la operación:
            {
                "success": bool,
                "data": List[Dict] | None,
                "error": str | None,
                "error_type": str | None,
                "validation_errors": List[str],
                "debug_info": Dict | None
            }
        """
        start_time = datetime.now()
        debug_info = {}
        validation_errors = []
        
        try:
            # 1. VALIDACIONES PREVIAS
            logger.info(f"{operation_context}: Iniciando validaciones para user_id={user_id}, category={category}")
            
            # Validar configuración de storage
            try:
                self.validate_storage_configuration(storage_v11)
            except StorageConfigurationError as e:
                validation_errors.append(str(e))
                return {
                    "success": False,
                    "data": None,
                    "error": str(e),
                    "error_type": "StorageConfigurationError",
                    "validation_errors": validation_errors,
                    "debug_info": debug_info
                }
            
            # Validar user_id
            try:
                self.validate_user_id(user_id)
            except ValidationError as e:
                validation_errors.append(str(e))
                return {
                    "success": False,
                    "data": None,
                    "error": str(e),
                    "error_type": "ValidationError",
                    "validation_errors": validation_errors,
                    "debug_info": debug_info
                }
            
            # Validar category
            try:
                self.validate_category(category)
            except ValidationError as e:
                validation_errors.append(str(e))
                return {
                    "success": False,
                    "data": None,
                    "error": str(e),
                    "error_type": "ValidationError",
                    "validation_errors": validation_errors,
                    "debug_info": debug_info
                }
            
            # 2. EJECUTAR OPERACIÓN CON MANEJO DE ERRORES
            logger.info(f"{operation_context}: Validaciones pasadas, ejecutando get_facts()")
            
            # Agregar información de debug
            if self.debug_mode:
                debug_info.update({
                    "storage_type": type(storage_v11).__name__,
                    "table_name": getattr(storage_v11, 'table_name', 'N/A'),
                    "region_name": getattr(storage_v11, 'region_name', 'N/A'),
                    "user_id": user_id,
                    "category": category,
                    "start_time": start_time.isoformat()
                })
            
            # Ejecutar get_facts con timeout
            try:
                facts = await asyncio.wait_for(
                    storage_v11.get_facts(user_id, category=category),
                    timeout=30.0  # 30 segundos timeout
                )
                
                if self.debug_mode:
                    debug_info["facts_count"] = len(facts) if facts else 0
                    debug_info["execution_time_ms"] = (datetime.now() - start_time).total_seconds() * 1000
                
                logger.info(f"{operation_context}: get_facts() completado exitosamente, {len(facts) if facts else 0} facts encontrados")
                
                return {
                    "success": True,
                    "data": facts or [],
                    "error": None,
                    "error_type": None,
                    "validation_errors": validation_errors,
                    "debug_info": debug_info
                }
                
            except asyncio.TimeoutError:
                error_msg = f"{operation_context}: Timeout al ejecutar get_facts() (30s)"
                logger.error(error_msg)
                return {
                    "success": False,
                    "data": None,
                    "error": error_msg,
                    "error_type": "TimeoutError",
                    "validation_errors": validation_errors,
                    "debug_info": debug_info
                }
            
        except Exception as e:
            # Capturar cualquier otra excepción
            error_msg = f"{operation_context}: Error inesperado en get_facts(): {str(e)}"
            logger.error(error_msg)
            logger.error(f"{operation_context}: Traceback: {traceback.format_exc()}")
            
            if self.debug_mode:
                debug_info["exception_type"] = type(e).__name__
                debug_info["exception_message"] = str(e)
                debug_info["traceback"] = traceback.format_exc()
                debug_info["execution_time_ms"] = (datetime.now() - start_time).total_seconds() * 1000
            
            return {
                "success": False,
                "data": None,
                "error": error_msg,
                "error_type": type(e).__name__,
                "validation_errors": validation_errors,
                "debug_info": debug_info
            }
    
    def create_error_response(
        self,
        error_message: str,
        error_type: str,
        validation_errors: List[str] = None,
        debug_info: Dict = None
    ) -> Dict[str, Any]:
        """
        Crear respuesta de error estandarizada.
        
        Args:
            error_message: Mensaje de error
            error_type: Tipo de error
            validation_errors: Lista de errores de validación
            debug_info: Información de debug
            
        Returns:
            Dict con respuesta de error estandarizada
        """
        return {
            "success": False,
            "data": None,
            "error": error_message,
            "error_type": error_type,
            "validation_errors": validation_errors or [],
            "debug_info": debug_info or {}
        }


# Instancia global del manager de validación
validation_manager = LuminoraCoreValidationManager()


# Decorador para métodos que necesitan validación
def validate_storage_operation(operation_name: str = "storage_operation"):
    """
    Decorador para métodos de storage que necesitan validación.
    
    Args:
        operation_name: Nombre de la operación para logging
    """
    def decorator(func):
        async def wrapper(self, *args, **kwargs):
            # Extraer user_id de los argumentos si está disponible
            user_id = None
            if len(args) > 0:
                user_id = args[0]
            elif 'user_id' in kwargs:
                user_id = kwargs['user_id']
            
            logger.info(f"{operation_name}: Iniciando operación para user_id={user_id}")
            
            try:
                # Validar configuración de storage
                validation_manager.validate_storage_configuration(self)
                
                # Ejecutar función original
                result = await func(self, *args, **kwargs)
                
                logger.info(f"{operation_name}: Operación completada exitosamente")
                return result
                
            except (StorageConfigurationError, ValidationError) as e:
                logger.error(f"{operation_name}: Error de validación: {e}")
                return validation_manager.create_error_response(
                    str(e),
                    type(e).__name__,
                    operation_context=operation_name
                )
            
            except Exception as e:
                logger.error(f"{operation_name}: Error inesperado: {e}")
                logger.error(f"{operation_name}: Traceback: {traceback.format_exc()}")
                return validation_manager.create_error_response(
                    f"Error inesperado: {str(e)}",
                    type(e).__name__,
                    operation_context=operation_name
                )
        
        return wrapper
    return decorator


# Función de conveniencia para configurar validación
def configure_validation(debug_mode: bool = False, validation_enabled: bool = True):
    """
    Configurar el sistema de validación.
    
    Args:
        debug_mode: Habilitar modo debug
        validation_enabled: Habilitar validaciones
    """
    validation_manager.enable_debug_mode(debug_mode)
    validation_manager.validation_enabled = validation_enabled
    
    logger.info(f"Validación configurada - Debug: {debug_mode}, Validaciones: {validation_enabled}")


# Ejemplo de uso
if __name__ == "__main__":
    print("=== TESTING LUMINORACORE VALIDATION FIX ===")
    
    # Configurar logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Configurar validación
    configure_validation(debug_mode=True)
    
    # Test de validaciones
    validation_manager.validate_user_id("test_user")
    validation_manager.validate_category("test_category")
    
    print("=== VALIDATION TEST COMPLETED ===")
