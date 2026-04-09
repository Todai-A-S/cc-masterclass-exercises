"""
Minimal MCP server — hello world template.

This is a complete, working MCP server in under 30 lines. It exposes two tools
that wrap a local folder (`~/notes/`):
  - list_notes()    → returns all files in ~/notes
  - read_note(name) → returns the contents of a specific file

Your job in Track B of the MCP exercise is to fork this file and change the
tools so they wrap something YOU actually have on disk — a log folder, a
config file, a CLI you run every day, a JSON export, whatever.

## Setup

    pip install --break-system-packages mcp
    # or, if you use uv:
    uv pip install mcp

## Run it standalone to verify it boots

    python server.py
    # (it will wait for stdio input — hit Ctrl+C to stop)

## Wire it up to Claude Code

    claude mcp add --transport stdio notes -- python $(pwd)/server.py

Then restart Claude Code and run `/mcp` to verify it shows up.

## Modify it

Each tool is just a Python function with an @mcp.tool() decorator and a
docstring. The docstring matters — it's what Claude reads to decide when to
call the tool. Make it descriptive.

Add a new tool by writing another @mcp.tool()-decorated function. Restart
Claude Code (or `/mcp reconnect`) to pick up changes.
"""

from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP("notes")

NOTES_DIR = os.path.expanduser("~/notes")


@mcp.tool()
def list_notes() -> list[str]:
    """List all note filenames in the user's ~/notes folder.

    Call this when the user asks about their notes, what they've written down,
    or what topics they have captured. Returns an empty list if the folder
    does not exist or is empty.
    """
    if not os.path.isdir(NOTES_DIR):
        return []
    return sorted(os.listdir(NOTES_DIR))


@mcp.tool()
def read_note(name: str) -> str:
    """Read the contents of a specific note by filename.

    Call this after list_notes() to get the actual content of a note the user
    is asking about. The name argument should be the exact filename as
    returned by list_notes().
    """
    path = os.path.join(NOTES_DIR, name)
    if not os.path.isfile(path):
        return f"Error: no such note '{name}' in {NOTES_DIR}"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    mcp.run()
