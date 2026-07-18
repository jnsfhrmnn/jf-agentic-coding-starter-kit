# Feature Specifications

This folder contains detailed feature specs created by `/2-csk-write-spec` and enriched by later workflow steps.

Whole-product intent lives in `docs/master-feature.md`. Feature specs should explain how one feature contributes to that master goal, USP, critical journey, interface, or quality attribute.

Engineering quality expectations live in `docs/engineering-principles.md`. Feature specs should capture local/cloud/privacy, performance, security, and AI/pipeline requirements as outcomes, not technology choices.

## Naming Convention

`PROJ-X-feature-name.md`

Examples:
- `PROJ-1-user-authentication.md`
- `PROJ-2-import-workflow.md`
- `PROJ-3-report-export.md`

## What Belongs In A Feature Spec?

### 1. User Stories
Describe what the user wants to do:

```markdown
As a [user type], I want to [action] so that [goal].
```

### 1b. Product Goal Contribution
Connect the feature to `docs/master-feature.md`:

```markdown
## Product Goal Contribution

- **Master Goal / USP:** [what this feature supports]
- **Critical Journey:** [journey from docs/master-feature.md, if any]
- **Interfaces / Boundaries:** [surface/core/data/process/file/service/artifact boundaries]
- **System Risk If Missing:** [what breaks at product level]
```

### 2. Acceptance Criteria
Concrete, testable criteria in German:

```markdown
- [ ] Angenommen [Vorbedingung], wenn [Aktion], dann [Ergebnis]
```

### 3. Edge Cases
Unexpected or risky situations:

```markdown
- What happens when required input is missing?
- What happens when a dependency is unavailable?
- What happens when two users or processes change the same item?
```

### 4. Tech Design
Added by `/3-csk-architecture`.

This section explains the approved technical approach in plain language:

```markdown
## Tech Design (Solution Architect)

### User-Facing Structure
Main workflow
+-- Input step
+-- Review step
+-- Completion state

### Data And State Model
Each item has an owner, status, timestamp, and audit note.

### Technology Decisions
The project stack is recorded in docs/architecture.md and reused here.

### Local / Cloud / Hybrid Decision
Each data or pipeline step records whether it runs offline/local, online/cloud, or hybrid.

### Frontier AI / Pipeline Decision
Current technology options and evaluation evidence are recorded when relevant.
```

### 5. QA Test Results
Added by `/6-csk-qa` at the end of the feature document:

```markdown
---

## QA Test Results

**Tested:** YYYY-MM-DD
**Test Target:** [local command, preview artifact, staging URL, CLI command, document, or package]

### Acceptance Criteria Status
- [x] AC-1 passed
- [ ] BUG: AC-2 failed

### Evidence
- `commit:<sha> | file:<path>:<line> | test:<name> | url:<endpoint>`

### Master Goal / USP Alignment
- Relevant master goal:
- Contribution:
- Gap:

### Cross-Feature Journeys
- Journey:
- Interfaces:
- Result:

### Bugs Found
**BUG-1: [Bug title]**
- **Severity:** High
- **Steps to Reproduce:**
- **Expected:**
- **Actual:**
```

### 6. Release, Packaging, Or Deployment Status
Added by `/7-csk-deploy`:

```markdown
---

## Release / Packaging / Deployment

**Status:** Deployed
**Released:** YYYY-MM-DD
**Target:** [approved target from docs/architecture.md]
**Artifact / URL / Version:** [value]
**Evidence:** commit:<sha> | file:<path>:<line> | test:<name> | url:<endpoint>
**Git Tag:** vX.Y.Z-PROJ-X
```

## Workflow

1. `/1-csk-init` creates the PRD, feature map, and master product contract.
2. `/2-csk-write-spec` creates one full feature spec.
3. The user reviews and approves the spec.
4. `/3-csk-architecture` adds the technical design, current technology checks, local/cloud decisions, and records stack decisions.
5. `/4-csk-frontend` and/or `/5-csk-backend` implement only the parts required by the approved architecture. The backend slot means core implementation, not necessarily a web server.
6. `/6-csk-qa` tests feature behavior, system journeys, interfaces, local/cloud mode, regressions, and master-goal fit.
7. `/7-csk-deploy` releases or packages the feature.

## Status Tracking

Feature status is tracked in `features/INDEX.md` and in the feature spec header:

```markdown
# PROJ-1: Feature Name

## Status: Planned
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD
```

Valid statuses:
- Roadmap
- Planned
- Architected
- In Progress
- In Review
- Approved
- Deployed
- Cancelled

`Approved` requires recorded QA evidence such as test output, a file reference with line, a URL, a commit SHA, or an artifact. Without evidence, keep the feature `In Review` and document the gap. `Deployed` requires release evidence such as an artifact, URL, version, tag, or handoff record. `Cancelled` is terminal and should include a one-line reason in the spec.

## Git As Source Of Truth

- Implementation details belong in commits.
- `git log --grep="PROJ-1"` shows changes for one feature.
- Keep feature specs focused on product scope, master-goal contribution, architecture decisions, QA results, and release status.
