"""Compile command for LuminoraCore CLI."""

import asyncio
from pathlib import Path
from typing import List, Optional, Dict, Any
import typer
from rich.console import Console

from luminoracore_cli.utils.errors import CLIError, ValidationError
from luminoracore_cli.utils.console import console, error_console
from luminoracore_cli.utils.files import find_personality_files, read_json_file
from luminoracore_cli.utils.formatting import format_compilation_result
from luminoracore_cli.core.validator import PersonalityValidator
from luminoracore_cli.core.client import get_client


def compile_command(
    personality: str = typer.Argument(..., help="Personality name or file path"),
    provider: str = typer.Option("openai", "--provider", "-p", help="LLM provider (openai, anthropic, etc.)"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Specific model to compile for"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("text", "--format", "-f", help="Output format (text, json, yaml)"),
    include_metadata: bool = typer.Option(True, "--include-metadata/--no-metadata", help="Include metadata in output"),
    validate: bool = typer.Option(True, "--validate/--no-validate", help="Validate personality before compilation"),
    strict: bool = typer.Option(False, "--strict", help="Use strict validation"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
) -> int:
    """Synchronous wrapper for async compile_command_impl."""
    return asyncio.run(_compile_command_impl(
        personality=personality,
        provider=provider,
        model=model,
        output=output,
        format=format,
        include_metadata=include_metadata,
        validate=validate,
        strict=strict,
        verbose=verbose
    ))


async def _compile_command_impl(
    personality: str,
    provider: str,
    model: Optional[str],
    output: Optional[str],
    format: str,
    include_metadata: bool,
    validate: bool,
    strict: bool,
    verbose: bool
) -> int:
    """
    Compile a personality to provider-specific prompts.
    
    This command takes a personality definition and compiles it to a prompt
    format suitable for the specified LLM provider and model.
    """
    try:
        # Find personality file - check if it's a direct path first
        personality_path = Path(personality)
        if not personality_path.exists():
            # Try to find by name
            found_paths = find_personality_files(personality)
            if not found_paths:
                error_console.print(f"[red]Error: Personality '{personality}' not found[/red]")
                raise typer.Exit(1)
            personality_path = found_paths[0] if isinstance(found_paths, list) else found_paths
        
        if verbose:
            console.print(f"[blue]Found personality file: {personality_path}[/blue]")
        
        # Load personality data
        try:
            personality_data = read_json_file(personality_path)
        except Exception as e:
            error_console.print(f"[red]Error loading personality file: {e}[/red]")
            raise typer.Exit(1)
        
        # Validate personality if requested
        if validate:
            if verbose:
                console.print("[blue]Validating personality...[/blue]")
            
            validator = PersonalityValidator()
            validation_result = validator.validate(personality_data, strict=strict)
            
            if not validation_result["valid"]:
                error_console.print("[red]Validation failed:[/red]")
                for error in validation_result["errors"]:
                    error_console.print(f"  [red]• {error}[/red]")
                raise typer.Exit(1)
            
            if verbose:
                console.print("[green]✓ Personality validation passed[/green]")
        
        # Get client and compile personality
        if verbose:
            console.print(f"[blue]Compiling for provider: {provider}[/blue]")
        
        client = get_client()
        
        # Compile personality
        compilation_result = await client.compile_personality(
            personality_data=personality_data,
            provider=provider,
            model=model,
            include_metadata=include_metadata
        )
        
        if verbose:
            console.print("[green]✓ Compilation completed[/green]")
        
        # Format output
        if format == "text":
            output_text = format_compilation_result(compilation_result)
        elif format == "json":
            import json
            output_text = json.dumps(compilation_result, indent=2)
        elif format == "yaml":
            import yaml
            output_text = yaml.dump(compilation_result, default_flow_style=False)
        else:
            error_console.print(f"[red]Error: Unsupported format '{format}'[/red]")
            raise typer.Exit(1)
        
        # Output result
        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(output_text)
            
            console.print(f"[green]✓ Compiled prompt saved to: {output_path}[/green]")
        else:
            console.print(output_text)
        
        return 0
        
    except ValidationError as e:
        error_console.print(f"[red]Validation error: {e}[/red]")
        raise typer.Exit(1)
    except CLIError as e:
        error_console.print(f"[red]CLI error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        error_console.print(f"[red]Unexpected error: {e}[/red]")
        if verbose:
            import traceback
            error_console.print(traceback.format_exc())
        raise typer.Exit(1)


if __name__ == "__main__":
    typer.run(compile_command)
