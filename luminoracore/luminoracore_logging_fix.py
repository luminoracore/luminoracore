"""
SOLUCIÓN PARA PROBLEMA DE LOGGING EN LUMINORACORE CORE

Este archivo resuelve el problema de logging no configurado en el core de LuminoraCore.
"""

import logging
import sys
import os
from typing import Optional, Dict, Any


class LuminoraCoreLoggingConfig:
    """
    Configuración de logging para LuminoraCore Core.
    """
    
    def __init__(self, level: str = "INFO", format_type: str = "simple"):
        """
        Inicializar configuración de logging.
        
        Args:
            level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            format_type: Tipo de formato ("simple", "json", "detailed")
        """
        self.level = level.upper()
        self.format_type = format_type
        self._configured = False
    
    def configure_logging(self) -> None:
        """
        Configurar el logging del core para que funcione correctamente.
        """
        if self._configured:
            return
        
        # Configurar el logger root
        root_logger = logging.getLogger()
        
        # Limpiar handlers existentes para evitar duplicados
        root_logger.handlers.clear()
        
        # Configurar nivel
        root_logger.setLevel(getattr(logging, self.level))
        
        # Crear handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, self.level))
        
        # Configurar formato
        if self.format_type == "json":
            formatter = JsonFormatter()
        elif self.format_type == "detailed":
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            )
        else:  # simple
            formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
        
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
        
        # Configurar loggers específicos del core
        core_loggers = [
            'luminoracore',
            'luminoracore.core',
            'luminoracore.core.memory',
            'luminoracore.core.memory.classifier',
            'luminoracore.core.memory.episodic',
            'luminoracore.core.memory.fact_extractor',
            'luminoracore.core.relationship',
            'luminoracore.core.relationship.affinity',
            'luminoracore.core.compiler_v1_1',
            'luminoracore.core.config',
            'luminoracore.core.config.feature_flags',
            'luminoracore.storage',
            'luminoracore.storage.migrations',
            'luminoracore.storage.migrations.migration_manager',
            'luminoracore.tools',
            'luminoracore.tools.compiler',
            'luminoracore.tools.validator',
            'luminoracore.tools.blender'
        ]
        
        for logger_name in core_loggers:
            logger = logging.getLogger(logger_name)
            logger.setLevel(getattr(logging, self.level))
            logger.propagate = True
        
        self._configured = True
        
        # Log de confirmación
        root_logger.info("LuminoraCore Core logging configurado correctamente")
        root_logger.info(f"Nivel de logging: {self.level}")
        root_logger.info(f"Formato: {self.format_type}")


class JsonFormatter(logging.Formatter):
    """
    Formatter para logs en formato JSON.
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
        
        return json.dumps(log_entry, ensure_ascii=False)


# Función de conveniencia
def configure_luminoracore_core_logging(level: str = "INFO", format_type: str = "simple") -> None:
    """
    Función de conveniencia para configurar rápidamente el logging del core.
    
    Args:
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_type: Tipo de formato ("simple", "json", "detailed")
    """
    config = LuminoraCoreLoggingConfig(level=level, format_type=format_type)
    config.configure_logging()


# Configuración automática
def auto_configure_for_environment() -> None:
    """
    Configurar automáticamente el logging basado en variables de entorno.
    """
    level = os.getenv("LUMINORACORE_CORE_LOG_LEVEL", "INFO")
    format_type = os.getenv("LUMINORACORE_CORE_LOG_FORMAT", "simple")
    
    configure_luminoracore_core_logging(level=level, format_type=format_type)


# Ejemplo de uso
if __name__ == "__main__":
    print("=== TESTING LUMINORACORE CORE LOGGING FIX ===")
    
    # Configurar logging
    configure_luminoracore_core_logging(level="DEBUG")
    
    # Test del core
    from luminoracore_logging_fix import LuminoraCoreLoggingConfig
    config = LuminoraCoreLoggingConfig()
    
    # Test de loggers
    logger = logging.getLogger(__name__)
    logger.info("Core logging test - esto debería aparecer")
    
    print("=== CORE LOGGING TEST COMPLETED ===")
