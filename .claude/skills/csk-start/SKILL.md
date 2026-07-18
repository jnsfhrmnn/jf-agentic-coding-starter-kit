---
name: csk-start
description: Standalone CSK repository-start and resume routine. Use on every repository open, after context loss, when the user asks what is open or says resume/continue/weiter, when first-use adoption must be classified, or whenever unfinished work must survive into a later session. Manages tracked project onboarding state in .csk/project-state.json and durable local work in tasks/INDEX.md entirely inside the current repository.
---

# CSK Start

Run a local, read-first start routine. Repository files, not chat memory, decide
what can safely continue. `.csk/project-state.json` is the source of truth for
project-wide onboarding; `tasks/INDEX.md` is the source of truth for immediate
durable work.

## Supported operations

- `/csk-start` — validate onboarding, inspect the repository, and show the board.
- `/csk-start --quick` — show the board without deeper feature reconciliation.
- `/csk-start --recheck-adoption` — explicitly repeat the repository inventory.
- `/csk-start --add "<task>"` — add or update durable open work.
- `/csk-start --block TASK-NNN --reason "<reason>"` — record a blocker.
- `/csk-start --close TASK-NNN --evidence "<evidence>" [--evidence-record <path>]` — close verified work.

Interpret equivalent natural language without requiring exact flag syntax. Do
not start implementation merely because the board was shown. If the user says
`weiter`, `continue`, `go`, or equivalent after the board, continue with the
recommended item and its applicable skill.

## State boundaries

- `.csk/project-state.json` owns the repository role and adoption decision.
- `tasks/INDEX.md` owns only immediate `open` and `blocked` durable work.
- A feature spec owns feature scope, status, decisions, and acceptance evidence.
- `features/INDEX.md` is a feature overview, not an open-task queue.
- `Expected branch` in a task row is advisory intent. Live Git state is
  authoritative and must be checked before work or branch completion.
- Do not copy feature status or full specifications into the task index.
- Completed work has no open-task row. Preserve evidence in its owning source of
  truth, a commit, a test result, or another local artifact. Git is the audit
  trail; create no task archive.

The first-use decision is project-wide, not checkout-local. It becomes
project-wide only when the commit containing `.csk/project-state.json` is
reachable from `origin/<default-branch>`. Until then, report its actual scope.
Never push this state to an `upstream` remote.

## Deterministic helper

Use `scripts/csk_start.py` for mechanical validation and mutation. Python 3.10+
is an explicit CSK tooling runtime, independent of the product stack. Detect it
in this order: `python3`, `python`, then Windows `py -3`. If no compatible
interpreter exists, keep the routine read-only, explain the missing tooling, and
do not hand-edit onboarding or task state.

Prefer the bundled launcher so detection and missing-runtime behavior stay
consistent:

```text
PowerShell: powershell -File scripts/csk-start.ps1 <area> <operation> ...
POSIX:      sh scripts/csk-start.sh <area> <operation> ...
```

Important commands:

```text
state check
state check-template-distribution [--snapshot HEAD|index]
state inventory
state decide --mode greenfield|adopt
state recheck
state adoption-complete --coverage-report .csk/adoption-coverage.json
state adoption-block --reason <reason>
tasks check
tasks list
tasks add ...
tasks update TASK-NNN ...
tasks block TASK-NNN --reason ...
tasks close TASK-NNN --evidence <typed-evidence>
```

Run the helper from the repository root and use `--repo <path>` when needed.
The helper owns syntax, invariants, locking, compare-and-swap checks, and atomic
writes. The LLM still owns semantic decisions: whether code or planning evidence
should be adopted, whether tasks are duplicates, which skill applies, and what
the safest next action is.

`state check-template-distribution` is a maintainer release gate, not a normal
project-start command. It reads `HEAD` by default and fails unless that Git
snapshot contains the exact initial `template/pending/not-assessed` state. Use
the explicit `--snapshot index` only as a pre-commit check of already staged
content. The working-tree file alone can never pass this distribution gate.

## Start routine

### 1. Discover capabilities

Before choosing an action:

1. Inspect the skills and tools exposed by the current runtime.
2. Inventory repository skills under `.claude/skills/*/SKILL.md` and Codex
   proxies under `.codex/skills/*/SKILL.md`.
3. Read every applicable skill before using it. Explicitly requested skills are
   mandatory.
4. Use semantic LLM judgment to choose relevant skills; do not route by keyword
   or regex alone.

Use repository copies of CSK skills. Never install or copy them into a
user-global Claude or Codex directory. Already available global runtime skills
may supplement the workflow but are not an installation target.

### 2. Enforce the first-use gate

Run `state check` before reading or creating tasks.

- Missing, malformed, contradictory, or unsupported state fails closed. Report
  the exact defect; never infer greenfield state from absence or damage.
- When state is `pending/not-assessed` (initial template or explicit recheck),
  run `state inventory`, review
  its candidate files semantically, then ask exactly one bounded question. Show
  the evidence and recommended mode, explain both routes, and offer these exact
  outcomes: `adopt and store`, `greenfield and store`, or `do not store yet`.
  Adoption routes to `csk-adopt-plan-scaffold`; greenfield routes to normal
  initialization. This single answer makes both the classification and its
  permission to write `.csk/project-state.json` unambiguous.
- The answer authorizes only that state write and the stated routing. It never
  authorizes a commit, push, merge, dependency installation, or implementation.
- After consent, run `state decide --mode adopt|greenfield`; do not hand-edit the
  state. The first decision changes `repository_role` from `template` to
  `project`, so the prompt does not recur in later clones after the state commit
  reaches the default branch.
- Read `distribution.origin_role`. `source-template` is never a project publish
  target. `missing`, `unconfirmed`, or `unconfirmed-template` requires the user
  to identify or create their own project remote before any push. Recommend
  renaming a cloned starter-kit `origin` to `upstream` and adding the project as
  `origin`, but perform remote changes only with explicit authority.
- After the state write, offer a selective handoff: commit the approved
  `.csk/project-state.json` change (and no unrelated paths), then push that commit
  only to the confirmed project `origin` default branch. Commit and push each
  require separate explicit authority. If the state lives on a feature branch,
  route its later integration through `/finish-branch`.
- For `project/adopt/pending`, resume `csk-adopt-plan-scaffold` without asking the
  first-use question again.
- For `project/adopt/blocked`, surface the recorded blocker and propose its next
  unblock action.
- For `project/adopt/complete`, verify the recorded scaffold evidence. If it has
  drifted or disappeared, use `state adoption-block`, create/update one durable
  repair task, and do not repeat the initial interview.
- For `project/greenfield/not-applicable`, continue normally.

Only explicit `--recheck-adoption` or an equivalent user request may run
`state recheck` and reopen classification. Always report whether the current
state is uncommitted, branch/local, or project-wide according to `state check`.

### 3. Read local work state

Read, in this order:

1. `tasks/INDEX.md` through EOF.
2. `git status --short --branch`, the current branch, worktree context, and
   repository operation state when this is a Git repository.
3. `features/INDEX.md` unless `--quick` was requested.
4. Only feature specs and source-of-truth files referenced by open task rows.

Do not contact a network service or inspect another repository.

### 4. Validate mechanically

Run `tasks check`. It verifies the exact table schema, the unique next-ID marker,
IDs, allowed states and priorities, required cells, dates, advisory branch
format, resume-skill format, and referenced paths. On failure, report the exact
defect and propose the smallest repair. Never silently discard or renumber tasks.

### 5. Reconcile semantically

Use LLM context judgment to:

- group related tasks by feature or subject;
- identify semantic duplicates despite different wording;
- detect drift between a task and its owning feature/specification;
- determine which available skill best handles each next action;
- validate `Expected branch` against live Git state;
- recommend one next item based on priority, blockers, context, dependencies,
  value, and switching cost.

A dirty working tree is unowned current work until understood. Surface changed
paths before recommending a different workflow. Do not infer that changes are
safe, complete, or related to an indexed task. File state beats remembered or
conversational state. Report feature/spec conflicts as drift; do not rewrite
either side during the read-only start routine.

### 6. Present the board

Before the board, give the user one plain-language sentence in the user's
language, for example: "Bevor wir arbeiten, prüfe ich den gespeicherten
Projektstand und die offenen Aufgaben, damit wir genau dort weitermachen, wo
die letzte Session aufgehört hat."

Use this compact shape:

```text
CSK START
Repository: <path>
Onboarding: <mode/status> | Scope: uncommitted/local/project-wide
Origin: <URL or missing> | Role: project/source-template/unconfirmed
Branch: <branch or n/a> | Working tree: clean/dirty
Open: <n> | Blocked: <n>

[1] TASK-NNN [priority/status] <task>
    Related: <feature/path/none>
    Expected branch: <branch/none>
    Next: <next action>
    Resume skill: </skill or direct>

Recommendation: <one item and why>
```

After the board, ask one concise question: continue the recommendation, choose a
numbered item, maintain the index, or stop.

If no task is open:

- With a dirty working tree, recommend inspecting and attributing those changes
  first. Offer one durable task only if the work will survive this turn.
- With a clean working tree, derive the normal next action from
  `.claude/rules/workflow-state.md` through `/csk-help`; do not invent work.

## Task mutations

Mutate the index only when the user explicitly requests task maintenance or the
current repository-change task already authorizes continuity for unfinished work
inside that same scope. A newly discovered, deferred, or out-of-scope follow-up
does not inherit that authority: show all proposed rows together as
`PENDING-AUTH` and ask once whether they should be stored. The read-only start
routine never grants mutation authority.

Use the helper for every mutation. It acquires the repository-local lock, reads
and validates current state, checks the input digest, writes atomically, rereads,
and verifies. Never bypass a lock, digest mismatch, validation error, or symlink
escape with a hand edit.

### Add or update

1. Search semantically for an existing task before invoking the helper.
2. Update the existing row instead of adding a duplicate.
3. Otherwise allocate the helper-managed next ID and add one concise row.
4. Record `Related`, advisory `Expected branch`, runtime-neutral `Resume skill`,
   and an executable next action.

Create a task only when the work is still open or blocked, is expected to span a
session, is explicitly deferred, or is a verified interruption/resume point. Do
not create and close rows for ordinary work expected to finish in the same turn.

### Block

Keep the row, set status to `blocked`, and record both the concrete blocker and
the next action that could remove it. Never mark uncertainty as completion.

### Close

1. Verify the outcome against the owning file, acceptance criteria, test,
   artifact, commit, or explicit user decision.
2. Supply typed evidence such as `commit:<sha>`, `file:<path>`, `test:<name>`,
   `url:<endpoint>`, or `artifact:<path>` to the helper.
3. Commit, file, and artifact evidence must resolve locally. Test and URL
   evidence also require `--evidence-record <relative-path>` pointing to a local
   proof file that contains the test name or URL. Store new proof files under
   `.csk/evidence/<TASK-ID>-<short-name>.md` unless an owning source of truth
   already holds the evidence.
4. Preserve evidence in the owning local source of truth when one exists.
5. Let the helper remove the row; create no archive.
6. Check that no dependent open task was orphaned.

If evidence is missing, keep the task open or blocked and report the gap.

## End-of-work continuity

When repository writes are authorized, before ending non-trivial work:

1. Identify unfinished, deferred, blocked, or interrupted work.
2. Ensure every durable follow-up has exactly one task row.
3. Remove completed rows only with evidence.
4. Leave the index unchanged when no durable follow-up exists.

For discovered or out-of-scope work, present exact proposed rows as
`PENDING-AUTH`, state that they are not durably conserved, and request one
consolidated authorization. Never claim chat-only work is durable.

## Safety

- Default start mode is read-only.
- Do not execute multiple tasks automatically.
- Do not modify feature status during task maintenance.
- Do not hide a dirty working tree or unrelated changes.
- Do not create cross-repository workflow state, external task stores, transport
  directories, or task archives.
- On repeated tool failure, report the blocker and stop instead of retrying in a
  loop.
