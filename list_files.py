import asyncio
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

async def list_root():
    toolset = McpToolset(connection_params=StreamableHTTPConnectionParams(url='http://127.0.0.1:8000/mcp'))
    # The tools are dynamically loaded, let's try to access them directly
    print("Available tools:", toolset.tools)
    # If the toolset structure is different, I might need to inspect it.
    # Given the previous error, McpToolset might not have a 'call' method.
    # Let's try listing the tools first.

if __name__ == "__main__":
    asyncio.run(list_root())
