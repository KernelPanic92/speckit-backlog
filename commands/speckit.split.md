---
description: Carve an EPIC or a USER STORY (with all its descendants) out of its current spec into a new spec where it becomes the root PBI - for map activities or epics that grew too big to plan and deliver together.
handoffs:
  - label: Plan The New Spec
    agent: speckit.plan
    prompt: Create a plan for the new spec. I am building with...
  - label: Clarify The New Spec
    agent: speckit.clarify
    prompt: Clarify the requirements of the new spec
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

## Goal

Move one PBI — an `EPIC` (typically a Backbone Macro-Activity of a map) or a `US` — together with all its descendants (stories, spikes, TASK PBIs that have it as PARENT, recursively) into a **new spec directory**, where it becomes the root PBI of `spec.md`. The original spec keeps a reference to it, so the product-level view (e.g. the map's Backbone and Release Lanes) stays whole.

Ids are project-wide unique, so files move without renaming and every relation (`PARENT`, `BLOCKED_BY`, `RELATED`) keeps resolving across specs.

Paths used by this command (preset `backlog`):

- `RULES` = `.specify/presets/backlog/knowledge/pbi-writing/rules.md` — its "Readable references" section applies to every marker, note and link this command writes in either spec, and to the report.
- `VALIDATOR` = `uv run --no-project --quiet --with pyyaml --with jsonschema python .specify/presets/backlog/scripts/validate_backlog.py` — `locate <ID> --descendants`, `check <feature-dir>`. If `uv` is not available, find the files with a text search for `id: <ID>` under `specs/` and follow the PARENT relations by hand. Run it as a standalone command (not chained with `;`, `&&` or pipes) so that it can be allow-listed in the agent's permissions.

## Execution Steps

1. **Parse the input**: one or more PBI ids (e.g. `EPIC-002`, `US-007`). Each id becomes **its own** new spec. Optional: a short name for each new spec. If no id is given, ask which PBI to split out, listing the EPICs (map) or US (epic) of the active spec (`.specify/feature.json`).

2. **Locate and check** each id with `VALIDATOR locate <ID> --descendants`:
   - The PBI must be an `EPIC` or a `US`. A `MAP` is always a root already; a `TASK` or `SPIKE` cannot be a spec root — stop and explain.
   - The PBI must be a child in its spec, not its root (a root is already a spec of its own).
   - Note the source spec directory (`SOURCE_DIR`), the files to move (the PBI and its descendants) and the PBIs in other files that reference any of them.

3. **Show the split plan and wait for confirmation** — for each id:
   - the new spec directory name (numbering as in `__SPECKIT_COMMAND_SPECIFY__`: `.specify/init-options.json` `feature_numbering`, sequential `NNN` by default; short name from the PBI title, 2-4 words);
   - the new mode: `epic` for an EPIC root, `story` for a US root;
   - every file that moves, and what changes in the source spec (see step 6);
   - whether the source has plan.md / tasks.md that will need regenerating.

   Proceed only after the user confirms.

4. **Create the new spec**:
   - Run `{SCRIPT}` and parse `TEMPLATE_CONTENT` as the spec envelope. If it fails, stop and report the resolution error.
   - `mkdir -p` the new directory and the `backlog/` subfolders needed.
   - Move the PBI file to the new `spec.md` and its descendants to the matching `backlog/` subfolders. In a git repository use `git mv` so history follows the files.
   - Append the envelope after the root PBI's body and fill it from the source envelope, keeping only what concerns the moved PBIs:
     - Spec Context: the new mode, the root PBI, status `Draft`, and `Input: split from [<source root title>](../<source dir>/spec.md)` (a link whose text names the source spec).
     - Backlog Index: the moved children, in the order the rules require.
     - Success Criteria, Key Entities, Non-Functional Requirements, External Dependencies, Security & Compliance Checklist: copy the items that apply to the moved PBIs (renumber `SC-###` from 001 in the new spec).
     - Open Questions that affect only moved PBIs: move them; questions that affect both specs: copy them in both, fixing their PBI links.
     - Clarifications that concern moved PBIs: copy them under `### Carried over from <source root title>`, with a link to the source spec right below the heading.
   - Relations stay as they are: the new root keeps its PARENT (e.g. the MAP it belongs to), and its children keep pointing to it.

5. **Root rules**: the new root must satisfy `RULES` as a root: an EPIC root keeps its Scope Boundaries and Acceptance Criteria; a US root keeps its Out of Scope. Do not rewrite stories beyond what the move requires.

6. **Update the source spec** (`SOURCE_DIR/spec.md`), without deleting the product-level view:
   - Map Backbone: keep the Epic's column and add ` → [moved to its own spec](../NNN-slug/spec.md)` after its title.
   - Map Release Lanes: keep the moved stories in their lanes, each followed by ` → [moved to the <new root title> spec](../NNN-slug/spec.md)`, so the release plan stays readable.
   - Backlog Index: replace the moved PBIs with one line `- Extracted: [TYPE [ID] Title](../NNN-slug/spec.md)`.
   - Move or copy Open Questions and Clarifications as in step 4.
   - If `SOURCE_DIR/tasks.md` exists: remove the lines of the moved TASK PBIs and add, at the top of the file, `> Tasks of TYPE [ID] Title moved to [the <new root title> spec](../NNN-slug/spec.md) by __SPECKIT_COMMAND_SPLIT__ — regenerate with __SPECKIT_COMMAND_TASKS__.` Report which moved tasks were already checked.
   - If `SOURCE_DIR/plan.md` exists: add the same kind of note at the top of the Summary; do not edit the design.

7. **Validate**: run `VALIDATOR check` on the new directory and on `SOURCE_DIR`. Fix structural errors caused by the move (e.g. Backlog Index links) and re-run. Then run the self-check of the "Readable references" section of `RULES` on what you wrote, including the relative links of the moved files (a PBI moved into `spec.md` or into another directory may now point to the wrong place).

8. **Active feature**: ask whether to make the new spec the active one (`.specify/feature.json` → `feature_directory`). Change it only if the user agrees.

## Completion Report

- New spec directory, mode and root PBI (`type [id] title`) for each split
- Files moved (count per type) and checked tasks among them
- Changes made to the source spec
- Validator results for both directories
- Next steps: `__SPECKIT_COMMAND_CLARIFY__` / `__SPECKIT_COMMAND_PLAN__` / `__SPECKIT_COMMAND_TASKS__` on the new spec; `__SPECKIT_COMMAND_PLAN__` / `__SPECKIT_COMMAND_TASKS__` on the source spec if they existed

## Done When

- [ ] Every requested PBI is the root of its own new spec, with its descendants moved
- [ ] The source spec references the extracted PBIs and has no dangling Backlog Index entries or task lines
- [ ] Validator passing on both specs (or remaining errors reported)
- [ ] Completion reported to user
