"""
SOLUCIÓN PARA PROBLEMA DE LOGGING EN LUMINORACORE CLI

Este archivo resuelve el problema de logging no configurado en el CLI de LuminoraCore.
"""

import logging
import sys
import os
from typing import Optional, Dict, Any


class LuminoraCoreCLILoggingConfig:
    """
    Configuración de logging para LuminoraCore CLI.
    """
    
    def __init__(self, level: str = "INFO", format_type: str = "cli"):
        """
        Inicializar configuración de logging.
        
        Args:
            level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            format_type: Tipo de formato ("cli", "json", "simple")
        """
        self.level = level.upper()
        self.format_type = format_type
        self._configured = False
    
    def configure_logging(self) -> None:
        """
        Configurar el logging del CLI para que funcione correctamente.
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
        elif self.format_type == "simple":
            formatter = logging.Formatter('%(levelname)s - %(message)s')
        else:  # cli
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
        
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
        
        # Configurar loggers específicos del CLI
        cli_loggers = [
            'luminoracore_cli',
            'luminoracore_cli.commands',
            'luminoracore_cli.config',
            'luminoracore_cli.core',
            'luminoracore_cli.interactive',
            'luminoracore_cli.server',
            'luminoracore_cli.utils'
        ]
        
        for logger_name in cli_loggers:
            logger = logging.getLogger(logger_name)
            logger.setLevel(getattr(logging, self.level))
            logger.propagate = True
        
        self._configured = True
        
        # Log de confirmación
        root_logger.info("LuminoraCore CLI logging configurado correctamente")
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
def configure_luminoracore_cli_logging(level: str = "INFO", format_type: str = "cli") -> None:
    """
    Función de conveniencia para configurar rápidamente el logging del CLI.
    
    Args:
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_type: Tipo de formato ("cli", "json", "simple")
    """
    config = LuminoraCoreCLILoggingConfig(level=level, format_type=format_type)
    config.configure_logging()


# Configuración automática
def auto_configure_for_environment() -> None:
    """
    Configurar automáticamente el logging basado en variables de entorno.
    """
    level = os.getenv("LUMINORACORE_CLI_LOG_LEVEL", "INFO")
    format_type = os.getenv("LUMINORACORE_CLI_LOG_FORMAT", "cli")
    
    configure_luminoracore_cli_logging(level=level, format_type=format_type)


# Ejemplo de uso
if __name__ == "__main__":
    print("=== TESTING LUMINORACORE CLI LOGGING FIX ===")
    
    # Configurar logging
    configure_luminoracore_cli_logging(level="DEBUG")
    
    # Test del CLI
    from luminoracore_cli_logging_fix import LuminoraCoreCLILoggingConfig
    config = LuminoraCoreCLILoggingConfig()
    
    # Test de loggers
    logger = logging.getLogger(__name__)
    logger.info("CLI logging test - esto debería aparecer")
    
    print("=== CLI LOGGING TEST COMPLETED ===")
