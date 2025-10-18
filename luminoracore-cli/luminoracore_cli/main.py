"""Main CLI application entry point."""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.traceback import install as install_rich_traceback

from . import __version__
from .config import Settings, load_settings
from .commands import (
    validate_command,
    compile_command,
    create_command,
    list_command,
    test_command,
    serve_command,
    blend_command,
    update_command,
    init_command,
    info_command,
    # v1.1 commands
    migrate,
    memory,
    snapshot,
)
from .utils.console import console, error_console
from .utils.errors import CLIError, handle_cli_error

# Install rich traceback for better error display
install_rich_traceback(show_locals=True)

# Create main app
app = typer.Typer(
    name="luminoracore",
    help="LuminoraCore CLI - Professional tool for AI personality management",
    epilog="Visit https://luminoracore.com for more information",
    no_args_is_help=True,
    rich_markup_mode="rich",
    pretty_exceptions_enable=False,  # We handle our own
    add_completion=True,
)

# Global options
@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        help="Show version and exit",
    ),
    config_file: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to configuration file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-V",
        help="Enable verbose output",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output",
    ),
    no_color: bool = typer.Option(
        False,
        "--no-color",
        help="Disable colored output",
    ),
    cache_dir: Optional[Path] = typer.Option(
        None,
        "--cache-dir",
        help="Custom cache directory",
    ),
) -> None:
    """
    LuminoraCore CLI - Professional tool for AI personality management.
    
    This tool provides comprehensive functionality for working with AI personalities:
    
    • Validate personality files against the official schema
    • Compile personalities to provider-specific prompts  
    • Create new personalities with interactive wizards
    • Test personalities in interactive chat mode
    • Blend multiple personalities with custom weights
    • Serve local development server with web interface
    
    Examples:
        luminoracore validate my_personality.json
        luminoracore compile dr_luna --model openai
        luminoracore test captain_hook --interactive
        luminoracore serve --port 8080
    """
    if version:
        console.print(f"LuminoraCore CLI v{__version__}")
        raise typer.Exit(0)
    
    # If no command provided, show help
    if ctx.invoked_subcommand is None and not version:
        console.print(ctx.get_help())
        raise typer.Exit(0)
    
    # Configure console based on options
    if no_color:
        console._color_system = None
        error_console._color_system = None
    
    if quiet:
        console.quiet = True
    
    # Load configuration
    try:
        settings = load_settings(config_file)
        ctx.obj = {
            "settings": settings,
            "verbose": verbose,
            "quiet": quiet,
        }
    except Exception as e:
        handle_cli_error(CLIError(f"Failed to load configuration: {e}"))
        raise typer.Exit(1)

# Register commands
# Note: Typer handles async commands internally
app.command("validate", help="Validate personality files")(validate_command)
app.command("compile", help="Compile personalities to prompts")(compile_command)
app.command("create", help="Create new personalities")(create_command)
app.command("list", help="List available personalities")(list_command)
app.command("test", help="Test personalities interactively")(test_command)
app.command("serve", help="Start development server")(serve_command)
app.command("blend", help="Blend multiple personalities")(blend_command)
app.command("update", help="Update personality cache")(update_command)
app.command("init", help="Initialize new project")(init_command)
app.command("info", help="Show personality information")(info_command)

# Register v1.1 commands
app.command("migrate", help="Database migration management")(migrate)
app.add_typer(memory, name="memory", help="Memory management (facts, episodes, affinity)")
app.add_typer(snapshot, name="snapshot", help="Session snapshot export/import")

# Exception handling
# @app.callback(invoke_without_command=True)  # DISABLED: conflicts with main callback
def handle_exceptions(ctx: typer.Context) -> None:
    """Global exception handler."""
    try:
        if ctx.invoked_subcommand is None:
            console.print(ctx.get_help())
    except Exception as e:
        handle_cli_error(e)
        raise typer.Exit(1)

def cli_main() -> None:
    """Entry point for the CLI application."""
    try:
        app()
    except KeyboardInterrupt:
        error_console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(130)
    except Exception as e:
        handle_cli_error(e)
        sys.exit(1)

if __name__ == "__main__":
    cli_main()
