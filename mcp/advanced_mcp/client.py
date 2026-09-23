import asyncio
import json
import os

from dotenv import load_dotenv
from mcp import Client
from openai import AsyncOpenAI

load_dotenv()


async def main():
    query = input("Enter banking request: ")
    model = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
    instructions = (
        "Use the tool for account data and the supplied policy for minimums. "
        "Ask for missing account IDs. Never invent facts or claim unsupported actions."
    )

    async with Client("http://localhost:8001/mcp") as mcp_client, AsyncOpenAI() as ai_client:
        # 1. Read the resource: context for the model.
        resource = await mcp_client.read_resource("banking://policies/minimum-balance")
        policy = resource.contents[0].text
        print("RESOURCE:\n" + policy)

        # 2. Get the prompt: reusable instructions around the user's full request.
        prompt = await mcp_client.get_prompt("review_account", {"query": query})
        request = prompt.messages[0].content.text
        print("PROMPT:\n" + request)
        messages = [
            {"role": "user", "content": "Bank policy context:\n" + policy},
            {"role": "user", "content": request},
        ]

        # 3. Give the model the available tool.
        tool_list = await mcp_client.list_tools()
        tools = [
            {"type": "function", "name": tool.name, "description": tool.description,
             "parameters": tool.input_schema, "strict": False}
            for tool in tool_list.tools
        ]
        response = await ai_client.responses.create(
            model=model, instructions=instructions, input=messages,
            tools=tools, parallel_tool_calls=False,
        )

        # 4. Execute the tool and send its result back for the final answer.
        for call in response.output:
            if call.type == "function_call":
                print("TOOL:", call.name)
                result = await mcp_client.call_tool(call.name, json.loads(call.arguments))
                text = result.content[0].text
                print("TOOL ERROR: " if result.is_error else "TOOL RESULT: ", text, sep="")
                messages.extend(response.output)
                messages.append({
                    "type": "function_call_output", "call_id": call.call_id,
                    "output": json.dumps({"is_error": result.is_error, "text": text}),
                })
                response = await ai_client.responses.create(
                    model=model, instructions=instructions, input=messages,
                )
                break

        print("ANSWER:\n" + response.output_text)


if __name__ == "__main__":
    asyncio.run(main())
