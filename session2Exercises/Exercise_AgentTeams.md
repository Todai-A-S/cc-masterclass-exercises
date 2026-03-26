# Exercise: Run an Agent Team

**Time: ~10 minutes**

---

## What Are Agent Teams?

Agent Teams are multiple Claude Code sessions coordinating as peers. Unlike subagents (where the main session delegates and gets results back), Agent Teams are peer-to-peer: each teammate has its own context window, works independently, and communicates directly with other teammates.

**The architecture:**

| Component | What it does |
|---|---|
| **Team lead** | Your main Claude Code session. Creates the team, assigns tasks, synthesizes results |
| **Teammates** | Separate Claude Code instances, each working on their assigned part |
| **Task list** | Shared list of work items. Teammates claim tasks and mark them complete. Tasks can have dependencies |
| **Mailbox** | Direct messaging between any agents. Teammates can message each other, not just the lead |

**How it differs from subagents:**

| | Subagents | Agent Teams |
|---|---|---|
| **Context** | Results return to caller's context | Each teammate fully independent |
| **Communication** | Report back to main agent only | Teammates message each other directly |
| **Coordination** | Main agent manages all work | Shared task list with self-coordination |
| **Best for** | Focused tasks where only the result matters | Complex work requiring discussion and collaboration |
| **Token cost** | Lower (results summarized back) | Higher (each teammate is a separate Claude instance) |

**Sweet spot**: 3-5 teammates, 5-6 tasks each. Agent teams use significantly more tokens than a single session, so use them when parallel exploration genuinely adds value.

---

## Enable Agent Teams

Agent Teams are experimental and disabled by default. Enable them in `.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Requires Claude Code v2.1.32 or later.

---

## Exercise: Try Running an Agent Team (7 min)

Pick a task from the list below (or invent your own) and ask Claude to create an agent team for it. The goal is to see how the team coordinates, not to produce a perfect result.

**Example tasks to choose from:**

- **Parallel code review**: "Create an agent team with 3 teammates to review [file/module]. One focused on security, one on performance, one on test coverage."
- **Bug investigation**: "Create an agent team to investigate [bug/issue]. Have 3 teammates test competing hypotheses and debate each other's findings."
- **Full-stack feature exploration**: "Create an agent team to explore how we'd add [feature]. One teammate on backend, one on frontend, one on testing."
- **Documentation sprint**: "Create an agent team with 3 teammates to document [module]. One on API docs, one on architecture, one on getting-started guide."

**Start it like this:**

```
Create an agent team with 3 teammates to [describe task].
One focused on [area 1], one on [area 2], one on [area 3].
```

Claude creates the team, spawns teammates, distributes tasks, and coordinates work based on your prompt.

---

## How to Inspect What's Happening

Once the team is running, you can observe and interact:

**Navigate between teammates:**
- Press **Shift+Down** to cycle through teammates. After the last teammate, it wraps back to the lead
- Press **Enter** to view a teammate's session in detail
- Press **Escape** to interrupt a teammate's current turn
- Press **Ctrl+T** to toggle the task list view

**Talk to teammates directly:**
- Cycle to any teammate with Shift+Down, then type to send them a message
- Give additional instructions, ask follow-up questions, or redirect their approach

**Watch the task list:**
- The lead's terminal shows all teammates and what they're working on
- Tasks move through states: pending, in progress, completed
- Tasks can depend on other tasks (blocked until dependencies complete)
- Teammates self-claim the next available task when they finish one

**Split pane mode** (if you have tmux or iTerm2):
- Each teammate gets its own pane so you can see everyone's output at once
- Set `"teammateMode": "tmux"` in settings.json, or pass `--teammate-mode tmux` as a flag
- Click into any pane to interact with that teammate directly

---

## Share (3 min)

If anyone got a team running, share what you saw:
- How did the teammates coordinate?
- Did they communicate with each other?
- What did the task list look like?
- Was it worth the extra tokens, or would subagents have been enough?

**Discussion prompt:**
> "When would you actually use this on your team? What task is complex enough to justify 3-5 parallel Claude sessions?"

---

## Good to Know

- The team lead makes decisions autonomously. You can influence it: "Only approve plans that include test coverage" or "Wait for all teammates to finish before synthesizing."
- You can require teammates to plan before implementing: "Require plan approval before they make any changes."
- Teammates load the same project context as a regular session (CLAUDE.md, MCP servers, skills) but don't inherit the lead's conversation history.
- Clean up when done: tell the lead to "clean up the team." Shut down teammates first.
- **One team per session.** Clean up the current team before starting a new one.

Full documentation: https://code.claude.com/docs/en/agent-teams
