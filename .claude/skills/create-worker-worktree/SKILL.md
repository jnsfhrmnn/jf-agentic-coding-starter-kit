---
name: create-worker-worktree
description: Create one permanent worker worktree so a second agent session can work in parallel without touching the main working copy. Use when a second session should open on the same repository, when the session guard reports another active session, when the user asks for parallel agents, a Codex/Claude worker, or a worktree, or when two sessions keep disturbing each other's files, index, or branch. Creates <repo>-<worker> on the protected branch <worker>-workbench from the default branch and registers it in .csk/worktrees.json.
user-invocable: true
---

# Create Worker Worktree

Give a second agent session its own permanent working folder ("worktree") next
to this repository, on its own protected branch. The worker session opens
directly in that folder; this main checkout stays on the default branch for
the orchestrating session.

When this skill starts, first give the user one or two plain-language
sentences in the user's language, for example: "Wir legen jetzt einen zweiten
Arbeitsordner für die parallele Session an — beide Sessions arbeiten dann
getrennt und können sich nichts mehr kaputt machen."

## Level check before creating anything

Parallel work has three levels (explained for beginners in
`docs/git-basics.md`). Confirm the situation first:

1. **One session at a time:** no worktree is needed. Working on the default
   branch is correct and simpler. Say so and stop.
2. **A second session on the same working copy:** warn. Both sessions share
   files, index, and HEAD; this is a risk mode, not a permanent setup. Offer
   this skill as the fix.
3. **Real parallel work:** proceed. Each additional agent gets exactly one
   permanent worker worktree and opens its session directly in it.

Ask for the worker name if not given (short lowercase name such as `codex`,
`claude2`, `worker2`; recommend the agent's product name). One worker = one
worktree = one branch, reused across many cycles - never recreate it per
task.

## Run the bundled script only

```text
python .claude/skills/create-worker-worktree/scripts/create_worker_worktree.py --worker <name>
```

The script owns all safety checks: default branch only, clean tracked tree,
no existing ref/folder/registered worktree, verification of the created
worktree, and registration in `.csk/worktrees.json` (worker entry plus
`protectedBranches`). Its only mutating git command is `git worktree add`.

**On failure:** show the script's message completely, explain in at most two
plain sentences what the user must fix manually, and stop. Do not run any
other git commands, do not retry with force, and do not clean up by hand.

## On success: hand the user the worker guide

Read the JSON result between `WORKER_WORKTREE_RESULT_BEGIN/END` and present,
in the user's language:

1. **Open the worker session in the new folder** - the exact path
   (`workerWorktreePath`). The whole trick is that the worker session opens
   directly in its worktree, never in this folder.
2. **Division of labour:** this checkout keeps the default branch
   (orchestrator). The worker works and commits only on `workerBranch` inside
   its worktree.
3. **The recurring cycle** (also in `docs/git-basics.md`):
   1. Create the worktree (done - once).
   2. Work in parallel.
   3. Worker integrates via `/finish-branch`: pull request with a real merge
      commit; the protected branch is re-synced, never deleted.
   4. Orchestrator updates the default branch with `/pull-main-ff`.
   5. Continue at 2 - worktree and branch persist.
4. **Copy local-only files if needed:** gitignored files such as `.env.local`
   are not part of the worktree. Tell the user which ones exist and let them
   copy what the worker genuinely needs - never copy secrets automatically.
5. **Propose committing `.csk/worktrees.json`:** until that commit reaches the
   default branch, other checkouts (including the new worker worktree) cannot
   see the registration; only the name rule (`*-workbench` is always
   protected) covers the gap. Show the exact path and ask for commit approval
   with one plain sentence; declining is safe and leaves the name rule in
   force.

## Never do

- Switch branches, pull, fetch, commit, push, stash, or reset in this skill.
- Delete or prune worktrees.
- Create the worktree when the level check says one session is enough.
- Remove the branch protection that the script recorded; removing a worker
  is an explicit, informed user decision (edit `.csk/worktrees.json`, remove
  the worktree deliberately) - never a side effect.
