# AI Coding Starter Kit

Technology-neutral, repository-local workflow for Claude Code and Codex. The
project stack is chosen by `/3-csk-architecture`, never by this template.

## Start every repository session

1. Inspect the skills and tools available in the runtime and this repository.
2. Read every applicable skill before acting; explicitly requested skills are
   mandatory. Prefer a suitable skill over an improvised workflow.
3. Run `/csk-start` before product or implementation work. It validates
   `.csk/project-state.json`, reads durable work from `tasks/INDEX.md`, and
   reconciles live Git state.
4. On the first project use only, `/csk-start` inventories the repository and
   asks whether existing code or product/planning evidence must be adopted. The
   tracked answer applies to all clones after its commit reaches the default
   branch. `yes` routes to `/csk-adopt-plan-scaffold`; `no` continues greenfield.
5. Follow `.claude/rules/workflow-state.md` for the one authoritative routing and
   status-transition model.

Use deterministic tools for repeatable mechanical work such as parsing,
validation, locking, and atomic state changes. Use LLM context judgment for
semantic relevance, ambiguity, design tradeoffs, and decisions that cannot be
reduced to one fixed algorithm. The opposite of deterministic is
**non-deterministic**.

## Local skills and agent compatibility

- Canonical skills live in `.claude/skills/`; ready Codex proxies live in
  `.codex/skills/`. `AGENTS.md` is the Codex entry point.
- Never install or synchronize kit skills into a user's global Claude or Codex
  directories.
- Run `/claude-skill-proxy-sync` after adding, renaming, moving, or removing a
  canonical skill or changing its trigger/interface metadata. Users can use the
  same skill to sync their own repository-local additions.
- Required workflow skills include numbered steps 1–7, `/csk-start`,
  `/csk-adopt-plan-scaffold`, `/finish-branch`, `/audit-plan-loop`,
  `/review-loop`, `/csk-refine`, and `/csk-help`.

## Core workflow rules

- Sources of truth: product in `docs/PRD.md`; whole-product contract in
  `docs/master-feature.md`; quality in `docs/engineering-principles.md`;
  technology in `docs/architecture.md`; feature state/details in
  `features/`; durable open work in `tasks/INDEX.md`.
- Use `csk.config.json` only for repository-local path/workflow adaptation.
- Do not select frameworks, runtimes, package managers, storage, tests, release
  targets, or generated scaffolds before architecture approves them.
- Preserve unrelated user changes; read before editing and verify after writing.
- Create a task only for work that remains open/blocked, spans a session, is
  deferred, or is a verified interruption point. Do not create same-turn churn.
- Use `/audit-plan-loop` for non-trivial plans and `/review-loop` for productive
  artifacts according to `.claude/rules/loop-policy.md`.
- QA findings return to the owning implementation skill and remain `In Review`
  until verified. Releases require both a pre-release readiness review and a
  final review of the actual result before `Deployed` bookkeeping.
- After verified work on a non-default branch, route to `/finish-branch` for safe
  commit, integration, and optional cleanup.
- Verification never authorizes commit, push, merge, pull request, tag, release,
  deployment, or deletion. Obtain explicit authority for those actions.

## Workflow

`/1-csk-init` → `/2-csk-write-spec` → `/3-csk-architecture` →
`/4-csk-frontend` and/or `/5-csk-backend` → `/6-csk-qa` →
`/finish-branch` when needed → `/7-csk-deploy`

@.claude/rules/general.md
@.claude/rules/workflow-state.md
@.claude/rules/loop-policy.md
@.claude/rules/adapter-config.md
@docs/PRD.md
@docs/master-feature.md
@docs/engineering-principles.md
@docs/architecture.md
@features/INDEX.md
@tasks/INDEX.md
