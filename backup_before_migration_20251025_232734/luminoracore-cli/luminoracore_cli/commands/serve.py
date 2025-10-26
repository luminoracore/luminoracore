"""Serve command for LuminoraCore CLI."""

import asyncio
from pathlib import Path
from typing import Optional, Dict, Any
import typer
from rich.console import Console
from rich.panel import Panel

from luminoracore_cli.utils.errors import CLIError
from luminoracore_cli.utils.console import console, error_console


def serve_command(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to bind to"),
    reload: bool = typer.Option(False, "--reload", help="Enable auto-reload"),
    api_only: bool = typer.Option(False, "--api-only", help="API only mode (no web UI)"),
    cors: bool = typer.Option(False, "--cors", help="Enable CORS"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
) -> int:
    """
    Start the LuminoraCore development server.
    
    This command starts a local development server with web interface,
    API endpoints, and WebSocket support for testing personalities.
    """
    try:
        if verbose:
            console.print(f"[blue]Starting server on {host}:{port}[/blue]")
            if api_only:
                console.print("[blue]API only mode enabled[/blue]")
            if cors:
                console.print("[blue]CORS enabled[/blue]")
            if reload:
                console.print("[blue]Auto-reload enabled[/blue]")
        
        # Start server
        start_server(host, port, reload, api_only, cors, verbose)
        
        return 0
        
    except CLIError as e:
        error_console.print(f"[red]CLI error: {e}[/red]")
        return 1
    except Exception as e:
        error_console.print(f"[red]Unexpected error: {e}[/red]")
        if verbose:
            import traceback
            error_console.print(traceback.format_exc())
        return 1


def start_server(host: str, port: int, reload: bool, api_only: bool, cors: bool, verbose: bool) -> None:
    """Start the development server."""
    try:
        # Import server components
        from luminoracore_cli.server.app import create_app
        
        # Create FastAPI app
        app = create_app(api_only=api_only, cors=cors)
        
        # Start server
        import uvicorn
        
        console.print("")
        console.print(Panel(
            f"[bold green]LuminoraCore Development Server[/bold green]\n\n"
            f"Server running on: http://{host}:{port}\n"
            f"API Documentation: http://{host}:{port}/docs\n"
            f"WebSocket Chat: ws://{host}:{port}/ws/chat\n\n"
            f"Press Ctrl+C to stop the server",
            title="Server Started",
            border_style="green"
        ))
        
        # Run server
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=reload,
            log_level="info" if verbose else "warning"
        )
        
    except ImportError as e:
        error_console.print(f"[red]Missing dependencies: {e}[/red]")
        error_console.print("[yellow]Install server dependencies with: pip install 'luminoracore-cli[server]'[/yellow]")
        raise CLIError("Server dependencies not installed")
    except Exception as e:
        raise CLIError(f"Failed to start server: {e}")


if __name__ == "__main__":
    typer.run(serve_command)
