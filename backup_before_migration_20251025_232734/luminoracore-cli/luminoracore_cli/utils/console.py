"""Console utilities for LuminoraCore CLI."""

from __future__ import annotations

import sys
from typing import Optional, Any
from rich.console import Console as RichConsole
from rich.theme import Theme

# Define custom theme
THEME = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red",
    "success": "green",
    "debug": "dim",
    "prompt": "bold blue",
    "highlight": "bold yellow",
})

# Create console instances
console = RichConsole(
    theme=THEME,
    force_terminal=True,
    width=None,
    color_system="auto",
    markup=True,
)

error_console = RichConsole(
    theme=THEME,
    file=sys.stderr,
    force_terminal=True,
    width=None,
    color_system="auto",
    markup=True,
)


class ConsoleManager:
    """Manager for console operations."""
    
    def __init__(self, console_instance: RichConsole):
        """Initialize console manager."""
        self.console = console_instance
        self.quiet = False
    
    def print(self, *args, **kwargs) -> None:
        """Print with quiet mode support."""
        if not self.quiet:
            self.console.print(*args, **kwargs)
    
    def info(self, message: str, **kwargs) -> None:
        """Print info message."""
        self.print(f"[info]{message}[/info]", **kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        """Print warning message."""
        self.print(f"[warning]{message}[/warning]", **kwargs)
    
    def error(self, message: str, **kwargs) -> None:
        """Print error message."""
        self.print(f"[error]{message}[/error]", **kwargs)
    
    def success(self, message: str, **kwargs) -> None:
        """Print success message."""
        self.print(f"[success]{message}[/success]", **kwargs)
    
    def debug(self, message: str, **kwargs) -> None:
        """Print debug message."""
        self.print(f"[debug]{message}[/debug]", **kwargs)


# Create console managers
console_manager = ConsoleManager(console)
error_console_manager = ConsoleManager(error_console)
