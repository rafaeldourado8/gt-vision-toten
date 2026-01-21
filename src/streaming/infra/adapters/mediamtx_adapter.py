"""MediaMTX adapter."""
import httpx
from typing import Dict, Any


class MediaMTXAdapter:
    """MediaMTX API adapter."""

    def __init__(self, api_url: str, username: str, password: str) -> None:
        self._api_url = api_url.rstrip("/")
        self._auth = (username, password)

    async def add_path(self, stream_path: str, source_url: str) -> bool:
        """Add path to MediaMTX."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self._api_url}/v3/config/paths/add/{stream_path}",
                    json={"source": source_url},
                    auth=self._auth,
                    timeout=10.0,
                )
                return response.status_code in [200, 201]
        except Exception:
            return False

    async def remove_path(self, stream_path: str) -> bool:
        """Remove path from MediaMTX."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self._api_url}/v3/config/paths/remove/{stream_path}",
                    auth=self._auth,
                    timeout=10.0,
                )
                return response.status_code in [200, 204]
        except Exception:
            return False

    async def get_path_status(self, stream_path: str) -> Dict[str, Any] | None:
        """Get path status from MediaMTX."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._api_url}/v3/paths/get/{stream_path}",
                    auth=self._auth,
                    timeout=10.0,
                )
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception:
            return None

    async def list_paths(self) -> list[Dict[str, Any]]:
        """List all paths from MediaMTX."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._api_url}/v3/paths/list",
                    auth=self._auth,
                    timeout=10.0,
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("items", [])
                return []
        except Exception:
            return []
