## Preset `backlog` addendum

> This project uses the `backlog` preset. The rules below **refine the steps above**; where they conflict with the generic wording above, these rules win.

**Artifacts** — `FEATURE_DIR/spec.md` has 4 blocks: Header with `**Scope**:`, rendered Backlog, optional Key Entities and measurable Success Criteria (plus any clarification log). All permanent PBIs live in repository-root `backlog/{maps,epics,features,stories,spikes,tasks,bugs}/`. Load scoped US (Connextra, Gherkin ACs, Out of Scope), parent FEATURE (Outcome, Constraints, Out of Scope), EPIC/MAP context and existing TASKs. The seven-type model includes FEATURE and BUG (BUG creation belongs to the bug extension). Data Model, API Design / Contracts and Testing Strategy are sections of plan.md, not separate data-model.md / contracts/. Terms follow `.specify/memory/product.md` → Ubiquitous Language.

Read `.specify/presets/backlog/knowledge/pbi-writing/rules.md` and `.specify/presets/backlog/knowledge/delivery/rules.md`. `BACKLOG_TOOL` = `uv run --no-project --quiet --with pyyaml --with jsonschema python .specify/presets/backlog/scripts/backlog.py`. Every operation below expands to that full invocation as a **standalone command** from root, never chained with `;`, `&&`, or `|`, so permissions can allow-list it. Stop/report if unavailable rather than fabricating a check or hand-authoring rendered state. Resolve Scope with `BACKLOG_TOOL locate <ID> --descendants`; inspect `BACKLOG_TOOL schedule --spec FEATURE_DIR` for computed Story/Task Waves and `[P]` (BLOCKED_BY + rank + disjoint exact TASK Files). Each US keeps its own PR/MR, isolated in a worktree by default under constitution Delivery Conventions; do not turn convergence into a cross-story implementation PR.

**Source references** — map the generic keys above to this project's keys:

| Generic key above | Key in this project |
|-------------------|---------------------|
| `FR-###` | `US-xxx/AC-n "scenario title"` — a Gherkin scenario of a story, always with its title |
| `US1/AC2` | `US-001/AC-2 "Card declined"` |
| `SC-###` | `SC-### "short name"` — measurable outcomes in spec.md; MAP lane Metrics contextualize the scoped lane |
| "P1 user story" | a story in the first scoped Story Wave or first Outcome-titled Release Lane; use its real title |
| Scope boundary | the Out of Scope of `US [US-xxx] Title` **and** its parent `FEATURE [FEATURE-xxx] Title` — building either excluded capability is an `unrequested` finding |

Every key in the findings and in the appended tasks follows the "Readable references" section of `.specify/presets/backlog/knowledge/pbi-writing/rules.md`: the id stays for traceability, the title always comes with it, and the `§` notation is never used.

**Appending convergence tasks** — replace any generic instruction to append hand-written tasks.md lines with this source-PBI workflow (after the generic command's required approval):

1. Inspect existing tasks to avoid duplicate findings; completed TASK files stay untouched. Allocate each new permanent ID using `BACKLOG_TOOL next-id TASK` (or `--count N` and consume each returned ID once), not `T{M+1:03d}`. Save allocated files before requesting further IDs of that type.
2. Resolve `pbi-task-template` with `.specify/scripts/bash/resolve-template.sh pbi-task-template --json`, `.specify/scripts/powershell/resolve-template.ps1 pbi-task-template -Json`, or `python .specify/scripts/python/resolve_template.py pbi-task-template --json`. Use composed `TEMPLATE_CONTENT`; stop on resolution failure.
3. Write `backlog/tasks/<ID>-<slug>.md` (lowercase ASCII kebab-case slug, max 6 words). Set `PARENT` to the story the finding traces to, or the spec's **FEATURE/EPIC container** for a cross-story finding (single-story spec: that US). For a MAP/multi-container spec, select the relevant FEATURE/EPIC or ask if ownership is unclear; never create orphan tasks. Set sibling rank in increments of 10. Declare `BLOCKED_BY` prior story TASKs or stories when needed so convergence lands **after** the work it repairs; do not rely on a manually appended phase for order. Relations follow PARENT, BLOCKED_BY, RELATED, then canonical type and ID.
4. Put the readable source reference (`US-xxx/AC-n "title"`, `SC-### "short name"`, parent Out of Scope, or a named constitution/plan rule) and gap type in the Outcome. Include exact `## Files`, checkable Actions, Out of Scope and DoD; acceptance-test tasks have `**Covers:**` with titled scenarios. From the central TASK file compute links such as `../../specs/<dir>/plan.md#api-design--contracts` or `../stories/US-xxx-<slug>.md#ac-n-title`. Group cohesive fixes; do not explode a finding into boilerplate micro-tasks.
5. Run `BACKLOG_TOOL render-tasks FEATURE_DIR`, then `BACKLOG_TOOL render-index`, then `BACKLOG_TOOL check --spec FEATURE_DIR`, each standalone. **Never hand-write generated task lines, checkboxes, phases or `[P]` markers.** If new touched-file conflicts change rendered Story Waves, refresh only the generated spec block with `BACKLOG_TOOL render-spec FEATURE_DIR` and rerun the check. Refresh other impacted generated indices as necessary; functional PBI bodies, Scope and plan remain untouched. Fix only new TASK source errors; report unrelated existing defects rather than silently broadening scope.

Task completion remains exclusively in each central TASK's **Actions to complete** and **Definition of Done** checkboxes; the renderer derives tasks.md `[X]`. Report new TASKs with readable titles, AC/outcome/scope traceability, computed placement and validation outcome. Apply the Readable References self-check to findings, tasks and final report.
