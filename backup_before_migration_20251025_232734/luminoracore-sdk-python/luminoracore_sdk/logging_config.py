"""
LuminoraCore SDK - Logging Configuration Module

This module provides professional logging configuration for the LuminoraCore SDK.
It ensures all SDK logs are visible in production environments (AWS Lambda, Docker, etc.).

Author: LuminoraCore Team
Version: 1.1.0
"""

import logging
import sys
import os
from typing import Optional, Literal

# Type definitions for format types
FormatType = Literal["lambda", "json", "text", "detailed"]


def setup_logging(
    level: str = "INFO",
    format_type: FormatType = "lambda",
    include_boto: bool = True,
    propagate: bool = True
) -> None:
    """
    Configure logging for LuminoraCore SDK.
    
    This function must be called at the start of your application to ensure
    all SDK logs are properly captured and visible.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_type: Log format type:
            - "lambda": Optimized for AWS Lambda/CloudWatch
            - "json": Structured JSON format
            - "text": Simple text format
            - "detailed": Verbose text format with full context
        include_boto: If True, configure boto3/botocore logging
        propagate: If True, logs propagate to root logger
    
    Examples:
        In AWS Lambda:
        >>> from luminoracore_sdk import setup_logging
        >>> setup_logging(level="DEBUG", format_type="lambda")
        
        In development:
        >>> from luminoracore_sdk import setup_logging
        >>> setup_logging(level="DEBUG", format_type="text")
        
        In production with structured logging:
        >>> from luminoracore_sdk import setup_logging
        >>> setup_logging(level="INFO", format_type="json")
    
    Environment Variables:
        LUMINORACORE_LOG_LEVEL: Override log level
        LUMINORACORE_LOG_FORMAT: Override format type
        AWS_LAMBDA_FUNCTION_NAME: Auto-detects Lambda environment
    """
    # Override with environment variables if present
    level = os.getenv("LUMINORACORE_LOG_LEVEL", level).upper()
    format_type = os.getenv("LUMINORACORE_LOG_FORMAT", format_type)
    
    # Auto-detect Lambda environment
    if os.getenv("AWS_LAMBDA_FUNCTION_NAME") and format_type not in ["json", "detailed"]:
        format_type = "lambda"
    
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
    
    # Set formatter based on type
    formatter = _create_formatter(format_type)
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    
    # Configure all SDK loggers
    sdk_loggers = [
        'luminoracore_sdk',
        'luminoracore_sdk.client',
        'luminoracore_sdk.client_v1_1',
        'luminoracore_sdk.session',
        'luminoracore_sdk.session.memory_v1_1',
        'luminoracore_sdk.session.storage_v1_1',
        'luminoracore_sdk.session.storage_dynamodb_flexible',
        'luminoracore_sdk.session.storage_sqlite_flexible',
        'luminoracore_sdk.session.storage_postgresql_flexible',
        'luminoracore_sdk.session.storage_redis_flexible',
        'luminoracore_sdk.session.storage_mongodb_flexible',
        'luminoracore_sdk.providers',
        'luminoracore_sdk.analysis',
        'luminoracore_sdk.evolution',
        'luminoracore_sdk.monitoring',
        'luminoracore_sdk.utils'
    ]
    
    for logger_name in sdk_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(numeric_level)
        logger.propagate = propagate
    
    # Configure boto3/botocore if requested
    if include_boto:
        for boto_logger_name in ['boto3', 'botocore', 'urllib3', 's3transfer']:
            boto_logger = logging.getLogger(boto_logger_name)
            boto_logger.setLevel(logging.WARNING)
            boto_logger.propagate = True
    
    # Log confirmation
    logger = logging.getLogger('luminoracore_sdk')
    logger.info(f"✓ LuminoraCore SDK logging configured: level={level}, format={format_type}")


def _create_formatter(format_type: FormatType) -> logging.Formatter:
    """Create formatter based on format type."""
    if format_type == "lambda":
        return logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    elif format_type == "json":
        return JsonFormatter()
    elif format_type == "detailed":
        return logging.Formatter(
            '[%(asctime)s] %(levelname)-8s [%(name)s:%(funcName)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:  # text
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
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in ["name", "msg", "args", "levelname", "levelno", 
                          "pathname", "filename", "module", "exc_info", 
                          "exc_text", "stack_info", "lineno", "funcName", 
                          "created", "msecs", "relativeCreated", "thread", 
                          "threadName", "processName", "process", "getMessage"]:
                log_data[key] = value
        
        return json.dumps(log_data, ensure_ascii=False, default=str)


def auto_configure() -> None:
    """
    Auto-configure logging based on environment.
    
    This function detects the environment and applies appropriate defaults:
    - AWS Lambda: Uses "lambda" format with INFO level
    - Development (DEBUG=1): Uses "text" format with DEBUG level
    - Production: Uses "json" format with INFO level
    
    Environment Variables:
        AWS_LAMBDA_FUNCTION_NAME: Detected Lambda environment
        DEBUG: Enable debug mode (set to "1", "true", or "yes")
        LUMINORACORE_LOG_LEVEL: Override log level
        LUMINORACORE_LOG_FORMAT: Override format type
    
    Example:
        >>> from luminoracore_sdk.logging_config import auto_configure
        >>> auto_configure()
    """
    # Detect environment
    is_lambda = bool(os.getenv("AWS_LAMBDA_FUNCTION_NAME"))
    is_debug = os.getenv("DEBUG", "").lower() in ["1", "true", "yes"]
    
    # Determine defaults
    if is_lambda:
        default_level = "INFO"
        default_format = "lambda"
    elif is_debug:
        default_level = "DEBUG"
        default_format = "text"
    else:
        default_level = "INFO"
        default_format = "json"
    
    # Get from environment or use defaults
    level = os.getenv("LUMINORACORE_LOG_LEVEL", default_level)
    format_type = os.getenv("LUMINORACORE_LOG_FORMAT", default_format)
    
    # Configure
    setup_logging(level=level, format_type=format_type)


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger for the given name.
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Configured logger instance
    
    Example:
        >>> from luminoracore_sdk.logging_config import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Application started")
    """
    return logging.getLogger(name)


# Convenience function for backward compatibility
configure_logging = setup_logging


__all__ = [
    "setup_logging",
    "auto_configure",
    "get_logger",
    "configure_logging",  # Backward compatibility
]
