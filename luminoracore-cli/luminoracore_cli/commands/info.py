"""Info command for LuminoraCore CLI."""

import json
from pathlib import Path
from typing import Optional, Dict, Any
import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.tree import Tree

from luminoracore_cli.utils.errors import CLIError
from luminoracore_cli.utils.console import console, error_console
from luminoracore_cli.utils.files import find_personality_files, read_json_file
from luminoracore_cli.utils.formatting import format_personality_info, create_tree_from_personality
from luminoracore_cli.core.validator import PersonalityValidator
from luminoracore_cli.core.client import get_client


def info_command(
    personality: str = typer.Argument(..., help="Personality name or file path"),
    provider: Optional[str] = typer.Option(None, "--provider", "-p", help="LLM provider for compilation info"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Specific model for compilation info"),
    validate: bool = typer.Option(False, "--validate", help="Show validation information"),
    format: str = typer.Option("tree", "--format", "-f", help="Output format (tree, panel, json, yaml)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
) -> int:
    """
    Show detailed information about a personality.
    
    This command displays comprehensive information about a personality,
    including its structure, validation status, and compilation details.
    """
    try:
        # Find personality file
        personality_path = find_personality_files(personality)
        if not personality_path:
            error_console.print(f"[red]Error: Personality '{personality}' not found[/red]")
            return 1
        
        if verbose:
            console.print(f"[blue]Found personality file: {personality_path}[/blue]")
        
        # Load personality data
        try:
            personality_data = read_json_file(personality_path)
        except Exception as e:
            error_console.print(f"[red]Error loading personality file: {e}[/red]")
            return 1
        
        # Create info object
        info = {
            "file_path": str(personality_path),
            "personality": personality_data,
            "validation": None,
            "compilation": None
        }
        
        # Add validation info if requested
        if validate:
            if verbose:
                console.print("[blue]Validating personality...[/blue]")
            
            validator = PersonalityValidator()
            validation_result = validator.validate(personality_data, strict=True)
            info["validation"] = validation_result
            
            if verbose:
                status = "✓ VALID" if validation_result["valid"] else "✗ INVALID"
                console.print(f"[blue]Validation status: {status}[/blue]")
        
        # Add compilation info if provider specified
        if provider:
            if verbose:
                console.print(f"[blue]Getting compilation info for provider: {provider}[/blue]")
            
            try:
                client = get_client()
                compilation_result = client.compile_personality(
                    personality_data=personality_data,
                    provider=provider,
                    model=model,
                    include_metadata=True
                )
                info["compilation"] = compilation_result
                
                if verbose:
                    console.print("[blue]Compilation info retrieved[/blue]")
            except Exception as e:
                if verbose:
                    console.print(f"[yellow]Warning: Could not get compilation info: {e}[/yellow]")
                info["compilation"] = {"error": str(e)}
        
        # Display results
        if format == "json":
            console.print(json.dumps(info, indent=2))
        elif format == "yaml":
            import yaml
            console.print(yaml.dump(info, default_flow_style=False))
        elif format == "panel":
            display_panel_format(info)
        else:  # tree format
            display_tree_format(info)
        
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


def display_tree_format(info: Dict[str, Any]) -> None:
    """Display personality info in tree format."""
    personality_data = info["personality"]
    
    # Create main tree
    tree = Tree(f"[bold blue]Personality Information[/bold blue]")
    
    # File info branch
    file_branch = tree.add("[bold green]File Information[/bold green]")
    file_branch.add(f"Path: {info['file_path']}")
    file_branch.add(f"Size: {get_file_size(info['file_path'])}")
    
    # Personality tree
    personality_tree = create_tree_from_personality(personality_data)
    tree.add(personality_tree)
    
    # Validation branch
    if info.get("validation"):
        validation_branch = tree.add("[bold yellow]Validation Information[/bold yellow]")
        validation = info["validation"]
        
        if validation["valid"]:
            validation_branch.add("[green]✓ Valid[/green]")
        else:
            validation_branch.add("[red]✗ Invalid[/red]")
            for error in validation.get("errors", []):
                validation_branch.add(f"[red]• {error}[/red]")
        
        if validation.get("warnings"):
            for warning in validation["warnings"]:
                validation_branch.add(f"[yellow]⚠ {warning}[/yellow]")
    
    # Compilation branch
    if info.get("compilation"):
        compilation_branch = tree.add("[bold magenta]Compilation Information[/bold magenta]")
        compilation = info["compilation"]
        
        if "error" in compilation:
            compilation_branch.add(f"[red]Error: {compilation['error']}[/red]")
        else:
            compilation_branch.add(f"Provider: {compilation.get('provider', 'Unknown')}")
            compilation_branch.add(f"Model: {compilation.get('model', 'Unknown')}")
            compilation_branch.add(f"Compiled at: {compilation.get('compiled_at', 'Unknown')}")
            
            if compilation.get("metadata"):
                metadata_branch = compilation_branch.add("Metadata")
                for key, value in compilation["metadata"].items():
                    metadata_branch.add(f"{key}: {value}")
    
    console.print(tree)


def display_panel_format(info: Dict[str, Any]) -> None:
    """Display personality info in panel format."""
    personality_data = info["personality"]
    
    # Basic info panel
    basic_info = format_personality_info(personality_data.get("persona", {}))
    console.print(Panel(basic_info, title="Basic Information", border_style="blue"))
    
    # Core traits panel
    if personality_data.get("core_traits"):
        traits_text = format_traits_text(personality_data["core_traits"])
        console.print(Panel(traits_text, title="Core Traits", border_style="green"))
    
    # Linguistic profile panel
    if personality_data.get("linguistic_profile"):
        ling_text = format_linguistic_text(personality_data["linguistic_profile"])
        console.print(Panel(ling_text, title="Linguistic Profile", border_style="yellow"))
    
    # Behavioral rules panel
    if personality_data.get("behavioral_rules"):
        rules_text = format_rules_text(personality_data["behavioral_rules"])
        console.print(Panel(rules_text, title="Behavioral Rules", border_style="magenta"))
    
    # Validation panel
    if info.get("validation"):
        validation_text = format_validation_text(info["validation"])
        console.print(Panel(validation_text, title="Validation Status", border_style="red"))
    
    # Compilation panel
    if info.get("compilation"):
        compilation_text = format_compilation_text(info["compilation"])
        console.print(Panel(compilation_text, title="Compilation Info", border_style="cyan"))


def format_traits_text(traits: Dict[str, Any]) -> str:
    """Format core traits for display."""
    lines = []
    
    lines.append(f"Archetype: {traits.get('archetype', 'Unknown')}")
    lines.append(f"Temperament: {traits.get('temperament', 'Unknown')}")
    lines.append(f"Communication Style: {traits.get('communication_style', 'Unknown')}")
    
    if traits.get("values"):
        lines.append(f"Values: {', '.join(traits['values'])}")
    
    if traits.get("motivations"):
        lines.append(f"Motivations: {', '.join(traits['motivations'])}")
    
    return "\n".join(lines)


def format_linguistic_text(ling: Dict[str, Any]) -> str:
    """Format linguistic profile for display."""
    lines = []
    
    if ling.get("tone"):
        lines.append(f"Tone: {', '.join(ling['tone'])}")
    
    if ling.get("vocabulary"):
        lines.append(f"Vocabulary: {', '.join(ling['vocabulary'][:10])}...")
    
    if ling.get("speech_patterns"):
        lines.append(f"Speech Patterns: {', '.join(ling['speech_patterns'])}")
    
    lines.append(f"Formality Level: {ling.get('formality_level', 'Unknown')}")
    lines.append(f"Response Length: {ling.get('response_length', 'Unknown')}")
    
    return "\n".join(lines)


def format_rules_text(rules: list) -> str:
    """Format behavioral rules for display."""
    lines = []
    
    for i, rule in enumerate(rules, 1):
        lines.append(f"{i}. {rule}")
    
    return "\n".join(lines)


def format_validation_text(validation: Dict[str, Any]) -> str:
    """Format validation results for display."""
    lines = []
    
    if validation["valid"]:
        lines.append("[green]✓ Valid[/green]")
    else:
        lines.append("[red]✗ Invalid[/red]")
        for error in validation.get("errors", []):
            lines.append(f"  [red]• {error}[/red]")
    
    if validation.get("warnings"):
        for warning in validation["warnings"]:
            lines.append(f"  [yellow]⚠ {warning}[/yellow]")
    
    return "\n".join(lines)


def format_compilation_text(compilation: Dict[str, Any]) -> str:
    """Format compilation info for display."""
    lines = []
    
    if "error" in compilation:
        lines.append(f"[red]Error: {compilation['error']}[/red]")
    else:
        lines.append(f"Provider: {compilation.get('provider', 'Unknown')}")
        lines.append(f"Model: {compilation.get('model', 'Unknown')}")
        lines.append(f"Compiled at: {compilation.get('compiled_at', 'Unknown')}")
        
        if compilation.get("metadata"):
            lines.append("Metadata:")
            for key, value in compilation["metadata"].items():
                lines.append(f"  {key}: {value}")
    
    return "\n".join(lines)


def get_file_size(file_path: str) -> str:
    """Get human-readable file size."""
    try:
        size = Path(file_path).stat().st_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    except OSError:
        return "Unknown"


if __name__ == "__main__":
    typer.run(info_command)
