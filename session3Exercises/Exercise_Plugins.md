# Exercise: Make your own plugin

**Duration:** 18 min hands-on + a few minutes of sharing
**Format:** Solo or pair. Bring the best thing you built in Session 2 (a skill, a hook, a custom agent) — or build something new now.


## What is a plugin — the short version

A plugin is a **folder** — with your skill/hook/agent definitions inside.

The smallest useful plugin structure:

```
my-plugin/
└── .claude-plugin/
    └── plugin.json
```

With this `plugin.json`:

```json
{
  "name": "my-plugin",
  "description": "What this plugin does",
  "version": "1.0.0"
}
```

> **Note:** As of current Claude Code, `.claude-plugin/plugin.json` is technically optional — a folder with just a `skills/` directory will load. But you want a manifest for anything you'll share (it sets the name, namespace, and version), and it's required to list the plugin in a marketplace. Keep it.

You add content by placing folders *next to* `.claude-plugin/`:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/              ← your skills (recommended)
│   └── pr-review/
│       └── SKILL.md
├── agents/              ← your custom agents (one .md per agent)
│   └── code-reviewer.md
├── hooks/               ← your hooks
│   └── hooks.json
├── commands/            ← legacy flat-file skills (see note below)
└── .mcp.json            ← bundled MCP server configs
```

> **`skills/` vs `commands/`:** Both produce invocable `/name` skills. `commands/` is the older *flat Markdown file* form; `skills/` (a folder per skill with a `SKILL.md`) is what the docs recommend for new plugins. Use `skills/`.

**Important gotcha:** `commands/`, `agents/`, `skills/`, `hooks/` must live at the plugin **root**. They must **not** sit inside `.claude-plugin/`. Only `plugin.json` goes inside `.claude-plugin/`. This is the most common first-time mistake.

## Test a plugin locally — no distribution required

```bash
claude --plugin-dir ./my-plugin
```

That's the entire distribution story. The flag loads your plugin straight from the folder. You don't need a marketplace, a git repo, or an install command. For development and local testing, this is all you'll ever need.

> **Tip:** `--plugin-dir` also accepts a `.zip` archive of the plugin folder (`claude --plugin-dir ./my-plugin.zip`), and you can repeat the flag to load several plugins at once. To load a zip hosted at a URL (e.g. a CI build artifact), use `--plugin-url https://example.com/my-plugin.zip` instead.

When you run `claude --plugin-dir ./my-plugin`:

- The plugin manifest is read (if present)
- Skills become available as `/my-plugin:skill-name` (note the namespace prefix — automatic)
- Hooks become active
- Agents show up in `/agents`
- MCP servers defined in the plugin's `.mcp.json` get connected

If you change a file in the plugin folder while CC is running: `/reload-plugins` — changes are picked up without a restart (this reloads skills, agents, hooks, plugin MCP servers, and plugin LSP servers).

> **Even faster dev loop — skills-directory plugins.** If you don't want to pass `--plugin-dir` on every launch, run `claude plugin init my-tool`. It scaffolds `~/.claude/skills/my-tool/` with a manifest and a starter `SKILL.md`, and Claude Code auto-loads it every session as `my-tool@skills-dir` — no flag, no marketplace, no install step.

---

## Your task

Pack your best S2 work as a plugin and verify it loads correctly.

### Step 1: Scaffold (3 min)

```bash
mkdir -p my-plugin/.claude-plugin
cat > my-plugin/.claude-plugin/plugin.json << 'EOF'
{
  "name": "my-plugin",
  "description": "Best of my S2 work, packaged",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  }
}
EOF
```

The name you pick becomes the namespace prefix on all your skills. So if you call the plugin `my-plugin` and have a skill called `pr-review`, it's invoked as `/my-plugin:pr-review` after install. Pick something short and clear.

### Step 2: Copy your S2 work in (7 min)

**If you built a skill in S2:**
```bash
mkdir -p my-plugin/skills
cp -r ~/path/to/your/skill my-plugin/skills/
# Structure should be: my-plugin/skills/<skill-name>/SKILL.md
```

**If you built a hook in S2:**
```bash
mkdir -p my-plugin/hooks
# Copy the hook config from .claude/settings.json into:
# my-plugin/hooks/hooks.json
# (same JSON format as settings.json — copy the "hooks" object as-is)
```

Example `my-plugin/hooks/hooks.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/safety-check.sh" }
        ]
      }
    ]
  }
}
```

Note `${CLAUDE_PLUGIN_ROOT}` — that's the env var the plugin system sets so your hook script can be found regardless of where the plugin folder lives.

**If you built a custom agent in S2:**
```bash
mkdir -p my-plugin/agents
cp ~/.claude/agents/your-agent.md my-plugin/agents/
```

> **Heads up:** project and user `.claude/agents/` definitions override a same-named plugin agent. If your agent doesn't seem to come from the plugin, remove the original from `.claude/agents/`.

**If you wired up an MCP server today:**
```bash
# Copy the server config into .mcp.json at the plugin root
# (same format as the .mcp.json you edited earlier today)
```

### Step 3: Test locally (5 min)

```bash
# Quit your current CC session and restart with the plugin-dir flag:
claude --plugin-dir ./my-plugin

# Inside Claude Code:
/help         # skills from your plugin show up under namespace my-plugin:*
/agents       # your agents should be in the list
/mcp          # if you included an MCP server, it should be connected
```

Try invoking one of your skills: `/my-plugin:pr-review`. Try triggering a hook by doing the thing it watches for. Verify everything works *exactly as it did in S2* — just packaged now.

### Step 4: Iterate (3 min)

Change a file in the plugin. E.g. edit your SKILL.md to change an instruction. Inside CC:

```
/reload-plugins
```

Verify the change is picked up. This is the loop you'll use whenever you develop plugins from now on.

> **Sanity-check before you share:** run `claude plugin validate ./my-plugin` (or `/plugin validate ./my-plugin` inside CC). It checks the manifest schema *and* the frontmatter of every skill, agent, command, and hook — much more than a JSON linter catches.

---

## Debugging cheat sheet

| Symptom | Likely cause | Fix |
|---|---|---|
| Plugin doesn't load | Missing / misnamed `.claude-plugin/plugin.json` | Check path and filename — there's a leading dot on `.claude-plugin` |
| "Invalid plugin manifest" | JSON syntax or schema error | Run `claude plugin validate .` (or `/plugin validate .`) — it pinpoints the error |
| Skill doesn't show under `/help` | Wrong folder structure | `skills/` belongs at the plugin root, not inside `.claude-plugin/` |
| Hook doesn't trigger | `hooks.json` not picked up | Make sure the file is named exactly `hooks.json` and lives in `hooks/` |
| `$CLAUDE_PLUGIN_ROOT` not working | Env var not expanded in shell script | Use `${CLAUDE_PLUGIN_ROOT}` in `hooks.json`, not in the shell |
| Frontmatter silently ignored | Bad YAML in a SKILL.md / agent | `claude plugin validate .` flags `YAML frontmatter failed to parse` |
| Changes not picked up | Plugin cached | `/reload-plugins` or restart CC |

---

## If you want to share your plugin with a colleague

Four ways, in increasing formality. Pick the lightest one that solves your problem.

### 1. Send a zip
```bash
zip -r my-plugin.zip my-plugin/
```
Send it. The recipient runs `claude --plugin-dir ./my-plugin.zip` (the flag reads the zip directly — no unzip needed). High speed, zero infrastructure.

### 2. Commit to an internal git repo
Drop the plugin folder into a shared repo (your existing monorepo, or a new one). Colleagues clone and run `claude --plugin-dir ./path/to/plugin`. You get version history and PR flow for free.

### 3. Local marketplace folder
A marketplace is a catalog structure that lets you list multiple plugins in one place and install them via `/plugin install`. **GitHub is not required** — a marketplace can also be a local folder.

Minimum structure:

```
zeronorth-marketplace/
├── .claude-plugin/
│   └── marketplace.json     ← catalog of plugins
└── plugins/
    └── my-plugin/
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/...
```

`marketplace.json`:
```json
{
  "name": "zeronorth",
  "owner": {
    "name": "ZeroNorth Engineering",
    "email": "you@zeronorth.com"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./plugins/my-plugin",
      "description": "What my-plugin does"
    }
  ]
}
```

Install and test locally:
```bash
/plugin marketplace add ./zeronorth-marketplace
/plugin install my-plugin@zeronorth
```

> **Pick a non-reserved marketplace name.** `zeronorth` is fine. Names like `claude-community`, `claude-plugins-official`, `anthropic-*`, and other official-looking names are reserved and will be rejected.

### 4. Hosted marketplace (recommended if you want broad sharing)

When you're ready to move out of local folders: host the marketplace catalog in a git repo, and colleagues can add it with one command.

**For an internal ZeroNorth team setup the recommended form is a private GitHub repo:**

```bash
# First-time setup: someone pushes a marketplace with the structure above to
# e.g. github.com/zeronorth/claude-marketplace
# Rest of the team runs:

claude plugin marketplace add zeronorth/claude-marketplace
# (or from inside CC: /plugin marketplace add zeronorth/claude-marketplace)

# Then install specific plugins:
/plugin install pr-review@zeronorth
/plugin install safety-hooks@zeronorth
```

> **The `version` footgun — read this before you push updates.** Claude Code resolves a plugin's version from `plugin.json` → the marketplace entry → the git commit SHA, in that order. If you **set** `"version": "1.0.0"` and push new commits *without bumping that string*, existing users get **nothing** — CC sees the same version and keeps the cached copy. Two safe options:
> - **Bump `version` on every release**, or
> - **Omit `version` entirely** so each new commit (its SHA) counts as a new version — simplest for internal, actively-developed plugins.
>
> Also avoid setting `version` in *both* `plugin.json` and the marketplace entry; `plugin.json` silently wins.

**Other supported sources** (all work — pick what fits your infra):

| Source | Use case | Add command |
|---|---|---|
| **GitHub `owner/repo`** | Recommended for ZeroNorth | `/plugin marketplace add zeronorth/claude-marketplace` |
| **Git URL** | GitLab, Bitbucket, self-hosted | `/plugin marketplace add https://gitlab.zeronorth.com/team/claude-marketplace.git` |
| **Local path** | Quick test or offline | `/plugin marketplace add ./zeronorth-marketplace` |
| **Direct URL to marketplace.json** | Statically hosted, no git | `/plugin marketplace add https://internal.zeronorth.com/marketplace.json` |

> **Caveat on the direct-URL source:** it downloads only the `marketplace.json` file, so plugin entries that use relative `"./plugins/..."` sources won't resolve. For URL-hosted catalogs, point each plugin `source` at a `github` / `url` / `npm` source instead of a relative path.

**Private repos:** work out of the box if you already have `gh auth login` running. For background auto-updates (which run at startup, before credential helpers), set `GITHUB_TOKEN` (or `GH_TOKEN`) in your shell. GitLab uses `GITLAB_TOKEN`/`GL_TOKEN`; Bitbucket uses `BITBUCKET_TOKEN`.

**Auto-installer for the whole team:** if you want the marketplace to be offered automatically when someone trusts a ZeroNorth repo, drop this into `.claude/settings.json` in the repo:

```json
{
  "extraKnownMarketplaces": {
    "zeronorth": {
      "source": {
        "source": "github",
        "repo": "zeronorth/claude-marketplace"
      }
    }
  },
  "enabledPlugins": {
    "pr-review@zeronorth": true
  }
}
```

Full docs: https://code.claude.com/docs/en/plugin-marketplaces

### Which path should I pick?

- **Just one colleague asking?** Zip or git-clone of the folder.
- **Whole squad on the same setup?** Local marketplace folder in your squad repo, no central thing to maintain.
- **Whole engineering org?** Private GitHub repo + auto-install via `extraKnownMarketplaces` in your standard repo template.

Today the point is that you understand the *anatomy* and can test locally. Tomorrow you pick the distribution form that fits your team.

---

## Stretch goals (if you finish early)

1. **Bundle several things.** Put a skill, a hook, and a custom agent into the same plugin. Verify they all load.
2. **Add an `.mcp.json` to the plugin.** So when someone installs your plugin, they automatically get an MCP server wired up.
3. **Document it.** Write a `README.md` in the plugin root with install instructions and examples. This is the difference between "this is a plugin" and "this is a plugin I actually share with colleagues."
4. **Validate it.** Run `claude plugin validate ./my-plugin` and get a clean pass — this is what the community-marketplace review pipeline runs on every submission.

---

## Resources

- **Plugins guide:** https://code.claude.com/docs/en/plugins
- **Plugins reference (full schema):** https://code.claude.com/docs/en/plugins-reference
- **Plugin marketplaces (if you want distribution later):** https://code.claude.com/docs/en/plugin-marketplaces
- **Discover & install existing plugins:** https://code.claude.com/docs/en/discover-plugins
