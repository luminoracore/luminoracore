"""
Command-line interface for LuminoraCore.
"""

import json
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
import click
import colorama
from colorama import Fore, Style

from ..core.personality import Personality, PersonalityError
from ..tools.validator import PersonalityValidator
from ..tools.compiler import PersonalityCompiler, LLMProvider
from ..tools.blender import PersonaBlend, BlendWeights

# Initialize colorama
colorama.init()

# CLI version
__version__ = "0.1.0"


def print_success(message: str) -> None:
    """Print success message in green."""
    click.echo(f"{Fore.GREEN}[OK] {message}{Style.RESET_ALL}")


def print_error(message: str) -> None:
    """Print error message in red."""
    click.echo(f"{Fore.RED}[ERROR] {message}{Style.RESET_ALL}")


def print_warning(message: str) -> None:
    """Print warning message in yellow."""
    click.echo(f"{Fore.YELLOW}[WARNING] {message}{Style.RESET_ALL}")


def print_info(message: str) -> None:
    """Print info message in blue."""
    click.echo(f"{Fore.BLUE}[INFO] {message}{Style.RESET_ALL}")


@click.group()
@click.version_option(version=__version__)
def cli():
    """LuminoraCore - Universal AI Personality Management Standard."""
    pass


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--verbose', '-v', is_flag=True, help='Show detailed validation results')
def validate(file_path: str, verbose: bool):
    """Validate a personality file."""
    try:
        validator = PersonalityValidator()
        result = validator.validate(file_path)
        
        if result.is_valid:
            print_success(f"Personality file is valid: {file_path}")
            if verbose:
                if result.warnings:
                    print_warning(f"Warnings ({len(result.warnings)}):")
                    for warning in result.warnings:
                        click.echo(f"  • {warning}")
                
                if result.suggestions:
                    print_info(f"Suggestions ({len(result.suggestions)}):")
                    for suggestion in result.suggestions:
                        click.echo(f"  • {suggestion}")
        else:
            print_error(f"Personality file is invalid: {file_path}")
            for error in result.errors:
                print_error(f"  • {error}")
            
            if result.warnings:
                print_warning(f"Warnings ({len(result.warnings)}):")
                for warning in result.warnings:
                    click.echo(f"  • {warning}")
            
            sys.exit(1)
            
    except Exception as e:
        print_error(f"Validation failed: {e}")
        sys.exit(1)


@cli.command()
@click.argument('directory', type=click.Path(exists=True))
@click.option('--verbose', '-v', is_flag=True, help='Show detailed results for each file')
def validate_all(directory: str, verbose: bool):
    """Validate all personality files in a directory."""
    try:
        validator = PersonalityValidator()
        results = validator.validate_directory(directory)
        
        if not results:
            print_warning(f"No JSON files found in {directory}")
            return
        
        summary = validator.get_validation_summary(results)
        
        click.echo(f"\nValidation Summary for {directory}:")
        click.echo(f"  Total files: {summary['total_files']}")
        print_success(f"  Valid files: {summary['valid_files']}")
        if summary['invalid_files'] > 0:
            print_error(f"  Invalid files: {summary['invalid_files']}")
        
        if verbose:
            click.echo(f"\nDetailed Results:")
            for filename, result in results.items():
                if result.is_valid:
                    print_success(f"  {filename}")
                else:
                    print_error(f"  {filename}")
                    for error in result.errors:
                        click.echo(f"    • {error}")
        
        if summary['invalid_files'] > 0:
            sys.exit(1)
            
    except Exception as e:
        print_error(f"Validation failed: {e}")
        sys.exit(1)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--provider', '-p', type=click.Choice([p.value for p in LLMProvider]), 
              default='openai', help='LLM provider to compile for')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--max-tokens', type=int, help='Maximum token limit')
def compile_prompt(file_path: str, provider: str, output: Optional[str], max_tokens: Optional[int]):
    """Compile a personality into a provider-specific prompt."""
    try:
        personality = Personality(file_path)
        compiler = PersonalityCompiler()
        
        provider_enum = LLMProvider(provider)
        result = compiler.compile(personality, provider_enum, max_tokens)
        
        if output:
            compiler.save_compiled(result, output)
            print_success(f"Compiled prompt saved to: {output}")
        else:
            if isinstance(result.prompt, dict):
                click.echo(json.dumps(result.prompt, indent=2))
            else:
                click.echo(result.prompt)
        
        print_info(f"Token estimate: {result.token_estimate}")
        
    except Exception as e:
        print_error(f"Compilation failed: {e}")
        sys.exit(1)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output-dir', '-o', type=click.Path(), default='./compiled', 
              help='Output directory for compiled prompts')
@click.option('--max-tokens', type=int, help='Maximum token limit')
def compile_all(file_path: str, output_dir: str, max_tokens: Optional[int]):
    """Compile a personality for all supported providers."""
    try:
        personality = Personality(file_path)
        compiler = PersonalityCompiler()
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = compiler.compile_all_providers(personality)
        
        for provider, result in results.items():
            filename = f"{personality.persona.name.lower().replace(' ', '_')}_{provider.value}.json"
            if provider == LLMProvider.ANTHROPIC:
                filename = filename.replace('.json', '.txt')
            
            output_file = output_path / filename
            compiler.save_compiled(result, output_file)
            print_success(f"Compiled for {provider.value}: {output_file}")
        
        print_info(f"All prompts compiled to: {output_dir}")
        
    except Exception as e:
        print_error(f"Compilation failed: {e}")
        sys.exit(1)


@cli.command()
@click.argument('personality_files', nargs=-1, type=click.Path(exists=True))
@click.option('--weights', '-w', help='Comma-separated weights for each personality (e.g., "0.6,0.4")')
@click.option('--strategy', '-s', type=click.Choice(['weighted_average', 'dominant', 'hybrid', 'random']), 
              default='weighted_average', help='Blending strategy')
@click.option('--name', '-n', help='Name for the blended personality')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def blend(personality_files: List[str], weights: Optional[str], strategy: str, name: Optional[str], output: Optional[str]):
    """Blend multiple personalities together."""
    try:
        if len(personality_files) < 2:
            print_error("Need at least 2 personality files to blend")
            sys.exit(1)
        
        # Load personalities
        personalities = [Personality(file_path) for file_path in personality_files]
        
        # Parse weights
        if weights:
            weight_values = [float(w.strip()) for w in weights.split(',')]
            if len(weight_values) != len(personality_files):
                print_error("Number of weights must match number of personality files")
                sys.exit(1)
            weights_dict = {p.persona.name: w for p, w in zip(personalities, weight_values)}
        else:
            # Equal weights
            weights_dict = {p.persona.name: 1.0 for p in personalities}
        
        # Blend personalities
        blender = PersonaBlend()
        result = blender.blend(personalities, weights_dict, strategy, name)
        
        if output:
            result.blended_personality.save(output)
            print_success(f"Blended personality saved to: {output}")
        else:
            click.echo(result.blended_personality.to_json(indent=2))
        
        print_info(f"Blending strategy: {strategy}")
        print_info(f"Source personalities: {', '.join(result.blend_info['source_personalities'])}")
        
    except Exception as e:
        print_error(f"Blending failed: {e}")
        sys.exit(1)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
def info(file_path: str):
    """Display information about a personality."""
    try:
        personality = Personality(file_path)
        
        click.echo(f"\n{Fore.CYAN}Personality Information{Style.RESET_ALL}")
        click.echo(f"Name: {personality.persona.name}")
        click.echo(f"Version: {personality.persona.version}")
        click.echo(f"Author: {personality.persona.author}")
        click.echo(f"Language: {personality.persona.language}")
        click.echo(f"Description: {personality.persona.description}")
        
        click.echo(f"\n{Fore.CYAN}Core Traits{Style.RESET_ALL}")
        click.echo(f"Archetype: {personality.core_traits.archetype}")
        click.echo(f"Temperament: {personality.core_traits.temperament}")
        click.echo(f"Communication Style: {personality.core_traits.communication_style}")
        
        click.echo(f"\n{Fore.CYAN}Linguistic Profile{Style.RESET_ALL}")
        click.echo(f"Tone: {', '.join(personality.linguistic_profile.tone)}")
        click.echo(f"Syntax: {personality.linguistic_profile.syntax}")
        click.echo(f"Vocabulary: {', '.join(personality.linguistic_profile.vocabulary[:5])}...")
        
        click.echo(f"\n{Fore.CYAN}Compatibility{Style.RESET_ALL}")
        click.echo(f"Providers: {', '.join(personality.persona.compatibility)}")
        
        click.echo(f"\n{Fore.CYAN}Tags{Style.RESET_ALL}")
        click.echo(f"Tags: {', '.join(personality.persona.tags)}")
        
        if personality.examples and personality.examples.sample_responses:
            click.echo(f"\n{Fore.CYAN}Examples{Style.RESET_ALL}")
            for i, example in enumerate(personality.examples.sample_responses[:2], 1):
                click.echo(f"Example {i}:")
                click.echo(f"  Input: {example.input}")
                click.echo(f"  Output: {example.output}")
        
    except Exception as e:
        print_error(f"Failed to read personality: {e}")
        sys.exit(1)


@cli.command()
@click.argument('directory', type=click.Path(exists=True))
def list_personalities(directory: str):
    """List all personalities in a directory."""
    try:
        directory_path = Path(directory)
        json_files = list(directory_path.glob("*.json"))
        
        if not json_files:
            print_warning(f"No JSON files found in {directory}")
            return
        
        click.echo(f"\n{Fore.CYAN}Personalities in {directory}{Style.RESET_ALL}")
        
        for file_path in sorted(json_files):
            try:
                personality = Personality(file_path)
                click.echo(f"{personality.persona.name} ({personality.persona.version}) - {personality.persona.description}")
            except Exception as e:
                print_error(f"Failed to read {file_path.name}: {e}")
        
    except Exception as e:
        print_error(f"Failed to list personalities: {e}")
        sys.exit(1)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--provider', '-p', type=click.Choice([p.value for p in LLMProvider]), 
              default='openai', help='LLM provider to test with')
def test_compilation(file_path: str, provider: str):
    """Test compilation for a specific provider."""
    try:
        personality = Personality(file_path)
        compiler = PersonalityCompiler()
        
        provider_enum = LLMProvider(provider)
        result = compiler.compile(personality, provider_enum)
        
        print_success(f"Compilation successful for {provider}")
        print_info(f"Token estimate: {result.token_estimate}")
        print_info(f"Format: {result.metadata.get('format', 'unknown')}")
        
        if isinstance(result.prompt, dict):
            print_info("Prompt structure:")
            for key in result.prompt.keys():
                click.echo(f"  • {key}")
        
    except Exception as e:
        print_error(f"Test compilation failed: {e}")
        sys.exit(1)


@cli.command()
def version():
    """Show version information."""
    click.echo(f"LuminoraCore CLI version {__version__}")
    click.echo("Universal AI Personality Management Standard")


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()
