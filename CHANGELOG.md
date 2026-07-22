# Changelog

All notable public changes to this project are documented here.

The current kit version lives in the root `VERSION` file; the top entry here
must always match it.

## 1.2.0 - 2026-07-22

- Added `docs/git-basics.md`: bilingual Git concepts for beginners, the
  three-level parallel-work decision guide, the orchestrator/worker worktree
  cycle, and a plain-language table for every safety stop.
- Added the `create-worker-worktree` and `pull-main-ff` skills with
  fail-closed Python tooling: permanent worker worktrees on protected
  `<worker>-workbench` branches, fast-forward-only default-branch updates,
  and a merge-commit gate against work that bypassed the pull-request door.
- Made `pull-main-ff` context-sensitive - one command for both sides: on the
  default branch it fast-forwards; on a protected worker branch it re-syncs
  onto the new default and fast-forward-pushes the remote ref (restoring it
  after host auto-delete), refusing fail-closed while unmerged worker
  commits exist.
- Added an advisory session guard to `csk-start` that warns when a second
  agent session shares one working copy.
- Hardened `finish-branch`: protected worker branches are never deleted and
  are re-synced after a real merge commit; every approval and stop now
  carries a plain-language sentence.
- Recorded the parallel-session model in the workflow-state SSOT and banned
  destructive Git techniques kit-wide.
- Added the canonical root `VERSION` file; the kit version is shown at
  session start and checked for consistency by the contract tests.
- Expanded the README since 1.1.0: five-line task-system guide, Git-safety
  and adoption sections, an honest two-sided framework comparison, and
  credential-intake guidance for beginners.

## 1.1.0 - 2026-07-18

- Added a branch lifecycle rule: a one-time branch question before
  implementation, checkpoint commits after verified increments, and completion
  only through `finish-branch`.
- Added beginner step banners: every workflow skill now opens with one or two
  plain-language sentences explaining what happens and why.
- Added a feature-collection gate before the architecture decision and a
  bilingual "Why this order?" rationale to the README.
- Clarified the commit-format rule for project-wide changes, the pull-request
  check timeout, the evidence-record location, and the onboarding gate in the
  implementation skills.

## 1.0.0 - 2026-07-18

- Published the technology-neutral AI development starter kit for Claude Code
  and Codex.
- Added repository-local canonical Claude skills and ready-made Codex proxies.
- Added a Git-tracked first-use decision for greenfield and existing projects.
- Added deterministic session startup and durable task continuity.
- Added a shared workflow-state source of truth for planning, architecture,
  implementation, QA, release, and cancellation.
- Added adoption, review-loop, audit-plan-loop, skill-sync, and safe
  finish-branch workflows.
- Added upstream attribution, MIT terms, bilingual beginner documentation,
  requirements, and automated public-release validation.
