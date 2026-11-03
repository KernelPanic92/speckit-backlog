## Preset `backlog` addendum

> This project uses the `backlog` preset. The rules below **refine the steps above**; where they conflict with the generic wording above, these rules win.

**Artifacts in this project**

- `spec.md` is the root PBI (MAP, EPIC or US) plus the spec envelope; the child PBIs live under `FEATURE_DIR/backlog/` (`epics/`, `stories/`, `spikes/`, `tasks/`).
- `tasks.md` is an **execution index**: each line is `- [ ] TASK-xxx [P?] [US-xxx?] Title → backlog/tasks/TASK-xxx-….md`, under the heading of its story (`### US [US-xxx] Title`). The task's details (Outcome, `Covers:`, Files, Actions to complete, Out of Scope, DoD, BLOCKED_BY relations) live in the linked TASK file.
- There is no data-model.md, contracts/ or quickstart.md: the data model, the API contracts and the testing strategy are sections of plan.md; the validation scenarios are the Gherkin Acceptance Criteria of the stories (`US-xxx/AC-n`).

**Step 3 (load context)** — also read, for the phase being executed, the stories it covers (`backlog/stories/`), and `.specify/memory/product.md` so that code names follow the Ubiquitous Language terms. For UI work read `.specify/memory/design.md`: use its tokens through the code locations the plan names (never hard-coded values), follow its component rules and its Do's and Don'ts, and keep every text/background pair at the accessibility target it states.

**Step 5 (parse tasks.md)** — the phases are those of the spec mode: map → Setup, Walking Skeleton, one phase per Release Lane, Polish; epic → Setup, Foundational, one phase per story, Polish; story → Setup, Spikes, one phase per Acceptance Criterion or group, Polish. Task order inside a phase also follows the BLOCKED_BY relations of the TASK files.

**Step 6-8 (execution)** — for every task:

1. Open its TASK file and do exactly what its Outcome, Files and Actions describe; respect its Out of Scope.
2. For acceptance-test tasks (`Covers: US-xxx/AC-n "title"`), turn each covered Gherkin scenario into an automated test that fails before the implementation, keeping the scenario's Given/When/Then wording recognizable.
3. When done, tick the task's Actions to complete and its DoD items in the TASK file, then mark its line `[X]` in tasks.md.
4. Never mark a task done while one of the tasks it is BLOCKED_BY is still open.
5. If the task is RELATED to a SPIKE it closes (a prototype the research could not replace), record the answer in research.md as a decision headed by its topic, tick the Spike's Exit Criteria and link that decision from them (`[the payment provider decision](../../research.md#payment-provider)`).

**Checkpoints** — at the end of each phase verify that every Gherkin scenario of the stories in that phase passes (map: the lane's Metrics can be measured). Report the phase as complete only then; otherwise stop and report which scenarios fail, each as `US-xxx/AC-n "title"` with its story title.

**References** — whatever you write in the TASK files, research.md or tasks.md and whatever you report follows the "Readable references" section of `.specify/presets/backlog/knowledge/pbi-writing/rules.md`: tasks as `TASK [id] title`, stories as `US [id] title`, scenarios as `US-xxx/AC-n "title"`, other documents as links whose text names the topic; never a bare id, a bare path or a section number.

**Step 9 (completion validation)** — "matches the original specification" means: every story implemented in this run satisfies all its Acceptance Criteria and none of its Out of Scope items was built.
