# [PROJECT_NAME] Constitution
<!-- Example: TaskFlow Constitution. This file answers HOW we build; WHAT we build and for WHOM lives in .specify/memory/product.md -->

## Project Identity

**Name**: [PROJECT_NAME]

**Purpose**: [PROJECT_PURPOSE]
<!-- One-sentence mission statement -->

**Primary Users**: [PRIMARY_USERS]
<!-- Short reference only: the full Personas live in [the product's Personas](product.md#personas) -->

**Domain**: [BUSINESS_DOMAIN]

## Core Principles

### [PRINCIPLE_1_NAME]
<!-- Example: Library-First. Principles are named, not numbered: plans and analyses cite them by name -->
[PRINCIPLE_1_DESCRIPTION]
<!-- Example: Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented; Clear purpose required - no organizational-only libraries -->

### [PRINCIPLE_2_NAME]
<!-- Example: Test-First (NON-NEGOTIABLE) -->
[PRINCIPLE_2_DESCRIPTION]
<!-- Example: TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced -->

### [PRINCIPLE_3_NAME]
<!-- Example: Simplicity -->
[PRINCIPLE_3_DESCRIPTION]
<!-- Example: Start simple, YAGNI; every added abstraction must be justified in the plan's Complexity Tracking -->

## Technology Stack

<!-- Confirmed choices that every plan must respect. Mark unknowns as NEEDS CLARIFICATION. Remove the groups that do not apply. -->

### Frontend
- Framework: [FRONTEND_FRAMEWORK]
- Language: [FRONTEND_LANGUAGE]
- Styling: [FRONTEND_STYLING]
- Design system: [the design system](design.md) (DESIGN.md format) — remove this line for products without UI
- State: [FRONTEND_STATE]

### Backend
- Runtime: [BACKEND_RUNTIME]
- Framework: [BACKEND_FRAMEWORK]
- Database: [DATABASE]
- ORM / data access: [DATA_ACCESS]

### Infrastructure
- Hosting: [HOSTING]
- CI/CD: [CI_CD]
- Containers / orchestration: [CONTAINERS]

## Three-Tier Rules

### Tier 1: MUST (non-negotiable)
These constraints are absolute and must never be violated.
<!-- Example:
**Security:** MUST validate all user input; MUST use parameterized queries; MUST NOT log sensitive data (passwords, tokens, PII); MUST NOT commit secrets.
**Quality:** MUST write tests for all business logic; MUST pass CI before merge.
**Architecture:** MUST [project-specific constraint]. -->
[TIER_1_RULES]

### Tier 2: SHOULD (strong recommendations)
Established patterns to follow unless a documented reason to deviate exists.
<!-- Example: SHOULD follow [pattern] for file structure; SHOULD keep functions under [X] lines; SHOULD mock external dependencies; SHOULD document public APIs. -->
[TIER_2_RULES]

### Tier 3: MAY (preferences)
Style guidelines that can be adapted to the context.
<!-- Example: MAY prefer [approach] over [alternative] for [situation]. -->
[TIER_3_RULES]

## Agent Boundaries

<!-- What an AI agent working on this repository does on its own, asks first, or never does. -->

### ✅ Always Do
[AGENT_ALWAYS]
<!-- Example: Run tests before commits; Follow the naming conventions; Use parameterized queries; Add type annotations on public functions -->

### ⚠️ Ask First
[AGENT_ASK_FIRST]
<!-- Example: Modifying database schemas; Adding new dependencies; Changing CI/CD configuration; Refactoring shared utilities; Modifying authentication logic -->

### ❌ Never Do
[AGENT_NEVER]
<!-- Example: Commit secrets or API keys; Edit vendor directories; Remove failing tests without explicit approval; Modify production configuration; Delete data without backup confirmation -->

## Quality Standards

### Testing Requirements
- Unit test coverage: [UNIT_COVERAGE]
- Integration tests: [INTEGRATION_TESTS_POLICY]
- E2E tests: [E2E_POLICY]
- Performance tests: [PERFORMANCE_TESTS_POLICY]

### Code Quality
- Linting: [LINT_TOOL]
- Formatting: [FORMAT_TOOL]
- Type checking: [TYPE_CHECKING]
- Complexity limits: [COMPLEXITY_LIMITS]

### Performance Baselines
- API p95: [API_P95]
- Page load: [PAGE_LOAD]
- Bundle size: [BUNDLE_SIZE]

## Security Posture

### Authentication & Authorization
- Auth pattern: [AUTH_PATTERN]
- Token expiry: [TOKEN_EXPIRY]
- Required for: [AUTH_REQUIRED_FOR]

### Data Protection
- Encryption at rest: [ENCRYPTION_AT_REST]
- Encryption in transit: [ENCRYPTION_IN_TRANSIT]
- PII handling: [PII_HANDLING]

### Compliance
- GDPR: [GDPR]
- [OTHER_REGULATION]: [OTHER_REGULATION_STATUS]
<!-- Example: HIPAA, SOC2, PCI-DSS - Yes / No / N/A -->

## Delivery Conventions

<!-- Read by the commands of the "backlog" preset. -->

- **Acceptance tests from Gherkin**: [ACCEPTANCE_TESTS]
  <!-- "on" (default): /speckit.tasks turns every Gherkin scenario (US-xxx/AC-n) into an acceptance-test task written before the story's implementation. "off": tests only when explicitly requested. -->
- **Default specify mode**: [DEFAULT_SPEC_MODE]
  <!-- "ask" (default) | "map" | "epic" | "story". With "ask", /speckit.specify always asks and recommends a mode. -->
- **Task manager**: [TASK_MANAGER]
  <!-- "none" (default) | "clickup" | "multica": the tool /speckit.sync publishes the backlog to (its mapping lives in .specify/sync/<tool>.md). PBI ids stay local (US-001…); the tool's ids are stored in each PBI's `external` block. -->
- **Readable references**: specs and documents are written for the people who steer the work. Every reference a person reads says what it is about before it is opened and leads to the right spot: a PBI as `type [id] title`, a scenario as `US-001/AC-1 "title"`, a section of another document as a relative link whose text names the topic and whose address ends with the heading anchor, a principle or rule of this constitution by its name. Never the `§` notation, section numbers, coined abbreviations, bare ids, bare URLs or bare paths. The commands of the "backlog" preset apply the full rule (its "Readable references" section).

## Exceptions Process

When a constitutional principle cannot be followed:

1. **Document** the specific principle being violated (in the plan's Complexity Tracking)
2. **Explain** why the violation is necessary
3. **Describe** mitigation measures
4. **Get approval** from: [EXCEPTION_APPROVER]
5. **Set a review trigger** (e.g., "before the next release", "when X is upgraded")

Exceptions are tracked in: `.specify/memory/exceptions.md`

## Governance
<!-- Example: The constitution supersedes all other practices; amendments go through a pull request reviewed by [ROLE], with a migration plan when existing specs or code are affected -->

[GOVERNANCE_RULES]
<!-- Example: All PRs/reviews must verify compliance; complexity must be justified; use [GUIDANCE_FILE] for runtime development guidance. History of amendments is git history: no version numbers or amendment tables in this file. -->

### Review Schedule *(optional)*
- **Quarterly**: review principles for relevance
- **On major release**: review technology choices
- **On incident**: review security posture
