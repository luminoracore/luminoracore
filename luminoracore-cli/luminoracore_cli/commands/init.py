"""Init command for LuminoraCore CLI."""

import json
from pathlib import Path
from typing import Optional, Dict, Any
import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

from luminoracore_cli.utils.errors import CLIError
from luminoracore_cli.utils.console import console, error_console
from luminoracore_cli.utils.files import read_json_file, write_json_file
from luminoracore_cli.templates import get_template, list_templates


def init_command(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Project name"),
    template: Optional[str] = typer.Option("basic", "--template", "-t", help="Project template to use"),
    path: Optional[str] = typer.Option(".", "--path", "--directory", "-d", help="Directory to initialize in"),
    force: bool = typer.Option(False, "--force", "-f", help="Force initialization in non-empty directory"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive mode"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
) -> int:
    """
    Initialize a new LuminoraCore project.
    
    This command creates a new project structure with the specified template,
    including personality files, configuration, and documentation.
    """
    try:
        # Get target directory
        target_dir = Path(path).resolve()
        
        if verbose:
            console.print(f"[blue]Initializing project in: {target_dir}[/blue]")
        
        # Check if directory is empty (unless force is specified)
        if not force and target_dir.exists() and any(target_dir.iterdir()):
            error_console.print(f"[red]Directory {target_dir} is not empty. Use --force to override.[/red]")
            return 1
        
        # Create directory if it doesn't exist
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Get project name
        if not name:
            if interactive:
                name = Prompt.ask("Project name", default=target_dir.name)
            else:
                name = target_dir.name
        
        if verbose:
            console.print(f"[blue]Project name: {name}[/blue]")
        
        # Get template
        if interactive:
            available_templates = list_templates("project")
            if available_templates:
                console.print("\n[bold blue]Available project templates:[/bold blue]")
                for i, tmpl in enumerate(available_templates, 1):
                    console.print(f"  {i}. {tmpl['name']} - {tmpl.get('description', 'No description')}")
                
                while True:
                    try:
                        choice = Prompt.ask("Select template", default="1")
                        template_index = int(choice) - 1
                        if 0 <= template_index < len(available_templates):
                            template = available_templates[template_index]["id"]
                            break
                        else:
                            error_console.print("[red]Invalid template selection[/red]")
                    except ValueError:
                        error_console.print("[red]Please enter a valid number[/red]")
            else:
                template = "basic"
        
        if verbose:
            console.print(f"[blue]Using template: {template}[/blue]")
        
        # Load template
        try:
            template_data = get_template("project", template)
        except Exception as e:
            error_console.print(f"[red]Error loading template '{template}': {e}[/red]")
            return 1
        
        # Get template variables
        template_vars = template_data.get("template_vars", {})
        
        # Collect template variable values
        if interactive:
            collected_vars = {}
            for var_name, var_config in template_vars.items():
                var_type = var_config.get("type", "string")
                var_description = var_config.get("description", "")
                var_default = var_config.get("default", "")
                
                prompt_text = f"{var_description or var_name}"
                if var_default:
                    prompt_text += f" (default: {var_default})"
                
                if var_type == "string":
                    collected_vars[var_name] = Prompt.ask(prompt_text, default=var_default)
                elif var_type == "boolean":
                    collected_vars[var_name] = Confirm.ask(prompt_text, default=bool(var_default))
                else:
                    collected_vars[var_name] = var_default
        else:
            # Use defaults for non-interactive mode
            collected_vars = {}
            for var_name, var_config in template_vars.items():
                collected_vars[var_name] = var_config.get("default", "")
        
        # Add project-specific variables
        collected_vars["project_name"] = name
        collected_vars["description"] = template_data.get("description", f"A LuminoraCore project: {name}")
        
        if verbose:
            console.print(f"[blue]Template variables: {collected_vars}[/blue]")
        
        # Create project files
        files_created = []
        
        for file_config in template_data.get("files", []):
            file_path = target_dir / file_config["path"]
            file_content = file_config["content"]
            
            # Replace template variables
            for var_name, var_value in collected_vars.items():
                placeholder = f"{{{{{var_name}}}}}"
                file_content = file_content.replace(placeholder, str(var_value))
            
            # Create file
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(file_content)
            
            files_created.append(file_path)
            
            if verbose:
                console.print(f"[green]Created: {file_path}[/green]")
        
        # Create additional project files
        create_additional_files(target_dir, name, collected_vars, verbose=verbose)
        
        # Show success message
        console.print("")
        console.print(Panel(
            f"[bold green]Project '{name}' initialized successfully![/bold green]\n\n"
            f"Created {len(files_created)} files in {target_dir}\n\n"
            f"Next steps:\n"
            f"1. Configure your API keys in config/luminoracore.yaml\n"
            f"2. Test your personality: luminoracore test personalities/\n"
            f"3. Start developing with your new LuminoraCore project!",
            title="Project Initialized",
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


def create_additional_files(target_dir: Path, project_name: str, template_vars: Dict[str, Any], verbose: bool = False) -> None:
    """Create additional project files."""
    
    # Create .gitignore
    gitignore_path = target_dir / ".gitignore"
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# LuminoraCore
cache/
*.log
.env

# API keys
api_keys.yaml
secrets.yaml
"""
    
    with open(gitignore_path, "w") as f:
        f.write(gitignore_content)
    
    if verbose:
        console.print(f"[green]Created: {gitignore_path}[/green]")
    
    # Create requirements.txt if not exists
    requirements_path = target_dir / "requirements.txt"
    if not requirements_path.exists():
        requirements_content = """luminoracore>=1.0.0
"""
        
        with open(requirements_path, "w") as f:
            f.write(requirements_content)
        
        if verbose:
            console.print(f"[green]Created: {requirements_path}[/green]")
    
    # Create .env.example
    env_example_path = target_dir / ".env.example"
    env_example_content = """# LuminoraCore Configuration
LUMINORACORE_API_KEY=your-api-key-here
LUMINORACORE_DEFAULT_PROVIDER=openai
LUMINORACORE_DEFAULT_MODEL=gpt-3.5-turbo
LUMINORACORE_CACHE_DIR=./cache
LUMINORACORE_STRICT_VALIDATION=false
"""
    
    with open(env_example_path, "w") as f:
        f.write(env_example_content)
    
    if verbose:
        console.print(f"[green]Created: {env_example_path}[/green]")


if __name__ == "__main__":
    typer.run(init_command)
