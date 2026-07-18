---
paths:
  - "api/**"
  - "automation/**"
  - "backend/**"
  - "core/**"
  - "db/**"
  - "engine/**"
  - "jobs/**"
  - "scripts/**"
  - "server/**"
  - "services/**"
  - "src/**"
  - "workers/**"
---

# Core / Data / Service Rules

## Stack Comes From Architecture
- Read `docs/architecture.md`, `docs/master-feature.md`, `docs/engineering-principles.md`, `.claude/rules/loop-policy.md`, and the feature spec before editing core, backend, API, data, automation, or integration code.
- Use the runtime, framework or scripting environment, storage/file format, auth/permission approach, validation strategy, process boundary, and test tools recorded there.
- If no core implementation, data, service, or integration layer is part of the approved architecture, do not create one.
- If the feature appears to need persistence, sync, auth, jobs, local process orchestration, IPC, file exchange, or third-party integrations not covered by the architecture, pause and return to `/3-csk-architecture`.
- If AI, RAG, ML, media, GPU, evaluation, agentic, automation, or data-pipeline technology is involved, use the current technology decision recorded in architecture; do not pick a provider/model/runtime from memory.
- If data crosses a local/cloud boundary, verify the pipeline contract in `docs/architecture.md` before coding.

## No Server Assumption
- Backend/core work may be a local Python module, script, native helper, embedded library, worker, file transformer, command-line tool, desktop-app service layer, hosted API, database layer, or external integration.
- Do not assume an HTTP server, cloud deployment, database, API route, or client/server split.
- For local software, respect OS differences, paths, permissions, install locations, shell quoting, process lifecycle, file locking, and offline/recovery behavior.

## Data Safety
- Validate all untrusted input at the trusted execution boundary.
- Enforce authorization or ownership close to the data/core/service boundary.
- Use safe APIs for the chosen storage engine, file format, command invocation, or external integration.
- Add indexes, constraints, migrations, file locks, schema validation, or recovery mechanisms where the chosen persistence layer supports them.
- Handle retries, idempotency, and partial failure for side effects and integrations.
- Minimize data movement across trust boundaries; redact, encrypt, retain, delete, and log according to the approved local/cloud/hybrid mode.

## Core, API, And Service Design
- Keep route, command, module, process, file, or service boundaries aligned with the feature spec.
- Return or surface meaningful errors without leaking secrets or internal implementation details.
- Limit list/read operations where large result sets are possible.
- Avoid repeated per-record lookups when the chosen data layer supports joins, batching, preloading, or aggregation.
- Keep integration contracts explicit: inputs, outputs, encoding, working directory, timeout, retries, and ownership of temporary files.

## Verification
- Run the project's documented core tests, implementation tests, integration tests, migration checks, local process smoke tests, or build/package commands if they exist.
- If commands are missing, document the gap and add only the minimum test tooling approved by architecture.
- Run or document the review-loop gate for productive core changes, especially security/privacy, AI/pipeline, local/cloud, performance, or interface changes.
