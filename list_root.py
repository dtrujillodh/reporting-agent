import asyncio
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

async def list_root():
    tool = McpToolset(connection_params=StreamableHTTPConnectionParams(url='http://127.0.0.1:8000/mcp'))
    # Try using 'root' as folder_id
    try:
        files = await tool.call('list_folder_files', {'folder_id': 'root'})
        print(files)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(list_root())
