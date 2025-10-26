"""LuminoraCore CLI - Professional tool for AI personality management."""

from . import __version__

# Logging configuration
from .logging_config import setup_logging, auto_configure, get_logger

__version__ = __version__.__version__
__author__ = "LuminoraCore Team"
__email__ = "cli@luminoracore.com"

__all__ = [
    "__version__",
    "__author__", 
    "__email__",
    # Logging configuration
    "setup_logging",
    "auto_configure",
    "get_logger",
]
