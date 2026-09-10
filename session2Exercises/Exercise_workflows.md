# Exercise: Run a workflow

Time: 10 minutes. Start one 2 min, watch it 6 min, talk 2 min.

Works on all paid plans, Team included. If `ultracode` doesn't highlight in your prompt, check `/config` for "Dynamic workflows".

---

## What a workflow is

A script that runs many subagents. Claude writes the script for the task you describe, a runtime executes it in the background, and one result comes back to your session. The intermediate work lives in script variables, not in your context.

The difference from everything else today is who holds the plan:

| | Subagent | Skill | Workflow |
|---|---|---|---|
| What it is | A worker Claude spawns | Instructions Claude follows | A script the runtime executes |
| Who decides what runs next | Claude, turn by turn | Claude, following the prompt | The script |
| Where the results live | Your context window | Your context window | Script variables |
| Scale | A few tasks per turn | Same | Dozens to hundreds of agents per run |

A subagent is one worker. A workflow is a plan for thirty workers, with the loop, the branching and the cross-checking written down where you can read it and run it again.

Reach for one when the job is bigger than a handful of subagents, or when you want findings verified before you see them: audit every route handler, migrate 200 files, review every file in a PR and merge the findings into one ranked list.

---

## How to start one

Put `ultracode` in the prompt, or say "use a workflow". Claude writes the script and shows you the phases before anything runs.

```
ultracode: review every file under services/ for unit mismatches
(knots vs km/h, nautical miles vs km, tonnes vs kg). Verify each
finding with a second agent before reporting it. Return one ranked list.
```

The approval prompt has three options: run it, view the raw script, or no. Ctrl+G opens the script in your editor. In auto mode you see this prompt once and then not again.

`/deep-research <question>` is a workflow that ships with Claude Code. It fans out web searches, cross-checks the sources, and returns a cited report. Good for "what changed in library X between versions".

---

## Do it (10 min)

Before you start: `/config workflowSizeGuideline=small`. That tells Claude to aim for fewer than five agents. You want to see the mechanism, not spend the afternoon's budget.

Pick a task that reads, not writes. An audit, a review, a search. Save the migration for a day when you're not sharing a screen.

On the demo repo, the units prompt above works. On your own repo:

```
ultracode: review every file changed on this branch for correctness
issues. Have a second agent verify each finding. Merge into one summary.
```

Then:

1. Read the phases in the approval prompt. That's the plan. Say yes.
2. Run `/workflows`, select the run, press Enter. You see each phase, its agents, tokens and time. Drill into an agent to read its prompt and what it found.
3. Ask Claude something unrelated while it runs. Your session isn't blocked.
4. When the report lands, count what came back. One list, not thirty transcripts.
5. If it's a run you'd repeat, press `s` in `/workflows` to save it. It becomes `/name` in this repo. Put it in `.claude/workflows/` and the whole team has it.

Keys in the `/workflows` view: `p` pauses, `x` stops, `s` saves.

---

## Talk (2 min)

With your sparring partner:

1. What would you run this on tomorrow? Name the repo and the question.
2. Where's the line? At what size does a subagent stop being enough?

---

## A note on agent teams

You may have read about agent teams: several full Claude Code sessions with a lead, a shared task list and a mailbox. It exists, it's experimental, and it's off by default. Turn it on and Claude starts turning named subagents into teammates whether you asked or not. We're not doing it today. Workflows cover the same ground with a script you can read.

---

## If you finish early

1. Open the saved script. It's short JavaScript: `agent()` runs one, `pipeline()` runs one per item, `parallel()` runs a set at once. Ask Claude to add a phase.
2. Try `/deep-research` on a library your repo depends on: "what changed between the version we pin and latest".
3. Set `/effort ultracode` for the session. Now Claude decides on its own when a task deserves a workflow. Watch how often it does. Drop back with `/effort high`.

---

Subagents for a task. Workflows for a job. The script is the difference.
