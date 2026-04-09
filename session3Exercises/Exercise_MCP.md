# Exercise: MCP — connect or build

**Duration:** 25 min hands-on + 5 min round-robin
**Format:** Two self-selected tracks. Pick one.

---

## Before you start

1. Run `/mcp` in Claude Code and see which MCP servers are already configured for you. If the list is empty, that's normal — that's the whole point of this exercise.
2. Open `.mcp.json` in your project (if it exists) and look at the structure.
3. Make a quick decision: **Track A or Track B?**

### Track A — Connect a real one
Pick this if you have credentials (API keys, tokens) for a system you'd like to give Claude access to, or if you just want to see a real external system phone home. You'll wire up a real MCP server and use it for an actual task.

### Track B — Build a tiny one
Pick this if you don't have credentials for anything, or if you'd rather understand the *anatomy* of an MCP server. You fork a minimal Python template (`mcp-hello-template/`) and modify it to wrap something you have on disk — a JSON file, a local database, a script you run daily, a folder of logs.

**Both tracks end with the same deliverable:** a list of **3 concrete tasks you can now do that were hard or impossible before.** Write them down — we use them in the lightning round afterward.

---

## Track A — Connect a real one

### Step 1: Pick a server (2 min)

Pick from the cheat sheet below. Choose something you actually have credentials for, or something that runs locally without auth.

| Server | Good for | Credentials | Command |
|---|---|---|---|
| **GitHub** | PRs, issues, code search, commits | Personal Access Token (`repo`, `read:org`) | `claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer $GITHUB_TOKEN"` |
| **Sentry** | Errors, issues, Seer analysis | OAuth on first use | `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp` |
| **Linear** | Issues, projects, comments | OAuth on first use | `claude mcp add --transport http linear https://mcp.linear.app/mcp` |
| **Notion** | Docs, databases | OAuth | `claude mcp add --transport http notion https://mcp.notion.com/mcp` |
| **Datadog** (official) | Metrics, logs, monitors, incidents | `DD_API_KEY` + `DD_APP_KEY` | See https://docs.datadoghq.com/bits_ai/mcp_server/ |
| **Postgres** (local) | Query a real DB | Connection string | See "Throwaway Postgres" below |
| **Your own ticket/issue tracker** | Whatever you use | Whatever it requires | Check https://registry.modelcontextprotocol.io |

**If you use something not on the list:** search https://registry.modelcontextprotocol.io — the official MCP registry, launched Sept 2025, backed by Anthropic + GitHub + Microsoft.

### Throwaway Postgres (if you don't have a database)

In one terminal:
```bash
docker run --rm -e POSTGRES_PASSWORD=test -p 5432:5432 postgres:16
```

In another terminal, seed it with some data:
```bash
psql postgresql://postgres:test@localhost:5432/postgres -c "
  CREATE TABLE orders (id int, customer text, total numeric, created_at timestamp);
  INSERT INTO orders VALUES
    (1, 'Maersk', 12500, '2026-04-01'),
    (2, 'MSC', 8900, '2026-04-02'),
    (3, 'CMA CGM', 15200, '2026-04-03');
"
```

Then wire it up:
```bash
claude mcp add --transport stdio localdb \
  -- npx -y @bytebase/dbhub --dsn "postgresql://postgres:test@localhost:5432/postgres"
```

### Step 2: Wire it up (5 min)

1. Run `claude mcp add` with your chosen server.
2. Restart Claude Code (or run `/mcp reconnect` if that's enough).
3. Run `/mcp` and verify the server shows as **connected**.
4. Ask Claude: *"What tools do you have from the [name] MCP server?"* — it should list them.

**If it fails:**
- Read the `/mcp` output — the reason is usually right there.
- Check JSON syntax in `.mcp.json` if you edited it directly. Trailing commas kill it.
- Windows: use forward slashes in paths, and wrap `npx` in `cmd /c`.
- Token problems: check scopes, and that env vars are actually exported in the shell where you started Claude.

### Step 3: Do something real (15 min)

This is the important part. Use the server to do an actual task that previously would have cost you time, context-switching, or fumbling with UIs.

Suggestions — pick one or invent your own:

- *"Find the 3 most-triggered Sentry issues this week and propose a triage plan with links to the files most likely to be the root cause."*
- *"Pull the open issues assigned to me in Linear, group them by project, and suggest which three I should close out this week."*
- *"Query the `orders` table and tell me which customer grew the most in the last 7 days. Explain your query."*
- *"Read the most recent 5 open PRs in [repo] via GitHub MCP and summarize the review status of each."*
- *"Find the Datadog monitor that's alerted most often this month and suggest a tighter threshold based on the actual metric distribution."*

If you're using Track A on your own ticket system: take a real sprint task or bug report and run it through the Research → Plan → Implement workflow from Session 1, but with the Research phase now using your new MCP.

### Step 4: Write down "tasks now possible" (2 min)

Before we move on, write 3 concrete tasks you can now do that were hard or impossible before. These are what you'll use in the lightning round.

---

## Track B — Build a tiny one

The goal is *not* to build something production-ready. The goal is for you to see **the anatomy of an MCP server**, so you can build one when you actually need to.

### Step 1: Fork the template (3 min)

The template lives in `session3Exercises/mcp-hello-template/`. Copy it to your own workspace:

```bash
cp -r session3Exercises/mcp-hello-template ~/my-first-mcp
cd ~/my-first-mcp
```

The template is a complete, working MCP server in under 30 lines of Python. It exposes two tools:
- `list_notes()` — lists files in `~/notes/`
- `read_note(name)` — reads a specific file

### Step 2: Install and wire it up (5 min)

```bash
# Install MCP Python SDK
pip install --break-system-packages mcp
# or with uv (faster, recommended if you have uv)
uv pip install mcp

# Sanity check
python server.py
# (Ctrl+C to stop — it's waiting on stdio input)

# Wire it up in Claude Code
claude mcp add --transport stdio notes -- python $(pwd)/server.py

# Restart CC and verify
/mcp
```

Claude should now see the `notes` server. Ask it: *"What notes do I have?"* — if it calls `list_notes()`, it works.

### Step 3: Modify it to wrap something YOU have (15 min)

This is the interesting part. Change the template so it wraps something you actually use. Three good categories:

**1. A folder of files**
- Logs (`~/logs/`)
- Notes, docs, cheat sheets (`~/Documents/notes/`)
- Repo-specific things (`.claude/conventions/`)

**2. A script you run daily**
- A helper that dumps the status of something
- A CLI that prints JSON
- A `curl` command that hits an internal API

**3. A local JSON/CSV file**
- Team structure
- Repo conventions
- An exported dataset

**Mechanic:** modify the `list_notes` and `read_note` functions in `server.py`. Add a third tool if you like. Notice how little code it takes to expose something.

Every time you change the file, restart Claude Code (or run `/mcp reconnect`) so it picks up the changes.

### Step 4: Write down "tasks now possible" (2 min)

Same deliverable as Track A. 3 concrete tasks your new server enables.

---

## After the exercise — round-robin

Each pair says one thing out loud: *"The one task I can now do that used to be annoying is: ___"*. 20 seconds per pair. No demo, just the sentence. This feeds the lightning round.

---

## Troubleshooting cheat sheet

| Symptom | Likely cause | Fix |
|---|---|---|
| `/mcp` shows the server as "failed" | Command can't start | Run it manually in the terminal — see what it screams |
| Claude says "no tools from that server" | No tools registered | Check that you have the `@mcp.tool()` decorator in the Python template |
| `.mcp.json` not loading | Wrong location | It belongs in the project root, not in `.claude/` |
| Changes to server.py not picked up | Old process still running | Restart CC, or `/mcp reconnect` |
| Env vars missing | Shell scope | Export them in the same shell where you start `claude` |
| Trailing comma in JSON | … | Validate `.mcp.json` in a JSON linter |

---

## Resources

- **MCP docs:** https://code.claude.com/docs/en/mcp
- **Official registry:** https://registry.modelcontextprotocol.io
- **Python SDK:** https://github.com/modelcontextprotocol/python-sdk
- **Datadog MCP (official):** https://docs.datadoghq.com/bits_ai/mcp_server/
- **Popular servers (live list):** the "Popular MCP servers" section on https://code.claude.com/docs/en/mcp
