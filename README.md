# speckit-backlog

A [Spec Kit](https://github.com/github/spec-kit) preset for durable backlog management and backlog-driven specifications. It is a preset, not a fork: keep using the official `specify` CLI and its upgrades.

`/speckit.backlog` writes reusable Agile/BDD Product Backlog Items (PBIs) to the central `backlog/`. `/speckit.specify` accepts free text or any functional PBI (`MAP`, `EPIC`, `FEATURE`, or `US`) and produces a clean four-block `spec.md` linked to that backlog. `/speckit.tasks` idempotently reconciles implementation TASKs. `scripts/backlog.py` computes deterministic wave-based `[P]` scheduling and supports one PR/worktree per User Story.

The backlog follows INVEST, vertical slicing, Gherkin acceptance criteria, and User Story Mapping. Documents use readable references: name a PBI with its type, ID, and title; name the scenario and section in links; avoid bare IDs and paths. Constitution, plan, research, and tasks merge upstream templates with material from *Non-Deterministic Spec-Driven Development* by Enrico Papalini. Git is the document history; the documents do not carry version or changelog metadata.

## Workflow

| Command | Purpose |
|---------|---------|
| `/speckit.constitution` | Set engineering principles and write product context: personas, journeys, constraints, and Ubiquitous Language. For UI products, also establish `design.md`. |
| `/speckit.backlog` | Create, map, refine, reorder, and retire PBIs in the central `backlog/`. |
| `/speckit.specify` | Turn free text or a functional PBI into a scoped, four-block `spec.md`. |
| `/speckit.clarify` | Resolve scope questions with the user and record accepted clarifications in the specification. |
| `/speckit.plan` | Produce feature research and a modular `plan.md` with conditional `data-model.md`, `contracts/`, `quickstart.md`, and delivery slices; durable decisions go in `docs/adr/`. |
| `/speckit.tasks` | Reconcile central TASK PBIs idempotently and render the task execution index. |
| `/speckit.analyze` | Check consistency across product context, PBIs, acceptance criteria, and computed schedule. |
| `/speckit.implement` | Execute scheduled work, with one PR/worktree per User Story and TASK-owned progress. |
| `/speckit.checklist` | Generate a requirements checklist with specification and PBI traceability. |
| `/speckit.converge` | Review outcomes and scope, record findings, and reconcile follow-up TASKs. |

In skills-based agents such as Claude Code, commands are invoked as `/speckit-constitution`, `/speckit-backlog`, and so on.

## 7-Type PBI Hierarchy & Central Layout

The functional hierarchy is `MAP → EPIC → FEATURE → US → TASK/SPIKE`. `BUG` is also tolerated for Spec Kit's bug extension. Each PBI has a permanent project-wide ID and a file in its type directory; moving it in the hierarchy changes its `PARENT`, not its path.

```text
backlog/
├── index.md
├── maps/
├── epics/
├── features/
├── stories/
├── spikes/
├── tasks/
└── bugs/                 # optional; used by the bug extension

specs/003-online-purchase/
├── spec.md               # Header, Backlog, Key Entities, Success Criteria
├── research.md
├── plan.md
├── data-model.md         # when entities or state change
├── contracts/            # when external interfaces change
├── quickstart.md         # runnable verification runbook
├── tasks.md              # rendered schedule and TASK links
└── checklists/
    └── requirements.md

docs/adr/                  # durable, atomic project-wide architecture decisions
└── 0001-example-decision.md
```

The `spec.md` **Scope** selects functional PBIs; its `## Backlog` block is rendered from the central `backlog/`. PBI files stay in the repository-wide backlog and can be referenced by multiple specifications.

## Modular Plan, Research & ADRs

`research.md` holds feature-scoped facts and, only for genuine architectural forks, a trade-off matrix with 10x stress tests and poison-pill analysis. `docs/adr/` holds durable, atomic project-wide decisions and their supersession history. The modular `plan.md`, conditional `data-model.md` and `contracts/`, and runnable `quickstart.md` keep feature execution zero-fluff, human-reviewable, and progressively loadable by parallel sub-agents.

## Ordering, Waves & Parallel Execution

Declare three scheduling inputs: sibling `rank` (lower ranks first), `BLOCKED_BY` dependencies, and exact touched paths in each TASK's `## Files`. `scripts/backlog.py` combines them into one computed schedule. It respects dependencies and avoids placing items with conflicting file paths in the same wave. Every item in a wave with two or more independent items receives the computed `[P]` marker; authors do not hand-maintain wave assignments or `[P]`.

Deliver one PR/worktree per `US`. The `Story isolation` convention controls whether to use a worktree, branch, or ask first. TASK files own completion checkboxes under `## Actions to complete` and `## Definition of Done`; `tasks.md` is a rendered index, not a second source of progress state.

## Design system: design.md

For products with a user interface, `/speckit.constitution` writes `.specify/memory/design.md` in the [DESIGN.md format](https://github.com/google-labs-code/design.md) (Google Labs, format version `alpha`). It contains YAML design tokens (`colors`, `typography`, `rounded`, `spacing`, `components`) and the eight canonical visual sections in a fixed order, plus extension sections for responsive behavior, motion, accessibility, sources, and known gaps.

- `version: alpha` identifies the format, not a document version.
- The command can derive tokens and rules from code, a design file through a connector, an exported DESIGN.md, or an interview. For a new system it proposes provisional values and records gaps.
- Plan, tasks, implementation, and analysis use the design system for UI work, including tokens, component rules, and accessibility targets.
- Check the file with `npx @google/design.md lint .specify/memory/design.md`.

## Installation

Prerequisites: Spec Kit `>= 1.2.5`, [uv](https://docs.astral.sh/uv/), and PyYAML for the Python interpreter used by Spec Kit's template resolver. Install PyYAML for `python3` or set `SPECKIT_PYTHON_EXECUTABLE` to an interpreter that has it.

Initialize a project with the preset (its constitution template seeds the project):

```bash
specify init my-project --integration claude --extension git --preset /path/to/speckit-backlog
```

Install into an existing project from a release archive:

```bash
specify preset add --from https://github.com/KernelPanic92/speckit-backlog/archive/refs/tags/v0.2.0.zip
```

Or add the catalog, which also makes `specify init --preset backlog` available:

```bash
specify preset catalog add https://raw.githubusercontent.com/KernelPanic92/speckit-backlog/main/catalog.json --name backlog --install-allowed
specify preset add backlog
```

The preset is copied to `.specify/presets/backlog/`; commit that directory so the team shares the same rules. In Claude Code, allow the backlog CLI in `.claude/settings.json` if desired:

```json
{
  "permissions": {
    "allow": [
      "Bash(uv run --no-project --quiet --with pyyaml --with jsonschema python .specify/presets/backlog/scripts/backlog.py:*)"
    ]
  }
}
```

## Configuration

`/speckit.constitution` writes **Delivery Conventions** for the workflow to follow:

| Convention | Values | Default |
|------------|--------|---------|
| Acceptance tests from Gherkin | `on` or `off` | `on` |
| Story isolation | `worktree`, `branch`, or `ask` | `worktree` |

Templates can be overridden in `.specify/templates/overrides/` using their template filenames, such as `pbi-story-template.md`.

## What the preset changes

| Upstream artifact | Preset behavior |
|-------------------|-----------------|
| `speckit.constitution` | Keeps the upstream flow without document versioning and adds product context and delivery conventions. |
| `speckit.specify` | Replaces the flow with free-text/PBI selection, central backlog references, and a rendered four-block specification. |
| `speckit.backlog` | Adds central PBI lifecycle management, ID allocation, rendering, and validation through `scripts/backlog.py`. |
| `speckit.clarify`, `speckit.plan`, `speckit.analyze` | Adapts the upstream commands to central PBIs, research, and computed scheduling. |
| `speckit.tasks` | Reconciles TASK PBIs and renders an idempotent, wave-based execution index. |
| `speckit.implement`, `speckit.checklist`, `speckit.converge` | Adds PBI traceability and delivery guidance to the upstream commands. |
| Templates | Supplies 14 templates for project context, specifications, modular plans, research, ADRs, tasks, and the six PBI types. |

`NOTICE.md` documents template provenance and third-party licenses.

## `scripts/backlog.py` CLI

Run the CLI from the repository root, or use the installed copy shown here:

```bash
uv run --no-project --quiet --with pyyaml --with jsonschema \
  python .specify/presets/backlog/scripts/backlog.py <command> [arguments]
```

| Command | Purpose |
|---------|---------|
| `next-id <TYPE>` | Allocate the next available permanent PBI ID. |
| `locate <ID> [--descendants]` | Find a PBI, its references, affected specs, and optionally descendants. |
| `schedule` | Compute the dependency- and file-aware delivery schedule. |
| `render-index` | Rebuild the central `backlog/index.md`. |
| `render-spec <spec-dir>` | Render a specification's central backlog block. |
| `render-tasks <spec-dir>` | Reconcile the rendered task schedule and `[P]` markers. |
| `check` | Validate PBI structure, relations, links, Gherkin acceptance criteria, and generated artifacts. |
| `export-features <spec-dir> <out-dir>` | Write one Gherkin `.feature` file per user story in the spec's scope (`<out-dir>` is relative to the project root). |

The CLI emits JSON and returns a non-zero exit status when a command cannot complete or validation finds errors.

## Development

Run unit tests and try a real installation in a scratch project:

```bash
uv run --no-project --with pytest --with pyyaml --with jsonschema pytest tests
specify init /tmp/try --integration claude --extension git --preset "$PWD"
bash tests/check_install.sh /tmp/try
```

`specify init` copies the preset; after editing it, reinstall it in the scratch project to test the latest files.

### Keeping up with Spec Kit

The replaced commands derive from Spec Kit **v1.2.5** and retain upstream wording where possible. When a new version ships, compare the upstream files and port relevant hook, placeholder, and workflow changes into `commands/` and `templates/`, then update the required Spec Kit version.

## License

MIT — see `LICENSE`. Third-party material from Spec Kit and Non-Deterministic SDD is credited in `NOTICE.md`.
