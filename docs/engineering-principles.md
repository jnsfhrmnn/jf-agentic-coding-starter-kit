# Engineering Principles

## Purpose

This file is the source of truth for engineering quality across projects created with this starter kit. It complements:

- `docs/master-feature.md` for product goal and USP.
- `docs/architecture.md` for technology decisions.
- `.claude/rules/loop-policy.md` for planning and review hardening.

## Quality First

Prefer correctness, robustness, security, privacy, maintainability, observability, and measurable performance over speed of implementation.

Do not treat "works once" as done. A result is ready only when the relevant evidence exists: tests, checks, benchmarks, manual verification, artifact validation, security review, or a documented reason why a check is not available yet.

## Frontier AI Pipeline Principle

For AI, RAG, ML, media, GPU, evaluation, agentic, or automation pipelines:

- Use current, capable technology when the architecture is still open.
- Verify current options at decision time instead of relying on stale memory.
- Prefer official docs, primary model/provider docs, benchmark reports, release notes, and project-native evidence.
- Record the decision date, evaluated options, rejected options, and rationale in `docs/architecture.md`.
- Avoid hardcoding a provider, model, runtime, orchestration framework, vector store, inference backend, or cloud target before `/3-csk-architecture` approves it.

State-of-the-art does not mean hype-first. It means the chosen option is current, fit for the product goal, measurable, maintainable, secure, and compatible with the data locality decision.

## Local / Cloud / Hybrid Decision Gate

Every architecture touching data, inference, processing, storage, search, evaluation, file handling, or external services must classify the pipeline mode:

| Mode | Meaning |
|------|---------|
| Offline / local | Processing stays on the user's machine or approved local infrastructure. |
| Online / cloud | Data or computation leaves the local trust boundary for a hosted service, API, GPU, storage, queue, or remote runtime. |
| Hybrid | Some steps are local and some steps are remote, with explicit boundaries. |

The decision must document:

- What data enters the pipeline.
- Which data is sensitive, confidential, regulated, user-provided, customer-provided, or secret-bearing.
- Which steps run locally, which run remotely, and why.
- What crosses the boundary: prompts, files, embeddings, metadata, logs, telemetry, model outputs, intermediate artifacts, caches, or identifiers.
- Privacy and security controls: minimization, redaction, encryption, access control, retention, deletion, logging, and auditability.
- Operational tradeoffs: latency, throughput, cost, GPU/CPU needs, memory, disk, availability, offline behavior, reproducibility, and failure recovery.
- User-visible implications: consent, disclosure, configuration, mode switch, fallback, or "offline only" guarantee.

If the mode is unclear, architecture is not complete.

## Performance Engineering

Performance work must be measurable.

For performance-sensitive code or pipelines:

- Identify hot paths, expected data sizes, concurrency, and target platforms.
- Define workload fixtures or benchmark scenarios.
- Measure before claiming improvement.
- Consider algorithmic complexity, batching, caching, streaming, parallelism, memory use, I/O, GPU/CPU placement, startup time, and cleanup.
- Record performance assumptions and verification commands in `docs/architecture.md` or the feature spec.

## Security And Review

Security is not a final polish step.

Apply security thinking during:

- Product goal definition: what data and trust boundaries exist?
- Feature spec: what misuse, privacy, and abuse cases matter?
- Architecture: what runs local, cloud, or hybrid?
- Implementation: what inputs, outputs, secrets, files, subprocesses, dependencies, and permissions are touched?
- QA/release: what evidence proves the risks are controlled?

Any productive code, architecture, rules, config, or release artifact that affects security, privacy, local/cloud boundaries, dependencies, execution, or data movement must pass the review-loop gate described in `.claude/rules/loop-policy.md`.

## Evidence Standards

Use the project-approved tools from `docs/architecture.md`. If none exist yet, document the gap instead of inventing a default toolchain.

Evidence can include:

- Test, build, package, lint, typecheck, static analysis, benchmark, smoke, dry-run, fixture comparison, artifact validation, or manual verification output.
- Exact file paths and sections that were inspected.
- Current official docs or release notes when choosing fast-moving AI technology.
- A clear "not verified" note when evidence is not available.

Never mark a feature, system, or release as ready when a critical local/cloud/privacy/security/performance assumption is unverified.
