"""Advanced logging for LuminoraCore SDK."""

import logging
import sys
from typing import Dict, Any, Optional, Union
from datetime import datetime
import json
from pathlib import Path

from ..utils.helpers import sanitize_api_key


class LuminoraLogger:
    """Advanced logger for LuminoraCore SDK."""
    
    def __init__(
        self,
        name: str = "luminoracore",
        level: str = "INFO",
        log_file: Optional[str] = None,
        format: str = "json",
        include_timestamp: bool = True,
        include_level: bool = True,
        include_module: bool = True,
        sanitize_sensitive: bool = True
    ):
        """
        Initialize the LuminoraCore logger.
        
        Args:
            name: Logger name
            level: Logging level
            log_file: Optional log file path
            format: Log format (json, text)
            include_timestamp: Whether to include timestamp
            include_level: Whether to include log level
            include_module: Whether to include module information
            sanitize_sensitive: Whether to sanitize sensitive information
        """
        self.name = name
        self.level = getattr(logging, level.upper())
        self.log_file = log_file
        self.format = format
        self.include_timestamp = include_timestamp
        self.include_level = include_level
        self.include_module = include_module
        self.sanitize_sensitive = sanitize_sensitive
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # Add console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.level)
        console_handler.setFormatter(self._create_formatter())
        self.logger.addHandler(console_handler)
        
        # Add file handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(self.level)
            file_handler.setFormatter(self._create_formatter())
            self.logger.addHandler(file_handler)
    
    def _create_formatter(self) -> logging.Formatter:
        """Create log formatter based on configuration."""
        if self.format == "json":
            return JsonFormatter(
                include_timestamp=self.include_timestamp,
                include_level=self.include_level,
                include_module=self.include_module,
                sanitize_sensitive=self.sanitize_sensitive
            )
        else:
            return TextFormatter(
                include_timestamp=self.include_timestamp,
                include_level=self.include_level,
                include_module=self.include_module,
                sanitize_sensitive=self.sanitize_sensitive
            )
    
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        self.logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs) -> None:
        """Log error message."""
        self.logger.error(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs) -> None:
        """Log critical message."""
        self.logger.critical(message, extra=kwargs)
    
    def log_api_call(
        self,
        provider: str,
        model: str,
        endpoint: str,
        method: str,
        status_code: int,
        response_time: float,
        tokens_used: Optional[int] = None,
        **kwargs
    ) -> None:
        """Log API call information."""
        self.info(
            "API call completed",
            provider=provider,
            model=model,
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            response_time=response_time,
            tokens_used=tokens_used,
            **kwargs
        )
    
    def log_session_event(
        self,
        session_id: str,
        event_type: str,
        message: str,
        **kwargs
    ) -> None:
        """Log session-related event."""
        self.info(
            f"Session event: {event_type}",
            session_id=session_id,
            event_type=event_type,
            message=message,
            **kwargs
        )
    
    def log_personality_event(
        self,
        personality_name: str,
        event_type: str,
        message: str,
        **kwargs
    ) -> None:
        """Log personality-related event."""
        self.info(
            f"Personality event: {event_type}",
            personality_name=personality_name,
            event_type=event_type,
            message=message,
            **kwargs
        )
    
    def log_error(
        self,
        error_type: str,
        message: str,
        exception: Optional[Exception] = None,
        **kwargs
    ) -> None:
        """Log error with additional context."""
        error_data = {
            "error_type": error_type,
            "message": message,
            "exception": str(exception) if exception else None,
            **kwargs
        }
        
        self.error(f"Error: {error_type}", **error_data)
    
    def log_metrics(
        self,
        metrics_name: str,
        value: Union[int, float],
        metric_type: str,
        **kwargs
    ) -> None:
        """Log metrics information."""
        self.info(
            f"Metrics: {metrics_name}",
            metrics_name=metrics_name,
            value=value,
            metric_type=metric_type,
            **kwargs
        )


class JsonFormatter(logging.Formatter):
    """JSON formatter for logs."""
    
    def __init__(
        self,
        include_timestamp: bool = True,
        include_level: bool = True,
        include_module: bool = True,
        sanitize_sensitive: bool = True
    ):
        """
        Initialize JSON formatter.
        
        Args:
            include_timestamp: Whether to include timestamp
            include_level: Whether to include log level
            include_module: Whether to include module information
            sanitize_sensitive: Whether to sanitize sensitive information
        """
        super().__init__()
        self.include_timestamp = include_timestamp
        self.include_level = include_level
        self.include_module = include_module
        self.sanitize_sensitive = sanitize_sensitive
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "message": record.getMessage(),
        }
        
        if self.include_timestamp:
            log_data["timestamp"] = datetime.utcnow().isoformat()
        
        if self.include_level:
            log_data["level"] = record.levelname
        
        if self.include_module:
            log_data["module"] = record.name
            log_data["function"] = record.funcName
            log_data["line"] = record.lineno
        
        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in ["name", "msg", "args", "levelname", "levelno", "pathname", "filename", "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName", "created", "msecs", "relativeCreated", "thread", "threadName", "processName", "process", "getMessage"]:
                # Sanitize sensitive information
                if self.sanitize_sensitive and self._is_sensitive_key(key):
                    log_data[key] = self._sanitize_value(value)
                else:
                    log_data[key] = value
        
        return json.dumps(log_data, default=str)
    
    def _is_sensitive_key(self, key: str) -> bool:
        """Check if a key contains sensitive information."""
        sensitive_keys = [
            "api_key", "password", "secret", "token", "auth",
            "credential", "key", "private", "sensitive"
        ]
        return any(sensitive in key.lower() for sensitive in sensitive_keys)
    
    def _sanitize_value(self, value: Any) -> Any:
        """Sanitize sensitive values."""
        if isinstance(value, str):
            return sanitize_api_key(value)
        elif isinstance(value, dict):
            return {k: self._sanitize_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._sanitize_value(v) for v in value]
        else:
            return value


class TextFormatter(logging.Formatter):
    """Text formatter for logs."""
    
    def __init__(
        self,
        include_timestamp: bool = True,
        include_level: bool = True,
        include_module: bool = True,
        sanitize_sensitive: bool = True
    ):
        """
        Initialize text formatter.
        
        Args:
            include_timestamp: Whether to include timestamp
            include_level: Whether to include log level
            include_module: Whether to include module information
            sanitize_sensitive: Whether to sanitize sensitive information
        """
        super().__init__()
        self.include_timestamp = include_timestamp
        self.include_level = include_level
        self.include_module = include_module
        self.sanitize_sensitive = sanitize_sensitive
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as text."""
        parts = []
        
        if self.include_timestamp:
            parts.append(f"[{datetime.utcnow().isoformat()}]")
        
        if self.include_level:
            parts.append(f"[{record.levelname}]")
        
        if self.include_module:
            parts.append(f"[{record.name}]")
        
        # Add message
        parts.append(record.getMessage())
        
        # Add extra fields
        extra_fields = []
        for key, value in record.__dict__.items():
            if key not in ["name", "msg", "args", "levelname", "levelno", "pathname", "filename", "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName", "created", "msecs", "relativeCreated", "thread", "threadName", "processName", "process", "getMessage"]:
                # Sanitize sensitive information
                if self.sanitize_sensitive and self._is_sensitive_key(key):
                    value = self._sanitize_value(value)
                extra_fields.append(f"{key}={value}")
        
        if extra_fields:
            parts.append(f"({', '.join(extra_fields)})")
        
        return " ".join(parts)
    
    def _is_sensitive_key(self, key: str) -> bool:
        """Check if a key contains sensitive information."""
        sensitive_keys = [
            "api_key", "password", "secret", "token", "auth",
            "credential", "key", "private", "sensitive"
        ]
        return any(sensitive in key.lower() for sensitive in sensitive_keys)
    
    def _sanitize_value(self, value: Any) -> Any:
        """Sanitize sensitive values."""
        if isinstance(value, str):
            return sanitize_api_key(value)
        elif isinstance(value, dict):
            return {k: self._sanitize_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._sanitize_value(v) for v in value]
        else:
            return value


# Global logger instance
logger = LuminoraLogger()
