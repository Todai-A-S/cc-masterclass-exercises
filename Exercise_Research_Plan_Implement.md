# Exercise: Research → Plan → Implement

In this exercise, you work **individually** on a coding task from your own daily work using the **Research → Plan → Implement** workflow in Claude Code. At two points, you pause to spar with your neighbour — a structured exchange, not pair-programming.

The goal is to experience the difference between "just prompt and hope" and a structured approach where you maintain oversight and ownership of the code.

## Time: approx. 50 minutes

| Time | Phase | Activity |
|---|---|---|
| 0:00–0:05 | Setup | Choose task, open repo in terminal, confirm CC is running |
| 0:05–0:20 | Research | Claude investigates codebase in `/plan` mode, you review output |
| 0:20–0:25 | **Sparring #1** | Show your neighbour your research — they ask: "What's missing?" |
| 0:25–0:35 | Plan | Claude writes plan, you review and adjust |
| 0:35–0:40 | **Sparring #2** | Neighbour reviews your plan — "Are the acceptance criteria testable?" |
| 0:40–0:50 | Implement | Execute step by step with `/diff` after each step |

> **Note:** You will probably not finish implementing everything. That's the point. Research and plan are where your review has the greatest impact — not in implementation.

---

## 1. Choose Your Task

### Do you have a Bring-Your-Own-Task?

If you've prepared a task from your daily work, it's ideal. Good tasks have these characteristics:

- Requires understanding existing code (not purely greenfield)
- Complex enough that you can't hold the entire context in your head
- Concrete enough that you can validate the result

Examples: add a new API endpoint, fix a bug spanning multiple files, refactor a component, write tests for an untested module, extend existing functionality.

### No prepared task? Use one of these:

**Option A — Test Coverage:** Pick a module in your codebase that lacks tests. Task: understand the module, plan a test strategy, implement tests.

**Option B — Safe Refactoring:** Find a file or component that the team knows is "legacy" or messy. Task: understand dependencies, plan a safe refactoring, implement one step.

**Option C — Documentation with Substance:** Pick a part of the codebase that's hard to onboard to. Task: let Claude research and understand the code, plan documentation structure, generate meaningful documentation.

---

## 2. Setup (5 min)

Open your repo in the terminal and start Claude Code:

```bash
cd /path/to/your/repo
claude
```

Confirm that Claude Code is running and has access to your codebase. Check with `/context` that you have a fresh context window.

**Quick checklist before you start:**
- [ ] Claude Code is running in your repo
- [ ] You know which task you're working on
- [ ] You have the CLAUDE.md we built together loaded (confirm with `/memory`)

---

## 3. Research Phase (15 min)

**Purpose:** Understand the relevant part of the codebase deeply enough to make a good plan.

### How to do it:

Start by switching to Plan mode — Claude will analyse without changing anything:

```
/plan
```

Then describe your task and ask for research:

```
I need to [describe the task].

Please investigate the codebase and help me understand:
- Which files and functions are relevant?
- What patterns are used in the existing code?
- What dependencies and integration points should I be aware of?
- Are there edge cases or risks?

Write your findings to a file: context/research-[task-name].md
```

Claude will use grep, glob, and file search to explore the codebase. Let it work — but **read the output critically**.

### Tips for good research:

- **Use `@`-mentions** to point Claude at specific files: `@src/api/handlers.py`
- **Correct misunderstandings immediately:** *"No, that function is used for X, not Y. Look at [file] instead."*
- **Ask for specifics:** *"What tests already cover this module?"*
- **Try `ultrathink`** if the codebase is complex: *"ultrathink — analyse the dependency graph for [module]"*

### Review the research document (IMPORTANT)

Read through the research file and evaluate:

- **Correctness:** Is Claude's understanding right? Errors here cascade into the plan.
- **Completeness:** Are important integration points missing?
- **Specificity:** Does it reference concrete files, functions, and line numbers — or is it vague?

If there are gaps, ask Claude to dig deeper: *"You don't mention [X]. Please investigate how [specific question]."*

### Clear the context

When the research is satisfactory, compact before the next phase. You can guide what to preserve:

```
/compact focus on the research findings and task definition
```

---

## Sparring #1: Research Review (5 min)

**Pause.** Turn to your neighbour and show them your research document (`context/research-[task-name].md`).

Your neighbour's job is to ask: **"What's missing?"**

- Do they see files or dependencies the research didn't cover?
- Is the research specific enough — or does it feel like a generic summary?
- Would *you* feel confident planning from this document alone?

Take 2 minutes each. Then continue individually.

---

## 4. Plan Phase (10 min)

**Purpose:** Create a detailed, step-by-step implementation plan you can execute mechanically.

### How to do it:

Exit Plan mode if still active (Shift+Tab to cycle back to normal mode), then:

```
Read context/research-[task-name].md and create an implementation plan.

The plan should include:
- Phases in logical order (3-5 phases)
- For each phase: concrete file changes, test strategy, verification steps
- Risks and what could go wrong
- Definition of Done for the entire task

Write the plan to context/plan-[task-name].md
```

### Review the plan (IMPORTANT — this is your highest-leverage review point)

Read through the plan and evaluate:

- **Logical order:** Do the phases make sense? Can each be verified independently?
- **Specificity:** Are file changes concrete enough that you could make them yourself?
- **Test strategy:** Is it realistic and aligned with your conventions?
- **Alignment:** Does the plan match the research findings?

Adjust the plan directly: *"Phase 2 should come before phase 3, because [reason]. Update the plan."*

### Clear context again

```
/compact focus on the implementation plan
```

---

## Sparring #2: Plan Review (5 min)

**Pause.** Show your neighbour your plan (`context/plan-[task-name].md`).

Your neighbour evaluates:

- **"Are the acceptance criteria testable?"** — Could you write a test that verifies each one?
- **"Can you execute this plan?"** — Is each step concrete enough to hand off to Claude as a single instruction?
- **"Does it match the research?"** — Or did Claude drift from what it found?

This is the most valuable review moment. If the plan is solid, implementation is mechanical. If the plan is vague, you'll debug instead of build.

Take 2 minutes each. Then continue individually.

---

## 5. Implement Phase (10 min)

**Purpose:** Execute the plan step by step with validation after each step.

### How to do it:

Make sure you're back in normal mode (not Plan mode). Then:

```
Read context/plan-[task-name].md and implement phase 1.

Implement only phase 1. Stop when it's done, show me the changes, and wait for my go-ahead.
```

### Key principles:

- **One step at a time.** Don't let Claude rush through the entire plan.
- **Verify after each step.** Use `/diff` to inspect changes. Run tests.
- **Stay mechanical.** Claude executes the plan — it should not make new design decisions.
- **If something doesn't fit:** Stop and discuss. *"This doesn't match the plan. What's going on?"*

### Permission tip:

If Claude keeps asking for permission to edit files and run commands, press **Shift+Tab** to switch to Auto-Accept mode. You've reviewed the plan — now let Claude execute.

### If the context fills up:

Run `/compact`, start a new prompt, and reference the plan:

```
Continue implementation from context/plan-[task-name].md.
Phases 1 and 2 are done. Implement phase 3.
```

---

## 6. Reflection (done individually after plenary)

After the plenary sharing, write down briefly — ideally in a file `context/learnings-[task-name].md`:

### What worked?
- Where did research add the most value?
- Where did plan review catch problems?
- What CC features saved you time?

### What didn't work?
- Where did Claude misunderstand the codebase?
- Where was the plan too vague or too detailed?
- Where did you take a shortcut that cost time?

### Context management
- Did `/compact` between phases help?
- Did you use `/plan` mode for research? How did it compare to normal mode?

### Key takeaway
- What would you do differently next time?
- What should go into your CLAUDE.md based on this experience?

---

## Sharing in Plenary

Prepare to share with the group:

1. **Best prompt** — the one that delivered the most value
2. **Biggest trap** — the mistake that cost the most time
3. **What surprised you** — something you didn't expect

---

## Stretch Challenges (for early finishers)

Done with the main exercise? Pick one:

1. **Iterate on CLAUDE.md** — Based on your experience: what should be added to the team's CLAUDE.md? Write 3-5 concrete suggestions.
2. **Try ultrathink** — Take the hardest part of your task. Run it with `ultrathink`. Compare quality with your normal plan.
3. **Research a second task** — Got another task from your backlog? Run just the research phase. Is your research better now than 30 minutes ago?
4. **Deep-dive /plan mode** — Use `/plan` to do an architecture review of a part of your codebase you're curious about. What does Claude find that you didn't know?
5. **Write a mini-spec** — Write Problem → Constraints → Acceptance Criteria for your task *after* implementing it. What would you have done differently with the spec upfront? *(Preview of Session 2.)*

---

## Remember

> This exercise is not about writing the most code. It's about experiencing **where your review has the greatest impact** — and that's in the research and plan phases, not in implementation. If you spend 80% of the time on research, plan, and review — and only 20% executing — you're doing it right.
