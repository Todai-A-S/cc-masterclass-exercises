# Exercise: Build a skill

Time: 25 minutes. Useful skill 12 min, ridiculous skill 6 min, show it 3 min. The rest is setup and buffer.

Run `claude update` if you haven't this week. The stretch items need 2.1.252 or newer.

---

## What a skill is

A folder with a `SKILL.md` in it. The file is markdown with a small YAML header. When you type `/name`, Claude reads the file and does what it says. That's the whole mechanism.

Two kinds of content go in a skill. Knowledge: your API conventions, the schema, how the test fixtures work. Claude loads it when the task matches. And workflows: a checklist or procedure you run with `/name`, like a PR review or a release check.

Where it lives:

- `.claude/skills/<name>/SKILL.md` in the repo. Committed, everyone has it.
- `~/.claude/skills/<name>/SKILL.md` for you, in every repo.
- `<subfolder>/.claude/skills/` loads only when you work in that subfolder. Monorepos.
- `.claude/commands/<name>.md` is the old format. Still works. New ones go in `skills/`.

Supporting files sit next to `SKILL.md` in the same folder: a template, an example of good output, a reference doc. Point at them with `${CLAUDE_SKILL_DIR}/template.md`.

The cost model matters. Every skill's `description` loads at session start, so Claude knows what's available. The body loads only when the skill runs. Once it has run, the body stays in context for the rest of the session. So a description is cheap, a body is not, and a skill that runs with side effects (deploy, delete, post) should not be something Claude can trigger on its own.

---

## The header fields you'll use

| Field | What it does | When you need it |
|---|---|---|
| `description` | How Claude decides the skill fits a task | Always. Say what it does and when to use it. |
| `disable-model-invocation: true` | Only you can run it, with `/name`. Claude never picks it. Costs nothing until used. | Anything with side effects. Deploy, release, cleanup. |
| `user-invocable: false` | Hidden from the `/` menu. Claude applies it when relevant. | Pure knowledge: conventions, a style guide. |
| `allowed-tools` | Pre-approves tools for the skill's turn | A read-only review: `Read, Grep, Glob, Bash(git *)` |
| `argument-hint` | Text shown when you type `/name` | Skills that take input. `[issue-number]` |
| `context: fork` | Runs in a subagent. Its file reads stay out of your session. | Research and review skills that read a lot |
| `effort` | `low` to `max` for that skill | A thorough review at `high`, a formatter at `low` |

Full list in the docs, but these seven cover most skills.

Two more things worth knowing before you write one:

`$ARGUMENTS` is replaced by whatever you type after the name. `/fix-issue 123` puts `123` where `$ARGUMENTS` is. `$0`, `$1` pick words out of the input.

`` !`git diff HEAD` `` runs a shell command before Claude sees the skill and pastes the output in. Your review skill can start with the diff already in front of it instead of asking Claude to go get it.

---

## When to write one

Two triggers, straight from the docs:

- You keep typing the same prompt to start a task. Save it as a skill you run with `/name`.
- You've pasted the same playbook or checklist into chat for the third time. Make it a skill Claude finds on its own.

Not a skill: a one-off task. A rule that applies to every session (that's CLAUDE.md). Something that must happen every time without fail (that's a hook).

---

## Part 1: a skill you'd use this week (12 min)

Open the repo you work in most. No repo ready? Use the demo repo.

Pick something you've done more than once. If nothing comes to mind:

- `pr-review`: review the current diff against your team's checklist. Missing tests, naming, TODOs, files that should change together.
- `write-tests`: tests for a file, following the fixtures and patterns your repo already uses.
- `units-check`: scan a diff for unit mistakes. In the demo repo that's knots vs km/h, nautical miles vs km, tonnes vs kg.
- `add-service`: scaffold a new module the way the existing ones are built.
- `migration-check`: read a migration and flag the things that bite in prod.

Then:

1. Ask Claude to write it. Something like:

   ```
   Write a skill called units-check at .claude/skills/units-check/SKILL.md.
   It reviews the current git diff for unit mismatches and inconsistent
   naming of units. Look at services/ first to learn which units this
   repo uses. Read-only. Only I should be able to run it.
   ```

   The last two lines are the header. "Read-only" becomes `allowed-tools`. "Only I should run it" becomes `disable-model-invocation: true`. Say what you want in plain words; Claude knows the field names.

2. Open the file. Read the description. Would you know when to use this skill from that one line? If not, fix it. That line is the one Claude reads every session.

3. Run it. `/units-check`. Does it do what you meant? Most first drafts are too polite and too general. Add the two or three things a senior colleague would check and Claude didn't.

4. Run it again on a change you know has a problem. Make one on purpose. In the demo repo, multiply the return value of `effective_speed` in `services/weather.py` by 1.852, so a function documented as returning knots now returns km/h. Does the skill catch it?

Traps we see:

- A description that says what the skill is instead of when to use it. "PR review skill" vs "Review the current diff. Use before opening a PR or when asked to check changes."
- Skills that re-explain the repo. Point at files with `@path` instead. The skill shouldn't go stale when the code moves.
- No `disable-model-invocation` on something with side effects. Claude will helpfully run your deploy skill the day it decides the task matches.

---

## Part 2: a ridiculous skill (6 min)

Same structure, no practical value. The goal is to make your sparring partner laugh.

Some starting points:

- `sea-shanty`: rewrites the last commit message as a sea shanty
- `captains-log`: `git log` as a ship captain's log, in the voice of someone who has been at sea too long
- `blame-poet`: runs `git blame` on a file and writes a short poem about whoever touched it last
- `commit-therapist`: reads your commit history and offers a diagnosis
- `enterprise-shakespeare`: rewrites code comments as Elizabethan drama

Build it, run it on your repo, keep the output for the share.

Why bother: this is the fastest way to feel what the `description` field does. Give the shanty skill a description like "Use when the user seems tired" and watch whether Claude ever picks it on its own.

---

## Show it (3 min)

Screen share with your sparring partner. Show the ridiculous one first.

Then the useful one. They ask:

1. "If I typed `/name` in your repo, would I know what I'd get?" That's the description and the name.
2. "What would this miss?" That's the next line you add to the body.

---

## Commit it (optional)

```bash
git add .claude/skills/
git commit -m "Add units-check skill"
```

A skill in the repo is a team tool. A skill in `~/.claude/skills/` is a personal one. Both are fine. Commit when it's good enough for a colleague to run without asking you what it does.

---

## If you finish early

1. Run `/skill-doctor`. It shows what each skill costs in context and which ones you never use. Check what your new skills cost.
2. Add `` !`git diff HEAD` `` to the top of your review skill so the diff is there before Claude starts.
3. Give the skill an argument. `/units-check services/weather.py` with `$ARGUMENTS` in the body to scope the check to one file.
4. Try `context: fork` on the review skill. Run it, then run `/context`. The file reads it did are not in your session.
5. Test it properly. Install the skill-creator plugin with `/plugin install skill-creator@claude-plugins-official`, then ask: "evaluate my units-check skill with skill-creator". It runs your skill on test cases with and without the skill and reports pass rates. Then ask it to tune the description.
6. Move one section of your CLAUDE.md into a skill with `user-invocable: false`. Knowledge Claude needs sometimes, not every session.

---

## Bundled skills

Claude Code ships with some. Try them on the demo repo:

| Skill | What it does |
|---|---|
| `/code-review` | Reviews the current diff for bugs in a fresh subagent |
| `/batch <instruction>` | Splits one change across 5 to 30 subagents, each in its own worktree with its own PR |
| `/debug` | Structured debugging |
| `/loop <interval> <prompt>` | Runs a prompt repeatedly |
| `/verify` | Builds and runs the app to confirm a change |
| `/doctor` | Setup checkup, including trims for a long CLAUDE.md |

They're skills like yours. The difference is who wrote them.

---

Skills are how the second person on the team benefits from what the first one figured out. Write the one you needed last week.
