"""Error handling utilities for LuminoraCore CLI."""

from __future__ import annotations

import sys
from typing import Optional, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.traceback import Traceback


class CLIError(Exception):
    """Base exception for CLI errors."""
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        exit_code: int = 1
    ):
        """
        Initialize CLI error.
        
        Args:
            message: Error message
            error_code: Optional error code
            details: Optional error details
            exit_code: Exit code for the error
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.exit_code = exit_code
    
    def __str__(self) -> str:
        """String representation of the error."""
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class ValidationError(CLIError):
    """Validation error."""
    
    def __init__(self, message: str, field: Optional[str] = None, **kwargs):
        """Initialize validation error."""
        super().__init__(message, error_code="VALIDATION_ERROR", **kwargs)
        self.field = field


class ConfigurationError(CLIError):
    """Configuration error."""
    
    def __init__(self, message: str, config_key: Optional[str] = None, **kwargs):
        """Initialize configuration error."""
        super().__init__(message, error_code="CONFIG_ERROR", **kwargs)
        self.config_key = config_key


class NetworkError(CLIError):
    """Network error."""
    
    def __init__(self, message: str, url: Optional[str] = None, **kwargs):
        """Initialize network error."""
        super().__init__(message, error_code="NETWORK_ERROR", **kwargs)
        self.url = url


class FileError(CLIError):
    """File operation error."""
    
    def __init__(self, message: str, file_path: Optional[str] = None, **kwargs):
        """Initialize file error."""
        super().__init__(message, error_code="FILE_ERROR", **kwargs)
        self.file_path = file_path


def handle_cli_error(error: Exception, console: Optional[Console] = None) -> None:
    """
    Handle CLI errors with rich formatting.
    
    Args:
        error: Exception to handle
        console: Optional console instance
    """
    if console is None:
        console = Console(file=sys.stderr)
    
    if isinstance(error, CLIError):
        # Handle custom CLI errors
        error_panel = Panel(
            f"[bold red]{error.message}[/bold red]\n\n"
            f"[dim]Error Code: {error.error_code}[/dim]\n"
            f"[dim]Exit Code: {error.exit_code}[/dim]",
            title="[bold red]CLI Error[/bold red]",
            border_style="red",
            padding=(1, 2),
        )
        console.print(error_panel)
        
        # Show details if available
        if error.details:
            details_text = "\n".join([
                f"• {key}: {value}"
                for key, value in error.details.items()
            ])
            details_panel = Panel(
                details_text,
                title="[bold yellow]Details[/bold yellow]",
                border_style="yellow",
                padding=(1, 2),
            )
            console.print(details_panel)
    
    elif isinstance(error, KeyboardInterrupt):
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
    
    else:
        # Handle unexpected errors
        error_panel = Panel(
            f"[bold red]Unexpected error: {str(error)}[/bold red]\n\n"
            f"[dim]This is likely a bug. Please report it with the traceback below.[/dim]",
            title="[bold red]Unexpected Error[/bold red]",
            border_style="red",
            padding=(1, 2),
        )
        console.print(error_panel)
        
        # Show traceback
        traceback = Traceback(show_locals=True)
        console.print(traceback)


def format_error_summary(errors: list[CLIError]) -> str:
    """
    Format a summary of multiple errors.
    
    Args:
        errors: List of CLI errors
        
    Returns:
        Formatted error summary
    """
    if not errors:
        return ""
    
    summary = f"Found {len(errors)} error(s):\n\n"
    
    for i, error in enumerate(errors, 1):
        summary += f"{i}. {error.message}\n"
        if error.error_code:
            summary += f"   Code: {error.error_code}\n"
        if error.details:
            for key, value in error.details.items():
                summary += f"   {key}: {value}\n"
        summary += "\n"
    
    return summary
