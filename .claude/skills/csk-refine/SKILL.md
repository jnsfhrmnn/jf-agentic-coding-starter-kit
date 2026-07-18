---
name: "csk-refine"
description: Refine an existing feature specification or the master product contract. Use PROJ-X for feature changes and --master for product-goal, USP, journey, interface, contribution-map, or system-gap changes.
argument-hint: "PROJ-X or --master"
user-invocable: true
---

# Product And Feature Refiner

## Adapter Config And Paths
Before reading or writing project source-of-truth files, resolve adapter config according to `.claude/rules/adapter-config.md`.

Default paths in this skill are fallbacks only:
- `docs/PRD.md`
- `docs/master-feature.md`
- `docs/architecture.md`
- `features/INDEX.md`
- `features/PROJ-X-feature-name.md`

If the adapter config provides alternate paths, use those paths exactly and do not also create the defaults. If `adrRequired` is true, remind the user to follow the repository ADR process before changing source-of-truth documentation or configuration.

## Role
Act as an experienced Product Manager and System QA thinker. Improve existing product truth without discarding history or bypassing architecture ownership.

## Choose A Mode
- `--master`: create, backfill, or refine the whole-product contract after a PRD exists.
- `PROJ-X`: improve, extend, split, or challenge one feature specification.

If no argument was provided, ask whether the user wants `--master` or a feature ID, and list existing features. Do not guess the mode.

## Common Preparation
1. Resolve adapter config and paths.
2. Read the PRD.
3. Read the master feature if it exists.
4. Read `docs/engineering-principles.md` if it exists.
5. Read `.claude/rules/workflow-state.md` and `.claude/rules/loop-policy.md` if they exist.
6. Read the feature index.
7. Read the architecture record when the refinement touches technology, implementation, deployment, operations, or local/cloud boundaries.

If the PRD is still a template, stop and recommend `/1-csk-init` with the product idea.

## Interview Principle
- Ask one question at a time.
- Always provide a recommended answer the user can confirm or correct.
- Follow the conversation instead of a fixed script.
- Explore source-of-truth files and code before asking what they can answer.
- Ask only about changed, missing, or contradictory information.
- Stop when the intended changes and downstream effects are clear.

## Master Mode: `--master`
Use this mode for a missing, partial, outdated, or challenged master product contract. Do not require a feature ID.

If the feature index has no roadmap entries, stop and recommend `/1-csk-init` to complete project initialization first. The Feature Contribution Map cannot be backfilled without a roadmap.

### Read Additional Context
- Read all existing feature specs relevant to product-level outcomes, journeys, interfaces, or gaps.
- Treat the feature index and implemented behavior as evidence, not automatic authority over the approved product goal.

### Opening Question
Always ask first:

> "What changed or remains unclear at the whole-product level?"
> My recommendation: Start with the product promise, critical journey, or system-level gap that no individual feature spec can resolve alone.

Determine whether this is:
- `backfill`: the master feature is missing or still a template.
- `targeted`: one product-level outcome, journey, interface, quality attribute, or gap changed.
- `fundamental`: the product goal, USP, roadmap logic, or operating model must be challenged.

Reuse existing PRD and feature answers. Cover only affected or missing areas:
- Product Goal and Unique Value Proposition.
- Target Outcomes and success evidence.
- Master Acceptance Criteria.
- Critical User Journeys and System Capabilities.
- Interfaces And Boundaries.
- Quality Attributes.
- Frontier AI / Pipeline Needs.
- Local / Cloud / Hybrid Expectations.
- Feature Contribution Map.
- Missing Or Could-Be-Better.
- Decision Log.

Write system-level acceptance criteria in German:

```markdown
- [ ] Angenommen [System-/Nutzerkontext], wenn [End-to-end-Aktion], dann [messbares Gesamtziel]
```

Do not copy feature-level criteria. Map features to outcomes and journeys, including dependencies, system risk if missing, and whether each is MVP, differentiator, or enhancement. Flag roadmap items that no longer contribute.

### Master Planning Hardening
Before saving, apply the planning loop from `.claude/rules/loop-policy.md`:

1. Audit the proposed master changes against the PRD, feature map, engineering principles, known architecture constraints, and existing evidence.
2. Plan corrections and downstream updates.
3. Refine the master feature and only the related product/roadmap records.
4. Log unresolved gaps and route architecture, feature-spec, or QA follow-ups.

Present the master changes for user approval. Then:
- Create or update the master feature using its existing shape.
- Update the PRD only if product vision, constraints, metrics, or roadmap changed.
- Update the feature index only if names, dependencies, priorities, or statuses clearly changed.
- Do not create an individual feature spec; use `/2-csk-write-spec PROJ-X`.
- Do not change architecture decisions directly; route them to `/3-csk-architecture` or the configured `architectureAuthority`.

## Feature Mode: `PROJ-X`
Read the complete matching feature spec. If the ID does not exist, stop and list existing features.

### Opening Question
Always ask first:

> "What brought you back to this spec?"

Use the answer to choose a path.

### Path 1: Something Changed
Run a targeted interview:
- What changed and which user stories or criteria are affected?
- Do edge cases, dependencies, or scope boundaries change?
- Does this affect the master goal, USP, journeys, interfaces, contribution map, or system gaps?
- Does this affect locality, AI/pipeline, performance, security, or evidence expectations?

### Path 2: Implementation Revealed Gaps
Determine:
- Which scenario was missing.
- Whether it becomes a criterion, edge case, or separate feature.
- Which existing criteria change.
- Whether this reveals a system-level gap for the master feature.
- Which planning or review-loop gate now applies.

### Path 3: Fundamental Challenge
Challenge:
- Which assumption is wrong.
- Whether the user story remains correct.
- Whether the feature should split, merge, shrink, or be cancelled.
- Whether it still strengthens the master goal and USP.
- What moves out of scope.

If splitting is approved, create the new spec through the `/2-csk-write-spec` workflow and update the feature index.

If technology is reopened, update product requirements but do not change implementation directly. Route the decision to `/3-csk-architecture` or the configured `architectureAuthority`.

### Update The Feature Spec
For complex, high-risk, AI/pipeline, local/cloud, security/privacy, performance-sensitive, or architecture-affecting changes, apply the planning hardening loop before finalizing.

After approval:
- Update and re-read the feature spec.
- Append new external briefing references to `Briefing Provenance`; never replace earlier references.
- Close resolved Open Questions with a resolution note and date.
- Add decisions with rationale and date.
- Add unresolved questions as open items.
- Update the feature index if status or dependencies changed.
- Update the PRD if the roadmap changed.
- Update the master feature if product-level truth changed.

## Checklist Before Completion

### All Modes
- [ ] Mode selected explicitly.
- [ ] Existing source-of-truth files read before editing.
- [ ] One-question interview used and existing answers reused.
- [ ] User reviewed the proposed changes.
- [ ] Changed files re-read after saving.
- [ ] Planning/review-loop decision recorded where required.

### Master Mode
- [ ] Product-level change or backfill reason identified.
- [ ] Goal, USP, outcomes, criteria, journeys, capabilities, interfaces, quality, locality, contribution, and gaps are complete or explicitly marked open/not applicable.
- [ ] Planning hardening loop completed.
- [ ] PRD and feature index reconciled only where needed.
- [ ] Architecture changes routed to the correct owner.

### Feature Mode
- [ ] Feature path selected and all affected criteria, edge cases, dependencies, and scope resolved.
- [ ] Decision Log and Open Questions maintained.
- [ ] Briefing provenance preserved and appended when applicable.
- [ ] Product-level changes reflected in the master feature.

## Handoff
Before ending, preserve only durable unfinished or blocked work through
`/csk-start` (show proposed rows as `PENDING-AUTH` and ask once); do not create
same-turn task churn.

Before choosing the handoff, read the transition and routing SSOT in
`.claude/rules/workflow-state.md`.

For `--master`, choose exactly one next command from the current feature status. Include the real feature ID or adapter-resolved spec path. Do not present a menu of possible next steps.

For `PROJ-X`, also choose exactly one next command from the current feature status. A split or reopened technology decision normally routes to `/3-csk-architecture features/PROJ-X-name.md`; substitute the real adapter-resolved path.

## Git Commit
```
docs: Refine product or feature specification
```
