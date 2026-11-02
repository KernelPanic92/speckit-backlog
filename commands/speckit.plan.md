---
description: Execute the implementation planning workflow - a single plan.md (design, data model, contracts, delivery slices) plus research.md that answers the unknowns and the backlog Spikes.
handoffs:
  - label: Create Tasks
    agent: speckit.tasks
    prompt: Break the plan into tasks
    send: true
  - label: Create Checklist
    agent: speckit.checklist
    prompt: Create a checklist for the following domain...
scripts:
  sh: scripts/bash/setup-plan.sh --json
  ps: scripts/powershell/setup-plan.ps1 -Json
  py: scripts/python/setup_plan.py --json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before planning)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_plan` key
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

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, FEATURE_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `/memory/constitution.md`. Load IMPL_PLAN template (already copied).
   - FEATURE_SPEC is the root PBI (MAP, EPIC or US: see its frontmatter `type` and the envelope's Spec Context) followed by the spec envelope (Backlog Index, Success Criteria, Key Entities, NFR, dependencies, compliance, Open Questions). Also read every child PBI under `FEATURE_DIR/backlog/`: the stories' Gherkin Acceptance Criteria (`US-xxx/AC-n`) are the requirements, the Spikes are open research questions, the map's Release Lanes and Walking Skeleton are the delivery order.
   - **IF EXISTS**: Read `.specify/memory/product.md` (Personas, Ubiquitous Language): entity, endpoint and field names in the plan use its terms.
   - **IF EXISTS** and the feature has a user interface: Read `.specify/memory/design.md` (DESIGN.md format: tokens in the front matter, rules in the prose). The plan's Technical Context names it as the design system, the Architecture and Project Structure say where its tokens live in code (CSS variables, Tailwind theme, component library theme), and UI components needed by the stories that design.md does not define are listed in Open Technical Questions.
   - If unchecked items remain in the envelope's Open Questions, warn that downstream rework risk increases and suggest `__SPECKIT_COMMAND_CLARIFY__`; continue only if the user confirms or the questions do not affect the design.

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill the header (spec mode, root PBI, links), Summary and Technical Context (start from the constitution's Technology Stack; mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified; justified violations go to Complexity Tracking following the constitution's Exceptions Process)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION and answer every Spike)
   - Phase 1: Fill the design sections of plan.md itself (Architecture, Project Structure, Data Model, API Design / Contracts, Integration, Security, Performance, Error Handling, Observability, Testing Strategy, Delivery Slices, Migration, Patterns)
   - Re-evaluate Constitution Check post-design

## Mandatory Post-Execution Hooks

**You MUST complete this section before reporting completion to the user.**

Check if `.specify/extensions.yml` exists in the project root.
- If it does not exist, or no hooks are registered under `hooks.after_plan`, skip to the Completion Report.
- If it exists, read it and look for entries under the `hooks.after_plan` key.
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

Command ends after Phase 1 design. Report branch, IMPL_PLAN path, research.md path, Spikes answered vs still open, Constitution Check result (and Complexity Tracking entries, if any), and readiness for `__SPECKIT_COMMAND_TASKS__`.

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

   For each SPIKE under `FEATURE_DIR/backlog/spikes/`:
     Task: "Answer {spike Outcome question} within {spike Timebox}"

3. **Consolidate findings** in `research.md`:
   - Resolve the `research-template` by running the template resolver (`.specify/scripts/bash/resolve-template.sh research-template --json`, or `.specify/scripts/powershell/resolve-template.ps1 research-template -Json` on PowerShell) and use its `TEMPLATE_CONTENT` as the structure. If it fails, stop and report the resolution error.
   - List every question in Research Questions with its source (Technical Context unknown, Spike, dependency, integration).
   - For each question write a Decisions block using format:
     - Decision: [what was chosen]
     - Rationale: [why chosen]
     - Alternatives considered: [what else evaluated]
   - Add Key Findings with sources, Version Information for the libraries the decisions depend on, and the Validity refresh trigger. Do not add dates, authors or changelogs: git history records them.
   - For each Spike that the research answers, tick its Exit Criteria in the SPIKE file and reference the Decisions block. A Spike that needs a prototype rather than desk research stays open: say so in research.md, and `__SPECKIT_COMMAND_TASKS__` will schedule it.

**Output**: research.md with all NEEDS CLARIFICATION resolved and every Spike answered or explicitly scheduled

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

Everything in this phase is written **inside plan.md** (single document): do not create data-model.md, contracts/ or quickstart.md.

1. **Extract entities from the spec's Key Entities and the stories' scenarios** → plan.md › Data Model:
   - Entity name (Ubiquitous Language term), fields, relationships
   - Validation rules from the Acceptance Criteria, quoted exactly (length, nullability, enums)
   - State transitions if applicable

2. **Define interface contracts** (if project has external interfaces) → plan.md › API Design / Contracts:
   - Identify what interfaces the project exposes to users or other systems
   - Document the contract format appropriate for the project type, with request/response and error examples
   - Examples: public APIs for libraries, command schemas for CLI tools, endpoints for web services, grammars for parsers, UI contracts for applications
   - Name the stories each contract serves
   - Skip if project is purely internal (build scripts, one-off tools, etc.)

3. **Validation scenarios** → plan.md › Testing Strategy:
   - The Gherkin scenarios of the stories are the validation scenarios (they replace quickstart.md). State whether acceptance tests are on or off (constitution › Delivery Conventions, default on) and where they live in the Project Structure.
   - Add unit, integration/contract and E2E strategy per the constitution's Quality Standards.

4. **Delivery Slices** → plan.md › Delivery Slices:
   - map: the Walking Skeleton first, then one row per Release Lane with its stories in Backbone order.
   - epic: one row per story in BLOCKED_BY / release order.
   - story: one row per Acceptance Criterion (or group).
   - For each row, the components of the Architecture Overview it touches.

**Output**: plan.md with all design sections filled

## Key rules

- Use absolute paths for filesystem operations; use project-relative paths for references in documentation
- ERROR on gate failures or unresolved clarifications
- Name entities, fields and endpoints with the Ubiquitous Language terms of product.md
- No document versioning: no dates, authors or changelogs in plan.md or research.md

## Done When

- [ ] Plan workflow executed: plan.md with all design sections, research.md with all unknowns resolved and Spikes answered or scheduled
- [ ] Extension hooks dispatched or skipped according to the rules in Mandatory Post-Execution Hooks above
- [ ] Completion reported to user with branch, plan path, and generated artifacts
