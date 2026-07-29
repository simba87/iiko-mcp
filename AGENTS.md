# AGENTS.md

Instructions for AI agents working on this repository.

## Context
This is an MCP (Model Context Protocol) server for the iiko restaurant management system REST API (iikoServer). It wraps iikoServer endpoints as MCP tools.

- **get_revenue_at_time** — Get revenue up to a specific time on a given date.
## Key files
- `server.py` — main MCP server with all tool definitions
- `README.md` — user-facing documentation listing all tools
- `requirements.txt` — Python dependencies

## Tool patterns
All tools follow this pattern:
1. Define the tool schema with `@tool(...)` decorator
2. Implement the async handler function
3. Register the handler in `ToolRegistry`

## Testing
- Run `python3 -m py_compile server.py` for syntax validation
- The server connects to an iikoServer instance for actual testing

## README
After adding a tool, always update README.md with a brief description.
