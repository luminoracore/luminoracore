"""HTTP utilities for LuminoraCore CLI."""

import httpx
import asyncio
from typing import Dict, Any, Optional, Union
from pathlib import Path
import json

from luminoracore_cli.utils.errors import CLIError
from luminoracore_cli.utils.console import console


class HTTPClient:
    """HTTP client for LuminoraCore API interactions."""
    
    def __init__(
        self,
        base_url: str = "https://api.luminoracore.com/v1",
        api_key: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        
        # Setup headers
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "LuminoraCore-CLI/1.0.0"
        }
        
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        for attempt in range(self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.request(
                        method=method,
                        url=url,
                        headers=self.headers,
                        json=data,
                        params=params
                    )
                    
                    # Handle HTTP errors
                    if response.status_code >= 400:
                        if response.status_code == 401:
                            raise CLIError("Authentication failed. Check your API key.")
                        elif response.status_code == 404:
                            raise CLIError(f"Resource not found: {endpoint}")
                        elif response.status_code == 429:
                            raise CLIError("Rate limit exceeded. Please try again later.")
                        else:
                            raise CLIError(f"HTTP {response.status_code}: {response.text}")
                    
                    # Parse JSON response
                    try:
                        return response.json()
                    except json.JSONDecodeError:
                        raise CLIError(f"Invalid JSON response: {response.text}")
                        
            except httpx.TimeoutException:
                if attempt < self.max_retries:
                    console.print(f"[yellow]Request timeout, retrying... ({attempt + 1}/{self.max_retries})[/yellow]")
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    raise CLIError("Request timeout after multiple retries")
                    
            except httpx.ConnectError:
                if attempt < self.max_retries:
                    console.print(f"[yellow]Connection error, retrying... ({attempt + 1}/{self.max_retries})[/yellow]")
                    await asyncio.sleep(2 ** attempt)
                    continue
                else:
                    raise CLIError("Failed to connect to LuminoraCore API")
                    
            except Exception as e:
                raise CLIError(f"Request failed: {str(e)}")
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request."""
        return await self._make_request("GET", endpoint, params=params)
    
    async def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make POST request."""
        return await self._make_request("POST", endpoint, data=data)
    
    async def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make PUT request."""
        return await self._make_request("PUT", endpoint, data=data)
    
    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request."""
        return await self._make_request("DELETE", endpoint)
    
    async def download_file(self, url: str, output_path: Path) -> None:
        """Download file from URL."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream("GET", url, headers=self.headers) as response:
                    if response.status_code >= 400:
                        raise CLIError(f"Failed to download file: HTTP {response.status_code}")
                    
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(output_path, "wb") as f:
                        async for chunk in response.aiter_bytes():
                            f.write(chunk)
                            
        except Exception as e:
            raise CLIError(f"Failed to download file: {str(e)}")


def create_http_client(
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: Optional[int] = None,
    max_retries: Optional[int] = None
) -> HTTPClient:
    """Create HTTP client with optional configuration."""
    return HTTPClient(
        base_url=base_url or "https://api.luminoracore.com/v1",
        api_key=api_key,
        timeout=timeout or 30,
        max_retries=max_retries or 3
    )


async def test_connection(client: HTTPClient) -> bool:
    """Test connection to LuminoraCore API."""
    try:
        await client.get("/health")
        return True
    except CLIError:
        return False
