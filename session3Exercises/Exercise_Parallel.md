# Exercise: Two lanes

Time: 22 minutes. Setup 4 min, both lanes running 13 min, decide 3 min, share 2 min.

---

## The one idea

In Session 2, Claude worked in parallel inside one task: subagents and workflows. Today it's you running more than one Claude, each on its own task, each in its own worktree.

A worktree is a second checkout of your repo, in its own folder, on its own branch, with the same git history. Two sessions in two worktrees can both edit files and never touch each other's work.

```bash
claude -w task      # creates .claude/worktrees/task/ on branch worktree-task
claude -w side      # second terminal, second checkout
```

In the desktop app: new session (Cmd/Ctrl+N), select **worktree** next to the branch name.

Your attention is the limit, not Claude. Two lanes today.

---

## Setup (4 min)

In your main checkout, outside Claude:

```bash
git status                                    # commit the plan and run skill if they aren't
echo ".claude/worktrees/" >> .gitignore
printf ".env\n.env.local\n" > .worktreeinclude    # gitignored files the worktree needs
```

New worktrees start from your default branch on the remote, so they won't see what you committed today. Make them start from your local work instead. Add this to `.claude/settings.local.json`:

```json
{ "worktree": { "baseRef": "head" } }
```

---

## Run both lanes (13 min)

**Terminal 1, lane `task`:**

```bash
claude -w task
```

```
/rename task
implement task 1 of @docs/superpowers/plans/[your plan].md. Install what the
worktree needs first. When it's done, run /verify on it and show me what you ran.
```

If superpowers offers to create a worktree, say no: you're already in one.

**Terminal 2, lane `side`:**

```bash
claude -w side
```

```
/rename side
```

Give it something small and unrelated from your backlog, that doesn't need your app running. Examples:

- add a test for a query nobody tests
- fix a runbook that's out of date
- clean up a warning in the CI config
- add comments to the migration nobody understands

While both run: answer whichever one asks you something. Don't watch them work.

---

## Parallel code is easy, parallel state isn't

Two worktrees don't share files. They do share everything else on your machine. If both lanes start your stack:

- Both want port 5432. Give lane 2 another port.
- `docker compose` uses the folder name for container names. Set `COMPOSE_PROJECT_NAME` per lane.
- Both migrate the same local database. One database or schema per lane.
- Never two lanes that apply infrastructure. Terraform state locks, and one of them loses.

That's why lane 2 today is something that doesn't need the app running.

---

## Decide (3 min)

For each lane, look at the evidence first and the diff second:

- `task`: did `/verify` show it working? Would you accept that proof?
- `side`: does the change do what you asked, and nothing else?

Then exit each session. Claude asks keep or remove. Keep if it's worth merging; you merge or open a PR from the branch later. `git worktree list` shows where they are.

---

## Share (2 min)

One line in the chat:

> I ran two lanes. What slowed me down was ___.

---

## If you finish early

1. A third lane that reviews `task` against the plan: start a plain `claude` in the main checkout and ask it to review branch `worktree-task` against the plan. It hasn't seen the reasoning that wrote the code.
2. `claude --worktree "#123"` starts a session on pull request 123's branch.
3. Fire and forget: `claude --bg "..."` starts a session in the background, `claude agents` shows them all. Research preview.
4. Off your laptop: `claude --cloud "..."` runs on Anthropic's machines and keeps going when you close the lid. Pull it back with `claude --teleport`. Plugins from your machine don't load there.

---

One lane is you typing. Two lanes is you deciding.
