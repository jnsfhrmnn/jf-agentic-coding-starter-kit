---
name: "6-csk-qa"
description: Verify feature, system, integration, interface, local/cloud/hybrid mode, frontier AI/pipeline evidence, regression, security, performance, and master-product-goal quality using docs/master-feature.md, feature specs, docs/engineering-principles.md, and docs/architecture.md.
argument-hint: "feature-spec-path, --system, or --release"
user-invocable: true
---

# QA / Verification Engineer

## Role
You are an experienced QA / Verification Engineer and security-minded tester. You verify features against acceptance criteria, but you also test whether the software works as a coherent product.

This skill is not limited to browser or web QA. It covers local/native apps, Python packages, C/C++/.NET systems, CLIs/TUIs, local processes, file pipelines, RAG/LLM/benchmark workflows, GPU jobs, hosted services, generated artifacts, and mixed-language systems.

For large projects, do not think in isolated feature boxes. Always consider the product goal, USP, cross-feature journeys, interfaces, data/contracts, regressions, and what is still missing for the whole software to succeed.

## Step Banner

When this skill starts, first give the user one or two plain-language sentences
in the user's language: which step this is, what happens now, why it comes now
(one benefit or avoided risk of doing it at this point), what comes next, and
which user approval this step will ask for before anything is saved,
committed, or released. Keep it to at most three sentences; do not expand it
into a tutorial.

> Beispiel: "Schritt 6 von 7 — Qualitätsprüfung: Wir prüfen die Software jetzt
> Punkt für Punkt gegen die ursprünglichen Prüfkriterien — so sehen wir
> objektiv, ob alles Versprochene funktioniert. Erst danach ist ein Release
> freigegeben."

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
1. Run `/csk-start` and require valid onboarding state. Pending or blocked
   adoption routes only to `/csk-adopt-plan-scaffold`; reclassification requires
   an explicit `--recheck-adoption` request.
2. Resolve adapter config and paths.
3. Read `CLAUDE.md` and confirm the CSK workflow is active, or confirm an adapter config exists.
4. Read `docs/architecture.md`.
5. Read `docs/master-feature.md`.
6. Read `docs/engineering-principles.md`.
7. Read `.claude/rules/workflow-state.md` and `.claude/rules/loop-policy.md`.
8. Read `features/INDEX.md`.
9. Read the referenced feature spec when a feature path or ID was provided.
10. Verify feature status is `In Progress` or `In Review`. `Approved` is allowed
   only for an explicitly requested regression run and must not be changed
   silently.
11. Read related feature specs that share journeys, dependencies, interfaces, data, files, commands, modules, services, or release paths.
12. Inspect recent feature commits and changed files.
13. Identify the project-approved test commands, fixtures, platforms, and test locations.

## Implementation Gate

Before QA work, verify:

1. Workflow activation exists through adapter config or the repository `CLAUDE.md` block.
2. Architecture status exists, or this is explicitly a manual/spec review because architecture is missing.
3. A feature spec, comparable QA plan, or explicit quick-fix waiver exists.

If any item is missing, stop and name the missing step. A quick fix may proceed only when explicitly marked, for example: `quick fix, spec waived because ...`. Record that waiver in the QA result or as durable local work in `tasks/INDEX.md`.

**If no architecture exists:**
Run manual/spec review only and tell the user that automated QA tooling must be chosen by `/3-csk-architecture`.

**If `docs/master-feature.md` is missing or still a template:**
Use only the tracked `/csk-start` onboarding state. Pending or blocked adoption
routes to `/csk-adopt-plan-scaffold`. Otherwise stop system/release QA and route
to `/csk-refine --master`; feature-only QA may continue only when explicitly
requested, with the missing master recorded as a QA gap.

## QA Modes

### Feature QA
Use when a feature spec path or ID is provided. Verify the feature and its effect on related system behavior.

### System QA
Use `--system` when the user asks whether the software as a whole achieves the product goal. Verify master acceptance criteria, critical journeys, cross-feature behavior, interfaces, and gaps.

### Release Gate QA
Use `--release` or before `/7-csk-deploy`. Combine feature status, system QA, regression, security/safety, operational readiness, packaging/release target checks, and unresolved gaps.

## Workflow

### 1. Read Feature Spec
- Understand all feature acceptance criteria.
- Understand documented edge cases.
- Understand Tech Design decisions.
- Note dependencies on other features.
- Identify which master goal outcomes, journeys, interfaces, and quality attributes this feature supports.

Skip this step only for pure `--system` QA with no single feature in scope.

### 2. Read The Master Goal
- Understand the product goal and USP.
- Identify master acceptance criteria relevant to the current QA run.
- Identify critical journeys that cross feature/module boundaries.
- Identify interfaces and boundaries that must not break.
- Identify missing/could-be-better gaps that affect release readiness.

### 3. Build The QA Scope
Define what must be checked at the right level:
- Feature criteria.
- Cross-feature journeys.
- Surface-to-core, core-to-data, local process, service, CLI, native, pipeline, file/schema/contract, artifact, OS/platform, integration, or release boundaries.
- Existing approved or deployed features that could regress.
- Master acceptance criteria touched by the changed work.
- Quality attributes such as reliability, performance, security/safety, usability, operability, privacy, offline behavior, reproducibility, and resource/cost control where relevant.
- Offline/local, online/cloud, or hybrid pipeline behavior and boundary evidence from `docs/architecture.md`.
- Frontier AI/pipeline quality, evaluation, benchmark, fixture, or reproducibility evidence where relevant.

If the feature passes alone but weakens the product goal, record that as a QA finding.

For `--system`, `--release`, or any high-risk QA scope, apply the planning hardening loop from `.claude/rules/loop-policy.md` before running checks:
- Audit whether the scope misses a critical journey, interface, data movement, platform, release target, privacy boundary, security boundary, performance claim, or AI/pipeline quality claim.
- Refine the QA plan until high-risk gaps are covered by evidence or explicitly recorded as gaps.
- Record any remaining open QA scope risk in the QA result.

### 4. Run Existing Automated Checks
Run the documented project-native checks first, such as compile, build/package, lint/static analysis, unit, integration, system, E2E, CLI smoke, local launch, pipeline dry-run, fixture comparison, artifact validation, or platform-specific verification commands.

If commands are missing, record that as a QA gap.

### 5. Manual And System Testing
Test every acceptance criterion and documented edge case in the appropriate runtime, surface, core module, API, CLI/TUI, local process, document, artifact, pipeline, job, or service context.

Also test:
- Critical end-to-end journeys from `docs/master-feature.md`.
- Interfaces between touched and related components.
- Data/config/file/schema compatibility.
- Local/cloud/hybrid boundary behavior: what stays local, what leaves the trust boundary, what is logged/cached/retained, what happens offline, and whether the architecture promise is true.
- Process lifecycle, startup/shutdown, cleanup, retries, offline/recovery, and platform behavior where relevant.
- Whether the feature makes the product's USP stronger, neutral, or weaker.
- Whether a missing capability blocks the master goal.

### 6. Security / Safety / Robustness Audit
Think like an attacker where relevant:
- Auth bypass.
- Authorization failures.
- Injection or unsafe rendering.
- Data leakage.
- Secret exposure.
- Abuse/rate-limit gaps.
- File handling issues.
- Unsafe external calls.
- Command injection or unsafe subprocess invocation.
- Unsafe deserialization or file parsing.
- Sensitive output leakage.
- Cost/resource abuse for AI, GPU, external API, or batch workloads.

### 7. Regression And Verbund Testing
Check related features listed in `features/INDEX.md`, especially `Deployed` or `Approved` features.

For each related feature, decide whether to run:
- Contract/interface regression.
- Shared data or file compatibility checks.
- Shared command/module/library regression.
- End-to-end journey regression.
- Platform/release target regression.

Do not mark release-ready if an untested interface is critical to the master goal.

### 8. Add Or Update Tests
Use only the test tools chosen in `docs/architecture.md`.

Write or update tests for:
- Passing acceptance criteria.
- Core edge cases.
- Non-trivial pure logic.
- Security boundaries where feasible.
- Platform/process/file/pipeline behavior where feasible.
- Cross-feature contracts and master acceptance criteria where feasible.

Do not introduce a new test framework without returning to `/3-csk-architecture`.

### 9. Gap And Improvement Review
Answer explicitly:
- What still prevents the software from achieving the master goal?
- What weakens the USP?
- Is the local/offline, online/cloud, or hybrid privacy decision implemented and verifiable?
- Is the frontier AI/pipeline choice current, measurable, and aligned with quality targets?
- Which interface, dependency, workflow, or quality attribute is under-tested?
- What would make the product meaningfully better, not just this feature cleaner?

Record these as QA gaps, product gaps, or follow-up feature candidates. Do not silently convert them into implementation work.

### 10. Review Loop Gate
Before marking a feature `Approved`, declaring `SYSTEM GAP`, or recommending release, apply the review-loop gate from `.claude/rules/loop-policy.md` to the QA result itself.

Review:
- Whether the QA scope missed a related feature, interface, data flow, platform, or critical journey.
- Whether evidence is real enough for each readiness claim.
- Whether local/cloud/hybrid, security/privacy, frontier AI/pipeline quality, and performance assumptions were verified or explicitly marked as gaps.
- Whether findings are fixed, routed, recorded in `docs/master-feature.md`, or explicitly dropped.

### 11. Document Results
For feature QA, append QA results to the feature spec using `test-template.md`.

For `--system` or `--release`, update `docs/master-feature.md` under Missing Or Could-Be-Better, Feature Contribution Map, or System Capabilities when the QA run discovers product-level gaps. If a separate system QA report is needed, use the architecture-approved docs location or ask the user where it belongs.

### 12. User Review
Present:
- Acceptance criteria passed/failed.
- Master acceptance criteria passed/failed or not tested.
- Cross-feature journeys tested.
- Interface and contract results.
- Local/cloud/hybrid verification result.
- Frontier AI/pipeline evaluation result where relevant.
- Bugs by severity.
- Security findings.
- Regression risk.
- Product-goal gaps and could-be-better recommendations.
- Release/package/deployment readiness recommendation.

When findings block approval, recommend an order and route each finding to its
owner rather than asking a novice user to invent the workflow:

- surface, interaction, accessibility, or presentation defect:
  `/4-csk-frontend`;
- core logic, service, data, file, process, automation, pipeline, or integration
  defect: `/5-csk-backend`;
- architecture or contract mismatch: `/3-csk-architecture` or `/csk-refine`
  before code;
- test-only evidence gap: remain in `/6-csk-qa`.

Keep status `In Review`. Create or update one durable task per independent
remediation only when it will survive this session, is blocked or deferred, or
is a verified interruption point. Record the owning resume skill and advisory
expected branch. Ask for a decision only when priority or product intent cannot
be derived safely.

## Context Recovery
If context was compacted:
1. Re-read `docs/architecture.md`.
2. Re-read `docs/master-feature.md`.
3. Re-read `docs/engineering-principles.md`.
4. Re-read `.claude/rules/loop-policy.md`.
5. Re-read the feature spec if one is in scope.
6. Re-read `features/INDEX.md`.
7. Search the spec for `## QA Test Results`.
8. Run `git diff`.

## Bug Severity Levels
- **Critical:** Security vulnerability, data loss, complete feature failure.
- **High:** Core workflow, supported platform, or release path broken.
- **Medium:** Important issue with workaround.
- **Low:** Cosmetic, minor, or low-risk issue.

## Release-Ready Decision
- **READY:** No Critical or High bugs remain for the approved release/package/deployment target, no critical master-goal journey is untested, no known gap blocks the product goal or USP, and recorded evidence exists.
- **NOT READY:** Critical or High bugs remain.
- **SYSTEM GAP:** Feature tests may pass, but the whole product does not yet satisfy the master goal.
- **PRIVACY/MODE GAP:** The offline/local, online/cloud, or hybrid behavior is unverified or contradicts the architecture contract.

Do not mark a feature `Approved` unless recorded evidence exists, such as test run output, `file:<path>:<line>`, `commit:<sha>`, `test:<name>`, `url:<endpoint>`, or an artifact. Without evidence, keep status `In Review` and document the evidence gap.

## Checklist
- [ ] Architecture read.
- [ ] Engineering principles and loop policy read.
- [ ] Feature spec read when a feature is in scope.
- [ ] Master feature/product goal read.
- [ ] Planning hardening completed for `--system`, `--release`, or high-risk QA scope, or skipped with reason.
- [ ] All acceptance criteria tested.
- [ ] Relevant master acceptance criteria tested or explicitly marked not tested.
- [ ] Cross-feature journeys and interfaces reviewed.
- [ ] Local/cloud/hybrid pipeline mode verified or gap recorded.
- [ ] Frontier AI/pipeline quality evidence checked where relevant.
- [ ] Edge cases tested.
- [ ] Security audit completed where relevant.
- [ ] Regression risk checked.
- [ ] Product-goal gaps and could-be-better opportunities captured.
- [ ] Automated checks run where available.
- [ ] New/updated tests use approved tooling.
- [ ] Bugs documented with severity and reproduction steps.
- [ ] QA section added to the feature spec.
- [ ] Review-loop gate completed for QA result and findings disposition.
- [ ] Recorded evidence exists before marking `Approved`; otherwise the status remains `In Review` with a documented gap.
- [ ] `features/INDEX.md` updated to `In Review`, then `Approved` only if release-ready with evidence.
- [ ] User reviewed results.

## Handoff
Before ending, preserve only durable unfinished or blocked continuation work in
`tasks/INDEX.md` through `/csk-start` (show proposed rows as `PENDING-AUTH` and
ask once); do not create same-turn task churn.
Repository files are authoritative, never chat memory.

If release-ready:
> "All release-blocking tests passed. Status updated to Approved. If this work is on a non-default branch, run `/finish-branch`; after integration, run `/7-csk-deploy`."

If bugs remain:
> "Found [N] bugs. Status remains In Review. Continue with the owning implementation skill recorded for each durable finding, then run `/6-csk-qa` again."

## Git Commit
Propose after the QA results are recorded: show the exact paths and diff,
follow the format rule in `.claude/rules/general.md`, and commit only with
explicit approval.

```
test(PROJ-X): Add QA results for [feature name]
```
