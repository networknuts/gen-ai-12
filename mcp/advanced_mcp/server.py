import requests
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("Banking: Tool, Resource, and Prompt")


@mcp.tool()
def get_balance(account_id: str):
    """Get the live balance, account type, and holder for a bank account."""
    try:
        response = requests.get(
            f"http://127.0.0.1:8080/accounts/{account_id}/balance", timeout=5
        )
    except requests.RequestException as exc:
        raise ToolError("Start the banking API on port 8080.") from exc
    if not response.ok:
        raise ToolError(str(response.json()["detail"]))
    return response.json()


@mcp.resource("banking://policies/minimum-balance")
def minimum_balance_policy():
    """Read the fictional minimum-balance policy for this demo bank."""
    return """Demo bank policy (fictional):
Savings accounts require a minimum balance of INR 10,000.00.
Current accounts require a minimum balance of INR 50,000.00.
This policy checks the current balance, not a monthly average.
A balance equal to or above the minimum meets the requirement.
No fees or penalties are defined by this demo policy.
"""


@mcp.prompt()
def review_account(query: str):
    """Help with a full banking request using account data and the demo policy."""
    return f"""Answer the user's banking request below.
Use get_balance when account data is needed. Ask for the account ID if missing.
For policy-only questions, answer from the supplied policy without calling a tool.
For an account review, use three headings: Balance, Policy check, and Next step.
Show the surplus or shortfall and any top-up needed when the user asks about the minimum.
If the request is just an account ID, treat it as a request to review that account.
Only balance lookup and policy explanations are available; explain other limitations.
If the policy is missing, say the minimum is unknown. Do not invent a threshold.
If the tool fails, explain the error instead of inventing account details.

User request:
{query}
"""


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8001, json_response=True)
