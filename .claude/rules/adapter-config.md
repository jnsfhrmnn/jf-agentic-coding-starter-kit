# Adapter Config

## Purpose

The kit works standalone with its default layout. An existing repository may
adapt source-of-truth paths and workflow handoffs through one optional local
`csk.config.json` file at the repository root.

Before a skill reads or writes project source-of-truth files:

1. Read `csk.config.json` when it exists.
2. Fall back field by field to the kit defaults.
3. Ignore unknown fields and report invalid values before writing through them.

No second config location, external context transport, or cross-repository state
is part of the kit.

## Supported fields

```json
{
  "profile": "default",
  "paths": {
    "architecture": "docs/architecture.md",
    "prd": "docs/PRD.md",
    "master_feature": "docs/master-feature.md",
    "features_dir": "features/"
  },
  "orchestrator": null,
  "deploySkill": null,
  "adrRequired": false,
  "architectureAuthority": null
}
```

Derived paths:

- Feature index: `<paths.features_dir>/INDEX.md`
- Feature specs: `<paths.features_dir>/PROJ-X-feature-name.md`

## Required behavior

- Treat every default path in kit instructions as a fallback only.
- Resolve configured paths inside the repository; reject absolute paths or paths
  that escape the repository.
- Use configured paths exactly; do not also create their defaults.
- Substitute adapter-resolved paths in recommended commands.
- If `orchestrator` is set, architecture and surface work follow that named local
  workflow instead of making independent workflow decisions.
- If `deploySkill` is set, `/7-csk-deploy` delegates release execution to that
  named local skill after its readiness gates pass.
- If `adrRequired` is true, follow the repository ADR process before changing
  architecture, config, deployment, or source-of-truth documentation.
- If `architectureAuthority` is set, `/3-csk-architecture` documents and verifies
  the prescribed architecture; change requests route to the named authority.
- Preserve greenfield behavior when `csk.config.json` does not exist.
