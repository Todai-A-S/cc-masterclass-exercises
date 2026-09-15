# Exercise: MCP, connect or build

Time: 25 minutes. Step 0 for everyone 3 min, then Track A or Track B 18 min, share 4 min.

---

## What MCP is

A protocol, not a product. An MCP server is a small program that wraps an external system (GitHub, a database, Sentry, an internal API) and exposes named tools. Claude Code is the client: when it decides it needs data from that system mid-task, it calls the tool and the result lands in the conversation. Fresh, at the moment it's needed. That's the difference from pasting data in.

Two transports you'll use: `http` for a hosted server, `stdio` for a program on your own machine. Three scopes: `local` (you, this project, the default), `project` (`.mcp.json` in the repo, the team gets it), `user` (you, every project).

---

## Step 0: everyone (3 min)

First, in a Claude Code session:

```
/mcp
```

You may already have servers you never installed. On the Team plan, connectors you've added at claude.ai show up here marked "claude.ai". If the list is empty, that's normal too.

Then, in your shell, not inside Claude:

```bash
claude mcp add --transport http claude-code-docs https://code.claude.com/docs/mcp
claude mcp list
```

That's Anthropic's docs server. No login, no token. `claude mcp list` should show `✔ Connected`. Back in Claude:

```
use the claude-code-docs server to look up what MCP_TIMEOUT does
```

The tool call is labelled with the server name. That's how you know the answer came through MCP and not from Claude's own memory. You've now connected one. Pick a track.

---

## Track A or Track B

**Track A, connect a real one.** You have credentials for something (GitHub at minimum, everyone here does) and you want to see Claude pull real data into a real task.

**Track B, build a tiny one.** You want to see the anatomy: how a function with a decorator becomes a tool Claude can call. You fork a 50-line Python template that wraps a SQLite database, then point it at something of yours.

Same deliverable either way: one line in the chat at the end.

---

## Track A: connect a real one

### Step 1: pick a server (2 min)

GitHub is the default; everyone at ZeroNorth has an account. The token needs `repo` and `read:org`, exported in the shell you start Claude from.

| Server | Good for | Auth | Command (run in your shell) |
|---|---|---|---|
| **GitHub** | PRs, issues, code search | Personal access token | `claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer $GITHUB_TOKEN"` |
| **Sentry** | Errors, issues | Browser sign-in | `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp` |
| **Linear** | Issues, projects | Browser sign-in | `claude mcp add --transport http linear https://mcp.linear.app/mcp` |
| **Notion** | Docs, databases | Browser sign-in | `claude mcp add --transport http notion https://mcp.notion.com/mcp` |
| **Datadog** | Monitors, logs, metrics | `DD_API_KEY` + `DD_APP_KEY` | https://docs.datadoghq.com/bits_ai/mcp_server/ |
| **Postgres, throwaway** | A real SQL query | None | See below |
| **Anything else** | | | https://registry.modelcontextprotocol.io |

The GitHub server also ships as a plugin: `/plugin install github@claude-plugins-official` does the `claude mcp add` for you. Same server, packaged. Either way works; the command above shows you what's happening.

**Throwaway Postgres**, if you'd rather query a database than a repo:

```bash
docker run --rm -e POSTGRES_PASSWORD=test -p 5432:5432 postgres:16
```

In a second terminal:

```bash
psql postgresql://postgres:test@localhost:5432/postgres -c "
  CREATE TABLE orders (id int, customer text, total numeric, created_at timestamp);
  INSERT INTO orders VALUES
    (1, 'Maersk', 12500, '2026-09-01'),
    (2, 'MSC', 8900, '2026-09-02'),
    (3, 'CMA CGM', 15200, '2026-09-03');
"
claude mcp add --transport stdio localdb -- npx -y @bytebase/dbhub --dsn "postgresql://postgres:test@localhost:5432/postgres"
```

Note the `--`. Everything after it is the server's own command, passed through untouched. Claude Code's flags go before it. Put a flag on the wrong side and the server starts with arguments it doesn't understand.

### Step 2: wire it up (4 min)

1. Run the `claude mcp add` line in your shell.
2. `claude mcp list`. Read the status; the table at the bottom of this sheet says what each one means.
3. Servers with browser sign-in show `! Needs authentication`. Start Claude, run `/mcp`, select the server, choose **Authenticate**. Or from the shell: `claude mcp login sentry`.
4. In Claude: "what tools do you have from the github server?" It lists them.

### Step 3: do something real (10 min)

The point of the exercise. Use the server on a task you'd otherwise have done by hand in a browser tab.

```
read the 5 most recent open PRs in [org/repo] and summarise the review status of each. which one has been waiting longest?
```

```
find the 3 most-triggered Sentry issues this week and propose a triage order, with the files most likely to be the root cause
```

```
pull the open Linear issues assigned to me, group them by project, and suggest which three to close out this week
```

```
query the orders table: which customer grew the most in the last 7 days? show me the SQL
```

Better: take the task you're actually on this sprint and run Research → Plan → Implement from Session 1, with the research phase now able to read the ticket, the PR history, or the error tracker itself.

While it runs, `/context all` shows what each MCP tool costs you. Tool search is on by default, so an idle server costs almost nothing; only the tools Claude actually uses load their schemas.

### Step 4: share (2 min)

One line in the chat:

> With [server] I can now ___ without leaving the terminal.

A TA reads three out. That's the share-out.

---

## Track B: build a tiny one

Not production. The point is to see that an MCP server is a function with a decorator, so you can write one the day you need it.

### Step 1: fork the template (3 min)

```bash
cp -r session3Exercises/mcp-hello-template ~/my-first-mcp
cd ~/my-first-mcp
```

A complete server in about 50 lines of Python. It wraps a SQLite database and exposes three tools: `list_tables()`, `describe_table(name)`, `run_query(sql)`. SQLite on purpose: Claude can't run SQL on its own, so the first query that lands in the chat makes the point without a slide.

### Step 2: install, seed, wire (5 min)

```bash
pip install --break-system-packages mcp     # or: uv pip install mcp
python seed.py                              # creates ~/mcp-hello.db: customers, shipments
python server.py                            # boots and waits on stdin. Ctrl+C.
claude mcp add --transport stdio mydb -- python $(pwd)/server.py
claude mcp list
```

`which python` must be the same Python that installed `mcp`. If `claude mcp list` says failed, that's the first thing to check.

In Claude: "which customer shipped the most tons in April?" If it calls `list_tables` then `describe_table` then `run_query` and answers from the rows, it works.

### Step 3: wrap something of yours (8 min)

Open `server.py`. Three things carry the whole design:

1. `FastMCP("mydb")`: the name that shows in `/mcp`.
2. `@mcp.tool()`: the decorator that turns a function into a tool.
3. The docstring. Claude reads it to decide when to call the tool. Write it like you mean it: what it does, when to use it, what comes back.

Now change the tools to wrap something Claude can't reach today, in rough order of "value lands instantly":

- A real database: swap `sqlite3` for `psycopg2` and the connection string. Read-only.
- A `curl` against an internal API. Anything behind the VPN or SSO. Parse the JSON, return a dict.
- A status script you already run daily: `run_daily_report() -> str`.
- A local JSON or CSV file Claude doesn't know about.

After each change: `/mcp` in Claude, select the server, reconnect. That's the loop. Restart Claude only if reconnect misses a changed command line.

One limit worth knowing: tool output over 25,000 tokens gets written to a file instead of the chat, with a warning at 10,000. If your `run_query` returns the whole table, Claude gets a file path. Return summaries, or add a `LIMIT`.

### Step 4: share (2 min)

One line in the chat:

> My tool: [docstring, first line]. Without MCP this would have taken ___.

---

## Sharing a server with the team

```bash
claude mcp add --scope project --transport http github https://api.githubcopilot.com/mcp/
```

writes `.mcp.json` in the repo root. Commit it. Teammates get an approval prompt the first time they start Claude in the repo; after that it connects. `claude mcp reset-project-choices` if you rejected one by mistake. Tokens don't go in the file: use `${GITHUB_TOKEN}` and let each person export their own.

Resources and prompts, the two things besides tools: a server's resources show up as `@` mentions, its prompts as `/mcp__github__list_prs` style commands. Neither is today's exercise, but they're in the `@` and `/` menus now.

---

## Troubleshooting

`claude mcp list` from your shell, or `/mcp` inside a session. Match the status.

| Status or symptom | What it means | Fix |
|---|---|---|
| `✘ Failed to connect` | Server didn't start or URL didn't respond. Since 2.1.219 the HTTP status is on the line | Run the command by hand in the terminal and read the error. For stdio: did you put `--` before the command? `claude mcp get <name>` shows what Claude Code will run |
| `! Needs authentication` | Reachable, needs a sign-in or a token | `/mcp` → server → Authenticate, or `--header "Authorization: Bearer ..."` on the add command |
| `⏸ Pending approval` | A project-scope `.mcp.json` you haven't approved | Start `claude` in the repo and approve, or `/mcp` |
| `! Connected · tools fetch failed` | Connected but no tool list | `claude mcp get <name>` for the detail. Usually a missing env var |
| Server connects, no tools | Nothing registered | Track B: the `@mcp.tool()` decorator. Track A: an env var the server needs |
| Changes to `server.py` not picked up | Old process still running | `/mcp` → reconnect |
| `ModuleNotFoundError: mcp` | Wrong Python | `which python` must match the one in `claude mcp add` |
| `.mcp.json` ignored | Wrong place | Repo root. Not `.claude/`, not `~/.claude/` |
| Env var missing | Shell scope | Export it in the shell where you run `claude` |
| Auth fails after pasting a token | Hidden whitespace | `claude mcp list` warns about leading or trailing whitespace. Re-add |
| Windows | Paths and npx | Forward slashes; wrap `npx` in `cmd /c` |

---

## Resources

- MCP in Claude Code: https://code.claude.com/docs/en/mcp
- Quickstart (the docs server walkthrough): https://code.claude.com/docs/en/mcp-quickstart
- Registry: https://registry.modelcontextprotocol.io
- Python SDK: https://github.com/modelcontextprotocol/python-sdk
- Datadog MCP: https://docs.datadoghq.com/bits_ai/mcp_server/

---

MCP isn't more context. It's fresh context, when Claude needs it.
