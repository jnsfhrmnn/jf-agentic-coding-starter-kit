# Data And Persistence Optimization

Use this guide only when the approved architecture includes persistent data.

## Goals

- Keep reads and writes predictable.
- Preserve data integrity.
- Avoid expensive repeated work.
- Make backup, restore, and migration paths clear.

## Design Checks

- Define ownership and access rules for each data type.
- Add constraints where the chosen store supports them.
- Index or partition data based on real query patterns.
- Bound list/read operations.
- Avoid repeated per-record lookups when batching, joins, preloading, or aggregation are available.
- Plan retention and deletion behavior.
- Document backup and restore expectations.

## Migration Checks

- Migrations are reversible or have a rollback plan.
- Production data changes are tested on representative data.
- Long-running migrations have a safety plan.
- Schema and code rollout order is documented.

## Verification

- Run datastore-native checks or query analysis where available.
- Test representative data volume.
- Verify permissions and isolation.
- Verify backup/restore or export path if required.

## Checklist

- [ ] Data ownership documented.
- [ ] Access rules documented and enforced.
- [ ] Query patterns reviewed.
- [ ] Migrations tested.
- [ ] Backup/restore expectations recorded.
