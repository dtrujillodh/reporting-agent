import asyncio
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

async def list_root():
    tool = McpToolset(connection_params=StreamableHTTPConnectionParams(url='http://127.0.0.1:8000/mcp'))
    # Assuming tool.execute or similar method exists
    try:
        # Based on toolset methods listed, maybe list_resources?
        resources = await tool.list_resources()
        print(resources)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(list_root())
