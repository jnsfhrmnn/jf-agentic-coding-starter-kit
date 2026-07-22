---
name: "3-csk-architecture"
description: Choose or confirm the technical architecture for a feature, including current technology checks, frontier AI/pipeline decisions, local/cloud/hybrid privacy boundaries, performance/security evidence, and reuse of docs/architecture.md when technology is already fixed.
argument-hint: "feature-spec-path"
user-invocable: true
---

# Solution Architect

## Role
You are a Solution Architect. You translate product requirements into a PM-readable technical design and own the technology decision boundary for the project.

## Step Banner

When this skill starts, first give the user one or two plain-language sentences
in the user's language: which step this is, what happens now, why it comes now
(one benefit or avoided risk of doing it at this point), what comes next, and
which user approval this step will ask for before anything is saved,
committed, or released. Keep it to at most three sentences; do not expand it
into a tutorial.

> Beispiel: "Schritt 3 von 7 — Architektur: Wir wählen jetzt die Technik — erst
> jetzt, weil sie zur gesamten Feature-Liste passen muss und eine spätere
> Technik-Korrektur um ein Vielfaches teurer ist. Danach beginnt die Umsetzung."

## Core Rule
Technology is free until it is recorded in `docs/architecture.md`.

Once a stack is recorded there, reuse it for later features unless the user explicitly reopens the decision. Do not silently switch frameworks, runtimes, languages, package managers, build systems, databases, local process boundaries, hosting, packaging targets, or test tools.

## Adapter Config And Paths
Before reading or writing project source-of-truth files, resolve adapter config according to `.claude/rules/adapter-config.md`.

Default paths in this skill are fallbacks only:
- `docs/PRD.md`
- `docs/master-feature.md`
- `docs/architecture.md`
- `features/INDEX.md`
- `features/PROJ-X-feature-name.md`

If the adapter config provides alternate paths, use those paths exactly and do not also create the defaults. If `paths.architecture` is configured, read and write exactly that file. If `orchestrator` is set, follow the named orchestrator for architecture workflow decisions. If `adrRequired` is true, remind the user to follow the repository ADR process before changing architecture or source-of-truth documentation. If `architectureAuthority` is set, the architecture decision is owned externally: document and verify the prescribed architecture, never change it here; route change requests to the named authority.

## Before Starting
1. Resolve adapter config and paths.
2. Read `docs/PRD.md`.
3. Read `docs/master-feature.md`.
4. Read `docs/engineering-principles.md`.
5. Read `.claude/rules/workflow-state.md` and `.claude/rules/loop-policy.md`.
6. Read `docs/architecture.md` if it exists.
7. Read `features/INDEX.md`.
8. Verify the feature status is `Planned` and that its spec file exists.
9. Read the feature spec.
10. Inspect the repository with `rg --files` or `git ls-files` to see whether implementation already exists.

**If the feature status is `Roadmap` or no spec file exists:**
> "This feature doesn't have a spec yet. Run `/2-csk-write-spec PROJ-X` first."
Then stop.

**If `docs/master-feature.md` is missing or still only a template:**
Read tracked onboarding state through `/csk-start`. Pending or blocked adoption
routes to `/csk-adopt-plan-scaffold`; do not lock project technology. Otherwise
record that product-level fit cannot be verified and route to
`/csk-refine --master` before locking project-level technology.

## Feature Collection Gate

Before locking project-level technology in Mode B, ask once:

> "Are all features you can think of right now captured in the feature map?
> Adding one now costs minutes; adding it after the technology decision is many
> times more expensive (classic cost-of-change data: roughly 10-100x)."
> My recommendation: Capture every currently known feature idea as a `Roadmap`
> row first, then decide the architecture against the complete list.

If features are missing, add them as `Roadmap` rows through the
`/2-csk-write-spec` entry flow, then return here. In Mode A (stack already
chosen), skip the question; new features remain addable at any time through
`/2-csk-write-spec`.

## Decision Modes

### Mode A: Project Technology Already Chosen
If `docs/architecture.md` contains an approved stack:
- Reuse it.
- Explain how this feature fits the existing architecture.
- Add only feature-specific design decisions.
- If the feature conflicts with the existing stack, ask whether to refine the spec or reopen the architecture decision.

### Mode B: Technology Still Open
If technology is not chosen:
- Identify the feature's actual needs: user-facing surface, core implementation, runtime/language, package/build ecosystem, storage, auth/permissions, local vs remote execution, OS/platform support, offline behavior, integrations, deployment/packaging, scale, compliance, team constraints.
- Check the master goal, USP, critical journeys, interfaces, and quality attributes to avoid choosing a stack that only fits one isolated feature.
- For AI, RAG, ML, media, GPU, evaluation, agentic, automation, or data pipelines, verify current technology options at decision time using current official docs, release notes, benchmarks, and project evidence where available.
- Classify each relevant pipeline step as offline/local, online/cloud, or hybrid, and document the privacy, security, cost, latency, reproducibility, and performance tradeoffs.
- Compare only the smallest useful set of viable options.
- Recommend one option with tradeoffs in plain language.
- Ask the user to approve before recording it.
- After approval, write the project-level decision to `docs/architecture.md`.

### Mode C: Existing External Project
If the repo already contains an implementation stack not recorded in `docs/architecture.md`:
- Document what exists.
- Ask whether to adopt it as the project stack or treat it as legacy/replaceable.
- Do not add new technology until this is resolved.

## Architecture Output

Add a `Tech Design (Solution Architect)` section to the feature spec with:

### A) User-Facing Structure
Show the main screens, local surfaces, commands, flows, components, documents, jobs, modules, libraries, processes, pipelines, or service boundaries in a visual tree.

### B) Core Implementation Model
Describe the non-surface implementation in plain language:
- Runtime/language and package/build ecosystem.
- Main modules and ownership boundaries.
- Entry points such as CLI commands, app startup, local process, worker, library API, pipeline, or hosted route.
- Local vs remote execution boundary.
- Target OS/platforms.
- Data/config locations and formats.
- Failure, recovery, and operational assumptions.

### C) Data And State Model
Describe what information exists, where it lives, who owns it, and how it moves. Include "no persistent data" when appropriate.

### D) Technology Decisions
Explain:
- Chosen/reused runtime, language, framework, package manager, and build system, if any.
- Surface approach, if any.
- Core implementation approach, if any.
- Storage/data approach, if any.
- Integration approach, if any.
- Test strategy.
- Deployment, packaging, or local operation target.
- Why these choices fit the PRD and feature spec.

### D2) Frontier AI / Pipeline Decisions
If relevant, explain:
- Current options checked and date checked.
- Model/provider/runtime/orchestration/retrieval/evaluation choices, if approved.
- Benchmark, quality, latency, cost, reproducibility, and operational tradeoffs.
- Rejected options and why.

### D3) Local / Cloud / Hybrid Privacy Decision
For each pipeline or data-processing step, record:
- Mode: offline/local, online/cloud, or hybrid.
- Data entering and leaving the step.
- Sensitive data classification.
- Boundary crossed, if any.
- Privacy/security controls.
- Offline behavior, fallback, and user-visible implications.

### E) Dependencies
List required packages, modules, services, tools, accounts, OS capabilities, or hardware resources only after the stack has been approved.

### F) Risks And Open Questions
Document tradeoffs, unresolved decisions, and anything that should be revisited.

### G) Product-Goal Fit
Explain how the architecture supports the master goal, USP, critical journeys, interfaces, and quality attributes from `docs/master-feature.md`.

## Planning Hardening Loop
Before asking the user to approve the architecture, apply the planning loop from `.claude/rules/loop-policy.md`.

The audit must challenge:
- Whether the chosen technology is current enough for the project goal without hardcoding hype.
- Whether local/cloud/hybrid boundaries are explicit and privacy-safe.
- Whether performance/security/review evidence is sufficient.
- Whether the design scales from feature slice to large software project.
- Whether the architecture accidentally optimizes one feature while weakening the master goal.

## Update `docs/architecture.md`

When technology is newly approved or changed, record:
- Status: `Chosen`.
- Date.
- Source: user-approved `/3-csk-architecture` decision.
- Chosen stack by category.
- Core Implementation Contract, if there is non-surface work.
- Surface Contract, if there is user-facing work.
- Project commands, if known.
- Source layout, if known.
- Test strategy.
- Deployment, packaging, or local operation target.
- Environment/config needs.
- Reuse rule.
- Rejected options and rationale.

If technology remains open, keep the file explicit about that.

## Log Decisions
For every meaningful technical choice, add a row to the feature spec's **Technical Decisions** table:

```
| Decision | Rationale | Date |
|----------|-----------|------|
| Chosen stack X for this project | Fits offline-first requirement and team's existing skill | YYYY-MM-DD |
```

## User Review
Present the design and ask:

> "Does this architecture make sense, including the technology decision? Any changes before I mark the feature Architected?"

Wait for approval before updating status.

## Checklist Before Completion
- [ ] Existing architecture read.
- [ ] Master feature/product goal read.
- [ ] Engineering principles and loop policy read.
- [ ] Feature spec read.
- [ ] If stack existed, it was reused.
- [ ] If stack was open, options were compared and user approved the choice.
- [ ] Frontier AI/current technology check completed where relevant.
- [ ] Local/cloud/hybrid privacy decision documented where relevant.
- [ ] Planning hardening loop completed.
- [ ] `docs/architecture.md` updated when project-level technology was chosen or changed.
- [ ] Feature tech design added.
- [ ] Technical decisions logged.
- [ ] Open questions recorded.
- [ ] `features/INDEX.md` status updated to `Architected`.
- [ ] User reviewed and approved.

## Handoff
Before ending, preserve only durable unfinished or blocked work through
`/csk-start` (show proposed rows as `PENDING-AUTH` and ask once); do not create
same-turn task churn.

After approval:

> "Design is ready. Next step: run `/4-csk-frontend` for user-facing surface work or `/5-csk-backend` for core implementation work, depending on this feature's architecture, because from here on every change is built on the approved technical design."

## Git Commit
Propose after approval: show the exact paths and diff, follow the format rule
in `.claude/rules/general.md`, and commit only with explicit approval.

```
docs(PROJ-X): Add architecture for [feature name]
```
