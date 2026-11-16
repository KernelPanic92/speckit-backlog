---
description: Perform read-only cross-artifact analysis of modular spec artifacts, backlog PBIs, ADRs, schedules, and task coverage.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-spec --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireSpec -RequireTasks -IncludeTasks
  py: scripts/python/check_prerequisites.py --json --require-spec --require-tasks --include-tasks
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before analysis)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_analyze` key
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

    Wait for the result of the hook command before proceeding to the Goal.
    ```
    After emitting the block above you MUST actually invoke the hook and wait for it to finish before continuing. Run it the same way you would run the command yourself in this agent/session (the invocation may differ from the literal `{command}` id shown above, e.g. a skills-mode agent runs it as `/skill:speckit-...` or `$speckit-...`). Emitting the block alone does not run the hook.
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## Goal

Identify inconsistencies, duplication, ambiguity and underspecification across the 4-block `spec.md` (`**Scope**:` + rendered `## Backlog`, optional Key Entities, Success Criteria), permanent PBIs in repository-root `backlog/`, `plan.md`, optional `data-model.md`, `contracts/`, `research.md`, `quickstart.md`, generated `tasks.md`, Accepted ADRs in `docs/adr/`, and product/governance context before implementation. This command MUST run only after `__SPECKIT_COMMAND_TASKS__` has produced `tasks.md`; validation may still expose defects. Never treat spec.md as a PBI file.

## Operating Constraints

**STRICTLY READ-ONLY**: Do **not** modify any files. Output a structured analysis report. Offer an optional remediation plan (user must explicitly approve before any follow-up editing commands would be invoked manually).

**Constitution Authority**: The project constitution (`/memory/constitution.md`) is **non-negotiable** within this analysis scope. Constitution conflicts are automatically CRITICAL and require adjustment of the spec, plan, or tasks—not dilution, reinterpretation, or silent ignoring of the principle. If a principle itself needs to change, that must occur in a separate, explicit constitution update outside `__SPECKIT_COMMAND_ANALYZE__`.

## Execution Steps

### 1. Initialize Analysis Context

Run `{SCRIPT}` once from repo root and parse JSON for FEATURE_DIR and AVAILABLE_DOCS. Derive absolute paths:

- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md
- TASKS = FEATURE_DIR/tasks.md

- BACKLOG = repository-root `backlog/` (`maps/`, `epics/`, `features/`, `stories/`, `spikes/`, `tasks/`, `bugs/`), never FEATURE_DIR/backlog/
- RESEARCH = FEATURE_DIR/research.md (if present)
- DATA_MODEL = FEATURE_DIR/data-model.md (if present)
- CONTRACTS = FEATURE_DIR/contracts/ (if present; inspect per boundary/story file)
- QUICKSTART = FEATURE_DIR/quickstart.md (if present)
- ADRs = Accepted decisions under `docs/adr/` (plus recognized legacy archives)
- PRODUCT = `.specify/memory/product.md` (if present)
- REFERENCES = the "Readable references" section of `.specify/presets/backlog/knowledge/pbi-writing/rules.md`: what a readable reference is, for detection pass G and for this report
- DELIVERY_RULES = `.specify/presets/backlog/knowledge/delivery/rules.md`: rank/blockers/files, computed wave scheduling, one PR/MR per US and default worktree isolation
- SCHEMA = `.specify/presets/backlog/schemas/pbi-frontmatter.schema.json`: `MAP`, `EPIC`, `FEATURE`, `US`, `SPIKE`, `BUG`, `TASK` (BUG creation is outside these commands)
- BACKLOG_TOOL = `uv run --no-project --quiet --with pyyaml --with jsonschema python .specify/presets/backlog/scripts/backlog.py`

Abort with an error message if any required file is missing (instruct the user to run missing prerequisite command).

Run `BACKLOG_TOOL check --spec FEATURE_DIR` once (read-only), then `BACKLOG_TOOL schedule --spec FEATURE_DIR` (read-only). Keep JSON validator errors and `story_waves`, `task_waves`, `critical_path`, `parallel` booleans for detection pass G. Every BACKLOG_TOOL operation expands to the full invocation above as a **standalone command**, never chained with `;`, `&&`, or `|`, so permissions can allow-list it. If tooling cannot run, report the analysis as incomplete; do not fabricate a passing check or computed schedule. **Never run render-index, render-spec or render-tasks here**: stale output is a finding, not permission to write.
For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

### 2. Load Artifacts (Progressive Disclosure)

Load only the minimal necessary context from each artifact:

**From spec.md:**

- Header: `**Scope**:` selectors (only MAP / EPIC / FEATURE / US), Status and Input
- Rendered `## Backlog` block between `<!-- BEGIN BACKLOG -->` / `<!-- END BACKLOG -->`, with central PBI links and computed Story Waves / `[P]`
- Success Criteria (measurable outcomes — e.g., performance, security, availability, user success, business impact)
- Key Entities (if applicable); Clarifications session log if present (only spec.md may hold Q&A)

**From the PBIs under root backlog/:**

- Run `BACKLOG_TOOL locate <ID> --descendants` for every Scope ID. Read scoped PBIs, their FEATURE/EPIC/MAP ancestors, blocking SPIKEs and related TASKs, even when references cross the current spec. The locator returns file, rank, referenced_by, specs and descendants.
- Frontmatter (id, title, type, rank, relations); hierarchy and canonical relation order
- Stories: Connextra, Acceptance Criteria (`AC-n` ids, Given/When/Then), Out of Scope, INVEST & DoR Check
- Features: bounded capability, Outcome, cross-story Constraints, Out of Scope; Epics: Scope Boundaries; MAPs: Backbone, Walking Skeleton, Outcome-titled Release Lanes, DoR Check
- Spikes: question, timebox and Exit Criteria; TASKs: Covers, exact Files, Actions / DoD checkboxes (the sole completion source), parent and blockers

**From research.md (if present):**

- Research Questions, Fact-finding/Technical Findings, Architectural Trade-offs and Verdicts; Spikes answered or still open. Flag durable cross-feature decisions buried here without an ADR.

**From product.md (if present):**

- Personas and Ubiquitous Language terms

**From design.md (if present and the feature has a UI):**

- Token groups and component names (front matter), Do's and Don'ts, accessibility target

**From plan.md and modular design artifacts:**

- `plan.md`: feature-specific architecture/stack deltas, Constitution Check, Project Structure, delivery slices, and technical constraints; flag copied constitution boilerplate/filler.
- `data-model.md`: entities, fields, validation constraints, relations, state transitions and migration details when present.
- `contracts/`: boundary contracts per story slice when present.
- `quickstart.md`: runnable acceptance-suite and smoke verification commands when present.
- Accepted ADRs in `docs/adr/`: governing cross-feature decisions and supersession status; flag contradictions with artifacts or constitution.

**From tasks.md:**

- Task IDs, story labels and links to TASK files
- Titles
- Phase grouping (Setup, Walking Skeleton / Foundational, Story Waves or map Release Lanes, Polish)
- Parallel markers [P]
- Traceability Matrix
- Referenced file paths (from the TASK files' Files sections)
- Compare against `backlog/index.md` (functional hierarchy, story waves, tasks: done/total counters without exploding implementation tasks)

**From constitution:**

- Load `/memory/constitution.md` for principle validation

### 3. Build Semantic Models

Create internal representations (do not include raw artifacts in output):

- **Requirements inventory**: one stable key per Gherkin scenario (`US-xxx/AC-n`), plus Success Criteria (`SC-###`) and Feature/ancestor Constraints requiring buildable work (load testing, security audit tooling). Do not demand implementation TASKs for post-launch outcome metrics/business KPIs such as "Reduce support tickets by 50%". Human-facing rows include titles beside every traceability ID.
- **User story/action inventory**: one discrete behavior per US, with ACs, FEATURE/EPIC/MAP ancestry, rank, real BLOCKED_BY, lane and computed Story Wave
- **Schedule model**: tool-computed Story Waves, Task Waves, critical path and file conflicts; aggregate descendant TASK Files to each US, do not invent a separate author-maintained schedule
- **Task coverage mapping**: Map each task to stories and scenarios through its PARENT relation, its `Covers:` line and its story label in tasks.md; use keyword inference only as a fallback
- **Product model**: personas and Ubiquitous Language terms from product.md
- **Constitution rule set**: Extract principle names and MUST/SHOULD normative statements

### 4. Detection Passes (Token-Efficient Analysis)

Focus on high-signal findings. Limit to 50 findings total; aggregate remainder in overflow summary.

#### A. Duplication Detection

- Identify near-duplicate requirements
- Mark lower-quality phrasing for consolidation

#### B. Ambiguity Detection

- Flag vague adjectives (fast, scalable, secure, intuitive, robust) lacking measurable criteria
- Flag unresolved placeholders (TODO, TKTK, ???, `<placeholder>`, etc.)

#### C. Underspecification

- Requirements with verbs but missing object or measurable outcome
- User stories missing acceptance criteria alignment
- Tasks referencing files or components not defined in spec/plan

#### D. Constitution Alignment

- Any requirement or plan element conflicting with a MUST principle or Accepted ADR
- Missing mandated sections or quality gates from constitution

#### E. Coverage Gaps

- Requirements with zero associated tasks
- Stories with zero tasks
- When acceptance tests are on (constitution › Delivery Conventions, default on): scenarios `US-xxx/AC-n` not covered by any acceptance-test task
- Tasks with no mapped requirement/story (except Setup, Walking Skeleton/Foundational and Polish tasks)
- Success Criteria requiring buildable work (performance, security, availability) not reflected in tasks

#### F. Inconsistency

- Terminology drift (same concept named differently across files)
- Data entities referenced in plan/data-model but absent in spec (or vice versa)
- Contract, story, data-model and `quickstart.md` verification inconsistencies
- Contradictions with Accepted ADRs, unrecorded cross-feature decisions hidden in `research.md`, or constitution boilerplate filler in `plan.md`
- Task ordering contradictions (e.g., integration tasks before foundational setup tasks without dependency note; a task listed before a task it is BLOCKED_BY)
- Phase order contradicting computed Story/Task Waves, `rank` / `BLOCKED_BY`, or map Release Lane / Backbone order
- Conflicting requirements (e.g., one requires Next.js while other specifies Vue)

#### G. Backlog & Schedule Structure

- Every validator error: schema, forbidden hierarchy/multiple PARENTs, unknown/duplicate IDs, cycles, inverse or out-of-order relations, required sections, placeholders, map lanes, relative links and AC coverage
- **rank vs BLOCKED_BY inversions**, including sibling priority that places a dependent ahead of its blocker; artificial dependencies that undermine INVEST
- **Stale rendered blocks** in `spec.md`, generated `tasks.md`, or root `backlog/index.md`; missing/extra scoped PBIs, manual generated-line edits, incorrect task counters or `[X]` inconsistent with TASK Actions/DoD
- **`ac-uncovered`**: when Acceptance tests from Gherkin is on (default), every `US-xxx/AC-n "title"` needs an acceptance-test TASK Covers entry before implementation; titles alone do not count
- Scheduling claims inconsistent with `schedule`: `[P]` outside a computed multi-item wave, overlapping exact TASK `## Files`, blockers not satisfied, or an attempt to start a story before its blocking story's PR is merged
- Missing task parent (including Setup/Foundational/Polish), invalid container ownership, Polish without real blockers, or prototype closing TASKs absent / ordered after the story work they must unblock
- PBIs without an Out of Scope section (EPIC: Scope Boundaries); Out of Scope items without where they go; scenarios without `AC-n` ids
- **Readable References violations** in PBIs, spec, plan, research, tasks and checklists: bare PBI/scenario IDs outside allowed labels, `§` notation, coined labels, untitled section numbers, bare URLs/paths, non-topical links, wrong relative traversal/anchors, spec-local files as the only explanation of a central PBI, or numbered constitution principles
- **INVEST / splitting violations**: conjunctions in I want, >5 scenarios without value-atomicity justification, Read/Write or List/Detail combined, horizontal slices, phantom UI, unbounded Features or more than one Feature Outcome
- Spikes neither answered in research.md nor scheduled as tasks

#### H. Product Consistency

- Connextra personas not defined in product.md's Personas
- Domain terms used in PBIs, plan or tasks that are synonyms of a Ubiquitous Language term, or missing from it
- Key Entities and plan Data Model names that differ from the Ubiquitous Language terms
- When `.specify/memory/design.md` exists and the feature has a UI: UI tasks or plan sections that use literal colors, fonts or sizes instead of design tokens, components the stories need that design.md does not define, and an accessibility target different from the constitution's

### 5. Severity Assignment

Use this heuristic to prioritize findings:

- **CRITICAL**: Violates constitution MUST, missing core spec artifact, validator schema error, or requirement with zero coverage that blocks baseline functionality (e.g. a story of the first Release Lane without tasks)
- **HIGH**: Duplicate or conflicting requirement, ambiguous security/performance attribute, untestable acceptance criterion
- **MEDIUM**: Terminology drift, missing non-functional task coverage, underspecified edge case
- **LOW**: Style/wording improvements, minor redundancy not affecting execution order

### 6. Produce Compact Analysis Report

Output a Markdown report (no file writes) with the following structure:

## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| A1 | Duplication | HIGH | Acceptance Criteria of US [US-003] Product page (`backlog/stories/US-003-product-page.md`, lines 40-52) | Two similar requirements ... | Merge phrasing; keep clearer version |

(Add one row per finding; generate stable IDs prefixed by category initial. Locations name the document, the PBI as `type [id] title` and the section by its heading, with the file and lines in brackets; when a finding is cited again, in Next Actions or in remediation, repeat its summary next to its ID.)

**Coverage Summary Table:**

| Requirement Key | Requirement | Has Task? | Tasks | Notes |
|-----------------|-------------|-----------|-------|-------|
| US-001/AC-1 | Catalog list: "Products listed" | Yes | TASK-010 Catalog list acceptance tests, TASK-011 Catalog list query | |

(The Requirement column carries the story title and the scenario title, or the Success Criterion's short name; every task carries its title.)

**Validator Result:** (pass, or the error count by kind)

**Constitution Alignment Issues:** (if any)

**Unmapped Tasks:** (if any, as `TASK [id] title`)

**Metrics:**

- Total PBIs by type and Total Requirements (scenarios + buildable SC/NFR)
- Total Tasks
- Coverage % (requirements with >=1 task)
- Acceptance-test coverage % (scenarios with a test task, when tests are on)
- Ambiguity Count
- Duplication Count
- Critical Issues Count

### 7. Provide Next Actions

At end of report, output a concise Next Actions block:

- If CRITICAL issues exist: Recommend resolving before `__SPECKIT_COMMAND_IMPLEMENT__`
- If only LOW/MEDIUM: User may proceed, but provide improvement suggestions
- Provide explicit suggestions: `__SPECKIT_COMMAND_CLARIFY__` for ambiguity, `__SPECKIT_COMMAND_PLAN__` for architecture, `__SPECKIT_COMMAND_TASKS__` for AC coverage/task reconciliation, `__SPECKIT_COMMAND_BACKLOG__` for PBI splitting/reordering, or `__SPECKIT_COMMAND_SPECIFY__` to select a smaller Feature/Release Lane. Name the affected PBIs/scenarios with titles.

### 8. Offer Remediation

Ask the user: "Would you like me to suggest concrete remediation edits for the top N issues?" (Do NOT apply them automatically.)

## Mandatory Post-Execution Hooks

### 9. Check for extension hooks

After reporting, check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.after_analyze` key
- If the YAML cannot be parsed or is invalid, do not skip silently: tell the user that `.specify/extensions.yml` could not be read (include the parser error) and that no hooks were checked, including any mandatory (`optional: false`) hooks registered there, then continue normally
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- For each executable hook, output the following based on its `optional` flag:
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Mandatory hook** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
    After emitting the block above you MUST actually invoke the hook and wait for it to finish before continuing. Run it the same way you would run the command yourself in this agent/session (the invocation may differ from the literal `{command}` id shown above, e.g. a skills-mode agent runs it as `/skill:speckit-...` or `$speckit-...`). Emitting the block alone does not run the hook.
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## Operating Principles

### Context Efficiency

- **Minimal high-signal tokens**: Focus on actionable findings, not exhaustive documentation
- **Progressive disclosure**: Load artifacts incrementally; don't dump all content into analysis
- **Token-efficient output**: Limit findings table to 50 rows; summarize overflow
- **Deterministic results**: Rerunning without changes should produce consistent IDs and counts

### Analysis Guidelines

- **NEVER modify files** (this is read-only analysis)
- **NEVER hallucinate missing sections** (if absent, report them accurately)
- **Prioritize constitution violations** (these are always CRITICAL)
- **Use examples over exhaustive rules** (cite specific instances, not generic patterns)
- **Report zero issues gracefully** (emit success report with coverage statistics)
- **Readable report**: before printing, run the self-check of REFERENCES on the report itself: every PBI, scenario, task and section it names must be understandable without opening the files

## Context

{ARGS}
