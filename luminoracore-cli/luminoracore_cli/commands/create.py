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
from luminoracore_cli.templates.loader import TemplateType
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
    """Create personality interactively with 10-step wizard."""
    try:
        console.print(Panel(
            "[bold blue]🎭 PERSONALITY CREATION WIZARD[/bold blue]\n\n"
            "This wizard will help you create a new personality.\n"
            "Press Ctrl+C at any time to cancel.",
            title="LuminoraCore Wizard",
            border_style="blue"
        ))
        console.print("")
        
        # Step 1: Basic Information
        console.print(Panel(
            "[bold]Step 1/10: Basic Information[/bold]",
            border_style="yellow"
        ))
        
        name = prompt_with_validation(
            "Personality name",
            validate_name,
            "Please enter a valid name (2-50 characters)"
        )
        
        description = prompt_with_validation(
            "Description (min 50 characters)",
            lambda x: len(x) >= 50,
            "Description must be at least 50 characters long"
        )
        
        author = Prompt.ask("Author (optional, press Enter to skip)", default="")
        if not author:
            author = "LuminoraCore User"
        
        tags_input = Prompt.ask("Tags (comma-separated, e.g., helpful, friendly)", default="")
        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] if tags_input else []
        
        # Step 2: Core Traits
        console.print(Panel(
            "[bold]Step 2/10: Core Traits[/bold]",
            border_style="yellow"
        ))
        
        archetype = select_from_list(
            "Archetype (e.g., The Helper, The Innovator, The Guide)",
            [
                "The Helper", "The Innovator", "The Guide", "The Teacher",
                "The Mentor", "The Creative", "The Analyst", "The Leader",
                "The Friend", "The Expert", "Custom"
            ]
        )
        
        if archetype == "Custom":
            archetype = Prompt.ask("Enter custom archetype")
        
        temperament = Prompt.ask("Temperament (e.g., Calm and patient, Energetic and motivated)", default="Friendly and helpful")
        communication_style = Prompt.ask("Communication style (e.g., Direct and concise, Warm and detailed)", default="Clear and organized")
        
        # Step 3: Tone
        console.print(Panel(
            "[bold]Step 3/10: Tone[/bold]",
            border_style="yellow"
        ))
        
        num_tones = prompt_int("How many tones to define? (recommended 3-5)", default=4, min_val=1, max_val=10)
        tones = []
        
        for i in range(num_tones):
            tone = Prompt.ask(f"Tone {i+1}")
            if tone:
                tones.append(tone)
        
        # Step 4: Vocabulary
        console.print(Panel(
            "[bold]Step 4/10: Vocabulary[/bold]",
            border_style="yellow"
        ))
        
        console.print("Enter characteristic phrases (one per line, press Enter twice to finish):")
        phrases = []
        phrase_count = 1
        
        while True:
            phrase = Prompt.ask(f"Phrase {phrase_count}", default="")
            if not phrase:
                break
            phrases.append(phrase)
            phrase_count += 1
        
        console.print(f"✓ Added {len(phrases)} phrases")
        
        # Step 5: Behavioral Rules
        console.print(Panel(
            "[bold]Step 5/10: Behavioral Rules[/bold]",
            border_style="yellow"
        ))
        
        console.print("Enter behavioral rules (one per line, press Enter twice to finish):")
        rules = []
        rule_count = 1
        
        while True:
            rule = Prompt.ask(f"Rule {rule_count}", default="")
            if not rule:
                break
            rules.append(rule)
            rule_count += 1
        
        console.print(f"✓ Added {len(rules)} rules")
        
        # Step 6: Advanced Parameters
        console.print(Panel(
            "[bold]Step 6/10: Advanced Parameters[/bold]",
            border_style="yellow"
        ))
        
        console.print("Set advanced parameters (0.0 - 1.0)")
        
        verbosity = prompt_float("Verbosity (how detailed, 0=brief, 1=very detailed)", default=0.5)
        formality = prompt_float("Formality (0=casual, 1=formal)", default=0.5)
        humor = prompt_float("Humor (0=serious, 1=humorous)", default=0.5)
        empathy = prompt_float("Empathy (0=neutral, 1=very empathetic)", default=0.5)
        creativity = prompt_float("Creativity (0=structured, 1=creative)", default=0.5)
        directness = prompt_float("Directness (0=indirect, 1=direct)", default=0.5)
        
        # Step 7: Trigger Responses
        console.print(Panel(
            "[bold]Step 7/10: Trigger Responses (Optional)[/bold]",
            border_style="yellow"
        ))
        
        greetings = []
        if Confirm.ask("Add greeting responses?", default=True):
            console.print("Enter greeting responses (one per line, press Enter twice to finish):")
            greeting_count = 1
            while True:
                greeting = Prompt.ask(f"Greeting {greeting_count}", default="")
                if not greeting:
                    break
                greetings.append(greeting)
                greeting_count += 1
        
        goodbyes = []
        if Confirm.ask("Add goodbye responses?", default=True):
            console.print("Enter goodbye responses (one per line, press Enter twice to finish):")
            goodbye_count = 1
            while True:
                goodbye = Prompt.ask(f"Goodbye {goodbye_count}", default="")
                if not goodbye:
                    break
                goodbyes.append(goodbye)
                goodbye_count += 1
        
        confusion_responses = []
        if Confirm.ask("Add confusion responses?", default=False):
            console.print("Enter confusion responses (one per line, press Enter twice to finish):")
            confusion_count = 1
            while True:
                confusion = Prompt.ask(f"Confusion response {confusion_count}", default="")
                if not confusion:
                    break
                confusion_responses.append(confusion)
                confusion_count += 1
        
        success_responses = []
        if Confirm.ask("Add success responses?", default=False):
            console.print("Enter success responses (one per line, press Enter twice to finish):")
            success_count = 1
            while True:
                success = Prompt.ask(f"Success response {success_count}", default="")
                if not success:
                    break
                success_responses.append(success)
                success_count += 1
        
        error_responses = []
        if Confirm.ask("Add error responses?", default=False):
            console.print("Enter error responses (one per line, press Enter twice to finish):")
            error_count = 1
            while True:
                error = Prompt.ask(f"Error response {error_count}", default="")
                if not error:
                    break
                error_responses.append(error)
                error_count += 1
        
        # Step 8: Safety Guards
        console.print(Panel(
            "[bold]Step 8/10: Safety Guards (Optional)[/bold]",
            border_style="yellow"
        ))
        
        forbidden_topics = []
        if Confirm.ask("Add forbidden topics?", default=False):
            console.print("Enter forbidden topics (one per line, press Enter twice to finish):")
            topic_count = 1
            while True:
                topic = Prompt.ask(f"Forbidden topic {topic_count}", default="")
                if not topic:
                    break
                forbidden_topics.append(topic)
                topic_count += 1
        
        content_filters = []
        if Confirm.ask("Add content filters?", default=False):
            console.print("Enter content filters (one per line, press Enter twice to finish):")
            filter_count = 1
            while True:
                filter_item = Prompt.ask(f"Content filter {filter_count}", default="")
                if not filter_item:
                    break
                content_filters.append(filter_item)
                filter_count += 1
        
        # Step 9: Examples
        console.print(Panel(
            "[bold]Step 9/10: Examples (Optional)[/bold]",
            border_style="yellow"
        ))
        
        examples = []
        if Confirm.ask("Add example interactions?", default=False):
            console.print("Enter example interactions (one per line, press Enter twice to finish):")
            example_count = 1
            while True:
                input_text = Prompt.ask(f"Example input {example_count}", default="")
                if not input_text:
                    break
                output_text = Prompt.ask(f"Example output {example_count}", default="")
                if output_text:
                    examples.append({
                        "input": input_text,
                        "output": output_text
                    })
                example_count += 1
        
        # Step 10: Review & Save
        console.print(Panel(
            "[bold]Step 10/10: Review & Save[/bold]",
            border_style="yellow"
        ))
        
        # Show summary
        show_personality_summary(
            name, description, author, tags, archetype, temperament, 
            communication_style, tones, phrases, rules, verbosity, 
            formality, humor, empathy, creativity, directness,
            greetings, goodbyes, confusion_responses, success_responses, 
            error_responses, forbidden_topics, content_filters, examples
        )
        
        if not Confirm.ask("Save this personality?", default=True):
            console.print("[yellow]Personality creation cancelled.[/yellow]")
            return 0
        
        # Generate filename
        if not output:
            output = f"{name.lower().replace(' ', '_')}.json"
        
        # Create personality data
        personality_data = create_personality_data(
            name, description, author, tags, archetype, temperament,
            communication_style, tones, phrases, rules, verbosity,
            formality, humor, empathy, creativity, directness,
            greetings, goodbyes, confusion_responses, success_responses,
            error_responses, forbidden_topics, content_filters, examples
        )
        
        # Validate personality
        if verbose:
            console.print("\n[blue]Validating personality...[/blue]")
        
        validator = PersonalityValidator()
        validation_result = validator.validate(personality_data)
        
        if not validation_result.is_valid:
            error_console.print("[red]Validation failed:[/red]")
            for error in validation_result.errors:
                error_console.print(f"  [red]• {error}[/red]")
            return 1
        
        # Save personality
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        write_json_file(output_path, personality_data)
        
        console.print("")
        console.print(Panel(
            f"[bold green]✅ Personality created successfully![/bold green]\n\n"
            f"File: {output_path}\n\n"
            f"Next steps:\n"
            f"• Test it: luminoracore test {output_path}\n"
            f"• Compile it: luminoracore compile {output_path}\n"
            f"• Edit manually: Open {output_path} in your editor",
            title="Personality Created",
            border_style="green"
        ))
        
        return 0
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Personality creation cancelled by user.[/yellow]")
        return 0
    except Exception as e:
        error_console.print(f"[red]Failed to create personality: {e}[/red]")
        if verbose:
            import traceback
            error_console.print(traceback.format_exc())
        return 1


def create_from_template(template: str, name: Optional[str] = None, archetype: Optional[str] = None, output: Optional[str] = None, verbose: bool = False) -> int:
    """Create personality from template."""
    try:
        # Load template
        template_data = get_template(template, TemplateType.PERSONALITY)
        
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
        
        # Override name if provided
        if name and "persona" in personality_data:
            personality_data["persona"]["name"] = name
        
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


# Helper functions for the wizard
def validate_name(name: str) -> bool:
    """Validate personality name."""
    return 2 <= len(name) <= 50 and name.strip() == name

def prompt_with_validation(prompt_text: str, validator, error_message: str) -> str:
    """Prompt with validation."""
    while True:
        value = Prompt.ask(prompt_text)
        if validator(value):
            return value
        error_console.print(f"[red]❌ {error_message}[/red]")

def select_from_list(prompt_text: str, options: List[str]) -> str:
    """Select from a list of options."""
    console.print(f"\n[bold blue]{prompt_text}:[/bold blue]")
    for i, option in enumerate(options, 1):
        console.print(f"  {i}. {option}")
    
    while True:
        try:
            choice = Prompt.ask("Select option", default="1")
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(options):
                return options[choice_index]
            else:
                error_console.print("[red]Invalid selection[/red]")
        except ValueError:
            error_console.print("[red]Please enter a valid number[/red]")

def prompt_int(prompt_text: str, default: int = 1, min_val: int = 1, max_val: int = 10) -> int:
    """Prompt for integer with validation."""
    while True:
        try:
            value = int(Prompt.ask(prompt_text, default=str(default)))
            if min_val <= value <= max_val:
                return value
            else:
                error_console.print(f"[red]Value must be between {min_val} and {max_val}[/red]")
        except ValueError:
            error_console.print("[red]Please enter a valid number[/red]")

def prompt_float(prompt_text: str, default: float = 0.5) -> float:
    """Prompt for float with validation."""
    while True:
        try:
            value = float(Prompt.ask(prompt_text, default=str(default)))
            if 0.0 <= value <= 1.0:
                return value
            else:
                error_console.print("[red]Value must be between 0.0 and 1.0[/red]")
        except ValueError:
            error_console.print("[red]Please enter a valid number[/red]")

def show_personality_summary(
    name: str, description: str, author: str, tags: List[str], archetype: str,
    temperament: str, communication_style: str, tones: List[str], phrases: List[str],
    rules: List[str], verbosity: float, formality: float, humor: float, empathy: float,
    creativity: float, directness: float, greetings: List[str], goodbyes: List[str],
    confusion_responses: List[str], success_responses: List[str], error_responses: List[str],
    forbidden_topics: List[str], content_filters: List[str], examples: List[dict]
) -> None:
    """Show personality summary before saving."""
    console.print(Panel(
        "[bold]📋 PERSONALITY SUMMARY[/bold]",
        border_style="green"
    ))
    
    table = Table(title="Personality Details")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Name", name)
    table.add_row("Description", description[:100] + "..." if len(description) > 100 else description)
    table.add_row("Author", author)
    table.add_row("Tags", ", ".join(tags) if tags else "None")
    table.add_row("Archetype", archetype)
    table.add_row("Temperament", temperament)
    table.add_row("Communication Style", communication_style)
    table.add_row("Tones", ", ".join(tones) if tones else "None")
    table.add_row("Phrases", f"{len(phrases)} defined")
    table.add_row("Rules", f"{len(rules)} defined")
    table.add_row("Verbosity", f"{verbosity:.1f}")
    table.add_row("Formality", f"{formality:.1f}")
    table.add_row("Humor", f"{humor:.1f}")
    table.add_row("Empathy", f"{empathy:.1f}")
    table.add_row("Creativity", f"{creativity:.1f}")
    table.add_row("Directness", f"{directness:.1f}")
    table.add_row("Greetings", f"{len(greetings)} defined")
    table.add_row("Goodbyes", f"{len(goodbyes)} defined")
    table.add_row("Confusion Responses", f"{len(confusion_responses)} defined")
    table.add_row("Success Responses", f"{len(success_responses)} defined")
    table.add_row("Error Responses", f"{len(error_responses)} defined")
    table.add_row("Forbidden Topics", f"{len(forbidden_topics)} defined")
    table.add_row("Content Filters", f"{len(content_filters)} defined")
    table.add_row("Examples", f"{len(examples)} defined")
    
    console.print(table)

def create_personality_data(
    name: str, description: str, author: str, tags: List[str], archetype: str,
    temperament: str, communication_style: str, tones: List[str], phrases: List[str],
    rules: List[str], verbosity: float, formality: float, humor: float, empathy: float,
    creativity: float, directness: float, greetings: List[str], goodbyes: List[str],
    confusion_responses: List[str], success_responses: List[str], error_responses: List[str],
    forbidden_topics: List[str], content_filters: List[str], examples: List[dict]
) -> Dict[str, Any]:
    """Create personality data structure."""
    return {
        "persona": {
            "name": name,
            "description": description,
            "archetype": archetype,
            "version": "1.0.0",
            "author": author,
            "tags": tags
        },
        "core_traits": {
            "archetype": archetype,
            "temperament": temperament,
            "communication_style": communication_style
        },
        "linguistic_profile": {
            "tone": tones,
            "vocabulary": phrases,
            "speech_patterns": phrases,  # Use phrases as speech patterns
            "formality_level": "casual" if formality < 0.3 else "professional" if formality < 0.7 else "formal",
            "response_length": "short" if verbosity < 0.3 else "moderate" if verbosity < 0.7 else "detailed"
        },
        "behavioral_rules": rules,
        "trigger_responses": {
            "on_greeting": greetings,
            "on_goodbye": goodbyes,
            "on_confusion": confusion_responses,
            "on_success": success_responses,
            "on_error": error_responses
        },
        "safety_guards": {
            "forbidden_topics": forbidden_topics,
            "content_filters": content_filters
        },
        "examples": {
            "sample_responses": examples
        },
        "advanced_parameters": {
            "verbosity": verbosity,
            "formality": formality,
            "humor": humor,
            "empathy": empathy,
            "creativity": creativity,
            "directness": directness,
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 500,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }
    }


if __name__ == "__main__":
    typer.run(create_command)
