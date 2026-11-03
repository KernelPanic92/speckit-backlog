---
description: Combine specs - absorb the root PBI of one spec as a child of another spec's container (US into EPIC, EPIC into MAP), or group several specs under a new EPIC or MAP.
handoffs:
  - label: Clarify The Merged Spec
    agent: speckit.clarify
    prompt: Clarify the requirements of the merged spec
  - label: Plan The Merged Spec
    agent: speckit.plan
    prompt: Create a plan for the merged spec. I am building with...
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

The inverse of `__SPECKIT_COMMAND_SPLIT__`. The root PBI of a **source** spec, with all its descendants, becomes a child of a **target** container, and the source spec directory is retired. Two forms:

- **Absorb**: `<source> into <target>` — `<source>` is a spec directory or its root id; `<target>` is a spec directory or a container id (its root, or an EPIC that is a child of a map spec).
- **Group**: `<source> <source> … --new-epic "Title"` or `--new-map "Title"` — creates a new spec whose root is a new EPIC or MAP, and makes each source root its child.

Ids are project-wide unique, so files move without renaming and relations keep resolving.

Paths used by this command (preset `backlog`):

- `RULES` = `.specify/presets/backlog/knowledge/pbi-writing/rules.md` — the hierarchy (MAP → EPIC → US → TASK/SPIKE), the map rules (Backbone, Walking Skeleton, Release Lanes, gravity) and how to write a new EPIC or MAP. Its "Readable references" section applies to every marker, note and link this command writes, and to the plan and the report it prints.
- `VALIDATOR` = `uv run --no-project --quiet --with pyyaml --with jsonschema python .specify/presets/backlog/scripts/validate_backlog.py` — `locate <ID> --descendants`, `next-id <TYPE>`, `check <feature-dir>`. If `uv` is not available, find the files with a text search for `id: <ID>` under `specs/` and check them by hand against `.specify/presets/backlog/schemas/pbi-frontmatter.schema.json`. Run it as a standalone command (not chained with `;`, `&&` or pipes) so that it can be allow-listed in the agent's permissions.

## Allowed combinations

| Source root | Target | Result |
|-------------|--------|--------|
| US | EPIC (a spec root, or a child Epic of a map) | the US becomes a child of the Epic (PARENT: that EPIC) |
| US | MAP | ask which Backbone Epic receives it, then as above; ask its Release Lane |
| EPIC | MAP | the Epic becomes a new Backbone Macro-Activity (PARENT: the MAP); ask its position in the Backbone and the lane of each of its stories |
| EPIC | EPIC | an Epic cannot be a child of an Epic: propose to re-parent the source Epic's stories to the target Epic and retire the source Epic, merging its Scope Boundaries into the target's; do it only if the user agrees |
| several US | `--new-epic` | new EPIC root, the stories become its children |
| several EPIC (and US) | `--new-map` | new MAP root, the Epics become its Backbone; US roots must be grouped under an Epic first (ask) |
| MAP | anything | not supported (a map is a product-level root); suggest moving its Epics instead |

## Execution Steps

1. **Parse and locate**: resolve every source and the target with `VALIDATOR locate <ID> --descendants` (for a directory, read the root id from its `spec.md` frontmatter). Read `RULES` and `.specify/memory/product.md`. Stop with an explanation if the combination is not allowed.

2. **Show the merge plan and wait for confirmation**:
   - the target spec directory (for `--new-epic` / `--new-map`: the new directory, numbered as in `__SPECKIT_COMMAND_SPECIFY__`, and the new root's id from `VALIDATOR next-id EPIC|MAP`);
   - the files that move and their new location under the target's `backlog/`;
   - the questions you need answered (Backbone position, Release Lanes, receiving Epic), each with a recommendation based on `RULES` (gravity, lane Outcome as the filter: "is this story strictly necessary to reach this lane's Outcome?");
   - that the source spec directory will be removed after the move, with what it contains (plan.md, tasks.md, research.md, checklists/).

   Proceed only after the user confirms and answers.

3. **New root (Group form only)**: write the new EPIC or MAP root with its template (resolve `pbi-epic-template` or `pbi-map-template` with `.specify/scripts/bash/resolve-template.sh <name> --json`, or the PowerShell equivalent), following `RULES`: Connextra with a persona from product.md, Outcome, Scope Boundaries (EPIC) or Backbone / Walking Skeleton / Release Lanes / DoR Check (MAP — run Phase 3b of the rules with the user). Then append the spec envelope (`{SCRIPT}` → `TEMPLATE_CONTENT`).

4. **Move the PBIs**:
   - The source `spec.md` is split in two: its root PBI (frontmatter + body) becomes a child file under the target's `backlog/` (`epics/` or `stories/`, named `<ID>-<slug>.md`); its envelope is merged into the target envelope (step 5).
   - The source descendants move to the matching target `backlog/` subfolders. In a git repository use `git mv` so history follows the files.
   - Set the moved root's `PARENT` relation to its new container (replace any previous PARENT, keep the canonical relation order of `RULES`). Descendants keep their relations.
   - For the EPIC → EPIC case agreed with the user: re-parent the stories, merge the Scope Boundaries, then delete the source EPIC file.

5. **Merge the envelopes** into the target `spec.md`:
   - Backlog Index: add the moved PBIs in the order the rules require.
   - Success Criteria: append the source criteria, renumbered after the target's last `SC-###`, dropping exact duplicates.
   - Key Entities, Non-Functional Requirements, External Dependencies, Security & Compliance Checklist: merge, keeping one entry per concept (Ubiquitous Language terms).
   - Open Questions: move them, fixing their PBI links. Clarifications: copy them under `### Carried over from <source root title>` (the source directory is removed, so name the spec by its root's title, not by its path).
   - Map targets: update the Backbone (new column at the agreed position, referencing the Epic as `EPIC [id] title`), add a Walking Skeleton item for a new Macro-Activity (a TASK or SPIKE with the Epic as PARENT, from `pbi-task-template` / `pbi-spike-template`), place every moved story in its agreed Release Lane respecting BLOCKED_BY, and re-run the map's DoR Check.
   - Remove any ` → [moved to …](…)` extraction markers that pointed to the source spec, and fix every relative link that pointed into it.

6. **Retire the source spec directory**: if it contains research.md, copy its Decisions that still apply into the target's research.md (or note in the Completion Report that the target needs `__SPECKIT_COMMAND_PLAN__`). Then remove the source directory (`git rm -r` in a git repository). If `.specify/feature.json` pointed to it, point it to the target.

7. **Stale artifacts**: if the target has plan.md or tasks.md, add a note at the top (`> Merged TYPE [ID] Title, formerly a spec of its own, by __SPECKIT_COMMAND_MERGE__ — regenerate with __SPECKIT_COMMAND_PLAN__ / __SPECKIT_COMMAND_TASKS__.`). Moved TASK PBIs keep their files; their lines are added to tasks.md only when tasks are regenerated.

8. **Validate**: run `VALIDATOR check` on the target directory (and on any other spec whose PBIs reference the moved ones). Fix structural errors caused by the move and re-run. Then run the self-check of the "Readable references" section of `RULES` on what you wrote, including the relative links of the moved files, which may now point to the wrong place.

## Completion Report

- Target spec directory and root PBI (`type [id] title`)
- PBIs moved (count per type), relations changed, source directory removed
- Map changes (Backbone, Walking Skeleton, Release Lanes), if any
- Validator results
- Next steps: `__SPECKIT_COMMAND_CLARIFY__`, then `__SPECKIT_COMMAND_PLAN__` and `__SPECKIT_COMMAND_TASKS__` on the target

## Done When

- [ ] Every source root is a child of the target container, with its descendants moved and relations updated
- [ ] Target envelope merged; source spec directory retired after confirmation
- [ ] Validator passing (or remaining errors reported)
- [ ] Completion reported to user
