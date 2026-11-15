---
description: Idempotently reconcile cohesive TASK PBIs in root backlog/tasks/ and deterministically render tasks.md with wave-based [P] scheduling and Gherkin AC coverage.
handoffs:
  - label: Analyze For Consistency
    agent: speckit.analyze
    prompt: Run a project analysis for consistency
    send: true
  - label: Implement Project
    agent: speckit.implement
    prompt: Start the implementation in phases
    send: true
scripts:
  sh: scripts/bash/setup-tasks.sh --json
  ps: scripts/powershell/setup-tasks.ps1 -Json
  py: scripts/python/setup_tasks.py --json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before tasks generation)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_tasks` key
- If the YAML cannot be parsed or is invalid, do not skip silently: tell the user that `.specify/extensions.yml` could not be read (include the parser error) and that no hooks were checked, including any mandatory (`optional: false`) hooks registered there, then continue normally
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- For each executable hook, output the following based on its `optional` flag:
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Pre-Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Mandatory hook** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Pre-Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}

    Wait for the result of the hook command before proceeding to the Outline.
    ```
    After emitting the block above you MUST actually invoke the hook and wait for it to finish before continuing. Run it the same way you would run the command yourself in this agent/session (the invocation may differ from the literal `{command}` id shown above, e.g. a skills-mode agent runs it as `/skill:speckit-...` or `$speckit-...`). Emitting the block alone does not run the hook.
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## Outline

**Paths and tool** (preset `backlog`):

- `PBI_RULES` = `.specify/presets/backlog/knowledge/pbi-writing/rules.md` — Task/Spike writing, schema conventions, required sections and Readable References.
- `DELIVERY_RULES` = `.specify/presets/backlog/knowledge/delivery/rules.md` — root placement, rank/blockers/files as the only scheduling inputs, computed waves/`[P]`, one PR/MR per US with worktree isolation by default.
- `SCHEMA` = `.specify/presets/backlog/schemas/pbi-frontmatter.schema.json` — seven types `MAP`, `EPIC`, `FEATURE`, `US`, `SPIKE`, `BUG`, `TASK`; do not create BUGs here.
- `BACKLOG_TOOL` = `uv run --no-project --quiet --with pyyaml --with jsonschema python .specify/presets/backlog/scripts/backlog.py`.

Expand every `BACKLOG_TOOL` operation below to this full invocation, run from repo root as a **standalone command**, never chained with `;`, `&&`, or `|`, so permissions can allow-list it. Parse JSON and stop/report if tooling is unavailable; do not substitute hand-authored rendered lines.

1. **Setup**: Run `{SCRIPT}` (setup-tasks) from repo root once and parse `FEATURE_DIR`, `TASKS_TEMPLATE_CONTENT`, `TASKS_TEMPLATE`, `AVAILABLE_DOCS`. Paths supplied as absolute must remain absolute for filesystem operations. Read the resolved tasks scaffold for conventions, **not** to hand-write the index.
   - Resolve `pbi-task-template` with `.specify/scripts/bash/resolve-template.sh pbi-task-template --json`, `.specify/scripts/powershell/resolve-template.ps1 pbi-task-template -Json`, or `python .specify/scripts/python/resolve_template.py pbi-task-template --json`. Use `TEMPLATE_CONTENT` (including composition/overrides); stop on resolution failure.
   - Treat `$ARGUMENTS` as direct guidance, with **no subcommand ceremony**: honor targeted splitting, merging, regeneration for a named story, or retiring a task, subject to completed-task preservation and deletion confirmation below.

2. **Load context and inventory**:
   - Required: `FEATURE_DIR/spec.md` (4 blocks with `**Scope**:` and rendered Backlog) and `plan.md` (Technical Context, Project Structure, Data Model, API Design / Contracts, Testing Strategy, Delivery Slices). Read `research.md` for decisions and open prototype Spikes when present; report its absence, never invent decisions.
   - Run `BACKLOG_TOOL locate <ID> --descendants` for each scope selector. Read scoped stories and FEATURE/EPIC/MAP ancestors from root `backlog/`, blocking SPIKEs, Walking Skeleton items, and **existing `backlog/tasks/TASK-*.md` belonging to scoped PBIs**. Keep locator `specs` for shared-artifact refreshes. Do not treat `FEATURE_DIR` as the root of backlog paths.
   - Read `.specify/memory/constitution.md` (`/memory/constitution.md` in the upstream workflow). **Acceptance tests from Gherkin** is `on` by default; Quality Standards supply task DoD. Read `.specify/memory/product.md` for Ubiquitous Language.
   - For UI work read `.specify/memory/design.md`; task Outcomes/Actions name real design tokens and components instead of inventing literal colors, sizes or fonts.
   - Read `PBI_RULES`, `DELIVERY_RULES` and `SCHEMA`. Inventory task completion from the TASK files, **never** from cached `tasks.md` checkboxes.

3. **Design cohesive task briefs**:
   - Target **~2–4 cohesive TASKs per US**, not single-boilerplate micro-tasks. When acceptance tests are `on`, plan **one acceptance-test task before 1–3 implementation tasks**. Its `**Covers:** US-xxx/AC-1 "Title", ...` lists every covered scenario with its title. Implementing tasks declare real `BLOCKED_BY` on the tests, so tests are written and fail first. When tests are `off`, create test tasks only when requested; do not demand artificial AC coverage contrary to the constitution.
   - Map each story's full end-to-end behavior, entities and contracts to its task set. Group useful work a human can track and an autonomous sub-agent can complete, rather than splitting every file or layer into an artificial task.
   - **Zero orphan tasks**: story tasks set `PARENT` to their US. Cross-story **Setup**, **Foundational** and **Polish** tasks set `PARENT` to the spec's container (`FEATURE` or `EPIC`); for a single-story spec, to that US. Walking Skeleton items keep their valid EPIC/FEATURE parent. For MAP/multi-container scope choose the relevant FEATURE/EPIC for each shared item (split the item if needed); never use MAP or no parent as a shortcut. If ownership cannot be determined, ask before writing.
   - **Polish** TASKs declare `BLOCKED_BY` on the stories or final story tasks they follow; do not rely on a phase label alone to impose ordering.
   - Each open **prototype SPIKE** gets a closing TASK (`PARENT`: the blocked US; `RELATED`: the SPIKE, reason "closes the Spike"). Story tasks declare `BLOCKED_BY` that closing TASK. Do not make it `BLOCKED_BY` the Spike it closes; that would deadlock. It documents the research decision and satisfies Spike Exit Criteria before the story's implementation proceeds. For shared Spikes, identify the owning blocked US and make every affected story's work wait for the same closing task; ask if ownership is unclear.
   - Declare exact touched paths in each TASK's `## Files`, real `BLOCKED_BY`, and sibling `rank` in steps of 10 (`10, 20, 30...`). The scheduler computes Story Waves and Task Waves / `[P]` from these; neither authors nor a hand-edited task index declare parallelism.

4. **Idempotently reconcile existing central TASKs**, respecting the user guidance:
   - Match by parent story/container and actual Outcome / covered ACs, not just a similar title or previous line position. Reuse existing Walking Skeleton and prior-run tasks; never duplicate them.
   - **Completed tasks**: all checkboxes in `## Actions to complete` and `## Definition of Done` (the template's `## Definition of Done (DoD)`) are checked `[x]` / `[X]`. **Preserve these files untouched**, including metadata, paths, IDs and checkboxes. If requirements changed, add a delta TASK instead of reopening, deleting, renumbering or rewriting completed history.
   - **Open matching tasks**: reuse the permanent `TASK-xxx` ID and path; update Outcome, `Covers:`, `## Files`, Actions, DoD, real `BLOCKED_BY` and `rank` in place as required. Preserve checked sub-actions that remain valid; do not reset progress as a side effect of regeneration.
   - **New tasks**: allocate with `BACKLOG_TOOL next-id TASK` (or `--count N` and consume each returned ID exactly once), then write `backlog/tasks/<ID>-<slug>.md` using the resolved template. Save allocated files before requesting more IDs. Slug: lowercase ASCII kebab-case, at most 6 words; IDs and existing paths never change on re-parenting.
   - **Obsolete open tasks**: list them with readable titles and the affected references/descendants from `BACKLOG_TOOL locate <ID> --descendants`. Ask for confirmation and a reference migration before removing via `git rm` (tracked) / `rm` (untracked). Unconfirmed tasks remain, explicitly reported. A user request to regenerate is not blanket authorization to delete.
   - TASK frontmatter is schema-valid, with at most one PARENT; relations are child/blocked-side only and canonically ordered (`PARENT`, `BLOCKED_BY`, `RELATED`; then `MAP`, `EPIC`, `FEATURE`, `US`, `SPIKE`, `BUG`, `TASK`; then ID).
   - TASK bodies contain a concrete **Outcome**, optional acceptance-test `**Covers:**`, exact **Files**, checkable **Actions to complete**, **Out of Scope** with destinations/not planned, and **Definition of Done** reflecting the constitution. No Connextra/INVEST for technical tasks. Write enough context for a self-contained sub-agent brief; quote Data Model field constraints (length, nullability, enum, validation) **verbatim**, not "as appropriate".
   - From `backlog/tasks/`, link plan decisions as `[the card payment contract](../../specs/<dir>/plan.md#api-design--contracts)` and research as `[the provider decision](../../specs/<dir>/research.md#provider)`, computing the actual path/anchor. Include necessary technical detail in the TASK itself; spec-local working files must not be its only explanation.

5. **Render deterministically and validate**, each standalone:
   - Run `BACKLOG_TOOL render-tasks FEATURE_DIR`. **Do NOT hand-write `tasks.md` task lines, phases, completion checkboxes, wave assignments or `[P]` markers.** The tool derives everything from scoped PBIs, TASK files and their completion checkboxes.
   - Run `BACKLOG_TOOL render-spec FEATURE_DIR` (task file conflicts can change Story Waves in the rendered Backlog), then `BACKLOG_TOOL render-index`.
   - Run `BACKLOG_TOOL schedule --spec FEATURE_DIR` to inspect `story_waves`, `task_waves`, `critical_path` and computed `parallel` booleans for the report. Honor blockers even if tasks have different files.
   - Refresh other impacted specs / existing task indices from locator results when shared tasks, scopes or schedules changed.
   - Run `BACKLOG_TOOL check --spec FEATURE_DIR`. Fix schema, parent, dependency, rank/file, link, stale-render or **`ac-uncovered`** errors, then re-render and re-check (up to 3 iterations; report blockers if still failing). When acceptance tests are on, every scoped Gherkin AC needs a test TASK `Covers:` entry; a test-like title alone is not coverage.
   - Apply the Readable References self-check to TASKs, indices and report: type/ID/title, `US-xxx/AC-n "title"`, descriptive relative links with correct anchors. Never patch generated text to conceal an error in the source PBIs.

## Mandatory Post-Execution Hooks

**You MUST complete this section before reporting completion to the user.**

Check if `.specify/extensions.yml` exists in the project root.
- If it does not exist, or no hooks are registered under `hooks.after_tasks`, skip to the Completion Report.
- If it exists, read it and look for entries under the `hooks.after_tasks` key.
- If the YAML cannot be parsed or is invalid, do not skip silently: tell the user that `.specify/extensions.yml` could not be read (include the parser error) and that no hooks were checked, including any mandatory (`optional: false`) hooks registered there, then continue to the Completion Report.
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- For each executable hook, output the following based on its `optional` flag:
  - **Mandatory hook** (`optional: false`) — **You MUST emit `EXECUTE_COMMAND:` for each mandatory hook**:
    ```
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
    After emitting the block above you MUST actually invoke the hook and wait for it to finish before continuing. Run it the same way you would run the command yourself in this agent/session (the invocation may differ from the literal `{command}` id shown above, e.g. a skills-mode agent runs it as `/skill:speckit-...` or `$speckit-...`). Emitting the block alone does not run the hook.
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```

## Completion Report

Report the generated tasks.md path and:
- Total task count and reconciliation counts: created, reused/updated open, completed preserved, delta tasks, obsolete open tasks removed with confirmation or retained pending it
- Task count per phase/story, approximately 2–4 cohesive items per US; justified exceptions
- Computed Story Waves, Task Waves, `[P]` opportunities and critical path; one PR/MR per US and constitution-selected isolation
- Independent acceptance/checkpoint criteria and suggested first delivery wave / first Outcome-titled Release Lane
- Acceptance tests on/off and AC coverage (gaps as `US-xxx/AC-n "title"`)
- Validator outcome and refreshed indices; next step `__SPECKIT_COMMAND_ANALYZE__` before `__SPECKIT_COMMAND_IMPLEMENT__`

Context for task generation: {ARGS}

The tasks.md index plus the TASK files should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Generated Index and Progress Rules

The renderer organizes Setup → Walking Skeleton / Foundational → Story Waves (or map Release Lanes) → Polish from actual metadata. Within story waves, TASK waves respect blockers and disjoint `## Files`; `[P]` means two or more eligible items packed in the **same wave**, not "could be parallel someday". Do not add artificial dependencies just to manufacture a preferred list order; rank breaks otherwise eligible ties and must not invert real sibling blockers.

Generated task lines link from the spec directory to root backlog, for example:

```text
- [ ] TASK-012 [P] [US-007] Card payment acceptance tests → [../../backlog/tasks/TASK-012-card-payment-acceptance.md](../../backlog/tasks/TASK-012-card-payment-acceptance.md)
```

This example describes output, not permission to author it. `[P]` is included only when the scheduler computes it. The `[US-007]` label gets its readable title from the story heading. Completion becomes `[X]` **only** when the TASK's Actions and DoD checkboxes are all checked. `__SPECKIT_COMMAND_IMPLEMENT__` edits those central TASK checkboxes and regenerates tasks.md, never a second progress ledger. Each US opens one PR/MR; a story blocked by another starts only after the blocking PR is merged. Parallel stories use isolated worktrees by default, subject to constitution Delivery Conventions.

## Done When

- [ ] Central TASKs reconciled idempotently; completed files untouched, no orphan tasks, deletions confirmed
- [ ] tasks.md generated only by render-tasks; spec/index renders reflect computed waves and TASK-owned progress
- [ ] Validator passing (or remaining errors reported)
- [ ] Extension hooks dispatched or skipped according to the rules in Mandatory Post-Execution Hooks above
- [ ] Completion reported to user with task count, phase/story breakdown, AC coverage and MVP scope
