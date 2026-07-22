# Workflow State

This file is the single source of truth for CSK routing and feature-state
transitions. Skills may summarize it, but must not define a conflicting table.

## Routing precedence

Evaluate these gates in order and stop at the first applicable gate:

1. Run the `/csk-start` onboarding gate. Invalid project state blocks productive
   work; `adopt/pending` or `adopt/blocked` routes to
   `/csk-adopt-plan-scaffold`.
2. Reconcile durable `open` or `blocked` rows in `tasks/INDEX.md`. An actionable
   open continuation normally precedes new work. A blocked row remains visible
   but does not prevent unrelated work.
3. Reconcile a dirty working tree and live Git state before changing scope or
   branch.
4. Route feature work from the authoritative feature spec and
   `features/INDEX.md`. If they disagree, report drift and repair it before
   advancing.
5. When no existing feature owns the requested scope, use `/2-csk-write-spec`.

Adapter-resolved paths are authoritative. Chat memory, a task's advisory
`Expected branch`, and transported recommendations never override repository or
Git state.

## Branch lifecycle

- Documentation-phase commits from `/1-csk-init`, `/2-csk-write-spec`, and
  `/3-csk-architecture` may be proposed on the default branch; each commit still
  requires explicit user approval.
- Before productive implementation in `/4-csk-frontend` or `/5-csk-backend`,
  when the live checkout is on the default branch, ask once whether to create
  `feature/PROJ-X-<name>` (recommended) or deliberately continue on the default
  branch. Record the choice; never switch or create branches silently.
- After each verified increment, propose a checkpoint commit on the working
  branch so progress survives session loss. Committing always requires explicit
  approval; push, merge, and pull-request actions are never implied.
- A non-default branch is completed only through `/finish-branch` after QA.
  Passing checks never authorize commit, push, merge, tag, or cleanup.

## Parallel agent sessions

- One repository has exactly one orchestrating session working in the main
  checkout on the default branch. Every additional agent session gets its own
  permanent worker worktree and branch through `/create-worker-worktree` and
  opens directly in that worktree.
- A second session detected on the same working copy (session guard in
  `/csk-start`) is a warned risk mode, never a permanent setup; route it to
  `/create-worker-worktree`.
- Worker branches are protected by name (`*-workbench`) and by registration
  in `.csk/worktrees.json`; the name rule also holds while that config is not
  yet committed or not visible in the current worktree. Protected branches
  integrate through `/finish-branch` with a real merge commit and are then
  re-synced onto the new default branch - never deleted, not even on request
  inside a finish run.
- `/pull-main-ff` is the one context-sensitive sync command for both sides:
  on the default branch it fast-forwards from origin (orchestrator step); on
  a protected worker branch it re-syncs the branch onto the new default and
  fast-forward-pushes the remote ref. Unmerged worker commits block the
  re-sync fail-closed and route through `/finish-branch`. The merge-commit
  gate applies in both modes.

## Feature lifecycle

| Current status | Allowed next status | Normal next action |
|---|---|---|
| `Roadmap` | `Planned` or `Cancelled` | `/2-csk-write-spec PROJ-X` |
| `Planned` | `Architected` or `Cancelled` | `/3-csk-architecture features/PROJ-X-name.md` |
| `Architected` | `In Progress`, `Planned`, or `Cancelled` | `/4-csk-frontend` and/or `/5-csk-backend` from Tech Design |
| `In Progress` | `In Review`, `Architected`, or `Cancelled` | Continue implementation; enter QA when acceptance scope is ready |
| `In Review` | `Approved`, `In Progress`, or `Cancelled` | `/6-csk-qa`; route documented remediation to implementation |
| `Approved` | `Deployed`, `In Review`, or `Cancelled` | Finish an open feature branch, then `/7-csk-deploy` |
| `Deployed` | `In Review` | Finish an open release branch; otherwise the feature is closed |
| `Cancelled` | none | Closed; reopening requires an explicit user decision and revised spec |

Backward transitions require a reason and evidence in the owning feature spec.
`Cancelled` requires a one-line reason. `Approved` requires recorded QA evidence.
`Deployed` requires recorded release evidence and the final post-release review.

## Skill entry contracts

- `/1-csk-init`: project state passed the onboarding gate and no adopted scaffold
  is pending.
- `/2-csk-write-spec`: feature is `Roadmap`, or the user is creating a new
  feature that will receive a `Roadmap` row before specification.
- `/3-csk-architecture`: feature is `Planned`.
- `/4-csk-frontend` and `/5-csk-backend`: feature is `Architected` or
  `In Progress`. `In Review` is allowed only for remediation already documented
  by QA or review findings.
- `/6-csk-qa`: feature is `In Progress` or `In Review`. `Approved` is allowed
  only for an explicitly requested regression run and does not silently alter
  status.
- `/7-csk-deploy`: feature is `Approved`; no other status may release.
- `/finish-branch`: live Git state proves a non-default branch is in scope and
  the requested integration target is known.

If an entry contract is not met, do not force the state. Explain the exact
missing transition and route to the owning skill.

## Skill exit contracts

Every productive skill must:

1. Verify its own output and acceptance evidence before advancing status.
2. Update the feature spec and feature index together when status changes.
3. Preserve one durable task only for work that remains open or blocked, is
   expected to span a session, is explicitly deferred, or is a verified
   interruption/resume point. Do not create same-turn task churn.
4. If work occurred on a non-default branch, recommend `/finish-branch` after
   verification. Never imply that verification itself authorized commit, push,
   merge, pull-request, or cleanup actions.
5. Report the next user-controlled action. External writes require their own
   explicit authority.

## Review and release gates

- Apply `.claude/rules/loop-policy.md` before high-risk planning or implementation.
- QA findings return to the surface or core implementation skill that owns the
  affected component; keep `In Review` until remediation is verified.
- Deployment requires a readiness review before external release action.
- After the release attempt and smoke checks, run a final review on the actual
  result before writing `Deployed`, creating a release tag, or closing release
  bookkeeping.
- Failed or partial release actions remain visible as durable tasks with exact
  recovery evidence; never report a partial push, pull request, tag, artifact, or
  deployment as complete.
