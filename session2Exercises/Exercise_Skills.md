# Exercise: Build a Skill

**Duration:** ~20 minutes

---

## What is a Claude Code Skill?

A skill is a reusable prompt template that lives in your repo at `.claude/skills/<name>/SKILL.md`. It's a markdown file—optionally with YAML frontmatter—that encodes a workflow you want Claude to follow consistently. Key features:

- **Frontmatter fields**: `description` (used for discoverability), `allowed-tools` (restrict what Claude can use), `context: fork` (runs in isolated context), `$ARGUMENTS` (parameterised input)
- **Supporting files**: Keep templates, examples, and reference docs in the same directory as your skill
- **Invocation**: Call it with `/skill-name` in Claude Code
- **Scope**: User-invocable (you trigger them) or model-invocable (Claude runs them automatically based on description)
- **Distribution**: Commit to repo, available to the whole team
- **Bundled examples**: `/batch`, `/simplify`, `/debug`

---

## When to Build a Skill

Build a skill when:

- You've written the same prompt pattern more than twice
- You want consistent output format across your team
- You're encoding team conventions (naming patterns, testing standards, review criteria)
- You want to constrain what Claude can do for a specific workflow (e.g., read-only analysis)

---

## Exercise Part 1: Build a Useful Skill (12 minutes)

Think about your current repo or daily work. What repetitive task would benefit from a skill?

**Brainstorming prompts:**
- "What prompt do I keep typing over and over?"
- "What does our Definition of Done checklist look like - could a skill verify it?"
- "What review criteria do I apply to every PR?"
- "What's the most annoying boilerplate I write?"

**Example skill ideas** (pick one, or invent your own):

- `pr-review` - reviews a PR against your team's conventions and coding standards
- `write-tests` - generates tests following your project's specific test patterns
- `safe-refactor` - refactors code with mandatory test verification after each change
- `migration-checklist` - validates database migrations for common pitfalls
- `api-endpoint` - scaffolds a new REST endpoint following existing patterns in your codebase

**Steps:**

1. **Ask Claude to help you build it.** Use a prompt like:
   ```
   Help me build a skill called [name].
   It should: [describe what it does in one sentence]
   It should follow the patterns in our codebase.
   Create it at .claude/skills/[name]/SKILL.md
   ```

2. **Let Claude explore first.** Have Claude examine relevant files in your repo to understand existing patterns before writing the skill.

3. **Test immediately.** Once created, invoke your skill and see what happens. Does it produce what you expected?

---

## Exercise Part 2: The Ridiculous Skill (5 minutes)

Now for some fun. Build a completely absurd, pointless, delightful skill. The goal: make your sidebuddy laugh.

**Inspiration** (but be creative):

- `enterprise-shakespeare` - Converts code comments into dramatic Elizabethan prose. "Please avoid side effects here" becomes "Thou hast summoned chaos where purity was demanded, forsaking all that is pure in this module!"
- `test-the-tests` - Generates tests that test whether your tests are actually testing things. Includes an existential crisis metric. (Because 100% coverage is overrated.)
- `blame-poet` - Runs `git blame` and writes a short poem about whoever last touched the file
- `commit-therapist` - Analyzes your commit history and provides a psychological profile of your coding style

**Steps:**

1. Build it with the same `.claude/skills/<name>/SKILL.md` structure
2. Run it on your codebase
3. Share the output with your sidebuddy and enjoy the results

---

## Sharing (3 minutes)

Show your sidebuddy both skills.

**Discussion:**
- What made the useful skill actually useful?
- What would make it better?
- Would your team benefit from having this in the repo?

**Optional:** If the skill feels solid, commit it to your repo so the whole team can use it. (But no pressure—personal experiments are fine too.)

---

## Stretch Challenge (if you finish early)

- **Add supporting files**: Include a template, example output, or reference doc in the same directory
- **Add frontmatter**: Write a clear `description` field and explore `allowed-tools` to restrict Claude's capabilities
- **Try `context: fork`**: See how an isolated context changes the skill's behavior—useful for read-only analysis or sandboxed workflows

---

## Remember

Skills are team infrastructure, not personal hacks. But the best team skills start as personal experiments. Build what you need, test it, share it if it works. The skill that solves your problem today might solve three teammates' problems tomorrow.

Now, go build something useful. Then build something ridiculous.
