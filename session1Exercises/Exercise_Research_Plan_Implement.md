# Exercise: Research, plan, implement

You work alone on a task from your own codebase, in your own Claude Code session. Once, before you implement anything, you stop and show your plan to a sparring partner. That's peer review, not pair programming.

You will not finish the task. That's the design. The phases where your review changes the outcome are research and plan. Implementation is where you find out whether the plan was any good.

## Time: 50 minutes

| Time | Phase | What happens |
|---|---|---|
| 0:00 to 0:05 | Setup | Pick the task, open the repo, check your mode |
| 0:05 to 0:18 | Research | Claude explores in plan mode, you read critically |
| 0:18 to 0:35 | Plan and mini-spec | Claude writes the plan, you edit it in your editor |
| 0:35 to 0:40 | Sparring | Partner asks "can you check these criteria without asking Claude?" |
| 0:40 to 0:50 | Implement | Approve the plan, phase 1 only, `/diff` |

Rule of thumb: 70% of your time on research, plan and review. 30% on implementation. Today it'll be closer to 85/15 and that's fine.

---

## 1. Pick your task

Brought one from your backlog? Use it. Good tasks need you to understand existing code, are too big to hold in your head, and have a result you can check. Add an endpoint that follows existing patterns, fix a bug that spans a few files, write tests for a module that has none, refactor something the team calls "legacy".

No task ready? Pick one:

- Tests: a module with no tests. Understand it, plan a test strategy, write the first tests.
- Refactor: a file everyone avoids. Map its dependencies, plan a safe first step, take it.
- Onboarding docs: a part of the codebase that's hard to join. Have Claude research it and plan documentation that says something the code doesn't.

If you're done with the whole workflow in 20 minutes, the task was too small. Take one of the stretch options at the end.

---

## 2. Setup (5 min)

```bash
cd /path/to/your/repo
claude
```

Then check three things:

1. `/context` lists your CLAUDE.md under Memory files. If not, you're in the wrong directory.
2. Look at the status bar. On the Team plan a new session starts in auto mode (`⏵⏵ auto mode on`). That's fine for now; you'll switch to plan mode in the next step.
3. `claude --version` is 2.1.233 or newer. Older versions cycle modes differently and this sheet won't match. Run `claude update` if needed.

How you change mode:

- Terminal: `Shift+Tab` cycles Manual, Accept edits, Plan, then back to Auto. From auto mode the first press lands on Manual.
- Desktop app or VS Code: the mode selector next to the send button.
- Any interface: start a prompt with `/plan` to enter plan mode for that task.

---

## 3. Research (13 min)

Plan mode lets Claude read files and run commands but not edit anything. That's the point of research: understand first, change nothing.

Type `/plan` followed by your task. Ask for findings, not a plan:

```
/plan I need to <describe the task>.

Don't write a plan yet. First research the codebase and tell me:
- which files and functions are involved, with paths and line numbers
- what patterns the existing code follows that this change has to respect
- what already exists that we can reuse instead of adding
- which tests cover this area today
- risks and edge cases you see

Keep it to what I need to plan this change.
```

Claude will grep, read and summarise. Read the summary as if a new colleague wrote it. Errors here cascade into the plan.

Ways to steer:

- `@src/api/handlers.py` points Claude at a specific file.
- Correct it immediately: "No, that function is used for X, not Y. Look at `<file>` instead."
- Ask for specifics: "Which tests cover this? Which callers would break?"
- `/btw <question>` asks a side question without adding to the conversation. Handy for "which files did you read?"

Check the findings for three things:

- Correct. Does Claude's picture of the code match yours?
- Complete. Are the integration points there? The callers? The tests?
- Specific. File paths and line numbers, or "the auth module handles this"?

Gaps? Push back: "You don't mention `<X>`. How does `<specific thing>` work?"

Before you move on, ask yourself the question a colleague would: what's missing? A file you know is involved that the findings skip? A caller? A test? If you can name one, Claude can find it. Do that now, not in the plan.

If Claude jumps ahead and presents a plan with an approval prompt, choose "No, keep planning" and ask for the findings first.

---

## 4. Plan and mini-spec (17 min)

Still in plan mode. Now ask for the plan, with a spec on top. The spec forces the question the plan alone skips: what does done look like, and how would you check it?

```
Now write the plan. Use exactly this structure:

## Problem
What are we solving and why it matters.

## Constraints and out of scope
Patterns we must follow, contracts we can't break, what we're explicitly not doing.

## Acceptance criteria
- [ ] one concrete, testable thing per line
- [ ] each one checkable without asking you a question

## Definition of done
Which items from the definition of done in CLAUDE.md apply here, plus anything task-specific.

## Design notes
Files that change, patterns to follow, risks.

## Implementation plan
Phase 1, 2, 3. Each phase names the files and functions it touches and can be verified on its own.
```

Claude presents the plan and asks how to proceed. Don't approve yet.

Press `Ctrl+G`. The plan opens in your editor. This is your spec now. Read it and edit it directly:

- Order: do the phases make sense? Can each be verified on its own?
- Specific: could you execute phase 1 yourself from what's written?
- Consistent: does the plan use what the research found, or did Claude drift?
- Acceptance criteria: could you write a test for each one right now? If not, rewrite it until you could.
- Definition of done: does it map to the team's CLAUDE.md, or did Claude invent new criteria?

Save and close. If you'd rather have Claude fix something, choose "No, keep planning" and tell it what to change: "Phase 2 before phase 3, because <reason>. Criterion 3 isn't testable, make it concrete." (In the Desktop app, if `Ctrl+G` doesn't open an editor, review the plan in the session and use "No, keep planning" for every change.)

The plan is saved on disk by Claude Code and survives `/compact`, so you can compact freely from here if the context is getting full: `/compact focus on the plan and the acceptance criteria`.

---

## Sparring: plan review (5 min)

Stop. Share your screen with your partner and show them the plan in your editor.

They check three things:

- "Can you verify each acceptance criterion without asking Claude anything?" If not, it's too vague.
- "Could you hand phase 1 to Claude as one instruction?" If not, it's not concrete enough.
- "Does the definition of done come from your CLAUDE.md?" Or did the plan make up its own?

This is the review that saves you the debugging later. If your partner can't tell what done looks like, Claude can't either.

Two minutes each.

---

## 5. Implement (10 min)

Approve the plan. Choose "Yes, and use auto mode" if you want Claude to run without prompts, or "Yes, manually approve edits" if you want to see every diff before it lands. Both are fine. Pick on purpose.

Then:

```
Implement phase 1 only. Stop when it's done, show me what changed, and wait.
```

While it works:

- One phase at a time. Don't let it run through the whole plan.
- `/diff` after the phase. Read it.
- `Esc` stops Claude mid-action. `Esc Esc` opens the rewind menu if you want to go back to before the phase started.
- If something doesn't fit the plan, say so: "This isn't in the plan. What happened?"
- Claude executes. It doesn't make new design decisions. If it needs one, it should ask.

You'll get through phase 1, maybe start phase 2. That's the expected outcome.

Want the artifacts in the repo? Now that Claude can write files, ask it: "Save the research findings to `context/research-<task>.md` and the plan to `context/plan-<task>.md`."

---

## 6. Reflection (after the plenary, individual)

Write a few lines in `context/retro-<task>.md`:

- Where did research change what you would have built?
- Which acceptance criterion caught a problem, or would have?
- Where did Claude misread the codebase?
- Was the plan too vague, or too detailed?
- What belongs in your CLAUDE.md after this?

---


## If you finish early

1. Update CLAUDE.md with three concrete lines from what you just learned. These feed the wrap-up.
2. Rewind (`Esc Esc`, restore code and conversation to before phase 1) and implement phase 1 in Manual mode instead. Count the prompts. Now you know what auto mode is doing for you.
3. Run the research phase on a second task from your backlog. Is your research better now than 45 minutes ago?
4. Use `/plan` for an architecture review of a part of the codebase you're curious about. What does Claude find that you didn't know?
5. Re-read your spec against the implementation. What survived contact? What would you write differently?

---

Research and plan are where your review has the most effect. The mini-spec isn't paperwork; it's the fifteen minutes that replace hours of debugging. You're the architect, the spec is the blueprint, Claude is the craftsman.
