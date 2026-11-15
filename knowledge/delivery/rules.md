# Delivery and Scheduling Rules

These rules define repository placement, computed execution order, parallel work, and delivery state. `scripts/backlog.py` computes the schedule from PBI metadata and touched files; do not maintain a separate hand-authored wave schedule.

## Repository Layout

The root `backlog/` directory is the central, durable PBI repository:

- `backlog/index.md`
- `backlog/maps/`
- `backlog/epics/`
- `backlog/features/`
- `backlog/stories/`
- `backlog/spikes/`
- `backlog/tasks/`
- `backlog/bugs/`

Feature implementation context lives separately under `specs/NNN-slug/`: `spec.md`, `research.md`, `plan.md`, and `tasks.md`. PBI files always remain in the central `backlog/`; re-parenting a PBI changes its `PARENT` relation, never its path.

## Three Declared Inputs, One Computed Schedule

Declare only these three scheduling inputs. `scripts/backlog.py` computes the schedule from them:

1. **`rank`:** Optional integer on a child PBI, conventionally assigned in increments of 10 (`10`, `20`, `30`, …). Lower numbers mean higher priority and earlier delivery among siblings sharing the same `PARENT`. A rank that contradicts a `BLOCKED_BY` dependency among siblings is an error.
2. **`BLOCKED_BY`:** A strict finish-to-start dependency. A blocked PBI and its descendants wait until the blocker and all of the blocker's descendants are done. A child `SPIKE` blocking its own `PARENT` story is valid; exempt that dependency from ancestor self-inheritance so it does not block itself.
3. **Touched files:** Read the exact paths from `## Files` in each `TASK`. Aggregate descendant Task paths to their parent `US` when calculating story-level file conflicts. A `SPIKE` touches no code files.

## Waves and the `[P]` Marker

`[P]` and wave assignment are computed by `scripts/backlog.py`, not declared by authors. Pack items into sequential waves while respecting `BLOCKED_BY` and ensuring that no two items in the same wave share touched files; use `rank` to break otherwise eligible ties. Every item in a wave of size two or more carries `[P]`: those items can run concurrently without file conflicts.

## Execution, PRs, and State

- Create one PR/MR per `US`. Read `.specify/memory/constitution.md` under **Delivery Conventions** for the `Story isolation` mode: `worktree` by default, `branch`, or `ask`. For `ask`, stop before execution, ask the user, and recommend `worktree`.
- For a `US`-level `BLOCKED_BY` dependency, "done" means the blocking story's PR has been merged.
- Task completion state lives exclusively in the checkboxes in `backlog/tasks/TASK-xxx.md`, under `## Actions to complete` and `## Definition of Done`. Do not maintain parallel task state in `tasks.md`; this avoids merge conflicts across parallel worktrees. `scripts/backlog.py render-tasks` derives the corresponding `- [X]` state for `tasks.md` from those task files.
- Plan approximately 2–4 cohesive `TASK`s per `US` (for example, Gherkin acceptance tests, domain/persistence, and endpoint/UI work). Each task should be a useful board item for a human developer and a self-contained brief for an autonomous sub-agent. Do not create trivial, single-file boilerplate micro-tasks.
