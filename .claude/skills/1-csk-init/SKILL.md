---
name: "1-csk-init"
description: Initialize or adopt a project by creating the PRD, technology constraints, prioritized feature map, and complete master product contract without choosing a stack.
argument-hint: "description of what you want to build"
user-invocable: true
---

# Project And Master Product Initializer

## Role
Act as an experienced Product Strategist and System QA thinker. Turn the user's product idea into two distinct sources of truth:

- `docs/PRD.md` for product vision, users, roadmap, constraints, and success metrics.
- `docs/master-feature.md` for the whole-product goal, USP, system acceptance criteria, critical journeys, interfaces, quality attributes, feature contribution, and product gaps.

Do not choose implementation technology. Record fixed constraints and existing decisions, then leave open choices to `/3-csk-architecture`.

## Step Banner

When this skill starts, first give the user one or two plain-language sentences
in the user's language: which step this is, what happens now, why it comes now
(one benefit or avoided risk of doing it at this point), what comes next, and
which user approval this step will ask for before anything is saved,
committed, or released. Keep it to at most three sentences; do not expand it
into a tutorial.

> Beispiel: "Schritt 1 von 7 — Produktdefinition: Wir klären jetzt, was die
> Software können soll, für wen und woran wir Erfolg messen — damit wir bauen,
> was wirklich gebraucht wird, statt einfach loszulegen. Danach schreiben wir
> für das erste Feature eine genaue Spezifikation."

## Interview Principle
Interview until there is a complete shared understanding.

- Ask one question at a time.
- Always provide a recommended answer the user can confirm or correct.
- Follow the conversation instead of a fixed script.
- Explore existing files before asking if the answer may already be present.
- Reuse every answer across the PRD, feature map, and master product contract. Never ask the same product question twice.
- Stop only when the product, constraints, first build slice, and system-level success target are clear.

## Adapter Config And Paths
Before reading or writing project source-of-truth files, resolve adapter config according to `.claude/rules/adapter-config.md`.

Default paths in this skill are fallbacks only:
- `docs/PRD.md`
- `docs/master-feature.md`
- `docs/architecture.md`
- `features/INDEX.md`
- `features/PROJ-X-feature-name.md`

If the adapter config provides alternate paths, use those paths exactly and do not also create the defaults. If `adrRequired` is true, remind the user to follow the repository ADR process before changing source-of-truth documentation.

## Before Starting
1. Run `/csk-start` and require valid project state.
2. Read `.claude/rules/workflow-state.md`.
3. Resolve adapter config and paths.
4. Read the PRD and determine whether it is still a template.
5. Read `docs/engineering-principles.md` and `.claude/rules/loop-policy.md`.
6. Read the feature index and determine whether features exist.
7. Read the master feature and determine whether it is missing, a template, partial, or complete.
8. Read the architecture record if it exists.
9. Inspect the repository with `rg --files` or `git ls-files` for existing source, docs, and config.

## Initialization Modes
Use the mode already stored by `/csk-start` in `.csk/project-state.json`; do not
classify the repository again here:

- `greenfield`: no meaningful pre-existing product, architecture, feature,
  implementation, or workflow evidence exists. Template-only CSK files do not
  disqualify this mode.
- `adopt`: meaningful project evidence predates the CSK scaffold and requires
  reconciliation. Run `/csk-adopt-plan-scaffold` and stop until adoption state is
  `complete`.
- `partial`: meaningful CSK source-of-truth content exists, but important CSK pieces
  are missing or still templates after adoption is complete or not applicable.
  Preserve existing content and fill
  only clear gaps.

If state is missing, invalid, pending, or blocked, return to `/csk-start`. Never
guess a mode from repository contents in this skill.

In `adopt` mode, produce an inventory and gap list first. Only create or edit files after the user approves the proposed mapping. Prefer adapter config when equivalent product, architecture, or feature-tracking files already exist.

Before applying the missing-master fallback, require adoption state `complete` or
`not-applicable`. Pending or blocked adoption routes to
`/csk-adopt-plan-scaffold`. Use `/csk-refine --master` only after that gate.

If a prior run already completed the PRD and feature map but the master product contract is missing, partial, or still a template, do not repeat initialization. Tell the user to run `/csk-refine --master`, then stop.

If the PRD, feature map, and master product contract are already complete, tell the user:

> "This project is already initialized. Use `/2-csk-write-spec` to create a feature spec, `/csk-refine PROJ-X` to update one, `/csk-refine --master` to revisit product-level scope, or `/3-csk-architecture` to choose or confirm technology."

Then stop unless the user explicitly requested an adopt or partial inventory. Product-level refinement belongs to `/csk-refine --master`.

## Shared Product Interview
Start from the user's argument. If none was given, ask:

> "What do you want to build, and what problem does it solve?"
> My recommendation: Start with the user pain - what frustrates people today that your product will fix?

Cover these topics naturally:
- Core problem and primary target users.
- Must-have MVP outcomes versus later ideas.
- Existing alternatives and what must be meaningfully different.
- Success metrics and evidence.
- Constraints: timeline, budget, team, compliance, devices, offline needs, integrations.
- Non-goals for the first version.
- Persistent data, accounts, sync, jobs, files, payments, and third-party integrations.
- Quality expectations: reliability, performance, security/safety, usability, operability, review, and evidence.
- Frontier AI, RAG, ML, media, GPU, evaluation, agentic, automation, or data-pipeline ambitions.
- Data locality: what must be offline/local, what may be online/cloud, and where hybrid processing is acceptable.
- Existing design system, brand guidance, UI references, or style direction.

### Technology Constraint Gate
Resolve before creating the feature map:

> "Do we already have hard technology constraints, existing code, hosting, compliance, team skills, or tools that must be reused or avoided?"
> My recommendation: If there is no existing project constraint, keep technology open until `/3-csk-architecture` evaluates the first real feature.

Record the answer under **Technology Constraints** in the PRD. Do not choose a stack unless the user explicitly states it is already fixed.

If technology is fixed:
- Record it in the architecture file as an existing project decision, not a recommendation from this skill.
- Require later implementation to reuse it unless the user reopens the decision.

If technology is open:
- Record `Technology status: Open - to be chosen by /3-csk-architecture`.
- Do not add package managers, frameworks, databases, or hosting providers.

### Capability And Data Gate
Capture required capabilities as product requirements, not vendor choices. If cross-cutting setup is clearly required, add a generic **Project Foundation** feature as an early P0 item. It may cover environment, persistence/auth/integration foundation, deployment baseline, or repository structure, but must not name technology unless already fixed.

### Quality And Data Locality Gate
Capture quality, performance, security, privacy, offline/local, cloud, hybrid, and AI/pipeline expectations as outcomes. Record broad constraints in the PRD and turn product-wide expectations into testable targets in the master product contract.

### Design Direction Gate
If design direction exists, save it to `docs/design-system.md` or reference the provided file and add a PRD constraint. Otherwise mark design as open for `/3-csk-architecture` or `/4-csk-frontend`.

## Phase A: Project Foundation

### Draft The PRD
Include:
- Vision.
- Pointer to the master feature for whole-product goal and USP.
- Target users.
- Core features and roadmap.
- Success metrics.
- Constraints and non-goals.
- Technology constraints.
- Required product capabilities.
- Engineering quality constraints.

### Draft The Feature Map
Apply Single Responsibility:
- Each feature is one testable, releasable unit.
- Identify dependencies and recommended build order.
- Assign priority P0, P1, or P2.
- Keep technology names out of titles unless they are user-mandated constraints.

Each feature-index entry contains ID, name, one-line description, priority, dependencies, and status `Roadmap`. Update `Next Available ID`.

Present the PRD and feature map together. Apply feedback and save them only after user approval.

### Create Or Update The Architecture Record
Ensure the adapter-resolved architecture file exists.

If `architectureAuthority` is set, preserve the externally owned decision, record the named authority and prescribed constraints or status, and route every change request to that authority. Do not independently classify or rewrite the architecture as `Open` or `Chosen`.

Otherwise, if technology is open, record status `Open`, known constraints, banned/required technologies, and that `/3-csk-architecture` owns the decision. If fixed, record status `Chosen`, the stack, source of decision, and reuse rule.

## Phase B: Master Product Contract
Run this phase during every initialization after Phase A. Do not finish initialization with a template master feature.

Derive as much as possible from the approved PRD, roadmap, and earlier answers. Ask only about unresolved system-level details:
- What the complete software must accomplish.
- The explicit USP.
- Target outcomes and success evidence.
- Critical end-to-end journeys across features or modules.
- System capabilities required by those journeys.
- Important interfaces and boundaries for QA.
- Non-negotiable quality attributes.
- Frontier AI or pipeline needs and evaluation targets.
- Offline/local, online/cloud, or hybrid expectations.
- How each planned feature contributes to the product goal.
- What is missing, weak, unclear, or could make the product substantially better.

### Planning Hardening Loop
Before saving the final master product contract, apply the planning loop from `.claude/rules/loop-policy.md`:

1. Audit the product goal, USP, journeys, interfaces, AI/pipeline assumptions, local/cloud assumptions, quality attributes, feature contribution, and gaps.
2. Plan concrete refinements.
3. Refine the master feature and any affected roadmap entries.
4. Log remaining gaps and why the contract is clear enough for feature specs and architecture.

### Write The Master Feature
Use the existing file shape if present. Ensure these sections exist:

1. Product Goal.
2. Unique Value Proposition.
3. Target Outcomes.
4. Master Acceptance Criteria.
5. Critical User Journeys.
6. System Capabilities.
7. Interfaces And Boundaries.
8. Quality Attributes.
9. Frontier AI / Pipeline Needs.
10. Local / Cloud / Hybrid Expectations.
11. Feature Contribution Map.
12. Missing Or Could-Be-Better.
13. Decision Log.

Write system-level acceptance criteria in German:

```markdown
- [ ] Angenommen [System-/Nutzerkontext], wenn [End-to-end-Aktion], dann [messbares Gesamtziel]
```

Do not duplicate feature-level criteria. Master criteria prove that the product works as a whole.

For every roadmap feature, record the supported outcome or journey, dependencies, product risk if missing or weak, and whether it is required for MVP, a differentiator, or an enhancement. Flag features that do not contribute instead of silently retaining them.

Always challenge the result:
- What is missing for the product to achieve the goal?
- What would strengthen the USP?
- Which interface or dependency is under-specified?
- Which locality, privacy, AI, or performance assumption needs architecture verification?
- Which system-level QA scenario must exist later?

Present the master feature for user review before saving. After approval, update the PRD pointer and reconcile feature names, dependencies, priorities, or statuses only when the master analysis requires it.

## What Not To Do
- Do not create individual feature spec files.
- Do not write implementation code.
- Do not choose technology unless the user states it is fixed already.
- Do not add package manifests, lockfiles, framework config, databases, hosting config, or generated scaffolds.
- Do not collapse the PRD and master feature into one file; they have different downstream responsibilities.

## Checklist Before Completion
- [ ] Initialization mode identified and existing content preserved.
- [ ] PRD fully filled out and approved.
- [ ] Technology constraints and architecture status recorded.
- [ ] Capability, quality, AI/pipeline, and locality needs captured without vendor lock-in.
- [ ] Design direction resolved or marked open.
- [ ] Feature map approved, single-responsibility, prioritized, dependency-aware, and indexed as `Roadmap`.
- [ ] Master product goal and USP are concrete.
- [ ] System acceptance criteria, journeys, capabilities, interfaces, and quality attributes are testable.
- [ ] AI/pipeline and local/cloud/hybrid expectations are captured or marked not applicable/open.
- [ ] Feature Contribution Map and Missing Or Could-Be-Better review are complete.
- [ ] Planning hardening loop completed for the master product contract.
- [ ] User reviewed and approved both product sources of truth.

## Handoff
Before ending, preserve only durable unfinished or blocked work through
`/csk-start` (show proposed rows as `PENDING-AUTH` and ask once); do not create
a task for same-turn work. Repository files, never chat memory, own workflow
state.

After approval:

> "Project and master product contract are ready. Next step: run `/2-csk-write-spec PROJ-X` for **[recommended first feature name]**, because a precise specification is the checklist the finished software will be tested against. If more feature ideas come up, add them to the roadmap before the architecture step — additions are cheapest now."

## Git Commit
Propose after approval: show the exact paths and diff, follow the format rule
in `.claude/rules/general.md`, and commit only with explicit approval.

```
feat: Initialize project and master product contract
```
