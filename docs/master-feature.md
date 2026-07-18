# Master Feature / Product Goal

## Status
Draft template - fill through `/1-csk-init` or backfill through `/csk-refine --master`.

## Purpose
This file is the source of truth for the whole product goal. It describes what the software must accomplish as a complete system, why it should matter, and how individual features contribute to the product promise.

Feature specs describe one releasable slice. This file describes the software as a whole.

## Product Goal
_What must the software be able to do when it works as intended?_

## Unique Value Proposition
_What makes this product meaningfully better, different, faster, safer, cheaper, more reliable, more local, more private, more automated, or more useful than the current alternatives?_

## Target Outcomes
| Outcome | User / Stakeholder | How We Know It Worked |
|---------|--------------------|------------------------|
| _Outcome 1_ | _User_ | _Evidence or metric_ |

## Master Acceptance Criteria
Write system-level acceptance criteria in German:

```markdown
- [ ] Angenommen [System-/Nutzerkontext], wenn [End-to-end-Aktion], dann [messbares Gesamtziel]
```

## Critical User Journeys
| Journey | Start | End | Required Features / Modules |
|---------|-------|-----|-----------------------------|
| _Journey 1_ | _Starting state_ | _Successful outcome_ | _Feature IDs or modules_ |

## System Capabilities
| Capability | Required For | Current Status | Gaps |
|------------|--------------|----------------|------|
| _Capability_ | _Outcome or journey_ | _Unknown / Planned / Built / Verified_ | _Open gap_ |

## Interfaces And Boundaries
List important boundaries that QA must verify across features:

- User-facing surface to core implementation.
- Core implementation to data/storage/config.
- Local process, service, CLI, native, pipeline, job, or external integration boundaries.
- File formats, schemas, contracts, or generated artifacts.
- OS/platform, permission, install, packaging, or runtime boundaries.

## Quality Attributes
| Attribute | Target | Verification Idea |
|-----------|--------|-------------------|
| Reliability | _Target behavior_ | _How QA can check it_ |
| Performance | _Target behavior_ | _How QA can check it_ |
| Security / Safety | _Target behavior_ | _How QA can check it_ |
| Usability / Operability | _Target behavior_ | _How QA can check it_ |

## Frontier AI / Pipeline Needs
_Fill this when the product uses AI, RAG, ML, media, GPU, evaluation, agentic, automation, or data pipelines._

| Pipeline Need | Product Outcome | Quality / Evaluation Target | Open Architecture Question |
|---------------|-----------------|-----------------------------|----------------------------|
| _Need_ | _Outcome_ | _Metric, fixture, benchmark, or review target_ | _Question for /3-csk-architecture_ |

## Local / Cloud / Hybrid Expectations
_Capture product expectations before architecture chooses the implementation._

| Pipeline Step / Data Flow | Preferred Mode | Data Sensitivity | Reason / Constraint | Open Question |
|---------------------------|----------------|------------------|---------------------|---------------|
| _Step_ | _Offline/local, online/cloud, hybrid, or open_ | _Low/medium/high/secret/customer/etc._ | _Privacy, performance, cost, capability, availability_ | _Question_ |

## Feature Contribution Map
| Feature ID | Contribution To Product Goal | Dependencies | System Risk If Missing |
|------------|------------------------------|--------------|------------------------|
| _PROJ-X_ | _Contribution_ | _Dependencies_ | _Risk_ |

## Missing Or Could-Be-Better
Use this section to capture questions that go beyond a single feature:

- What is still missing for the product to reach the master goal?
- Which rough edge weakens the USP?
- Which feature, integration, workflow, or quality improvement would make the software meaningfully better?
- Which hidden dependency or interface could break the whole product later?

## Decision Log
| Decision | Rationale | Date |
|----------|-----------|------|
| _Decision_ | _Reason_ | _YYYY-MM-DD_ |
