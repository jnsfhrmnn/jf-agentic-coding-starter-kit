# Core Engineering Implementation Checklist

## Architecture
- [ ] Read `docs/architecture.md`.
- [ ] Read `docs/master-feature.md`, `docs/engineering-principles.md`, and `.claude/rules/loop-policy.md`.
- [ ] Confirmed non-surface implementation work is required.
- [ ] Confirmed runtime/language/package ecosystem.
- [ ] Confirmed target OS/platforms.
- [ ] Confirmed local vs remote execution boundary.
- [ ] Confirmed offline/local, online/cloud, or hybrid pipeline mode and data movement where relevant.
- [ ] Confirmed frontier AI/current-technology and evaluation assumptions where relevant.
- [ ] Confirmed build/test/package/smoke commands where they exist.
- [ ] Did not introduce unapproved runtimes, package managers, frameworks, databases, queues, local service wrappers, IPC protocols, or deployment mechanisms.

## Existing System
- [ ] Inspected existing modules, entry points, config, tests, and conventions.
- [ ] Identified ownership/module boundary for the feature.
- [ ] Reused existing patterns where possible.
- [ ] Avoided unrelated refactors.

## Implementation
- [ ] Implemented the feature in the approved stack.
- [ ] Inputs and outputs are explicit.
- [ ] Validation happens at trusted boundaries.
- [ ] Errors are meaningful and do not leak secrets.
- [ ] Side effects are idempotent or recoverable where relevant.
- [ ] File paths, encoding, temp files, locking, and cleanup handled where relevant.
- [ ] Local process lifecycle, working directory, env/config, timeouts, and cancellation handled where relevant.
- [ ] Data/schema/migration/index/cache behavior handled where relevant.
- [ ] AI/RAG/ML/media/GPU resource assumptions handled where relevant.
- [ ] Performance-sensitive paths measured or verification gap documented where relevant.
- [ ] Cross-platform differences handled where relevant.

## Integration
- [ ] Connected approved caller: surface, CLI/TUI, library API, worker, hosted API, file/config workflow, or test harness.
- [ ] Did not invent a new boundary when architecture already defined one.
- [ ] Backward compatibility considered for existing callers/data.

## Verification
- [ ] Project-native build/check/test/package/smoke commands run where available.
- [ ] Edge cases from the feature spec addressed.
- [ ] Regression risk in adjacent modules checked.
- [ ] Review-loop gate completed with findings fixed, routed, or explicitly dropped.
- [ ] Verification gaps documented if commands/tools are missing.
- [ ] Feature spec updated with implementation notes.
- [ ] `features/INDEX.md` status updated to `In Progress`.
- [ ] Code committed to git when requested.
