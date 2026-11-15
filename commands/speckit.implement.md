## Preset `backlog` addendum

> This project uses the `backlog` preset. The rules below **refine the steps above**; where they conflict with the generic wording above, these rules win.

### Artifacts and tool

- `FEATURE_DIR/spec.md` has four blocks: Header with `**Scope**:`, rendered `## Backlog`, optional Key Entities and Success Criteria. A Clarifications log may follow; no root PBI is embedded here.
- All durable PBIs live in **repository-root** `backlog/{maps,epics,features,stories,spikes,tasks,bugs}/`. The model has seven types (`MAP`, `EPIC`, `FEATURE`, `US`, `SPIKE`, `BUG`, `TASK`); these commands do not create BUGs. Read scoped stories, their FEATURE/EPIC/MAP ancestors and blocking SPIKEs, not only the spec's rendered summary.
- `FEATURE_DIR/tasks.md` is a **generated execution index**, not a progress source. TASK Outcomes, `Covers:`, exact `## Files`, Actions, Out of Scope, DoD, PARENT, BLOCKED_BY and rank live in `backlog/tasks/TASK-xxx-<slug>.md`. Links from tasks.md use `../../backlog/tasks/...`.
- Data Model, API Design / Contracts and Testing Strategy live in the single `plan.md`; Gherkin scenarios in central stories are the validation scenarios. Do not expect separate data-model.md, contracts/ or quickstart.md.
- Read `.specify/presets/backlog/knowledge/delivery/rules.md`, the PBI writing rules' Readable References, `.specify/memory/constitution.md` and `.specify/memory/product.md` (Ubiquitous Language). For UI work also read `.specify/memory/design.md`; use its actual tokens/components through the code locations the plan names and meet its accessibility target.

`BACKLOG_TOOL` = `uv run --no-project --quiet --with pyyaml --with jsonschema python .specify/presets/backlog/scripts/backlog.py`.

Every operation below expands to this full invocation from repo root as a **standalone command**, never chained with `;`, `&&`, or `|`, so permissions can allow-list it. Stop/report if unavailable, rather than inventing a schedule or hand-editing generated state.

### One PR/MR per User Story and Story Isolation

1. **Before execution**, check **Story isolation** in `.specify/memory/constitution.md` → **Delivery Conventions**: `worktree` (default recommendation), `branch`, or `ask`. When `ask` **or absent**, ask the user and wait; recommend `worktree`. Never interpret missing configuration as permission to run concurrent stories in a shared checkout.
2. Each US gets **one separate PR/MR** and its own isolated story branch. In `worktree` mode create a **new worktree with a new branch per US**; never recycle another session's worktree or alter its branch, uncommitted changes, commits or index. In `branch` mode execute stories sequentially on their separate branches; do not run concurrent branch checkouts in one working directory. Coordinate shared Setup/Foundational work before dependent story branches, and separately assign cross-story Polish work without mixing multiple US implementations into one PR.
3. Run `BACKLOG_TOOL render-tasks FEATURE_DIR`, then `BACKLOG_TOOL schedule --spec FEATURE_DIR`. Inspect JSON **Story Waves**, **Task Waves**, `critical_path` and computed `parallel` booleans. `[P]` is computed from **BLOCKED_BY + rank + disjoint `## Files`** (story file sets aggregate descendant TASK paths). Never mark a story/task parallel by guesswork.
4. Stories marked `[P]` **in the same Story Wave** can run concurrently **in isolated git worktrees**, after all blockers and shared prerequisites are satisfied. A US `BLOCKED_BY` another US starts **only after the blocking story's PR/MR is merged**, not merely after its tasks are checked or its branch exists. Bring merged prerequisites into the new story branch using the project's normal integration policy.
5. Execute Setup → Walking Skeleton / Foundational → computed Story Waves (or map Release Lanes) → Polish as generated, respecting actual blockers rather than treating section position as the source of dependencies. Recompute when source inputs change; do not maintain a second wave schedule.

### Task execution and parallel sub-agents

For each eligible task:

1. Open `backlog/tasks/TASK-xxx-<slug>.md`; do exactly its Outcome, Files and Actions, respecting Out of Scope and the relevant plan/research decisions. Never mark completion while a declared blocker is open.
2. When **Acceptance tests from Gherkin** is `on` (default), execute the story's acceptance-test TASK before implementation: turn each `**Covers:** US-xxx/AC-n "title"` scenario into a recognizable Given/When/Then automated test, observe the expected failure, then implement until it passes. Preserve completed TASK history; changed requirements use delta tasks through `__SPECKIT_COMMAND_TASKS__`.
3. **Within a story/phase**, TASKs marked `[P]` **in the same Task Wave** have disjoint exact Files and satisfied blockers. Delegate them **concurrently to sub-agents when supported**. Pass the TASK file, relevant `plan.md` sections and research decisions, assigned worktree/branch, allowed Files/Out of Scope, dependencies and verification command as a **self-contained brief**. Do not delegate work with file overlap or run sequential calls while claiming parallel execution. If sub-agents are unavailable, execute eligible tasks sequentially without weakening the dependency rules.
4. If a closing TASK is RELATED to an open prototype SPIKE, complete its evidence-producing work, record the decision under a named topic in research.md and tick only satisfied Spike Exit Criteria. From the root Spike file, link back as `[the payment provider decision](../../specs/<dir>/research.md#payment-provider)`, computing the actual relative path/heading. Do not mark a Spike answered just because its TASK was scheduled.

### Progress state and generated indices

**The sole task completion source** is the checkboxes under `## Actions to complete` and `## Definition of Done` (including the template's `## Definition of Done (DoD)`) **inside each `backlog/tasks/TASK-xxx-<slug>.md`**. Check off only verified actions / satisfied DoD there.

After progress updates run `BACKLOG_TOOL render-tasks FEATURE_DIR`, then `BACKLOG_TOOL render-index`. `[X]` in tasks.md is derived only when all Actions/DoD checkboxes in the TASK are checked; **never manually mark a tasks.md line**. Workers update their assigned TASK source files, not shared checkbox ledgers; regenerate aggregate indices during integration rather than resolving generated checkbox conflicts by hand. Do not touch another worker's worktree to refresh its state.

If Files, blockers, scope or schedule inputs changed, coordinate source reconciliation through `__SPECKIT_COMMAND_TASKS__`, re-run schedule, and refresh affected spec blocks with `BACKLOG_TOOL render-spec FEATURE_DIR`. Finish with `BACKLOG_TOOL check --spec FEATURE_DIR` and report any blocking errors instead of claiming completion.

### Checkpoints, references and completion

At each completed story/phase, verify every scoped Gherkin scenario (map: also measure the lane's Metrics where applicable). "Matches the original specification" means the delivered US meets all its ACs and **none of its own or parent FEATURE's Out of Scope items was built**. A completed implementation is not a merged PR; report those states separately, with story PR/MR links and blocked next waves.

Apply Readable References to files and reports: `TASK [id] title`, `US [id] title`, `FEATURE [id] title`, `US-xxx/AC-n "title"`, `SC-### "short name"` and topical document links with correct anchors. No bare IDs, paths, URLs or untitled section numbers in prose. Report tests run/results, TASK progress, generated-index/check results, story isolation mode, PR/MR status and any remaining blockers honestly.
