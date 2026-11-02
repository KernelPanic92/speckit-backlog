---
description: Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, the backlog PBIs, product.md, plan.md, research.md and tasks.md after task generation.
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

Identify inconsistencies, duplications, ambiguities, and underspecified items across the core artifacts (`spec.md` with the root PBI, the child PBIs under `backlog/`, `plan.md`, `research.md`, `tasks.md`) and the product context (`.specify/memory/product.md`) before implementation. This command MUST run only after `__SPECKIT_COMMAND_TASKS__` has successfully produced a complete `tasks.md`.

## Operating Constraints

**STRICTLY READ-ONLY**: Do **not** modify any files. Output a structured analysis report. Offer an optional remediation plan (user must explicitly approve before any follow-up editing commands would be invoked manually).

**Constitution Authority**: The project constitution (`/memory/constitution.md`) is **non-negotiable** within this analysis scope. Constitution conflicts are automatically CRITICAL and require adjustment of the spec, plan, or tasks—not dilution, reinterpretation, or silent ignoring of the principle. If a principle itself needs to change, that must occur in a separate, explicit constitution update outside `__SPECKIT_COMMAND_ANALYZE__`.

## Execution Steps

### 1. Initialize Analysis Context

Run `{SCRIPT}` once from repo root and parse JSON for FEATURE_DIR and AVAILABLE_DOCS. Derive absolute paths:

- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md
- TASKS = FEATURE_DIR/tasks.md

- BACKLOG = FEATURE_DIR/backlog/ (epics/, stories/, spikes/, tasks/)
- RESEARCH = FEATURE_DIR/research.md (if present)
- PRODUCT = `.specify/memory/product.md` (if present)

Abort with an error message if any required file is missing (instruct the user to run missing prerequisite command).

Then run the structural validator once (read-only):

`uv run --no-project --quiet --with pyyaml --with jsonschema python .specify/presets/backlog/scripts/validate_backlog.py check FEATURE_DIR`

Keep its JSON errors for detection pass G. Run it as a standalone command (not chained with `;`, `&&` or pipes) so that it can be allow-listed in the agent's permissions. If `uv` is not available, perform pass G by hand against `.specify/presets/backlog/schemas/pbi-frontmatter.schema.json` and say so in the report.
For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

### 2. Load Artifacts (Progressive Disclosure)

Load only the minimal necessary context from each artifact:

**From spec.md:**

- Root PBI: type (MAP / EPIC / US), Connextra, Outcome, Out of Scope; for a MAP: Backbone, Walking Skeleton, Release Lanes, DoR Check
- Spec Context (mode, status) and Backlog Index
- Success Criteria (measurable outcomes — e.g., performance, security, availability, user success, business impact)
- Key Entities, Non-Functional Requirements, Security & Compliance Checklist (if present)
- Open Questions and Clarifications

**From the PBIs under backlog/:**

- Frontmatter (id, title, type, relations)
- Stories: Connextra, Acceptance Criteria (`AC-n` ids, Given/When/Then), Out of Scope, INVEST & DoR Check
- Epics: Scope Boundaries; Spikes: question, Exit Criteria; TASKs: Covers, Files, relations

**From research.md (if present):**

- Research Questions and Decisions; Spikes answered or still open

**From product.md (if present):**

- Personas and Ubiquitous Language terms

**From design.md (if present and the feature has a UI):**

- Token groups and component names (front matter), Do's and Don'ts, accessibility target

**From plan.md:**

- Architecture/stack choices
- Data Model references
- Phases
- Technical constraints

**From tasks.md:**

- Task IDs, story labels and links to TASK files
- Titles
- Phase grouping (Walking Skeleton / Release Lanes / stories / ACs)
- Parallel markers [P]
- Traceability Matrix
- Referenced file paths (from the TASK files' Files sections)

**From constitution:**

- Load `/memory/constitution.md` for principle validation

### 3. Build Semantic Models

Create internal representations (do not include raw artifacts in output):

- **Requirements inventory**: In this project the requirements are the Gherkin scenarios of the stories: record one stable key per scenario, `US-xxx/AC-n`. Add one key per Success Criterion (SC-###) and per Non-Functional Requirement that requires buildable work (e.g., load-testing infrastructure, security audit tooling); exclude post-launch outcome metrics and business KPIs (e.g., "Reduce support tickets by 50%").
- **User story/action inventory**: Discrete user actions (one per story) with their acceptance criteria, PARENT, BLOCKED_BY and lane/order
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

- Any requirement or plan element conflicting with a MUST principle
- Missing mandated sections or quality gates from constitution

#### E. Coverage Gaps

- Requirements with zero associated tasks
- Stories with zero tasks
- When acceptance tests are on (constitution › Delivery Conventions, default on): scenarios `US-xxx/AC-n` not covered by any acceptance-test task
- Tasks with no mapped requirement/story (except Setup, Walking Skeleton/Foundational and Polish tasks)
- Success Criteria requiring buildable work (performance, security, availability) not reflected in tasks

#### F. Inconsistency

- Terminology drift (same concept named differently across files)
- Data entities referenced in plan but absent in spec (or vice versa)
- Task ordering contradictions (e.g., integration tasks before foundational setup tasks without dependency note; a task listed before a task it is BLOCKED_BY)
- Phase order contradicting the spec: phases not following the Release Lanes (map) or the stories' BLOCKED_BY / release order (epic)
- Conflicting requirements (e.g., one requires Next.js while other specifies Vue)

#### G. Backlog Structure

- Every error reported by the validator (schema, more than one PARENT or a forbidden hierarchy, unknown ids, inverse relations, relation order, duplicate ids, leftover placeholders, a story in a lane earlier than its blocker, tasks.md lines without a TASK file or TASK files missing from tasks.md)
- Child PBIs missing from the Backlog Index, or listed there but missing on disk
- PBIs without an Out of Scope section (EPIC: Scope Boundaries); scenarios without `AC-n` ids
- Stories that break the rules of `.specify/presets/backlog/knowledge/user-story-writer/rules.md` in an evident way: conjunctions in the "I want" clause, more than 5 scenarios without justification, Read and Write in the same story, phantom UI
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
| A1 | Duplication | HIGH | spec.md:L120-134 | Two similar requirements ... | Merge phrasing; keep clearer version |

(Add one row per finding; generate stable IDs prefixed by category initial.)

**Coverage Summary Table:**

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| US-001/AC-1 | Yes | TASK-010, TASK-011 | |

**Validator Result:** (pass, or the error count by kind)

**Constitution Alignment Issues:** (if any)

**Unmapped Tasks:** (if any)

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
- Provide explicit command suggestions: e.g., "Run __SPECKIT_COMMAND_CLARIFY__ to resolve the open questions", "Run __SPECKIT_COMMAND_PLAN__ to adjust architecture", "Run __SPECKIT_COMMAND_TASKS__ to add coverage for US-004/AC-2", "Run __SPECKIT_COMMAND_SPLIT__ to carve the Checkout epic out of this map"

### 8. Offer Remediation

Ask the user: "Would you like me to suggest concrete remediation edits for the top N issues?" (Do NOT apply them automatically.)

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

## Context

{ARGS}
