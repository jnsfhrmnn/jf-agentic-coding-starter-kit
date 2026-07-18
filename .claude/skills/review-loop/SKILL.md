---
name: review-loop
description: "Deep, iterative, evidence-based review of existing repository artifacts such as code, architecture, plans, specifications, prompts, skills, rules, configuration, documentation, tests, and release output. Use when asked to review, audit, harden, verify, or refine completed work; after productive changes covered by .claude/rules/loop-policy.md; or when reviewing the current session delta, an explicit target, or all session work. Produces an authority-aware local disposition for every real finding: persist it only when repository writes are authorized, otherwise name its exact proposed SSOT or task target as PENDING-AUTH."
---

# Review Loop

Review existing work adversarially until coverage and evidence converge. The
goal is to find real weaknesses, not to generate a long list or defend earlier
work.

## Determine Authority And Mode

Respect the authority of the current user request:

- **Audit-only:** default when the user asks to review, diagnose, inspect, or
  report. Read and verify, but do not mutate the reviewed artifacts.
- **Review + fix:** use when the user explicitly requests fixes, uses `--fix`, or
  the review is a verification phase inside an already-authorized build/change
  task. Keep fixes inside that authorized scope.
- **Non-mutable target:** always audit-only.

Never commit, publish, deploy, contact another repository, or broaden scope
unless the current request separately authorizes it.

## Resolve Scope

Choose one scope before reviewing:

1. An explicit path, module, diff, PR, or named artifact overrides all defaults.
2. With no target, review the current session delta: every artifact created or
   changed since the last completed review-loop pass. Include staged,
   unstaged, untracked, and committed session work plus non-code artifacts.
3. `--all` reviews all work produced in the session, even if reviewed earlier.
4. `--deep` increases depth, not scope.
5. `--panel` requests independent reviewers for distinct dimensions.

List the concrete inventory before classification. Do not sample silently. If
earlier review coverage cannot be reconstructed after context compaction, state
the uncertainty and use an explicit target or conservative full coverage.

For more than roughly eight materially different artifacts, present a compact
coverage proposal and ask only if choosing full review versus risk-focused
triage would materially change time or outcome.

## Classify The Artifacts

Always check these core dimensions:

- correctness and consistency with requirements and SSOTs;
- completeness and missing paths;
- robustness, edge cases, and failure recovery;
- security, privacy, abuse, secrets, and data locality;
- performance, scalability, and resource use where relevant;
- interface, schema, and compatibility risk;
- maintainability, drift, and regression risk;
- evidence quality.

Add the applicable type lens:

| Type | Additional focus | Preferred evidence |
|---|---|---|
| Code/architecture | boundaries, concurrency, complexity, error handling, tests | project-native test/lint/typecheck/build/diff |
| Gate/guard | fail-closed behavior, bypasses, false positives/negatives | positive and negative trigger cases |
| Plan/spec/design | goals, acceptance criteria, assumptions, feasibility, alternatives | requirements and SSOT comparison |
| Config/infra/schema | safe defaults, validation, idempotence, migration/rollback, secrets | parser, validator, lint, dry run |
| Prompt/skill/rule | trigger precision, ambiguity, precedence, scope, counterexamples | validator plus realistic trigger/non-trigger cases |
| Documentation | accuracy against repository reality, paths, commands, links | path/link/command checks |
| Data/content | provenance, semantic consistency, completeness, sensitive data | source comparison plus LLM semantic review |
| Process/workflow | happy path, failures, ownership, restartability, lost-task risk | walkthrough and failure simulation |

Apply multiple lenses when an artifact has multiple roles. For an unknown type,
derive and state the most relevant quality and failure dimensions from first
principles.

## Use Evidence Safely

- Read repository instructions and architecture before selecting commands.
- Use deterministic checks for mechanical facts and LLM judgment for semantic
  intent, coherence, omissions, and trade-offs.
- Show actual sanitized evidence: exit code, test result, diff, path/line, or
  fact checked against its source.
- Label anything that cannot be verified as `unverified`; never report false
  green.
- Inspect unfamiliar scripts and dependency hooks before executing them.
- Reuse existing processes where possible. Stop any temporary server, watcher,
  or process started solely for verification.
- Never expose secrets, credentials, private data, or raw sensitive output.

For code, explicitly consider injection, authorization, input validation,
output encoding, path traversal, unsafe subprocesses, secrets, cryptography,
deserialization, uploads, SSRF, concurrency, dependency risk, insecure defaults,
and fail-open error handling when applicable.

## Finding Model

Every finding records:

```text
ID | artifact/location | dimension | severity | confidence | problem | evidence | recommendation | status
```

Severity is `critical`, `high`, `medium`, or `low`. Confidence is 0–100 and
measures whether the diagnosis is correct, not its impact. Prioritize by both.
Do not silently filter uncertain high-impact suspicions; verify them before a
fix. Do not inflate style preferences or pre-existing unrelated issues into
findings.

## Run The Review

### Phase A: Scope And Baseline

- Read `AGENTS.md`, `CLAUDE.md`, applicable skills/rules, and `tasks/INDEX.md`.
- Inventory and classify every artifact in scope.
- Record Git/status baseline without modifying or hiding user changes.
- Select the project-native evidence for each artifact.

### Phase B: Review Each Artifact

For each artifact, up to 12 iterations but stopping early on convergence:

1. **STAND:** identify artifact, type, and intended contract.
2. **CRITIQUE:** apply core dimensions, type lenses, edge cases, and evidence.
3. **DECIDE:** select verified findings in severity/confidence order.
4. **REFINE:** only in authorized Review + fix mode; use the smallest coherent
   change and preserve unrelated work.
5. **VERIFY:** rerun the relevant checks and inspect the actual diff.
6. **CONVERGENCE:** stop when no critical/high finding remains and another pass
   finds no substantial new issue.

Log compactly:

```text
Artifact <path>, iteration N — findings: C/H/M/L | fixed: <IDs> | open: <IDs> | evidence: <result>
```

### Phase C: Cross-Artifact Pass

Check the in-scope set for contradictions, missing connections, ripple effects,
interface drift, duplicated SSOT state, and whether the combined result solves
the stated problem. This pass remains limited to artifacts and state inside the
current repository.

## Independent Verification

Before fixing a critical/high finding below 90 confidence, ask an independent
agent to try to disprove it when one is available. Give it the artifact, claimed
defect, applicable contract, and verification tooling, but not the desired
conclusion. If no agent is available, perform and log a contrary refutation pass
in the current context.

Use `--panel` by assigning distinct dimensions to independent agents, then
deduplicate their evidence. For a reproducible finding at confidence 90 or
above, a logged cause/fix confirmation may replace fan-out.

## Phase D: Local Finding Disposition

Give every real finding exactly one terminal disposition. Persist findings only
when the current request already authorizes repository writes. In audit-only
mode without that authority, do not mutate a source of truth merely to satisfy
this phase; prepare the exact proposed target and use `PENDING-AUTH`.

- `FIX-DONE`: fixed in authorized scope and verified.
- `OWNER-SSOT`: recorded in the relevant feature spec, master feature,
  architecture record, QA evidence, or release record.
- `TASK-INDEX`: continuation recorded once in `tasks/INDEX.md` through
  `/csk-start`, linked to its owner, only when it remains open/blocked, will span
  the current session, is explicitly deferred, or is a verified interruption
  point. Do not create and close a row for same-turn review/fix work.
- `ASK`: a material user decision is still required; persist a blocked task only
  when that decision must survive beyond the current session and repository
  writes are authorized.
- `PENDING-AUTH`: audit-only finding with an exact proposed local SSOT/task
  target, awaiting permission to persist it.
- `DROP`: false positive, accepted risk, or explicitly rejected item with reason.

Use the narrowest existing SSOT. Do not duplicate feature status in the task
index. With write authority, keep the complete review record and every
continuation inside the current repository. Without it, name that exact local
target without writing.

The completion invariant is:

```text
all findings == FIX-DONE + OWNER-SSOT + TASK-INDEX + ASK + PENDING-AUTH + DROP
undisposed findings == 0
```

An `ASK` is durably complete only after its blocked continuation is stored
locally. `PENDING-AUTH` makes the read-only report complete but not durably
conserved; state that limitation and request one consolidated authorization.
If the invariant does not balance, the review is not complete.

## Final Handoff

Report:

1. scope and coverage;
2. findings ordered by severity and confidence;
3. fixes and actual verification evidence, if authorized;
4. cross-artifact risks;
5. every local disposition and the balanced completion invariant;
6. anything unverified or deliberately not reviewed.
