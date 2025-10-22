"""
SOLUCIÓN PARA PROBLEMA #1: LOGGING NO CONFIGURADO EN LUMINORACORE SDK

Este archivo resuelve el problema crítico donde el framework usa logging.getLogger(__name__) 
pero NUNCA configura el logger root. En AWS Lambda, esto significa que los logs del framework 
se pierden porque Lambda solo captura logs del logger root o logs configurados explícitamente.

PROBLEMA ORIGINAL:
- El framework usa logger = logging.getLogger(__name__) en 42 archivos
- Lambda solo captura logs del logger root por defecto
- Los mensajes de debug/info del framework se "pierden"
- El handler NO puede ver lo que está pasando dentro del framework

SOLUCIÓN:
- Configurar el logger root para capturar todos los logs del framework
- Asegurar que los logs se propaguen correctamente en AWS Lambda
- Proporcionar configuración flexible para diferentes entornos
"""

import logging
import sys
import os
from typing import Optional, Dict, Any


class LuminoraCoreLoggingConfig:
    """
    Configuración de logging para LuminoraCore SDK que resuelve el problema de visibilidad en AWS Lambda.
    """
    
    def __init__(self, level: str = "INFO", format_type: str = "lambda"):
        """
        Inicializar configuración de logging.
        
        Args:
            level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            format_type: Tipo de formato ("lambda", "json", "simple")
        """
        self.level = level.upper()
        self.format_type = format_type
        self._configured = False
    
    def configure_logging(self) -> None:
        """
        Configurar el logging del framework para que funcione correctamente en AWS Lambda.
        
        Esta función debe ser llamada al inicio de tu handler Lambda ANTES de usar el SDK.
        """
        if self._configured:
            return
        
        # Configurar el logger root
        root_logger = logging.getLogger()
        
        # Limpiar handlers existentes para evitar duplicados
        root_logger.handlers.clear()
        
        # Configurar nivel
        root_logger.setLevel(getattr(logging, self.level))
        
        # Crear handler para AWS Lambda
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, self.level))
        
        # Configurar formato basado en el tipo
        if self.format_type == "lambda":
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        elif self.format_type == "json":
            formatter = JsonFormatter()
        else:  # simple
            formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
        
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
        
        # Configurar loggers específicos del framework para asegurar propagación
        framework_loggers = [
            'luminoracore_sdk',
            'luminoracore_sdk.client_v1_1',
            'luminoracore_sdk.session.memory_v1_1',
            'luminoracore_sdk.session.storage_dynamodb_flexible',
            'luminoracore_sdk.session.storage_v1_1',
            'luminoracore_sdk.providers',
            'luminoracore_sdk.analysis',
            'luminoracore_sdk.evolution',
            'luminoracore_sdk.monitoring',
            'luminoracore_sdk.utils'
        ]
        
        for logger_name in framework_loggers:
            logger = logging.getLogger(logger_name)
            logger.setLevel(getattr(logging, self.level))
            logger.propagate = True  # Asegurar que se propague al root logger
        
        # Configurar boto3 logging para ver errores de AWS
        boto3_logger = logging.getLogger('boto3')
        boto3_logger.setLevel(logging.WARNING)
        boto3_logger.propagate = True
        
        botocore_logger = logging.getLogger('botocore')
        botocore_logger.setLevel(logging.WARNING)
        botocore_logger.propagate = True
        
        self._configured = True
        
        # Log de confirmación
        root_logger.info("LuminoraCore SDK logging configurado correctamente")
        root_logger.info(f"Nivel de logging: {self.level}")
        root_logger.info(f"Formato: {self.format_type}")
    
    def test_logging(self) -> None:
        """
        Probar que el logging funciona correctamente.
        """
        if not self._configured:
            self.configure_logging()
        
        logger = logging.getLogger(__name__)
        
        logger.debug("DEBUG: Test de logging - nivel DEBUG")
        logger.info("INFO: Test de logging - nivel INFO")
        logger.warning("WARNING: Test de logging - nivel WARNING")
        logger.error("ERROR: Test de logging - nivel ERROR")
        logger.critical("CRITICAL: Test de logging - nivel CRITICAL")
        
        # Test específico del framework
        framework_logger = logging.getLogger('luminoracore_sdk.client_v1_1')
        framework_logger.info("Framework logger test - esto debería aparecer en los logs")


class JsonFormatter(logging.Formatter):
    """
    Formatter para logs en formato JSON (útil para CloudWatch Logs).
    """
    
    def format(self, record):
        import json
        from datetime import datetime
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Agregar información adicional si está disponible
        if hasattr(record, 'extra') and record.extra:
            log_entry.update(record.extra)
        
        return json.dumps(log_entry, ensure_ascii=False)


# Función de conveniencia para configuración rápida
def configure_luminoracore_logging(level: str = "INFO", format_type: str = "lambda") -> None:
    """
    Función de conveniencia para configurar rápidamente el logging del framework.
    
    Args:
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_type: Tipo de formato ("lambda", "json", "simple")
    
    USO EN TU HANDLER LAMBDA:
    
    ```python
    import luminoracore_sdk_logging_fix
    
    def lambda_handler(event, context):
        # CONFIGURAR LOGGING ANTES DE USAR EL SDK
        luminoracore_sdk_logging_fix.configure_luminoracore_logging(level="DEBUG")
        
        # Ahora usar el SDK normalmente
        from luminoracore_sdk import LuminoraCoreClient
        # ... resto de tu código
    ```
    """
    config = LuminoraCoreLoggingConfig(level=level, format_type=format_type)
    config.configure_logging()


# Configuración automática para entornos de desarrollo
def auto_configure_for_environment() -> None:
    """
    Configurar automáticamente el logging basado en variables de entorno.
    
    Variables de entorno soportadas:
    - LUMINORACORE_LOG_LEVEL: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - LUMINORACORE_LOG_FORMAT: Formato de logging (lambda, json, simple)
    - AWS_LAMBDA_FUNCTION_NAME: Si está presente, configura para Lambda
    """
    level = os.getenv("LUMINORACORE_LOG_LEVEL", "INFO")
    format_type = os.getenv("LUMINORACORE_LOG_FORMAT", "lambda")
    
    # Si estamos en Lambda, usar formato lambda por defecto
    if os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        format_type = "lambda"
    
    configure_luminoracore_logging(level=level, format_type=format_type)


# Ejemplo de uso completo
if __name__ == "__main__":
    print("=== TESTING LUMINORACORE LOGGING FIX ===")
    
    # Configurar logging
    configure_luminoracore_logging(level="DEBUG")
    
    # Test del framework
    from luminoracore_sdk_logging_fix import LuminoraCoreLoggingConfig
    config = LuminoraCoreLoggingConfig()
    config.test_logging()
    
    print("=== LOGGING TEST COMPLETED ===")
