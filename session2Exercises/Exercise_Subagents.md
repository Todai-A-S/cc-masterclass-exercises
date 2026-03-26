# Exercise: Create a Custom Subagent

**Time: ~7 minutes**

---

## What Are Subagents?

Subagents are specialized AI assistants that run in their own context window. Claude Code delegates tasks to them automatically, and they report back with results. Think of it as delegation: your main session stays clean while the subagent does the heavy lifting in isolation.

**Built-in subagents** (Claude uses these automatically):

| Subagent | Model | Access | When |
|---|---|---|---|
| **Explore** | Haiku (fast) | Read-only | Searching, code exploration |
| **Plan** | Inherited | Read-only | Architecture, planning |
| **General-purpose** | Inherited | Full access | Complex multi-step tasks |

**Custom subagents** live at `.claude/agents/<name>.md` - a markdown file with YAML frontmatter. You define what tools it gets, which model it runs on, its permission level, and its system prompt.

---

## When to Build a Custom Subagent

Build a subagent when:

- A task produces **verbose output** you don't need in your main context (test runs, log analysis)
- You want to **enforce constraints** - e.g. a reviewer that can only read, never edit
- You want a **specialist** with a focused system prompt for a specific domain
- You want to **control costs** by routing simple tasks to Haiku instead of Opus

---

## Exercise: Create Your Subagent

**Option A - Use `/agents` (recommended, 5 min):**

1. Run `/agents` in Claude Code
2. Select **Create new agent**
3. Choose **Project** (saves to `.claude/agents/`)
4. Select **Generate with Claude** and describe what you want:

```
A [describe role] agent that [describe what it does].
It should focus on [specific area] and only have access to [tools].
```

5. Pick the tools, model, and colour
6. Save and test it by asking Claude to use it

**Option B - Write it manually (5 min):**

Create a file at `.claude/agents/<name>.md`:

```yaml
---
name: code-reviewer
description: Reviews code for quality, security, and best practices. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a senior code reviewer. When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Review for: readability, error handling, security, test coverage
4. Organize feedback by priority: Critical > Warning > Suggestion
```

Then test: ask Claude to "use the code-reviewer agent to review recent changes."

**Subagent ideas for your repo:**

- `test-runner` - runs tests in isolation, returns only failures
- `security-scanner` - read-only agent that checks for vulnerabilities
- `documentation-writer` - generates docs from code, with write access only to docs/
- `migration-checker` - validates database migrations, read-only

---

## Share with your sidebuddy (1 min)

Show your sidebuddy your agent. Discuss: "Would this actually save you time?"

---

## Stretch Challenges

If you finish early, try adding advanced features to your subagent:

1. **Persistent memory** - Add `memory: project` to your frontmatter. The subagent gets a memory directory at `.claude/agent-memory/<name>/` that persists across conversations. It can build up knowledge over time (codebase patterns, recurring issues). Try asking it to "save what you learned to your memory" after a task.

2. **Worktree isolation** - Add `isolation: worktree` to run the subagent in a temporary git worktree. It gets its own copy of the repo to experiment in without affecting your working directory. Great for risky refactors or exploratory changes.

3. **Hooks inside your agent** - Add a `hooks` block to the frontmatter. For example, add a `PreToolUse` hook on `Bash` that validates commands before execution. The hook only runs while that specific subagent is active.

4. **Preload skills** - Add `skills: [skill-name]` to inject a skill's full content into the subagent's context at startup. The subagent gets domain knowledge without needing to discover it. Useful for making sure it follows your team's conventions.

5. **Background mode** - Add `background: true` to always run this subagent concurrently while you keep working. Claude will pre-approve permissions before launching it so it can run unattended.

Full reference for all frontmatter fields: https://code.claude.com/docs/en/sub-agents

---

> **Key insight**: Use subagents when you care about the result, not the journey. The verbose stuff (test output, search results, log analysis) stays in the subagent's context. You get back a clean summary - and your main session stays focused.
