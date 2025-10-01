"""File utilities for LuminoraCore CLI."""

from __future__ import annotations

import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from .errors import FileError


def find_personality_files(directory: Path) -> List[Path]:
    """
    Find all personality files in a directory.
    
    Args:
        directory: Directory to search
        
    Returns:
        List of personality file paths
    """
    if not directory.exists() or not directory.is_dir():
        raise FileError(f"Directory does not exist: {directory}")
    
    personality_files = []
    
    # Search for JSON files
    for json_file in directory.rglob("*.json"):
        try:
            # Quick check if it looks like a personality file
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'persona' in data:
                    personality_files.append(json_file)
        except Exception:
            continue  # Skip invalid JSON files
    
    # Search for YAML files
    for yaml_file in directory.rglob("*.yaml"):
        try:
            # Quick check if it looks like a personality file
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if isinstance(data, dict) and 'persona' in data:
                    personality_files.append(yaml_file)
        except Exception:
            continue  # Skip invalid YAML files
    
    # Also check .yml files
    for yml_file in directory.rglob("*.yml"):
        try:
            # Quick check if it looks like a personality file
            with open(yml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if isinstance(data, dict) and 'persona' in data:
                    personality_files.append(yml_file)
        except Exception:
            continue  # Skip invalid YAML files
    
    return sorted(personality_files)


def read_json_file(file_path: Path) -> Dict[str, Any]:
    """
    Read JSON file with error handling.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON data
        
    Raises:
        FileError: If file cannot be read or parsed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileError(f"File not found: {file_path}", file_path=str(file_path))
    except json.JSONDecodeError as e:
        raise FileError(f"Invalid JSON in {file_path}: {e}", file_path=str(file_path))
    except Exception as e:
        raise FileError(f"Failed to read file {file_path}: {e}", file_path=str(file_path))


def read_yaml_file(file_path: Path) -> Dict[str, Any]:
    """
    Read YAML file with error handling.
    
    Args:
        file_path: Path to YAML file
        
    Returns:
        Parsed YAML data
        
    Raises:
        FileError: If file cannot be read or parsed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        raise FileError(f"File not found: {file_path}", file_path=str(file_path))
    except yaml.YAMLError as e:
        raise FileError(f"Invalid YAML in {file_path}: {e}", file_path=str(file_path))
    except Exception as e:
        raise FileError(f"Failed to read file {file_path}: {e}", file_path=str(file_path))


def write_json_file(file_path: Path, data: Dict[str, Any], indent: int = 2) -> None:
    """
    Write JSON file with error handling.
    
    Args:
        file_path: Path to write JSON file
        data: Data to write
        indent: JSON indentation
        
    Raises:
        FileError: If file cannot be written
    """
    try:
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
    except Exception as e:
        raise FileError(f"Failed to write file {file_path}: {e}", file_path=str(file_path))


def write_yaml_file(file_path: Path, data: Dict[str, Any], indent: int = 2) -> None:
    """
    Write YAML file with error handling.
    
    Args:
        file_path: Path to write YAML file
        data: Data to write
        indent: YAML indentation
        
    Raises:
        FileError: If file cannot be written
    """
    try:
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, indent=indent, allow_unicode=True)
    except Exception as e:
        raise FileError(f"Failed to write file {file_path}: {e}", file_path=str(file_path))


def read_file(file_path: Path) -> Dict[str, Any]:
    """
    Read file (JSON or YAML) with automatic format detection.
    
    Args:
        file_path: Path to file
        
    Returns:
        Parsed file data
        
    Raises:
        FileError: If file cannot be read or parsed
    """
    suffix = file_path.suffix.lower()
    
    if suffix == '.json':
        return read_json_file(file_path)
    elif suffix in ['.yaml', '.yml']:
        return read_yaml_file(file_path)
    else:
        # Try to detect format by content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if content.startswith('{') or content.startswith('['):
                return read_json_file(file_path)
            else:
                return read_yaml_file(file_path)
        except Exception:
            raise FileError(f"Unsupported file format: {file_path}", file_path=str(file_path))


def write_file(file_path: Path, data: Dict[str, Any], format: str = "json") -> None:
    """
    Write file (JSON or YAML) with specified format.
    
    Args:
        file_path: Path to write file
        data: Data to write
        format: File format ("json" or "yaml")
        
    Raises:
        FileError: If file cannot be written
    """
    if format.lower() == "json":
        write_json_file(file_path, data)
    elif format.lower() in ["yaml", "yml"]:
        write_yaml_file(file_path, data)
    else:
        raise FileError(f"Unsupported format: {format}")


def backup_file(file_path: Path, backup_suffix: str = ".backup") -> Path:
    """
    Create a backup of a file.
    
    Args:
        file_path: Path to file to backup
        backup_suffix: Suffix for backup file
        
    Returns:
        Path to backup file
        
    Raises:
        FileError: If backup cannot be created
    """
    if not file_path.exists():
        raise FileError(f"File does not exist: {file_path}", file_path=str(file_path))
    
    backup_path = file_path.with_suffix(file_path.suffix + backup_suffix)
    
    try:
        import shutil
        shutil.copy2(file_path, backup_path)
        return backup_path
    except Exception as e:
        raise FileError(f"Failed to create backup: {e}", file_path=str(file_path))


def ensure_directory(directory: Path) -> None:
    """
    Ensure directory exists.
    
    Args:
        directory: Directory path
        
    Raises:
        FileError: If directory cannot be created
    """
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise FileError(f"Failed to create directory {directory}: {e}", file_path=str(directory))


def get_file_size(file_path: Path) -> int:
    """
    Get file size in bytes.
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in bytes
        
    Raises:
        FileError: If file does not exist
    """
    if not file_path.exists():
        raise FileError(f"File does not exist: {file_path}", file_path=str(file_path))
    
    return file_path.stat().st_size


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    
    return f"{size:.1f} {units[unit_index]}"
