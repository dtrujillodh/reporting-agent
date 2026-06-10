import asyncio
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

async def list_tools():
    tool = McpToolset(connection_params=StreamableHTTPConnectionParams(url='http://127.0.0.1:8000/mcp'))
    tools = await tool.get_tools()
    print(tools)

if __name__ == "__main__":
    asyncio.run(list_tools())
