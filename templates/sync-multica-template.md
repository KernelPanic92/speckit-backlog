---
tool: multica
workspace_id: "[MULTICA_WORKSPACE_ID]"
project_id: "[MULTICA_PROJECT_ID]"
# content language written to Multica; the repository always stays in English
language: en
---

<!--
  MULTICA MAPPING (preset "backlog")

  /speckit.sync reads this document every time it talks to Multica. The front matter holds the
  settings; the sections below describe the mapping in plain words: change them to change the
  behaviour. Multica is reached through its CLI (`multica`, always with `--output json`):
  authenticated with a personal access token on a laptop, or automatically with MULTICA_TOKEN
  inside a Multica run. No token lives here.

  Remove this comment block once the settings are filled in.
-->

# Multica mapping

## Items

Every PBI becomes an issue of the project, including the MAP (Multica nests issues without a depth limit).

| PBI | Multica issue | Title |
|-----|---------------|-------|
| MAP | top-level issue | `{title}` |
| EPIC | sub-issue of its MAP, or top-level without a map | `{title}` |
| US | sub-issue of its EPIC | `{title}` |
| TASK, SPIKE | sub-issue of their US (Walking Skeleton items: of their EPIC) | `{title}` (SPIKE: `Spike: {title}`) |
| BUG | sub-issue of its EPIC | `{title}` |

- **Custom properties** (created once by `/speckit.sync multica setup` if missing; a workspace has at most 20):
  - `PBI Type` — select: MAP, EPIC, US, TASK, SPIKE, BUG
  - `Backlog ID` — text: the PBI's local id (`US-007`); it makes pushes idempotent (`multica issue list --property "Backlog ID=US-007"`)
  - `Release` — select, optional: the Release Lane title of a story in a map spec
- **Issue metadata**: `speckit.id`, `speckit.type`, `speckit.path` (file in the repository), `speckit.blocked_by`, `speckit.related` (comma-separated local ids).
- **No runs on import**: create issues with status `backlog` and no assignee; update them with `--no-start`. Assigning an issue to an agent is a human decision.

## Hierarchy (default: native nesting)

`parent` = the issue of the PBI's PARENT (`--parent <key or UUID>`), created first. A spec whose root came from an existing Multica issue (see "Specs started from Multica") nests its children under that issue.

## Relations

| Backlog | Multica |
|---------|---------|
| PARENT | parent issue |
| BLOCKED_BY | metadata `speckit.blocked_by` + a "Blocked by" line in the description linking the blockers' keys |
| RELATED | metadata `speckit.related` + a "Related" line in the description |

Multica has no blocking/related relations yet (an `issue_relation` API is proposed upstream). When the workspace exposes `POST /api/issues/{id}/relations`, use `blocks` (from the blocker to this issue) and `related` instead, and remove the description lines.

## Description

- Markdown from the PBI body: Connextra sentence, Outcome, Acceptance Criteria (`AC-n`, Given/When/Then), Out of Scope, Additional Notes, Assumptions, Risks; TASK and SPIKE sections as in their templates. Leave out the INVEST & DoR check and the frontmatter.
- Then the "Blocked by" / "Related" lines, and `Source: {file} ({id})`.
- `language: it` → translate the content into Italian when writing it; the repository is never translated.

## References written back

`external.multica` in the PBI's frontmatter: `id` = issue UUID (durable), `key` = issue key such as `MUL-123` (display only: it changes if the workspace prefix is renamed), `url`, `hash`. The PBI keeps its local id.

## Specs started from Multica

`/speckit.specify MUL-42` (or an issue URL) reads the issue with `multica issue get MUL-42 --output json`, uses its title and description as the feature description, and records that issue as the root PBI's `external.multica`: the next push nests every child under it.

## Running the Spec Kit commands inside Multica

A Multica agent running Claude Code (or another supported CLI) can run `/speckit.specify`, `/speckit.plan`, `/speckit.tasks` on an issue:

1. Project resource: the repository as a **local directory in worktree mode** (the run's working directory is the repo root, so `.specify/` and `.claude/skills/speckit-*` are in place). With a GitHub repo resource the agent must `cd` into the checkout first.
2. Agent instructions (paste into the agent's instructions in Multica):
   > When an issue is assigned to you, run the `speckit-specify` skill with the issue's key as the description (it reads the issue itself). Commit on the task branch and do not switch branches. Then run `/speckit.sync multica push` so the backlog becomes sub-issues of this issue. Post a summary as a comment and set the issue to `in_review`. If the command needs answers from a human, post the questions as a comment and set the issue to `blocked` instead of guessing.
3. Disable the `git` extension's branch hook for these runs (`hooks.before_specify` → `enabled: false` in `.specify/extensions.yml` of the checkout Multica uses): Multica refuses deliveries made on a branch other than the run's own.
4. Keep the Spec Kit skills model-invocable (the default), and add `.multica/` to `.gitignore`.
5. Multica launches Claude Code without permission prompts: every command of the run executes unattended.

## Pull

Statuses, assignees and comments stay in Multica: a pull reports them. Changes to title or description made in Multica are shown as a diff and applied to the PBI only after confirmation.
