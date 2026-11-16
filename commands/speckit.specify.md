---
description: Turn free-text feature descriptions or existing MAP, EPIC, FEATURE or US PBIs into a focused 4-block specification linked to the central root backlog/.
handoffs:
  - label: Build Technical Plan
    agent: speckit.plan
    prompt: Create a plan for the spec. I am building with...
  - label: Clarify Spec Requirements
    agent: speckit.clarify
    prompt: Clarify specification requirements
    send: true
scripts:
  sh: scripts/bash/resolve-template.sh spec-template --json
  ps: scripts/powershell/resolve-template.ps1 spec-template -Json
  py: scripts/python/resolve_template.py spec-template --json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before specification)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_specify` key
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

The text the user typed after `__SPECKIT_COMMAND_SPECIFY__` **is** `$ARGUMENTS`. Use it even if `{ARGS}` appears literally below. Do not ask the user to repeat non-empty input. This command creates one clean spec referencing permanent PBIs; it never embeds a root PBI in `spec.md`.

**Paths and tools** (repository root unless otherwise stated):

- `PBI_RULES` = `.specify/presets/backlog/knowledge/pbi-writing/rules.md` — writing rules, conditional references and Readable References.
- `DELIVERY_RULES` = `.specify/presets/backlog/knowledge/delivery/rules.md` — central placement, rank, computed waves / `[P]`, one PR/MR per US and worktree isolation by default.
- `SCHEMA` = `.specify/presets/backlog/schemas/pbi-frontmatter.schema.json` — seven types: `MAP`, `EPIC`, `FEATURE`, `US`, `SPIKE`, `BUG`, `TASK` (BUG creation belongs to the bug extension).
- `PRODUCT` = `.specify/memory/product.md` — Personas and Ubiquitous Language.
- `CONSTITUTION` = `/memory/constitution.md` (the project's `.specify/memory/constitution.md`) — principles and Delivery Conventions.
- `BACKLOG_TOOL` = `uv run --no-project --quiet --with pyyaml --with jsonschema python .specify/presets/backlog/scripts/backlog.py`.

Every `BACKLOG_TOOL` operation below means this full invocation as a **standalone command**, never chained with `;`, `&&`, or `|`, so permissions can allow-list it. Parse JSON results; stop and report unavailable tooling rather than silently bypassing deterministic generation or checks.

1. **Parse input**: accept a free-text feature description **or one or more existing PBI IDs** (`MAP-xxx`, `EPIC-xxx`, `FEATURE-xxx`, `US-xxx`). If empty, ERROR "No feature description or PBI scope provided". Reject `TASK-xxx` and `SPIKE-xxx` as spec scope: **TASK and SPIKE have no functional requirements**. SPIKEs are resolved in `__SPECKIT_COMMAND_PLAN__` or via the story they block; TASKs are managed by `__SPECKIT_COMMAND_TASKS__`. Ask for a functional PBI or description instead.

2. **Load rules and context**: read `PBI_RULES`, `DELIVERY_RULES`, `SCHEMA`, `PRODUCT`, and `CONSTITUTION`. Writing rules govern how PBIs are written; this workflow governs placement. If product context is missing, warn and suggest `__SPECKIT_COMMAND_CONSTITUTION__`; proceed only with user-confirmed personas and domain context.

3. **Constraint 0 and clarification discipline**:
   - Check Personas, business context, system constraints and Ubiquitous Language. Never invent actors or critical business facts. Propose new personas/terms for approval and add approved entries to `PRODUCT`.
   - Ask at most **3 blocking questions total**, prioritized scope > security/privacy > UX. Present each with context, a full interrogative, and a structured options table; wait for answers and apply them immediately before generation:

     | Option | Answer | Implications |
     | --- | --- | --- |
     | A | Recommended answer | Effect on scope or acceptance |
     | B | Alternative answer | Different effect |
     | Custom | User-provided answer | Describe the choice |

   - Use reasonable defaults for non-blocking details and record them in the affected PBI's `## Assumptions`, not in a spec-level question list. **Zero `[NEEDS CLARIFICATION]` markers or unanswered question lists remain at completion.** If a genuinely blocking decision is still missing, stop instead of claiming a finished spec.

4. **Prepare PBIs in central root `backlog/`**:
   - For each referenced PBI, run `BACKLOG_TOOL locate <ID> --descendants`. Read target, ancestors, descendants, `referenced_by` and impacted `specs`. **Reuse existing US slices as-is** when complete and compliant with INVEST and `PBI_RULES`; do not rewrite or renumber valid PBIs simply to attach a spec.
   - For free text, an unsliced MAP/EPIC/FEATURE, or an oversized US, execute the same splitting/mapping phases as `__SPECKIT_COMMAND_BACKLOG__` within this workflow. Resolve every required `pbi-*-template` via the template resolver (same resolver as `{SCRIPT}`, replacing `spec-template` with `pbi-story-template`, `pbi-feature-template`, `pbi-epic-template`, `pbi-map-template`, `pbi-spike-template`, or `pbi-task-template`). Parse `TEMPLATE_CONTENT`; honor composition and overrides, and stop on failure.
   - Allocate each permanent ID with `BACKLOG_TOOL next-id <TYPE>` (or reserve a batch with `--count N`, using each returned ID once); save files before further allocation of that type. Assign sibling `rank` `10, 20, 30...` without contradicting real `BLOCKED_BY` relations.
   - **Phase 1 Macro-Analysis**: print Request, Container decision and Working criteria. **Container rule**: if free text without a map splits into multiple User Stories, always create a `FEATURE` as their `PARENT`. A single story needs no new container.
   - **Phase 3a** when more than one user activity or a map is requested: read the map rules reference, write MAP, one EPIC per Backbone activity, Walking Skeleton TASK/SPIKE items parented to the Epics, and exactly one FEATURE per populated Epic × Release Lane intersection, **printing Feature Check before each Feature**. The first lane is the MVP but its title is its Outcome, not a generic release label.
   - **Phase 2 Iterative Drafting**: print a **Feature Check before each Feature** and **Micro-Scope Reasoning before each US**, as concise decision summaries, never private deliberation. Apply Connextra, INVEST, separate Read/Write and List/Detail, vertical value slices, ~2–5 `AC-n` Gherkin scenarios, one `When`, binary outcomes, complete asynchronous cycles and required Out of Scope. If estimation is blocked, create a timeboxed SPIKE and have the blocked PBI declare `BLOCKED_BY` it. Never create story implementation TASKs here; only map Walking Skeleton TASKs belong to this phase.
   - **Phase 3b** if mapped: complete lanes with Features and stories in lane/Backbone order, Metrics and justified DoR. **Final Check & Summary**: re-split violations and summarize readable PBIs in release order, never Epic by Epic.
   - Write **every PBI**, including MAP/EPIC/FEATURE containers and a standalone US, to its own `backlog/{maps,epics,features,stories,spikes,tasks}/<ID>-<slug>.md` file. Slug: lowercase ASCII kebab-case, max 6 words. Metadata is schema-valid frontmatter; omit empty optional keys, comments and placeholders. Relations are child/blocked-side only, ordered `PARENT`, `BLOCKED_BY`, `RELATED`, then type (`MAP`, `EPIC`, `FEATURE`, `US`, `SPIKE`, `BUG`, `TASK`), then ID. Existing paths never change on re-parenting.

5. **Scope size guardrail before writing `spec.md`**: if the resulting candidate scope spans **more than one Release Lane or more than 7 User Stories**, warn that all generated PBIs are already saved in `backlog/`. Recommend scoping this spec to the **first Feature or first Release Lane (MVP)** to keep planning/review/implementation focused, with subsequent slices in later `__SPECKIT_COMMAND_SPECIFY__` runs. Ask whether to narrow `**Scope**:` to that slice (recommended) or keep the entire scope; wait for the answer. When choosing only a lane, list the Feature/US IDs that select it, not the whole MAP/EPIC. Preserve all out-of-spec PBIs in `backlog/`.

6. **Generate a concise short name** (2-4 words) for the feature:
   - Analyze the feature description and extract the most meaningful keywords
   - Use action-noun format when possible (e.g., "add-user-auth", "online-checkout")
   - Preserve technical terms and acronyms (OAuth2, API, JWT, etc.)
   - Examples: "I want customers to buy from the catalog" → "online-purchase"; "Create a dashboard for analytics" → "analytics-dashboard"

7. **Branch creation** (optional, via hook):

   If a `before_specify` hook ran successfully in the Pre-Execution Checks above, it will have created/switched to a git branch and output JSON containing `BRANCH_NAME` and `FEATURE_NUM`. Note these values for reference, but the branch name does **not** dictate the spec directory name.

   If the user explicitly provided `GIT_BRANCH_NAME`, pass it through to the hook so the branch script uses the exact value as the branch name (bypassing all prefix/suffix generation).

8. **Create the spec feature directory**:

   Specs live under the default `specs/` directory unless the user explicitly provides `SPECIFY_FEATURE_DIRECTORY`.

   **Resolution order for `SPECIFY_FEATURE_DIRECTORY`**:
   1. If the user explicitly provided `SPECIFY_FEATURE_DIRECTORY` (e.g., via environment variable, argument, or configuration), use it as-is
   2. Otherwise, auto-generate it under `specs/`:
      - Check `.specify/init-options.json` for `feature_numbering` (preferred) or `branch_numbering` (deprecated, migration only — will be removed in a future release)
      - If `"timestamp"`: prefix is `YYYYMMDD-HHMMSS` (current timestamp)
      - If `"sequential"` or absent: prefix is `NNN` (next available 3-digit number after scanning existing directories in `specs/`)
      - Construct the directory name: `<prefix>-<short-name>` (e.g., `003-online-purchase` or `20260319-143022-online-purchase`)
      - Set `SPECIFY_FEATURE_DIRECTORY` to `specs/<directory-name>`
      - If `branch_numbering` was used (and `feature_numbering` was absent), emit a one-line warning: "⚠️ `branch_numbering` in init-options.json is deprecated. Rename to `feature_numbering`."

   **Resolve the templates and create the directory**:
   - Run `{SCRIPT}` from the repository root and parse `TEMPLATE_CONTENT` as the active 4-block `spec-template`. If it fails, stop and report the resolution error; do not continue with only one contributing template layer.
   - `mkdir -p SPECIFY_FEATURE_DIRECTORY`. The PBI folders already live under repository-root `backlog/`, never inside the spec directory.
   - Set `SPEC_FILE` to `SPECIFY_FEATURE_DIRECTORY/spec.md`
   - Persist the resolved path to `.specify/feature.json`:
     ```json
     {
       "feature_directory": "<resolved feature dir>"
     }
     ```
     Write the actual resolved directory path value (for example, `specs/003-online-purchase`), not the literal string `SPECIFY_FEATURE_DIRECTORY`.
     This allows downstream commands (`__SPECKIT_COMMAND_PLAN__`, `__SPECKIT_COMMAND_TASKS__`, etc.) to locate the feature directory without relying on git branch name conventions.

   **IMPORTANT**:
   - You must only create one feature per `__SPECKIT_COMMAND_SPECIFY__` invocation. To refine an existing spec use `__SPECKIT_COMMAND_CLARIFY__`; to manage the reusable PBIs use `__SPECKIT_COMMAND_BACKLOG__`.
   - The spec directory name and the git branch name are independent — they may be the same but that is the user's choice
   - The spec directory and file are always created by this command, never by the hook

9. **Write `SPEC_FILE` from the resolved template**, with only these four blocks (no PBI frontmatter or embedded PBI body):
   - **Header**: feature name, branch (if any), Status `Draft`, Input and `**Scope**:` containing comma-separated MAP/EPIC/FEATURE/US IDs selected above. The Scope IDs are machine-readable selectors, not a replacement for readable titled links in prose.
   - **`## Backlog`** with `<!-- BEGIN BACKLOG -->` / `<!-- END BACKLOG -->` markers. The tool renders linked PBIs, hierarchy, computed waves and `[P]`; never hand-edit the block.
   - **`## Key Entities`**, only when data is involved: use exact Ubiquitous Language terms, no implementation recipes.
   - **`## Success Criteria` → `### Measurable Outcomes`**: `SC-###` plus short name, measurable technology-agnostic outcomes derived from the scoped Outcome. No FR list, duplicate Gherkin, assumptions or unanswered-question section; those functional details live in the PBIs.

10. **Render and validate**, each as a standalone invocation:
    - `BACKLOG_TOOL render-spec SPECIFY_FEATURE_DIRECTORY`
    - `BACKLOG_TOOL render-index`
    - If shared PBIs changed, refresh every other affected spec from `locate` `specs`, and existing affected task indices with `render-tasks <spec-dir>`.
    - `BACKLOG_TOOL check --spec SPECIFY_FEATURE_DIRECTORY`
    Fix structural errors and re-render as necessary, up to **3 iterations**, then report any remaining errors without claiming readiness. Apply the Readable References self-check to all written files and reports: readable type/ID/title, titled scenarios and topic links to exact headings.

11. **Specification Quality Validation**:

   a. **Create the Spec Quality Checklist** at `SPECIFY_FEATURE_DIRECTORY/checklists/requirements.md` with these items:

      ```markdown
      # Specification Quality Checklist: [FEATURE NAME]

      **Purpose**: Validate the backlog before proceeding to planning
      **Feature**: [[Feature name] specification](../spec.md)

      ## Structure

      - [ ] backlog.py check --spec passes (schema, hierarchy, relations, ids, rendered blocks, applicable coverage)
      - [ ] spec.md has the 4-block structure, valid Scope and rendered Backlog linked to central backlog/
      - [ ] Zero [NEEDS CLARIFICATION] markers or unanswered question lists remain
      - [ ] Required Out of Scope (EPIC: Scope Boundaries) names exclusions and their destinations
      - [ ] Readable References everywhere: type/id/title, titled scenarios, topic links and correct anchors; no bare references
      - [ ] Success Criteria are measurable and technology-agnostic

      ## User Stories & Features

      - [ ] Every story uses the Connextra format with a persona defined in product.md
      - [ ] The "so that" clause states a real benefit and does not repeat the action
      - [ ] Every story passes INVEST (Independent, Negotiable, Valuable, Estimable, Small, Testable)
      - [ ] No conjunctions in the "I want" clause; no vague adjectives; no prescriptive UI; no application layers
      - [ ] Read and Write are separate stories; List and Detail are separate stories
      - [ ] Vertical slices only, no horizontal slicing by architectural layer; no phantom UI
      - [ ] Features have one Outcome, cross-story Constraints and bounded reviewable scope
      - [ ] Only real dependencies, declared with BLOCKED_BY, consistent with sibling rank

      ## Acceptance Criteria

      - [ ] Every scenario has an id (AC-n), Given/When/Then, a single When and a binary outcome
      - [ ] 2-5 scenarios per story (or the atomicity exception is justified)
      - [ ] Every scenario is pertinent to the "I want" clause (no scope creep from "so that")
      - [ ] Asynchronous operations describe the full cycle (trigger, loading indicator, outcome, error, retry)
      - [ ] Ubiquitous Language terms from product.md are used, one term per concept

      ## Map *(only when a MAP is involved)*

      - [ ] Every Backbone Macro-Activity is an Epic; every Release Lane crosses all the Epics
      - [ ] Lanes are titled with Outcomes, not labels; no two items with the same priority
      - [ ] The Walking Skeleton is TASK/SPIKE items and differs from the MVP
      - [ ] Every populated Epic × Release Lane intersection has exactly one Feature parenting its stories
      - [ ] No story sits in a lane earlier than a story that blocks it

      ## Notes

      - Items marked incomplete require spec updates before `__SPECKIT_COMMAND_CLARIFY__` or `__SPECKIT_COMMAND_PLAN__`
      ```

      Remove the Map section when no MAP is involved.

   b. **Run Validation Check**: review the backlog against each checklist item; for each failing item document the specific issue, naming the PBI as `type [id] title` and the section by its heading, and quoting the text at fault.

   c. **Handle Validation Results**:

      - **If all items pass**: mark the checklist complete and proceed to the Mandatory Post-Execution Hooks section.
      - **If items fail**: list the failing items and issues, update the PBIs (re-splitting stories when needed), re-run the validator and the checklist until all items pass (max 3 iterations). If still failing after 3 iterations, document the remaining issues in the checklist notes and warn the user.
      - **If a blocking ambiguity remains**: do not leave it as a marker or unanswered list. Use the remaining allowance of the 3 blocking questions from step 3; wait and apply the answer to the affected PBI. If that allowance is exhausted, stop and report that the specification is not ready. Q&A session logs are owned by `__SPECKIT_COMMAND_CLARIFY__`, not embedded in PBIs.

   d. **Update Checklist**: after each validation iteration, update the checklist file with the current pass/fail status.

## Mandatory Post-Execution Hooks

**You MUST complete this section before reporting completion to the user.**

Check if `.specify/extensions.yml` exists in the project root.
- If it does not exist, or no hooks are registered under `hooks.after_specify`, skip to the Completion Report.
- If it exists, read it and look for entries under the `hooks.after_specify` key.
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

Report completion to the user with:
- `SPECIFY_FEATURE_DIRECTORY` — the feature directory path and selected Scope PBIs (`type [id] title`)
- `SPEC_FILE` and the PBIs created vs reused in root `backlog/`, per type
- Validator result and checklist results summary
- Changes made to `.specify/memory/product.md` (personas, terms), if any
- Scope-size warning and the user's narrow/keep decision, if applicable; any validation blockers (never claim ready if unresolved)
- Readiness for the next phase (`__SPECKIT_COMMAND_CLARIFY__` or `__SPECKIT_COMMAND_PLAN__`)

**NOTE:** Branch creation is handled by the `before_specify` hook (git extension). Spec directory and file creation are always handled by this core command.

## Quick Guidelines

- Focus on **WHAT** users need and **WHY**; the backlog must be understandable by a non-technical person.
- Avoid HOW to implement (no tech stack, APIs, code structure, application layers). Technical work appears only as Walking Skeleton TASK/SPIKE items.
- Every PBI's metadata lives in its own root-backlog file's frontmatter; `spec.md` contains spec-level context and rendered references only.
- DO NOT create checklists embedded in the PBIs other than the ones their templates define (INVEST & DoR, map DoR). Other checklists are a separate command.

### Section Requirements

- **Mandatory sections**: each PBI template's required sections; the spec's Header with Scope, rendered Backlog and Success Criteria
- **Optional sections**: include only when relevant
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### Success Criteria Guidelines

Success criteria must be:

1. **Measurable**: Include specific metrics (time, percentage, count, rate)
2. **Technology-agnostic**: No mention of frameworks, languages, databases, or tools
3. **User-focused**: Describe outcomes from user/business perspective, not system internals
4. **Verifiable**: Can be tested/validated without knowing implementation details

**Good examples**: "Customers complete checkout in under 3 minutes"; "95% of searches return results in under 1 second"; "Task completion rate improves by 40%".

**Bad examples**: "API response time is under 200ms" (too technical); "Redis cache hit rate above 80%" (technology-specific).

## Done When

- [ ] Functional PBIs prepared/reused in root `backlog/`; selected Scope confirmed when large; clean 4-block `SPEC_FILE` written
- [ ] No unanswered question lists or [NEEDS CLARIFICATION] markers remain
- [ ] Validator passing (or remaining errors reported) and quality checklist written
- [ ] Extension hooks dispatched or skipped according to the rules in Mandatory Post-Execution Hooks above
- [ ] Completion reported with feature directory, Scope, created/reused PBI counts and checklist results
