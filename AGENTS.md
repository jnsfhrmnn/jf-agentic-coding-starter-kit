# Codex Repository Instructions

<!-- CODEX_CLAUDE_COMPATIBILITY -->

This starter kit supports both Codex and Claude. `CLAUDE.md` and the repository
rules define the shared workflow; these instructions add the Codex entry point.

## Session Start

1. Inspect the skills and tools currently available.
2. Prefer an applicable skill when one exists. Use deterministic tools for
   mechanical checks and LLM judgment for semantic, contextual, or
   non-deterministic decisions.
3. Read `CLAUDE.md` and relevant `.claude/rules/`.
4. Run `$csk-start` before selecting work. It validates the tracked first-use
   decision in `.csk/project-state.json`, routes adopted repositories to
   `$csk-adopt-plan-scaffold`, and then reads `tasks/INDEX.md` plus live Git state.
5. Follow `.claude/rules/workflow-state.md` as the routing and transition SSOT.

## Claude And Codex Skills

- Canonical skills live only in `.claude/skills/`.
- Ready-to-use Codex proxies live only in `.codex/skills/` and load their
  canonical Claude skill at runtime.
- Never install, copy, or synchronize kit skills into a user's global Claude or
  Codex directories.
- Run `$claude-skill-proxy-sync` after adding, renaming, moving, or removing a
  canonical skill, or after changing its frontmatter trigger/UI metadata.
- Ordinary canonical skill body and resource changes do not require a sync.
- `/csk-adopt-plan-scaffold` / `$csk-adopt-plan-scaffold` is required and must
  remain bundled.
- `/finish-branch` / `$finish-branch`, `/audit-plan-loop` / `$audit-plan-loop`,
  and `/review-loop` / `$review-loop` are required and must remain bundled.

## Work Rules

- Codex may perform productive repository work; it is not restricted to review.
- Use source-of-truth files instead of duplicating state. `features/INDEX.md` and
  feature specs own feature state; `tasks/INDEX.md` owns immediate open or blocked
  durable continuation work; `.csk/project-state.json` owns onboarding state.
- Create task rows only for work that survives the current session, is blocked or
  deferred, or is a verified interruption point.
- After verified work on a non-default branch, use `$finish-branch`; Git and
  external mutations still require explicit authority.
- Read files before modifying them, preserve unrelated user changes, and verify
  edits and tests before claiming completion.
- Change `CLAUDE.md` only with concrete user authorization for that change.
- Keep all generated proxy paths repository-relative and reject global fallbacks.
