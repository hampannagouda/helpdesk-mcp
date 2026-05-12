import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    print("Starting MCP Client...")
    
    # Configure the parameters to start the MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
    )

    # Connect to the server using standard I/O
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            print("Initializing session...")
            await session.initialize()
            
            print("Listing available tools...")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f" - Tool found: {tool.name}")

            print("\nCalling 'create_ticket' tool...")
            result = await session.call_tool(
                "create_ticket",
                arguments={"title": "Verification Ticket from Client Script"}
            )
            
            print("---------------------------------")
            print("Tool Response:")
            print(result)
            print("---------------------------------")
            print("Verification Complete! The MCP Server is fully operational.")

if __name__ == "__main__":
    asyncio.run(main())
