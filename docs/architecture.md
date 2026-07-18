# Architecture Decision Record

## Status
Open

## Decision Rule
This starter kit does not prescribe a framework, runtime, package manager, database, core implementation style, UI library, test runner, packaging format, or deployment target.

`/3-csk-architecture` chooses or confirms technology based on the PRD, `docs/master-feature.md`, feature spec, existing project constraints, and user approval. Once a stack is recorded here, later skills reuse it unless the user explicitly reopens the decision.

## Existing Constraints
- Required technologies: None recorded yet
- Forbidden technologies: None recorded yet
- Existing codebase constraints: None recorded yet
- Team/hosting/compliance constraints: None recorded yet

## Chosen Stack
_Not chosen yet._

| Category | Decision | Rationale |
|----------|----------|-----------|
| Runtime / language | _Open_ | _To be decided by /3-csk-architecture_ |
| Application structure | _Open_ | _To be decided by /3-csk-architecture_ |
| User-facing surface | _Open_ | _Target surface, OS/platform, language/runtime, and local/remote boundary to be decided by /3-csk-architecture_ |
| Data / persistence | _Open_ | _To be decided by /3-csk-architecture_ |
| Auth / permissions | _Open_ | _To be decided by /3-csk-architecture_ |
| Testing | _Open_ | _To be decided by /3-csk-architecture_ |
| Release / deployment | _Open_ | _To be decided by /3-csk-architecture_ |

## Product Goal Fit
_Use `docs/master-feature.md` to record whether the chosen architecture supports the master goal, USP, critical journeys, interfaces, and quality attributes._

| Area | Decision / Fit |
|------|----------------|
| Master goal support | _Open_ |
| USP support | _Open_ |
| Critical journeys | _Open_ |
| Key interfaces / boundaries | _Open_ |
| Quality attributes | _Open_ |
| Known product-level risks | _Open_ |

## Frontier AI / Pipeline Decision Record
_Use this for AI, RAG, ML, media, GPU, evaluation, agentic, automation, or data pipelines._

| Question | Decision |
|----------|----------|
| Current options checked | _Open_ |
| Date checked | _Open_ |
| Sources checked | _Open_ |
| Model/provider/runtime/orchestration choice | _Open_ |
| Evaluation strategy | _Open_ |
| Quality target | _Open_ |
| Latency / throughput target | _Open_ |
| Cost/resource target | _Open_ |
| Reproducibility / determinism approach | _Open_ |
| Rejected options | _Open_ |

## Local / Cloud / Hybrid Pipeline Contract
_Every pipeline step that touches data, inference, processing, storage, search, evaluation, files, logs, telemetry, or external services must be classified._

| Step | Mode | Data In | Data Out | Sensitivity | Boundary Crossed | Controls | Rationale |
|------|------|---------|----------|-------------|------------------|----------|-----------|
| _Step_ | _Offline/local, online/cloud, or hybrid_ | _Open_ | _Open_ | _Open_ | _Open_ | _Open_ | _Open_ |

## Performance / Security / Review Gates
| Gate | Decision |
|------|----------|
| Performance fixtures or benchmark commands | _Open_ |
| Security/privacy review scope | _Open_ |
| Required planning hardening loop | _Open_ |
| Required review-loop gate | _Open_ |
| Evidence required before QA approval | _Open_ |

## Core Implementation Contract
_Fill this in when a feature or project has non-surface implementation work._

| Question | Decision |
|----------|----------|
| Core runtime/language | _Open_ |
| Package/build ecosystem | _Open_ |
| Target OS/platforms | _Open_ |
| Module ownership / boundaries | _Open_ |
| Entry points | _Open_ |
| Data/config locations | _Open_ |
| Local/remote process model | _Open_ |
| Boundary to surface/callers | _Open_ |
| Verification commands | _Open_ |
| Packaging/distribution | _Open_ |

## Surface Contract
_Fill this in when a feature or project has user-facing work._

| Question | Decision |
|----------|----------|
| Target surface type | _Open_ |
| Target OS/platform | _Open_ |
| Surface language/runtime | _Open_ |
| Local or deployed | _Open_ |
| Boundary to core implementation | _Open_ |
| Launch/preview command | _Open_ |
| Packaging/distribution | _Open_ |

## Project Commands
_No commands yet. Add project-native commands after the stack is chosen._

## Source Layout
_No implementation layout yet. Add folders after the stack is chosen._

## Rejected Options
_None recorded yet._

## Reuse Rule
After this file records a chosen stack, implementation skills must reuse it. Any stack change requires an explicit architecture update.
