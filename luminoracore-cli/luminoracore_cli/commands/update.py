"""Update command for LuminoraCore CLI."""

import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any
import typer
from rich.console import Console

from luminoracore_cli.utils.errors import CLIError
from luminoracore_cli.utils.console import console, error_console
from luminoracore_cli.utils.progress import ProgressTracker, track_progress
from luminoracore_cli.utils.cache import get_cache_manager
from luminoracore_cli.utils.files import read_json_file, write_json_file
from luminoracore_cli.core.client import get_client


def update_command(
    personality: Optional[str] = typer.Argument(None, help="Specific personality to update (optional)"),
    version: Optional[str] = typer.Option(None, "--version", help="Update personality version"),
    force: bool = typer.Option(False, "--force", "-f", help="Force update even if already cached"),
    cache_only: bool = typer.Option(False, "--cache-only", help="Only update cache, don't download new personalities"),
    list_available: bool = typer.Option(False, "--list", help="List available personalities from repository"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
) -> int:
    """
    Update personality cache from repository.
    
    This command downloads and caches personalities from the LuminoraCore
    repository, making them available for local use.
    """
    try:
        # Update personality version if specified
        if version and personality:
            if verbose:
                console.print(f"[blue]Updating version of {personality} to {version}[/blue]")
            
            personality_path = Path(personality)
            if not personality_path.exists():
                error_console.print(f"[red]Error: Personality file not found: {personality}[/red]")
                raise typer.Exit(1)
            
            # Read personality data
            personality_data = read_json_file(personality_path)
            
            # Update version
            if "persona" not in personality_data:
                personality_data["persona"] = {}
            personality_data["persona"]["version"] = version
            
            # Write back
            write_json_file(personality_path, personality_data)
            
            console.print(f"[green]✓ Updated {personality} to version {version}[/green]")
            return 0
        
        # Get cache manager
        cache_manager = get_cache_manager()
        
        if verbose:
            console.print(f"[blue]Cache directory: {cache_manager.cache_dir}[/blue]")
        
        # List available personalities if requested
        if list_available:
            return list_available_personalities(verbose=verbose)
        
        # Get client
        client = get_client()
        
        # Update specific personality
        if personality:
            return update_single_personality(personality, force=force, verbose=verbose)
        
        # Update all personalities
        return update_all_personalities(force=force, cache_only=cache_only, verbose=verbose)
        
    except CLIError as e:
        error_console.print(f"[red]CLI error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        error_console.print(f"[red]Unexpected error: {e}[/red]")
        if verbose:
            import traceback
            error_console.print(traceback.format_exc())
        raise typer.Exit(1)


def list_available_personalities(verbose: bool = False) -> int:
    """List available personalities from repository."""
    try:
        client = get_client()
        
        if verbose:
            console.print("[blue]Fetching available personalities from repository...[/blue]")
        
        personalities = client.list_personalities()
        
        if not personalities:
            console.print("[yellow]No personalities available in repository[/yellow]")
            return 0
        
        console.print(f"[green]Found {len(personalities)} personalities in repository:[/green]")
        console.print("")
        
        # Display personalities
        for personality in personalities:
            name = personality.get("name", "Unknown")
            archetype = personality.get("archetype", "Unknown")
            version = personality.get("version", "Unknown")
            author = personality.get("author", "Unknown")
            description = personality.get("description", "No description")
            
            console.print(f"[bold cyan]{name}[/bold cyan] ({archetype}) v{version}")
            console.print(f"  Author: {author}")
            console.print(f"  Description: {description}")
            console.print("")
        
        return 0
        
    except Exception as e:
        error_console.print(f"[red]Failed to list personalities: {e}[/red]")
        raise typer.Exit(1)


def update_single_personality(personality: str, force: bool = False, verbose: bool = False) -> int:
    """Update a single personality."""
    try:
        client = get_client()
        cache_manager = get_cache_manager()
        
        if verbose:
            console.print(f"[blue]Updating personality: {personality}[/blue]")
        
        # Check if already cached
        cache_key = f"personality_{personality}"
        if not force and cache_manager.get(cache_key):
            console.print(f"[yellow]Personality '{personality}' is already cached[/yellow]")
            if not force:
                return 0
        
        # Download personality
        personality_data = client.get_personality(personality)
        
        if not personality_data:
            error_console.print(f"[red]Personality '{personality}' not found in repository[/red]")
            raise typer.Exit(1)
        
        # Cache personality
        cache_manager.set(cache_key, personality_data)
        
        console.print(f"[green]✓ Updated personality: {personality}[/green]")
        
        return 0
        
    except Exception as e:
        error_console.print(f"[red]Failed to update personality '{personality}': {e}[/red]")
        raise typer.Exit(1)


def update_all_personalities(force: bool = False, cache_only: bool = False, verbose: bool = False) -> int:
    """Update all personalities from repository."""
    try:
        client = get_client()
        cache_manager = get_cache_manager()
        
        if verbose:
            console.print("[blue]Updating all personalities from repository...[/blue]")
        
        # Get list of available personalities
        personalities = client.list_personalities()
        
        if not personalities:
            console.print("[yellow]No personalities available in repository[/yellow]")
            return 0
        
        # Filter personalities to update
        if not force:
            personalities_to_update = []
            for personality in personalities:
                name = personality.get("name", "")
                cache_key = f"personality_{name}"
                
                if not cache_manager.get(cache_key):
                    personalities_to_update.append(personality)
        else:
            personalities_to_update = personalities
        
        if not personalities_to_update:
            console.print("[yellow]All personalities are already up to date[/yellow]")
            return 0
        
        console.print(f"[blue]Updating {len(personalities_to_update)} personalities...[/blue]")
        
        # Update personalities with progress tracking
        with track_progress("Updating personalities", len(personalities_to_update)) as progress:
            updated_count = 0
            failed_count = 0
            
            for personality in personalities_to_update:
                name = personality.get("name", "")
                
                try:
                    # Download personality data
                    personality_data = client.get_personality(name)
                    
                    if personality_data:
                        # Cache personality
                        cache_key = f"personality_{name}"
                        cache_manager.set(cache_key, personality_data)
                        updated_count += 1
                        
                        if verbose:
                            console.print(f"[green]✓ Updated: {name}[/green]")
                    else:
                        failed_count += 1
                        if verbose:
                            console.print(f"[red]✗ Failed: {name}[/red]")
                
                except Exception as e:
                    failed_count += 1
                    if verbose:
                        console.print(f"[red]✗ Failed: {name} - {e}[/red]")
                
                progress.update(1, f"Updated {updated_count}, Failed {failed_count}")
        
        # Summary
        console.print("")
        console.print(f"[green]✓ Successfully updated: {updated_count} personalities[/green]")
        if failed_count > 0:
            console.print(f"[red]✗ Failed to update: {failed_count} personalities[/red]")
        
        # Show cache info
        cache_info = cache_manager.info()
        console.print(f"[blue]Cache now contains: {cache_info['total_entries']} entries[/blue]")
        console.print(f"[blue]Cache size: {format_file_size(cache_info['total_size'])}[/blue]")
        
        return 0 if failed_count == 0 else 1
        
    except Exception as e:
        error_console.print(f"[red]Failed to update personalities: {e}[/red]")
        raise typer.Exit(1)


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


if __name__ == "__main__":
    typer.run(update_command)
