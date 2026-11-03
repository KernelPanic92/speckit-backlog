---
description: Create or update the project constitution (how we build), the product context (what we build, for whom, and its ubiquitous language) and the design system (how the product looks, in the DESIGN.md format).
handoffs:
  - label: Build Specification
    agent: speckit.specify
    prompt: Implement the feature specification based on the updated constitution. I want to build...
scripts:
  sh: scripts/bash/resolve-template.sh constitution-template --json
  ps: scripts/powershell/resolve-template.ps1 constitution-template -Json
  py: scripts/python/resolve_template.py constitution-template --json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Scope Guard

This command's own work is limited to three governance documents:

- `.specify/memory/constitution.md` — HOW we build (principles, stack, rules, boundaries, quality, security, delivery conventions, governance).
- `.specify/memory/product.md` — WHAT we build and for WHOM (vision, problem, personas, goals, scope, journeys, constraints, stakeholders, ubiquitous language).
- `.specify/memory/design.md` — how the product LOOKS: design tokens and visual rules in the [DESIGN.md format](https://github.com/google-labs-code/design.md) (spec version `alpha`). Only for products with a user interface.

Dependent templates and commands read both documents at runtime and are not modified here.

- Classify every part of the user input as constitution content, product content, design content, or a separate,
  non-governance intent. If the input concerns only some of the documents, update only those.
- If the input includes feature implementation, code generation, refactoring, building, or
  deployment requests, you **MUST NOT** execute them. Extract them as deferred intents instead.
- You **MUST NOT** create, modify, or delete application source files, feature routes,
  components, tests, deployment files, specs, or other artifacts unrelated to this workflow.
- If it is unclear whether an instruction is constitution, product, design or none of them, ask for clarification before
  making changes.
- After completing the update, include a `Next Actions` section for each deferred
  intent. List the original intent and suggest the appropriate follow-up Spec Kit command, such
  as `__SPECKIT_COMMAND_SPECIFY__`, without invoking it.
- If there are no non-governance intents, omit the `Next Actions` section.

## Pre-Execution Checks

**Check for extension hooks (before constitution update)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_constitution` key
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

You are updating the project constitution at `.specify/memory/constitution.md`, the product context at
`.specify/memory/product.md` and the design system at `.specify/memory/design.md`. The active scaffolds are
resolved at command time from `constitution-template`, `product-template` and `design-template` through the
Spec Kit preset/template resolution stack.

**Readable references.** The three documents are read by the people who steer the product. Every reference in them follows the "Readable references" section of
`.specify/presets/backlog/knowledge/user-story-writer/rules.md`: a reference between them is a relative Markdown link whose text names
the section (`[the Personas of the product](product.md#personas)`), principles and rules are named, never numbered, so that plans and
analyses can cite them by name; sources are links whose text says what they are (`[Checkout UI kit in Figma](https://…)`), never bare
URLs or paths.

**No document versioning.** No document carries version numbers, ratification/amendment dates,
"approved by" fields, amendment history or changelog tables, nor a Sync Impact Report comment. Git history is the
record of changes; the rationale of a change goes in the commit message. If an existing document contains
such fields, remove them and mention it in the summary.

Follow this execution flow:

1. **Resolve the templates.**
   - Run `{SCRIPT}` from the repository root and parse `TEMPLATE_CONTENT` as the active constitution template.
   - Run the same resolver again with the template name `product-template` instead of `constitution-template`
     and parse its `TEMPLATE_CONTENT` as the active product template; do the same with `design-template` for the
     active design template.
   - The shared resolver applies project overrides, composing preset layers, and extension layers
     before the core template fallback. It MUST succeed before continuing. If it fails, stop and report the
     resolution error; do not continue with only one contributing template layer.
   - For each document: if it exists, load it as the source of current project-specific values. Preserve
     information that is still applicable when applying the newly resolved scaffold. If it does not exist, use the
     resolved template as the initial document.
   - Do not write back to any template layer.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]` in both documents.
   **IMPORTANT**: The user might require less or more principles, personas, journeys or terms than the ones used in
   the templates. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. **Collect/derive values for placeholders.**
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, existing specs under `specs/`, the existing documents).
   - **Product interview.** When product.md is being created and the input does not cover them, ask for the
     essentials before drafting: the elevator pitch, the problem, the personas (who they are, what they need,
     their context), the key user journeys, and the domain terms that business and developers must share.
     Ask at most 5 questions at a time, numbered, each with a table of suggested answers:

     ```markdown
     ## Question [N]: [Topic]

     **Context**: [Why it matters for the product document]

     | Option | Answer | Implications |
     |--------|--------|--------------|
     | A      | [First suggested answer] | [What this means] |
     | B      | [Second suggested answer] | [What this means] |
     | Custom | Provide your own answer | |
     ```

     If the agent has a native question tool, you may use it instead of the table. Never invent personas
     or business facts: mark what stays unknown as `TODO(<FIELD_NAME>): explanation`.
   - **Design system** (design.md). Skip it, and say so in the summary, when the product has no user interface
     (a library, an API, a CLI). Otherwise fill the tokens and the prose from the best source available, in
     this order, and record the source in `## Sources & Sync`:
     1. **Code tokens already in the repository**: CSS custom properties (`:root`), a Tailwind theme
        (`@theme` block or `tailwind.config` `theme.extend`), a `tokens.json` (W3C DTCG format), a component
        library theme. Keep the token names used in code; convert units to px/em/rem. The format expects a
        `primary` color: when the main action color has another name in code (e.g. `brand`), add `primary` with
        the same value and say in Colors which code token it mirrors.
     2. **Figma**, when the user gives a Figma file or library and the agent has a Figma connector: semantic
        color variables (default mode) → `colors`, text styles → `typography`, number variables → `spacing`
        and `rounded`, effect styles → Elevation & Depth prose, component sets and variants →
        `components.<name>-<variant>-<state>` (only the supported properties), library descriptions and
        guidelines → prose and Do's and Don'ts. A DESIGN.md exported by a Figma plugin or by Google Stitch is
        a valid starting point: adopt it and fix what does not follow the format.
     3. **Interview**: ask for a specific visual reference (not adjectives), audience and density, light or
        dark, brand colors and fonts (with licensing), corner style, elevation style, the UI framework or
        component library, the accessibility target, platforms and breakpoints.
     4. **No design system yet**: propose a minimal provisional set seeded from the chosen UI framework's
        defaults (`primary`/`on-primary`, `surface`/`on-surface`, `neutral`, `error`, 3-6 type levels, a 4/8px
        spacing scale, 3-4 radii, button and input components) with AA contrast for every text/background pair,
        and list it under `## Known Gaps` as provisional. Never invent brand colors: confirm them with the user.
     Keep the format valid: front matter on line 1, `version: alpha` (the version of the DESIGN.md format,
     not of the document), tokens only in the front matter, no ```yaml fences in the body, quoted values that
     start with `#`, `[` or `{`, dimensions in px/em/rem, numeric `fontWeight`, sections in the template's order.
     Groups deliberately left out go in an `omitted:` list with a reason.
   - **Personas** must be real humans or distinct system actors, never technical roles ("Frontend developer",
     "Database"): they are the only personas the backlog commands accept in the Connextra sentence.
   - **Ubiquitous Language**: one term per concept, no synonyms of the same object; each term gets a business
     definition (the language of marketing and stakeholders) and a dev definition (how it maps to the system).
   - **Delivery Conventions** (constitution): default to acceptance tests from Gherkin `on`, default specify mode
     `ask`, task manager `none`, unless the user says otherwise.

3. **Draft the updated documents** using the resolved templates as the required structure:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained
     template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy; comments can be removed once replaced unless they still add clarifying guidance.
   - Remove optional sections and stack groups that do not apply instead of writing "N/A".
   - Ensure each Principle section: succinct name line (other documents cite the principle by this name, never by a number
     such as "Principle II"), paragraph (or bullet list) capturing non‑negotiable rules,
     explicit rationale if not obvious.
   - Ensure the Governance section lists the amendment procedure and compliance review expectations
     (amendments are reviewed changes to this file; no versioning policy).

4. **Validation before writing:**
   - No remaining unexplained bracket tokens.
   - No version, date-of-amendment, approval or changelog fields in any document (design.md's `version: alpha` is the
     format version and stays).
   - Principles and rules are declarative, testable, and free of vague language ("should" → replace with
     MUST/SHOULD rationale where appropriate).
   - Every persona has who/needs/context; every Ubiquitous Language row has both definitions.
   - Every reference passes the self-check of the "Readable references" section: links between the documents point to
     a section heading and name it, sources are links whose text says what they are, no `§` notation, section or
     principle numbers, bare URLs or bare paths.
   - Constitution and product do not contradict each other (e.g. a compliance regulation required by product.md's
     constraints is reflected in the constitution's Security Posture).
   - design.md agrees with the constitution (accessibility target, UI framework in the Technology Stack) and every
     token referenced as `{group.token}` exists. If Node.js is available, run
     `npx --yes @google/design.md lint .specify/memory/design.md` as a standalone command and fix every error;
     report the warnings. If it cannot run, check the format rules by hand and say so in the summary.

5. **Write** the completed documents back to `.specify/memory/constitution.md`, `.specify/memory/product.md` and `.specify/memory/design.md`
   (overwrite only the ones that changed).

6. **Output a final summary** to the user with:
   - Change report, per document: modified principles (old title → new title if renamed), added and removed
     sections, added/changed personas and terms, design tokens added or changed and their source, removed
     versioning fields if any.
   - Dependent artifacts to review: existing specs whose personas or terms no longer match product.md, plans
     whose Constitution Check may change (each named by its feature and the section affected, with its path;
     do not edit them).
   - Any TODO placeholders or deferred items requiring manual follow-up.
   - Suggested commit message carrying the rationale (e.g., `docs(constitution): add test-first principle; docs(product): add Back-office Operator persona; docs(design): import tokens from the Figma library`).
   - A `Next Actions` section for any deferred non-governance intents.

Formatting & Style Requirements:

- Use Markdown headings exactly as in the templates (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision or one new term), still perform validation.

Write only `.specify/memory/constitution.md`, `.specify/memory/product.md` and `.specify/memory/design.md`; do not create or modify template source files.

## Post-Execution Checks

**Check for extension hooks (after constitution update)**:
Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.after_constitution` key
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
