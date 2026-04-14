# Exercise: Research → Plan → Implement with Mini-Spec

In this exercise, you work **individually** on a coding task from your own daily work using the **Research → Plan → Implement** workflow in Claude Code. At two points, you pause to spar with your neighbour — a structured exchange, not pair-programming.

The goal is to experience the difference between "just prompt and hope" and a structured approach where you maintain oversight and ownership of the code. **You will probably not finish implementing — that's by design. The value is in the research and plan phases, not in getting to done.**

## Time: approx. 50 minutes

| Time | Phase | Activity |
|---|---|---|
| 0:00–0:05 | Setup | Choose task, open repo in terminal, confirm CC is running |
| 0:05–0:18 | Research | Claude investigates codebase in `/plan` mode, you review output |
| 0:18–0:23 | **Sparring #1** | Show your neighbour your research — they ask: "What's missing?" |
| 0:23–0:38 | Plan + Mini-Spec | Claude writes plan with spec sections; you review and adjust |
| 0:38–0:43 | **Sparring #2** | Neighbour reviews your plan — "Are the acceptance criteria testable?" |
| 0:43–0:50 | Implement | Execute step by step with `/diff` after each step (may not finish) |

> **Mindset:** You will not finish. That's not a failure — it's a feature. Research and plan are where your review has the greatest impact. If you spend 70% of time on research + plan + review, and 30% on implementation, you're doing it right.

---

## 1. Choose Your Task

### Do you have a Bring-Your-Own-Task?

If you've prepared a task from your daily work, it's ideal. Good tasks:

- Require understanding existing code (not purely greenfield)
- Are complex enough that you can't hold the entire context in your head
- Are concrete enough that you can validate the result

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

## 3. Research Phase (13 min)

**Purpose:** Understand the relevant part of the codebase deeply enough to make a good plan. This is your chance to correct Claude's understanding before it cascades.

### How to do it:

Switch to Plan mode — Claude will analyse without changing anything:

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

Claude will use grep, glob, and file search to explore the codebase. **Read the output critically.** Errors in research cascade into your plan.

### Tips for good research:

- **Use `@`-mentions** to point Claude at specific files: `@src/api/handlers.py`
- **Correct misunderstandings immediately:** *"No, that function is used for X, not Y. Look at [file] instead."*
- **Ask for specifics:** *"What tests already cover this module?"*
- **Try `ultrathink`** if the codebase is complex: *"ultrathink — analyse the dependency graph for [module]"*

### Review the research document (CRITICAL)

Read through the research file and evaluate:

- **Correctness:** Is Claude's understanding right? Errors here cascade into the plan.
- **Completeness:** Are important integration points missing?
- **Specificity:** Does it reference concrete files, functions, and line numbers — or is it vague?

If there are gaps, ask Claude to dig deeper: *"You don't mention [X]. Please investigate how [specific question]."*

### Clear the context

When the research is satisfactory, compact before the next phase:

```
/compact focus on the research findings and task definition
```

---

## Sparring #1: Research Review (5 min)

**Pause.** Turn to your neighbour and show them your research document (`context/research-[task-name].md`).

Your neighbour's job is to ask: **"What's missing?"**

- Do they see files or dependencies the research didn't cover?
- Is the research specific enough — or does it feel like a generic summary?
- Would *they* feel confident planning from this document alone?

Take 2 minutes each. Then continue individually.

---

## 4. Plan + Mini-Spec Phase (15 min)

**Purpose:** Create a detailed, step-by-step implementation plan *and* a mini-spec that clarifies what done means *before* you code.

This is your highest-leverage review point. The mini-spec forces you to answer: *what does "done" actually look like, and can I test it?*

### How to do it:

Exit Plan mode if still active (Shift+Tab to cycle back to normal mode), then:

```
Read context/research-[task-name].md and create an implementation plan with a mini-spec.

Use this structure:

## Problem
What problem are we solving? Why does it matter?

## Constraints & Out-of-Scope
- What must we work within? (existing patterns, API contracts, performance requirements)
- What is explicitly out-of-scope?

## Acceptance Criteria
- [ ] [Concrete, testable thing 1]
- [ ] [Concrete, testable thing 2]
- [ ] [Concrete, testable thing 3]
- [ ] [Concrete, testable thing 4]

## Definition of Done
Reference the Definition of Done in our team CLAUDE.md. Which of those apply?
Add any task-specific DoD items.

## Design Notes
- Which files need to change?
- Which patterns should be followed?
- What risks do we see?

## Implementation Plan
- Phase 1: [what, with concrete files/functions]
- Phase 2: [what, with concrete files/functions]
- Phase 3: [what, with concrete files/functions]

Write the full spec + plan to context/plan-[task-name].md
```

### Review the plan + spec (CRITICAL — this is your highest-leverage review point)

Read through and evaluate:

**Plan section:**

- **Logical order:** Do the phases make sense? Can each be verified independently?
- **Specificity:** Are file changes concrete enough that you could execute them yourself?
- **Alignment:** Does the plan match the research findings?

**Mini-spec section:**

- **Acceptance Criteria:** Can you write a test for each one without asking Claude? If not, it's too vague.
- **Definition of Done:** Does it map to your team's CLAUDE.md DoD? Are there gaps?
- **Problem & Constraints:** Do they accurately capture the task, or did Claude drift?

Adjust directly: *"Phase 2 should come before phase 3, because [reason]. And acceptance criteria #3 isn't testable — make it concrete."*

### Clear context again

```
/compact focus on the implementation plan and acceptance criteria
```

---

## Sparring #2: Plan Review (5 min)

**Pause.** Show your neighbour your plan + spec (`context/plan-[task-name].md`).

Your neighbour evaluates (this is the most important review moment):

- **"Can you check the acceptance criteria without asking Claude questions?"** — If the answer is no, the criteria are too vague.
- **"Can you execute this plan mechanically?"** — Is each phase concrete enough to hand off to Claude as a single instruction?
- **"Does the DoD map back to the team CLAUDE.md?"** — Or did you invent new criteria?

**This is the moment where clarity prevents debugging later.** If your neighbour can't understand what done looks like, neither will Claude.

Take 2 minutes each. Then continue individually.

---

## 5. Implement Phase (7 min)

**Purpose:** Execute the plan step by step. You will probably not finish — that's the point.

### How to do it:

Make sure you're back in normal mode (not Plan mode). Then:

```
Read context/plan-[task-name].md and implement phase 1.

Implement only phase 1. Stop when it's done, show me the changes, and wait for my go-ahead.
```

### Key principles:

- **One step at a time.** Don't let Claude rush through the entire plan.
- **Verify after each step.** Use `/diff` to inspect changes. Run tests if you can.
- **Stay mechanical.** Claude executes the plan — it should not make new design decisions.
- **If something doesn't fit:** Stop and discuss. *"This doesn't match the plan. What's going on?"*

### Permission tip:

If Claude keeps asking for permission to edit files and run commands, press **Shift+Tab** to switch to Auto-Accept mode. You've reviewed the plan and spec — now let Claude execute.

### Expected outcome:

You will likely finish phase 1, maybe touch phase 2. You will **not** finish the entire task. **This is OK.** The learning is in the process, not the artifact.

---

## 6. Reflection (individual, after plenary)

After the plenary sharing, write down briefly in `context/learnings-[task-name].md`:

### What worked?
- Where did research add the most value?
- Where did the mini-spec catch problems?
- Which CC features saved you time?

### What didn't work?
- Where did Claude misunderstand the codebase?
- Where was the plan too vague or too detailed?
- Where was a criterion not testable?

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

Done early? Pick one — don't just start a new task:

1. **Iterate on CLAUDE.md** — Based on your experience: what should be added to the team's CLAUDE.md? Write 3-5 concrete suggestions.
2. **Try ultrathink** — Take the hardest part of your task. Run it with `ultrathink`. Compare quality with your normal plan.
3. **Research a second task** — Got another task from your backlog? Run just the research phase. Is your research better now than an hour ago?
4. **Deep-dive /plan mode** — Use `/plan` to do an architecture review of a part of your codebase you're curious about. What does Claude find that you didn't know?
5. **Spec retrospective** — Re-read your mini-spec. Did it survive contact with implementation? What would you change for next time?

---

## Remember

> **Research and plan are where your review has the greatest impact.** The mini-spec is not bureaucracy — it's an investment in clarity. A good spec taking 15 minutes saves hours of debugging. Most importantly: it enables Claude to work *with* your intentions, not *in spite of* them.
>
> You are the architect. The spec is your blueprint. Claude is the craftsman.
