"""
MÉTODOS MEJORADOS PARA LUMINORACORE SDK

Este archivo contiene las versiones mejoradas de los métodos problemáticos del framework,
con validación robusta y manejo de errores adecuado.

INCLUYE:
- get_facts() mejorado para ClientV11
- get_facts() mejorado para MemoryManagerV11  
- get_facts() mejorado para FlexibleDynamoDBStorageV11
- Validación de credenciales AWS
- Manejo de errores con logging detallado
"""

import logging
import asyncio
import boto3
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
import traceback

# Importar el sistema de validación
from luminoracore_sdk_validation_fix import validation_manager, ValidationError, StorageConfigurationError

logger = logging.getLogger(__name__)


class ImprovedClientV11:
    """
    Versión mejorada de ClientV11 con validación robusta.
    """
    
    def __init__(self, base_client, storage_v11=None, memory_v11=None):
        self.base_client = base_client
        self.storage_v11 = storage_v11
        self.memory_v11 = memory_v11
    
    async def get_facts(
        self,
        user_id: str,
        category: Optional[str] = None
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Versión mejorada de get_facts() con validación completa y manejo de errores.
        
        Args:
            user_id: ID del usuario
            category: Categoría opcional para filtrar
            
        Returns:
            Lista de facts si es exitoso, o Dict con información de error
        """
        operation_context = "ClientV11.get_facts"
        logger.info(f"{operation_context}: Iniciando para user_id={user_id}, category={category}")
        
        try:
            # 1. VALIDACIÓN DE MEMORY_V11
            if not self.memory_v11:
                error_msg = f"{operation_context}: Memory v1.1 no está configurado"
                logger.error(error_msg)
                return validation_manager.create_error_response(
                    error_msg,
                    "MemoryNotConfiguredError",
                    operation_context=operation_context
                )
            
            # 2. VALIDACIÓN DE STORAGE_V11
            if not self.storage_v11:
                error_msg = f"{operation_context}: Storage v1.1 no está configurado"
                logger.error(error_msg)
                return validation_manager.create_error_response(
                    error_msg,
                    "StorageNotConfiguredError",
                    operation_context=operation_context
                )
            
            # 3. USAR VALIDACIÓN SEGURA
            options = {"category": category} if category else {}
            
            logger.info(f"{operation_context}: Delegando a memory_v11.get_facts()")
            result = await self.memory_v11.get_facts(user_id, options=options)
            
            # Verificar si el resultado es un error
            if isinstance(result, dict) and not result.get("success", True):
                logger.error(f"{operation_context}: Error en memory_v11.get_facts(): {result.get('error')}")
                return result
            
            logger.info(f"{operation_context}: Completado exitosamente, {len(result)} facts encontrados")
            return result
            
        except Exception as e:
            error_msg = f"{operation_context}: Error inesperado: {str(e)}"
            logger.error(error_msg)
            logger.error(f"{operation_context}: Traceback: {traceback.format_exc()}")
            
            return validation_manager.create_error_response(
                error_msg,
                type(e).__name__,
                operation_context=operation_context
            )


class ImprovedMemoryManagerV11:
    """
    Versión mejorada de MemoryManagerV11 con validación robusta.
    """
    
    def __init__(self, storage_v11=None, vector_store=None):
        self.storage = storage_v11
        self.vector_store = vector_store
    
    async def get_facts(
        self,
        user_id: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Versión mejorada de get_facts() con validación completa y manejo de errores.
        
        Args:
            user_id: ID del usuario
            options: Opciones de consulta (category, max_results, etc.)
            
        Returns:
            Lista de facts si es exitoso, o Dict con información de error
        """
        operation_context = "MemoryManagerV11.get_facts"
        logger.info(f"{operation_context}: Iniciando para user_id={user_id}, options={options}")
        
        try:
            # 1. VALIDACIÓN DE STORAGE
            if not self.storage:
                error_msg = f"{operation_context}: Storage no está configurado"
                logger.error(error_msg)
                return validation_manager.create_error_response(
                    error_msg,
                    "StorageNotConfiguredError",
                    operation_context=operation_context
                )
            
            # 2. VALIDACIÓN DE CONFIGURACIÓN DE STORAGE
            try:
                validation_manager.validate_storage_configuration(self.storage)
            except StorageConfigurationError as e:
                error_msg = f"{operation_context}: Configuración de storage inválida: {str(e)}"
                logger.error(error_msg)
                return validation_manager.create_error_response(
                    error_msg,
                    "StorageConfigurationError",
                    operation_context=operation_context
                )
            
            # 3. VALIDACIÓN DE USER_ID
            try:
                validation_manager.validate_user_id(user_id)
            except ValidationError as e:
                error_msg = f"{operation_context}: user_id inválido: {str(e)}"
                logger.error(error_msg)
                return validation_manager.create_error_response(
                    error_msg,
                    "ValidationError",
                    operation_context=operation_context
                )
            
            # 4. EXTRAER CATEGORÍA DE OPCIONES
            category = None
            if options and isinstance(options, dict):
                category = options.get("category")
                
                # Validar categoría si se proporciona
                if category is not None:
                    try:
                        validation_manager.validate_category(category)
                    except ValidationError as e:
                        error_msg = f"{operation_context}: category inválida: {str(e)}"
                        logger.error(error_msg)
                        return validation_manager.create_error_response(
                            error_msg,
                            "ValidationError",
                            operation_context=operation_context
                        )
            
            # 5. USAR VALIDACIÓN SEGURA
            logger.info(f"{operation_context}: Delegando a storage.get_facts() con category={category}")
            result = await validation_manager.safe_get_facts(
                self.storage,
                user_id,
                category=category,
                operation_context=operation_context
            )
            
            # Verificar si hay errores
            if not result.get("success", True):
                logger.error(f"{operation_context}: Error en storage.get_facts(): {result.get('error')}")
                return result
            
            facts = result.get("data", [])
            
            # 6. APLICAR FILTROS ADICIONALES
            if options and isinstance(options, dict):
                # Filtrar facts inactivos si se especifica
                if not options.get("include_inactive", True):
                    facts = [f for f in facts if f.get("is_active", True)]
                
                # Limitar resultados si se especifica
                max_results = options.get("max_results")
                if max_results and max_results > 0:
                    facts = facts[:max_results]
            
            logger.info(f"{operation_context}: Completado exitosamente, {len(facts)} facts encontrados")
            return facts
            
        except Exception as e:
            error_msg = f"{operation_context}: Error inesperado: {str(e)}"
            logger.error(error_msg)
            logger.error(f"{operation_context}: Traceback: {traceback.format_exc()}")
            
            return validation_manager.create_error_response(
                error_msg,
                type(e).__name__,
                operation_context=operation_context
            )


class ImprovedFlexibleDynamoDBStorageV11:
    """
    Versión mejorada de FlexibleDynamoDBStorageV11 con validación robusta.
    """
    
    def __init__(self, table_name: str, region_name: str = None, **kwargs):
        self.table_name = table_name
        self.region_name = region_name or "us-east-1"
        self._initialized = False
        self._initialization_error = None
        
        # Intentar inicializar
        try:
            self._initialize_dynamodb()
        except Exception as e:
            self._initialization_error = str(e)
            logger.error(f"Error inicializando DynamoDB: {e}")
    
    def _initialize_dynamodb(self):
        """Inicializar DynamoDB con validación de credenciales."""
        logger.info(f"Inicializando DynamoDB: table={self.table_name}, region={self.region_name}")
        
        # 1. VALIDAR CREDENCIALES AWS
        self._validate_aws_credentials()
        
        # 2. INICIALIZAR DYNAMODB
        self.dynamodb = boto3.resource('dynamodb', region_name=self.region_name)
        self.table = self.dynamodb.Table(self.table_name)
        
        # 3. VALIDAR QUE LA TABLA EXISTE
        self._validate_table_exists()
        
        # 4. AUTO-DETECTAR ESQUEMA
        self._detect_table_schema()
        
        self._initialized = True
        logger.info(f"DynamoDB inicializado correctamente: {self.table_name}")
    
    def _validate_aws_credentials(self):
        """Validar que las credenciales AWS estén configuradas."""
        try:
            # Intentar obtener credenciales
            session = boto3.Session()
            credentials = session.get_credentials()
            
            if not credentials:
                raise StorageConfigurationError("Credenciales AWS no encontradas")
            
            # Verificar que las credenciales sean válidas
            sts = boto3.client('sts', region_name=self.region_name)
            sts.get_caller_identity()
            
            logger.info("Credenciales AWS validadas correctamente")
            
        except Exception as e:
            error_msg = f"Error validando credenciales AWS: {str(e)}"
            logger.error(error_msg)
            raise StorageConfigurationError(error_msg)
    
    def _validate_table_exists(self):
        """Validar que la tabla DynamoDB existe."""
        try:
            response = self.table.meta.client.describe_table(TableName=self.table_name)
            table_status = response['Table']['TableStatus']
            
            if table_status != 'ACTIVE':
                raise StorageConfigurationError(f"Tabla {self.table_name} no está activa: {table_status}")
            
            logger.info(f"Tabla {self.table_name} validada correctamente")
            
        except Exception as e:
            error_msg = f"Error validando tabla {self.table_name}: {str(e)}"
            logger.error(error_msg)
            raise StorageConfigurationError(error_msg)
    
    def _detect_table_schema(self):
        """Auto-detectar el esquema de la tabla."""
        try:
            response = self.table.meta.client.describe_table(TableName=self.table_name)
            table_info = response['Table']
            
            # Detectar esquema de clave primaria
            key_schema = table_info['KeySchema']
            self.detected_hash_key = key_schema[0]['AttributeName']
            self.detected_range_key = key_schema[1]['AttributeName'] if len(key_schema) > 1 else None
            
            # Usar esquema detectado
            self.hash_key_name = self.detected_hash_key
            self.range_key_name = self.detected_range_key
            
            logger.info(f"Esquema detectado: {self.hash_key_name}/{self.range_key_name}")
            
        except Exception as e:
            logger.error(f"Error detectando esquema de tabla: {e}")
            # Fallback a esquema común
            self.hash_key_name = 'session_id'
            self.range_key_name = 'timestamp'
            self.detected_hash_key = self.hash_key_name
            self.detected_range_key = self.range_key_name
    
    async def get_facts(
        self,
        user_id: str,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Versión mejorada de get_facts() con validación completa y manejo de errores.
        
        Args:
            Integración con el sistema de validación y manejo de errores robusto.
            
        Returns:
            Lista de facts o lanza excepción con detalles del error
        """
        operation_context = "FlexibleDynamoDBStorageV11.get_facts"
        
        # Verificar inicialización
        if not self._initialized:
            if self._initialization_error:
                error_msg = f"{operation_context}: Error de inicialización: {self._initialization_error}"
                logger.error(error_msg)
                raise StorageConfigurationError(error_msg)
            else:
                error_msg = f"{operation_context}: Storage no inicializado"
                logger.error(error_msg)
                raise StorageConfigurationError(error_msg)
        
        logger.info(f"{operation_context}: Iniciando para user_id={user_id}, category={category}")
        
        try:
            # 1. VALIDACIONES
            validation_manager.validate_user_id(user_id)
            if category:
                validation_manager.validate_category(category)
            
            # 2. EJECUTAR CONSULTA CON TIMEOUT
            facts = await asyncio.wait_for(
                self._execute_get_facts_query(user_id, category),
                timeout=30.0
            )
            
            logger.info(f"{operation_context}: Completado exitosamente, {len(facts)} facts encontrados")
            return facts
            
        except asyncio.TimeoutError:
            error_msg = f"{operation_context}: Timeout al ejecutar consulta DynamoDB (30s)"
            logger.error(error_msg)
            raise StorageConfigurationError(error_msg)
            
        except (ValidationError, StorageConfigurationError):
            # Re-lanzar errores de validación
            raise
            
        except Exception as e:
            error_msg = f"{operation_context}: Error inesperado: {str(e)}"
            logger.error(error_msg)
            logger.error(f"{operation_context}: Traceback: {traceback.format_exc()}")
            raise StorageConfigurationError(error_msg)
    
    async def _execute_get_facts_query(
        self,
        user_id: str,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Ejecutar la consulta DynamoDB para obtener facts.
        
        Args:
            user_id: ID del usuario
            category: Categoría opcional
            
        Returns:
            Lista de facts
        """
        try:
            # Usar SCAN para máxima compatibilidad
            if category:
                response = self.table.scan(
                    FilterExpression='user_id = :user_id AND #category = :category AND begins_with(#range_key, :fact_prefix)',
                    ExpressionAttributeNames={
                        '#range_key': self.range_key_name,
                        '#category': 'category'
                    },
                    ExpressionAttributeValues={
                        ':user_id': user_id,
                        ':category': category,
                        ':fact_prefix': 'FACT#'
                    }
                )
            else:
                response = self.table.scan(
                    FilterExpression='user_id = :user_id AND begins_with(#range_key, :fact_prefix)',
                    ExpressionAttributeNames={
                        '#range_key': self.range_key_name
                    },
                    ExpressionAttributeValues={
                        ':user_id': user_id,
                        ':fact_prefix': 'FACT#'
                    }
                )
            
            # Procesar resultados
            facts = []
            for item in response.get('Items', []):
                if item.get('key') and item.get('category'):
                    try:
                        fact_value = item['value']
                        if isinstance(fact_value, str):
                            try:
                                import json
                                fact_value = json.loads(fact_value)
                            except:
                                pass  # Mantener como string si no es JSON
                        
                        fact = {
                            'category': item['category'],
                            'key': item['key'],
                            'value': fact_value,
                            'confidence': float(item.get('confidence', 1.0)),
                            'created_at': item.get('created_at'),
                            'updated_at': item.get('updated_at')
                        }
                        
                        facts.append(fact)
                        
                    except Exception as e:
                        logger.warning(f"Error procesando fact item: {e}")
                        continue
            
            return facts
            
        except Exception as e:
            logger.error(f"Error ejecutando consulta DynamoDB: {e}")
            raise


# Función de conveniencia para crear instancias mejoradas
def create_improved_storage(table_name: str, region_name: str = None, **kwargs):
    """
    Crear instancia mejorada de FlexibleDynamoDBStorageV11.
    
    Args:
        table_name: Nombre de la tabla DynamoDB
        region_name: Región AWS
        **kwargs: Argumentos adicionales
        
    Returns:
        Instancia mejorada de storage
    """
    return ImprovedFlexibleDynamoDBStorageV11(table_name, region_name, **kwargs)


def create_improved_memory_manager(storage_v11=None, vector_store=None):
    """
    Crear instancia mejorada de MemoryManagerV11.
    
    Args:
        storage_v11: Instancia de storage
        vector_store: Instancia de vector store
        
    Returns:
        Instancia mejorada de memory manager
    """
    return ImprovedMemoryManagerV11(storage_v11, vector_store)


def create_improved_client_v11(base_client, storage_v11=None, memory_v11=None):
    """
    Crear instancia mejorada de ClientV11.
    
    Args:
        base_client: Cliente base de LuminoraCore
        storage_v11: Instancia de storage
        memory_v11: Instancia de memory manager
        
    Returns:
        Instancia mejorada de client v11
    """
    return ImprovedClientV11(base_client, storage_v11, memory_v11)


# Ejemplo de uso
if __name__ == "__main__":
    print("=== TESTING LUMINORACORE IMPROVED METHODS ===")
    
    # Configurar logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Configurar validación
    from luminoracore_sdk_validation_fix import configure_validation
    configure_validation(debug_mode=True)
    
    print("=== IMPROVED METHODS TEST COMPLETED ===")
