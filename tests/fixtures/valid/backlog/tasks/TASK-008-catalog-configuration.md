---
id: TASK-008
title: Catalog configuration
type: TASK
rank: 10
relations:
  FEATURE-001:
    title: Catalog browsing
    type: FEATURE
    relationType: PARENT
    reason: Share catalog configuration across its implementation tasks.
---

## Outcome

Provide validated store currency and catalog storage settings.

## Files

- `config/settings.py`

## Actions to complete

- [ ] Validate required settings at startup.

## Out of Scope

- Storage adapter: TASK [TASK-009] Catalog storage.

## Definition of Done

- [ ] Invalid currency settings fail with a diagnostic.
