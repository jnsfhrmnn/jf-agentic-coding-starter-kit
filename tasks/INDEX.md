# Open Work Index

<!-- next-id: TASK-002 -->

This file is the single source of truth for immediate unfinished work that must
survive across sessions. It contains only `open` and `blocked` items. Feature
scope and status remain in the related feature specification.

Create a row only for work that remains open/blocked, spans the current session,
is explicitly deferred, or is a verified interruption point. `Expected branch`
is advisory; live Git state is authoritative. `Resume skill` must be a
runtime-neutral repository skill name such as `csk-adopt-plan-scaffold`.

| ID | Status | Priority | Related | Expected branch | Resume skill | Task | Next action | Blocker | Updated |
|---|---|---|---|---|---|---|---|---|---|
| TASK-001 | open | medium | .claude/skills/csk-start/scripts/csk_start.py | n/a | 5-csk-backend | Remaining adoption-gate bypass hardening (core inventory/reason hardening shipped in kit 1.3.0): re-validate coverage-report internals during state check so a hand-edited complete state with format-valid fake digests cannot pass, and surface inventory growth since adoption as advisory information on an explicit recheck | Extend validate_state/state_drift in csk_start.py with report re-validation plus advisory inventory-growth reporting, with negative tests | - | 2026-07-22 |

Completed rows are removed only after evidence is recorded in the owning local
source of truth. Git history provides the audit trail; no separate task archive
is maintained.
