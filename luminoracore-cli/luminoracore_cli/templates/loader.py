"""
Template loader module for LuminoraCore CLI.

This module handles loading and managing templates for personalities,
projects, and integrations.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Type
from dataclasses import dataclass
from enum import Enum

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from rich.console import Console

from ..utils.errors import FileError, ValidationError


class TemplateType(Enum):
    """Types of templates available."""
    PERSONALITY = "personality"
    PROJECT = "project"
    INTEGRATION = "integration"


@dataclass
class TemplateInfo:
    """Information about a template."""
    name: str
    template_type: TemplateType
    description: str
    file_path: Path
    variables: List[str]
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class TemplateLoader:
    """Main template loader class."""
    
    def __init__(self, templates_dir: Optional[Path] = None, console: Optional[Console] = None):
        """Initialize the template loader.
        
        Args:
            templates_dir: Directory containing templates
            console: Optional Rich console for output
        """
        self.console = console or Console()
        
        # Set up templates directory
        if templates_dir is None:
            templates_dir = Path(__file__).parent
        
        self.templates_dir = Path(templates_dir)
        
        # Set up Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        # Cache for loaded templates
        self._template_cache: Dict[str, Any] = {}
    
    def list_templates(self, template_type: Optional[TemplateType] = None) -> List[TemplateInfo]:
        """List available templates.
        
        Args:
            template_type: Filter by template type
            
        Returns:
            List of template information
        """
        templates = []
        
        for template_path in self._scan_template_directory():
            try:
                template_info = self._load_template_info(template_path)
                if template_type is None or template_info.template_type == template_type:
                    templates.append(template_info)
            except Exception as e:
                self.console.print(f"[yellow]Failed to load template info for {template_path}: {e}[/yellow]")
        
        return sorted(templates, key=lambda t: t.name)
    
    def get_template(self, name: str, template_type: TemplateType) -> Optional[Dict[str, Any]]:
        """Get a specific template.
        
        Args:
            name: Template name
            template_type: Type of template
            
        Returns:
            Template data or None if not found
        """
        cache_key = f"{template_type.value}_{name}"
        
        if cache_key in self._template_cache:
            return self._template_cache[cache_key]
        
        template_path = self.templates_dir / template_type.value / f"{name}.json"
        
        if not template_path.exists():
            return None
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            
            self._template_cache[cache_key] = template_data
            return template_data
            
        except Exception as e:
            self.console.print(f"[red]Failed to load template {name}: {e}[/red]")
            return None
    
    def get_template_info(self, name: str, template_type: TemplateType) -> Optional[TemplateInfo]:
        """Get template information.
        
        Args:
            name: Template name
            template_type: Type of template
            
        Returns:
            Template info or None if not found
        """
        template_path = self.templates_dir / template_type.value / f"{name}.json"
        
        if not template_path.exists():
            return None
        
        try:
            return self._load_template_info(template_path)
        except Exception as e:
            self.console.print(f"[red]Failed to load template info for {name}: {e}[/red]")
            return None
    
    def render_template(
        self,
        name: str,
        template_type: TemplateType,
        variables: Dict[str, Any],
        output_path: Optional[Path] = None
    ) -> str:
        """Render a template with variables.
        
        Args:
            name: Template name
            template_type: Type of template
            variables: Variables to substitute
            output_path: Optional output path for file-based templates
            
        Returns:
            Rendered template content
        """
        template_data = self.get_template(name, template_type)
        if not template_data:
            raise FileError(f"Template '{name}' not found")
        
        # Create Jinja2 template from the data
        template_str = json.dumps(template_data, indent=2)
        template = self.jinja_env.from_string(template_str)
        
        # Render with variables
        rendered_content = template.render(**variables)
        
        # Parse back to JSON and format
        try:
            rendered_data = json.loads(rendered_content)
            formatted_content = json.dumps(rendered_data, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            # If not valid JSON, return as-is
            formatted_content = rendered_content
        
        # Write to file if output path specified
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(formatted_content)
        
        return formatted_content
    
    def render_directory_template(
        self,
        name: str,
        template_type: TemplateType,
        variables: Dict[str, Any],
        output_dir: Path
    ) -> List[Path]:
        """Render a directory-based template.
        
        Args:
            name: Template name
            template_type: Type of template
            variables: Variables to substitute
            output_dir: Output directory
            
        Returns:
            List of created files
        """
        template_data = self.get_template(name, template_type)
        if not template_data:
            raise FileError(f"Template '{name}' not found")
        
        created_files = []
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Process each file in the template
        for file_path, file_content in template_data.items():
            if file_path.startswith('_meta'):
                continue  # Skip metadata
            
            # Resolve file path
            if isinstance(file_content, str):
                # Simple file content
                resolved_path = output_dir / file_path
                resolved_content = self._substitute_variables(file_content, variables)
            elif isinstance(file_content, dict):
                # File with metadata
                resolved_path = output_dir / file_path
                resolved_content = self._substitute_variables(
                    file_content.get('content', ''),
                    variables
                )
            else:
                continue
            
            # Create directory structure
            resolved_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(resolved_path, 'w', encoding='utf-8') as f:
                f.write(resolved_content)
            
            created_files.append(resolved_path)
        
        return created_files
    
    def get_template_variables(self, name: str, template_type: TemplateType) -> List[str]:
        """Get variables used in a template.
        
        Args:
            name: Template name
            template_type: Type of template
            
        Returns:
            List of variable names
        """
        template_info = self.get_template_info(name, template_type)
        if template_info:
            return template_info.variables
        
        return []
    
    def validate_template(self, name: str, template_type: TemplateType) -> bool:
        """Validate a template.
        
        Args:
            name: Template name
            template_type: Type of template
            
        Returns:
            True if template is valid
        """
        try:
            template_data = self.get_template(name, template_type)
            if not template_data:
                return False
            
            # Basic validation based on template type
            if template_type == TemplateType.PERSONALITY:
                required_fields = ['name', 'version', 'description', 'persona', 'core_traits', 'linguistic_profile', 'behavioral_rules']
                for field in required_fields:
                    if field not in template_data:
                        self.console.print(f"[red]Missing required field: {field}[/red]")
                        return False
            
            elif template_type == TemplateType.PROJECT:
                if not isinstance(template_data, dict):
                    self.console.print(f"[red]Project template must be a dictionary[/red]")
                    return False
            
            elif template_type == TemplateType.INTEGRATION:
                if not isinstance(template_data, dict):
                    self.console.print(f"[red]Integration template must be a dictionary[/red]")
                    return False
            
            return True
            
        except Exception as e:
            self.console.print(f"[red]Template validation failed: {e}[/red]")
            return False
    
    def _scan_template_directory(self) -> List[Path]:
        """Scan the template directory for template files.
        
        Returns:
            List of template file paths
        """
        template_files = []
        
        for template_type in TemplateType:
            template_dir = self.templates_dir / template_type.value
            
            if template_dir.exists():
                for template_file in template_dir.glob("*.json"):
                    template_files.append(template_file)
        
        return template_files
    
    def _load_template_info(self, template_path: Path) -> TemplateInfo:
        """Load template information from a file.
        
        Args:
            template_path: Path to template file
            
        Returns:
            Template information
        """
        with open(template_path, 'r', encoding='utf-8') as f:
            template_data = json.load(f)
        
        # Determine template type from path
        template_type_name = template_path.parent.name
        template_type = TemplateType(template_type_name)
        
        # Extract template name
        name = template_path.stem
        
        # Extract description
        description = template_data.get('description', f"{name} template")
        
        # Extract variables (look for Jinja2-style variables)
        variables = self._extract_variables(template_data)
        
        # Extract tags
        tags = template_data.get('tags', [])
        if not isinstance(tags, list):
            tags = []
        
        return TemplateInfo(
            name=name,
            template_type=template_type,
            description=description,
            file_path=template_path,
            variables=variables,
            tags=tags
        )
    
    def _extract_variables(self, data: Any, variables: Optional[set] = None) -> List[str]:
        """Recursively extract Jinja2 variables from template data.
        
        Args:
            data: Template data
            variables: Set to store found variables
            
        Returns:
            List of variable names
        """
        if variables is None:
            variables = set()
        
        if isinstance(data, dict):
            for value in data.values():
                self._extract_variables(value, variables)
        elif isinstance(data, list):
            for item in data:
                self._extract_variables(item, variables)
        elif isinstance(data, str):
            # Look for Jinja2 variable patterns
            import re
            pattern = r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}'
            matches = re.findall(pattern, data)
            variables.update(matches)
        
        return sorted(list(variables))
    
    def _substitute_variables(self, content: str, variables: Dict[str, Any]) -> str:
        """Substitute variables in content.
        
        Args:
            content: Content with variables
            variables: Variable substitutions
            
        Returns:
            Content with variables substituted
        """
        template = self.jinja_env.from_string(content)
        return template.render(**variables)


# Global template loader instance
_template_loader: Optional[TemplateLoader] = None


def get_template_loader() -> TemplateLoader:
    """Get the global template loader instance.
    
    Returns:
        Template loader instance
    """
    global _template_loader
    if _template_loader is None:
        _template_loader = TemplateLoader()
    return _template_loader


def get_template(name: str, template_type: TemplateType) -> Optional[Dict[str, Any]]:
    """Get a template using the global loader.
    
    Args:
        name: Template name
        template_type: Type of template
        
    Returns:
        Template data or None
    """
    return get_template_loader().get_template(name, template_type)


def list_templates(template_type: Optional[TemplateType] = None) -> List[TemplateInfo]:
    """List templates using the global loader.
    
    Args:
        template_type: Filter by template type
        
    Returns:
        List of template information
    """
    return get_template_loader().list_templates(template_type)


def get_all_templates() -> Dict[str, List[TemplateInfo]]:
    """Get all templates organized by type.
    
    Returns:
        Dictionary mapping template types to lists of templates
    """
    templates = {}
    
    for template_type in TemplateType:
        templates[template_type.value] = list_templates(template_type)
    
    return templates


def validate_template(name: str, template_type: TemplateType) -> bool:
    """Validate a template using the global loader.
    
    Args:
        name: Template name
        template_type: Type of template
        
    Returns:
        True if template is valid
    """
    return get_template_loader().validate_template(name, template_type)
