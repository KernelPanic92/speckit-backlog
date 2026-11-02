---
description: Generate the TASK PBIs (one file each under backlog/tasks/) and the dependency-ordered tasks.md execution index, phased by the spec mode (release lanes, stories or acceptance criteria).
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

Paths used by this command (preset `backlog`):

- `RULES` = `.specify/presets/backlog/knowledge/user-story-writer/rules.md` — the TASK rules (no Connextra, no INVEST; Outcome, Actions, DoD; relations declared only from the child/blocked side).
- `VALIDATOR` = `uv run --no-project --quiet --with pyyaml --with jsonschema python .specify/presets/backlog/scripts/validate_backlog.py` (`next-id <TYPE>`, `check <feature-dir>`). If `uv` is not available, check the frontmatter by hand against `.specify/presets/backlog/schemas/pbi-frontmatter.schema.json`. Run it as a standalone command (not chained with `;`, `&&` or pipes) so that it can be allow-listed in the agent's permissions.

1. **Setup**: Run `{SCRIPT}` from repo root and parse FEATURE_DIR, TASKS_TEMPLATE_CONTENT, TASKS_TEMPLATE, and AVAILABLE_DOCS list. `FEATURE_DIR` and `TASKS_TEMPLATE` must be absolute paths when provided. `AVAILABLE_DOCS` is a list of document names/relative paths available under `FEATURE_DIR` (for example `research.md`). For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").
   - Resolve the TASK PBI template by running the template resolver with the name `pbi-task-template` (`.specify/scripts/bash/resolve-template.sh pbi-task-template --json`, or `.specify/scripts/powershell/resolve-template.ps1 pbi-task-template -Json` on PowerShell) and parse its `TEMPLATE_CONTENT`. If it fails, stop and report the resolution error.

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md (tech stack, project structure, data model, contracts, testing strategy, **Delivery Slices**), spec.md (root PBI + envelope: mode, Backlog Index), every PBI under `backlog/` (stories with their Acceptance Criteria `US-xxx/AC-n`, epics, spikes, existing TASK PBIs such as the Walking Skeleton)
   - **Optional**: research.md (decisions, Spikes still open)
   - **IF EXISTS**: Load `/memory/constitution.md` for project principles and governance constraints; its Delivery Conventions say whether **acceptance tests from Gherkin** are on (default) or off, and its Quality Standards feed the Task Completion Criteria
   - **IF EXISTS** and the feature has a user interface: Read `.specify/memory/design.md`; UI tasks name, in their Outcome or Actions, the design tokens and components they must use (e.g. `{colors.primary}`, `button-primary`) instead of literal colors, sizes or fonts
   - Read `RULES` (Task and Spike parts, Frontmatter section)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

3. **Execute task generation workflow**:
   - Load plan.md and extract tech stack, libraries, project structure, data model, contracts and Delivery Slices
   - Load spec.md and determine the mode from the root PBI `type` (MAP → map, EPIC → epic, US → story) and the delivery order:
     - map: the MAP's Walking Skeleton, then its Release Lanes in order, stories left to right along the Backbone inside each lane
     - epic: the stories in BLOCKED_BY / release order (Backlog Index)
     - story: the root US's Acceptance Criteria in order
   - Map data-model entities and contracts to the stories that need them
   - If research.md exists: extract decisions for setup tasks; Spikes it could not answer become tasks scheduled before the stories they block
   - Generate TASK PBIs organized by delivery slice (see Task Generation Rules below)
   - Generate the dependency graph from the BLOCKED_BY relations
   - Create parallel execution examples per story
   - Validate task completeness (each story has all needed tasks and is independently testable; each AC has a test task when acceptance tests are on)

4. **Write the TASK PBIs**: one file per task in `FEATURE_DIR/backlog/tasks/<ID>-<slug>.md` (slug: title in lowercase ASCII kebab-case, at most 6 words), using the resolved `pbi-task-template`:
   - **Ids**: local and permanent: get the first free id with `VALIDATOR next-id TASK` and continue the sequence in execution order.
   - **Existing TASK PBIs** (Walking Skeleton items written by `__SPECKIT_COMMAND_SPECIFY__`, or tasks from a previous run) are reused, not duplicated: keep their ids and update them only if the plan changes what they must do. If tasks.md already exists, ask before discarding tasks that are already checked.
   - **Frontmatter**: `PARENT` = the story the task serves (Walking Skeleton items: the Epic of their Macro-Activity; Setup/Foundational/Polish tasks: no PARENT); `BLOCKED_BY` = the tasks that must be completed first. Relations only from this side, in the canonical order of `RULES`.
   - **Body**: Outcome (specific enough that an LLM can complete the task without additional context), `Covers:` for acceptance-test tasks, Files (exact paths consistent with the plan's Project Structure), Actions to complete, Out of Scope, DoD starting from the Task Completion Criteria of tasks.md.
   - For each field with constraints in the plan's Data Model (max length, nullable/required, enum values, validation rules), quote the constraint verbatim in the task's Outcome or Actions so it is not left to implementation-time discretion.

5. **Generate tasks.md**: Use TASKS_TEMPLATE_CONTENT (from the JSON output above) as the structure. For compatibility with older setup scripts that omit TASKS_TEMPLATE_CONTENT, read TASKS_TEMPLATE instead. Fill with:
   - Correct feature name, spec mode, root PBI and links
   - Summary (total tasks, parallelizable, phases, suggested MVP) and Task Completion Criteria from the constitution's Quality Standards
   - Phases by mode (see Phase Structure below), each with goal, independent test criteria and checkpoint
   - One strict checkbox line per TASK PBI (see Task Generation Rules below)
   - Dependency Graph, Phase Dependencies, Parallel Example per story, Implementation Strategy (MVP first, incremental delivery)
   - Risk Assessment and the Traceability Matrix (every story and every AC → test tasks and implementation tasks)

6. **Validate**: run `VALIDATOR check FEATURE_DIR`. It verifies the TASK frontmatter, the relations, and that every checkbox line of tasks.md has a TASK file and vice versa. Fix and re-run until it passes (max 3 iterations; then report the remaining errors).

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

Output path to generated tasks.md and summary:
- Total task count and TASK PBI files written (new vs reused)
- Task count per phase and per story
- Parallel opportunities identified
- Independent test criteria for each phase
- Acceptance tests on/off and AC coverage (ACs without a test task, if any)
- Suggested MVP scope (map: the first Release Lane; epic: the first story; story: the whole story)
- Format validation: confirm ALL task lines follow the checklist format and the validator passes

Context for task generation: {ARGS}

The tasks.md index plus the TASK files should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by delivery slice (Release Lane, story or Acceptance Criterion, depending on the mode) to enable independent implementation and testing.

**Tests follow the constitution**: when acceptance tests from Gherkin are on (the default), every scenario `US-xxx/AC-n` MUST be covered by an acceptance-test task (`Covers:` lists the scenarios) placed before the story's implementation tasks; one task may cover several scenarios of the same story. When off, generate test tasks only if explicitly requested in the spec or by the user.

### Checklist Format (REQUIRED)

Every line of tasks.md that represents a task MUST strictly follow this format:

```text
- [ ] [TaskID] [P?] [Story?] Title → [backlog/tasks/<ID>-<slug>.md](backlog/tasks/<ID>-<slug>.md)
```

**Format Components**:

1. **Checkbox**: ALWAYS start with `- [ ]` (markdown checkbox)
2. **Task ID**: the TASK PBI id (TASK-014), in execution order
3. **[P] marker**: Include ONLY if task is parallelizable (different files, no BLOCKED_BY on incomplete tasks)
4. **[Story] label**: the PARENT story, e.g. [US-007]
   - Setup phase: NO story label
   - Walking Skeleton / Foundational phase: NO story label
   - Story and lane phases: MUST have story label
   - Polish phase: NO story label
5. **Title**: the TASK PBI title (the Files and details live in the TASK file)
6. **Link**: relative link to the TASK file

**Examples**:

- ✅ CORRECT: `- [ ] TASK-001 Create project structure per implementation plan → [backlog/tasks/TASK-001-project-structure.md](backlog/tasks/TASK-001-project-structure.md)`
- ✅ CORRECT: `- [ ] TASK-012 [P] [US-007] Acceptance test for US-007/AC-1 and US-007/AC-2 → [backlog/tasks/TASK-012-card-payment-acceptance.md](backlog/tasks/TASK-012-card-payment-acceptance.md)`
- ❌ WRONG: `- [ ] Create User model` (missing ID, story label and link)
- ❌ WRONG: `TASK-001 [US-007] Create model → …` (missing checkbox)
- ❌ WRONG: `- [ ] TASK-014 [US-007] Create model` (missing link to the TASK file)

### Task Organization

1. **From Stories (backlog/stories/)** - PRIMARY ORGANIZATION:
   - Each story gets its own block inside its phase, in delivery order
   - Map all related components to their story: models, services, interfaces/UI needed for that story, and its acceptance tests (when on)
   - Mark story dependencies with BLOCKED_BY (most stories should be independent; respect the stories' own BLOCKED_BY relations)

2. **From Contracts (plan.md › API Design / Contracts)**:
   - Map each interface contract → to the story it serves
   - If tests are on: each interface contract → contract test task [P] before implementation in that story's block

3. **From Data Model (plan.md › Data Model)**:
   - Map each entity to the story(ies) that need it
   - If entity serves multiple stories: Put in earliest story or Setup phase
   - Relationships → service layer tasks in appropriate story block

4. **From Setup/Infrastructure**:
   - Shared infrastructure → Setup phase (Phase 1)
   - Walking Skeleton items (map) / blocking prerequisites (epic) → Phase 2
   - Story-specific setup → within that story's block

5. **From Spikes**: a Spike that research.md could not answer → a TASK (PARENT: the story the Spike serves; RELATED: the SPIKE it closes, with reason "closes the Spike") placed before that story, and the story's tasks are BLOCKED_BY it. When the task is done, `__SPECKIT_COMMAND_IMPLEMENT__` ticks the Spike's Exit Criteria.

### Phase Structure

- **map**: Phase 1 Setup → Phase 2 Walking Skeleton (the MAP's TASK/SPIKE items) → Phase 3+ one phase per Release Lane, titled with the lane's Outcome (the first lane is the 🎯 MVP), stories left to right along the Backbone → Final Phase Polish
- **epic**: Phase 1 Setup → Phase 2 Foundational (blocking prerequisites) → Phase 3+ one phase per story in BLOCKED_BY / release order (the first story is the 🎯 MVP) → Final Phase Polish
- **story**: Phase 1 Setup → Phase 2 Spikes (only if some are still open) → Phase 3+ one phase per Acceptance Criterion or coherent group of ACs → Final Phase Polish
- Within each story: Acceptance tests (when on) → Models → Services → Endpoints → Integration
- Each phase should be a complete, independently testable increment, closed by a **Checkpoint**: all the Gherkin scenarios of the phase pass (map: the lane's Metrics can be measured)

## Done When

- [ ] TASK PBI files written (or reused) under backlog/tasks/ and tasks.md generated with all phases, task lines and links
- [ ] Validator passing (or remaining errors reported)
- [ ] Extension hooks dispatched or skipped according to the rules in Mandatory Post-Execution Hooks above
- [ ] Completion reported to user with task count, phase/story breakdown, AC coverage and MVP scope
