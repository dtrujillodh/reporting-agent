import asyncio
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

async def list_root():
    tool = McpToolset(connection_params=StreamableHTTPConnectionParams(url='http://127.0.0.1:8000/mcp'))
    tools = await tool.get_tools()
    list_tool = next(t for t in tools if t.name == 'list_folder_files')
    # Using internal method _execute_with_session as found in dir()
    files = await tool._execute_with_session(list_tool, {'folder_id': 'root'})
    print(files)

if __name__ == "__main__":
    asyncio.run(list_root())
