# Surface / Interface Implementation Checklist

Before marking user-facing surface work complete:

## Architecture
- [ ] Read `docs/architecture.md`.
- [ ] Read `docs/master-feature.md`, `docs/engineering-principles.md`, and `.claude/rules/loop-policy.md`.
- [ ] Confirmed the target surface type, OS/platform, language/runtime, source layout, presentation approach, and commands.
- [ ] Confirmed the boundary to the core implementation: embedded module, local process, localhost service, IPC, file exchange, stdin/stdout, database, or external API.
- [ ] Confirmed offline/local, online/cloud, or hybrid implications visible to users.
- [ ] Did not introduce unapproved frameworks, component libraries, desktop wrappers, shell frameworks, package managers, or build tools.

## Existing Code
- [ ] Inspected existing files with `rg --files` or `git ls-files`.
- [ ] Reused existing project patterns where possible.

## Design
- [ ] Read `docs/design-system.md` if it exists.
- [ ] Clarified missing visual decisions with the user.
- [ ] Followed the component, command, view, artifact, or flow structure from the feature's Tech Design.

## Implementation
- [ ] All planned user-facing surface elements implemented.
- [ ] Loading, error, empty, disabled, success, and permission states handled where relevant.
- [ ] Accessibility considered for the chosen platform.
- [ ] Responsive, keyboard, terminal, viewport, artifact, or device behavior tested for the target surface in the spec.
- [ ] Local OS constraints handled where relevant: paths, permissions, config locations, quoting, process lifecycle, and offline behavior.

## Verification
- [ ] Project-native build/check/test/local-launch commands run where available.
- [ ] All surface-related acceptance criteria addressed.
- [ ] Review-loop gate completed or consciously skipped with rationale.
- [ ] Feature spec updated with implementation notes.
- [ ] `features/INDEX.md` status updated to `In Progress`.

## Completion
- [ ] User reviewed the result.
- [ ] Code committed to git when requested.
