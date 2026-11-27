---
description: Plan scoped central backlog PBIs with modular design artifacts, research, and durable ADRs.
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

**Rules and tool**:

- `PBI_RULES` = `.specify/presets/backlog/knowledge/pbi-writing/rules.md` (including Readable References).
- `DELIVERY_RULES` = `.specify/presets/backlog/knowledge/delivery/rules.md` (rank, blockers, computed Story/Task Waves and `[P]`, one PR/MR per US and default worktree isolation).
- `BACKLOG_TOOL` = `uv run --no-project --quiet --with pyyaml --with jsonschema python .specify/presets/backlog/scripts/backlog.py`.

Every `BACKLOG_TOOL` operation below expands to that full invocation from the repository root as a **standalone command**, never chained with `;`, `&&`, or `|`, so permissions can allow-list it. Parse JSON output; stop and report unavailable tooling rather than hand-authoring a substitute schedule.

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, FEATURE_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `/memory/constitution.md`. Load IMPL_PLAN template (already copied).
   - FEATURE_SPEC is the **4-block spec**: Header with `**Scope**:`, rendered Backlog, optional Key Entities, Success Criteria. Run `BACKLOG_TOOL locate <ID> --descendants` for each scope ID; read scoped PBIs, FEATURE/EPIC/MAP ancestors and blocking SPIKEs from **root** `backlog/{maps,epics,features,stories,spikes,tasks}/`. Follow dependencies outside the immediate descendants where needed. The seven-type model also accepts BUG references (creation belongs to the bug extension). Gherkin `US-xxx/AC-n "title"` scenarios are requirements; Feature Constraints / Epic Scope Boundaries and map lanes contextualize them.
   - **IF EXISTS**: Read `.specify/memory/product.md` (Personas, Ubiquitous Language): entity, endpoint and field names in the plan use its terms.
   - **IF EXISTS** and the feature has a user interface: Read `.specify/memory/design.md` (DESIGN.md format). Name it in Technical Context, identify code locations for tokens/components in Architecture and Project Structure, and resolve missing UI component decisions during research rather than inventing tokens.
   - Load the project's `.specify/memory/constitution.md` for principles, stack, Quality Standards and Delivery Conventions. If a high-impact functional ambiguity prevents design, suggest `__SPECKIT_COMMAND_CLARIFY__` and stop for the decision; do not create an unanswered-question section in the spec.
   - Load `ARCH_RULES` = `.specify/presets/backlog/knowledge/architecture/rules.md` and scan ADR archives in this order: `docs/architecture/adr/`, `docs/adr/` (the former default), `docs/decisions/`, `doc/adr/`, `adr/`. Accepted ADRs govern Technical Context and Constitution Check alongside `constitution.md`; use `docs/architecture/adr/` as the default archive when creating an ADR.
   - Read `PBI_RULES` and `DELIVERY_RULES`. Every reference in plan/research/Spike edits must be readable: titled PBIs/scenarios, topic links with correct anchors, named constitution principles (never numbers or coined labels).
   - Run `BACKLOG_TOOL schedule --spec FEATURE_DIR`. Keep JSON `story_waves`, `task_waves`, `critical_path` and computed `parallel` booleans; use these Story Waves in Delivery Slices, never invent `[P]`. Where TASK file declarations do not exist yet, describe that the task command will refine file-conflict scheduling.

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill the header (selected Scope PBIs and links), Summary and Technical Context (start from the constitution's Technology Stack; mark technical unknowns as "NEEDS CLARIFICATION" until Phase 0 resolves them)
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified; justified violations go to Complexity Tracking following the constitution's Exceptions Process)
   - Phase 0: Generate `research.md`, classify each unknown/Spike as Fact-finding or Trade-off, resolve desk-research Spikes and identify prototype Spikes that remain open for task scheduling.
   - Crystallize durable, cross-feature decisions as atomic ADRs when they are not already governed by the constitution or an existing ADR.
   - Phase 1: Fill the slim, delta-only `plan.md`; generate `data-model.md` only for persistent/domain entities, `contracts/*` only for external interfaces, and a concise runnable `quickstart.md`.
   - Re-evaluate Constitution Check post-design, each gate named after its principle or rule
   - Run the Readable References self-check on plan.md, research.md and edited Spike Exit Criteria; fix references. After Spike updates run `BACKLOG_TOOL render-spec FEATURE_DIR`, `BACKLOG_TOOL render-index`, and `BACKLOG_TOOL check --spec FEATURE_DIR` as separate standalone commands; refresh other impacted specs / existing task indices when necessary. Do not report ready with unresolved structural errors.

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

Command ends after Phase 1 design. Report branch, selected Scope, modular artifact paths, ADRs created or reused, Story Waves and critical path, Spikes answered vs prototype work still open (each as `SPIKE [id] title`), validator and Constitution Check results with named rules (plus Complexity Tracking entries), and readiness for `__SPECKIT_COMMAND_TASKS__`.

## Phases

### Phase 0: Outline & Research

1. **Classify unknowns and Spikes** from Technical Context, dependencies, integrations and scoped/blocking Spikes:
   - **Fact-finding** is the default when the stack and existing constitution/ADRs settle the design. Perform a concise empirical check and report evidence; do not create option matrices or manufacture an architectural fork.
   - **Trade-off** is only for a genuine architectural fork or Spike. Apply `ARCH_RULES`: state Latent Gaps & Assumptions and what changes if each is false; compare 3–4 distinct options including status quo; include the Decision Matrix with `Xh @ Y% risk` Effort and a Poison pill; run the 10x Stress Test; and give one Verdict. Include confidence with effort estimates.
   - Record which mode applies and why for each question. Resolve empirical unknowns; keep prototype-dependent Spikes open and identify the required closing TASK.

2. **Generate and dispatch focused research work**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

   For each scoped or blocking SPIKE in root `backlog/spikes/`:
     Task: "Answer {spike Outcome question} within {spike Timebox}, if desk research suffices; otherwise identify required prototype work"

3. **Consolidate findings** in `research.md`:
   - Resolve `research-template` via `.specify/scripts/bash/resolve-template.sh research-template --json`, `.specify/scripts/powershell/resolve-template.ps1 research-template -Json`, or `python .specify/scripts/python/resolve_template.py research-template --json`. Use resolved `TEMPLATE_CONTENT`; stop on failure.
   - List every question in Research Questions as a full question, without numbering, with its source as a readable reference (the Technical Context unknown as a link to that section of plan.md, the Spike as a link whose text is `SPIKE [id] title`, the dependency or integration by name) and a link to its decision block.
   - In Fact-finding mode, use concise `## Technical Findings` with evidence/sources and a direct result; avoid fake matrices.
   - In Trade-off mode, use `## Architectural Trade-offs` and the full `ARCH_RULES` structure. Preserve a single Verdict and explain confidence/risk.
   - Link every question to its topic decision/findings. Include version information where library versions materially affect findings and a validity refresh trigger. Do not add dates, authors or changelogs: git history records them.
   - For each desk-research Spike answered with evidence, tick **only satisfied** Exit Criteria in `backlog/spikes/SPIKE-xxx-<slug>.md` and link to the decision from that root-backlog file, e.g. `[the payment provider decision](../../specs/<dir>/research.md#payment-provider)`. Compute the real relative path and anchor. Do not tick work that was not done. A Spike needing a prototype stays open; document that boundary in research.md so `__SPECKIT_COMMAND_TASKS__` creates its closing TASK before the story work it blocks.

**Output**: research.md with all NEEDS CLARIFICATION resolved and every Spike answered or explicitly scheduled

### ADR Crystallization

When Phase 0 or Phase 1 settles a durable, cross-feature architectural decision not already covered by `constitution.md` or an existing ADR, resolve `adr-template` using the shared resolver (`.specify/scripts/bash/resolve-template.sh adr-template --json`, PowerShell equivalent, or Python equivalent) and use its `TEMPLATE_CONTENT`. Allocate the next `NNNN` ID across the ADR archive; create `docs/architecture/adr/NNNN-kebab-slug.md` by default. Write one atomic decision per file using heading `# ADR-NNNN: Adopt X for Y`, required metadata (`Status`, `Supersedes`, `Origin`, `Tags`), and at least two concrete bullets under `### Negative` in `## Consequences`. Set `Accepted` only when the user confirms the decision; otherwise use `Proposed`. If replacing an ADR, follow strict supersession: the new ADR names what it supersedes, and edit only the old ADR's `Status` row to link to the replacement. Never emit ADRs for routine local choices or duplicate `docs/tdd/` files.

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Write `plan.md`** using resolved `plan-template` as the slim (~100-line) backbone: Summary, Technical Context, Constitution Check, Project Structure, Delivery Slices, and optional Complexity Tracking. Record only feature-specific deltas; do not repeat constitution rules, stack boilerplate, or constitution policy. Include a Resilience, Migration & Rollout Deltas subsection only when this feature changes them.

2. **Write `data-model.md` only when persistent or domain entities are introduced or modified**:
   - Use Ubiquitous Language entity names; document fields, exact validation rules traceable to `AC-n`, relationships, indexes, state transitions, and migration reversibility as applicable.
   - Keep entity sections and anchors stable for task-level references. If no relevant data/entities change, do not create this file.

3. **Write `contracts/*` only when an external interface changes or is introduced**:
   - Use the boundary's suitable format (for example OpenAPI, `.proto`, `.graphql`, JSON Schema, CLI or UI contract).
   - Create one file per boundary/story slice so workers can load only the contract they need. Link each file to its applicable stories and acceptance criteria. Omit the directory if no external interface exists.

4. **Write `quickstart.md`** as a concise, runnable ~20–40-line verification runbook: prerequisites/environment, the exact command for the feature's Gherkin acceptance suite, and one or two smoke commands linked to stories/contracts. Do not duplicate Gherkin scenarios.

5. **Delivery Slices** → `plan.md` › Delivery Slices:
   - Walking Skeleton / foundational prerequisites first, then rows aligned with the **Story Waves** returned by `BACKLOG_TOOL schedule --spec FEATURE_DIR`; retain Outcome-titled Release Lanes and Backbone order when a map is scoped. A single-story spec still uses its computed wave, not a separate AC scheduling model.
   - For every row, link PBIs as `type [id](../../backlog/<type-dir>/<ID>-<slug>.md) title`, identify touched components, blockers, critical-path implications and only scheduler-computed `[P]` opportunities. Explain that dependent stories wait for their blockers' PRs to merge and each US gets its own PR/MR (worktree by default, per constitution).

**Output**: modular plan artifacts appropriate to the feature, with no duplicated constitution boilerplate or Gherkin scenarios

## Key rules

- Use absolute paths for filesystem operations; in documentation, a reference to another file is a relative Markdown link whose text names the topic and whose address ends with the heading anchor (the "Readable references" section), never a bare path
- ERROR on gate failures or unresolved clarifications
- Name entities, fields and endpoints with the Ubiquitous Language terms of product.md
- Accepted ADRs and `constitution.md` govern design; do not contradict them or hide a new cross-feature decision in research alone.
- No document versioning: no dates, authors or changelogs in plan or research artifacts

## Done When

- [ ] `plan.md` is a slim delta-only backbone; optional `data-model.md`, `contracts/*` and runnable `quickstart.md` exist only when applicable
- [ ] `research.md` uses Fact-finding or genuine Trade-off mode correctly; durable cross-feature decisions are captured in atomic ADRs
- [ ] research.md resolves technical unknowns and desk-research Spikes; prototype Spikes remain explicitly open for tasks; Spike decision links use correct root-relative traversal
- [ ] Rendered indices refreshed when affected; backlog check and Constitution Check pass; Readable References checked
- [ ] Extension hooks dispatched or skipped according to the rules in Mandatory Post-Execution Hooks above
- [ ] Completion reported to user with branch, plan path, and generated artifacts
