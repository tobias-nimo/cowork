import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient

_client = MultiServerMCPClient({
    "google-workspace": {
        "command": "gws",
        "args": ["mcp", "-s", "gmail,calendar,drive,docs,sheets", "--tool-mode", "compact"],
        "transport": "stdio",
    }
})


async def _load():
    await _client.__aenter__()
    return _client.get_tools()


gws_tools = asyncio.run(_load())
