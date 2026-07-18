---
name: csk-help
description: Context-aware CSK guide for locating the current project phase, reconciling durable tasks and Git state, and recommending exactly one safe next action from the repository workflow. Use when the user asks what to do next, where the project stands, how skills fit together, or which skill should handle a finding.
argument-hint: optional question
user-invocable: true
---

# Project Help Guide

Answer the user's specific question first, then show where the repository is and
recommend exactly one primary next action.

## Read first

1. Read `.csk/project-state.json` through `/csk-start` state validation.
2. Read `.claude/rules/workflow-state.md`; it is the transition and routing SSOT.
3. Resolve optional local paths through `.claude/rules/adapter-config.md` and
   repository-root `csk.config.json`.
4. Read `tasks/INDEX.md`, live Git status/branch, the adapter-resolved PRD,
   master feature, architecture, feature index, and only applicable feature specs.
5. Read `docs/engineering-principles.md` and `.claude/rules/loop-policy.md` when
   quality, architecture, QA, release, planning, or review is in scope.
6. Inventory code with `rg --files` or `git ls-files`; assume no language,
   framework, package manager, test runner, or deployment target.

Do not contact another repository or rely on chat memory. Repository and Git
state win over a task's advisory branch or any prior recommendation.

## Determine the next action

Apply the routing precedence and entry contracts from
`.claude/rules/workflow-state.md`. Stop at the first applicable gate:

- Invalid onboarding state: repair the state; do no productive work.
- Adoption pending or blocked: run `/csk-adopt-plan-scaffold`.
- Actionable durable work: run `/csk-start`, reconcile it, and continue the
  selected item with its recorded runtime-neutral resume skill.
- Dirty or ambiguous Git state: inspect and attribute it before switching scope.
- Incomplete project initialization: run `/1-csk-init` with the user's idea.
- Missing master product contract: run `/csk-refine --master`.
- Unowned requested scope: run `/2-csk-write-spec`.
- Existing feature: use its authoritative status and the workflow-state rule.
- Verified work on a non-default branch: run `/finish-branch` before deployment
  or closure.

For QA or review findings, route the fix to the component owner:

- user-facing surface or interaction: `/4-csk-frontend`;
- core behavior, service, data, automation, pipeline, or integration:
  `/5-csk-backend`;
- architecture mismatch: `/3-csk-architecture` or `/csk-refine` before code;
- test-only gap: `/6-csk-qa`;
- release-only gap: `/7-csk-deploy` after the feature returns to `Approved`.

Keep a feature in `In Review` while remediation is open. Create one durable task
only if the remediation will survive the current session, is deferred, blocked,
or is a verified interruption point.

## Response format

Use this compact structure:

```text
Project Status
Onboarding: <mode/status and actual distribution scope>
Product: <initialized/incomplete>
Architecture: <open/chosen/adopted>
Git: <branch and clean/dirty>
Tasks: <open/blocked counts>
Feature: <PROJ-X — authoritative status, when applicable>

Next step: Run /<skill> to <specific action>.
Why: <one or two evidence-based sentences>
```

Mention a blocker or state drift before the recommendation. Do not list several
competing next commands unless the user explicitly asks for options.

## Common questions

- Why this order: the numbered steps follow the classic engineering cycle —
  requirements, then specification, then architecture, then implementation,
  then QA against the original acceptance criteria, then release. See
  "Why this order?" in `README.md` for the short rationale.
- Available workflow skills: numbered skills 1–7 plus `/csk-start`,
  `/csk-adopt-plan-scaffold`, `/csk-refine`, `/csk-help`, `/finish-branch`,
  `/audit-plan-loop`, `/review-loop`, and `/claude-skill-proxy-sync`.
- Plan/review hardening: explain `/audit-plan-loop`, `/review-loop`, and
  `.claude/rules/loop-policy.md`.
- Codex compatibility: `.claude/skills` is canonical and repo-local; ready Codex
  proxies live in `.codex/skills`; `/claude-skill-proxy-sync` refreshes them.
- Deterministic versus non-deterministic: deterministic work has repeatable rules
  and mechanically checkable outputs. Its opposite is non-deterministic; in this
  workflow that usually means semantic judgment can legitimately depend on
  context, evidence, and tradeoffs rather than one fixed algorithmic answer.

## Safety

- Help and status inspection are read-only.
- Never claim that a task, feature transition, commit, push, merge, pull request,
  tag, release, or deployment happened without direct evidence.
- Never install repo skills globally.
- Never bypass onboarding, workflow entry contracts, or explicit external-action
  approval merely because the next command appears obvious.
