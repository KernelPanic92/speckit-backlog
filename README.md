# speckit-backlog

A [Spec Kit](https://github.com/github/spec-kit) preset that turns specifications into a **backlog**.

`/speckit.specify` asks how you want to work — **user story map**, **epic + user stories** or **single user story** — and writes the spec as Product Backlog Items (PBIs): INVEST user stories with Gherkin acceptance criteria, epics, spikes and walking-skeleton tasks, each in its own file with a validated YAML frontmatter. The rest of the workflow (clarify, plan, tasks, analyze, implement) understands that backlog.

It is a preset, not a fork: you keep using the official `specify` CLI and its upgrades.

- The backlog rules come from the *user-story-writer* skill (INVEST, vertical splitting, Gherkin, user story mapping after Patton, Rubin, Lawrence, Wake), ported to English.
- Constitution, plan, research and tasks merge current upstream templates with the ones of *Non-Deterministic Spec-Driven Development* (Enrico Papalini, [popoloni/non-deterministic-sdd](https://github.com/popoloni/non-deterministic-sdd)).
- No document versioning anywhere: no version numbers, "last amended" dates or changelog tables in constitution, product, design, plan or research. Git is the history.
- The backlog can be published to **ClickUp** or **Multica** with `/speckit.sync`, and the Spec Kit commands can run inside Multica as skills.

## Workflow

| Step | Command | What it produces |
|------|---------|------------------|
| 1 | `/speckit.constitution` | `.specify/memory/constitution.md` (how we build), `.specify/memory/product.md` (vision, **personas**, journeys, constraints, **Ubiquitous Language**) and, for products with a UI, `.specify/memory/design.md` (design system in the **DESIGN.md** format) |
| 2 | `/speckit.specify [--mode map\|epic\|story] <description>` | `specs/NNN-slug/spec.md` (root PBI + spec envelope) and `backlog/` children, `checklists/requirements.md` |
| 3 | `/speckit.clarify` | answers Open Questions, updates PBIs, adds personas/terms to product.md |
| 4 | `/speckit.plan` | a single `plan.md` (design, data model, contracts, delivery slices) and `research.md` (unknowns and Spikes answered) |
| 5 | `/speckit.tasks` | one TASK PBI per task in `backlog/tasks/` and the `tasks.md` execution index |
| 6 | `/speckit.analyze` | read-only consistency report (backlog validator, AC coverage, product.md consistency) |
| 7 | `/speckit.implement` | executes tasks phase by phase; Gherkin scenarios become acceptance tests |
| — | `/speckit.split <ID>` | carves an epic or story out of a spec into a new spec where it is the root |
| — | `/speckit.merge <source> into <target>` | absorbs a spec into another container, or groups specs under a new epic/map |
| — | `/speckit.sync <clickup\|multica> <setup\|push\|pull\|status>` | publishes the PBIs to a task manager and reads it back, following `.specify/sync/<tool>.md` |
| — | `/speckit.checklist`, `/speckit.converge` | upstream commands, extended with the backlog's identifiers |

In skills-based agents (Claude Code by default) the commands are invoked as `/speckit-specify`, `/speckit-plan`, …

## Spec modes

| Mode | `spec.md` root | Children in `backlog/` | Phases of `tasks.md` |
|------|----------------|------------------------|----------------------|
| `map` | MAP | one EPIC per Backbone Macro-Activity, their US, Walking Skeleton TASK/SPIKE | Setup → Walking Skeleton → one phase per Release Lane (the first is the MVP) → Polish |
| `epic` | EPIC | its US, SPIKEs when estimation is blocked | Setup → Foundational → one phase per story → Polish |
| `story` | US | SPIKEs if needed (TASKs come from `/speckit.tasks`) | Setup → Spikes → one phase per Acceptance Criterion → Polish |

`/speckit.specify` recommends a mode from its macro-analysis (more than one user activity → map). If a `story` turns out to need several stories it proposes `epic`. A spec that grows too big can be cut with `/speckit.split` and recombined with `/speckit.merge`.

```text
specs/003-online-purchase/
├── spec.md                         # root PBI (frontmatter type: MAP | EPIC | US) + spec envelope
├── backlog/
│   ├── epics/EPIC-002-checkout.md
│   ├── stories/US-007-card-payment.md
│   ├── spikes/SPIKE-001-payment-provider.md
│   └── tasks/TASK-014-card-payment-acceptance.md
├── checklists/requirements.md
├── research.md
├── plan.md
└── tasks.md                        # - [ ] TASK-014 [P] [US-007] Title → backlog/tasks/TASK-014-….md
```

PBI ids (`US-007`, `EPIC-002`, …) are unique across the whole project, so specs can be split and merged without renaming, and relations (`PARENT`, `BLOCKED_BY`, `RELATED`) keep resolving across specs.

## Design system: design.md

For products with a user interface, `/speckit.constitution` also writes `.specify/memory/design.md` in the [DESIGN.md format](https://github.com/google-labs-code/design.md) (Google Labs, open-sourced from Stitch; spec version `alpha`): design tokens in the YAML front matter (`colors`, `typography`, `rounded`, `spacing`, `components`) and the visual rules in eight sections in a fixed order (Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts), plus extension sections (Responsive Behavior, Motion, Accessibility, Sources & Sync, Known Gaps).

- `version: alpha` in its front matter is the version of the **format**, required by its tooling: it is not a version of the document.
- Figma does not export DESIGN.md natively. The command fills the tokens from code (CSS variables, Tailwind theme, `tokens.json`), from a Figma file through a Figma connector, from a DESIGN.md exported by Stitch or by a Figma plugin, or from an interview; with no design system yet it proposes a provisional set and lists it under Known Gaps.
- `/speckit.plan`, `/speckit.tasks`, `/speckit.implement` and `/speckit.analyze` use it for UI work: tokens instead of literal values, component rules, the accessibility target.
- Check it with the format's linter: `npx @google/design.md lint .specify/memory/design.md`.

## Task managers: ClickUp and Multica

`/speckit.sync <tool> <action>` publishes the PBIs of a spec to a task manager. The repository stays the source of truth for the content; the tool stays the source of truth for the workflow (status, assignees, comments).

```text
/speckit.sync clickup setup      # writes .specify/sync/clickup.md: settings + mapping rules
/speckit.sync clickup status     # what a push would create or update
/speckit.sync clickup push       # creates/updates items, parents first, then dependencies and links
/speckit.sync clickup pull       # reads statuses and edits made in the tool back (applied on confirmation)
```

- **Mapping documents.** `.specify/sync/<tool>.md` has the settings in its front matter and the mapping in prose (types, hierarchy, names, relations, description, language). The default is native nesting (Epic → User Story → Task); edit the prose to change it, e.g. to the one-level Epic → subtask convention described in the document.
- **Ids.** PBI ids never change. The tool's references are stored in each PBI's frontmatter, written only by the command through the validator:

  ```yaml
  external:
      clickup:
          id: "86c1x2abc"
          key: "DE-14620"
          url: "https://app.clickup.com/t/86c1x2abc"
          hash: "sha256:…"
  ```

  `hash` is the content hash at the last push: `sync-plan` compares it to tell what must be updated.
- **ClickUp** is reached through the agent's ClickUp connector (MCP): BLOCKED_BY becomes a native dependency, RELATED a task link.
- **Multica** is reached through its `multica` CLI: every PBI becomes an issue (the MAP too), nested by PARENT; `PBI Type` and `Backlog ID` custom properties make pushes idempotent; BLOCKED_BY/RELATED go in issue metadata and in the description until Multica ships issue relations. Issues are created in `backlog` with no assignee, so a push never starts an agent run.
- **Start from an item.** `/speckit.specify DE-14620` or `/speckit.specify MUL-42` reads the item as the feature description and links the spec's root PBI to it: the next push nests the backlog under it.
- **Content language** in the tool is a setting of the mapping document (default English); the repository is never translated.

### Running Spec Kit inside Multica

A Multica agent running Claude Code can run `/speckit.specify`, `/speckit.plan` and `/speckit.tasks` on an issue, as skills: give the project the repository as a local-directory resource in worktree mode (so `.specify/` and `.claude/skills/speckit-*` are in the run's working directory), paste the agent instructions from `.specify/sync/multica.md`, and disable the git extension's branch hook for those runs. Multica runs agents without permission prompts: every command of the run executes unattended.

## Installation

Prerequisites:

- Spec Kit `>= 1.2.5` and [uv](https://docs.astral.sh/uv/).
- **PyYAML for the Python that Spec Kit's template resolver uses.** With any preset installed, `.specify/scripts/bash/resolve-template.sh` needs PyYAML. Install it for your `python3` (`python3 -m pip install pyyaml`), or point Spec Kit to an interpreter that has it with `SPECKIT_PYTHON_EXECUTABLE`.

New project, preset installed at init (the preset's constitution template is used for the first seed):

```bash
specify init my-project --integration claude --extension git --preset /path/to/speckit-backlog
```

Existing project, from a release archive:

```bash
specify preset add --from https://github.com/KernelPanic92/speckit-backlog/archive/refs/tags/v0.1.0.zip
```

From the self-hosted catalog, which also enables `specify init --preset backlog`:

```bash
specify preset catalog add https://raw.githubusercontent.com/KernelPanic92/speckit-backlog/main/catalog.json --name backlog --install-allowed
specify preset add backlog
```

The preset is copied to `.specify/presets/backlog/`. Commit it with the project so the team shares the same rules.

In Claude Code you can allow the validator once for the project, so the commands run it without a permission prompt (`.claude/settings.json`):

```json
{
  "permissions": {
    "allow": [
      "Bash(uv run --no-project --quiet --with pyyaml --with jsonschema python .specify/presets/backlog/scripts/validate_backlog.py:*)"
    ]
  }
}
```

## Configuration

`/speckit.constitution` writes a **Delivery Conventions** section that the commands read:

| Convention | Values | Default |
|------------|--------|---------|
| Acceptance tests from Gherkin | `on`: every scenario `US-xxx/AC-n` gets an acceptance-test task written before the story's implementation; `off`: tests only on request | `on` |
| Default specify mode | `ask`, `map`, `epic`, `story` | `ask` |
| Task manager | `none`, `clickup` or `multica`: the tool `/speckit.sync` publishes the backlog to. PBI ids stay local (`US-007`); the tool's ids go in each PBI's `external` block | `none` |

Templates can be overridden per project as usual in Spec Kit: put a file with the template's name in `.specify/templates/overrides/` (e.g. `pbi-story-template.md`).

## What the preset changes

| Upstream artifact | In this preset |
|-------------------|----------------|
| `speckit.specify` | Replaced: mode selection, product context check, user-story-writer phases, PBI files, validator, skill-based quality checklist. Upstream hooks (git branch creation) kept verbatim |
| `speckit.clarify`, `speckit.plan`, `speckit.analyze` | Upstream text with targeted changes: PBIs instead of FR-###, single plan + research template, backlog validator |
| `speckit.tasks` | Replaced: TASK PBI files + execution index, phases by spec mode, Gherkin-driven test tasks |
| `speckit.constitution` | Upstream flow without semver/dates/Sync Impact Report; also writes product.md |
| `speckit.implement`, `speckit.checklist`, `speckit.converge` | Upstream command + an appended addendum (`strategy: append`) |
| `speckit.split`, `speckit.merge`, `speckit.sync` | New |
| templates | constitution, plan, tasks and spec envelope merged from upstream and Papalini; product, research and the five PBI templates added |

`NOTICE.md` lists, for every template, where each section comes from.

## The validator

`scripts/validate_backlog.py` makes the structural checks deterministic. The commands call it; you can too:

```bash
uv run --no-project --quiet --with pyyaml --with jsonschema \
  python .specify/presets/backlog/scripts/validate_backlog.py check --all
```

- `check <feature-dir> | --all` — frontmatter against `schemas/pbi-frontmatter.schema.json`, hierarchy (at most one PARENT, allowed parent types), unknown ids, cycles, canonical relation order, duplicate ids, leftover placeholders, EPIC Scope Boundaries and `AC-n` ids, Backlog Index links, Release Lane order vs `BLOCKED_BY`, `tasks.md` lines vs TASK files.
- `next-id <TYPE> [--count N]` — first free project-wide id.
- `locate <ID> [--descendants]` — file, spec, references and descendants of a PBI.

JSON on stdout; exit code 1 when errors are found.

## Development

```bash
# unit tests of the validator
uv run --no-project --with pytest --with pyyaml --with jsonschema pytest tests

# try the preset in a scratch project
specify init /tmp/try --integration claude --extension git --preset "$PWD"
# after editing the preset, reinstall it (a --dev install is a copy, not a link)
cd /tmp/try && specify preset add --dev /path/to/speckit-backlog
```

### Keeping up with Spec Kit

The replaced commands were derived from Spec Kit **v1.2.5** and keep upstream's wording wherever possible. When a new Spec Kit version ships:

```bash
tools/upstream-diff.sh v1.3.0     # diff of the upstream files this preset replaces or composes, v1.2.5 → v1.3.0
```

Port the relevant changes (new hook wording, new placeholders, new steps) into `commands/` and `templates/`, bump `BASE` in the script and `requires.speckit_version` in `preset.yml`.

## License

MIT — see `LICENSE`. Third-party material (Spec Kit, Non-Deterministic SDD templates) is credited in `NOTICE.md`.
