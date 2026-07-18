---
paths:
  - "app/**"
  - "client/**"
  - "cli/**"
  - "desktop/**"
  - "frontend/**"
  - "gui/**"
  - "interfaces/**"
  - "src/**"
  - "surfaces/**"
  - "tools/**"
  - "tui/**"
  - "ui/**"
  - "web/**"
  - "windows/**"
  - "linux/**"
---

# Surface / Interface Development Rules

## Stack Comes From Architecture
- Read `docs/architecture.md`, `docs/master-feature.md`, `docs/engineering-principles.md`, `.claude/rules/loop-policy.md`, and the feature spec before editing interface code.
- Use the target surface type, OS/platform, language/runtime, UI/shell technology, styling/presentation method, component/command conventions, and build/run commands recorded there.
- If no stack has been chosen yet, stop and run `/3-csk-architecture` for the feature.
- Do not install or introduce a UI framework, desktop wrapper, shell framework, component library, package manager, or local service wrapper just because it is familiar.

## No Web Assumption
- A user-facing surface may be a web app, local browser UI, desktop app, CLI/TUI, plugin panel, OS configuration UI, generated artifact, or another approved surface.
- Do not assume public deployment, browser hosting, JavaScript, a web server, or a frontend/backend split.
- If the surface talks to local code, such as a Python process or native service, follow the architecture-approved boundary instead of inventing one.

## Existing Project First
- Inspect existing components, routes, screens, commands, dialogs, config surfaces, styles, design tokens, launch scripts, and OS integration points before creating new files.
- Reuse established project patterns and naming conventions.
- Create custom interface code only where it represents product-specific behavior or composition.

## Local OS Awareness
- For local Windows/Linux/macOS surfaces, respect paths, permissions, install locations, config file conventions, service/process lifecycle, shell quoting, and offline behavior.
- Keep local-only behavior local; do not add a hosted deployment path unless architecture requires it.
- If a surface exposes a local/cloud/hybrid pipeline mode to the user, make the mode, boundary, failure state, and privacy implication consistent with `docs/architecture.md`.

## Design Standards
- Follow `docs/design-system.md` if it exists.
- If no design system exists, ask for the smallest necessary visual, interaction, command, keyboard, or artifact-format decision and record it in the feature spec or architecture notes.
- Implement loading, error, empty, disabled, and success states when relevant.
- Make interfaces usable across the target devices, windows, terminals, panels, or generated artifact constraints defined in the feature spec.
- Use semantic markup and accessibility primitives appropriate to the chosen stack.

## Verification
- Run the project's documented typecheck, lint, build/package, local launch, preview, smoke, UI, CLI/TUI, or artifact validation commands if they exist.
- If commands are missing, document the gap instead of inventing a toolchain.
- Run or document the review-loop gate for productive surface changes, especially local/cloud, privacy, input, file, command, external call, or accessibility-sensitive changes.
