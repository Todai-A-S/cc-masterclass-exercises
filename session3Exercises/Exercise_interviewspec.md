# Exercise: Let Claude interview you

Time: 12 minutes. Interview 6 min, read the spec 3 min, sparring 3 min.

---

## Before you start

Pick a real task from your backlog that is bigger than a bug fix. Something you'd normally spend an hour thinking about before you touched code: a new endpoint with two consumers, a change that crosses a service boundary, a migration. It has to be yours and it has to be real; the spec you write today is the one you'll implement in the next exercise.

Open a fresh Claude session in the repo where the task lives. Not plan mode: Claude has to write `SPEC.md` at the end, and plan mode blocks writes.

---

## Why this is an exercise

In Session 1 you wrote a mini-spec by hand. It worked, and it took the whole planning slot. This is the same output with the roles reversed: Claude asks, you answer. Claude is good at finding the questions you'd have skipped (what happens on retry, who else reads this table, what does "done" look like for the second consumer). You're good at answering them. Each does the part it's good at.

The best practices guide calls this "let Claude interview you". It's the one technique from that page that senior developers tend to adopt on the spot, because for once they're the ones with the answers.

---

## Part 1: the interview (6 min)

Paste this, with your task in the brackets:

```
I want to build [one-sentence description of the task]. Interview me in
detail using the AskUserQuestion tool.

Ask about technical implementation, UI/UX, edge cases, concerns, and
tradeoffs. Don't ask obvious questions; dig into the hard parts I might
not have considered.

Keep interviewing until we've covered everything, then write a complete
spec to SPEC.md.
```

Claude asks one question at a time, often with options to pick from. Answer honestly, including "I don't know, find out from the code" when that's true. Say "skip" if a question doesn't apply. If it's still asking at minute five, say "that's enough, write the spec".

Two things to notice while it runs:

- The question that made you stop and think. That's the one you would have discovered during implementation, at the worst possible time.
- The question you couldn't answer. That's the research the plan needs.

---

## Part 2: read the spec (3 min)

Open `SPEC.md`. A spec that will survive implementation has four things. Check for each:

| Check | Why it matters |
|---|---|
| It names the files and interfaces involved | Claude implements what's named. "Update the API" becomes ten files. |
| It says what is out of scope | Without this, Claude does the adjacent thing too. |
| It ends with an end-to-end verification step | This is what Claude runs to know it's done. No step, no "done". |
| Every requirement is something you could check without asking Claude | The Session 1 rule: if you can't verify it, it isn't a requirement, it's a wish. |

Fix what's missing by asking, not editing: "add an out-of-scope section: we're not touching the billing side". Claude rewrites the file.

---

## Sparring (3 min)

Screen share with your partner. They read your spec, not your conversation, and answer one question:

> "Could you implement this without asking me anything?"

Every "no" is a line the spec still needs. Swap.

---

## What happens next

Don't implement in this session. The spec is done; the conversation that produced it is forty questions of context you don't need any more. In the next exercise you'll start a fresh session and hand it the spec: `/plan implement @SPEC.md, phase 1 only`. Clean context, written spec, no memory of the interview. That's the pattern.

---

## If you finish early

1. Ask: "what in this spec are you least sure about?" Claude's answer is usually the thing to research first.
2. Ask for the acceptance criteria as a test file skeleton. Empty tests with names are a spec Claude can run.
3. Try the interview on a task you already finished last week. Count how many of its questions you actually handled.

---

Time spent making the spec precise pays off more than time spent watching the implementation.
