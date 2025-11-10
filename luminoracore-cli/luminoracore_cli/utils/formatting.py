"""Formatting utilities for LuminoraCore CLI."""

from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import json
import yaml

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
from rich.tree import Tree
from rich import box

from luminoracore_cli.utils.console import console


def format_personality_info(personality: Dict[str, Any]) -> str:
    """Format personality information for display."""
    lines = []
    
    # Basic info
    lines.append(f"[bold blue]Name:[/bold blue] {personality.get('name', 'Unknown')}")
    lines.append(f"[bold blue]Description:[/bold blue] {personality.get('description', 'No description')}")
    lines.append(f"[bold blue]Archetype:[/bold blue] {personality.get('archetype', 'Unknown')}")
    lines.append(f"[bold blue]Version:[/bold blue] {personality.get('version', 'Unknown')}")
    
    if personality.get('author'):
        lines.append(f"[bold blue]Author:[/bold blue] {personality['author']}")
    
    if personality.get('tags'):
        tags = ", ".join(personality['tags'])
        lines.append(f"[bold blue]Tags:[/bold blue] {tags}")
    
    return "\n".join(lines)


def format_validation_results(results: List[Dict[str, Any]]) -> str:
    """Format validation results for display."""
    if not results:
        return "[green]No validation results to display.[/green]"
    
    lines = []
    
    for result in results:
        file_path = result.get('file', 'Unknown')
        is_valid = result.get('valid', False)
        
        status = "[green]✓ VALID[/green]" if is_valid else "[red]✗ INVALID[/red]"
        lines.append(f"{status} [bold]{file_path}[/bold]")
        
        if not is_valid and result.get('errors'):
            for error in result['errors']:
                lines.append(f"  [red]• {error}[/red]")
        
        if result.get('warnings'):
            for warning in result['warnings']:
                lines.append(f"  [yellow]⚠ {warning}[/yellow]")
        
        lines.append("")  # Empty line between results
    
    return "\n".join(lines)


def format_personality_list(personalities: List[Dict[str, Any]], detailed: bool = False) -> str:
    """Format list of personalities for display."""
    if not personalities:
        return "[yellow]No personalities found.[/yellow]"
    
    if detailed:
        return format_personality_table(personalities)
    else:
        lines = []
        for personality in personalities:
            name = personality.get('name', 'Unknown')
            archetype = personality.get('archetype', 'Unknown')
            version = personality.get('version', 'Unknown')
            lines.append(f"[bold]{name}[/bold] ({archetype}) v{version}")
        
        return "\n".join(lines)


def format_personality_table(personalities: List[Dict[str, Any]]) -> str:
    """Format personalities as a rich table."""
    table = Table(title="Available Personalities", box=box.ROUNDED)
    
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Archetype", style="magenta")
    table.add_column("Version", style="green")
    table.add_column("Author", style="yellow")
    table.add_column("Tags", style="blue")
    
    for personality in personalities:
        name = personality.get('name', 'Unknown')
        archetype = personality.get('archetype', 'Unknown')
        version = personality.get('version', 'Unknown')
        author = personality.get('author', 'Unknown')
        tags = ", ".join(personality.get('tags', []))
        
        table.add_row(name, archetype, version, author, tags)
    
    return table


def format_compilation_result(result: Dict[str, Any]) -> str:
    """Format compilation result for display."""
    lines = []
    
    lines.append(f"[bold blue]Provider:[/bold blue] {result.get('provider', 'Unknown')}")
    lines.append(f"[bold blue]Model:[/bold blue] {result.get('model', 'Unknown')}")
    lines.append(f"[bold blue]Personality:[/bold blue] {result.get('personality_name', 'Unknown')}")
    lines.append(f"[bold blue]Compiled at:[/bold blue] {result.get('compiled_at', 'Unknown')}")
    
    if result.get('metadata'):
        lines.append(f"[bold blue]Metadata:[/bold blue] {result['metadata']}")
    
    lines.append("")
    lines.append("[bold blue]Compiled Prompt:[/bold blue]")
    lines.append("─" * 50)
    lines.append(result.get('prompt', 'No prompt generated'))
    
    return "\n".join(lines)


def format_blend_result(result: Dict[str, Any]) -> str:
    """Format blend result for display."""
    lines = []
    
    lines.append(f"[bold blue]Blended Personality:[/bold blue] {result.get('name', 'Unknown')}")
    lines.append(f"[bold blue]Components:[/bold blue]")
    
    for component in result.get('components', []):
        name = component.get('name', 'Unknown')
        weight = component.get('weight', 0.0)
        lines.append(f"  • {name}: {weight:.1%}")
    
    lines.append(f"[bold blue]Created at:[/bold blue] {result.get('created_at', 'Unknown')}")
    
    return "\n".join(lines)


def format_json_output(data: Any) -> str:
    """Format data as JSON output."""
    try:
        return json.dumps(data, indent=2, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        return f"[red]Error formatting JSON: {e}[/red]"


def format_yaml_output(data: Any) -> str:
    """Format data as YAML output."""
    try:
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)
    except (TypeError, ValueError) as e:
        return f"[red]Error formatting YAML: {e}[/red]"


def format_error(error: Exception) -> str:
    """Format error for display."""
    error_type = type(error).__name__
    error_message = str(error)
    
    return f"[red]Error ({error_type}): {error_message}[/red]"


def format_success(message: str) -> str:
    """Format success message."""
    return f"[green]✓ {message}[/green]"


def format_warning(message: str) -> str:
    """Format warning message."""
    return f"[yellow]⚠ {message}[/yellow]"


def format_info(message: str) -> str:
    """Format info message."""
    return f"[blue]ℹ {message}[/blue]"


def format_progress(current: int, total: int, description: str = "") -> str:
    """Format progress information."""
    percentage = (current / total) * 100 if total > 0 else 0
    return f"[cyan]{description}[/cyan] [{current}/{total}] ({percentage:.1f}%)"


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def format_duration(seconds: float) -> str:
    """Format duration in human readable format."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def format_cache_info(info: Dict[str, Any]) -> str:
    """Format cache information for display."""
    lines = []
    
    lines.append(f"[bold blue]Cache Directory:[/bold blue] {info.get('cache_dir', 'Unknown')}")
    lines.append(f"[bold blue]Total Entries:[/bold blue] {info.get('total_entries', 0)}")
    lines.append(f"[bold blue]Total Size:[/bold blue] {format_file_size(info.get('total_size', 0))}")
    lines.append(f"[bold blue]Max Size:[/bold blue] {format_file_size(info.get('max_size', 0))}")
    lines.append(f"[bold blue]Usage:[/bold blue] {info.get('usage_percent', 0):.1f}%")
    lines.append(f"[bold blue]TTL:[/bold blue] {format_duration(info.get('ttl', 0))}")
    
    return "\n".join(lines)


def create_tree_from_personality(personality: Dict[str, Any]) -> Tree:
    """Create a rich tree from personality data."""
    tree = Tree(f"[bold blue]{personality.get('name', 'Unknown')}[/bold blue]")
    
    # Persona branch
    persona_branch = tree.add("[bold green]Persona[/bold green]")
    if personality.get('persona'):
        persona = personality['persona']
        persona_branch.add(f"Name: {persona.get('name', 'Unknown')}")
        persona_branch.add(f"Description: {persona.get('description', 'No description')}")
        persona_branch.add(f"Archetype: {persona.get('archetype', 'Unknown')}")
        persona_branch.add(f"Version: {persona.get('version', 'Unknown')}")
        if persona.get('author'):
            persona_branch.add(f"Author: {persona['author']}")
        if persona.get('tags'):
            persona_branch.add(f"Tags: {', '.join(persona['tags'])}")
    
    # Core traits branch
    traits_branch = tree.add("[bold yellow]Core Traits[/bold yellow]")
    if personality.get('core_traits'):
        traits = personality['core_traits']
        traits_branch.add(f"Archetype: {traits.get('archetype', 'Unknown')}")
        traits_branch.add(f"Temperament: {traits.get('temperament', 'Unknown')}")
        traits_branch.add(f"Communication Style: {traits.get('communication_style', 'Unknown')}")
        if traits.get('values'):
            traits_branch.add(f"Values: {', '.join(traits['values'])}")
        if traits.get('motivations'):
            traits_branch.add(f"Motivations: {', '.join(traits['motivations'])}")
    
    # Linguistic profile branch
    ling_branch = tree.add("[bold magenta]Linguistic Profile[/bold magenta]")
    if personality.get('linguistic_profile'):
        ling = personality['linguistic_profile']
        if ling.get('tone'):
            ling_branch.add(f"Tone: {', '.join(ling['tone'])}")
        if ling.get('vocabulary'):
            ling_branch.add(f"Vocabulary: {', '.join(ling['vocabulary'][:5])}...")
        if ling.get('speech_patterns'):
            ling_branch.add(f"Speech Patterns: {', '.join(ling['speech_patterns'][:3])}...")
        ling_branch.add(f"Formality: {ling.get('formality_level', 'Unknown')}")
        ling_branch.add(f"Response Length: {ling.get('response_length', 'Unknown')}")
    
    return tree
