---
name: pull-main-ff
description: Safely update the local default branch (main/master) strictly by fast-forward from origin after a pull-request merge. Use after a worker or feature branch was merged, when the user says the local main is behind, or in the orchestrator step of the parallel-worktree cycle. Never switches branches, never creates a merge commit, blocks on uncommitted tracked changes, and stops with a MERGE-COMMIT-GATE when the incoming commits did not arrive through a pull-request merge.
user-invocable: true
---

# Pull Default Branch (Fast-Forward Only)

Bring the local default branch up to date with `origin` - and nothing else.
This is the orchestrator's step 4 in the parallel-worktree cycle and the safe
default whenever the local `main` is behind.

When this skill starts, first give the user one plain-language sentence in
the user's language, for example: "Ich hole jetzt den neuesten Stand von
GitHub auf deinen lokalen Hauptstand — nur vorwärts, ohne irgendetwas zu
verändern oder zu mischen."

## Run the bundled script only

```text
python .claude/skills/pull-main-ff/scripts/pull_main_ff.py
```

Show the user the complete script output. The script guarantees: no branch
switch, no merge commit (`--ff-only`), a hard stop on uncommitted tracked
changes (untracked files are allowed), and an honest result - it
distinguishes "already up to date" from "fast-forwarded `<sha> -> <sha>`
(N commits)".

## MERGE-COMMIT-GATE

If the output contains the marker `MERGE-COMMIT-GATE`, the incoming commits
contain **no merge commit**. The expected workflow is a worker or feature
branch merged into the default branch through a pull request - that always
creates a merge commit. A missing merge commit points to a direct push to the
default branch, a squash merge, or a rebase merge.

In that case:

1. Do **not** simply rerun the skill.
2. Show the user the listed incoming commits and explain in one plain
   sentence: work reached the default branch without going through the normal
   pull-request door, and the stop is protection, not a defect.
3. Ask **why** there is no merge commit (direct push? squash/rebase merge?
   something unexpected?).
4. Only after the user explicitly confirms, rerun deliberately:

```text
python .claude/skills/pull-main-ff/scripts/pull_main_ff.py --allow-non-merge-ff
```

## Never do

- Run any other git command or modify files in this skill.
- Switch branches or create a merge commit.
- Resolve a reported divergence yourself; explain it and let the user decide
  the next step.
