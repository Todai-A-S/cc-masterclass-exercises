# Exercise: Let a method plan your task

Time: 17 minutes. Install 2 min, brainstorm 10 min, read the plan 3 min, share 2 min.

---

## What you're installing

superpowers is a plugin: a set of skills, written by someone who uses Claude Code all day, that make Claude follow one way of working. Brainstorm the design with you, write a plan, build it test-first, review, finish the branch. Each step is a skill, like the ones you wrote in Session 2.

Today you use the first two steps only. Claude interviews you about a task, writes a design, then turns it into a plan. No code gets written. Brainstorming won't let it until you've approved the design.

The plan you get out of this is what you implement in the parallel exercise later today.

---

## Install (2 min)

In a Claude session in your repo:

```
/plugin install superpowers@claude-plugins-official
```

Pick **user** scope when it asks. Then `/reload-plugins`, or restart Claude.

Before you trust any plugin, look at what it runs on your machine. `claude plugin details superpowers` in your shell shows its skills, hooks and servers.

If the install is blocked on your machine, skip to the fallback at the bottom. Same output, no plugin.

---

## Brainstorm (10 min)

Pick one task from your backlog. Small enough to build a first slice of in 15 minutes later today. Examples:

- add an index and the migration for it, plus the query that needs it
- a new step in a pipeline that fails the build when a check doesn't pass
- a health check endpoint that also checks the database connection
- turn a manual runbook step into a script

Type `/brain`, pick superpowers' brainstorming from the menu, and describe the task in one or two sentences.

What happens:

1. Claude reads the repo, then asks one question per message. Answer short. "I don't know, check the code" is a fine answer.
2. Every few questions it plays back what it understood. Correct it if it's wrong.
3. It proposes two or three approaches and recommends one. Pick one.
4. It writes a design doc to `docs/superpowers/specs/` and asks you to approve it. Read it, then approve or ask for changes.
5. It moves on to writing the plan: small tasks, each with the files it touches and how to check it.

When it asks how to execute the plan, stop there. Say "not now". You'll do that in the parallel exercise.

If it's still asking questions at minute 7, say: "that's enough, write the design with what you have".

---

## Read the plan (3 min)

Open the plan in `docs/superpowers/plans/`. Three questions:

- Which question during brainstorming made you stop and think?
- Is the first task small enough to build in 15 minutes? If not, ask: "split task 1 into something smaller".
- How does task 1 get checked? A unit test, or something that runs the real thing?

Then commit both files. Worktrees start from committed work, so the parallel exercise can't see them otherwise:

```
commit the design doc and the plan
```

---

## Share (2 min)

One line in the chat:

> superpowers asked me ___, which I hadn't thought about.

---

## Fallback: no plugin

Same output, by hand. Fresh session, not plan mode:

```
I want to build [one sentence]. Interview me in detail using the
AskUserQuestion tool. Dig into the hard parts I might not have considered.
When we've covered it, write a design to docs/design.md, then a plan to
docs/plan.md: small tasks, each with the files it touches and how to check it.
```

---

## If you finish early

1. Open one of superpowers' skills and read it: `~/.claude/plugins/` has the files. `brainstorming/SKILL.md` is a good example of how to write a skill that asks before it acts.
2. Try pstack, a different method: principles instead of phases. Community port for Claude Code: `/plugin marketplace add michael-denyer/pstack-claude`, then `/plugin install pstack@pstack-claude`, then `/pstack:setup-pstack`. It installs a hook that can switch it on by itself; setup lets you turn that off. Heavy on tokens.
3. Turn superpowers off again if it gets in your way: `claude plugin disable superpowers@claude-plugins-official`.

---

A plugin is someone else's way of working. Take the parts that work for you.
