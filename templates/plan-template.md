# Implementation Plan: [FEATURE]

**Spec**: [link to spec.md] | **Spec mode**: [map | epic | story] | **Root PBI**: [TYPE [ID] Title]

**Research**: [link to research.md] | **Product**: `.specify/memory/product.md` | **Status**: [Draft | Review | Approved]

**Note**: This template is filled in by the `__SPECKIT_COMMAND_PLAN__` command; its definition describes the execution workflow. It is a single document: data model, API contracts and validation scenarios live here (no separate data-model.md, contracts/ or quickstart.md). Research lives in research.md.

## Summary

[2-3 sentences: the primary requirement (from the root PBI's Connextra and Outcome) and the technical approach (from research)]

**Key technical decisions:**
- [Decision 1]
- [Decision 2]
- [Decision 3]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. Start from the constitution's Technology Stack; mark every unknown
  as NEEDS CLARIFICATION — Phase 0 turns each one into a research question.
-->

**Language/Version**: [e.g., TypeScript 5.x, Python 3.12 or NEEDS CLARIFICATION]

**Primary Dependencies**: [e.g., React 18, FastAPI or NEEDS CLARIFICATION]

**Storage**: [if applicable, e.g., PostgreSQL 16, files or N/A]

**Cache / Messaging**: [if applicable, e.g., Redis 7, Kafka or N/A]

**Design System**: [`.specify/memory/design.md` (tokens and components) and where its tokens live in code, or N/A for products without UI]

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

[Gates determined from the constitution: Core Principles, Three-Tier Rules (MUST items are blocking), Agent Boundaries, Quality Standards, Security Posture, Delivery Conventions. One line per gate: PASS / VIOLATION (→ Complexity Tracking).]

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
├── spec.md              # Root PBI + spec envelope (__SPECKIT_COMMAND_SPECIFY__)
├── backlog/             # Child PBIs: epics/, stories/, spikes/, tasks/
├── checklists/          # requirements.md (__SPECKIT_COMMAND_SPECIFY__) and others
├── research.md          # Phase 0 output (__SPECKIT_COMMAND_PLAN__)
├── plan.md              # This file (__SPECKIT_COMMAND_PLAN__)
└── tasks.md             # Execution index (__SPECKIT_COMMAND_TASKS__ - NOT created by __SPECKIT_COMMAND_PLAN__)
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
├── acceptance/      # Gherkin scenarios (US-xxx/AC-n), when acceptance tests are on
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
| GET | `/api/v1/[resource]` | List [resources] | [US-001] |
| POST | `/api/v1/[resource]` | Create [resource] | [US-002] |

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

- **Acceptance tests**: [on | off, from the constitution's Delivery Conventions]. When on, every Gherkin scenario (US-xxx/AC-n) becomes an automated acceptance test, written before the story's implementation. The Gherkin scenarios are the feature's validation scenarios (they replace upstream's quickstart.md).
- **Unit tests**: [coverage target, framework, mocking approach]
- **Integration / contract tests**: [scope, tools]
- **E2E tests**: [framework, critical paths]

## Delivery Slices

<!--
  How the backlog maps onto the architecture, in delivery order. /speckit.tasks uses this table to build its phases.
  map mode: Walking Skeleton first, then one block per Release Lane (stories in Backbone order).
  epic mode: one row per story in BLOCKED_BY / release order.
  story mode: one row per Acceptance Criterion.
-->

| Slice | PBIs | Components touched | Notes |
|-------|------|--------------------|-------|
| Walking Skeleton | [TASK [TASK-001] …, SPIKE [SPIKE-001] …] | [components] | [end-to-end path] |
| [Release 1: Outcome title] | [US [US-001] …, US [US-002] …] | [components] | [MVP] |

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

## Open Technical Questions

- [ ] TQ-1: [Question]

## References

- [Link to architecture diagram, API docs, related research]
