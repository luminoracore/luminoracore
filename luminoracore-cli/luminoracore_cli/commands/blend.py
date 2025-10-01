"""Blend command for LuminoraCore CLI."""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

from luminoracore_cli.utils.errors import CLIError
from luminoracore_cli.utils.console import console, error_console
from luminoracore_cli.utils.files import find_personality_files, read_json_file, write_json_file
from luminoracore_cli.utils.formatting import format_blend_result
from luminoracore_cli.core.client import get_client


def blend_command(
    personalities: str = typer.Argument(..., help="Personalities to blend in format 'name1:weight1,name2:weight2'"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Custom name for blended personality"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive weight adjustment"),
    validate: bool = typer.Option(True, "--validate", help="Validate blended personality"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
) -> int:
    """
    Blend multiple personalities with custom weights.
    
    This command combines multiple personalities into a new blended personality
    with weighted characteristics from each source personality.
    """
    try:
        # Parse personality weights
        personality_weights = parse_personality_weights(personalities)
        
        if verbose:
            console.print(f"[blue]Blending {len(personality_weights)} personalities[/blue]")
        
        # Interactive weight adjustment
        if interactive:
            personality_weights = adjust_weights_interactively(personality_weights)
        
        # Validate weights
        total_weight = sum(personality_weights.values())
        if abs(total_weight - 1.0) > 0.01:
            error_console.print(f"[red]Error: Weights must sum to 1.0, got {total_weight:.3f}[/red]")
            return 1
        
        # Get personality data
        personality_data_list = []
        for personality_id, weight in personality_weights.items():
            personality_data = get_personality_data(personality_id)
            personality_data_list.append((personality_data, weight))
        
        # Blend personalities
        if verbose:
            console.print("[blue]Blending personalities...[/blue]")
        
        client = get_client()
        blended_personality = client.blend_personalities(personality_weights, custom_name=name)
        
        if verbose:
            console.print("[green]✓ Personalities blended successfully[/green]")
        
        # Validate blended personality if requested
        if validate:
            if verbose:
                console.print("[blue]Validating blended personality...[/blue]")
            
            from luminoracore_cli.core.validator import PersonalityValidator
            
            validator = PersonalityValidator()
            validation_result = validator.validate(blended_personality, strict=True)
            
            if not validation_result["valid"]:
                error_console.print("[red]Validation failed:[/red]")
                for error in validation_result["errors"]:
                    error_console.print(f"  [red]• {error}[/red]")
                return 1
            
            if verbose:
                console.print("[green]✓ Blended personality validation passed[/green]")
        
        # Save blended personality
        if not output:
            blended_name = blended_personality.get("persona", {}).get("name", "blended_personality")
            output = f"personalities/{blended_name.lower().replace(' ', '_').replace(':', '_')}.json"
        
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        write_json_file(output_path, blended_personality)
        
        # Display result
        console.print("")
        console.print(Panel(
            f"[bold green]Personalities blended successfully![/bold green]\n\n"
            f"Blended personality: {blended_personality.get('persona', {}).get('name', 'Unknown')}\n"
            f"Saved to: {output_path}\n\n"
            f"Components:\n" + 
            "\n".join([f"  • {name}: {weight:.1%}" for name, weight in personality_weights.items()]) + "\n\n"
            f"Next steps:\n"
            f"1. Test your blended personality: luminoracore test {output_path}\n"
            f"2. Compile for your provider: luminoracore compile {output_path} --provider openai\n"
            f"3. Use in your applications!",
            title="Personalities Blended",
            border_style="green"
        ))
        
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


def parse_personality_weights(personalities: str) -> Dict[str, float]:
    """Parse personality weights from string format."""
    personality_weights = {}
    
    try:
        # Split by comma
        parts = personalities.split(",")
        
        for part in parts:
            part = part.strip()
            
            # Split by colon
            if ":" not in part:
                raise CLIError(f"Invalid format: '{part}'. Use 'name:weight' format")
            
            name, weight_str = part.split(":", 1)
            name = name.strip()
            weight_str = weight_str.strip()
            
            # Parse weight
            try:
                weight = float(weight_str)
            except ValueError:
                raise CLIError(f"Invalid weight: '{weight_str}'. Must be a number")
            
            if weight < 0 or weight > 1:
                raise CLIError(f"Weight must be between 0 and 1, got {weight}")
            
            personality_weights[name] = weight
    
    except Exception as e:
        raise CLIError(f"Failed to parse personality weights: {e}")
    
    return personality_weights


def adjust_weights_interactively(personality_weights: Dict[str, float]) -> Dict[str, float]:
    """Adjust weights interactively."""
    console.print("\n[bold blue]Interactive Weight Adjustment[/bold blue]")
    console.print("Adjust the weights for each personality (weights must sum to 1.0)")
    console.print("")
    
    adjusted_weights = {}
    remaining_weight = 1.0
    
    personality_names = list(personality_weights.keys())
    
    for i, name in enumerate(personality_names[:-1]):  # All except last
        current_weight = personality_weights[name]
        max_weight = remaining_weight - (len(personality_names) - i - 1) * 0.01  # Leave some for others
        
        while True:
            try:
                new_weight = float(Prompt.ask(
                    f"Weight for '{name}' (current: {current_weight:.3f}, max: {max_weight:.3f})",
                    default=str(current_weight)
                ))
                
                if 0 <= new_weight <= max_weight:
                    adjusted_weights[name] = new_weight
                    remaining_weight -= new_weight
                    break
                else:
                    error_console.print(f"[red]Weight must be between 0 and {max_weight:.3f}[/red]")
            except ValueError:
                error_console.print("[red]Please enter a valid number[/red]")
    
    # Last personality gets remaining weight
    last_name = personality_names[-1]
    adjusted_weights[last_name] = remaining_weight
    
    console.print(f"\n[green]Final weights:[/green]")
    for name, weight in adjusted_weights.items():
        console.print(f"  {name}: {weight:.3f}")
    
    total = sum(adjusted_weights.values())
    console.print(f"[blue]Total: {total:.3f}[/blue]")
    
    return adjusted_weights


def get_personality_data(personality_id: str) -> Dict[str, Any]:
    """Get personality data by ID or file path."""
    try:
        # Try to find personality file
        personality_path = find_personality_files(personality_id)
        
        if personality_path:
            return read_json_file(personality_path)
        
        # Try to get from repository
        client = get_client()
        return client.get_personality(personality_id)
        
    except Exception as e:
        raise CLIError(f"Failed to get personality '{personality_id}': {e}")


if __name__ == "__main__":
    typer.run(blend_command)
