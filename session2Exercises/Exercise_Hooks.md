# Exercise: Build a Hook

**Time: ~15 minutes**

---

## What Are Hooks?

Hooks are automated quality gates that run without intervention, like git hooks but for Claude Code. They execute before or after Claude uses a tool, letting you enforce safety, quality, and team patterns automatically.

You configure them in `.claude/settings.json` (project-level or user-level):

**Most common hook events:**
- `PreToolUse`: runs *before* Claude uses a tool (use to block dangerous actions)
- `PostToolUse`: runs *after* Claude uses a tool (use for linting, validation)
- `Stop`: runs when Claude finishes responding (final quality checks)
- `SessionStart`: runs when a session begins (setup, logging)
- `Notification`: triggered when Claude needs your attention

There are many more events (ConfigChange, FileChanged, SubagentStart/Stop, CwdChanged, etc.). Full list: https://code.claude.com/docs/en/hooks-guide

**You can match on specific tools**, e.g. only trigger on `Edit`, `Bash`, `Write`, not everything.

**Four hook types:**
- **`command`**: runs a shell script. Exit code 0 = allow, exit code 2 = block the action
- **`prompt`**: sends to Claude for LLM-based evaluation ("Does this follow our patterns?")
- **`agent`**: spins up a subagent for multi-turn verification
- **`http`**: POSTs event data to an HTTP endpoint

The power: hooks run silently and automatically. No human has to remember to check.

---

## When to Build a Hook

- **Prevent dangerous operations** - e.g., never delete production config files, never run `DROP TABLE` on prod
- **Automatic quality checks** - lint after every edit, catch TODO comments before commit
- **Enforce team patterns** - naming conventions, code style, test coverage - without relying on memory
- **Audit and logging** - track what Claude does for compliance or debugging
- **Block operations in protected directories** - e.g., no deletes in `/infrastructure/prod`

---

## Real-World Examples

| Scenario | Hook Type | Event | Approach |
|----------|-----------|-------|----------|
| Block `rm -rf` or `DROP TABLE` | `command` | `PreToolUse` on `Bash` | Exit code 2 if pattern matches |
| Auto-lint after every file change | `command` | `PostToolUse` on `Edit`/`Write` | Run linter, fail if errors |
| Scan for API keys before write | `prompt` | `PreToolUse` on `Write` | Ask Claude: "Does this contain secrets?" |
| Verify tests updated | `command` | `Stop` | Check git diff: if `src/` changed, `tests/` must too |
| Enforce conventional commits | `prompt` | `Stop` | Ask Claude: "Does commit message follow format?" |

---

## Exercise: Build Your Hook (10 minutes)

### Step 1: Identify your problem (2 min)

Think about your team's biggest "oops" moments or the quality check you always miss until code review.

**Brainstorm prompts:**
- "What's the most dangerous command someone could run in our repo?"
- "What quality check do we always forget until PR review?"
- "What pattern violation keeps sneaking in?"
- "What would we want blocked automatically?"

### Step 2: Choose an approach (1 min)

Pick one:

**Option A - Safety guard**
- `PreToolUse` hook on `Bash`
- Block dangerous commands (e.g., `rm -rf`, `DROP TABLE`, deployment commands in wrong directory)

**Option B - Quality gate**
- `PostToolUse` hook on `Edit`/`Write`
- Run a linter, check for TODO comments, validate file structure

**Option C - Session enforcer**
- `Stop` hook
- Verify tests were updated, commit message format, or specific file changes

### Step 3: Build and test (7 min)

Ask Claude to help:

```
Help me build a hook that [describe what it should do].
It should be a [PreToolUse/PostToolUse/Stop] hook.
I want it to trigger on the [Bash/Edit/Write] tool.
Configure it in .claude/settings.json with a 'command' type.
```

**Tips:**
- Start with a **`command` type** - just a shell script that exits 0 or 2
- Keep it simple: a single `grep` pattern or small script
- For `PreToolUse`, you're checking the tool arguments; for `PostToolUse`, you're checking the result
- Test it by *intentionally* triggering the condition - Claude should be blocked (or warned, depending on your setup)

**Example hook config in `.claude/settings.json`:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/safety-check.sh"
          }
        ]
      }
    ]
  }
}
```

The hook script receives JSON on stdin with `tool_name` and `tool_input`. Exit 0 to allow, exit 2 to block.

---

## Sharing (5 minutes)

Share your hook with your sidebuddy. Then a few groups share with the room - 30 seconds each.

**Discussion prompt:**
> "What's the most dangerous thing Claude has done - or *could* do - in your repo? What guard would matter most?"

This isn't about blame. It's about understanding real risks and what automation should prevent.

---

## Stretch Challenge (if time)

1. **Upgrade to `prompt` type** - instead of a shell pattern, let Claude evaluate: "Is this action safe? Does it follow our team conventions?"
2. **Chain two hooks** - a `PreToolUse` safety check *and* a `PostToolUse` quality check
3. **Build an audit hook** - log all `Bash` commands Claude runs to a file for compliance/debugging

---

## Bonus Challenge: Break the Hook

Your team has a safety hook that blocks dangerous file deletions. It's a `PreToolUse` command hook on `Bash` that runs this script:

```bash
#!/bin/bash
# .claude/hooks/no-delete.sh
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block dangerous delete patterns
if echo "$COMMAND" | grep -iE '(rm\s|rm$|rmdir|unlink\s|DELETE\s+FROM|DROP\s+TABLE)' > /dev/null; then
  echo "BLOCKED: File deletion commands are not allowed." >&2
  exit 2
fi

exit 0
```

Configured in `.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/no-delete.sh"
          }
        ]
      }
    ]
  }
}
```

**Your mission:** Set up this exact hook, then find a way to make Claude delete a test file *without* triggering the block. The file to delete: create a `target.txt` in your repo and get Claude to make it disappear.

Rules: you can't edit the hook script or settings.json. You have to get around the hook using only your prompt to Claude.

Hint: The hook is checking the *command string* for patterns. Think about what it's NOT checking.

