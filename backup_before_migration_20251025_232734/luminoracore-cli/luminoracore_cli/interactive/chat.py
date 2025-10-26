"""
Interactive chat module for LuminoraCore CLI.

This module provides an interactive chat interface for testing personalities
with real LLM providers.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from datetime import datetime

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown

from ..core import PersonalityTester, PersonalityCompiler
from ..utils.errors import CLIError
from ..utils.files import read_json_file


@dataclass
class ChatMessage:
    """Represents a chat message."""
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime
    provider: Optional[str] = None


class InteractiveChat:
    """Interactive chat interface for testing personalities."""
    
    def __init__(
        self,
        personality_path: Union[str, Path],
        console: Optional[Console] = None,
        provider: str = "openai"
    ):
        """Initialize the interactive chat.
        
        Args:
            personality_path: Path to personality file
            console: Optional Rich console for output
            provider: LLM provider to use
        """
        self.personality_path = Path(personality_path)
        self.console = console or Console()
        self.provider = provider
        
        # Load personality
        self.personality = self._load_personality()
        
        # Initialize components
        self.compiler = PersonalityCompiler()
        self.tester = PersonalityTester()
        
        # Chat history
        self.messages: List[ChatMessage] = []
        
        # Chat settings
        self.max_history = 50
        self.show_timestamps = False
        self.show_provider = False
    
    def _load_personality(self) -> Dict[str, Any]:
        """Load personality from file.
        
        Returns:
            Personality data
        """
        if not self.personality_path.exists():
            raise CLIError(f"Personality file not found: {self.personality_path}")
        
        try:
            return read_json_file(self.personality_path)
        except Exception as e:
            raise CLIError(f"Failed to load personality: {e}")
    
    def start_chat(self) -> None:
        """Start the interactive chat session."""
        self.console.print(Panel(
            f"[bold blue]Interactive Chat with {self.personality.get('name', 'Unknown Personality')}[/bold blue]\n"
            f"Provider: {self.provider}\n"
            f"Type 'exit', 'quit', or 'bye' to end the chat\n"
            f"Type 'help' for commands",
            title="🤖 LuminoraCore Chat",
            border_style="blue"
        ))
        
        # Add system message
        system_message = self._get_system_message()
        if system_message:
            self.messages.append(ChatMessage(
                role="system",
                content=system_message,
                timestamp=datetime.now()
            ))
        
        while True:
            try:
                # Get user input
                user_input = questionary.text(
                    "You:",
                    style=questionary.Style([
                        ('question', 'fg:#673ab7 bold'),
                        ('answer', 'fg:#f44336 bold'),
                        ('pointer', 'fg:#673ab7 bold'),
                        ('highlighted', 'fg:#f44336 bold'),
                        ('selected', 'fg:#cc5454'),
                        ('separator', 'fg:#cc5454'),
                        ('instruction', ''),
                        ('text', ''),
                        ('disabled', 'fg:#858585 italic')
                    ])
                ).ask()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    self.console.print("[yellow]Goodbye! 👋[/yellow]")
                    break
                elif user_input.lower() == 'help':
                    self._show_help()
                    continue
                elif user_input.lower() == 'clear':
                    self._clear_history()
                    continue
                elif user_input.lower() == 'history':
                    self._show_history()
                    continue
                elif user_input.lower() == 'personality':
                    self._show_personality_info()
                    continue
                elif user_input.lower() == 'settings':
                    self._show_settings()
                    continue
                elif user_input.lower().startswith('provider'):
                    self._change_provider(user_input)
                    continue
                
                # Add user message
                user_message = ChatMessage(
                    role="user",
                    content=user_input,
                    timestamp=datetime.now()
                )
                self.messages.append(user_message)
                
                # Get assistant response
                assistant_response = self._get_assistant_response()
                
                # Add assistant message
                assistant_message = ChatMessage(
                    role="assistant",
                    content=assistant_response,
                    timestamp=datetime.now(),
                    provider=self.provider
                )
                self.messages.append(assistant_message)
                
                # Display response
                self._display_message(assistant_message)
                
                # Trim history if needed
                self._trim_history()
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Chat interrupted. Goodbye! 👋[/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
    
    def _get_system_message(self) -> str:
        """Get the system message for the personality.
        
        Returns:
            System message
        """
        try:
            # Compile personality to system message
            compiled = self.compiler.compile_to_openai(self.personality)
            return compiled.get('system_message', '')
        except Exception:
            # Fallback to basic personality info
            name = self.personality.get('name', 'Assistant')
            description = self.personality.get('description', '')
            return f"You are {name}. {description}"
    
    def _get_assistant_response(self) -> str:
        """Get assistant response from the LLM provider.
        
        Returns:
            Assistant response
        """
        try:
            # Prepare messages for the API
            api_messages = []
            
            # Add recent conversation history
            recent_messages = self.messages[-10:]  # Last 10 messages
            
            for msg in recent_messages:
                if msg.role != "system":
                    api_messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })
            
            # Get response from tester
            response = self.tester.test_openai(
                messages=api_messages,
                personality=self.personality
            )
            
            return response.get('content', 'I apologize, but I cannot generate a response at this time.')
            
        except Exception as e:
            return f"I apologize, but I encountered an error: {e}"
    
    def _display_message(self, message: ChatMessage) -> None:
        """Display a chat message.
        
        Args:
            message: Message to display
        """
        # Create header
        header_parts = [f"[bold green]{self.personality.get('name', 'Assistant')}[/bold green]"]
        
        if self.show_timestamps:
            header_parts.append(f"[dim]{message.timestamp.strftime('%H:%M:%S')}[/dim]")
        
        if self.show_provider and message.provider:
            header_parts.append(f"[dim]{message.provider}[/dim]")
        
        header = " | ".join(header_parts)
        
        # Display message
        self.console.print(f"\n{header}")
        
        # Try to render as markdown, fallback to plain text
        try:
            # Check if content looks like markdown
            if any(marker in message.content for marker in ['**', '*', '#', '`', '[', ']']):
                markdown = Markdown(message.content)
                self.console.print(markdown)
            else:
                self.console.print(message.content)
        except Exception:
            self.console.print(message.content)
    
    def _show_help(self) -> None:
        """Show help information."""
        help_text = """
[bold]Available Commands:[/bold]

• [cyan]help[/cyan] - Show this help message
• [cyan]clear[/cyan] - Clear chat history
• [cyan]history[/cyan] - Show recent chat history
• [cyan]personality[/cyan] - Show personality information
• [cyan]settings[/cyan] - Show current settings
• [cyan]provider <name>[/cyan] - Change LLM provider
• [cyan]exit/quit/bye[/cyan] - End the chat session

[bold]Tips:[/bold]
• Use [cyan]Ctrl+C[/cyan] to interrupt the current response
• Type [cyan]clear[/cyan] if the conversation gets too long
• Use [cyan]history[/cyan] to review recent messages
        """
        
        self.console.print(Panel(help_text, title="Help", border_style="green"))
    
    def _clear_history(self) -> None:
        """Clear chat history."""
        # Keep only the system message
        system_messages = [msg for msg in self.messages if msg.role == "system"]
        self.messages = system_messages
        
        self.console.print("[green]Chat history cleared![/green]")
    
    def _show_history(self) -> None:
        """Show recent chat history."""
        if len(self.messages) <= 1:  # Only system message
            self.console.print("[yellow]No chat history yet.[/yellow]")
            return
        
        history_text = ""
        for msg in self.messages[-10:]:  # Last 10 messages
            if msg.role == "system":
                continue
            
            timestamp = msg.timestamp.strftime('%H:%M:%S')
            role = "You" if msg.role == "user" else self.personality.get('name', 'Assistant')
            
            history_text += f"[dim]{timestamp}[/dim] [bold]{role}:[/bold] {msg.content}\n\n"
        
        self.console.print(Panel(history_text, title="Recent History", border_style="yellow"))
    
    def _show_personality_info(self) -> None:
        """Show personality information."""
        name = self.personality.get('name', 'Unknown')
        version = self.personality.get('version', 'Unknown')
        description = self.personality.get('description', 'No description')
        author = self.personality.get('author', 'Unknown')
        tags = self.personality.get('tags', [])
        
        info_text = f"""
[bold]Name:[/bold] {name}
[bold]Version:[/bold] {version}
[bold]Author:[/bold] {author}
[bold]Description:[/bold] {description}
[bold]Tags:[/bold] {', '.join(tags) if tags else 'None'}
        """
        
        self.console.print(Panel(info_text, title="Personality Info", border_style="blue"))
    
    def _show_settings(self) -> None:
        """Show current settings."""
        settings_text = f"""
[bold]Provider:[/bold] {self.provider}
[bold]Max History:[/bold] {self.max_history}
[bold]Show Timestamps:[/bold] {'Yes' if self.show_timestamps else 'No'}
[bold]Show Provider:[/bold] {'Yes' if self.show_provider else 'No'}
        """
        
        self.console.print(Panel(settings_text, title="Settings", border_style="cyan"))
    
    def _change_provider(self, command: str) -> None:
        """Change the LLM provider.
        
        Args:
            command: Command string (e.g., "provider openai")
        """
        parts = command.split()
        if len(parts) < 2:
            self.console.print("[red]Usage: provider <name>[/red]")
            return
        
        new_provider = parts[1].lower()
        valid_providers = ['openai', 'anthropic', 'google', 'cohere', 'huggingface']
        
        if new_provider not in valid_providers:
            self.console.print(f"[red]Invalid provider. Valid options: {', '.join(valid_providers)}[/red]")
            return
        
        self.provider = new_provider
        self.console.print(f"[green]Provider changed to: {new_provider}[/green]")
    
    def _trim_history(self) -> None:
        """Trim chat history to maximum length."""
        if len(self.messages) > self.max_history:
            # Keep system message and recent messages
            system_messages = [msg for msg in self.messages if msg.role == "system"]
            other_messages = [msg for msg in self.messages if msg.role != "system"]
            
            # Keep the most recent messages
            recent_messages = other_messages[-(self.max_history - len(system_messages)):]
            
            self.messages = system_messages + recent_messages


def start_interactive_chat(
    personality_path: Union[str, Path],
    provider: str = "openai",
    console: Optional[Console] = None
) -> None:
    """Start an interactive chat session.
    
    Args:
        personality_path: Path to personality file
        provider: LLM provider to use
        console: Optional Rich console for output
    """
    chat = InteractiveChat(personality_path, console, provider)
    chat.start_chat()
