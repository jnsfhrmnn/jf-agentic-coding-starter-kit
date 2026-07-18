# Loop Policy

## Purpose

This project uses two hardening patterns:

- Planning hardening: `AUDIT -> PLAN -> REFINE -> LOG` before important plans are accepted.
- Review hardening: deep artifact review after productive work is written.

Use the bundled repository-local `/audit-plan-loop` or `/review-loop` skill. Claude reads the canonical copy from `.claude/skills/`; Codex uses the generated proxy in `.codex/skills/`. Never require or install a user-global copy. If a runtime cannot load the skill, apply the policy below directly.

## Planning Hardening Loop

Use for forward-looking artifacts: product goal, feature spec, architecture, release plan, QA plan, migration plan, data contract, pipeline design, risk plan, or other design work.

Mandatory:

- `/1-csk-init` when creating the master product contract during initialization
- `/csk-refine --master` for every product-goal, USP, system-journey, interface, contribution-map, or system-gap change
- `/2-csk-write-spec`
- `/3-csk-architecture`
- `/6-csk-qa` when building a system/release QA scope
- `/7-csk-deploy` before a non-trivial release/package/deploy/handoff plan

Conditional but strongly recommended:

- `/1-csk-init` for the PRD and feature-map phase when the product is ambiguous, high-stakes, AI/data-heavy, privacy-sensitive, or large.
- `/csk-refine PROJ-X` when feature scope, dependencies, interfaces, data locality, or release risk changes.
- `/4-csk-frontend` and `/5-csk-backend` before implementation when the change is large, cross-module, performance-sensitive, security-sensitive, AI/pipeline-heavy, or touches local/cloud boundaries.

Minimum loop:

1. Gate 0: restate the task, assumptions, gaps, and blockers.
2. Audit: find weaknesses, missing decisions, contradictions, unverified assumptions, and edge cases.
3. Plan: list the next concrete refinements.
4. Refine: update the artifact or plan.
5. Log: record findings, changes, remaining risks, and why the loop converged.

Stop only when no blocking/high issues remain, or when remaining issues are explicitly marked as open and routed to the right next step.

## Review Loop Gate

Use for already-written artifacts: code, architecture text, specs, prompts, rules, config, docs, tests, release packages, process changes, generated artifacts, or QA reports.

Mandatory after productive changes in:

- `/4-csk-frontend`
- `/5-csk-backend`
- `/6-csk-qa` before marking `Approved`, `SYSTEM GAP`, or release-ready
- `/7-csk-deploy` before marking `Deployed`
- Any change to project rules, skills, agent roles, security policy, architecture records, or source-of-truth docs

`Approved` requires recorded QA evidence. `Deployed` requires release evidence. If evidence is missing, record the gap and keep the feature in the previous non-terminal workflow state.

Use review-loop automatically when any trigger is true:

- Security, privacy, secrets, auth, permissions, file handling, subprocesses, external calls, dependency changes, or data isolation are touched.
- The change affects local/offline, online/cloud, or hybrid processing boundaries.
- The work is AI/RAG/ML/media/GPU/evaluation/agentic/pipeline related.
- The change spans multiple modules, features, agents, skills, contracts, or release artifacts.
- The change is performance-sensitive or claims performance improvement.
- The change introduces or changes a runtime, package manager, model/provider, framework, storage, queue, service, IPC, file format, schema, CLI contract, API contract, or deployment/package target.
- The work is hard to reverse or affects a large project.

For trivial low-risk text edits, a full review-loop may be skipped only if the skill records why the skip is safe and still performs a quick self-review.

## Review Depth

Use `--deep` or equivalent depth for:

- Frontier AI pipeline architecture.
- Local/cloud/privacy decisions.
- Security-sensitive work.
- Release gates.
- Large multi-module changes.
- Any finding with Critical/High severity.

Use panel or independent adversarial review when available for Critical/High findings or irreversible decisions. If no independent agent/tool is available, perform an explicit contrary refutation pass in the same context and log that limitation.

## Required Review Dimensions

At minimum, review:

- Correctness and consistency against `docs/master-feature.md`, feature specs, and `docs/architecture.md`.
- Completeness and missing edge cases.
- Security, privacy, abuse, and data locality.
- Performance and scalability.
- Interface/contract compatibility.
- Regression risk across related features.
- Evidence quality: tests/checks/benchmarks/manual verification or a documented gap.

## Finding Disposition

When the current request authorizes repository writes, no important finding may
remain only in chat. A read-only review must not mutate repository state solely
to satisfy disposition; it names the exact proposed local target as
`PENDING-AUTH` and requests one consolidated authorization.

Each real finding must end as one of:

- Fixed and verified.
- Routed to a feature/spec/architecture/QA/release follow-up.
- Recorded as a product gap in `docs/master-feature.md`.
- Recorded as a QA/review gap in the relevant feature spec or local report.
- Pending write authorization with an exact proposed local SSOT/task target.
- Explicitly dropped with rationale.

Use only the current repository's existing sources of truth and
`tasks/INDEX.md`. Once writes are authorized, keep all review state in this
repository.

If no project issue tracker exists, write durable follow-up notes into the appropriate source-of-truth file rather than leaving them only in the final answer.
