# I implemented a read-only MCP server that exposed internal knowledge-base/runbook search to an AI coding assistant. The server exposed typed tools, resources, and prompts; the host application handled 
# model interaction, user consent, and tool invocation. I used stdio for local IDE usage and Streamable HTTP for remote deployment.”

# server.py

from mcp.server.fastmcp import FastMCP

# The host application connects to this server and discovers what tools it exposes. The host is usually something like Claude.
mcp = FastMCP("runbook-search")

# In production this would call our internal search service or documentation database.
DOCS = [
    {
        "title": "Rollback deployment",
        "body": "Use deployctl rollback --service <name> --to <version>.",
    },
    {
        "title": "Database migration",
        "body": "Use expand-contract migrations, take a backup, and avoid long locks.",
    },
    {
        "title": "Incident review",
        "body": "Include impact, timeline, root cause, action items, owners, and due dates.",
    },
]

# The decorator exposes this function as a model-callable MCP tool. The host can list it, inspect its schema, and call it with arguments.
@mcp.tool()
def search_runbook(query: str) -> list[dict[str, str]]:
    # The model sees this description when deciding whether to call the tool. This is more important than it looks. Good tool descriptions improve tool selection.
    """Search internal runbook documents by keyword."""
    query = query.lower()
