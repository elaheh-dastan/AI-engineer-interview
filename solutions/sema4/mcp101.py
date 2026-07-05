# I implemented a read-only MCP server that exposed internal knowledge-base/runbook search to an AI coding assistant. The server exposed typed tools, resources, and prompts; the host application handled 
# model interaction, user consent, and tool invocation. I used stdio for local IDE usage and Streamable HTTP for remote deployment.”

# server.py

from mcp.server.fastmcp import FastMCP

# The host application connects to this server and discovers what tools it exposes. The host is usually something like Claude.
mcp = FastMCP("runbook-search")

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

# In production this would call our internal search service or documentation database.

