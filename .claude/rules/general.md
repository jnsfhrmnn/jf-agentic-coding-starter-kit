# General Project Rules

## Start and capability discovery

- On every repository open, inspect available tools and repository-local skills,
  then run `/csk-start` before selecting productive work.
- Prefer an applicable skill and read its complete `SKILL.md` before acting.
- Use deterministic tooling for syntax, validation, state transitions, locking,
  and repeatable checks. Use LLM context judgment for semantic classification,
  relevance, ambiguity, design tradeoffs, and other non-deterministic decisions.
- `.csk/project-state.json` owns the tracked first-use/adoption decision.
  `tasks/INDEX.md` owns immediate durable open work. Follow
  `.claude/rules/workflow-state.md` for routing and status transitions.
- Never claim that chat-only work is durably conserved.

## Repository-local skills

- Canonical CSK skills live in `.claude/skills/`; generated Codex proxies live
  in `.codex/skills/`. Both remain inside the repository and travel through Git.
- Never install, copy, deploy, or synchronize kit skills into a user's global
  Claude or Codex skill directory.
- Keep `/csk-adopt-plan-scaffold`, `/finish-branch`, `/audit-plan-loop`,
  `/review-loop`, and `/claude-skill-proxy-sync` in the kit.
- Run `/claude-skill-proxy-sync` after adding, renaming, moving, or removing a
  canonical skill, or after changing trigger/interface frontmatter. Canonical
  body and resource changes are read through the proxy and need no regeneration.

## Project and adoption gates

1. Run the `/csk-start` state gate. Never infer an uninitialized or greenfield
   project from missing or invalid state.
2. If adoption is pending or blocked, run `/csk-adopt-plan-scaffold` before
   initialization, refinement, specification, architecture, or implementation.
3. Resolve optional path overrides only from repository-root `csk.config.json`
   according to `.claude/rules/adapter-config.md`.
4. Read the adapter-resolved PRD, master feature, engineering principles,
   architecture, feature index, and applicable feature specs.
5. If the PRD is still a template or the feature index is empty, do not choose a
   product stack or write implementation. Route the user's product idea to
   `/1-csk-init`.
6. If the product is initialized but the master feature remains a template, run
   `/csk-refine --master` before deep implementation, system QA, or release.
7. If requested scope has no feature, run `/2-csk-write-spec` before architecture
   or implementation.

## Single sources of truth

- Product decisions: adapter-resolved `docs/PRD.md`.
- Whole-product goal, journeys, interfaces, acceptance criteria, and gaps:
  adapter-resolved `docs/master-feature.md`.
- Quality, current-technology, processing-mode, performance, security, review,
  and evidence expectations: `docs/engineering-principles.md`.
- Technology and project commands: adapter-resolved `docs/architecture.md`.
- Feature overview and status: adapter-resolved `features/INDEX.md`.
- Feature scope, decisions, and evidence: one owning feature spec.
- Immediate open or blocked continuation work: `tasks/INDEX.md`.
- Workflow transitions and skill contracts: `.claude/rules/workflow-state.md`.

Reference these sources instead of duplicating their contents. When two owning
files conflict, report drift and repair it before advancing.

## Technology ownership

- The kit has no default application stack.
- `/3-csk-architecture` chooses technology, or verifies an already documented
  choice in an adopted project.
- Check fast-moving technology against current primary sources at architecture
  time. Record local/offline, online/cloud, or hybrid mode for relevant flows.
- Implementation skills must not introduce an unapproved framework, package
  manager, database, auth provider, deployment target, or test runner.
- If the documented stack no longer fits, pause and revise the decision through
  `/csk-refine` or `/3-csk-architecture` before changing code.

## Feature and task tracking

- Feature IDs are sequential, one feature per spec. Check existing files first.
- Follow the lifecycle and entry/exit contracts in
  `.claude/rules/workflow-state.md`; do not maintain another transition table.
- Update a feature spec and feature index together, then reread both.
- `Approved` requires recorded QA evidence. `Deployed` requires release evidence
  plus the final post-release review. `Cancelled` requires a one-line reason.
- Create a task only for work that remains open or blocked, will span a session,
  is explicitly deferred, or is a verified interruption/resume point. Ordinary
  same-turn work creates no task-row churn.
- Unfinished work already inside an authorized repository change may be
  checkpointed. Ask once before storing newly discovered, deferred, or
  out-of-scope follow-ups; until then show them as `PENDING-AUTH`.
- Close tasks only through `/csk-start` with typed evidence. Without repository
  write authority, show one exact `PENDING-AUTH` proposal instead of writing.

## Git and external actions

- Commit format: `type(PROJ-X): description` for feature-bound work; allowed
  types are `feat`, `fix`, `refactor`, `test`, `docs`, `deploy`, and `chore`.
  Project-wide documentation or workflow changes without one owning feature may
  use `type: description` without a scope.
- Inspect live branch, worktree, remotes, and operation state before Git changes.
- Verification never grants authority to commit, push, merge, create a pull
  request, tag, release, deploy, or delete a branch. Obtain explicit authority
  for the external or destructive action in scope.
- After verified work on a non-default branch, recommend `/finish-branch`.
- Never force-push. Never push project changes to an upstream template remote.

## Human decisions and review

- Ask for approval before finalizing PRDs, specs, architecture decisions, and
  deployments. Give a recommendation with decision questions.
- Never silently pass a phase gate. Follow `.claude/rules/loop-policy.md` for
  mandatory planning and implementation reviews.
- Remediation findings route to the owning skill and remain visible until fixed,
  accepted, or recorded as a durable blocker.

## File handling and handoff

- Read before editing; after context compaction, reread affected files.
- Use `rg --files` or `git ls-files` before guessing paths or implementation.
- Preserve unrelated user changes and verify with tests plus `git diff`.
- After a skill, report evidence and the next user-controlled action in the form
  `Next step: Run /skillname to ...` when another skill is appropriate.
- Before ending authorized non-trivial work, preserve only real durable follow-up
  through `/csk-start`; leave the task index unchanged when none exists.
