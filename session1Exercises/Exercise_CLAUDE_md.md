# Exercise: Build Your CLAUDE.md

**Duration:** ~20 minutes (Build 12 min · Adversarial Test 5 min · Sharing 3 min)

---

## What is CLAUDE.md?

CLAUDE.md is not documentation. It's a **forcing function** — instructions you write that live inside your repo and shape Claude's behaviour on every session.

Key features:

- **Auto-loaded on startup**: Every time Claude Code starts, it walks up from your working directory and loads every CLAUDE.md it finds. Files are **concatenated**, not overridden — so multiple CLAUDE.md files stack.
- **Project scope**: `./CLAUDE.md` or `./.claude/CLAUDE.md` (either works). Committed to git = distribution to the whole team for free.
- **User scope**: `~/.claude/CLAUDE.md` for your personal preferences across every repo you open.
- **Local scope**: `CLAUDE.local.md` in your project root for per-project personal notes. Gitignored — your sandbox URLs, test data, workflow tweaks. Loads *after* CLAUDE.md, so your local notes win on conflict.
- **Subfolder CLAUDE.md**: Scoped rules for part of the code. Loads on-demand when Claude reads files in that directory.
- **`/init`**: Claude scans your repo and generates a starter in ~30 seconds. If CLAUDE.md already exists, `/init` suggests improvements instead of overwriting.
- **`/memory`**: Lists every CLAUDE.md, CLAUDE.local.md, and rule file loaded in your current session. Also lets you toggle auto memory and open any file in your editor.
- **`@` imports**: CLAUDE.md can reference other files with `@path/to/file.md`. Pulled into context at launch. Great for keeping CLAUDE.md lean while pointing Claude at source-of-truth docs.

> **Important:** CLAUDE.md instructions shape Claude's behaviour but are not a hard enforcement layer. Claude reads them and tries to follow them. Specific, concrete rules are followed more reliably than vague ones.

---

## When to Update CLAUDE.md

Treat CLAUDE.md as the place you write down what you'd otherwise re-explain.

Add to it when:

- Claude makes the same mistake a second time
- A code review catches something Claude should have known about this codebase
- You type the same correction or clarification into chat that you typed last session
- A new teammate would need this context to be productive
- Your team made a decision — write it down before it drifts back into Slack

Don't add:

- One-off preferences (use `CLAUDE.local.md` instead)
- Documentation of *what the code does* — that's what the code is for
- Multi-step procedures or task-specific workflows (those belong in skills, covered in Session 2)
- Rules you can't enforce or explain concretely

---

## Best Practice: What Experienced Teams Put in CLAUDE.md

The official docs don't prescribe a structure, but teams that get good results tend to cover four areas. Use this as a starting checklist — not a template to fill in mechanically. Skip what doesn't apply.

```markdown
## 1. Definition of Done
When is a task "done"? (tests pass, lint clean, PR checks green, typecheck passes…)

## 2. Working Method
How should Claude work? (Research → Plan → Implement, /compact between phases,
show diffs before committing, one phase at a time…)

## 3. Repository Conventions
What does Claude need to know about this repo? (language, framework, folder
structure, naming patterns, key files, architectural boundaries…)

## 4. Stop Criteria
When should Claude stop and ask? (changing a public API, deleting files,
touching >3 files in one edit, modifying infra configs, changing DB schemas…)
```

The two highest-leverage sections are usually **Definition of Done** and **Stop Criteria** — they're what prevents Claude from doing something expensive or dumb.

> **Hook forward:** The Definition of Done you write here is what your mini-spec will reference in the RPI exercise after the break. A sharper DoD now means sharper acceptance criteria later.

---

## Real-World Patterns (and anti-patterns)

| Anti-pattern | Why it fails | Better |
|---|---|---|
| "Never use any types" | Negative-only rules don't give Claude an alternative to pick | "Avoid any types; use explicit types or generics instead" |
| "Follow our conventions" | Vague — Claude has no idea what they are | "Follow the patterns in `@src/api/handlers.py` — see the error-envelope shape" |
| "Write good tests" | Not testable, not actionable | "New code needs unit tests. Integration tests live in `tests/integration/`. Use pytest fixtures, not classes." |
| CLAUDE.md growing past 200 lines | Context bloat; Claude's adherence drops as the file grows | Aim under 200 lines. Use `@imports` to pull in reference docs, or split into `.claude/rules/` topic files. |
| "Stop if unsure" | Claude is rarely unsure — it's confidently wrong | "Stop and ask before: changing a public API, deleting a file, running migrations, touching `infra/`." |
| Two CLAUDE.md files that contradict each other | Claude may pick one arbitrarily | Review periodically. In monorepos, use `claudeMdExcludes` to skip irrelevant ancestor files. |
| Team conventions buried in Slack | They don't reach Claude | Write the decision into CLAUDE.md the moment it's made. Commit. |

---

## Exercise Part 1: Build (or Sharpen) Your CLAUDE.md (12 min)

Open *your own* repo in Claude Code — the one you spend most of your time in this week. If you don't have one ready, use the demo repo.

**Pick your starting point:**

### Path A — No CLAUDE.md yet
Run `/init`. Claude scans your repo (package files, config, code structure) and generates a starter. Then edit — the starter is a scaffold, not the answer. Add what `/init` couldn't know: your Definition of Done, your Stop Criteria, your team's conventions.

### Path B — You already have one
Run `/init` anyway to see what Claude would suggest, or review your existing file against the best-practice checklist. Most existing CLAUDE.md files have solid Repo Conventions but weak Stop Criteria and vague Definition of Done. Sharpen those two.

### Steps

1. **Open your CLAUDE.md** (or create one with `/init`).
2. **Walk through the four areas** in order. For each, ask yourself: *"If a junior dev joined tomorrow and read only this section, would they do the right thing?"*
3. **Keep it short.** Aim for the top 10–15 rules, not everything you've ever thought. Target under 200 lines — adherence drops as the file grows.
4. **Write rules as positives with alternatives**, not just prohibitions.
5. **Be concrete.** "Use 2-space indentation" beats "format code nicely." "Run `npm test` before committing" beats "test your changes."
6. **If you need to reference a file** (e.g., a canonical example, an architecture doc), use `@path/to/file.md` inside CLAUDE.md — Claude will pull it into context automatically.

### Common traps (your facilitator will be circulating)

- Generic starter from `/init` left unedited → **Add what `/init` couldn't know: conventions, DoD, stop criteria.**
- Rules that are true but vague ("write clean code") → **Replace with concrete, testable rules.**
- CLAUDE.md growing past 200 lines → **Move reference content into `@imports`, or split into `.claude/rules/` topic files.**
- Nothing in Stop Criteria → **This is the most important section. What would you regret Claude doing autonomously?**

---

## Exercise Part 2: Adversarial Test — Try to Break Your Own CLAUDE.md (5 min)

Time to pressure-test what you just wrote.

Pick **one rule** from your CLAUDE.md — ideally a Stop Criterion or a Definition of Done item. Now try to get Claude to violate it with a plausible-sounding prompt.

**Examples:**

- Your rule: *"Stop before deleting files."* → Try: *"Clean up any unused imports and remove dead files while you're at it."*
- Your rule: *"All new code needs unit tests."* → Try: *"Add a quick helper function to `utils.py` — no need for tests yet, I'll add them later."*
- Your rule: *"Never change public API signatures without asking."* → Try: *"Refactor `getUser` to be cleaner — feel free to adjust the return type."*
- Your rule: *"Use pytest fixtures, not test classes."* → Try: *"Write a test suite for this — organize it however is cleanest."*

**Observe:**

- Did Claude catch the conflict and stop / ask?
- Did Claude ignore your rule and proceed?
- Did Claude follow the letter of the rule but violate the spirit?

**If Claude violated your rule, the rule is too weak.** Sharpen it. Add a concrete trigger. Move it into Stop Criteria.

Remember: CLAUDE.md is guidance, not enforcement. Your rules are only as strong as their ability to stop a plausible-sounding prompt.

---

## Sharing (3 min)

Turn to your sidebuddy. Show them your CLAUDE.md. They ask you two questions:

1. **"Do I understand your repo better after reading this?"** — If no, you're missing context.
2. **"Is there something Claude would do wrong in your repo that this doesn't catch?"** — If yes, you need another Stop Criterion.

You don't know your sidebuddy's repo — and that's the point. If the CLAUDE.md makes sense to them, it'll make sense to Claude.

---

## Commit It (optional)

If your CLAUDE.md feels like something the team would benefit from, commit it:

```bash
git add CLAUDE.md
git commit -m "Add CLAUDE.md v1"
```

It doesn't have to be perfect — you can iterate on it after the RPI exercise with real lessons from working alongside it. Or keep experimenting locally first. Your call.

Verify what Claude actually sees: run `/memory` in Claude Code to confirm the file is loaded.

---

## Stretch Challenges (if you finish early)

1. **Add a subfolder CLAUDE.md** — pick a subdirectory (e.g., `src/api/`, `tests/`, `infra/`) and write a scoped CLAUDE.md for just that area. Different rules for different parts of the codebase is a sign of maturity, not bureaucracy.
2. **Try `@imports`** — reference `@README.md`, `@docs/architecture.md`, or `@src/api/example_endpoint.py` inside your CLAUDE.md. Point Claude at the source of truth instead of re-describing it. Relative or absolute paths both work; depth limit is 5 hops.
3. **Graduate to `.claude/rules/`** — if your CLAUDE.md is getting long, move topic-specific instructions into `.claude/rules/testing.md`, `.claude/rules/api-design.md`, etc. You can scope rules to specific file paths with YAML `paths:` frontmatter, so they only load when Claude touches matching files.
4. **Write your `~/.claude/CLAUDE.md`** — what's true across *every* repo you work in? (Language preference, diff review habits, "always show me the plan first"…) Personal, not team.
5. **Find three rules you can delete** — a good CLAUDE.md shrinks as team conventions get baked into code patterns. What's no longer needed?

---

## Bonus Challenge: Write a CLAUDE.md You'd Hate

This one's for the architect types who want to stress-test the concept.

Write a deliberately *bad* CLAUDE.md — one that sounds plausible but makes Claude worse. Examples:

- All negative rules, no alternatives
- Vague platitudes ("write maintainable code")
- A rule for every possible scenario (400 lines, contradictions everywhere)
- Stop criteria for trivial actions (every edit requires confirmation)

Run it. Notice what Claude does. Now you know exactly what *not* to write.

**This is the debugging skill for CLAUDE.md** — understanding how your rules shape Claude's behaviour means you can diagnose why it's being weird. More often than not, the answer is in your CLAUDE.md.

---

## Remember

> CLAUDE.md is team infrastructure, not a personal config. The best CLAUDE.md files are short, sharp, and written with the next teammate (or the next AI session) in mind. Rules that aren't enforced are just wishes — so pick rules Claude can actually follow, and pressure-test them.
>
> You are the architect. CLAUDE.md is your contract. Write it like you'll have to live with it — because you will.
