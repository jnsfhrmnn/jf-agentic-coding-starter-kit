---
name: finish-branch
description: Safely complete a feature, fix, or release branch after its work is verified. Use when productive work on a non-default Git branch is ready to be intentionally committed, pushed, reviewed, merged, and optionally cleaned up; when the user asks to finish, close, merge, publish, or wrap up a branch; or when a CSK skill exits with verified branch work. Handles dirty trees, detached HEAD, worktrees, base drift, checks, pull requests, partial failures, and task closure without force-pushing or silently deleting branches.
---

# Finish Branch

Complete one Git branch with evidence and explicit action boundaries. Start
read-only. Never equate "tests passed" with permission to commit, push, merge,
open a pull request, tag, or delete a branch.

When this skill starts, first give the user one or two plain-language sentences
in the user's language explaining the step, for example: "Wir schließen jetzt
den Arbeits-Branch kontrolliert ab — committen, prüfen, zusammenführen — damit
nichts Ungeprüftes auf dem Hauptstand landet."

## Entry contract

- The repository onboarding gate passes.
- Live Git state proves which branch and worktree own the requested changes.
- The integration target is known or can be resolved unambiguously.
- Product/feature work has passed the applicable implementation, review, and QA
  gates. If not, return to the owning skill instead of bypassing it.

This skill is the normal exit after verified work on a non-default branch. A CSK
skill should recommend it automatically, but must not execute its mutations
without authority.

## Phase 1: Inspect without mutation

Read:

1. `git status --short --branch` and `git status --porcelain=v2`;
2. current branch or detached-HEAD state;
3. staged, unstaged, and untracked paths plus `git diff` and `git diff --cached`;
4. remotes and their URLs, upstream tracking, and the remote default branch;
5. linked worktrees with `git worktree list --porcelain`;
6. merge, rebase, cherry-pick, revert, bisect, or sequencer state;
7. commits unique to the branch and its merge base with the proposed target;
8. repository instructions, owning feature/task records, and required checks.

Classify every changed path as in-scope, unrelated user work, generated output,
secret/sensitive, or uncertain. Never stage unknown or unrelated paths.

## Phase 2: Resolve blockers and strategy

Stop before mutation when any of these applies:

- An unresolved Git operation is active. Continue or abort it only after showing
  the exact state and obtaining authority for that operation.
- HEAD is detached. Identify the containing branch or propose a named rescue
  branch. Creating it requires approval; never commit new work while detached.
- The current branch is the default branch. There is no branch to close; offer a
  scoped commit/publish workflow only if the user requests it.
- Target branch is ambiguous, absent, or checked out in another worktree whose
  state has not been inspected.
- In-scope and unrelated changes cannot be safely separated.
- Secrets, credentials, oversized artifacts, conflict markers, or validation
  failures are present.
- The feature/task status does not satisfy `.claude/rules/workflow-state.md`.

Resolve the default branch from `origin/HEAD`, repository configuration, or clear
local convention. Ask when evidence conflicts. A remote named `upstream` is a
template/source remote, never a publish target for project changes. If no safe
`origin` exists, use a local integration strategy or explain that publication is
unavailable.

Choose and state one strategy:

- existing repository pull-request workflow (preferred when configured);
- push branch to `origin`, open/reuse a pull request, wait for required checks,
  then merge;
- local integration into the target branch when no hosting workflow exists or
  the user explicitly chooses it;
- commit-only handoff when integration is intentionally deferred.

Do not rewrite published history. Never force-push. Do not rebase, squash,
fast-forward, or create a merge commit merely by preference; follow repository
policy or ask the user when the choice materially affects history.

## Phase 3: Verify before proposing mutation

Run the exact project-native format, lint, type, unit, integration, build, and
acceptance checks required by architecture and feature scope. Review the final
diff and verify that generated artifacts and documentation are current.

If the target may have advanced, propose a fetch before claiming the branch is
current. Fetch is a network action and requires authority. After current target
state is available, determine ahead/behind/diverged and test the actual
integration result where practical. Base drift, conflicts, timeouts, or failing
checks block completion and remain durable through `/csk-start` if not resolved
in the current session.

## Phase 4: Obtain explicit action authority

Present a compact execution proposal containing:

- branch and target;
- exact paths to commit and proposed commit message;
- verification evidence;
- remote/PR/merge strategy;
- whether local and remote cleanup are proposed.

Ask one consolidated approval for the exact commit, push, pull-request, and merge
actions in scope. Treat local-branch deletion and remote-branch deletion as two
separate optional cleanup targets; neither is implied by merge approval. If the
user authorizes only part, perform only that part and report the remaining state.

## Phase 5: Execute incrementally and verify each boundary

1. Stage only approved paths and reread the staged diff.
2. Commit with the repository convention; capture the commit SHA.
3. Rerun any checks whose result can change after formatting or generated output.
4. Push only the named branch to the approved `origin` target; verify remote
   tracking and the pushed SHA.
5. Create or reuse one pull request when that is the chosen strategy. Record its
   URL and actual state.
6. Wait for required checks with a bounded timeout: default 15 minutes, or the
   repository's documented CI budget when one exists. On expiry, report the
   actual check state and stop; a timeout or unavailable check is not success.
7. Merge only after required checks and review gates pass; verify the merge SHA
   is reachable from the target branch.
8. For local integration, inspect the target worktree, update it safely, perform
   the approved merge strategy, rerun integration checks, and verify reachability.
9. Delete only explicitly approved branch targets and only after proving the
   integration contains the finished commit.

After every external step, inspect actual state before continuing. Do not assume
that a successful command means the hosting service completed the operation.

## Failure matrix

- **Commit fails:** leave paths and index visible; do not push.
- **Push partially succeeds or tracking is unclear:** query local/remote refs,
  report exact SHAs, and do not duplicate the push blindly.
- **Pull request creation fails:** preserve the pushed branch and provide its
  recovery action; do not report a pull request URL unless verified.
- **Pull request is closed but unmerged:** do not delete branches or close the
  task; ask whether to reopen, replace, or defer.
- **Checks fail or time out:** keep the branch open and route findings to the
  owning implementation/QA skill.
- **Target advances:** recompute merge base and rerun affected checks.
- **Merge conflict:** leave a clearly reported operation state; resolve or abort
  only with authority, never guess conflict intent.
- **Merge succeeds but cleanup fails:** report integration as complete and
  cleanup as incomplete; never retry destructive deletion broadly.
- **Multiple worktrees:** operate in the worktree that owns each checked-out
  branch; never delete a branch still checked out anywhere.
- **Network or host unavailable:** preserve a commit-only handoff and one durable
  recovery task when authorized.

## Close state with evidence

After integration, verify:

- working trees involved are understood and no user changes were lost;
- the finished commit is reachable from the target;
- remote branch, pull request, checks, and cleanup match the approved strategy;
- feature/index state remains consistent;
- any owning task can be closed with typed evidence such as `commit:<sha>` or
  `url:<pull-request>` through `/csk-start`.

Do not close a task for commit-only or pushed-only work when merge/integration was
its acceptance condition. Persist any incomplete step as one durable task with
the exact next action and blocker.

## Completion report

Report branch, target, committed SHA, pushed SHA, pull-request URL/state, check
result, integration SHA, local/remote cleanup state, task/feature bookkeeping,
and any remaining risk. Use `not requested`, `not applicable`, or `incomplete`
instead of implying an action happened.
