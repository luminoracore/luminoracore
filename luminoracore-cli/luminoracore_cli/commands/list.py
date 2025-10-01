"""List command for LuminoraCore CLI."""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
import typer
from rich.console import Console
from rich.table import Table
from rich import box

from luminoracore_cli.utils.errors import CLIError
from luminoracore_cli.utils.console import console, error_console
from luminoracore_cli.utils.files import find_personality_files
from luminoracore_cli.utils.formatting import format_personality_list, format_personality_table
from luminoracore_cli.core.client import get_client


def list_command(
    search: Optional[str] = typer.Option(None, "--search", "-s", help="Search personalities by name or tags"),
    archetype: Optional[str] = typer.Option(None, "--archetype", "-a", help="Filter by archetype"),
    author: Optional[str] = typer.Option(None, "--author", help="Filter by author"),
    tags: Optional[str] = typer.Option(None, "--tags", "-t", help="Filter by tags (comma-separated)"),
    detailed: bool = typer.Option(False, "--detailed", "-d", help="Show detailed information"),
    format: str = typer.Option("table", "--format", "-f", help="Output format (table, list, json, yaml)"),
    local_only: bool = typer.Option(False, "--local-only", help="Show only local personalities"),
    remote_only: bool = typer.Option(False, "--remote-only", help="Show only remote personalities"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
) -> int:
    """
    List available personalities.
    
    This command shows all available personalities, with options to filter
    by various criteria and display in different formats.
    """
    try:
        personalities = []
        
        # Get local personalities
        if not remote_only:
            local_personalities = get_local_personalities(verbose=verbose)
            personalities.extend(local_personalities)
        
        # Get remote personalities
        if not local_only:
            remote_personalities = get_remote_personalities(verbose=verbose)
            personalities.extend(remote_personalities)
        
        # Apply filters
        if search:
            personalities = filter_by_search(personalities, search)
        
        if archetype:
            personalities = filter_by_archetype(personalities, archetype)
        
        if author:
            personalities = filter_by_author(personalities, author)
        
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",")]
            personalities = filter_by_tags(personalities, tag_list)
        
        # Remove duplicates (same name and version)
        personalities = remove_duplicates(personalities)
        
        # Sort personalities
        personalities.sort(key=lambda p: (p.get("name", ""), p.get("version", "")))
        
        if verbose:
            console.print(f"[blue]Found {len(personalities)} personalities[/blue]")
        
        # Display results
        if not personalities:
            console.print("[yellow]No personalities found matching the criteria[/yellow]")
            return 0
        
        if format == "json":
            import json
            console.print(json.dumps(personalities, indent=2))
        elif format == "yaml":
            import yaml
            console.print(yaml.dump(personalities, default_flow_style=False))
        elif format == "list":
            output = format_personality_list(personalities, detailed=detailed)
            console.print(output)
        else:  # table format
            if detailed:
                table = create_detailed_table(personalities)
                console.print(table)
            else:
                table = create_simple_table(personalities)
                console.print(table)
        
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


def get_local_personalities(verbose: bool = False) -> List[Dict[str, Any]]:
    """Get local personalities from cache and current directory."""
    personalities = []
    
    # Search in current directory
    current_dir = Path.cwd()
    personality_files = find_personality_files("*", search_dir=current_dir)
    
    for file_path in personality_files:
        try:
            personality_data = read_json_file(file_path)
            if personality_data.get("persona"):
                personality_data["source"] = "local"
                personality_data["file_path"] = str(file_path)
                personalities.append(personality_data)
        except Exception as e:
            if verbose:
                console.print(f"[yellow]Warning: Could not load {file_path}: {e}[/yellow]")
    
    # Search in cache directory
    cache_dir = Path.home() / ".luminoracore" / "cache"
    if cache_dir.exists():
        cache_files = list(cache_dir.glob("**/*.json"))
        
        for file_path in cache_files:
            try:
                personality_data = read_json_file(file_path)
                if personality_data.get("persona"):
                    personality_data["source"] = "cache"
                    personality_data["file_path"] = str(file_path)
                    personalities.append(personality_data)
            except Exception as e:
                if verbose:
                    console.print(f"[yellow]Warning: Could not load {file_path}: {e}[/yellow]")
    
    return personalities


def get_remote_personalities(verbose: bool = False) -> List[Dict[str, Any]]:
    """Get remote personalities from repository."""
    try:
        client = get_client()
        personalities = client.list_personalities()
        
        # Add source information
        for personality in personalities:
            personality["source"] = "remote"
        
        return personalities
    except Exception as e:
        if verbose:
            console.print(f"[yellow]Warning: Could not fetch remote personalities: {e}[/yellow]")
        return []


def filter_by_search(personalities: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """Filter personalities by search term."""
    search_lower = search.lower()
    filtered = []
    
    for personality in personalities:
        name = personality.get("persona", {}).get("name", "").lower()
        description = personality.get("persona", {}).get("description", "").lower()
        tags = personality.get("persona", {}).get("tags", [])
        tags_str = " ".join(tags).lower()
        
        if (search_lower in name or 
            search_lower in description or 
            search_lower in tags_str):
            filtered.append(personality)
    
    return filtered


def filter_by_archetype(personalities: List[Dict[str, Any]], archetype: str) -> List[Dict[str, Any]]:
    """Filter personalities by archetype."""
    archetype_lower = archetype.lower()
    filtered = []
    
    for personality in personalities:
        personality_archetype = personality.get("persona", {}).get("archetype", "").lower()
        if archetype_lower in personality_archetype:
            filtered.append(personality)
    
    return filtered


def filter_by_author(personalities: List[Dict[str, Any]], author: str) -> List[Dict[str, Any]]:
    """Filter personalities by author."""
    author_lower = author.lower()
    filtered = []
    
    for personality in personalities:
        personality_author = personality.get("persona", {}).get("author", "").lower()
        if author_lower in personality_author:
            filtered.append(personality)
    
    return filtered


def filter_by_tags(personalities: List[Dict[str, Any]], tags: List[str]) -> List[Dict[str, Any]]:
    """Filter personalities by tags."""
    tags_lower = [tag.lower() for tag in tags]
    filtered = []
    
    for personality in personalities:
        personality_tags = [tag.lower() for tag in personality.get("persona", {}).get("tags", [])]
        
        # Check if any of the requested tags are present
        if any(tag in personality_tags for tag in tags_lower):
            filtered.append(personality)
    
    return filtered


def remove_duplicates(personalities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate personalities (same name and version)."""
    seen = set()
    unique = []
    
    for personality in personalities:
        name = personality.get("persona", {}).get("name", "")
        version = personality.get("persona", {}).get("version", "")
        key = (name, version)
        
        if key not in seen:
            seen.add(key)
            unique.append(personality)
    
    return unique


def create_simple_table(personalities: List[Dict[str, Any]]) -> Table:
    """Create a simple table for personalities."""
    table = Table(title="Available Personalities", box=box.ROUNDED)
    
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Archetype", style="magenta")
    table.add_column("Version", style="green")
    table.add_column("Author", style="yellow")
    table.add_column("Source", style="blue")
    
    for personality in personalities:
        persona = personality.get("persona", {})
        name = persona.get("name", "Unknown")
        archetype = persona.get("archetype", "Unknown")
        version = persona.get("version", "Unknown")
        author = persona.get("author", "Unknown")
        source = personality.get("source", "Unknown")
        
        table.add_row(name, archetype, version, author, source)
    
    return table


def create_detailed_table(personalities: List[Dict[str, Any]]) -> Table:
    """Create a detailed table for personalities."""
    table = Table(title="Available Personalities (Detailed)", box=box.ROUNDED)
    
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Archetype", style="magenta")
    table.add_column("Version", style="green")
    table.add_column("Author", style="yellow")
    table.add_column("Tags", style="blue")
    table.add_column("Source", style="red")
    table.add_column("Description", style="white")
    
    for personality in personalities:
        persona = personality.get("persona", {})
        name = persona.get("name", "Unknown")
        archetype = persona.get("archetype", "Unknown")
        version = persona.get("version", "Unknown")
        author = persona.get("author", "Unknown")
        tags = ", ".join(persona.get("tags", []))
        source = personality.get("source", "Unknown")
        description = persona.get("description", "No description")
        
        # Truncate description if too long
        if len(description) > 50:
            description = description[:47] + "..."
        
        table.add_row(name, archetype, version, author, tags, source, description)
    
    return table


if __name__ == "__main__":
    typer.run(list_command)
