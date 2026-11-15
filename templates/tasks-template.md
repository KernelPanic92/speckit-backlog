---

description: "Task execution index template (preset backlog)"
---

# Tasks: [FEATURE NAME]

**Spec**: [[Feature name] specification](spec.md) | **Plan**: [[Feature name] implementation plan](plan.md)

**Generation**: `specs/[###-feature]/tasks.md` is the execution index, generated deterministically by `scripts/backlog.py render-tasks <spec-dir>` from the `TASK` PBIs in the repository-root `backlog/tasks/` and the scoped stories of `spec.md`. Task details, including `BLOCKED_BY`, `## Files`, `Actions to complete`, and `Definition of Done`, live in each TASK PBI.

<!--
  The renderer groups tasks into setup, walking-skeleton/foundational, story-wave (or map Release Lane),
  and polish phases. Each story has about 2–4 cohesive tasks: acceptance tests first when enabled,
  then implementation. Do not hand-edit generated task lines or scheduling markers.
-->

**Tests**: [Acceptance tests from Gherkin: on | off] — from [the Delivery Conventions of the constitution](../../.specify/memory/constitution.md#delivery-conventions). When on, every scenario cited as `US-001/AC-1 "title"` has an automated acceptance-test task written before implementation.

## Summary

**Total tasks:** [X] | **Parallelizable:** [X] (marked [P]) | **Waves:** [X] | **Suggested MVP:** [first delivery wave or Release Lane]

## Format: `- [ ] TASK-012 [P] [US-007] Title → [../../backlog/tasks/TASK-012-slug.md](../../backlog/tasks/TASK-012-slug.md)`

- `[TASK-012]` is the project-wide unique task identifier.
- `[P]` is computed from `BLOCKED_BY` plus disjoint `## Files` declarations.
- `[US-007]` identifies the story the task serves; omit it for container tasks.
- The task checkbox becomes `[X]` automatically when all checkboxes in `Actions to complete` and `Definition of Done` in that TASK PBI are checked.
- The link is relative to this spec directory and targets the TASK PBI in the root backlog.

## Task Completion Criteria

<!-- Global Definition of Done. TASK PBIs start from these items and keep only what applies. Adjust to the constitution's Quality Standards. -->

- [ ] Unit tests for new code (coverage per constitution: [X]%)
- [ ] Integration test when touching API boundaries
- [ ] API contract in plan.md respected (update it if the contract changes)
- [ ] Migration script when the schema changes
- [ ] Feature-flag wrapped when the plan requires gradual rollout

<!-- The following phases illustrate the renderer's output structure. The execution index and all task lines are generated from the root backlog; do not hand-edit generated content. -->

## Phase 1: Setup

<!-- Container tasks with no blockers. -->

- [ ] TASK-001 [P] Set up project structure → [../../backlog/tasks/TASK-001-project-structure.md](../../backlog/tasks/TASK-001-project-structure.md)

---

## Phase 2: Walking Skeleton / Foundational

<!-- Walking Skeleton items or pre-story blocking container tasks. Complete prerequisites before story waves. -->

- [ ] TASK-002 Implement the thinnest end-to-end path → [../../backlog/tasks/TASK-002-walking-skeleton.md](../../backlog/tasks/TASK-002-walking-skeleton.md)

---

## Phase 3+: Story Wave 1

<!-- For map specs, use the applicable Release Lane instead of Story Wave. [P] stories in the same wave may run in parallel. -->

### US [US-001] [P?] [Story title]

- [ ] TASK-010 [P] [US-001] Acceptance tests for [scenario titles, e.g. "products listed" and "empty catalog"] → [../../backlog/tasks/TASK-010-acceptance-tests.md](../../backlog/tasks/TASK-010-acceptance-tests.md)
- [ ] TASK-011 [US-001] Implement the story behavior → [../../backlog/tasks/TASK-011-story-implementation.md](../../backlog/tasks/TASK-011-story-implementation.md)

---

## Phase 4+: Story Wave 2

### US [US-002] [P?] [Story title]

- [ ] TASK-012 [P] [US-002] Acceptance tests for [scenario titles, e.g. "card accepted" and "card declined"] → [../../backlog/tasks/TASK-012-acceptance-tests.md](../../backlog/tasks/TASK-012-acceptance-tests.md)
- [ ] TASK-013 [US-002] Implement the story behavior → [../../backlog/tasks/TASK-013-story-implementation.md](../../backlog/tasks/TASK-013-story-implementation.md)

---

## Phase N: Polish

<!-- Container tasks with BLOCKED_BY relations to stories or story tasks. -->

- [ ] TASK-0XX [P] Polish and cross-cutting improvements → [../../backlog/tasks/TASK-0XX-polish.md](../../backlog/tasks/TASK-0XX-polish.md)

## Wave Schedule & Dependency Graph

<!-- Render the schedule from BLOCKED_BY relations and the scoped backlog, using delivery wave and rank. -->

| Wave / Slice | PBIs | Dependencies and parallelism |
|--------------|------|-------------------------------|
| Setup | TASK [TASK-001](../../backlog/tasks/TASK-001-project-structure.md) Set up project structure | No blockers |
| Walking Skeleton / Foundational | TASK [TASK-002](../../backlog/tasks/TASK-002-walking-skeleton.md) End-to-end path | Follows setup; blocks story waves |
| Story Wave 1 / Release Lane 1 | US [US-001](../../backlog/stories/US-001-slug.md) Story title | [P] only when eligible by blockers and file overlap |
| Story Wave 2 | US [US-002](../../backlog/stories/US-002-slug.md) Story title | Follows its declared blockers |
| Polish | TASK [TASK-0XX](../../backlog/tasks/TASK-0XX-polish.md) Polish | Blocked by selected stories/story tasks |

```text
[Setup TASKs] ──▶ [Walking Skeleton / Foundational TASKs] ──▶ [Story Wave 1]
                                                           ├──▶ [parallel US tasks marked [P]]
                                                           └──▶ [Story Wave 2] ──▶ [Polish]
```

## Traceability Matrix

<!-- Every scoped story and Acceptance Criterion appears here; each row cites its scenario as US-001/AC-1 "title". When acceptance tests are on, each criterion has a test task. -->

| User Story | Acceptance Criterion | Test tasks | Implementation tasks |
|------------|----------------------|------------|----------------------|
| US [US-001](../../backlog/stories/US-001-slug.md) Story title | US-001/AC-1 "Scenario title" | TASK-010 Acceptance tests | TASK-011 Implement story behavior |

## Implementation Strategy

1. Complete Setup tasks.
2. Complete Walking Skeleton / Foundational tasks before story work.
3. Work through story waves (or Release Lanes for map specs), respecting blockers and `[P]` scheduling.
4. Validate each wave against its scenarios and outcome before moving to the next.
5. Complete Polish tasks after their declared story or task blockers.
