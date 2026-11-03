---
tool: clickup
workspace_id: "[CLICKUP_WORKSPACE_ID]"
list_id: "[CLICKUP_LIST_ID]"
# content language written to ClickUp; the repository always stays in English
language: en
---

<!--
  CLICKUP MAPPING (preset "backlog")

  /speckit.sync reads this document every time it talks to ClickUp. The front matter holds the
  settings; the sections below describe the mapping in plain words: change them to change the
  behaviour (for example to switch to the flat hierarchy described under "Alternative").
  ClickUp is reached through the agent's ClickUp connector (MCP); no API token lives here.

  Remove this comment block once the settings are filled in.
-->

# ClickUp mapping

## Items

| PBI | ClickUp item | Task type | Name |
|-----|--------------|-----------|------|
| MAP | not synced: the map stays in the repository (it is not a work item) | — | — |
| EPIC | task in the list | `Epic` | `{title}` |
| US | subtask | `User Story` | `{title}` |
| TASK | subtask | default task type | `{title}` |
| SPIKE | subtask | default task type | `Spike: {title}` |
| BUG | subtask | `Bug` | `{title}` |

- Task types are passed by name and must already exist in the workspace. If a type is rejected, stop and report it: never fall back to another type silently.
- Tags: use only tags that already exist in the space; never create new ones.

## Hierarchy (default: native nesting)

The ClickUp hierarchy mirrors the backlog's PARENT relations:

- EPIC → a task in the list. When the spec's root is a MAP, its Epics are top-level tasks.
- US → subtask of its EPIC.
- TASK and SPIKE → subtask of their US (nested subtask). Walking Skeleton items, whose PARENT is an Epic, are subtasks of that Epic.
- A spec whose root is a US or an EPIC with no PARENT becomes a top-level task.

### Alternative: flat hierarchy (one level)

Some workspaces allow only Epic → subtask. To use that convention, replace the rules above with:

- EPIC → task in the list; US, TASK, SPIKE, BUG → subtasks of their nearest Epic ancestor, all at the same level, never nested in each other.
- Names of subtasks are prefixed with the Epic's title: `[{epic_title}] {title}`.
- A TASK or SPIKE whose PARENT is a US gets a task link to that US (it cannot be its subtask).

## Relations

| Backlog | ClickUp |
|---------|---------|
| PARENT | `parent` of the subtask (see Hierarchy) |
| BLOCKED_BY | dependency: this task is `waiting_on` the blocker |
| RELATED | task link |

Relations are set after every item of the run exists, so that both ends have a ClickUp id.

## Description

- Written as Markdown (`markdown_description`), from the PBI body: Connextra sentence, Outcome, Acceptance Criteria with their `AC-n` headings and Given/When/Then, Out of Scope, Additional Notes, Assumptions, Risks; for TASK: Outcome, Covers, Files, Actions to complete, Out of Scope, DoD; for SPIKE: question, Timebox, Expected output, Exit Criteria.
- Leave out the INVEST & DoR check and the frontmatter.
- References inside the description stay readable for a person who has only ClickUp (the "Readable references" rules of the backlog preset): a PBI cited as `type [id] title` keeps its title and, when that PBI has an `external.clickup.url`, its `[id]` becomes a link to that task; a relative link to a file of the repository (`spec.md`, `plan.md`, `research.md`, a PBI file) becomes a link to the same file and heading on the repository's web host when the remote is known (`git remote get-url origin`), otherwise its text stays as plain words without the address.
- End with one line that tells a reader where the PBI lives in the repository, naming it by id and title: `Source in the repository: [{id} {title}]({file on the repository's web host})`, or `Source in the repository: {id} {title}, file {file}` when the web host is not known.
- `language: it` → translate the content into Italian when writing it (section headings stay in English); the repository is never translated.
- Workspaces whose task types apply a description template after creation: create the task without description, read it again until the template has been applied (status no longer the initial one, or custom fields populated, at most ~15 attempts), then write the description.

## Release lanes (map specs)

Release lanes are not synced by default. To sync them, name an existing dropdown custom field here, e.g. `Release: custom field "Release" (dropdown), option = lane title`, and create its options in ClickUp first.

## References written back

`/speckit.sync` stores in each PBI's frontmatter (`external.clickup`): `id` = ClickUp task id, `key` = custom task id when the workspace uses them (e.g. `DE-14620`), `url` = task URL, `hash` = content hash at the last push. The PBI keeps its local id.

## Pull

ClickUp statuses, assignees and comments stay in ClickUp: a pull reports them. Changes to name or description made in ClickUp are shown as a diff and applied to the PBI only after confirmation.
