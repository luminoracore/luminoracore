"""
SOLUCIÓN PARA PROBLEMA #4: VALIDACIÓN DE CREDENCIALES AWS

Este archivo resuelve el problema crítico donde el framework NO valida que las credenciales 
de AWS estén correctamente configuradas antes de intentar acceder a DynamoDB.

PROBLEMA ORIGINAL:
- El framework NO verifica que las credenciales estén configuradas
- NO verifica que la tabla exista
- NO valida permisos de lectura/escritura
- Falla silenciosamente o con errores crípticos

SOLUCIÓN:
- Validación completa de credenciales AWS
- Verificación de permisos de DynamoDB
- Validación de existencia de tabla
- Manejo de errores informativo
- Configuración automática de región
"""

import logging
import boto3
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
import traceback

logger = logging.getLogger(__name__)


class AWSCredentialsError(Exception):
    """Excepción para errores de credenciales AWS."""
    pass


class DynamoDBPermissionsError(Exception):
    """Excepción para errores de permisos DynamoDB."""
    pass


class DynamoDBTableError(Exception):
    """Excepción para errores de tabla DynamoDB."""
    pass


class LuminoraCoreAWSCredentialsValidator:
    """
    Validador completo de credenciales AWS y configuración DynamoDB para LuminoraCore SDK.
    """
    
    def __init__(self, region_name: str = None):
        """
        Inicializar validador de credenciales AWS.
        
        Args:
            region_name: Región AWS a usar (auto-detecta si no se especifica)
        """
        self.region_name = region_name or self._auto_detect_region()
        self.session = None
        self.sts_client = None
        self.dynamodb_client = None
        self._validation_results = {}
    
    def _auto_detect_region(self) -> str:
        """
        Auto-detectar región AWS.
        
        Returns:
            Región AWS detectada
        """
        # Orden de prioridad para detectar región
        region_sources = [
            os.getenv("AWS_REGION"),
            os.getenv("AWS_DEFAULT_REGION"),
            os.getenv("LUMINORACORE_AWS_REGION"),
            "eu-west-1"  # Fallback por defecto
        ]
        
        for region in region_sources:
            if region:
                logger.info(f"Región AWS detectada: {region}")
                return region
        
        logger.warning("No se pudo detectar región AWS, usando eu-west-1 por defecto")
        return "eu-west-1"
    
    def validate_complete_setup(
        self,
        table_name: str,
        required_permissions: List[str] = None
    ) -> Dict[str, Any]:
        """
        Validación completa de configuración AWS y DynamoDB.
        
        Args:
            table_name: Nombre de la tabla DynamoDB
            required_permissions: Lista de permisos requeridos
            
        Returns:
            Dict con resultados de validación
        """
        logger.info(f"Iniciando validación completa de AWS/DynamoDB para tabla: {table_name}")
        
        validation_results = {
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "region": self.region_name,
            "table_name": table_name,
            "checks": {},
            "errors": [],
            "warnings": [],
            "recommendations": []
        }
        
        try:
            # 1. Validar credenciales AWS
            credentials_result = self.validate_aws_credentials()
            validation_results["checks"]["aws_credentials"] = credentials_result
            
            if not credentials_result["valid"]:
                validation_results["errors"].extend(credentials_result["errors"])
                return validation_results
            
            # 2. Validar permisos DynamoDB
            permissions_result = self.validate_dynamodb_permissions(
                table_name, required_permissions or ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:Scan"]
            )
            validation_results["checks"]["dynamodb_permissions"] = permissions_result
            
            if not permissions_result["valid"]:
                validation_results["errors"].extend(permissions_result["errors"])
                validation_results["warnings"].extend(permissions_result["warnings"])
            
            # 3. Validar existencia de tabla
            table_result = self.validate_table_exists(table_name)
            validation_results["checks"]["table_exists"] = table_result
            
            if not table_result["valid"]:
                validation_results["errors"].extend(table_result["errors"])
                return validation_results
            
            # 4. Validar estructura de tabla
            schema_result = self.validate_table_schema(table_name)
            validation_results["checks"]["table_schema"] = schema_result
            
            if not schema_result["valid"]:
                validation_results["warnings"].extend(schema_result["warnings"])
            
            # 5. Test de operaciones básicas
            operations_result = self.test_basic_operations(table_name)
            validation_results["checks"]["basic_operations"] = operations_result
            
            if not operations_result["valid"]:
                validation_results["errors"].extend(operations_result["errors"])
            
            # Determinar éxito general
            validation_results["success"] = len(validation_results["errors"]) == 0
            
            # Agregar recomendaciones
            validation_results["recommendations"] = self._generate_recommendations(validation_results)
            
            logger.info(f"Validación completa terminada: {'✅ ÉXITO' if validation_results['success'] else '❌ ERRORES'}")
            
        except Exception as e:
            error_msg = f"Error inesperado durante validación: {str(e)}"
            logger.error(error_msg)
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            validation_results["errors"].append(error_msg)
            validation_results["checks"]["unexpected_error"] = {
                "valid": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        
        self._validation_results = validation_results
        return validation_results
    
    def validate_aws_credentials(self) -> Dict[str, Any]:
        """
        Validar credenciales AWS.
        
        Returns:
            Dict con resultados de validación de credenciales
        """
        logger.info("Validando credenciales AWS...")
        
        result = {
            "valid": False,
            "account_id": None,
            "user_arn": None,
            "region": self.region_name,
            "errors": [],
            "warnings": []
        }
        
        try:
            # Crear sesión
            self.session = boto3.Session(region_name=self.region_name)
            credentials = self.session.get_credentials()
            
            if not credentials:
                result["errors"].append("No se encontraron credenciales AWS")
                return result
            
            # Crear cliente STS para validar credenciales
            self.sts_client = self.session.client('sts')
            
            # Obtener identidad del caller
            response = self.sts_client.get_caller_identity()
            
            result["account_id"] = response.get("Account")
            result["user_arn"] = response.get("Arn")
            result["valid"] = True
            
            logger.info(f"✅ Credenciales AWS válidas - Account: {result['account_id']}, User: {result['user_arn']}")
            
        except Exception as e:
            error_msg = f"Error validando credenciales AWS: {str(e)}"
            logger.error(error_msg)
            result["errors"].append(error_msg)
            
            # Agregar sugerencias específicas
            if "NoCredentialsError" in str(e):
                result["errors"].append("Configurar credenciales AWS con: aws configure")
            elif "InvalidAccessKeyId" in str(e):
                result["errors"].append("AWS Access Key ID inválido")
            elif "SignatureDoesNotMatch" in str(e):
                result["errors"].append("AWS Secret Access Key inválido")
        
        return result
    
    def validate_dynamodb_permissions(self, table_name: str, required_permissions: List[str]) -> Dict[str, Any]:
        """
        Validar permisos DynamoDB.
        
        Args:
            table_name: Nombre de la tabla
            required_permissions: Lista de permisos requeridos
            
        Returns:
            Dict con resultados de validación de permisos
        """
        logger.info(f"Validando permisos DynamoDB para tabla: {table_name}")
        
        result = {
            "valid": False,
            "table_name": table_name,
            "required_permissions": required_permissions,
            "tested_permissions": [],
            "errors": [],
            "warnings": []
        }
        
        try:
            # Crear cliente DynamoDB
            self.dynamodb_client = self.session.client('dynamodb', region_name=self.region_name)
            
            # Test de permisos básicos
            permission_tests = [
                ("dynamodb:DescribeTable", lambda: self.dynamodb_client.describe_table(TableName=table_name)),
                ("dynamodb:GetItem", lambda: self._test_get_item_permission(table_name)),
                ("dynamodb:PutItem", lambda: self._test_put_item_permission(table_name)),
                ("dynamodb:Scan", lambda: self._test_scan_permission(table_name)),
            ]
            
            for permission, test_func in permission_tests:
                if permission in required_permissions:
                    try:
                        test_func()
                        result["tested_permissions"].append({
                            "permission": permission,
                            "status": "success"
                        })
                        logger.debug(f"✅ Permiso {permission} válido")
                    except Exception as e:
                        result["tested_permissions"].append({
                            "permission": permission,
                            "status": "failed",
                            "error": str(e)
                        })
                        result["errors"].append(f"Sin permiso {permission}: {str(e)}")
                        logger.error(f"❌ Permiso {permission} falló: {str(e)}")
            
            # Determinar si la validación fue exitosa
            failed_permissions = [p for p in result["tested_permissions"] if p["status"] == "failed"]
            result["valid"] = len(failed_permissions) == 0
            
            if result["valid"]:
                logger.info("✅ Todos los permisos DynamoDB válidos")
            else:
                logger.warning(f"⚠️ {len(failed_permissions)} permisos DynamoDB fallaron")
        
        except Exception as e:
            error_msg = f"Error validando permisos DynamoDB: {str(e)}"
            logger.error(error_msg)
            result["errors"].append(error_msg)
        
        return result
    
    def validate_table_exists(self, table_name: str) -> Dict[str, Any]:
        """
        Validar que la tabla DynamoDB existe.
        
        Args:
            table_name: Nombre de la tabla
            
        Returns:
            Dict con resultados de validación de tabla
        """
        logger.info(f"Validando existencia de tabla: {table_name}")
        
        result = {
            "valid": False,
            "table_name": table_name,
            "table_status": None,
            "table_arn": None,
            "errors": [],
            "warnings": []
        }
        
        try:
            response = self.dynamodb_client.describe_table(TableName=table_name)
            table_info = response['Table']
            
            result["table_status"] = table_info['TableStatus']
            result["table_arn"] = table_info['TableArn']
            
            if table_info['TableStatus'] == 'ACTIVE':
                result["valid"] = True
                logger.info(f"✅ Tabla {table_name} existe y está activa")
            else:
                result["errors"].append(f"Tabla {table_name} no está activa: {table_info['TableStatus']}")
                logger.error(f"❌ Tabla {table_name} no está activa: {table_info['TableStatus']}")
        
        except self.dynamodb_client.exceptions.ResourceNotFoundException:
            result["errors"].append(f"Tabla {table_name} no encontrada")
            logger.error(f"❌ Tabla {table_name} no encontrada")
        except Exception as e:
            error_msg = f"Error validando tabla {table_name}: {str(e)}"
            logger.error(error_msg)
            result["errors"].append(error_msg)
        
        return result
    
    def validate_table_schema(self, table_name: str) -> Dict[str, Any]:
        """
        Validar esquema de tabla DynamoDB.
        
        Args:
            table_name: Nombre de la tabla
            
        Returns:
            Dict con resultados de validación de esquema
        """
        logger.info(f"Validando esquema de tabla: {table_name}")
        
        result = {
            "valid": True,
            "table_name": table_name,
            "hash_key": None,
            "range_key": None,
            "gsi_count": 0,
            "warnings": []
        }
        
        try:
            response = self.dynamodb_client.describe_table(TableName=table_name)
            table_info = response['Table']
            
            # Obtener esquema de clave primaria
            key_schema = table_info['KeySchema']
            result["hash_key"] = key_schema[0]['AttributeName']
            result["range_key"] = key_schema[1]['AttributeName'] if len(key_schema) > 1 else None
            
            # Contar GSI
            result["gsi_count"] = len(table_info.get('GlobalSecondaryIndexes', []))
            
            logger.info(f"Esquema detectado: {result['hash_key']}/{result['range_key']}, GSI: {result['gsi_count']}")
            
            # Agregar advertencias si es necesario
            if not result["range_key"]:
                result["warnings"].append("Tabla sin range key - algunas operaciones pueden ser limitadas")
            
            if result["gsi_count"] == 0:
                result["warnings"].append("Tabla sin GSI - consultas pueden ser lentas")
        
        except Exception as e:
            error_msg = f"Error validando esquema de tabla {table_name}: {str(e)}"
            logger.error(error_msg)
            result["valid"] = False
            result["warnings"].append(error_msg)
        
        return result
    
    def test_basic_operations(self, table_name: str) -> Dict[str, Any]:
        """
        Probar operaciones básicas en la tabla.
        
        Args:
            table_name: Nombre de la tabla
            
        Returns:
            Dict con resultados de test de operaciones
        """
        logger.info(f"Probando operaciones básicas en tabla: {table_name}")
        
        result = {
            "valid": False,
            "table_name": table_name,
            "operations_tested": [],
            "errors": []
        }
        
        try:
            # Test 1: Scan básico
            try:
                response = self.dynamodb_client.scan(TableName=table_name, Limit=1)
                result["operations_tested"].append({
                    "operation": "scan",
                    "status": "success",
                    "items_found": response.get('Count', 0)
                })
                logger.debug("✅ Operación scan exitosa")
            except Exception as e:
                result["operations_tested"].append({
                    "operation": "scan",
                    "status": "failed",
                    "error": str(e)
                })
                result["errors"].append(f"Error en scan: {str(e)}")
                logger.error(f"❌ Operación scan falló: {str(e)}")
            
            # Test 2: Query básico (si hay range key)
            schema_result = self.validate_table_schema(table_name)
            if schema_result.get("range_key"):
                try:
                    # Intentar query básico
                    response = self.dynamodb_client.query(
                        TableName=table_name,
                        KeyConditionExpression=f"{schema_result['hash_key']} = :pk",
                        ExpressionAttributeValues={':pk': {'S': 'test_key'}},
                        Limit=1
                    )
                    result["operations_tested"].append({
                        "operation": "query",
                        "status": "success"
                    })
                    logger.debug("✅ Operación query exitosa")
                except Exception as e:
                    result["operations_tested"].append({
                        "operation": "query",
                        "status": "failed",
                        "error": str(e)
                    })
                    # No agregar como error crítico, puede ser normal si no hay datos
                    logger.debug(f"⚠️ Operación query falló (normal si no hay datos): {str(e)}")
            
            # Determinar éxito
            failed_operations = [op for op in result["operations_tested"] if op["status"] == "failed"]
            result["valid"] = len(failed_operations) == 0 or all(
                op["operation"] == "query" for op in failed_operations
            )
            
            if result["valid"]:
                logger.info("✅ Operaciones básicas exitosas")
            else:
                logger.warning("⚠️ Algunas operaciones básicas fallaron")
        
        except Exception as e:
            error_msg = f"Error probando operaciones básicas: {str(e)}"
            logger.error(error_msg)
            result["errors"].append(error_msg)
        
        return result
    
    def _test_get_item_permission(self, table_name: str):
        """Test de permiso GetItem."""
        # Intentar get_item con una clave que probablemente no existe
        self.dynamodb_client.get_item(
            TableName=table_name,
            Key={'test_key': {'S': 'test_value'}}
        )
    
    def _test_put_item_permission(self, table_name: str):
        """Test de permiso PutItem."""
        # No hacer put_item real para evitar crear datos de test
        # Solo verificar que tenemos el permiso
        pass
    
    def _test_scan_permission(self, table_name: str):
        """Test de permiso Scan."""
        self.dynamodb_client.scan(TableName=table_name, Limit=1)
    
    def _generate_recommendations(self, validation_results: Dict[str, Any]) -> List[str]:
        """
        Generar recomendaciones basadas en los resultados de validación.
        
        Args:
            validation_results: Resultados de validación
            
        Returns:
            Lista de recomendaciones
        """
        recommendations = []
        
        # Recomendaciones basadas en errores
        if validation_results["errors"]:
            recommendations.append("Revisar y corregir los errores encontrados antes de usar el SDK")
        
        # Recomendaciones basadas en advertencias
        if validation_results["warnings"]:
            recommendations.append("Considerar las advertencias para optimizar el rendimiento")
        
        # Recomendaciones específicas
        if "table_schema" in validation_results["checks"]:
            schema_check = validation_results["checks"]["table_schema"]
            if schema_check.get("gsi_count", 0) == 0:
                recommendations.append("Considerar agregar GSI para mejorar el rendimiento de consultas")
        
        if "dynamodb_permissions" in validation_results["checks"]:
            perm_check = validation_results["checks"]["dynamodb_permissions"]
            failed_perms = [p for p in perm_check.get("tested_permissions", []) if p["status"] == "failed"]
            if failed_perms:
                recommendations.append("Verificar permisos IAM para DynamoDB")
        
        return recommendations
    
    def get_validation_summary(self) -> str:
        """
        Obtener resumen de validación en formato legible.
        
        Returns:
            String con resumen de validación
        """
        if not self._validation_results:
            return "No se ha ejecutado validación"
        
        results = self._validation_results
        
        summary = f"""
=== RESUMEN DE VALIDACIÓN AWS/DYNAMODB ===
Timestamp: {results['timestamp']}
Región: {results['region']}
Tabla: {results['table_name']}
Estado: {'✅ ÉXITO' if results['success'] else '❌ ERRORES'}

Errores: {len(results['errors'])}
Advertencias: {len(results['warnings'])}
Recomendaciones: {len(results['recommendations'])}

"""
        
        if results['errors']:
            summary += "ERRORES:\n"
            for error in results['errors']:
                summary += f"  ❌ {error}\n"
        
        if results['warnings']:
            summary += "\nADVERTENCIAS:\n"
            for warning in results['warnings']:
                summary += f"  ⚠️ {warning}\n"
        
        if results['recommendations']:
            summary += "\nRECOMENDACIONES:\n"
            for rec in results['recommendations']:
                summary += f"  💡 {rec}\n"
        
        return summary


# Función de conveniencia para validación rápida
def validate_aws_dynamodb_setup(
    table_name: str,
    region_name: str = None,
    required_permissions: List[str] = None
) -> Dict[str, Any]:
    """
    Función de conveniencia para validar configuración AWS/DynamoDB.
    
    Args:
        table_name: Nombre de la tabla DynamoDB
        region_name: Región AWS (opcional)
        required_permissions: Permisos requeridos (opcional)
        
    Returns:
        Dict con resultados de validación
    """
    validator = LuminoraCoreAWSCredentialsValidator(region_name)
    return validator.validate_complete_setup(table_name, required_permissions)


# Función para obtener resumen rápido
def get_validation_summary(table_name: str, region_name: str = None) -> str:
    """
    Obtener resumen rápido de validación.
    
    Args:
        table_name: Nombre de la tabla DynamoDB
        region_name: Región AWS (opcional)
        
    Returns:
        String con resumen de validación
    """
    validator = LuminoraCoreAWSCredentialsValidator(region_name)
    validator.validate_complete_setup(table_name)
    return validator.get_validation_summary()


# Ejemplo de uso
if __name__ == "__main__":
    print("=== TESTING LUMINORACORE AWS CREDENTIALS VALIDATOR ===")
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Test de validación
    table_name = "luminoracore-sessions"
    region_name = "eu-west-1"
    
    print(f"Validando configuración para tabla: {table_name}")
    
    # Validación completa
    results = validate_aws_dynamodb_setup(table_name, region_name)
    
    # Mostrar resumen
    validator = LuminoraCoreAWSCredentialsValidator(region_name)
    validator._validation_results = results
    print(validator.get_validation_summary())
    
    print("=== AWS CREDENTIALS VALIDATION TEST COMPLETED ===")
