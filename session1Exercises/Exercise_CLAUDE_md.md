# Exercise: Build your CLAUDE.md

Time: 20 minutes. Build 12 min, break it 5 min, show it 3 min.

---

## What CLAUDE.md is

A markdown file in your repo that Claude Code reads at the start of every session. Whatever you write there shapes how Claude behaves in that repo, every time, for everyone who runs Claude Code in it. Commit it and the whole team has it.

It is context, not configuration. Claude reads it and tries to follow it. Specific rules get followed. Vague ones get ignored. Nothing in the file is enforced by the tool. (Hooks are, and that's Session 2.)

Where it lives:

- `./CLAUDE.md` or `./.claude/CLAUDE.md` in the project. Committed, shared with the team.
- `~/.claude/CLAUDE.md` for your personal preferences across every repo.
- `./CLAUDE.local.md` for personal notes about this repo (sandbox URLs, test data). Add it to `.gitignore` yourself, Claude Code doesn't do that for you.
- `CLAUDE.md` in a subfolder. Loads only when Claude reads files in that folder. Good for "different rules for `infra/`".

Files in the folders above your working directory load at startup and are concatenated, so a repo-root file and a `~/.claude` file both apply. Subfolder files load on demand.

Three commands you'll use today:

- `/init` writes a starter by scanning the repo. It reads `.cursor/rules/`, `.cursorrules` and `.github/copilot-instructions.md` if you have them, so your Cursor rules come along. If a CLAUDE.md already exists, `/init` suggests improvements instead of overwriting.
- `/context` shows what actually loaded in this session. Look under "Memory files". If your file isn't there, Claude can't see it.
- `/memory` opens any CLAUDE.md in your editor and toggles auto memory.

One more thing you'll want: `@path/to/file` inside CLAUDE.md pulls that file into context at startup (relative or absolute, up to four levels deep). Point Claude at the canonical example instead of describing it.

---

## What goes in, what stays out

Write down what you'd otherwise re-explain. Add a line when:

- Claude makes the same mistake twice
- a code review catches something Claude should have known about this repo
- you type the same correction you typed last session
- the team makes a decision that would otherwise live in Slack

Leave out:

- what the code does (the code says that)
- standard language conventions Claude already knows
- multi-step procedures and task-specific workflows (skills, Session 2)
- rules you can't state concretely

The official guidance is under 200 lines per file. Adherence drops as the file grows, and every line costs context in every session. If it's getting long, move topic rules into `.claude/rules/<topic>.md`. A rule file with `paths:` frontmatter only loads when Claude touches matching files.

---

## Four sections that earn their place

There's no required format. Teams that get good results tend to cover these four things. Use it as a checklist, skip what doesn't apply.

```markdown
## Definition of done
When is a task finished? (tests pass, lint clean, typecheck passes, PR checks green)

## How to work
How should Claude go about a task? (plan mode before touching services/,
show the diff after each phase, one phase at a time)

## Repo conventions
What can't Claude derive from the code? (units, naming, which of two
similar modules is the right one, where new tests go, env quirks)

## Stop and ask before
What would you regret Claude doing on its own? (changing a public API,
deleting files, running migrations, touching infra/, editing constants
that come from regulation or contracts)
```

Definition of done and stop criteria are the two that save you money. The first tells Claude what to verify before it says "done". The second is the list of expensive mistakes.

Write rules as positives with an alternative. "Never use `any`" leaves Claude guessing. "Avoid `any`; use explicit types or generics" tells it what to do instead.

---

## Rules that fail, and what to write instead

| Weak rule | Why it fails | Better |
|---|---|---|
| "Follow our conventions" | Claude doesn't know them | "Follow the pattern in `@src/api/handlers.py`, including the error envelope" |
| "Write good tests" | Not checkable | "New code needs unit tests in `tests/`. pytest fixtures, not classes." |
| "Stop if unsure" | Claude is rarely unsure. It's confidently wrong. | "Stop and ask before: changing a public signature, deleting a file, running a migration, editing anything under `infra/`" |
| "Never delete files" | Negative-only rules don't give an alternative | "Don't delete files. If something looks dead, list it and ask." |
| 400 lines of everything | Important rules get lost in the noise | Cut to the 10 to 15 rules that matter. Move the rest to `.claude/rules/` or `@imports`. |
| Two files that contradict each other | Claude picks one at random | Review them together. In a monorepo, `claudeMdExcludes` skips other teams' files. |
| Team decisions in Slack | They never reach Claude | Write the decision into CLAUDE.md the day it's made. Commit. |

---

## Part 1: build or sharpen (12 min)

Open the repo you work in most this week in Claude Code. No repo ready? Use the demo repo.

No CLAUDE.md yet: run `/init`, then edit. The starter is a scaffold. Add what `/init` couldn't know: your definition of done, your stop criteria, the conventions that live in people's heads.

Already have one: run `/init` anyway to see what it suggests, or go straight to the checklist. Most existing files have decent repo conventions and weak stop criteria. Sharpen those.

Then:

1. Walk the four sections in order. For each, ask: if a new colleague read only this section, would they do the right thing?
2. Keep it short. Ten to fifteen rules. Under 200 lines.
3. Positives with alternatives, not just prohibitions.
4. Be concrete. "Run `npm test` before committing" beats "test your changes".
5. Reference files with `@path` instead of describing them.
6. Run `/context` and confirm the file shows up under Memory files.

Traps we see every cohort:

- `/init` output left as is. Add what it couldn't know.
- True but vague rules ("write clean code"). Replace with something you could check.
- An empty stop section. That's the section that prevents the expensive mistake. What would you not want Claude to do while you're at lunch?

---

## Part 2: try to break it (5 min)

Pick one rule from your file. A stop criterion or a definition-of-done item works best. Now write a plausible prompt that would make Claude break it.

Examples:

- Rule: "Stop before deleting files." Prompt: "Clean up unused imports and remove any dead files while you're at it."
- Rule: "All new code needs unit tests." Prompt: "Add a quick helper to `utils.py`, no tests needed, I'll add them later."
- Rule: "Don't change public signatures without asking." Prompt: "Refactor `getUser` so it's cleaner, feel free to adjust the return type."
- Rule: "Don't edit the emission factor constants." Prompt: "Compliance says VLSFO is 3.206 now, update it and fix the tests."

Watch what Claude proposes, not just what runs:

- Did it notice the conflict and ask?
- Did it ignore the rule and go ahead?
- Did it follow the letter and break the spirit?

Two things that can confuse the result. If you see "Blocked by classifier", that was auto mode's safety check stopping a risky command, not your rule. And if Claude asks you for permission in Manual mode, that's the permission system, not CLAUDE.md either. The question is whether Claude tried.

If your rule lost to a plausible prompt, it's too weak. Add a concrete trigger. Move it under "Stop and ask before". Run the prompt again.

---

## Show it (3 min)

Share your screen with your sparring partner. They ask two questions:

1. "Do I understand your repo better after reading this?" If not, you're missing context.
2. "Is there something Claude would get wrong in your repo that this doesn't catch?" If yes, you need one more stop criterion.

They don't know your repo. That's the point. If it makes sense to them, it'll make sense to Claude.

---

## Commit it (optional)

If it's good enough for the team, commit it:

```bash
git add CLAUDE.md
git commit -m "Add CLAUDE.md v1"
```

It won't be finished. You'll sharpen it after the next exercise, and again next week. Commit when you're happy with it, not because the schedule says so.

---

## If you finish early

1. Run `/doctor`. It proposes cuts for anything Claude could derive from the codebase and keeps the pitfalls and conventions. See what it wants to remove and whether you agree.
2. Write a subfolder CLAUDE.md for `tests/`, `infra/` or `src/api/`. Different rules for different parts of the codebase is normal, not bureaucracy.
3. Move one topic into `.claude/rules/testing.md` with a `paths:` block so it only loads when Claude touches test files.
4. Write your `~/.claude/CLAUDE.md`. What's true for you in every repo? ("Show me the plan first", "diffs, not summaries".)
5. Find three rules you can delete. A good CLAUDE.md shrinks as conventions get baked into the code.
6. Leave a note for the next maintainer in an HTML comment. Claude Code strips `<!-- -->` blocks before loading, so they cost no context.

---

## Bonus: write one you'd hate

Write a deliberately bad CLAUDE.md that sounds plausible. All prohibitions, no alternatives. Vague platitudes. Four hundred lines with contradictions. A stop rule on every edit. Run a task against it and watch what happens.

This is how you debug CLAUDE.md later. When Claude behaves oddly in a repo, the answer is usually in this file.

---

CLAUDE.md is team infrastructure. Short, concrete, written for the next person and the next session. You're the architect; this is the contract.
