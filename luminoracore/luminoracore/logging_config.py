"""
LuminoraCore - Logging Configuration Module

This module provides professional logging configuration for the LuminoraCore engine.

Author: LuminoraCore Team
Version: 1.1.0
"""

import logging
import sys
import os
from typing import Optional, Literal

# Type definitions
FormatType = Literal["simple", "json", "detailed"]


def setup_logging(
    level: str = "INFO",
    format_type: FormatType = "simple",
    propagate: bool = True
) -> None:
    """
    Configure logging for LuminoraCore engine.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_type: Log format type:
            - "simple": Simple text format
            - "json": Structured JSON format
            - "detailed": Verbose format with full context
        propagate: If True, logs propagate to root logger
    
    Examples:
        >>> from luminoracore.logging_config import setup_logging
        >>> setup_logging(level="DEBUG", format_type="simple")
    
    Environment Variables:
        LUMINORACORE_CORE_LOG_LEVEL: Override log level
        LUMINORACORE_CORE_LOG_FORMAT: Override format type
    """
    # Override with environment variables
    level = os.getenv("LUMINORACORE_CORE_LOG_LEVEL", level).upper()
    format_type = os.getenv("LUMINORACORE_CORE_LOG_FORMAT", format_type)
    
    # Validate level
    numeric_level = getattr(logging, level, None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(numeric_level)
    
    # Create handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(numeric_level)
    
    # Set formatter
    formatter = _create_formatter(format_type)
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    
    # Configure core loggers
    core_loggers = [
        'luminoracore',
        'luminoracore.core',
        'luminoracore.core.personality',
        'luminoracore.core.compiler',
        'luminoracore.core.schema',
        'luminoracore.tools',
        'luminoracore.utils'
    ]
    
    for logger_name in core_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(numeric_level)
        logger.propagate = propagate
    
    # Log confirmation
    logger = logging.getLogger('luminoracore')
    logger.info(f"✓ LuminoraCore logging configured: level={level}, format={format_type}")


def _create_formatter(format_type: FormatType) -> logging.Formatter:
    """Create formatter based on format type."""
    if format_type == "json":
        return JsonFormatter()
    elif format_type == "detailed":
        return logging.Formatter(
            '[%(asctime)s] %(levelname)-8s [%(name)s:%(funcName)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:  # simple
        return logging.Formatter(
            '%(levelname)s - %(name)s - %(message)s'
        )


class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        import json
        from datetime import datetime
        
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False, default=str)


def auto_configure() -> None:
    """Auto-configure logging based on environment."""
    is_debug = os.getenv("DEBUG", "").lower() in ["1", "true", "yes"]
    
    level = "DEBUG" if is_debug else "INFO"
    format_type = "detailed" if is_debug else "simple"
    
    level = os.getenv("LUMINORACORE_CORE_LOG_LEVEL", level)
    format_type = os.getenv("LUMINORACORE_CORE_LOG_FORMAT", format_type)
    
    setup_logging(level=level, format_type=format_type)


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger."""
    return logging.getLogger(name)


# Backward compatibility
configure_logging = setup_logging

__all__ = [
    "setup_logging",
    "auto_configure",
    "get_logger",
    "configure_logging",
]
