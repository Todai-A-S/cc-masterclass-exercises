# Exercise: Writer and Reviewer in parallel

Time: 25 minutes. Setup 3 min, write 10 min, review 6 min, fix 4 min, wrap up 2 min.

---

## What a worktree is

A second checkout of the same repo, in its own folder, on its own branch, sharing the same git history. Two Claude sessions in two worktrees can both edit files and never touch each other's work.

```bash
claude --worktree writer
```

That creates `.claude/worktrees/writer/` on a branch called `worktree-writer`, and starts Claude inside it. Run it again with another name in another terminal and you have two isolated sessions. Omit the name and Claude invents one. The desktop app has the same thing as a checkbox when you start a session.

Three things to know before you start:

- **It branches from your default branch, not from your current work.** Uncommitted changes in your main checkout aren't in the worktree. If you need your current branch as the base, set `"worktree": { "baseRef": "head" }` in `.claude/settings.json` first.
- **It's a fresh checkout.** Gitignored files (`.env`, `node_modules`, a venv) aren't there. Put the small ones in a `.worktreeinclude` file (same syntax as `.gitignore`) and they're copied in every time. Dependencies: ask Claude to install them, or run your setup in the worktree folder.
- **On exit, Claude asks.** If the worktree has commits or changes, you choose keep or remove. Removing deletes the branch and everything on it.

Add `.claude/worktrees/` to `.gitignore` so the folders don't show up as untracked.

---

## Why two sessions

Session 2 was about protecting one context window. This is about using two. A reviewer that runs in a fresh session has never seen the reasoning that produced the code. It sees the diff and the spec, and it isn't attached to either. That's a better review than the session that wrote the code can give itself, and it's the docs' recommended pattern: one Claude writes, another reviews, you carry the findings between them.

Rule for this exercise: the reviewer only reports gaps that affect correctness or the stated requirements. A reviewer asked to find problems will always find some. Style goes in a separate pile you can ignore.

---

## Setup (3 min)

You need the `SPEC.md` from the interview exercise, committed or copied somewhere both sessions can read it. Simplest: commit it on your current branch, or copy it to the repo root of the worktree once it exists.

```bash
echo ".claude/worktrees/" >> .gitignore
printf ".env\n.env.local\n" > .worktreeinclude    # if you have those
```

Terminal 1:

```bash
claude --worktree writer
/rename writer
```

Terminal 2, from the main checkout (not inside the worktree):

```bash
claude
/rename reviewer
```

If the worktree needs dependencies, tell the writer session to install them first. Budget two minutes for that; if it takes longer, review the plan instead of the code (see the fallback below).

---

## Part 1: write (10 min)

In the **writer** session:

```
/plan implement @SPEC.md, phase 1 only
```

Read the plan, press Ctrl+G if you want to edit it, approve it. Let Claude implement. When it's done, have it commit:

```
run the tests, then commit with a message that references SPEC.md
```

It won't finish the whole spec in ten minutes. Phase 1 is enough to review.

---

## Part 2: review (6 min)

In the **reviewer** session. Replace `worktree-writer` if you named the worktree something else.

```
Review the changes on branch worktree-writer against @SPEC.md. Run
git diff main...worktree-writer to see them. Check that every phase 1
requirement is implemented, that the listed edge cases have tests, and
that nothing outside the task's scope changed. Report gaps that affect
correctness or the requirements. Put style comments in a separate list
at the end; I'll probably ignore them.
```

If your default branch isn't `main`, change it in the prompt.

While the reviewer works, look at what the writer did. You're the third reviewer.

---

## Part 3: fix (4 min)

Copy the reviewer's gaps into the **writer** session:

```
Here's the review feedback: [paste]. Address the correctness gaps, run the tests, and commit.
```

Then back to the reviewer: "re-check the diff against your previous findings". The loop closes when the reviewer has nothing left in the first list.

---

## Wrap up (2 min)

Exit the writer session. Claude asks whether to keep the worktree. Keep it; the branch has your commits. Merge it, or open a PR from it, when you're back at your desk: `git worktree list` shows where it is.

Post one line in the chat: "The reviewer caught ___ that the writer missed." A TA reads three out.

---

## Fallback: no dependencies, no time

If the worktree can't run your tests in the time you have, review the plan instead of the code. Writer: `/plan implement @SPEC.md` and stop at the plan. Reviewer: "read `.claude/worktrees/writer/` and review the plan Claude wrote there against @SPEC.md". Same pattern, no build required.

---

## If you finish early

1. Send the review across instead of pasting it. Type `@` in the reviewer session and pick the `writer` session from the list: "send your findings to the writer session". Claude passes the message; the writer receives it as a notification. (Cross-session messaging; the docs say macOS and Linux.)
2. Give a subagent its own worktree: add `isolation: worktree` to a custom agent's header. Every run gets a scratch checkout that disappears if it changes nothing.
3. `/branch try-other-approach` in the writer session copies the conversation so you can try a different implementation without losing this one. `/resume writer` brings you back.
4. `claude --worktree "#123"` starts a session on pull request 123's branch. Try it on a colleague's open PR: "review this PR against its description".

---

One session writes, another reads. Neither one grades its own homework.
