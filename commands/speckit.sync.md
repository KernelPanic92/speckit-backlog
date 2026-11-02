---
description: Sync the backlog (PBIs of a spec) with an external tool - ClickUp or Multica - following the project's mapping document; setup, push, pull or status.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --paths-only
  ps: scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly
  py: scripts/python/check_prerequisites.py --json --paths-only
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Publish the PBIs of a spec (MAP, EPIC, US, TASK, SPIKE) to an external tool and keep the two in step, while the repository stays the source of truth for the content and the tool stays the source of truth for the workflow (status, assignees, comments).

Input: `<tool> <action> [scope]`

- `tool`: `clickup` or `multica` (the adapters this preset ships). If missing, list the mapping documents found in `.specify/sync/` and ask.
- `action`: `setup` (create or update the mapping document), `push` (create/update items in the tool), `pull` (read the tool back), `status` (report only). Default: `status`.
- `scope`: a feature directory, a PBI id (that PBI and its descendants), or `--all`. Default: the active feature.

Paths used by this command (preset `backlog`):

- `MAPPING` = `.specify/sync/<tool>.md` — the project's mapping document: settings in the front matter, the mapping rules in prose. **Follow it literally**: the user edits it to change how PBIs become items (types, hierarchy, names, relations, description, language).
- `VALIDATOR` = `uv run --no-project --quiet --with pyyaml --with jsonschema python .specify/presets/backlog/scripts/validate_backlog.py` — `sync-plan <tool> <feature-dir>|--all [--only ID]`, `set-external <ID> <tool> --id … [--key …] [--url …] --hash-current`, `set-external <ID> <tool> --remove`, `check`. Run it as a standalone command (not chained with `;`, `&&` or pipes) so that it can be allow-listed in the agent's permissions. If `uv` is not available, stop: references to external tools must be written deterministically.

**Rules that hold for every action**

- PBI ids never change. The tool's ids live only in the PBI's `external.<tool>` block, written **only** through `VALIDATOR set-external` (never edit that block by hand).
- Writing to the tool is an outward-facing action: before the first write of a run, show what will be created and updated and wait for the user's confirmation. Exception: the user already asked for an unattended push in this request (e.g. inside a Multica run whose agent instructions say so).
- No credentials in the repository: ClickUp is reached through the agent's ClickUp connector (MCP); Multica through its CLI, authenticated by the user or by `MULTICA_TOKEN` inside a Multica run.
- Content language in the tool follows `language` in `MAPPING`; the repository is never translated.

## Execution Steps

1. **Setup context**: Run `{SCRIPT}` from repo root and parse `FEATURE_DIR` (the active feature). Resolve the scope to a feature directory, a PBI id or `--all`.

2. **Check the connection** to the tool:
   - ClickUp: the agent must have a ClickUp connector (tools to read, create and update tasks, add dependencies and links). If none is available, stop and tell the user to connect ClickUp to the agent.
   - Multica: run a read-only CLI call such as `multica issue list --output json --fields id` as a standalone command. If the CLI is missing or not authenticated, stop and tell the user how to install it and log in (or to run inside a Multica run).

3. **Setup** (action `setup`, or any action when `MAPPING` does not exist yet):
   - Resolve the mapping template with `.specify/scripts/bash/resolve-template.sh sync-<tool>-template --json` (PowerShell: `.specify/scripts/powershell/resolve-template.ps1 sync-<tool>-template -Json`) and parse `TEMPLATE_CONTENT`. If `MAPPING` exists, keep its values and its edited prose.
   - Fill the settings with the user, reading what you can from the tool:
     - ClickUp: workspace and list (resolve the list by name through the connector), whether the workspace uses custom task ids, the task type names that exist (`Epic`, `User Story`, `Bug`…), the content language.
     - Multica: workspace and project (`multica project list --output json`), the content language; check that the custom properties `PBI Type`, `Backlog ID` (and optionally `Release`) exist, and create the missing ones only after the user confirms (`multica property create …`).
   - Ask whether to keep the default **native nesting** or to switch to the alternative described in the document; edit the prose accordingly.
   - Write `MAPPING` (create `.specify/sync/` if needed). Do not store tokens or personal data in it. Remove the template's guidance comment.

4. **Plan**: run `VALIDATOR sync-plan <tool> <feature-dir>` (or `--all`, or `--only <ID>` for a PBI scope). It lists, parents before children, every PBI with its `action` (`create`, `update`, `unchanged`), its parent and ancestors, its non-PARENT relations, and the external references already known for parent and related PBIs. Apply the mapping's item rules to it (e.g. a MAP that the mapping does not sync is skipped).

5. **Push** (action `push`):
   1. Show the plan: counts per action and per type, and the items to create or update (`type [id] title`). Wait for confirmation (see the rules above).
   2. For each item in plan order:
      - `create`: create the item as `MAPPING` says (type, name, parent, description, properties). The parent's tool id comes from `parent_external` (or from the external reference of the ancestor the mapping names, e.g. the nearest Epic in a flat hierarchy). Then run `VALIDATOR set-external <ID> <tool> --id <tool id> --key <display key> --url <url> --hash-current`.
      - `update`: update name and description (and the properties the mapping lists) of the item in `external.<tool>.id`, without changing status or assignee; Multica: with `--no-start`. Then `VALIDATOR set-external <ID> <tool> --hash-current`.
      - `unchanged`: skip.
      - If the tool rejects an item, stop: report the error and what was already written. A new push resumes from there, because every item written so far carries its reference.
   3. **Relations pass**: for each pushed item, apply its BLOCKED_BY and RELATED relations as `MAPPING` says, between items that both have a reference in this tool. Read the item's existing dependencies/links first and add only the missing ones. A relation towards a PBI not yet in the tool is reported, not dropped: it is applied by a later push.
   4. Run `VALIDATOR check` on the feature directories touched (the `external` blocks must validate).

6. **Pull** (action `pull`): for each PBI in scope that has `external.<tool>`:
   - read the item; report its status, assignee and the number of new comments;
   - compare its name and description with what a push would write from the PBI; when they differ because someone edited the tool, show the difference and, only if the user confirms, update the PBI file (keep it valid against the rules in `.specify/presets/backlog/knowledge/user-story-writer/rules.md`), then `VALIDATOR set-external <ID> <tool> --hash-current`;
   - an item deleted in the tool: ask whether to remove the reference (`set-external <ID> <tool> --remove`).
   Statuses are never written into the PBIs.

7. **Status** (action `status`): run step 4 and report, without writing anything: items linked, to create, to update, relations still missing, and the location of `MAPPING`.

## Completion Report

- Tool, action, scope, and `MAPPING` path
- Created / updated / unchanged / failed items, by type, each with its display key (e.g. `US [US-007] Card payment → DE-14620`)
- Relations added and relations postponed
- Pull: statuses read, PBIs updated from the tool, references removed
- Validator result
- Next step (e.g. "assign the Release 1 stories in ClickUp", or "run `__SPECKIT_COMMAND_SYNC__ <tool> push` again after `__SPECKIT_COMMAND_TASKS__`")

## Done When

- [ ] The requested action ran against the tool named in the input, following `MAPPING`
- [ ] Every item written in the tool has its reference in the PBI's `external` block, set through the validator
- [ ] Validator passing on the touched specs (or remaining errors reported)
- [ ] Completion reported to user
