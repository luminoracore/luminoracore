"""Test command for LuminoraCore CLI."""

import asyncio
from pathlib import Path
from typing import Optional, Dict, Any
import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

from luminoracore_cli.utils.errors import CLIError
from luminoracore_cli.utils.console import console, error_console
from luminoracore_cli.utils.files import find_personality_files, read_json_file
from luminoracore_cli.core.client import get_client


async def test_command(
    personality: str = typer.Argument(..., help="Personality name or file path"),
    provider: str = typer.Option("openai", "--provider", "-p", help="LLM provider to use"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Specific model to use"),
    message: Optional[str] = typer.Option(None, "--message", help="Test message to send"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive testing mode"),
    validate: bool = typer.Option(True, "--validate", help="Validate personality before testing"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
) -> int:
    """
    Test a personality with a real LLM provider.
    
    This command allows you to test how a personality behaves with actual
    LLM providers, including interactive chat sessions.
    """
    try:
        # Find personality file
        personality_path = Path(personality)
        if not personality_path.exists():
            error_console.print(f"[red]Error: Personality file '{personality}' not found[/red]")
            return 1
        
        if verbose:
            console.print(f"[blue]Found personality file: {personality_path}[/blue]")
        
        # Load personality data
        try:
            personality_data = read_json_file(personality_path)
        except Exception as e:
            error_console.print(f"[red]Error loading personality file: {e}[/red]")
            return 1
        
        # Validate personality if requested
        if validate:
            if verbose:
                console.print("[blue]Validating personality...[/blue]")
            
            from luminoracore_cli.core.validator import PersonalityValidator
            
            validator = PersonalityValidator()
            validation_result = validator.validate(personality_data, strict=True)
            
            if not validation_result["valid"]:
                error_console.print("[red]Validation failed:[/red]")
                for error in validation_result["errors"]:
                    error_console.print(f"  [red]• {error}[/red]")
                return 1
            
            if verbose:
                console.print("[green][OK] Personality validation passed[/green]")
        
        # Get client
        client = get_client()
        
        # Interactive mode
        if interactive:
            return await test_interactive(personality_data, provider, model, verbose=verbose)
        
        # Single test
        return await test_single(personality_data, provider, model, message, verbose=verbose)
        
    except CLIError as e:
        error_console.print(f"[red]CLI error: {e}[/red]")
        return 1
    except Exception as e:
        error_console.print(f"[red]Unexpected error: {e}[/red]")
        if verbose:
            import traceback
            error_console.print(traceback.format_exc())
        return 1


async def test_single(personality_data: Dict[str, Any], provider: str, model: Optional[str], message: Optional[str], verbose: bool = False) -> int:
    """Test personality with a single message."""
    try:
        # Use default message if none provided
        if not message:
            message = "Hello, how are you?"
        
        if verbose:
            console.print(f"[blue]Testing with provider: {provider}[/blue]")
            if model:
                console.print(f"[blue]Using model: {model}[/blue]")
            console.print(f"[blue]Test message: {message}[/blue]")
        
        # Test personality
        from luminoracore_cli.core.tester import PersonalityTester
        
        tester = PersonalityTester()
        test_result = await tester.test(
            personality_data=personality_data,
            provider=provider,
            model=model,
            test_message=message
        )
        
        # Display results
        console.print("")
        console.print(Panel(
            f"[bold blue]Test Results[/bold blue]\n\n"
            f"Provider: {test_result.get('provider', 'Unknown')}\n"
            f"Model: {test_result.get('model', 'Unknown')}\n"
            f"Test Message: {test_result.get('test_message', 'Unknown')}\n"
            f"Tested At: {test_result.get('tested_at', 'Unknown')}\n\n"
            f"[bold green]Response:[/bold green]\n"
            f"{test_result.get('test_result', {}).get('response', 'No response')}",
            title="Personality Test",
            border_style="blue"
        ))
        
        # Show usage if available
        if test_result.get("test_result", {}).get("usage"):
            usage = test_result["test_result"]["usage"]
            console.print(f"\n[blue]Usage:[/blue] {usage}")
        
        return 0
        
    except Exception as e:
        error_console.print(f"[red]Test failed: {e}[/red]")
        return 1


async def test_interactive(personality_data: Dict[str, Any], provider: str, model: Optional[str], verbose: bool = False) -> int:
    """Test personality interactively."""
    try:
        console.print("")
        console.print(Panel(
            f"[bold blue]Interactive Testing Mode[/bold blue]\n\n"
            f"Personality: {personality_data.get('persona', {}).get('name', 'Unknown')}\n"
            f"Provider: {provider}\n"
            f"Model: {model if model and not hasattr(model, '__class__') else 'Default'}\n\n"
            f"Type 'quit' or 'exit' to end the session\n"
            f"Type 'clear' to clear the conversation history",
            title="Interactive Testing",
            border_style="blue"
        ))
        
        # Get client
        client = get_client()
        
        # Conversation history
        conversation_history = []
        
        while True:
            try:
                # Get user input
                user_message = Prompt.ask("\n[bold cyan]You[/bold cyan]")
                
                if user_message.lower() in ['quit', 'exit']:
                    console.print("[yellow]Goodbye![/yellow]")
                    break
                
                if user_message.lower() == 'clear':
                    conversation_history.clear()
                    console.print("[blue]Conversation history cleared[/blue]")
                    continue
                
                if not user_message.strip():
                    continue
                
                # Test personality
                if verbose:
                    console.print(f"[blue]Sending message: {user_message}[/blue]")
                
                from luminoracore_cli.core.tester import PersonalityTester
                
                tester = PersonalityTester()
                test_result = await tester.test(
                    personality_data=personality_data,
                    provider=provider,
                    model=model,
                    test_message=user_message
                )
                
                # Get response
                response = test_result.get("response", "No response")
                
                # Display response
                console.print(f"\n[bold green]{personality_data.get('persona', {}).get('name', 'AI')}[/bold green]: {response}")
                
                # Add to history
                conversation_history.append({
                    "user": user_message,
                    "assistant": response,
                    "timestamp": test_result.get("tested_at", "Unknown")
                })
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Goodbye![/yellow]")
                break
            except Exception as e:
                error_console.print(f"[red]Error: {e}[/red]")
                continue
        
        return 0
        
    except Exception as e:
        error_console.print(f"[red]Interactive testing failed: {e}[/red]")
        return 1


if __name__ == "__main__":
    typer.run(test_command)
