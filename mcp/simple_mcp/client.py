import asyncio
from mcp import Client
from dotenv import load_dotenv
from openai import AsyncOpenAI
import json 

# SETUP THE ENVIRONMENT
load_dotenv()
MCP_SERVER_URL = "http://localhost:8000/mcp"

async def main():
    query = input("Enter banking query: ")
    async with Client(MCP_SERVER_URL) as mcp_client, AsyncOpenAI() as ai_client:
        tool_list = await mcp_client.list_tools()
        tools = [
                {
                    "type": "function",
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema
                }
                for tool in tool_list.tools
        ]
        
        # LET MODEL CHOOSE A TOOL
        response = await ai_client.responses.create(
            model="gpt-5.6-luna",
            input=query,
            tools=tools,
            parallel_tool_calls=False,
            instructions="Use tools for banking requests, ask for missing account or card IDs if required."
        )
        for item in response.output:
            if item.type == "function_call":
                print(f"LLM SELECTED TOOL: {item.name}")
                result = await mcp_client.call_tool(item.name,json.loads(item.arguments))
                print(result.content[0].text)

asyncio.run(main())