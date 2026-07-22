---
name: pull-main-ff
description: Context-sensitive safe sync with origin - one command for both sides of the worker-worktree cycle. On the default branch (main/master) it fast-forwards from origin; on a protected worker branch (*-workbench or .csk/worktrees.json) it re-syncs the branch onto the new default and fast-forward-pushes the remote ref, restoring it after host auto-delete. Use after a pull-request merge, when the user says their branch or main is behind, or as the sync step of the parallel-worktree cycle (both sides). Never switches branches, never creates a merge commit, blocks on uncommitted tracked changes and on unmerged worker commits, and stops with a MERGE-COMMIT-GATE when incoming commits bypassed the pull-request door.
user-invocable: true
---

# Sync With Origin (Fast-Forward Only, Context-Sensitive)

One command for both sides: the user intention is always "bring me safely up
to date with origin" - the script detects the context itself and picks the
safe mechanics. A command that recognizes its context beats two commands the
user must choose between.

When this skill starts, first give the user one plain-language sentence in
the user's language, for example: "Egal wo du stehst — dieses eine Kommando
bringt dich sicher auf den neuesten Stand. Wenn es stoppt, sagt es dir warum
und was als Nächstes zu tun ist."

## Run the bundled script only

```text
python .claude/skills/pull-main-ff/scripts/pull_main_ff.py
```

Show the user the complete script output. The script detects the mode from
the current branch:

| Context | Behaviour |
|---|---|
| Default branch (`main`/`master`) | Mode A: fast-forward the default branch from origin - the orchestrator step of the cycle. |
| Protected worker branch (`*-workbench` or listed in `.csk/worktrees.json`) | Mode B: re-sync - `merge --ff-only` onto the new `origin/<base>`, then a fast-forward push so the remote ref follows (also restores a remote ref the host auto-deleted after the merge). |
| Worker branch with local commits not yet on origin | Fail-closed stop with guidance: integrate through a pull request first (`/finish-branch`), then re-sync. No silent merge. |
| Any other branch | Stop without changes. |

Both modes guarantee: no branch switch, no merge commit, a hard stop on
uncommitted tracked changes (untracked files are allowed), and an honest
result - "already up to date" is distinguished from "fast-forwarded
`<sha> -> <sha>` (N commits)" and from "local branch is ahead (unpushed
work)".

## MERGE-COMMIT-GATE (applies in both modes)

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
- Work around the unmerged-commits stop with a manual merge or push; route
  that work through `/finish-branch`.
- Resolve a reported divergence yourself; explain it and let the user decide
  the next step.
