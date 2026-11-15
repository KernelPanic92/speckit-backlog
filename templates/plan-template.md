# Implementation Plan: [FEATURE]

**Spec**: [[Feature name] specification](spec.md) | **Scope**: [scoped PBIs as type [id](../../backlog/...) title]

**Research**: [[Feature] research decisions](research.md) | **Product**: [personas and Ubiquitous Language](../../.specify/memory/product.md) | **Status**: [Draft | Review | Approved]

**Note**: This template is filled in by the `__SPECKIT_COMMAND_PLAN__` command; its definition describes the execution workflow. It is a single document: data model, API contracts and validation scenarios live here (no separate data-model.md, contracts/ or quickstart.md). Research lives in research.md.

<!-- References follow the "Readable references" rules of the backlog preset: a PBI as `type [id](relative/path.md) title`, a scenario as `US-001/AC-1 "title"`, a research decision, a constitution rule or a section of product.md as a relative link whose text names it, e.g. [the payment provider decision](research.md#payment-provider), [the "Test-First" principle](../../.specify/memory/constitution.md#test-first). Never a bare id, a bare path or a section number. -->

## Summary

[2-3 sentences: the primary requirements from the scoped PBIs and the technical approach from research]

**Key technical decisions:**
- [Decision 1, linked to its research block: [the payment provider decision](research.md#payment-provider)]
- [Decision 2]
- [Decision 3]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. Start from the constitution's Technology Stack and resolve unknowns
  in Phase 0 research.
-->

**Language/Version**: [e.g., TypeScript 5.x, Python 3.12 or NEEDS CLARIFICATION]

**Primary Dependencies**: [e.g., React 18, FastAPI or NEEDS CLARIFICATION]

**Storage**: [if applicable, e.g., PostgreSQL 16, files or N/A]

**Cache / Messaging**: [if applicable, e.g., Redis 7, Kafka or N/A]

**Design System**: [[the design system](../../.specify/memory/design.md) (tokens and components) and where its tokens live in code, or N/A for products without UI]

**Testing**: [e.g., Vitest + Playwright, pytest or NEEDS CLARIFICATION]

**Target Platform**: [e.g., Linux server, iOS 17+, browser or NEEDS CLARIFICATION]

**Project Type**: [e.g., library/cli/web-service/mobile-app/desktop-app or NEEDS CLARIFICATION]

**Performance Goals**: [domain-specific, from the spec's Non-Functional Requirements, e.g., 1000 req/s or NEEDS CLARIFICATION]

**Constraints**: [domain-specific, e.g., <200ms p95, offline-capable or NEEDS CLARIFICATION]

**Scale/Scope**: [domain-specific, e.g., 10k users, 50 screens or NEEDS CLARIFICATION]

### New Dependencies

| Dependency | Version | Purpose | License |
|------------|---------|---------|---------|
| [package] | [X.Y.Z] | [Why needed] | [MIT/Apache-2.0/etc] |

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

[Gates determined from the constitution: Core Principles, Three-Tier Rules (MUST items are blocking), Agent Boundaries, Quality Standards, Security Posture, Delivery Conventions. One line per gate, naming the principle or rule (never its number), as a link to its heading in the constitution: PASS / VIOLATION (→ Complexity Tracking).]

## Architecture Overview

### High-Level Design

```text
[ASCII diagram of component relationships]

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│     API     │────▶│  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Component Breakdown

| Component | Responsibility | Technology |
|-----------|----------------|------------|
| [Component 1] | [What it does] | [Tech] |

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── spec.md              # Feature specification and rendered backlog index
├── research.md          # Phase 0 research decisions
├── plan.md              # This implementation plan
├── tasks.md             # Generated execution index
└── checklists/
    └── [requirements and other checklists]
```

Repository-root backlog:

```text
backlog/
├── index.md
├── maps/
├── epics/
├── features/
├── stories/
├── spikes/
└── tasks/
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── acceptance/      # Gherkin scenarios (US-001/AC-1 "title"), when acceptance tests are on
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real directories captured above]

## Data Model

<!-- From the spec's Key Entities, named with the Ubiquitous Language terms of product.md. Quote field constraints (length, nullability, enums, validation rules) exactly: /speckit.tasks copies them verbatim into the tasks. -->

### Entities

#### [Entity Name]
```text
[Entity Name]
├── id: UUID (PK)
├── [field]: [type] [constraints]
├── createdAt: Timestamp
└── updatedAt: Timestamp
```

### Relationships
- [Entity A] → [Entity B]: [One-to-Many / Many-to-Many / One-to-One]

### State Transitions *(if any)*
- [Entity]: [state A] → [state B] when [event]

### Indexes
- `idx_[table]_[field]`: [Purpose]

## API Design / Contracts

<!-- The interface contracts this feature exposes or consumes (REST, GraphQL, events, CLI, library API). Each contract names the stories it serves. -->

### Endpoints

| Method | Path | Description | Serves |
|--------|------|-------------|--------|
| GET | `/api/v1/[resource]` | List [resources] | US [US-001](../../backlog/stories/US-001-[slug].md) Story title |
| POST | `/api/v1/[resource]` | Create [resource] | US [US-002](../../backlog/stories/US-002-[slug].md) Story title |

### Request/Response Examples

**POST /api/v1/[resource]**

Request:
```json
{ "field1": "value" }
```

Response (201):
```json
{ "id": "uuid", "field1": "value" }
```

Error response (400):
```json
{ "error": "VALIDATION_ERROR", "message": "field1 is required" }
```

## Integration Points

### External Services
| Service | Purpose | Auth Method | Fallback |
|---------|---------|-------------|----------|
| [Service] | [Purpose] | [API key / OAuth] | [Fallback behaviour] |

### Internal Services
| Service | Purpose | Protocol |
|---------|---------|----------|
| [Service] | [Purpose] | [REST / gRPC / events] |

## Security Design

- **Authentication**: [auth flow]
- **Authorization**: [permission model]
- **Data protection**: [encryption at rest / in transit, PII handling]
- **Compliance**: [how the spec's Security & Compliance Checklist is satisfied]

## Performance Design

- **Caching strategy**: [location, TTL, invalidation]
- **Database optimization**: [query patterns, pooling, replicas]
- **Scaling approach**: [horizontal scaling, rate limiting]

## Error Handling

| Category | Example | Handling | User-facing behaviour |
|----------|---------|----------|-----------------------|
| Validation | Invalid input | Return details | [as described by the AC] |
| Unavailable dependency | Timeout | Retry with backoff | [as described by the AC: error + retry action] |

- **Retryable errors**: [list]
- **Backoff / max attempts**: [strategy]

## Observability

- **Logging**: [format, levels, correlation id]
- **Metrics**: [name, type, purpose — include the spec's Success Criteria that can be measured in production]
- **Alerts**: [condition, severity]

## Testing Strategy

- **Acceptance tests**: [on | off, from the constitution's Delivery Conventions]. When on, every Gherkin scenario cited as US-001/AC-1 "title" becomes an automated acceptance test, written before the story's implementation. The Gherkin scenarios are the feature's validation scenarios (they replace upstream's quickstart.md).
- **Unit tests**: [coverage target, framework, mocking approach]
- **Integration / contract tests**: [scope, tools]
- **E2E tests**: [framework, critical paths]

## Delivery Slices

<!--
  Describe the wave-based schedule produced by `scripts/backlog.py schedule --spec <spec-dir>`.
  Schedule the Walking Skeleton first, then delivery waves and, for map specs, Release Lanes.
  Stories marked [P] in the same wave can run in parallel when their dependencies and files allow it.
-->

| Wave / Slice | PBIs | Components touched | Parallelism & Notes |
|--------------|------|--------------------|---------------------|
| Walking Skeleton | TASK [TASK-001](../../backlog/tasks/TASK-001-slug.md) Title; SPIKE [SPIKE-001](../../backlog/spikes/SPIKE-001-slug.md) Title | [components] | [End-to-end path; prerequisites before story waves] |
| Wave 1 — Release Lane 1 MVP | US [US-001](../../backlog/stories/US-001-slug.md) Title; US [US-002](../../backlog/stories/US-002-slug.md) Title | [components] | [P] stories with no dependency or file conflicts |
| Wave 2 | US [US-003](../../backlog/stories/US-003-slug.md) Title | [components] | [Blocked by Wave 1; release outcome] |

## Migration Plan *(if applicable)*

- **Database migrations**: [steps]
- **Data migration / backfill**: [yes/no, duration, rollback plan]

### Feature Flags
| Flag | Purpose | Default |
|------|---------|---------|
| [flag_name] | [Purpose] | [on/off] |

## Patterns Established

<!-- For early features: patterns later features must follow (API, error handling, test organization). Remove if nothing new is established. -->

- **API pattern**: [describe]
- **Error handling pattern**: [describe]
- **Test organization pattern**: [describe]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified.** Each row follows the constitution's Exceptions Process.

| Violation | Why Needed | Simpler Alternative Rejected Because | Mitigation | Approved by |
|-----------|------------|--------------------------------------|------------|-------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] | [mitigation] | [role] |

## References

<!-- One bullet per source, as a link whose text says what it is. Never a bare URL or path. -->

- [[What the source is, in words]](address that reaches the spot)
