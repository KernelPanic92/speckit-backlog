# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Spec**: [[Feature name] specification](spec.md) | **Scope**: [scoped PBIs as type [id](../../backlog/...) title]\
**Research**: [[Feature name] research](research.md) | **ADRs**: [governing ADRs as [ADR-NNNN: title](../../docs/architecture/adr/...) or none] | **Product**: [personas and Ubiquitous Language](../../.specify/memory/product.md)

## Summary

[2–3 sentences: primary outcomes and technical approach. Link to feature research and governing ADRs rather than repeating their rationale.]

## Technical Context

| Field | Value |
|-------|-------|
| Language/Version | [language and version] |
| Primary Dependencies | [existing dependencies] |
| Storage | [technology or N/A] |
| Design System | [the design system](../../.specify/memory/design.md) or N/A |
| Testing | [frameworks and relevant acceptance-test command] |
| Target Platform | [platform] |
| Project Type | [library, CLI, service, web, mobile, etc.] |
| Performance Goals | [measurable goal or N/A] |
| Constraints | [feature-specific constraints] |
| Scale/Scope | [expected load, volume, and bounded scope] |

### New Dependencies *(only when introducing packages)*

| Dependency | Version | Purpose |
|------------|---------|---------|
| [package] | [version] | [need] |

## Constitution Check

| Gate | Check |
|------|-------|
| [Named constitution principle](../../.specify/memory/constitution.md#principle-heading) | PASS / VIOLATION |
| [Accepted governing ADR](../../docs/architecture/adr/NNNN-slug.md) | PASS / VIOLATION |

## Architecture & Project Structure

### Documentation (this feature)

```text
specs/[###-feature-name]/
├── spec.md
├── research.md
├── plan.md
├── data-model.md       # only when entities or state change
├── contracts/          # only when external interfaces change
├── quickstart.md
└── tasks.md
docs/architecture/adr/   # durable project-wide decisions, when needed
backlog/                 # central PBIs
```

### Source Code & Component Boundaries

```text
[concrete repository paths for this feature; remove unused paths]
```

| Component | Responsibility | Key Artifacts |
|-----------|----------------|---------------|
| [component] | [feature-specific responsibility] | [data model](data-model.md#entity) · [contract slice](contracts/slice.yaml) |

### Resilience, Migration & Rollout Deltas *(omit if none)*

| Boundary / Change | Required behavior | Rollback gate / Point of no return |
|-------------------|-------------------|-----------------------------------|
| [network boundary or stateful migration] | [specific idempotency, timeout, retry, backpressure, fallback, or migration behavior] | [condition and explicit point of no return, if applicable] |

## Delivery Slices

<!-- Reflect `scripts/backlog.py schedule --spec <spec-dir>`; keep PBIs linked by type, ID, and title. -->

| Wave / Slice | PBIs | Artifacts & Components | Parallelism & Gate |
|--------------|------|------------------------|--------------------|
| [wave / slice] | [type [id](../../backlog/...) title] | [artifacts and components] | [parallel work and completion gate] |

## Complexity Tracking *(only if Constitution Check has violations)*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|--------------------------------------|
| [constitution gate] | [feature-specific reason] | [specific limitation] |
