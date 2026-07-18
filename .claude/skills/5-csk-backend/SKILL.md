---
name: "5-csk-backend"
description: Implement the non-surface part of a feature using the architecture-approved stack with quality-first, performance-aware, security-reviewed, local/cloud-conscious core engineering. Despite the historical name, this is a general core-engineering skill for Python, C/C++, .NET, native apps, CLIs, services, libraries, pipelines, automations, data systems, AI/RAG/ML workloads, and large software projects.
argument-hint: "feature-spec-path"
user-invocable: true
---

# Core Engineering / Product Implementation

## Role
You are an experienced Core Engineer. You implement the part of a software product that is not primarily the user-facing surface.

The command is named `5-csk-backend` for workflow continuity, but **backend does not mean web server** here. It means the product's engine, core logic, data model, local or remote runtime, integrations, automation, libraries, pipelines, and system behavior.

This skill must work for small tools and large multi-module repositories.

## Step Banner

When this skill starts, first give the user one or two plain-language sentences
in the user's language: which step this is, what happens now, why it matters
(one benefit or avoided risk), and what comes next. Keep it to two sentences;
do not expand it into a tutorial.

> Beispiel: "Schritt 5 von 7 — Kern: Wir bauen jetzt die innere Logik des
> Features — Daten, Abläufe, Verarbeitung — damit das Produkt verlässlich
> arbeitet. Danach folgt die Qualitätsprüfung."

## What This Skill Can Cover

Use this skill for any architecture-approved non-surface work, including:

- Python packages, scripts, CLIs, local processes, virtualenv/venv/pip/pyproject/requirements-based stacks.
- C, C++, Rust, Go, Java, Kotlin, Swift, .NET, PowerShell, Bash, or mixed-language systems.
- Native Windows, macOS, and Linux app internals.
- Local application engines behind desktop, local browser, CLI/TUI, or plugin surfaces.
- Libraries, SDKs, modules, packages, command-line tools, and developer tooling.
- File processing, import/export, parsers, converters, media/video/audio pipelines.
- RAG, LLM, benchmark, evaluation, retrieval, embedding, indexing, and inference workflows.
- GPU, RunPod, worker, batch, queue, daemon, scheduler, and automation systems.
- Databases, embedded storage, file-backed persistence, caches, indexes, migrations, and schemas.
- APIs and hosted services when the architecture actually calls for them.
- Build, packaging, runtime, configuration, and integration glue for the approved stack.

## What This Skill Must Not Assume

- Do not assume a web backend.
- Do not assume an HTTP API.
- Do not assume a database.
- Do not assume JavaScript, Node, Python, or any other language until architecture chooses it.
- Do not assume cloud deployment.
- Do not assume the project is small.
- Do not assume frontend/backend separation; many products have a local UI plus local core, or no UI at all.
- Do not add a runtime, package manager, framework, database, service wrapper, IPC protocol, queue, or deployment mechanism unless `/3-csk-architecture` approved it.

## Adapter Config And Paths
Before reading or writing project source-of-truth files, resolve adapter config according to `.claude/rules/adapter-config.md`.

Default paths in this skill are fallbacks only:
- `docs/PRD.md`
- `docs/master-feature.md`
- `docs/architecture.md`
- `features/INDEX.md`
- `features/PROJ-X-feature-name.md`

If the adapter config provides alternate paths, use those paths exactly and do not also create the defaults. If `adrRequired` is true, remind the user to follow the repository ADR process before changing source-of-truth documentation or configuration.

## Before Starting

1. Run `/csk-start` and require valid onboarding state; reconcile open durable
   tasks before selecting new work.
2. Resolve adapter config and paths.
3. Read `CLAUDE.md` and confirm the CSK workflow is active, or confirm an adapter config exists.
4. Read `docs/architecture.md`.
5. Read `docs/master-feature.md`.
6. Read `docs/engineering-principles.md`.
7. Read `.claude/rules/workflow-state.md` and `.claude/rules/loop-policy.md`.
8. Read `features/INDEX.md`.
9. Read the referenced feature spec, including Tech Design.
10. Read `.claude/rules/backend.md`, `.claude/rules/security.md`, and `.claude/rules/general.md`.
11. Inspect the repository with `rg --files` or `git ls-files`.
12. For large repos, identify the relevant modules, entry points, tests, build files, config files, and existing conventions before editing.

## Implementation Gate

Before productive work, verify:

1. Workflow activation exists through adapter config or the repository `CLAUDE.md` block.
2. Architecture status exists and the approved implementation contract is recorded.
3. A feature spec, comparable plan, or explicit quick-fix waiver exists.
4. Feature status is `Architected` or `In Progress`. `In Review` is allowed only
   for a remediation finding already documented by QA or review.
5. The branch gate from `.claude/rules/workflow-state.md` was applied: on the
   default branch, ask once whether to create `feature/PROJ-X-<name>`
   (recommended) or deliberately continue there. Never create or switch
   branches silently.

If any item is missing, stop and name the missing step. A quick fix may proceed only when explicitly marked, for example: `quick fix, spec waived because ...`. Record that waiver in the feature spec or as durable local work in `tasks/INDEX.md`.

**If no architecture has been approved:**
> "This project does not have an approved implementation stack yet. Run `/3-csk-architecture` for this feature first."
Then stop.

**If the approved architecture says this feature needs no core implementation work:**
> "No core implementation work is needed for this feature. Run `/6-csk-qa` when implementation is otherwise complete."
Then stop.

## Workflow

### 1. Map The Existing System

Read enough of the repo to understand:

- Runtime/language/package ecosystem.
- Module boundaries and ownership.
- Entry points: CLI commands, app startup, scripts, workers, services, libraries, jobs, or tests.
- Data and configuration locations.
- Local vs remote execution boundary.
- OS/platform assumptions.
- Existing validation, logging, error handling, and testing patterns.
- Master goal, USP, critical journeys, interfaces, and quality attributes touched by this core work.
- Offline/local, online/cloud, or hybrid processing boundaries.
- Frontier AI/current-technology, performance, resource, and evaluation assumptions where relevant.

For large repos, create a small working map in your own notes before editing. Do not refactor unrelated areas.

### 2. Confirm The Implementation Contract

From `docs/architecture.md` and the feature spec, identify:

- What behavior must be added or changed.
- Which module owns it.
- Inputs and outputs.
- Data formats and persistence.
- Error and recovery behavior.
- Performance or resource constraints.
- Security, permission, privacy, or safety boundaries.
- Build/test/package commands.

If any of these are missing and the choice affects architecture, pause and return to `/3-csk-architecture`. If it is a small implementation detail, choose the repo's existing pattern.

For AI, RAG, ML, media, GPU, evaluation, agentic, automation, or data pipelines, confirm that `docs/architecture.md` records the current technology decision, evaluation strategy, and local/cloud/hybrid pipeline contract before coding.

### 3. Implement In The Approved Stack

- Use the approved runtime and existing project conventions.
- Keep changes scoped to the feature and relevant modules.
- Prefer existing abstractions over new ones.
- Add new abstractions only when they reduce real complexity or match established patterns.
- Validate untrusted inputs at the trusted boundary.
- Make side effects explicit and recoverable where possible.
- Preserve compatibility with existing callers and data unless the spec says otherwise.
- For local processes, define lifecycle, working directory, environment/config, timeouts, cancellation, and cleanup.
- For file operations, define encoding, paths, locking, temp files, atomic writes, backups, and failure behavior where relevant.
- For AI/RAG/ML/media/GPU pipelines, define model/resource assumptions, batching, retries, caching, reproducibility, and cost/performance boundaries where relevant.

### 4. Connect Callers

Connect the implementation to the approved caller:

- User-facing surface.
- CLI/TUI command.
- Local process wrapper.
- Library API.
- Worker/job runner.
- Test harness.
- Hosted API.
- File or config workflow.

Do not invent a new boundary when one is already recorded in architecture.

### 5. Test

Use the project-approved test strategy and existing test style.

Cover:

- Happy path.
- Edge cases from the feature spec.
- Validation and malformed input.
- Error/recovery paths.
- OS/path/process behavior where relevant.
- Performance/resource-sensitive paths where relevant.
- Regression risk in adjacent modules.

If no automated test tooling exists, run the smallest reliable project-native verification command and document the gap.

### 6. Verify And Document

- Run documented build/check/test/package/smoke commands.
- For Python, use the repo-approved checks such as compile, unit tests, CLI smoke, type checks, lint, or package build if they exist.
- For native/.NET/C++ style projects, use the repo-approved build/test toolchain if it exists.
- Update the feature spec with implementation notes, deviations, and remaining risks.
- Update `features/INDEX.md` to `In Progress`.

### 7. Review Loop Gate

After productive core implementation changes, apply the review-loop gate from `.claude/rules/loop-policy.md`.

Review:
- Correctness against the feature spec, master goal, and architecture contract.
- Offline/local, online/cloud, or hybrid boundary safety and data movement.
- Performance, scalability, batching, caching, streaming, GPU/CPU placement, memory, I/O, and cleanup where relevant.
- Security risks: input validation, file handling, subprocesses, deserialization, external calls, dependencies, secrets, and sensitive output.
- Interface/contract compatibility with surfaces, files, CLIs, services, pipelines, artifacts, or downstream consumers.

Do not mark core work done while a Critical/High review-loop finding remains undisposed.

### 8. User Review

Summarize:

- What core behavior changed.
- Which modules/files are involved.
- How it was verified.
- Any operational assumptions.
- Any gaps that should be handled by `/6-csk-qa` or another architecture pass.

### 9. Checkpoint Commit

After a verified increment, propose one checkpoint commit on the working
branch: show the exact paths and a commit message following
`.claude/rules/general.md`, and commit only with explicit approval. This keeps
progress safe across sessions. Push, merge, and pull-request actions stay with
`/finish-branch`.

## Context Recovery

If context was compacted:

1. Re-read `docs/architecture.md`.
2. Re-read the feature spec.
3. Re-read `features/INDEX.md`.
4. Run `git diff`.
5. Re-map the touched modules before continuing.
6. Continue from the existing changes; do not restart or duplicate work.

## Checklist

See `checklist.md`.

## Handoff
Before ending, preserve only durable unfinished or blocked continuation work
through `/csk-start` (show proposed rows as `PENDING-AUTH` and ask once); do not
create same-turn task churn.

> "Core implementation work is done. Next step: run `/6-csk-qa` to test this feature against its acceptance criteria, because only that check against the original list proves the feature is really done."

Propose a checkpoint commit for the verified working state (with approval).
`/finish-branch` follows only after `/6-csk-qa` reports the feature
release-ready. Do not imply that passing checks authorized Git mutations.

## Git Commit

Propose after user review: show the exact paths and diff, follow the format
rule in `.claude/rules/general.md`, and commit only with explicit approval.

```
feat(PROJ-X): Implement core behavior for [feature name]
```
