# Exercise: Write a subagent

Time: 15 minutes. Build 7 min, run and watch 5 min, show it 3 min.

---

## What a subagent is

A separate Claude with its own context window. Your session hands it a task, it works in isolation, and only its answer comes back. The twenty files it read to get there never enter your context.

That's the point. Research, test runs, log analysis and reviews produce a lot of text you'll never look at again. Route them through a subagent and your main session stays small.

Three you'll meet come built in. Claude picks them without being asked.

| Subagent | What it's for | What it can do |
|---|---|---|
| Explore | Finding things in the codebase | Read-only. Skips CLAUDE.md to stay small. |
| Plan | Research during plan mode | Read-only |
| general-purpose | Anything that needs both reading and changing | Everything |

Custom ones are a markdown file in `.claude/agents/<name>.md` (the repo) or `~/.claude/agents/<name>.md` (you, everywhere). A header says what it can use, the body is its system prompt.

```markdown
---
name: units-reviewer
description: Reviews changes for unit mismatches (knots, nautical miles, tonnes). Use after edits in services/.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You review maritime calculation code for unit errors. For each finding,
give file, line, the two units in conflict, and a fix. Report nothing else.
```

Header fields you'll use: `tools` (or `disallowedTools`), `model` (`sonnet`, `opus`, `haiku`, `fable`, `inherit`), `skills` to preload one of your skills, `memory: project` to give it notes that persist, `isolation: worktree` to give it its own copy of the repo.

---

## Three things that changed recently

Read these before you start, or the exercise will feel broken.

`/agents` no longer opens a wizard. It prints a reminder to ask Claude or edit the file. So you create a subagent by asking Claude to write it, or by writing the file yourself.

Subagents run in the background by default. You ask for one, Claude kicks it off, and you get the prompt back. The result arrives as a notification a turn or two later. `/tasks` shows what's running and on which model. Ctrl+B sends a foreground task to the background.

There's a second kind called a fork. `/subtask <prompt>` starts a subagent that inherits your whole conversation, so it knows everything you've discussed, but its tool calls stay out of your context. Use it when the task needs your history. Use a normal subagent when it doesn't.

---

## What a subagent knows

It gets your CLAUDE.md files, the task Claude wrote for it, and any skills you preload. It does not get your conversation, the files you've read, or your auto memory. If it needs something you discussed, put it in the task or use a fork.

Explore and Plan skip CLAUDE.md too. That's why they're fast.

---

## Part 1: write one (7 min)

Pick a job in your repo that produces output you don't want to read. If nothing comes to mind:

- `test-runner`: runs the suite, returns only failures with the error text
- `units-reviewer`: the example above
- `security-reviewer`: read-only, checks a diff for the OWASP top ten
- `docs-writer`: reads code, writes to `docs/` only
- `migration-checker`: reads a migration, reports the risks, changes nothing

Ask Claude:

```
Write a subagent at .claude/agents/test-runner.md. It runs pytest and
returns only the failing tests with their error messages, nothing else.
It can run commands and read files but not edit them. Use Sonnet.
```

Open the file. Check three things:

1. The description says when to use it, not what it is. Claude reads that line to decide whether to delegate.
2. The tools match the job. A reviewer doesn't need `Edit`. A test runner doesn't need `Write`.
3. The body ends with what to return. "Report only failures" is the line that keeps your context clean. Without it you get the whole test log back.

---

## Part 2: run it and watch (5 min)

Delegate to it:

```
Use the test-runner subagent to run the suite and tell me what fails.
```

Or force it with an @-mention: type `@`, pick `test-runner (agent)` from the list. That guarantees this subagent runs; plain language lets Claude decide.

Then:

1. Run `/tasks`. Your subagent is in the list with its model.
2. Keep working while it runs. Ask Claude something unrelated. That's the background default.
3. When the result lands, run `/context`. The test output is not in your session. The summary is.
4. Ask a follow-up: "Continue that run and check only the weather tests." Claude resumes the same subagent with its history intact.

If Claude can't find the subagent, restart Claude Code. A running session doesn't notice a new `agents` folder.

---

## Show it (3 min)

Screen share with your sparring partner. Show the `/tasks` line and the `/context` output side by side. Then they ask:

1. "What comes back, and is that all I'd want?"
2. "Would you trust this to run while you're at lunch?" If not, which tool would you take away?

---

## Subagent, skill, or fork?

| You want | Use |
|---|---|
| The same instructions, reusable, in your context | Skill |
| A job done elsewhere, only the summary back | Subagent |
| A job that needs your conversation so far | Fork (`/subtask`) |
| Both: a subagent that follows your checklist | Subagent with `skills: [pr-review]` |

A skill with `context: fork` in its header is the last row from the other side. Same thing, started from the skill.

---

## If you finish early

1. Add `memory: project` to the header. The subagent gets a notes folder at `.claude/agent-memory/<name>/` that survives across sessions. Ask it to save what it learned about your test setup. Next run, it starts with that.
2. Add `isolation: worktree`. It gets its own copy of the repo. Try a refactor you'd be nervous about in your working tree.
3. Preload a skill: `skills: [units-check]`. The subagent starts with your checklist in its context instead of discovering it.
4. Try `/subtask draft tests for the change we just discussed`. Compare what it knows to what the normal subagent knew.
5. Ask Claude to research three modules in parallel with three subagents. Watch `/tasks` fill up.
6. Add a `hooks:` block with a `PreToolUse` on `Bash` that blocks anything with `rm`. The hook only runs while this subagent is active.

---

Use a subagent when you care about the answer, not the work. Everything else stays in the room.
