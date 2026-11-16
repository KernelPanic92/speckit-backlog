---
description: Create, map, split, refine, reorder, and retire Product Backlog Items (MAP, EPIC, FEATURE, US, SPIKE) in the central backlog/ following INVEST, vertical splitting, User Story Mapping, and Gherkin BDD rules.
handoffs:
  - label: Specify a Feature or Story from the backlog
    agent: speckit.specify
    prompt: Specify a Feature or Story from the backlog
  - label: Update product personas and Ubiquitous Language
    agent: speckit.constitution
    prompt: Update product personas and Ubiquitous Language
scripts:
  sh: scripts/bash/resolve-template.sh pbi-story-template --json
  ps: scripts/powershell/resolve-template.ps1 pbi-story-template -Json
  py: scripts/python/resolve_template.py pbi-story-template --json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

Manage the durable product backlog independently of spec creation. `__SPECKIT_COMMAND_SPECIFY__` selects functional PBIs into a specification; it does not own their files.

### 1. Load rules and context

- `PBI_RULES` = `.specify/presets/backlog/knowledge/pbi-writing/rules.md`. Read it in full; follow its conditional references when triggered. It owns PBI writing and Readable References; this command owns placement and workflow.
- `DELIVERY_RULES` = `.specify/presets/backlog/knowledge/delivery/rules.md`. Read it for hierarchy placement, rank, dependencies, wave-based `[P]` scheduling and one PR/MR per User Story with isolated worktrees by default.
- `SCHEMA` = `.specify/presets/backlog/schemas/pbi-frontmatter.schema.json`. The seven types are `MAP`, `EPIC`, `FEATURE`, `US`, `SPIKE`, `BUG`, `TASK`. Do not invent metadata; BUG creation belongs to the bug extension.
- `PRODUCT` = `.specify/memory/product.md`. Read Personas and Ubiquitous Language. If missing, warn and suggest `__SPECKIT_COMMAND_CONSTITUTION__`; proceed only with user-confirmed personas and business context, never invented actors.
- `BACKLOG_TOOL` = `uv run --no-project --quiet --with pyyaml --with jsonschema python .specify/presets/backlog/scripts/backlog.py`.

Every `BACKLOG_TOOL <subcommand> [args]` below means the full invocation above, run from the repository root as a **standalone command**, never chained with `;`, `&&`, or `|`, so permissions can allow-list it. Parse its JSON; if it cannot run, stop and report rather than pretending validation or rendering succeeded.

### 2. Classify and perform the request

Use `$ARGUMENTS` as natural-language guidance, not a required subcommand grammar. If empty, inspect `backlog/index.md` or root `backlog/` and ask what the user wants to create, map, split, refine, or reorder.

#### Create / Map / Split

Accept a raw idea/requirement or an existing PBI such as `EPIC-001` or `FEATURE-002`. For existing PBIs, first run `BACKLOG_TOOL locate <ID> --descendants` and read the returned files, `referenced_by`, `specs` and descendants. Keep valid existing slices and permanent IDs; do not duplicate them.

1. **Constraint 0 context check before generation.** Check product Personas, business context, system constraints and Ubiquitous Language. Ask at most **3 blocking questions** immediately, then wait and apply answers before writing. Propose new personas/terms for approval and add approved entries to `PRODUCT` (create only the user-confirmed context if missing). Put non-blocking reasonable defaults in the affected PBI's `## Assumptions`. Never deliver unanswered question lists or `[NEEDS CLARIFICATION]` markers in PBIs.
2. **Resolve templates before writing.** Run `{SCRIPT}` for `pbi-story-template`, parsing `TEMPLATE_CONTENT`. Use the same resolver with `pbi-feature-template`, `pbi-epic-template`, `pbi-map-template`, `pbi-spike-template`, or `pbi-task-template` for every type needed. Use resolved content, including project/preset overrides, never a raw template as a shortcut. Stop on resolution failure.
3. **Allocate permanent IDs.** Run `BACKLOG_TOOL next-id <TYPE>` for each new PBI (or `--count N` for a batch, consuming each returned ID once). Write allocated files before requesting further IDs of that type; never renumber existing PBIs. Assign sibling `rank` in steps of 10 (`10, 20, 30...`), consistent with real `BLOCKED_BY` dependencies.
4. **Execute the exact PBI_RULES phases.** Print concise decision summaries in the prescribed Macro-Analysis / Feature Check / Micro-Scope format, not private deliberation:
   - **Phase 1 Macro-Analysis**: Request, distinct user activities, **Container** decision and Working criteria. Without a map, a bounded capability is a `FEATURE`, an open-ended area an `EPIC`, a story-sized request needs no container.
   - **Phase 3a** before drafting when there is more than one user activity or a map is requested: load the map rules reference; write the MAP, one EPIC per Backbone Macro-Activity, one Walking Skeleton TASK/SPIKE per Epic, and one FEATURE per populated Epic × Release Lane intersection, **printing Feature Check before writing each Feature**. Lanes are titled by Outcome; the Walking Skeleton is not the MVP.
   - **Phase 2 Iterative Drafting**: print **Feature Check before each Feature**, then print **Micro-Scope Reasoning before each US**; never write two stories without their intervening checks. Use Connextra, INVEST, vertical slicing, separate Read/Write and List/Detail, ~2–5 Gherkin scenarios with stable `AC-n` headings, one `When`, binary outcomes and complete asynchronous cycles. Each US belongs to its FEATURE (or EPIC when no Feature exists). Add a timeboxed SPIKE when uncertainty prevents estimation; the blocked PBI declares `BLOCKED_BY` the Spike.
   - **Phase 3b** if mapped: complete Release Lanes with Features and stories in lane/Backbone order, Metrics and the justified DoR Check. A story never precedes its blocker in release order.
   - **Final Check & Summary**: re-read, re-split violations, and list PBIs as `type [id] title` in release order, never Epic by Epic. Apply Readable References throughout the files, relation reasons and conversation.
5. **Write one file per PBI at repository root**: `backlog/{maps,epics,features,stories,spikes,tasks}/<ID>-<slug>.md`, selecting the directory by type. Slugs are lowercase ASCII kebab-case, at most 6 words. All metadata stays in schema-valid frontmatter; omit empty optional keys and placeholders. Relations are child/blocked-side only, ordered by `PARENT`, `BLOCKED_BY`, `RELATED`, then type (`MAP`, `EPIC`, `FEATURE`, `US`, `SPIKE`, `BUG`, `TASK`), then ID. Keep required Out of Scope (EPIC: Scope Boundaries), with destinations or "not planned".

#### Refine / Reorder / Reparent

Run `BACKLOG_TOOL locate <ID> --descendants` for each target **before editing**, saving its impacted `specs`. Read the target and its ancestors, descendants and references. Update bodies, `PARENT`, `BLOCKED_BY`, or sibling `rank` **in-place**; paths and IDs never change on re-parenting. Preserve the single-parent hierarchy. Re-split if edits push a US past ~2–5 scenarios (unless value atomicity is justified), resolving templates and allocating new IDs as above. Reconcile map lanes and relation titles/reasons when affected. Never encode parallelism by hand: `[P]` comes from `BLOCKED_BY`, `rank` and disjoint TASK `## Files` through the scheduler.

#### Retire / Delete

Run `BACKLOG_TOOL locate <ID> --descendants` first. Show the user the target, descendants, **all `referenced_by` PBIs** and **all impacted `specs`**, with readable titles and links. Ask for explicit confirmation **and** how children and references should be re-parented/updated before removing anything. Apply that agreed migration, then use `git rm` for tracked files or `rm` for untracked files. Do not silently cascade-delete descendants, leave dangling references, or reuse retired IDs.

#### Boundary with `__SPECKIT_COMMAND_TASKS__`

Never create or edit implementation `TASK`s for User Stories here. The only TASKs `__SPECKIT_COMMAND_BACKLOG__` creates are Walking Skeleton items during Phase 3a of a User Story Map. Direct implementation-task changes to `__SPECKIT_COMMAND_TASKS__`; coordinate affected task reconciliation there rather than editing its owned content.

### 3. Refresh indices and validate

1. Collect impacted spec directories from `locate` results for every touched PBI, including newly re-parented ancestors; retain the pre-edit results for deleted/moved references.
2. Run `BACKLOG_TOOL render-index` to deterministically refresh `backlog/index.md` (functional hierarchy, story waves and `tasks: done/total` counters, not an exploded implementation-task list).
3. For every existing `specs/*/spec.md` whose `**Scope**:` includes touched PBIs, run `BACKLOG_TOOL render-spec <spec-dir>`. If task scope or scheduling changed for a spec with an existing `tasks.md`, also run `BACKLOG_TOOL render-tasks <spec-dir>`; never hand-edit rendered blocks or task lines.
4. Run `BACKLOG_TOOL check` and fix all structural errors (schema, hierarchy, canonical relations, cycles, rank/blockers, required sections, map lanes, relative links, stale renders and applicable AC coverage). If implementing a fix belongs to task reconciliation, route it to `__SPECKIT_COMMAND_TASKS__` and report the blocker instead of crossing the boundary. Stop and report if errors cannot be resolved; never claim completion with a failing check.
5. Apply the **Readable References self-check**: PBI references carry type/ID/title, scenarios carry `US-xxx/AC-n "title"`, links name their topic and land on the right heading; no bare IDs, URLs, paths, coined abbreviations or untitled section numbers in prose.

## Completion Report

Report the operation, created/reused/updated/retired PBIs by type and readable title in release order, changed personas/terms, affected specs and refreshed indices, validation outcome, and next command (`__SPECKIT_COMMAND_SPECIFY__` for a selected Feature/story or `__SPECKIT_COMMAND_TASKS__` for implementation-task reconciliation). Report remaining blockers honestly; no unanswered questions masquerading as finished PBIs.

## Done When

- [ ] User-confirmed context and approved Personas / Ubiquitous Language used; assumptions explicit
- [ ] Correct PBI_RULES phases completed; permanent IDs, hierarchy, rank and root backlog paths preserved
- [ ] Destructive changes confirmed with an agreed reference/child migration
- [ ] Root index and every impacted rendered spec/task index refreshed; `BACKLOG_TOOL check` passes
- [ ] Readable References checked; completion reported without unresolved question lists
