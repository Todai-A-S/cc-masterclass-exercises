# Mini exercise: one hook for your repo

Time: 8 minutes. Optional; run it if the MCP block finishes early, otherwise it's homework.

---

## The one idea

CLAUDE.md is a request. A hook is enforcement. A hook is a script Claude Code runs at a lifecycle event, every time, and Claude can't talk its way past it. The two events you'll use: `PostToolUse` (after Claude edits a file: run your formatter or linter) and `PreToolUse` (before a command runs: block the ones you never want).

You don't write hooks by hand. You ask Claude.

---

## Do this

In your own repo:

```
Write a hook in .claude/settings.json that runs [your formatter or linter]
on the file Claude just edited, after every Edit or Write. If the linter
reports problems, feed them back to Claude so it fixes them.
```

Swap in `black`, `ruff`, `prettier`, `dotnet format`, whatever the repo uses. Claude writes the JSON and, if needed, a small script in `.claude/hooks/`.

Then:

1. `/hooks` shows what's configured and where it came from.
2. Ask Claude to make a small edit that your linter would object to (a 130-character line, an unused import). Watch the hook fire and Claude fix it without being asked.
3. Commit `.claude/settings.json`. Now it fires for everyone on the repo.

---

## The line to remember

Hooks are guardrails for accidents, not for adversaries. Claude can also change files through shell commands, which a `PostToolUse` on `Edit` never sees. If a rule must never be broken, `permissions.deny` in the same settings file is the fence. The hook is the sign.

---

## If you want more

- A `Stop` hook that runs your tests and blocks Claude from finishing until they're green: ask Claude to write it. It must exit 0 when the `stop_hook_active` input field is true, or it loops.
- `PreToolUse` on `Bash` that blocks `git push --force` and `rm -rf`: the slide has it.
- Hooks can live in a skill's or a subagent's header too, active only while that runs.

Docs: https://code.claude.com/docs/en/hooks-guide
