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
| TASK-001 | open | high | .claude/skills/csk-start/scripts/csk_start.py | n/a | 5-csk-backend | Harden the adoption coverage gate against pass-through: require substantive non_feature_reason (class enum plus min length), compare stored inventory_sha256 against the live inventory in state drift checks, widen the inventory heuristic (sql/yaml/proto/tf/Dockerfile/html/css/ipynb, adr/decision/design/konzept keywords, project README), and add negative tests for the unmapped-candidate and blanket-reason paths (adversarial review 2026-07-22) | Design and implement the gate hardening in csk_start.py with tests, then rerun the full validation suites | - | 2026-07-22 |

Completed rows are removed only after evidence is recorded in the owning local
source of truth. Git history provides the audit trail; no separate task archive
is maintained.
