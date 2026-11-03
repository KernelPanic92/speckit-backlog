---
description: Turn a feature description into a backlog-driven specification - asks the working mode (user story map, epic + user stories, single user story) and writes the root PBI plus its children with the user-story-writer rules.
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

The text the user typed after `__SPECKIT_COMMAND_SPECIFY__` in the triggering message **is** the feature description. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command. An optional leading `--mode map|epic|story` selects the working mode.

**Paths used by this command** (preset `backlog`):

- `RULES` = `.specify/presets/backlog/knowledge/user-story-writer/rules.md` — the rules for writing PBIs. Its "Examples and references: when to read what" table tells you when to open `examples.md` and `references/*.md` (same folder).
- `SCHEMA` = `.specify/presets/backlog/schemas/pbi-frontmatter.schema.json` — the binding frontmatter schema.
- `VALIDATOR` = `uv run --no-project --quiet --with pyyaml --with jsonschema python .specify/presets/backlog/scripts/validate_backlog.py` — subcommands `next-id <TYPE>` and `check <feature-dir>`; JSON output, non-zero exit code on errors. If `uv` is not available, do the same checks by hand against `SCHEMA` and the rules, and say so in the Completion Report. Run it as a standalone command (not chained with `;`, `&&` or pipes) so that it can be allow-listed in the agent's permissions.
- `PRODUCT` = `.specify/memory/product.md` — Personas and Ubiquitous Language.
- `CONSTITUTION` = `/memory/constitution.md` — its Delivery Conventions set the default mode and the task manager.

Given that feature description, do this:

1. **Load the rules and the context**:
   - Read `RULES` in full before writing anything. The workflow below decides *which* phases of the rules run and *where* each PBI is written; the rules decide *how* every PBI is written. When this command and `RULES` seem to conflict on how to write a PBI, `RULES` wins.
   - **IF EXISTS**: Load `PRODUCT` and `CONSTITUTION`.
   - If `PRODUCT` does not exist, tell the user that personas and domain terms normally come from it and suggest `__SPECKIT_COMMAND_CONSTITUTION__`. You may continue only with personas the user gives you in this conversation; record "product.md missing" in the spec's Open Questions.
   - If the description is empty: ERROR "No feature description provided".
   - **Starting from a task-manager item**: if the description is only a reference to an item of a tool configured in `.specify/sync/` — a ClickUp task id, custom id or URL (`.specify/sync/clickup.md`), a Multica issue key or URL (`.specify/sync/multica.md`) — read that item (ClickUp connector; `multica issue get <key> --output json`) and use its title, description and comments as the feature description. Remember the item: after writing `SPEC_FILE`, link the root PBI to it with `VALIDATOR set-external <root id> <tool> --id <item id> --key <display key> --url <url>` (no `--hash-current`: the item still holds the original request, so the next `__SPECKIT_COMMAND_SYNC__ <tool> push` updates it and nests the children under it). If no mapping exists for that tool, say so and ask the user to paste the description or to run `__SPECKIT_COMMAND_SYNC__ <tool> setup` first.

2. **MACRO-ANALYSIS** (Phase 1 of `RULES`), printed in the conversation: restate the request briefly, count the distinct user activities it covers (e.g. search, choose, pay) and state the working criteria you have internalized.

3. **Choose the working mode.** Resolution order:
   1. `--mode` in the user input;
   2. otherwise the constitution's Delivery Conventions "Default specify mode", unless it is `ask` or missing;
   3. otherwise **ask the user and wait for the answer**. Recommend one option based on the macro-analysis: more than one user activity → `map`; one activity that splits into several stories → `epic`; one small behaviour that passes INVEST as it is → `story`. If the agent has a native question tool, use it; otherwise present:

   ```markdown
   ## Working mode

   **Recommended**: [option] — [one-line reason from the macro-analysis]

   | Option | Mode | spec.md (root PBI) | Children written in backlog/ |
   |--------|------|--------------------|------------------------------|
   | A | User Story Map (`map`) | MAP | one EPIC per Backbone Macro-Activity, their US, Walking Skeleton TASK/SPIKE |
   | B | Epic + User Stories (`epic`) | EPIC | its US (+ SPIKE when estimation is blocked) |
   | C | Single User Story (`story`) | US | SPIKE only if needed (its TASKs come from __SPECKIT_COMMAND_TASKS__) |

   **Your choice**: _[Wait for user response]_
   ```

   Mode rules:
   - `map` runs the phases of `RULES` in the order Phase 1 → Phase 3a → Phase 2 → Phase 3b. `epic` and `story` run Phase 1 → Phase 2 and skip Phase 3.
   - If the user picks `story` or `epic` but the request covers more than one user activity, say that `RULES` makes the map mandatory in that case and ask once whether to switch to `map`. Respect the user's final answer.
   - If the user picks `story` and the splitting in Phase 2 produces more than one story, **stop before writing** and propose switching to `epic` (a split requirement needs a container). If the user insists on `story`, keep only the first story in release order and list the others in the root US's Out of Scope as `- <capability> — candidate for a new __SPECKIT_COMMAND_SPECIFY__`.

4. **Context check** (Constraint 0 of `RULES`):
   - Take personas and domain terms from `PRODUCT`. Ask the user only for business context, personas or system constraints that are missing there and critical for the backlog. **Do not invent them.**
   - A persona or a domain term that is not in `PRODUCT` is proposed to the user; when approved, add it to `PRODUCT` (Personas / Ubiquitous Language) and mention the change in the Completion Report.
   - Ask at most 5 questions at a time, numbered, each in this format (or with the agent's native question tool):

     ```markdown
     ## Question [N]: [Topic]

     **Context**: [Quote the relevant part of the description]

     **What we need to know**: [Specific question]

     | Option | Answer | Implications |
     |--------|--------|--------------|
     | A      | [First suggested answer] | [What this means for the backlog] |
     | B      | [Second suggested answer] | [What this means for the backlog] |
     | Custom | Provide your own answer | [How to provide custom input] |

     **Your choice**: _[Wait for user response]_
     ```

   - Markdown tables must be well formed: spaces around cell content, header separators of at least 3 dashes.
   - Questions that are not blocking for writing the backlog go to the spec's Open Questions instead.

5. **Generate a concise short name** (2-4 words) for the feature:
   - Analyze the feature description and extract the most meaningful keywords
   - Use action-noun format when possible (e.g., "add-user-auth", "online-checkout")
   - Preserve technical terms and acronyms (OAuth2, API, JWT, etc.)
   - Examples: "I want customers to buy from the catalog" → "online-purchase"; "Create a dashboard for analytics" → "analytics-dashboard"

6. **Branch creation** (optional, via hook):

   If a `before_specify` hook ran successfully in the Pre-Execution Checks above, it will have created/switched to a git branch and output JSON containing `BRANCH_NAME` and `FEATURE_NUM`. Note these values for reference, but the branch name does **not** dictate the spec directory name.

   If the user explicitly provided `GIT_BRANCH_NAME`, pass it through to the hook so the branch script uses the exact value as the branch name (bypassing all prefix/suffix generation).

7. **Create the spec feature directory**:

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
   - Run `{SCRIPT}` from the repository root and parse `TEMPLATE_CONTENT` as the active `spec-template` (the **spec envelope**: the sections that exist only in `spec.md`). If it fails, stop and report the resolution error; do not continue with only one contributing template layer.
   - Run the same resolver again, replacing `spec-template` with each PBI template this mode needs, and parse each `TEMPLATE_CONTENT`:
     - `map`: `pbi-map-template`, `pbi-epic-template`, `pbi-story-template`, `pbi-task-template`, `pbi-spike-template`
     - `epic`: `pbi-epic-template`, `pbi-story-template`, `pbi-spike-template`
     - `story`: `pbi-story-template`, `pbi-spike-template`
     Always use the resolved content, never a template file read from disk: a preset or project override may compose it.
   - `mkdir -p SPECIFY_FEATURE_DIRECTORY` and the `backlog/` subfolders the mode needs (`epics/`, `stories/`, `spikes/`, `tasks/`).
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
   - You must only create one feature per `__SPECKIT_COMMAND_SPECIFY__` invocation. To refine an existing spec use `__SPECKIT_COMMAND_CLARIFY__`; to carve a spec out of another or combine specs use `__SPECKIT_COMMAND_SPLIT__` / `__SPECKIT_COMMAND_MERGE__`.
   - The spec directory name and the git branch name are independent — they may be the same but that is the user's choice
   - The spec directory and file are always created by this command, never by the hook

8. **PBI ids**: ids are local, project-wide unique and permanent. Get the first free id of a type with `VALIDATOR next-id <TYPE>` (e.g. `US`), then continue the sequence yourself for the PBIs you create in this run. Ids of a task manager never replace them: `__SPECKIT_COMMAND_SYNC__` stores them in each PBI's `external` block.

9. **Write the backlog** following the phases of `RULES` for the chosen mode. Every PBI is written with its resolved template and validated against `SCHEMA`:
   - **File layout**:
     - The **root PBI** goes to `SPEC_FILE`: its full template (frontmatter + body), followed by the spec envelope (`TEMPLATE_CONTENT` of `spec-template`). The root is the MAP (`map`), the EPIC (`epic`) or the US (`story`).
     - Every other PBI gets its own file: `backlog/epics/`, `backlog/stories/`, `backlog/spikes/`, `backlog/tasks/`, named `<ID>-<slug>.md` where `<slug>` is the title in lowercase ASCII kebab-case, at most 6 words (e.g. `backlog/stories/US-007-card-payment.md`).
   - **`map`**: Phase 3a writes the MAP root (Connextra with the global goal, Outcome as elevator pitch, Backbone, Walking Skeleton), one EPIC file per Macro-Activity (PARENT: the MAP) and one TASK/SPIKE file per Walking Skeleton item (PARENT: the Epic of its Macro-Activity). Start the Backbone from the Key User Journeys of `PRODUCT` when one matches. Phase 2 writes the US files (PARENT: their Epic), in lane order and left to right along the Backbone, never all the stories of one Epic in a row. Phase 3b completes the MAP: Release Lanes titled with Outcomes, Out of Scope, DoR Check.
   - **`epic`**: the EPIC root, then Phase 2 writes the US files with the EPIC as PARENT, in BLOCKED_BY / release order.
   - **`story`**: Phase 2 runs once and its story is the root US (it has no PARENT unless the user names an existing Epic).
   - **Spikes**: when uncertainty prevents estimating a story, write a SPIKE (PARENT: the story it serves) and declare it on the story with `BLOCKED_BY`. `__SPECKIT_COMMAND_PLAN__` answers spikes in research.md.
   - **The iterative discipline of Phase 2 applies**: print the Micro-Scope Reasoning block in the conversation before writing each story file; never write two stories in a row without it.
   - **Fill the spec envelope**: Spec Context (mode, root PBI, status `Draft`), Backlog Index (every child with a relative link, in the order the rules require), Success Criteria (`SC-###`, measurable and technology-agnostic), Key Entities with Ubiquitous Language terms (if data is involved), and — only when relevant — Non-Functional Requirements, External Dependencies, Security & Compliance Checklist, References. Open Questions lists what is still unknown, each naming the PBIs it affects. Remove the envelope's guidance comment block and every optional section that does not apply.
   - Never leave `{{...}}` or `[...]` placeholders, template comments that no longer guide anything, or empty optional keys.

10. **FINAL CHECK and SUMMARY** (end of Phase 2 of `RULES`), printed in the conversation: re-read every story against INVEST and the constraints and re-split where needed; re-read every reference in the PBIs, the relation `reason`s and the conversation blocks with the "NO mental mapping" test of `RULES` and rewrite coined abbreviations, section numbers without their title, bare URLs and files the reader cannot open (the feature's `spec.md` or `plan.md` is not a reference a task-manager reader can open); then list the final PBIs in release order (`type [id] title`) and — in `epic` mode with more than 5 stories — suggest the map in one line.

11. **Structural validation**: run `VALIDATOR check SPECIFY_FEATURE_DIRECTORY`. Fix every error it reports and run it again until it passes (max 3 iterations; then report the remaining errors).

12. **Specification Quality Validation**:

   a. **Create the Spec Quality Checklist** at `SPECIFY_FEATURE_DIRECTORY/checklists/requirements.md` with these items:

      ```markdown
      # Specification Quality Checklist: [FEATURE NAME]

      **Purpose**: Validate the backlog before proceeding to planning
      **Feature**: [Link to spec.md]
      **Mode**: [map | epic | story]

      ## Structure

      - [ ] The validator passes (schema, relations, ids, no placeholders)
      - [ ] Every PBI has an Out of Scope section (EPIC: Scope Boundaries) that lists only what a reader could assume is included, each item with where it goes
      - [ ] Every reference is readable without the generation context: other PBIs as `type [id] title`, documents as links whose text names the topic, no coined abbreviations, untitled section numbers, bare URLs or local files
      - [ ] The Backlog Index lists every child PBI in release order
      - [ ] Success Criteria are measurable and technology-agnostic

      ## User Stories

      - [ ] Every story uses the Connextra format with a persona defined in product.md
      - [ ] The "so that" clause states a real benefit and does not repeat the action
      - [ ] Every story passes INVEST (Independent, Negotiable, Valuable, Estimable, Small, Testable)
      - [ ] No conjunctions in the "I want" clause; no vague adjectives; no prescriptive UI; no application layers
      - [ ] Read and Write are separate stories; List and Detail are separate stories
      - [ ] Vertical slices only, no horizontal slicing by architectural layer; no phantom UI
      - [ ] Only real dependencies, declared with BLOCKED_BY

      ## Acceptance Criteria

      - [ ] Every scenario has an id (AC-n), Given/When/Then, a single When and a binary outcome
      - [ ] 2-5 scenarios per story (or the atomicity exception is justified)
      - [ ] Every scenario is pertinent to the "I want" clause (no scope creep from "so that")
      - [ ] Asynchronous operations describe the full cycle (trigger, loading indicator, outcome, error, retry)
      - [ ] Ubiquitous Language terms from product.md are used, one term per concept

      ## Map *(map mode only)*

      - [ ] Every Backbone Macro-Activity is an Epic; every Release Lane crosses all the Epics
      - [ ] Lanes are titled with Outcomes, not labels; no two items with the same priority
      - [ ] The Walking Skeleton is TASK/SPIKE items and differs from the MVP
      - [ ] No story sits in a lane earlier than a story that blocks it

      ## Notes

      - Items marked incomplete require spec updates before `__SPECKIT_COMMAND_CLARIFY__` or `__SPECKIT_COMMAND_PLAN__`
      ```

      Remove the Map section in `epic` and `story` mode.

   b. **Run Validation Check**: review the backlog against each checklist item; for each failing item document the specific issue (quote the PBI and section).

   c. **Handle Validation Results**:

      - **If all items pass**: mark the checklist complete and proceed to the Mandatory Post-Execution Hooks section.
      - **If items fail**: list the failing items and issues, update the PBIs (re-splitting stories when needed), re-run the validator and the checklist until all items pass (max 3 iterations). If still failing after 3 iterations, document the remaining issues in the checklist notes and warn the user.
      - **If Open Questions remain**: keep the 3 most critical (by scope > security/privacy > user experience > technical details), present them together in the question format of step 4 and wait for the answers. Update the affected PBIs, move each answered question to the envelope's Clarifications section (`### Session YYYY-MM-DD`, `- Q: … → A: …`) and re-run validation. The other questions stay in Open Questions for `__SPECKIT_COMMAND_CLARIFY__`.

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
- `SPECIFY_FEATURE_DIRECTORY` — the feature directory path, the mode and the root PBI (`type [id] title`)
- `SPEC_FILE` and the number of child PBIs written, per type
- Validator result and checklist results summary
- Changes made to `.specify/memory/product.md` (personas, terms), if any
- Open Questions left for `__SPECKIT_COMMAND_CLARIFY__`, if any
- Readiness for the next phase (`__SPECKIT_COMMAND_CLARIFY__` or `__SPECKIT_COMMAND_PLAN__`)

**NOTE:** Branch creation is handled by the `before_specify` hook (git extension). Spec directory and file creation are always handled by this core command.

## Quick Guidelines

- Focus on **WHAT** users need and **WHY**; the backlog must be understandable by a non-technical person.
- Avoid HOW to implement (no tech stack, APIs, code structure, application layers). Technical work appears only as Walking Skeleton TASK/SPIKE items.
- Every PBI's metadata lives in its frontmatter, never in the body; `spec.md`'s envelope sections are spec-level context, not PBI metadata.
- DO NOT create checklists embedded in the PBIs other than the ones their templates define (INVEST & DoR, map DoR). Other checklists are a separate command.

### Section Requirements

- **Mandatory sections**: every section of a PBI template that is not marked optional, plus the envelope's Spec Context, Backlog Index, Success Criteria and Open Questions
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

- [ ] Mode chosen (or confirmed) by the user, root PBI written to `SPEC_FILE` and every child PBI written to `backlog/`
- [ ] Validator passing (or remaining errors reported) and quality checklist written
- [ ] Extension hooks dispatched or skipped according to the rules in Mandatory Post-Execution Hooks above
- [ ] Completion reported to user with feature directory, mode, root PBI, PBI counts and checklist results
