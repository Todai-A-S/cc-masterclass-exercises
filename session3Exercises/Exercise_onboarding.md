# Exercise: Land in a repo you don't know

Time: 15 minutes. Setup 2 min, questions 8 min, `/init` 3 min, share 2 min.

---

## Before the session

Pick a repo in your organisation you have never worked in. A neighbouring team's service, a library you only consume, the thing you always open a ticket for instead of fixing yourself. Clone it. You need read access and nothing else.

Don't pick your own repo. The whole point is that you don't know where anything is.

---

## Why this is an exercise

Every earlier exercise ran on code you knew. Research → Plan → Implement in Session 1 started from a task you could already picture. This one starts cold, which is where most of the time in a career goes: the legacy service nobody owns, the repo you inherit, the bug that lives three teams away.

Claude reads a codebase faster than you do. The skill is asking it the questions a senior engineer would ask on day one, and checking the answers against the code instead of taking them on trust.

---

## Part 1: ask like a senior engineer (8 min)

Start Claude in the repo and switch to plan mode (`Shift+Tab` until the status bar says plan mode). Nothing gets edited today.

Ask these, in this order. Adapt the nouns to the repo.

```
give me an overview of this codebase: what it does, how it's laid out, and the three things I should read first
```

```
where does [the thing this repo is for] actually happen? name files and line numbers
```

```
trace one request end to end: from the entry point to the database or the external call. list every file it passes through
```

```
what edge cases does @src/[the module from the trace] handle, and which ones does it not?
```

```
if you had one afternoon to make this repo easier to work in, what would you change and why?
```

Two rules while you do this:

1. **Ask for evidence.** When an answer sounds right, ask "show me the line". Claude's second answer is the one you can trust. If it can't point at a line, it guessed.
2. **Use `@` for what you already know.** `@src/payments/` puts the directory listing in front of Claude; `@src/payments/refund.py` puts the file in. Faster than describing where things live.

Write down one thing you learned that would have cost you an afternoon to find by hand. That's your share-out line.

---

## Part 2: `/init` on a foreign repo (3 min)

Run `/init`. Claude scans the repo and drafts a CLAUDE.md.

Read it as the person who would have to maintain it. Three questions:

- What did it get right that you didn't know five minutes ago?
- What did it get wrong or overstate? (It will. `/init` reads the code, not the team.)
- Which three lines would the team that owns this repo add? Conventions, "don't touch X", the command that isn't in the README. You can't write those lines. That's the point from Session 1: the value of CLAUDE.md is what `/init` can't see.

Don't commit it. It's not your repo.

---

## Share (2 min)

Post your one line in the chat: "In [repo], Claude found ___ in ___ minutes." A TA reads three out. No discussion needed; the lines are the discussion.

---

## If you finish early

1. Ask about history, not just code: `look through the git history of [file] and summarise how it got this way`. Claude runs `git log` and `git blame` for you.
2. Install a code intelligence plugin for the repo's language: `/plugin install pyright-lsp@claude-plugins-official` (Python), `csharp-lsp` (.NET), `typescript-lsp` (TS). You need the language server binary installed too; the plugin details say which. With it, Claude jumps to definitions instead of grepping, and sees type errors after every edit.
3. Ask for a glossary: `list the project-specific terms and abbreviations in this codebase with one line each`. Paste it at the top of your notes.
4. `/btw` for the side questions ("what does this decorator do") so they don't fill your context.

---

Claude will tell you what a codebase does in five minutes. It takes you another five to check. Both halves are the job.
