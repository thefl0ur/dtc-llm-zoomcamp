import asyncio
from fastmcp import Client

async def main():
    async with Client("weather_server.py") as mcp_client:
        tools = await mcp_client.list_tools()
        print(f"Available tools: {tools}")
        result = await mcp_client.call_tool("get_weather", {"city": "berlin"})
        print(f"Result: {result}")

if __name__ == "__main__":
    test = asyncio.run(main())