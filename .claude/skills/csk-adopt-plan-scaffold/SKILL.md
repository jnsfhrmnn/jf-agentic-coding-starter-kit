---
name: csk-adopt-plan-scaffold
description: Exhaustive repository-local CSK adoption workflow for an existing codebase or project with implementation, plans, roadmaps, audits, backlogs, architecture, requirements, tests, handoffs, or product sources of truth. Use when .csk/project-state.json says adoption is pending or blocked, when a repository must be reverse-engineered before feature specification, or when existing evidence must become a provisional source-linked feature scaffold. Reads only the current repository and records completion or blockers through csk-start.
---

# CSK Adopt Plan Scaffold

## Objective

Treat the current repository as an existing product, not greenfield. Inventory
and read its relevant local code, plans, and sources of truth. Derive a
provisional feature scaffold that preserves confirmed decisions, implemented
maturity, known gaps, and source links. Review proposals with the user before
returning to the numbered CSK workflow.

## Entry contract

1. Resolve the current Git root dynamically and read repository instructions.
2. Run `/csk-start` state validation. Normal entry is
   `project/adopt/pending` or `project/adopt/blocked`.
3. If state is pending first-use classification, return to `/csk-start`; this
   skill must not make or store that decision implicitly.
4. Resolve source-of-truth paths only from repository-root `csk.config.json` and
   `.claude/rules/adapter-config.md`.
5. Read the canonical `/1-csk-init` skill and apply its adopt semantics when CSK
   product files are incomplete.

## Boundaries

- Inspect only the current repository. Do not read another repository, global
  task store, message broker, or external workflow state.
- Preserve user changes, dirty worktrees, and files with unclear ownership.
- Change protected files only with concrete authority for that file.
- Do not claim complete coverage until inventory, full-text reading, and mapping
  verification are complete.
- Do not substitute filenames, headings, search hits, or summaries for reading
  every relevant text artifact through EOF.
- Do not implement product code or create individual feature specs during the
  scaffold step.
- Mark derived entries provisional. Technical implementation does not by itself
  prove product approval or release status.
- Preserve decisions already stored in repository files or made in the current
  conversation; reopen them only when contradictory evidence requires it.

## Phase 1: Inventory repository evidence

Use `git ls-files`, `rg --files`, and targeted searches. Include tracked and
relevant untracked content; exclude `.git`, dependencies, caches, generated
output, builds, temporary files, vendored trees, and the starter-kit templates
themselves unless a project has intentionally filled them.

Search at least:

- implementation roots, package/module manifests, build files, and entry points;
- tests, fixtures, CI, release, packaging, and deployment configuration;
- plans, plan indexes, backlogs, portfolios, roadmaps, milestones, briefs,
  requirements, handoffs, and status records;
- PRDs, product vision, feature indexes, existing feature specs, user journeys,
  and acceptance criteria;
- architecture records, ADRs, diagrams, API or schema contracts, data-flow and
  security documentation;
- audits, reviews, remediation records, gaps, and operational runbooks;
- capability or gap inventories and other locally authoritative indexes.

For every candidate, record relative path, artifact class, title/purpose,
discovery source, read status, and product relevance. Reconcile indexes with
physical files: indexed-and-present, indexed-but-missing, present-but-unindexed,
or supporting artifact rather than independent scope.

## Phase 2: Read and classify evidence

Read every relevant text artifact through EOF in controlled batches. Inspect
non-text artifacts with an applicable repository/runtime skill when their content
is necessary. Extract:

- problem, objective, user or operational value, and product boundary;
- maturity and direct implementation/test evidence;
- dependencies, prerequisites, acceptance criteria, and non-goals;
- data, security, privacy, licensing, egress, and operating assumptions;
- open decisions, known gaps, conflicts, and supersession evidence;
- source links, commits, and other repository-local proof.

Classify each artifact as current, historical, superseded, resolved,
cross-cutting, generated, vendored, tooling-only, or unresolved. Preserve
contradictory claims with paths and evidence maturity. Prefer explicit ownership,
supersession, and direct proof—not file dates alone.

## Phase 3: Consolidate product knowledge

Separate evidence into:

1. confirmed product decisions;
2. derived current capabilities and maturity;
3. open gaps, contradictions, and undecided contracts.

Define features by user outcome and testable product contract, not by renaming
files or plan nodes. Several implementation artifacts may support one feature;
cross-cutting evidence may support several.

## Gate before writing

Write only when:

- all relevant local indexes and artifacts were read;
- every discovered scope source maps to a feature candidate or an explicit
  non-feature classification;
- known decisions and conflicts are recorded;
- existing feature files and the current Git diff were inspected;
- the adapter-resolved destination is confirmed.

If required local evidence is missing or unreadable, run the csk-start helper's
`state adoption-block --reason ...`, add/update one durable blocked task with the
exact recovery action, and stop. Do not present dependent claims as confirmed.

## Phase 4: Write the provisional scaffold

Integrate with the adapter-resolved feature index, normally
`features/INDEX.md`; preserve useful existing content and unrelated changes.
Include:

1. provisional-adoption status, date, source basis, and traceable counts;
2. confirmed product basis and uncertainty labels;
3. review groups by user journey or product boundary;
4. unique provisional `PROJ-*` IDs, titles, outcomes, priority, dependencies,
   `Roadmap` status, current evidence, and first known gap;
5. relative links from each feature to its supporting local sources;
6. an explicit mapping for historical, resolved, cross-cutting, generated,
   vendored, and tooling-only sources;
7. source-of-truth drift, cross-cutting gaps, review order, and next unused ID.

Do not create an empty greenfield list. Pre-fill what evidence proves and label
everything else provisional.

Also write `.csk/adoption-coverage.json` as machine-readable proof:

```json
{
  "schema_version": 1,
  "feature_index": "features/INDEX.md",
  "sources": [
    {
      "path": "relative/source-path",
      "feature_ids": ["PROJ-1"],
      "non_feature_reason": null,
      "manual_relevance_reason": null
    }
  ]
}
```

Every inventoried source appears exactly once. Map it to one or more real feature
rows, or use an empty `feature_ids` list plus a substantive
`non_feature_reason` in the form `<class>: <specific justification>`, where
`<class>` is one of `cross-cutting`, `generated`, `historical`, `non-product`,
`resolved`, `superseded`, `tooling-only`, or `vendored` and the justification
names why THIS source is not product scope (blanket one-word reasons are
rejected mechanically). A relevant source outside the deterministic inventory
also requires a substantive `manual_relevance_reason`; this makes the LLM's
semantic override explicit and reviewable. Never type summary counts by hand;
the deterministic tool derives them from this report and the current
inventory.

## Phase 5: Verify mechanically and semantically

Verify:

- every relevant source maps to a candidate or explicit non-feature class;
- every relative link resolves inside the repository;
- feature IDs are unique and the next ID is correct;
- dependencies reference existing IDs and cycles are absent or explicitly open;
- status and maturity claims do not exceed evidence;
- historical or superseded material is not presented as current architecture;
- feature links and classifications semantically match the source content;
- the deterministic `state adoption-complete --coverage-report ...` validation
  accepts the report, derives complete coverage, and rejects empty scaffolds;
- `git diff` contains only intended changes plus preserved user work.

For a large inventory, run a machine-readable coverage check and report counts.
A sample is not proof of complete coverage.

## Phase 6: Review and persist the adoption result

Review feature candidates one at a time, starting with the earliest dependency.
Ask one bounded question at a time and lead with a sourced recommendation. Cover
user value, release scope, roles, data lifecycle, processing/egress, failure and
abuse cases, quality/security/performance evidence, dependencies, and non-goals.

A candidate may be confirmed, renamed, split, merged, reprioritized, deferred,
or rejected with a reason. Do not create every feature spec automatically.

When the scaffold and its coverage are verified, run:

```text
csk_start.py state adoption-complete --coverage-report .csk/adoption-coverage.json
```

Then reread `.csk/project-state.json` and the scaffold. Completion state must
point to the validated coverage report, its digest, the feature index, and
derived coverage counts. If completion cannot be proved, keep adoption pending
or blocked; never mark it complete optimistically.

## Exit and continuation

Report inventory counts, scaffold path, candidate/review-group counts, coverage
result, remaining drift or blockers, and the next candidate to review.

After a confirmed candidate:

1. `/2-csk-write-spec` creates its full spec.
2. `/3-csk-architecture` owns stack and design decisions.
3. `/4-csk-frontend` and/or `/5-csk-backend` implement approved design.
4. `/6-csk-qa` verifies it.
5. `/finish-branch` safely closes non-default branch work.
6. `/7-csk-deploy` releases only an `Approved` feature.

Before exit, keep exactly one durable task for unfinished or blocked adoption
work when repository writes are authorized. Create no task for work expected to
finish in the same turn.
