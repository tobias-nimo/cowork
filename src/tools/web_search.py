# tools/web_research.py

import asyncio
from concurrent.futures import ThreadPoolExecutor

from langchain_mcp_adapters.client import MultiServerMCPClient

from ..config import settings


async def _load_tavily_mcp_tools() -> list:
    client = MultiServerMCPClient(
        {
            "tavily": {
                "command": "npx",
                "args": ["-y", "tavily-mcp@0.1.4"],
                "env": {
                    "TAVILY_API_KEY": settings.tavily_api_key,
                },
                "transport": "stdio",
            }
        }
    )
    return await client.get_tools()


def _load_tools_sync() -> list:
    """Load Tavily MCP tools, compatible with both sync and already-running event loops."""
    try:
        asyncio.get_running_loop()
        # We're inside a running event loop — run in a dedicated thread.
        with ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(asyncio.run, _load_tavily_mcp_tools()).result()
    except RuntimeError:
        # No running event loop — safe to call asyncio.run() directly.
        return asyncio.run(_load_tavily_mcp_tools())


# Load tools once at module import time.
tavily_tools = _load_tools_sync()
