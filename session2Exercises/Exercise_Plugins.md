# Exercise: Explore & Understand Plugins

**Duration:** ~15 minutes (optional, if time allows)

---

## What Are Plugins?

Plugins are the distribution layer for Claude Code customizations. They solve a fundamental problem: how do you share skills, hooks, agents, and configurations across your team without copying-pasting files or writing installation docs?

A plugin bundles everything together:
- **Skills** - reusable workflow automations
- **Hooks** - automated guardrails and triggers
- **Agents** - custom Claude personas
- **MCP server configs** - integrations with external tools

Instead of each developer configuring things manually, you install once and everyone gets the same setup. Think of it like npm packages, but for Claude Code workflows.

**Install:** `/plugin install name@marketplace` or from a local path

---

## Plugin Anatomy

Here's what a plugin structure looks like:

```
.claude-plugin/
├── plugin.json          # Manifest: name, version, description, permissions
├── skills/
│   └── my-skill/
│       └── SKILL.md     # Same format as regular skills
├── agents/
│   └── my-agent.md      # Same format as custom agents
├── hooks/
│   └── hooks.json       # Hook configurations
└── .mcp.json            # MCP server configs (if any)
```

The **plugin.json** file is the key:

```json
{
  "name": "zeronorth-productivity",
  "version": "1.0.0",
  "description": "Shared skills and automations for the ZeroNorth team",
  "author": "Your Name",
  "license": "MIT",
  "skills": ["code-review", "meeting-notes"],
  "hooks": ["auto-format-output"],
  "agents": ["code-assistant"],
  "permissions": ["file-system", "web"],
  "mcp-servers": ["slack", "github"]
}
```

---

## Exercise Part 1: Explore Existing Plugins (7 min)

Browse the plugin ecosystem to see what's out there.

**Option A: Command line**
```
/plugins search [keyword]
```
Examples: `code-review`, `documentation`, `testing`, `api-integration`

**Option B: Web**
Visit https://code.claude.com/docs/en/discover-plugins to browse community plugins.

**Your task:**
1. Find 2–3 plugins that could be useful for your team or workflow
2. For each plugin, note:
   - **What does it do?**
   - **Would you install it?** (yes/no)
   - **What concerns would you have?** (security, dependency bloat, maintenance)

**Discussion with sidebuddy:**
- Which plugins would you trust to install on your dev machine?
- Which wouldn't you install, and why?
- What would a plugin need to include for you to feel confident installing it at work?

---

## Exercise Part 2: Design a Plugin (8 min)

Think about the work you've done today - the skills you built, the hooks you configured. Imagine packaging them as a plugin for your team.

**Your task:**

Pick one of two approaches:

### Approach 1: Write a Plugin Manifest
Create a **concept** plugin.json for your team. Don't worry about it being functional - just think through the structure:

```json
{
  "name": "zeronorth-[your-name]",
  "version": "1.0.0",
  "description": "What this plugin does for the team",
  "author": "Your Name",
  "skills": ["list the skills you'd include"],
  "hooks": ["list the hooks you'd include"],
  "agents": ["list any agents"],
  "permissions": ["what access does it need?"]
}
```

Questions to ask yourself:
- What would the plugin be *called*?
- What problem does it solve for your team?
- Would you trust your teammates to install this?
- What documentation would it need?

### Approach 2: Package Your Work
Ask Claude to help you convert your earlier work into a plugin structure:

```
Help me create a plugin that bundles:
- The skill at .claude/skills/[name]
- The hook I configured earlier
- Any agents I set up

Create the plugin structure at .claude-plugin/ with a proper plugin.json manifest.
```

---

## The Distribution Angle

Here's the real win: Plugins turn personal experiments into team infrastructure.

Right now, if you've built a useful skill or hook, sharing it means:
- Slack message with a CLAUDE.md file
- Teammates manually copying it into their `.claude/` directory
- Someone asks a week later: "Wait, do I have the latest version?"
- That Slack message gets lost

With plugins:
```
/plugin install zeronorth-codereview@marketplace
```

Everyone gets the same version. Updates roll out automatically. Conventions are built in. Onboarding is instant.

The team that builds good plugins wins. Consistent quality. Shared conventions. Easy onboarding.

---

## Resources

- **Creating Plugins:** https://code.claude.com/docs/en/plugins
- **Discovering Plugins:** https://code.claude.com/docs/en/discover-plugins
- **Plugin Marketplaces:** Community-curated collections
- **Best Practices:** Documentation standards, permission scoping, versioning

---

## Key Takeaway

Plugins are where personal experiments become team infrastructure. The skills and hooks you built today? They're one `plugin.json` away from being shared with everyone.
