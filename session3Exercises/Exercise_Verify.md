# Exercise: Make Claude run it

Time: 20 minutes. Record the recipe 9 min, verify a change 9 min, share 2 min.

---

## The one idea

When Claude says "done", that's a claim. Tests Claude wrote for code Claude wrote can pass and still miss the point. The proof is running the real thing the way a person would and looking at what happens: the rows the query returns, the response the service sends, the output of the pipeline step.

Two bundled commands do this:

| Command | What it does |
|---|---|
| `/run-skill-generator` | Gets your app running from a clean start, then saves what worked (install steps, env vars, launch command) as a skill in `.claude/skills/run-<name>/`. Once per repo. |
| `/verify` | Builds and runs your app to check a change does what it should, without falling back on tests or type checks. After a change. |

`/verify` works without the recipe too, but it guesses how to start your app. Anything with a database, an env file or a multi-step build, it guesses wrong. That's why you record the recipe first.

Run it against something you can lose: a local container, a throwaway database, a sandbox account. Never production.

---

## Part 1: record the recipe (9 min)

In your repo:

```
/run-skill-generator
```

Claude works out how to start your app, tries it, fixes what fails, and writes the skill. Approve the commands it wants to run. If it needs a database, tell it: "use a local Postgres in Docker".

When it's done, open `.claude/skills/run-<name>/SKILL.md` and read it:

- Is that how you'd start it?
- Did it find a step that isn't in the README?
- Is anything in it pointing at a shared or production environment? Fix that now.

Not finished at minute 9? Stop it and go to Part 2. `/verify` writes down what worked when it has to figure it out itself.

---

## Part 2: verify a change (9 min)

Take your most recent change: your last commit, or a branch you have open. Tell `/verify` what it should do:

```
/verify the change in my last commit: [one sentence on what it should do]
```

Examples:

- `/verify the last commit: the new index makes the orders-by-customer query use an index scan`
- `/verify the last commit: /health returns 503 when the database is down`
- `/verify the last commit: the pipeline step fails when the schema file has a duplicate column`

Then read what it did, not just what it concluded:

- What did it actually run?
- What did it look at to decide? A query result, a response, a log line?
- Would you accept that as proof from a colleague?

If the answer is no, tell it what proof you'd want: "start the service, stop the database container, call /health, show me the response". That sentence is what a good check looks like.

---

## If your repo isn't an app

Same idea, different "run it":

- SQL and migrations: apply to a Postgres in Docker, run the queries that use it, look at the rows. Roll back, apply again.
- Terraform: `validate`, then `plan` against a sandbox. Read the plan.
- Pipelines and scripts: run the step locally with real input and check the exit code and output.

Ask Claude to do exactly that and show you the output.

---

## Can't start anything?

No Docker, the service needs cloud credentials, or nothing in the repo runs locally: pick the smallest thing that does. A script, one query against a Postgres in Docker, a CLI command. Ask Claude to run it and show you the output, then `/verify` a small change to it. The habit is the point, not the app.

---

## Share (2 min)

One line in the chat:

> /verify checked ___ by ___.

---

## If you finish early

1. Commit the run skill. Now everyone on the repo, and every Claude session in it, starts the app the same way.
2. Write three things the change should do in plain words, then: `/verify these three, one at a time, and show me the output for each`.
3. Ask a fresh session to verify without showing it the diff: only the three sentences and the run skill. It can't be convinced by code it hasn't read.
4. Want it every time? `/goal` for this session, or a Stop hook for every session. Session 2's ladder, top rung.

---

Tests say the code does what Claude thought. Running it says it does what you wanted.
