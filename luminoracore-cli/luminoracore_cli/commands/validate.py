"""Validation command implementation."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List, Optional, Tuple

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel

from ..core.validator import PersonalityValidator
from ..core.client import LuminoraCoreClient
from ..utils.console import console, error_console
from ..utils.files import find_personality_files, read_file
from ..utils.errors import CLIError, ValidationError


def get_client() -> LuminoraCoreClient:
    """Get a configured LuminoraCore client instance."""
    return LuminoraCoreClient()


def validate_command(
    files: List[Path] = typer.Argument(
        ...,
        help="Personality files to validate",
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True,
    ),
    schema_url: Optional[str] = typer.Option(
        None,
        "--schema",
        "-s",
        help="Custom schema URL or file path",
    ),
    strict: bool = typer.Option(
        False,
        "--strict",
        help="Enable strict validation mode",
    ),
    format: str = typer.Option(
        "table",
        "--format",
        "-f",
        help="Output format",
        # Typer v0.9 no expone Choice; validaremos manualmente más abajo
    ),
    output_file: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Save results to file",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Only show errors",
    ),
    parallel: bool = typer.Option(
        True,
        "--parallel/--sequential",
        help="Process files in parallel",
    ),
    max_workers: int = typer.Option(
        4,
        "--max-workers",
        help="Maximum parallel workers",
        min=1,
        max=16,
    ),
) -> None:
    """Synchronous wrapper for async validate_command_impl."""
    asyncio.run(_validate_command_impl(
        files=files,
        schema_url=schema_url,
        strict=strict,
        format=format,
        output_file=output_file,
        quiet=quiet,
        parallel=parallel,
        max_workers=max_workers
    ))


async def _validate_command_impl(
    files: List[Path],
    schema_url: Optional[str],
    strict: bool,
    format: str,
    output_file: Optional[Path],
    quiet: bool,
    parallel: bool,
    max_workers: int,
) -> None:
    """
    Validate personality files against the LuminoraCore schema.
    
    This command validates one or more personality files to ensure they conform
    to the official LuminoraCore personality schema. It can process individual
    files or recursively scan directories.
    
    Examples:
        luminoracore validate personality.json
        luminoracore validate personalities/ --strict
        luminoracore validate *.json --format json --output results.json
        luminoracore validate personalities/ --quiet
    
    The validator checks:
    • JSON schema compliance
    • Required field presence
    • Data type correctness
    • Value range validation
    • Content coherence
    • Best practice adherence
    """
    try:
        # Validate format option
        allowed_formats = {"table", "json", "yaml", "text"}
        if format not in allowed_formats:
            error_console.print(f"[red]Invalid format '{format}'. Use one of: {', '.join(sorted(allowed_formats))}[/red]")
            raise typer.Exit(2)

        # Collect all personality files
        all_files = []
        for file_path in files:
            # Convert string to Path if needed
            if isinstance(file_path, str):
                file_path = Path(file_path)
            
            if file_path.is_dir():
                found_files = find_personality_files(file_path)
                all_files.extend(found_files)
            else:
                all_files.append(file_path)
        
        if not all_files:
            error_console.print("[red]No personality files found[/red]")
            raise typer.Exit(1)
        
        # Initialize validator
        validator = PersonalityValidator()
        
        if not quiet:
            console.print(f"[blue]Validating {len(all_files)} file(s)...[/blue]")
        
        # Process files
        if parallel and len(all_files) > 1:
            results = await _validate_files_parallel(
                validator, all_files, max_workers, quiet
            )
        else:
            results = await _validate_files_sequential(
                validator, all_files, quiet
            )
        
        # Generate output
        await _output_results(results, format, output_file, quiet)
        
        # Exit with appropriate code
        errors = sum(1 for _, _, success, _ in results if not success)
        if errors > 0:
            if not quiet:
                error_console.print(f"[red]Validation failed: {errors} error(s)[/red]")
            raise typer.Exit(1)
        else:
            if not quiet:
                console.print("[green]✓ All files passed validation[/green]")
    
    except Exception as e:
        error_console.print(f"[red]Validation error: {e}[/red]")
        raise typer.Exit(1)


async def _validate_files_parallel(
    validator: PersonalityValidator,
    files: List[Path],
    max_workers: int,
    quiet: bool,
) -> List[Tuple[Path, str, bool, Optional[str]]]:
    """Validate files in parallel with progress display."""
    
    async def validate_single_file(file_path: Path) -> Tuple[Path, str, bool, Optional[str]]:
        try:
            personality_data = read_file(file_path)
            result = validator.validate(personality_data, strict=False)
            
            if result.get("valid", False):
                name = personality_data.get("persona", {}).get("name", "Unknown")
                return file_path, name, True, None
            else:
                error_msg = "\n".join([
                    f"• {error}"
                    for error in result.get("errors", [])
                ])
                return file_path, "Invalid", False, error_msg
                
        except Exception as e:
            return file_path, "Error", False, str(e)
    
    # Use semaphore to limit concurrent operations
    semaphore = asyncio.Semaphore(max_workers)
    
    async def validate_with_semaphore(file_path: Path):
        async with semaphore:
            return await validate_single_file(file_path)
    
    # Show progress if not quiet
    if not quiet:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task("Validating files...", total=len(files))
            
            results = []
            tasks = [validate_with_semaphore(file_path) for file_path in files]
            
            for coro in asyncio.as_completed(tasks):
                result = await coro
                results.append(result)
                progress.advance(task)
            
            return results
    else:
        # No progress display
        tasks = [validate_with_semaphore(file_path) for file_path in files]
        return await asyncio.gather(*tasks)


async def _validate_files_sequential(
    validator: PersonalityValidator,
    files: List[Path],
    quiet: bool,
) -> List[Tuple[Path, str, bool, Optional[str]]]:
    """Validate files sequentially."""
    
    results = []
    
    for file_path in files:
        try:
            personality_data = read_file(file_path)
            result = validator.validate(personality_data, strict=False)
            
            if result.get("valid", False):
                name = personality_data.get("persona", {}).get("name", "Unknown")
                results.append((file_path, name, True, None))
            else:
                error_msg = "\n".join([
                    f"• {error}"
                    for error in result.get("errors", [])
                ])
                results.append((file_path, "Invalid", False, error_msg))
                
        except Exception as e:
            results.append((file_path, "Error", False, str(e)))
    
    return results


async def _output_results(
    results: List[Tuple[Path, str, bool, Optional[str]]],
    format: str,
    output_file: Optional[Path],
    quiet: bool,
) -> None:
    """Output validation results in specified format."""
    
    if format == "table":
        _output_table(results, quiet)
    elif format == "json":
        _output_json(results, output_file, quiet)
    elif format == "yaml":
        _output_yaml(results, output_file, quiet)
    else:  # text
        _output_text(results, quiet)


def _output_table(results: List[Tuple[Path, str, bool, Optional[str]]], quiet: bool) -> None:
    """Output results as a table."""
    
    table = Table(
        title="Validation Results",
        show_header=True,
        header_style="bold magenta",
    )
    
    table.add_column("File", style="cyan", no_wrap=True)
    table.add_column("Name", style="white")
    table.add_column("Status", justify="center")
    table.add_column("Details", style="dim")
    
    for file_path, name, success, error_msg in results:
        status = "[green]✓ Valid[/green]" if success else "[red]✗ Invalid[/red]"
        details = error_msg if error_msg else "No issues found"
        
        table.add_row(
            str(file_path),
            name,
            status,
            details
        )
    
    console.print(table)


def _output_json(results: List[Tuple[Path, str, bool, Optional[str]]], output_file: Optional[Path], quiet: bool) -> None:
    """Output results as JSON."""
    
    import json
    
    output_data = {
        "summary": {
            "total_files": len(results),
            "valid_files": sum(1 for _, _, success, _ in results if success),
            "invalid_files": sum(1 for _, _, success, _ in results if not success),
        },
        "results": [
            {
                "file": str(file_path),
                "name": name,
                "valid": success,
                "errors": error_msg.split('\n') if error_msg else []
            }
            for file_path, name, success, error_msg in results
        ]
    }
    
    json_output = json.dumps(output_data, indent=2)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_output)
        if not quiet:
            console.print(f"[green]Results saved to {output_file}[/green]")
    else:
        console.print(json_output)


def _output_yaml(results: List[Tuple[Path, str, bool, Optional[str]]], output_file: Optional[Path], quiet: bool) -> None:
    """Output results as YAML."""
    
    import yaml
    
    output_data = {
        "summary": {
            "total_files": len(results),
            "valid_files": sum(1 for _, _, success, _ in results if success),
            "invalid_files": sum(1 for _, _, success, _ in results if not success),
        },
        "results": [
            {
                "file": str(file_path),
                "name": name,
                "valid": success,
                "errors": error_msg.split('\n') if error_msg else []
            }
            for file_path, name, success, error_msg in results
        ]
    }
    
    yaml_output = yaml.dump(output_data, default_flow_style=False, indent=2)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(yaml_output)
        if not quiet:
            console.print(f"[green]Results saved to {output_file}[/green]")
    else:
        console.print(yaml_output)


def _output_text(results: List[Tuple[Path, str, bool, Optional[str]]], quiet: bool) -> None:
    """Output results as plain text."""
    
    for file_path, name, success, error_msg in results:
        status = "[OK] VALID" if success else "[ERROR] INVALID"
        console.print(f"{status}: {file_path}")
        
        if not success and error_msg:
            for line in error_msg.split('\n'):
                console.print(f"  {line}")
        
        console.print()
