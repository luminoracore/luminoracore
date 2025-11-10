"""
Personality downloader module for LuminoraCore CLI.

This module handles downloading personalities from remote repositories,
caching them locally, and managing updates.
"""

import asyncio
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
import aiofiles

from rich.console import Console
from rich.progress import Progress, TaskID

from ..utils.errors import NetworkError, FileError
from ..utils.http import HTTPClient
from ..utils.cache import CacheManager
from ..utils.files import write_json_file, ensure_directory


@dataclass
class PersonalityInfo:
    """Information about a personality from the repository."""
    name: str
    version: str
    description: str
    author: Optional[str] = None
    tags: List[str] = None
    download_url: Optional[str] = None
    last_updated: Optional[datetime] = None
    size: Optional[int] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class DownloadResult:
    """Result of a download operation."""
    success: bool
    personality_name: str
    local_path: Optional[Path] = None
    error_message: Optional[str] = None
    cached: bool = False
    size: Optional[int] = None
    download_time: Optional[float] = None


class PersonalityDownloader:
    """Main downloader class for personalities."""
    
    def __init__(
        self,
        http_client: HTTPClient,
        cache_manager: CacheManager,
        console: Optional[Console] = None,
        cache_dir: Optional[Path] = None
    ):
        """Initialize the downloader.
        
        Args:
            http_client: HTTP client for making requests
            cache_manager: Cache manager for local storage
            console: Optional Rich console for output
            cache_dir: Directory for caching personalities
        """
        self.http_client = http_client
        self.cache_manager = cache_manager
        self.console = console or Console()
        self.cache_dir = cache_dir or Path.home() / '.luminoracore' / 'personalities'
        
        # Ensure cache directory exists
        ensure_directory(self.cache_dir)
        
        # Repository endpoints
        self.base_url = "https://api.luminoracore.com"
        self.personalities_endpoint = f"{self.base_url}/personalities"
        self.download_endpoint = f"{self.base_url}/download"
        
        # Cache settings
        self.cache_duration = timedelta(hours=1)  # Cache personality list for 1 hour
        self.personality_cache_duration = timedelta(days=7)  # Cache personalities for 7 days
    
    async def list_available_personalities(
        self,
        force_refresh: bool = False,
        tags: Optional[List[str]] = None,
        author: Optional[str] = None
    ) -> List[PersonalityInfo]:
        """List available personalities from the repository.
        
        Args:
            force_refresh: Force refresh from remote repository
            tags: Filter by tags
            author: Filter by author
            
        Returns:
            List of available personalities
        """
        cache_key = "personalities_list"
        
        # Check cache first
        if not force_refresh:
            cached_data = await self.cache_manager.get(cache_key)
            if cached_data:
                try:
                    personalities = [
                        PersonalityInfo(**p) for p in json.loads(cached_data)
                    ]
                    self.console.print(f"[green]Using cached personality list ({len(personalities)} personalities)[/green]")
                    return self._filter_personalities(personalities, tags, author)
                except Exception as e:
                    self.console.print(f"[yellow]Failed to load cached data: {e}[/yellow]")
        
        # Fetch from remote repository
        try:
            self.console.print("[blue]Fetching personality list from repository...[/blue]")
            
            response = await self.http_client.get(self.personalities_endpoint)
            response.raise_for_status()
            
            data = response.json()
            personalities = [PersonalityInfo(**p) for p in data.get('personalities', [])]
            
            # Cache the results
            await self.cache_manager.set(
                cache_key,
                json.dumps([p.__dict__ for p in personalities], default=str),
                ttl=self.cache_duration.total_seconds()
            )
            
            self.console.print(f"[green]Found {len(personalities)} personalities[/green]")
            return self._filter_personalities(personalities, tags, author)
            
        except Exception as e:
            self.console.print(f"[red]Failed to fetch personality list: {e}[/red]")
            
            # Try to return cached data even if expired
            cached_data = await self.cache_manager.get(cache_key, ignore_expiry=True)
            if cached_data:
                try:
                    personalities = [
                        PersonalityInfo(**p) for p in json.loads(cached_data)
                    ]
                    self.console.print(f"[yellow]Using expired cached data ({len(personalities)} personalities)[/yellow]")
                    return self._filter_personalities(personalities, tags, author)
                except Exception:
                    pass
            
            raise NetworkError(f"Failed to fetch personality list: {e}")
    
    def _filter_personalities(
        self,
        personalities: List[PersonalityInfo],
        tags: Optional[List[str]] = None,
        author: Optional[str] = None
    ) -> List[PersonalityInfo]:
        """Filter personalities by tags and author.
        
        Args:
            personalities: List of personalities to filter
            tags: Tags to filter by
            author: Author to filter by
            
        Returns:
            Filtered list of personalities
        """
        filtered = personalities
        
        if tags:
            tag_set = set(tags)
            filtered = [
                p for p in filtered
                if any(tag in tag_set for tag in p.tags)
            ]
        
        if author:
            filtered = [
                p for p in filtered
                if p.author and author.lower() in p.author.lower()
            ]
        
        return filtered
    
    async def download_personality(
        self,
        personality_name: str,
        version: Optional[str] = None,
        force_download: bool = False
    ) -> DownloadResult:
        """Download a personality from the repository.
        
        Args:
            personality_name: Name of the personality to download
            version: Specific version to download (latest if None)
            force_download: Force download even if cached
            
        Returns:
            Download result with success status and file path
        """
        start_time = datetime.now()
        
        # Check if already cached
        cache_key = f"personality_{personality_name}_{version or 'latest'}"
        local_path = self.cache_dir / f"{personality_name}.json"
        
        if not force_download and local_path.exists():
            cached_data = await self.cache_manager.get(cache_key)
            if cached_data:
                try:
                    # Verify the cached file is valid
                    with open(local_path, 'r', encoding='utf-8') as f:
                        json.load(f)  # Validate JSON
                    
                    self.console.print(f"[green]Using cached personality: {personality_name}[/green]")
                    return DownloadResult(
                        success=True,
                        personality_name=personality_name,
                        local_path=local_path,
                        cached=True,
                        size=local_path.stat().st_size,
                        download_time=0
                    )
                except Exception as e:
                    self.console.print(f"[yellow]Cached file is invalid, re-downloading: {e}[/yellow]")
        
        # Download from repository
        try:
            self.console.print(f"[blue]Downloading personality: {personality_name}[/blue]")
            
            # Get personality info first
            personalities = await self.list_available_personalities()
            personality_info = None
            
            for p in personalities:
                if p.name == personality_name:
                    personality_info = p
                    break
            
            if not personality_info:
                return DownloadResult(
                    success=False,
                    personality_name=personality_name,
                    error_message=f"Personality '{personality_name}' not found in repository"
                )
            
            # Download the personality file
            download_url = personality_info.download_url
            if not download_url:
                download_url = f"{self.download_endpoint}/{personality_name}"
                if version:
                    download_url += f"/{version}"
            
            response = await self.http_client.get(download_url)
            response.raise_for_status()
            
            personality_data = response.json()
            
            # Save to local file
            ensure_directory(local_path.parent)
            await write_json_file(local_path, personality_data)
            
            # Cache the download info
            await self.cache_manager.set(
                cache_key,
                json.dumps(personality_data),
                ttl=self.personality_cache_duration.total_seconds()
            )
            
            download_time = (datetime.now() - start_time).total_seconds()
            file_size = local_path.stat().st_size
            
            self.console.print(f"[green]Successfully downloaded: {personality_name}[/green]")
            
            return DownloadResult(
                success=True,
                personality_name=personality_name,
                local_path=local_path,
                cached=False,
                size=file_size,
                download_time=download_time
            )
            
        except Exception as e:
            return DownloadResult(
                success=False,
                personality_name=personality_name,
                error_message=f"Failed to download personality: {e}"
            )
    
    async def download_multiple_personalities(
        self,
        personality_names: List[str],
        versions: Optional[Dict[str, str]] = None,
        force_download: bool = False,
        max_concurrent: int = 3
    ) -> List[DownloadResult]:
        """Download multiple personalities concurrently.
        
        Args:
            personality_names: List of personality names to download
            versions: Optional dict mapping personality names to versions
            force_download: Force download even if cached
            max_concurrent: Maximum concurrent downloads
            
        Returns:
            List of download results
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def download_with_semaphore(name: str) -> DownloadResult:
            async with semaphore:
                version = versions.get(name) if versions else None
                return await self.download_personality(name, version, force_download)
        
        tasks = [download_with_semaphore(name) for name in personality_names]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(DownloadResult(
                    success=False,
                    personality_name=personality_names[i],
                    error_message=str(result)
                ))
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def update_personality(
        self,
        personality_name: str,
        check_only: bool = False
    ) -> DownloadResult:
        """Update a personality to the latest version.
        
        Args:
            personality_name: Name of the personality to update
            check_only: Only check if update is available, don't download
            
        Returns:
            Download result
        """
        # Get local version info
        local_path = self.cache_dir / f"{personality_name}.json"
        local_version = None
        
        if local_path.exists():
            try:
                with open(local_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    local_version = data.get('version')
            except Exception:
                pass
        
        # Get remote version info
        personalities = await self.list_available_personalities()
        remote_personality = None
        
        for p in personalities:
            if p.name == personality_name:
                remote_personality = p
                break
        
        if not remote_personality:
            return DownloadResult(
                success=False,
                personality_name=personality_name,
                error_message=f"Personality '{personality_name}' not found in repository"
            )
        
        # Check if update is needed
        if local_version and local_version == remote_personality.version:
            if check_only:
                return DownloadResult(
                    success=True,
                    personality_name=personality_name,
                    error_message="Already up to date"
                )
            else:
                self.console.print(f"[green]{personality_name} is already up to date[/green]")
                return DownloadResult(
                    success=True,
                    personality_name=personality_name,
                    local_path=local_path,
                    cached=True
                )
        
        if check_only:
            return DownloadResult(
                success=True,
                personality_name=personality_name,
                error_message=f"Update available: {local_version} -> {remote_personality.version}"
            )
        
        # Download the update
        self.console.print(f"[blue]Updating {personality_name}: {local_version} -> {remote_personality.version}[/blue]")
        return await self.download_personality(personality_name, force_download=True)
    
    async def list_local_personalities(self) -> List[PersonalityInfo]:
        """List locally cached personalities.
        
        Returns:
            List of local personalities
        """
        local_personalities = []
        
        for file_path in self.cache_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                personality_info = PersonalityInfo(
                    name=data.get('name', file_path.stem),
                    version=data.get('version', 'unknown'),
                    description=data.get('description', 'No description'),
                    author=data.get('author'),
                    tags=data.get('tags', []),
                    last_updated=datetime.fromtimestamp(file_path.stat().st_mtime),
                    size=file_path.stat().st_size
                )
                
                local_personalities.append(personality_info)
                
            except Exception as e:
                self.console.print(f"[yellow]Failed to read {file_path}: {e}[/yellow]")
        
        return local_personalities
    
    async def clear_cache(self, personality_name: Optional[str] = None) -> bool:
        """Clear the personality cache.
        
        Args:
            personality_name: Specific personality to clear (all if None)
            
        Returns:
            Success status
        """
        try:
            if personality_name:
                # Clear specific personality
                cache_key = f"personality_{personality_name}_latest"
                await self.cache_manager.delete(cache_key)
                
                local_path = self.cache_dir / f"{personality_name}.json"
                if local_path.exists():
                    local_path.unlink()
                
                self.console.print(f"[green]Cleared cache for: {personality_name}[/green]")
            else:
                # Clear all personalities
                await self.cache_manager.clear_pattern("personality_*")
                
                if self.cache_dir.exists():
                    shutil.rmtree(self.cache_dir)
                    ensure_directory(self.cache_dir)
                
                self.console.print("[green]Cleared all personality cache[/green]")
            
            return True
            
        except Exception as e:
            self.console.print(f"[red]Failed to clear cache: {e}[/red]")
            return False


async def create_downloader(
    console: Optional[Console] = None,
    cache_dir: Optional[Path] = None
) -> PersonalityDownloader:
    """Create a configured personality downloader.
    
    Args:
        console: Optional Rich console for output
        cache_dir: Optional cache directory
        
    Returns:
        Configured downloader instance
    """
    from ..utils.http import create_http_client
    from ..utils.cache import get_cache_manager
    
    http_client = await create_http_client()
    cache_manager = await get_cache_manager()
    
    return PersonalityDownloader(
        http_client=http_client,
        cache_manager=cache_manager,
        console=console,
        cache_dir=cache_dir
    )
