"""Create command for LuminoraCore CLI."""

import json
from pathlib import Path
from typing import Optional, Dict, Any, List
import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table

from luminoracore_cli.utils.errors import CLIError
from luminoracore_cli.utils.console import console, error_console
from luminoracore_cli.utils.files import write_json_file
from luminoracore_cli.templates import get_template, list_templates
from luminoracore_cli.core.validator import PersonalityValidator


def create_command(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Personality name"),
    archetype: Optional[str] = typer.Option(None, "--archetype", "-a", help="Personality archetype"),
    template: Optional[str] = typer.Option(None, "--template", "-t", help="Template to use"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive creation mode"),
    list_templates: bool = typer.Option(False, "--list-templates", help="List available templates"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
) -> int:
    """
    Create a new personality.
    
    This command creates a new personality definition using templates
    or interactive prompts, with validation and customization options.
    """
    try:
        # List templates if requested
        if list_templates:
            return list_available_templates()
        
        # Interactive mode
        if interactive:
            return create_interactive_personality(output=output, verbose=verbose)
        
        # Template-based creation
        if template:
            return create_from_template(template, name=name, archetype=archetype, output=output, verbose=verbose)
        
        # Quick creation with minimal parameters
        if name and archetype:
            return create_quick_personality(name, archetype, output=output, verbose=verbose)
        
        # No parameters provided, show help
        error_console.print("[red]Error: No creation method specified[/red]")
        error_console.print("Use --interactive, --template, or provide --name and --archetype")
        return 1
        
    except CLIError as e:
        error_console.print(f"[red]CLI error: {e}[/red]")
        return 1
    except Exception as e:
        error_console.print(f"[red]Unexpected error: {e}[/red]")
        if verbose:
            import traceback
            error_console.print(traceback.format_exc())
        return 1


def list_available_templates() -> int:
    """List available personality templates."""
    try:
        templates = list_templates("personality")
        
        if not templates:
            console.print("[yellow]No personality templates available[/yellow]")
            return 0
        
        console.print("[bold blue]Available Personality Templates:[/bold blue]")
        console.print("")
        
        table = Table(title="Personality Templates")
        table.add_column("Name", style="cyan")
        table.add_column("Archetype", style="magenta")
        table.add_column("Description", style="white")
        
        for template in templates:
            name = template.get("name", "Unknown")
            archetype = template.get("archetype", "Unknown")
            description = template.get("description", "No description")
            
            table.add_row(name, archetype, description)
        
        console.print(table)
        return 0
        
    except Exception as e:
        error_console.print(f"[red]Failed to list templates: {e}[/red]")
        return 1


def create_interactive_personality(output: Optional[str] = None, verbose: bool = False) -> int:
    """Create personality interactively."""
    try:
        console.print("[bold blue]Creating Personality Interactively[/bold blue]")
        console.print("")
        
        # Basic information
        name = Prompt.ask("Personality name")
        description = Prompt.ask("Description")
        author = Prompt.ask("Author", default="Developer")
        
        # Archetype selection
        archetypes = ["assistant", "scientist", "teacher", "coach", "creative", "custom"]
        console.print("\n[bold blue]Available archetypes:[/bold blue]")
        for i, arch in enumerate(archetypes, 1):
            console.print(f"  {i}. {arch}")
        
        while True:
            try:
                choice = Prompt.ask("Select archetype", default="1")
                archetype_index = int(choice) - 1
                if 0 <= archetype_index < len(archetypes):
                    archetype = archetypes[archetype_index]
                    break
                else:
                    error_console.print("[red]Invalid archetype selection[/red]")
            except ValueError:
                error_console.print("[red]Please enter a valid number[/red]")
        
        # Core traits
        console.print("\n[bold blue]Core Traits[/bold blue]")
        temperament = Prompt.ask("Temperament", default="friendly")
        communication_style = Prompt.ask("Communication style", default="clear")
        
        # Values
        values_input = Prompt.ask("Values (comma-separated)", default="helpfulness, accuracy")
        values = [v.strip() for v in values_input.split(",")]
        
        # Motivations
        motivations_input = Prompt.ask("Motivations (comma-separated)", default="assisting users, providing information")
        motivations = [m.strip() for m in motivations_input.split(",")]
        
        # Linguistic profile
        console.print("\n[bold blue]Linguistic Profile[/bold blue]")
        tone_input = Prompt.ask("Tone (comma-separated)", default="friendly, helpful")
        tone = [t.strip() for t in tone_input.split(",")]
        
        vocabulary_input = Prompt.ask("Key vocabulary (comma-separated)", default="help, assist, provide, explain")
        vocabulary = [v.strip() for v in vocabulary_input.split(",")]
        
        speech_patterns_input = Prompt.ask("Speech patterns (comma-separated)", default="I can help you, Let me assist")
        speech_patterns = [s.strip() for s in speech_patterns_input.split(",")]
        
        formality = Prompt.ask("Formality level", default="casual", choices=["casual", "professional", "formal"])
        response_length = Prompt.ask("Response length", default="moderate", choices=["short", "moderate", "detailed"])
        
        # Behavioral rules
        console.print("\n[bold blue]Behavioral Rules[/bold blue]")
        rules = []
        rule_count = 1
        
        while True:
            rule = Prompt.ask(f"Behavioral rule {rule_count} (empty to finish)", default="")
            if not rule:
                break
            rules.append(rule)
            rule_count += 1
        
        # Advanced parameters
        console.print("\n[bold blue]Advanced Parameters[/bold blue]")
        temperature = float(Prompt.ask("Temperature (0.0-1.0)", default="0.7"))
        top_p = float(Prompt.ask("Top-p (0.0-1.0)", default="0.9"))
        max_tokens = int(Prompt.ask("Max tokens", default="500"))
        
        # Create personality data
        personality_data = {
            "persona": {
                "name": name,
                "description": description,
                "archetype": archetype,
                "version": "1.0.0",
                "author": author,
                "tags": [archetype, "custom"]
            },
            "core_traits": {
                "archetype": archetype,
                "temperament": temperament,
                "communication_style": communication_style,
                "values": values,
                "motivations": motivations
            },
            "linguistic_profile": {
                "tone": tone,
                "vocabulary": vocabulary,
                "speech_patterns": speech_patterns,
                "formality_level": formality,
                "response_length": response_length
            },
            "behavioral_rules": rules,
            "advanced_parameters": {
                "temperature": temperature,
                "top_p": top_p,
                "max_tokens": max_tokens,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            }
        }
        
        # Validate personality
        if verbose:
            console.print("\n[blue]Validating personality...[/blue]")
        
        validator = PersonalityValidator()
        validation_result = validator.validate(personality_data, strict=True)
        
        if not validation_result["valid"]:
            error_console.print("[red]Validation failed:[/red]")
            for error in validation_result["errors"]:
                error_console.print(f"  [red]• {error}[/red]")
            return 1
        
        # Save personality
        if not output:
            output = f"personalities/{name.lower().replace(' ', '_')}.json"
        
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        write_json_file(output_path, personality_data)
        
        console.print("")
        console.print(Panel(
            f"[bold green]Personality '{name}' created successfully![/bold green]\n\n"
            f"Saved to: {output_path}\n\n"
            f"Next steps:\n"
            f"1. Test your personality: luminoracore test {output_path}\n"
            f"2. Compile for your provider: luminoracore compile {output_path} --provider openai\n"
            f"3. Use in your applications!",
            title="Personality Created",
            border_style="green"
        ))
        
        return 0
        
    except Exception as e:
        error_console.print(f"[red]Failed to create personality: {e}[/red]")
        return 1


def create_from_template(template: str, name: Optional[str] = None, archetype: Optional[str] = None, output: Optional[str] = None, verbose: bool = False) -> int:
    """Create personality from template."""
    try:
        # Load template
        template_data = get_template("personality", template)
        
        if verbose:
            console.print(f"[blue]Using template: {template}[/blue]")
        
        # Get template variables
        template_vars = template_data.get("template_vars", {})
        
        # Collect variable values
        collected_vars = {}
        for var_name, var_config in template_vars.items():
            var_default = var_config.get("default", "")
            
            if var_name == "name" and name:
                collected_vars[var_name] = name
            elif var_name == "archetype" and archetype:
                collected_vars[var_name] = archetype
            else:
                collected_vars[var_name] = var_default
        
        # Replace template variables
        personality_data = template_data.copy()
        
        def replace_vars(obj):
            if isinstance(obj, dict):
                return {k: replace_vars(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_vars(item) for item in obj]
            elif isinstance(obj, str):
                for var_name, var_value in collected_vars.items():
                    placeholder = f"{{{{{var_name}}}}}"
                    obj = obj.replace(placeholder, str(var_value))
                return obj
            else:
                return obj
        
        personality_data = replace_vars(personality_data)
        
        # Validate personality
        if verbose:
            console.print("[blue]Validating personality...[/blue]")
        
        validator = PersonalityValidator()
        validation_result = validator.validate(personality_data, strict=True)
        
        if not validation_result["valid"]:
            error_console.print("[red]Validation failed:[/red]")
            for error in validation_result["errors"]:
                error_console.print(f"  [red]• {error}[/red]")
            return 1
        
        # Save personality
        if not output:
            personality_name = personality_data.get("persona", {}).get("name", "personality")
            output = f"personalities/{personality_name.lower().replace(' ', '_')}.json"
        
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        write_json_file(output_path, personality_data)
        
        console.print(f"[green]✓ Created personality from template: {output_path}[/green]")
        
        return 0
        
    except Exception as e:
        error_console.print(f"[red]Failed to create personality from template: {e}[/red]")
        return 1


def create_quick_personality(name: str, archetype: str, output: Optional[str] = None, verbose: bool = False) -> int:
    """Create a quick personality with minimal parameters."""
    try:
        # Create basic personality data
        personality_data = {
            "persona": {
                "name": name,
                "description": f"A {archetype} personality created with LuminoraCore CLI",
                "archetype": archetype,
                "version": "1.0.0",
                "author": "Developer",
                "tags": [archetype, "quick-creation"]
            },
            "core_traits": {
                "archetype": archetype,
                "temperament": "helpful",
                "communication_style": "clear",
                "values": ["helpfulness", "accuracy"],
                "motivations": ["assisting users", "providing information"]
            },
            "linguistic_profile": {
                "tone": ["friendly", "helpful"],
                "vocabulary": ["help", "assist", "provide", "explain"],
                "speech_patterns": ["I can help you", "Let me assist"],
                "formality_level": "casual",
                "response_length": "moderate"
            },
            "behavioral_rules": [
                "Be helpful and friendly",
                "Provide accurate information",
                "Ask clarifying questions when needed"
            ],
            "advanced_parameters": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 500,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            }
        }
        
        # Validate personality
        if verbose:
            console.print("[blue]Validating personality...[/blue]")
        
        validator = PersonalityValidator()
        validation_result = validator.validate(personality_data, strict=True)
        
        if not validation_result["valid"]:
            error_console.print("[red]Validation failed:[/red]")
            for error in validation_result["errors"]:
                error_console.print(f"  [red]• {error}[/red]")
            return 1
        
        # Save personality
        if not output:
            output = f"personalities/{name.lower().replace(' ', '_')}.json"
        
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        write_json_file(output_path, personality_data)
        
        console.print(f"[green]✓ Created quick personality: {output_path}[/green]")
        
        return 0
        
    except Exception as e:
        error_console.print(f"[red]Failed to create quick personality: {e}[/red]")
        return 1


if __name__ == "__main__":
    typer.run(create_command)
