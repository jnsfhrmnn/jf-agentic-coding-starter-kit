# Performance Readiness

Use this guide after `/3-csk-architecture` defines the target platform and user experience expectations.

## Define Budgets

Record budgets in the feature spec or `docs/architecture.md`:

- Startup/load time.
- Interaction latency.
- Job or request duration.
- Memory or CPU limits.
- GPU/accelerator use where relevant.
- I/O, disk, network, and file size limits.
- Bundle/artifact size where relevant.
- Data volume limits.
- Cost/resource budget for cloud or external services.

## Common Checks

- Avoid loading work the user does not need yet.
- Keep large assets optimized for the target platform.
- Cache stable data when it is safe.
- Bound expensive queries, loops, or background work.
- Use batching, streaming, caching, indexing, parallelism, or incremental processing only when they fit the approved architecture.
- Keep offline/local, online/cloud, and hybrid pipeline steps measurable separately.
- Add progress or loading feedback for slow operations.
- Measure before optimizing.

## Verification

Use the tools approved in `docs/architecture.md`:

- Browser/runtime profiling.
- Load or smoke tests.
- Query plans or datastore metrics.
- AI/RAG/ML/media/GPU pipeline fixtures, quality checks, and benchmark scenarios.
- Local vs cloud timing, cost, and resource measurements.
- Production logs and timings.
- Real-user or synthetic monitoring.

## Checklist

- [ ] Performance budgets documented.
- [ ] Relevant measurements collected.
- [ ] Local/cloud/hybrid pipeline measurements separated where relevant.
- [ ] AI/pipeline quality and performance evidence collected where relevant.
- [ ] Slow paths identified.
- [ ] Obvious waste removed.
- [ ] Monitoring or manual verification path documented.
