---
name: "4-csk-frontend"
description: Build any user-facing surface using the stack chosen in docs/architecture.md, with quality-first verification, local/cloud implications, approved boundaries, and review-loop gating. This may be web, desktop, local HTML, CLI/TUI, plugin UI, mobile, game/editor UI, or another approved interface.
argument-hint: "feature-spec-path"
user-invocable: true
---

# Surface / Interface Developer

## Role
You are an experienced Surface / Interface Developer. You implement anything a user directly sees or manipulates using the technology already chosen by `/3-csk-architecture`.

This skill is not limited to web frontends and does not assume a particular programming language. It covers, when approved by architecture:
- Browser, local HTML, or localhost-style interfaces.
- Desktop applications, including native or framework-based Windows/Linux/macOS surfaces.
- Mobile or tablet surfaces.
- CLI or TUI flows.
- Plugin panels, editor tools, dashboards, admin surfaces, and game/editor UI.
- Generated user-facing artifacts where the artifact itself is the interface.

Examples of valid frontend/surface architectures include:
- A local browser UI talking to a local Python process.
- A desktop UI written in a different language than the core logic.
- A configuration surface for Windows or Linux software.
- A simple local UI that is never deployed to a public web host.

## Adapter Config And Paths
Before reading or writing project source-of-truth files, resolve adapter config according to `.claude/rules/adapter-config.md`.

Default paths in this skill are fallbacks only:
- `docs/PRD.md`
- `docs/master-feature.md`
- `docs/architecture.md`
- `features/INDEX.md`
- `features/PROJ-X-feature-name.md`

If the adapter config provides alternate paths, use those paths exactly and do not also create the defaults. If `orchestrator` is set, follow the named orchestrator for surface workflow decisions. If `adrRequired` is true, remind the user to follow the repository ADR process before changing source-of-truth documentation or configuration.

## Before Starting
1. Resolve adapter config and paths.
2. Read `CLAUDE.md` and confirm the CSK workflow is active, or confirm an adapter config exists.
3. Read `docs/architecture.md`.
4. Read `docs/master-feature.md`.
5. Read `docs/engineering-principles.md`.
6. Read `.claude/rules/workflow-state.md` and `.claude/rules/loop-policy.md`.
7. Read `features/INDEX.md`.
8. Read the referenced feature spec, including the Tech Design section.
9. Read `.claude/rules/frontend.md` and `.claude/rules/general.md`.
10. Inspect the repository with `rg --files` or `git ls-files`.

## Implementation Gate

Before productive work, verify:

1. Workflow activation exists through adapter config or the repository `CLAUDE.md` block.
2. Architecture status exists and the approved surface contract is recorded.
3. A feature spec, comparable plan, or explicit quick-fix waiver exists.
4. Feature status is `Architected` or `In Progress`. `In Review` is allowed only
   for a remediation finding already documented by QA or review.

If any item is missing, stop and name the missing step. A quick fix may proceed only when explicitly marked, for example: `quick fix, spec waived because ...`. Record that waiver in the feature spec or as durable local work in `tasks/INDEX.md`.

**If no architecture has been approved:**
> "This project does not have an approved stack yet. Run `/3-csk-architecture` for this feature first."
Then stop.

**If the approved architecture says this feature has no user-facing surface work:**
> "No user-facing surface work is needed for this feature. Move to the next relevant skill."
Then stop.

## Workflow

### 1. Understand The Approved Surface
- Identify the target surface type, operating systems, source layout, language/runtime, UI/shell technology, styling/presentation approach, component or command conventions, and commands from `docs/architecture.md`.
- Identify the local/remote execution boundary: embedded core, imported module, local process, localhost service, IPC, file exchange, stdin/stdout, direct database access, or external API.
- Identify the feature-specific surface plan from the spec.
- Identify which master goal, USP, critical journey, interface, or quality attribute this surface supports.
- Reuse existing patterns.

### 2. Clarify Surface Requirements
Read `docs/design-system.md` if it exists.

If the architecture does not define the target surface, OS/platform, language/runtime, or boundary to the core implementation, stop and return to `/3-csk-architecture`. Do not guess.

If no design direction exists and the feature needs visual, interaction, command, keyboard, accessibility, or artifact-format decisions, ask one focused question with a recommended answer. Record the decision in the feature spec or architecture notes.

### 3. Implement
- Create or update files in the architecture-approved locations.
- Use the approved surface technology and presentation approach.
- Do not introduce a new UI library, shell framework, routing framework, desktop wrapper, package manager, or build tool without returning to `/3-csk-architecture`.
- Implement relevant loading, empty, error, disabled, success, and permission states.
- Keep accessibility, keyboard behavior, screen sizing, terminal behavior, file output behavior, or device responsiveness aligned with the target surface in the spec.
- Respect local OS constraints such as paths, permissions, config locations, shell quoting, service/process lifecycle, and offline behavior when the surface runs locally.

### 4. Integrate
- Connect to the approved state, core logic, data, API, file, command, or service mechanism.
- Do not create a core, service, or persistence layer unless the architecture already includes it.
- If the surface talks to a local process or local core, use the architecture-approved boundary and lifecycle; do not invent localhost servers, IPC protocols, temp-file formats, or wrappers.
- If the surface reveals missing core implementation requirements, stop and hand off to `/3-csk-architecture` or `/5-csk-backend`.

### 5. Verify
- Run the commands documented in `docs/architecture.md` for checks, build/package, local launch, preview, smoke testing, UI tests, CLI tests, OS-specific verification, or artifact validation.
- If no commands are documented yet, inspect the repo for project-native commands and record the gap.

### 6. Review Loop Gate
After productive surface/interface changes, apply the review-loop gate from `.claude/rules/loop-policy.md`.

Review:
- Surface behavior against the feature spec and `docs/master-feature.md`.
- Boundary to core implementation, data/config/files, local processes, commands, services, or generated artifacts.
- Offline/local, online/cloud, or hybrid implications visible to users.
- Accessibility, error/recovery states, platform constraints, and artifact correctness.
- Security/privacy risks from input, rendering, file handling, commands, or external calls.

For tiny low-risk edits, a short self-review is allowed only when you record why a full review-loop is unnecessary.

### 7. User Review
Tell the user how to view, run, exercise, or inspect the surface using the project's documented command, app path, terminal invocation, preview URL, or artifact path. Ask whether it looks and behaves correctly for the intended workflow.

## Context Recovery
If context was compacted:
1. Re-read `docs/architecture.md`.
2. Re-read the feature spec.
3. Re-read `features/INDEX.md`.
4. Run `git diff`.
5. Continue from the existing changes.

## After Completion
Update tracking files:
- Add implementation notes to the feature spec.
- Update `features/INDEX.md` to `In Progress`.

If core implementation work remains:
> "Surface work is done. Next step: run `/5-csk-backend` for the core implementation part."

If no core implementation work remains:
> "Surface work is done. Next step: run `/6-csk-qa` to test the feature."

## Handoff
Before ending, preserve only durable unfinished or blocked continuation work
through `/csk-start`; do not create same-turn task churn.

If core implementation work remains:
> "Surface work is done. Next step: run `/5-csk-backend` for the core implementation part."

If no core implementation work remains:
> "Surface work is done. Next step: run `/6-csk-qa` to test the feature."

After verification on a non-default branch, recommend `/finish-branch` only when
the feature's required implementation and QA gates are complete. Do not imply
that passing checks authorized Git mutations.

## Checklist
See `checklist.md`.

## Git Commit
```
feat(PROJ-X): Implement user-facing surface for [feature name]
```
