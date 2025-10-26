"""Caching utilities for LuminoraCore CLI."""

import json
import hashlib
import time
from pathlib import Path
from typing import Dict, Any, Optional, Union
from datetime import datetime, timedelta

from luminoracore_cli.utils.errors import CLIError
from luminoracore_cli.utils.console import console


class CacheManager:
    """Manages local caching for LuminoraCore CLI."""
    
    def __init__(self, cache_dir: Path, max_size: int = 1073741824, ttl: int = 86400):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Directory to store cache files
            max_size: Maximum cache size in bytes (default: 1GB)
            ttl: Time-to-live for cache entries in seconds (default: 24 hours)
        """
        self.cache_dir = Path(cache_dir)
        self.max_size = max_size
        self.ttl = ttl
        
        # Create cache directory
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache metadata file
        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load cache metadata."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        return {
            "entries": {},
            "total_size": 0,
            "created_at": datetime.now().isoformat()
        }
    
    def _save_metadata(self) -> None:
        """Save cache metadata."""
        try:
            with open(self.metadata_file, "w") as f:
                json.dump(self.metadata, f, indent=2)
        except IOError as e:
            console.print(f"[red]Warning: Failed to save cache metadata: {e}[/red]")
    
    def _get_cache_key(self, key: str) -> str:
        """Generate cache key from string."""
        return hashlib.md5(key.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get cache file path for key."""
        return self.cache_dir / f"{cache_key}.json"
    
    def _is_expired(self, entry: Dict[str, Any]) -> bool:
        """Check if cache entry is expired."""
        created_at = datetime.fromisoformat(entry["created_at"])
        return datetime.now() - created_at > timedelta(seconds=self.ttl)
    
    def _cleanup_expired(self) -> None:
        """Remove expired cache entries."""
        expired_keys = []
        
        for key, entry in self.metadata["entries"].items():
            if self._is_expired(entry):
                expired_keys.append(key)
        
        for key in expired_keys:
            self._remove_entry(key)
    
    def _cleanup_size(self) -> None:
        """Remove oldest entries if cache size exceeds limit."""
        while self.metadata["total_size"] > self.max_size:
            if not self.metadata["entries"]:
                break
            
            # Find oldest entry
            oldest_key = min(
                self.metadata["entries"].keys(),
                key=lambda k: self.metadata["entries"][k]["created_at"]
            )
            
            self._remove_entry(oldest_key)
    
    def _remove_entry(self, key: str) -> None:
        """Remove cache entry."""
        if key in self.metadata["entries"]:
            entry = self.metadata["entries"][key]
            cache_path = self._get_cache_path(key)
            
            # Remove file if it exists
            if cache_path.exists():
                try:
                    cache_path.unlink()
                except IOError:
                    pass
            
            # Update metadata
            self.metadata["total_size"] -= entry["size"]
            del self.metadata["entries"][key]
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        cache_key = self._get_cache_key(key)
        
        # Check if entry exists in metadata
        if cache_key not in self.metadata["entries"]:
            return None
        
        entry = self.metadata["entries"][cache_key]
        
        # Check if expired
        if self._is_expired(entry):
            self._remove_entry(cache_key)
            self._save_metadata()
            return None
        
        # Load from file
        cache_path = self._get_cache_path(cache_key)
        if not cache_path.exists():
            self._remove_entry(cache_key)
            self._save_metadata()
            return None
        
        try:
            with open(cache_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            self._remove_entry(cache_key)
            self._save_metadata()
            return None
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        cache_key = self._get_cache_key(key)
        cache_path = self._get_cache_path(cache_key)
        
        # Serialize value
        try:
            json_data = json.dumps(value, indent=2)
            json_bytes = json_data.encode()
            size = len(json_bytes)
        except (TypeError, ValueError) as e:
            raise CLIError(f"Failed to serialize cache value: {e}")
        
        # Write to file
        try:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(cache_path, "w") as f:
                f.write(json_data)
        except IOError as e:
            raise CLIError(f"Failed to write cache file: {e}")
        
        # Remove existing entry if it exists
        if cache_key in self.metadata["entries"]:
            self._remove_entry(cache_key)
        
        # Add to metadata
        self.metadata["entries"][cache_key] = {
            "key": key,
            "size": size,
            "created_at": datetime.now().isoformat()
        }
        self.metadata["total_size"] += size
        
        # Cleanup
        self._cleanup_expired()
        self._cleanup_size()
        
        # Save metadata
        self._save_metadata()
    
    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        cache_key = self._get_cache_key(key)
        
        if cache_key in self.metadata["entries"]:
            self._remove_entry(cache_key)
            self._save_metadata()
            return True
        
        return False
    
    def clear(self) -> None:
        """Clear all cache entries."""
        # Remove all cache files
        for cache_file in self.cache_dir.glob("*.json"):
            if cache_file.name != "metadata.json":
                try:
                    cache_file.unlink()
                except IOError:
                    pass
        
        # Reset metadata
        self.metadata = {
            "entries": {},
            "total_size": 0,
            "created_at": datetime.now().isoformat()
        }
        self._save_metadata()
    
    def info(self) -> Dict[str, Any]:
        """Get cache information."""
        self._cleanup_expired()
        
        return {
            "cache_dir": str(self.cache_dir),
            "total_entries": len(self.metadata["entries"]),
            "total_size": self.metadata["total_size"],
            "max_size": self.max_size,
            "ttl": self.ttl,
            "usage_percent": (self.metadata["total_size"] / self.max_size) * 100
        }


def get_cache_manager(cache_dir: Optional[Path] = None) -> CacheManager:
    """Get cache manager instance."""
    if cache_dir is None:
        cache_dir = Path.home() / ".luminoracore" / "cache"
    
    return CacheManager(cache_dir)
