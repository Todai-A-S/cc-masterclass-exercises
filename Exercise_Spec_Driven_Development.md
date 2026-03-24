# Exercise: Spec-Driven Development

In this exercise, you work in pairs to build a feature, bugfix, or refactoring from your backlog using **Spec-Driven Development** — a structured approach where a mini-specification drives the implementation. The goal is to experience the difference between "prompt and hope" and a method where requirements are clear *before* code is written.

## Time: approx. 70 minutes

| Time | Phase | Activity |
|---|---|---|
| 0:00–0:05 | Setup | Choose task from backlog |
| 0:05–0:25 | Spec | Write mini-spec with Claude |
| 0:25–0:35 | Review | Pair-review of spec |
| 0:35–1:00 | Implement | Implement with skills/commands |
| 1:00–1:10 | Retrospective | What did the spec give us? |

---

## 1. Choose Your Task

### Do you have a Bring-Your-Own-Task?

Pick a task from your actual backlog — something you genuinely need to do. This gives the exercise the most value because:

- You know the context and can validate Claude's understanding
- The result is usable afterwards (not throwaway code)
- You experience the workflow on something realistic

Good candidates: a new feature, a bugfix, a refactoring, adding tests to an untested module, a migration.

### No prepared task? Use one of these:

**Option A — PR Review Skill:** Build a `/review-pr` skill that automatically reviews a PR. The spec defines: what to review (architecture, tests, naming), output format, when it should flag issues.

**Option B — Test Generator:** Build a `/write-tests` skill for a specific module in your codebase. The spec defines: test strategy, coverage goals, edge cases to cover.

**Option C — Deploy Checklist:** Build a `/pre-deploy` skill that checks everything before deploy. The spec defines: what to verify, in what order, what blocks deploy.

---

## 2. Write Mini-Spec (20 min)

**Purpose:** Define *what* you're building and *when it's done* — before writing a single line of code.

### Spec template

Ask Claude to help you fill in this structure:

```
Help me write a mini-spec for the following task: [describe the task]

Use this format:

## Problem
What problem are we solving? Why does it matter?

## Constraints
- What must we work within? (existing patterns, API contracts, performance requirements)
- What is explicitly out-of-scope?

## Acceptance Criteria
- [ ] [Concrete, testable thing 1]
- [ ] [Concrete, testable thing 2]
- [ ] [Concrete, testable thing 3]

## Design Notes
- Which files need to change?
- Which patterns should be followed?
- What risks do we see?

## Implementation Plan
- Phase 1: [what]
- Phase 2: [what]
- Phase 3: [what]

Write the spec to specs/[task-name]-spec.md
```

### Tips for good spec writing:

- **Acceptance Criteria are the most important part.** If you can't describe when it's *done*, you don't know what you're building.
- **Use Claude's codebase knowledge.** Ask it to check existing patterns: *"How do we do this elsewhere in the codebase?"*
- **Be explicit about out-of-scope.** This prevents scope creep during implementation.
- **Keep it short.** A good spec is 1-2 pages, not 10.

---

## 3. Pair-Review the Spec (10 min)

Swap specs with your partner and review each other's. Focus on:

- **Are acceptance criteria testable?** Can you write a test that verifies each point?
- **Is the plan realistic?** Can you see yourself executing it?
- **Is anything missing?** Are there edge cases or dependencies that were overlooked?
- **Is scope appropriate?** Too big → split up. Too small → expand.

Give concrete feedback and adjust the spec.

---

## 4. Implement with Claude Code (25 min)

**Purpose:** Execute the spec step by step using the skills you've built (or will build).

### Use the spec as your steering tool:

```
Read specs/[task-name]-spec.md.

Implement phase 1 from the implementation plan.
Follow the constraints and patterns described in the spec.
Stop after phase 1 and show me the changes.
```

### Workflow for each phase:

1. **Implement** — Let Claude execute the specific phase
2. **Verify** — Run tests, use `/diff` to inspect changes
3. **Check acceptance criteria** — Can you check off one or more items?
4. **Clear context** — `/compact` before the next phase

### Use your skills (if you've already built them in session 2):

```
/create_plan          → Create detailed plan based on spec
/implement_step       → Implement one step
/write_tests          → Generate tests for changed code
/pr_ready_check       → Check if everything meets DoD
```

### If you don't have skills yet:

Use the manual workflow — the point is the same: the spec steers, Claude executes, you validate.

### Key principles:

- **The spec is the contract.** If Claude suggests something that deviates from the spec, stop and discuss.
- **Acceptance criteria are your checklist.** Check them off as you go.
- **One step at a time.** Verify after each step.
- **If the spec turns out to be wrong:** That's OK — update the spec and continue. That's better than ignoring it.

---

## 5. Retrospective (10 min)

### Discuss in your pair:

**What did the spec give us?**
- Where did the spec save time vs. "just prompting"?
- Where did acceptance criteria prevent mistakes?
- Where did the pair-review catch problems?

**Where did the spec fail?**
- Was there something the spec didn't anticipate?
- Was it too detailed (overspecified) or too vague?
- Were constraints realistic?

**Spec as a team tool:**
- Could this spec help another developer understand the task?
- Could it be reused as a template for similar tasks?
- What should go into your spec template as standard?

---

## Sharing in Plenary

Prepare to share with the group:

1. **"The spec saved us time because..."** — the most concrete example
2. **"The spec didn't survive contact with reality when..."** — where it broke
3. **"Next time we would..."** — what you'd do differently

---

## Remember

> Spec-Driven Development is not bureaucracy — it's **an investment in clarity**. A good spec taking 20 minutes saves hours of debugging and refactoring. And most importantly: it enables Claude to work *with* your intentions, not *in spite of* them. You are the architect. The spec is the blueprint. Claude is the craftsman.
