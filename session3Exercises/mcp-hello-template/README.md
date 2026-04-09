# mcp-hello-template

A minimal, working MCP server you can fork and modify in 20 minutes. Used in Session 3, Track B of the MCP exercise.

## What this is

A complete Model Context Protocol server written in ~30 lines of Python. It wraps a local folder (`~/notes/`) and exposes two tools to Claude Code:

- `list_notes()` → list files in `~/notes`
- `read_note(name)` → read a specific file

That's it. That's the whole server. The point is to show you that an MCP server is *just a small program* that exposes named functions with typed arguments.

## Quickstart (2 minutes)

```bash
# 1. Fork this template into your own workspace
cp -r session3Exercises/mcp-hello-template ~/my-first-mcp
cd ~/my-first-mcp

# 2. Install the MCP Python SDK
pip install --break-system-packages mcp
# (or: uv pip install mcp)

# 3. Make sure there's something to list
mkdir -p ~/notes
echo "hello from my first MCP server" > ~/notes/test.txt

# 4. Sanity-check that server.py boots
python server.py
# It will wait silently on stdio. Ctrl+C to stop.

# 5. Wire it into Claude Code
claude mcp add --transport stdio notes -- python $(pwd)/server.py

# 6. Restart Claude Code, then inside Claude:
/mcp
# You should see "notes" listed as connected.

# 7. Ask Claude to use it:
# "What notes do I have? Read the test one."
```

If Claude calls `list_notes()` and then `read_note("test.txt")` and shows you the content — it works.

## Modify it

Open `server.py`. There are three things to notice:

1. **`FastMCP("notes")`** — creates the server and gives it a name. The name is what shows up in `/mcp`.
2. **`@mcp.tool()`** — any Python function with this decorator becomes a tool Claude can call. The function's **docstring** is what Claude reads to decide *when* to call it, so write docstrings like you mean them.
3. **Type hints matter.** `name: str` → Claude knows to pass a string. `-> list[str]` → Claude knows what comes back.

That's the whole mental model. Change the tool bodies to do whatever you want.

### Ideas for what to wrap

Pick something you actually have on disk or can easily reach:

- **A folder of logs.** `list_logs()`, `read_log(name)`, `search_logs(pattern)`.
- **A script you run daily.** Wrap it in a tool: `run_daily_report() → str`.
- **A local JSON/CSV file.** `get_team_members()`, `find_conventions(topic)`.
- **A `curl` command against an internal API.** Put the curl in a tool, have it parse the JSON and return it.
- **A SQLite or local Postgres.** `query(sql) → rows`.
- **Your `.claude/conventions/` folder.** `get_convention(topic)` for team-specific guidance.

### After you modify it

Every time you change `server.py`, do **one** of:

- Run `/mcp reconnect` inside Claude Code, or
- Restart Claude Code entirely.

Then test by asking Claude to do something that would use your new tool.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `/mcp` shows "failed" | Run `python server.py` in your terminal and look for the error |
| `ModuleNotFoundError: mcp` | The `pip install mcp` ran in a different Python. Check `which python`. |
| Claude doesn't call the tool | Your docstring isn't descriptive enough — Claude picks tools by their descriptions |
| Tool returns nothing | Check the tool function in isolation: `python -c "from server import list_notes; print(list_notes())"` |
| Changes not picked up | You didn't `/mcp reconnect` or restart Claude |

## What this template is NOT

- Not production-ready. It has no auth, no rate limiting, no error handling beyond the basics.
- Not a complete guide to the MCP protocol. See https://modelcontextprotocol.io and https://github.com/modelcontextprotocol/python-sdk for the full story.
- Not the only way to write an MCP server. There are Node, Go, Rust, and TypeScript SDKs too. Python with FastMCP is just the lowest-friction path for a 20-minute workshop.

## Resources

- **MCP docs (Claude Code):** https://code.claude.com/docs/en/mcp
- **Python SDK:** https://github.com/modelcontextprotocol/python-sdk
- **Protocol spec:** https://modelcontextprotocol.io
- **Registry of existing servers:** https://registry.modelcontextprotocol.io
