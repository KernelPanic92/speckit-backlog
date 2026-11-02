---

description: "Task execution index template (preset backlog)"
---

# Tasks: [FEATURE NAME]

**Spec**: [link to spec.md] | **Plan**: [link to plan.md] | **Spec mode**: [map | epic | story] | **Root PBI**: [TYPE [ID] Title]

**Organization**: Every task is a TASK PBI with its own file under `backlog/tasks/`. This file is the **execution index**: one checkbox line per task, grouped in phases. The checkbox is what `__SPECKIT_COMMAND_IMPLEMENT__` marks; the details (Outcome, Files, Actions, DoD, relations) live in the TASK file.

**Tests**: [Acceptance tests from Gherkin: on | off] — from the constitution's Delivery Conventions. When on, every scenario US-xxx/AC-n has an acceptance-test task, written before the story's implementation.

## Summary

**Total tasks:** [X] | **Parallelizable:** [X] (marked [P]) | **Phases:** [X] | **Suggested MVP:** [first Release Lane | first story]

## Format: `- [ ] [ID] [P?] [Story?] Title → file`

- **[ID]**: TASK PBI id (e.g. TASK-014), project-wide unique
- **[P]**: Can run in parallel (different files, no BLOCKED_BY on incomplete tasks)
- **[Story]**: The user story the task serves (its PARENT), e.g. [US-007]. No label for Setup, Walking Skeleton without a story, Foundational and Polish tasks
- **→ file**: relative link to the TASK PBI

## Task Completion Criteria

<!-- Global Definition of Done. Every TASK file's DoD starts from this list (keeping only what applies). Adjust to the constitution's Quality Standards. -->

- [ ] Unit tests for new code (coverage per constitution: [X]%)
- [ ] Integration test when touching API boundaries
- [ ] API contract in plan.md respected (update it if the contract changes)
- [ ] Migration script when the schema changes
- [ ] Feature-flag wrapped when the plan requires gradual rollout

<!--
  ============================================================================
  IMPORTANT: The phases and tasks below are SAMPLES for illustration only.

  __SPECKIT_COMMAND_TASKS__ MUST replace them with real phases, following the spec mode:
  - map:   Setup → Walking Skeleton → one phase per Release Lane (stories in Backbone order) → Polish
  - epic:  Setup → Foundational → one phase per user story (BLOCKED_BY / release order) → Polish
  - story: Setup → Spikes (if any) → one phase per Acceptance Criterion or group → Polish

  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] TASK-001 Create project structure per implementation plan → [backlog/tasks/TASK-001-project-structure.md](backlog/tasks/TASK-001-project-structure.md)
- [ ] TASK-002 [P] Configure linting and formatting tools → [backlog/tasks/TASK-002-linting.md](backlog/tasks/TASK-002-linting.md)

---

## Phase 2: Walking Skeleton (map mode) | Foundational (epic mode)

**Purpose**: map: the thinnest end-to-end path through every Macro-Activity (the TASK/SPIKE items already listed in the MAP). epic: blocking prerequisites for all stories.

**⚠️ CRITICAL**: No story work can begin until this phase is complete

- [ ] TASK-003 Static list of 3 products from the DB → [backlog/tasks/TASK-003-static-product-list.md](backlog/tasks/TASK-003-static-product-list.md)

**Checkpoint**: Skeleton/foundation ready - story implementation can now begin

---

## Phase 3: Release 1 — [Outcome title] 🎯 MVP

**Goal**: [The lane's Goal from the MAP (map) | the story's Outcome (epic/story)]

**Independent Test**: [How to verify the lane/story works on its own: its Metrics and the Gherkin scenarios of its stories]

### US [US-001] [Story title]

#### Acceptance tests (when on) ⚠️

> **Write these tests FIRST, ensure they FAIL before implementation**

- [ ] TASK-010 [P] [US-001] Acceptance test for US-001/AC-1 and US-001/AC-2 → [backlog/tasks/TASK-010-….md](backlog/tasks/TASK-010-….md)

#### Implementation

- [ ] TASK-011 [P] [US-001] Create [Entity] model → [backlog/tasks/TASK-011-….md](backlog/tasks/TASK-011-….md)
- [ ] TASK-012 [US-001] Implement [Service] → [backlog/tasks/TASK-012-….md](backlog/tasks/TASK-012-….md)

**Checkpoint**: Release 1 is fully functional: every scenario of its stories passes

---

[Add more phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple stories

- [ ] TASK-0XX [P] Documentation updates → [backlog/tasks/….md](backlog/tasks/….md)
- [ ] TASK-0XX Security hardening → [backlog/tasks/….md](backlog/tasks/….md)

---

## Dependency Graph

<!-- From the BLOCKED_BY relations of the TASK files. -->

```text
TASK-001 ──┬──▶ TASK-003 ──┬──▶ TASK-011
           │               │
TASK-002 ──┘               └──▶ TASK-012
```

### Phase Dependencies

- **Setup**: no dependencies - can start immediately
- **Walking Skeleton / Foundational**: depends on Setup - BLOCKS all story phases
- **Story / lane phases**: depend on the previous phase; inside a lane, stories follow the Backbone order and their BLOCKED_BY relations
- **Polish**: depends on all desired phases being complete

### Within Each Story

- Acceptance tests (when on) MUST be written and FAIL before implementation
- Models before services, services before endpoints, core before integration
- Story complete before moving to the next one

## Parallel Example: US [US-001]

```bash
# Launch the acceptance tests of US-001 together (when on):
Task: "TASK-010 Acceptance test for US-001/AC-1 and US-001/AC-2"

# Launch the models of US-001 together:
Task: "TASK-011 Create [Entity] model"
```

## Implementation Strategy

### MVP First

1. Complete Setup
2. Complete Walking Skeleton / Foundational (CRITICAL - blocks all stories)
3. Complete the first Release Lane (map) or the first story (epic/story)
4. **STOP and VALIDATE**: all Gherkin scenarios of the phase pass, the lane's Metrics can be measured
5. Deploy/demo if ready

### Incremental Delivery

1. Each following lane/story is added, tested on its own scenarios and deployed
2. Each increment adds value without breaking the previous ones

## Risk Assessment

| Task | Risk | Mitigation |
|------|------|------------|
| [TASK-012] | [Risk description] | [Mitigation strategy] |

## Traceability Matrix

<!-- Every story and every Acceptance Criterion must appear here. An AC without a test task (when acceptance tests are on) is a gap. -->

| User Story | Acceptance Criteria | Test tasks | Implementation tasks |
|------------|---------------------|------------|----------------------|
| [US-001] | AC-1, AC-2 | TASK-010 | TASK-011, TASK-012 |

## Notes

- [P] tasks = different files, no BLOCKED_BY on incomplete tasks
- The [Story] label maps the task to its PARENT story for traceability
- Commit after each task or logical group; stop at any checkpoint to validate independently
- Avoid: vague tasks, same-file conflicts, cross-story dependencies that break independence
