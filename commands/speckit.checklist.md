## Preset `backlog` addendum

> This project uses the `backlog` preset. The rules below **refine the steps above**; where they conflict with the generic wording above, these rules win.

**What "the spec" is here** — `FEATURE_DIR/spec.md` has **4 blocks**: Header with `**Scope**:`, rendered `## Backlog` between `<!-- BEGIN BACKLOG -->` / `<!-- END BACKLOG -->`, optional Key Entities and measurable Success Criteria. Only a Clarifications session log may follow; no root PBI or duplicate requirements envelope is embedded. Permanent PBIs live in **repository-root** `backlog/{maps,epics,features,stories,spikes,tasks,bugs}/`, never below `FEATURE_DIR`. Read scoped PBIs and their FEATURE/EPIC/MAP ancestors relevant to the checklist domain. The seven types include `FEATURE`; BUG creation belongs to the bug extension. Read `plan.md` plus applicable `data-model.md`, `contracts/`, `research.md`, and `quickstart.md`; Accepted ADRs in `docs/adr/` govern durable cross-feature choices alongside `constitution.md`.

**Rules and lookup** — read `.specify/presets/backlog/knowledge/pbi-writing/rules.md` (Readable References) and `.specify/presets/backlog/knowledge/delivery/rules.md` (rank, BLOCKED_BY, disjoint TASK Files, computed waves/`[P]`, one PR/MR per US and default worktree isolation). `BACKLOG_TOOL` = `uv run --no-project --quiet --with pyyaml --with jsonschema python .specify/presets/backlog/scripts/backlog.py`. To resolve Scope references use `BACKLOG_TOOL locate <ID> --descendants`; to inspect delivery assumptions use `BACKLOG_TOOL schedule --spec FEATURE_DIR`, and to check structural quality use `BACKLOG_TOOL check --spec FEATURE_DIR`. Every operation means the full invocation from root as a standalone command, never chained with `;`, `&&`, or `|`. Do not mutate PBIs or generated indices while producing a checklist, or claim a check passed when tooling could not run.

**Requirement identifiers** — there are no `FR-###` items, and no `§` markers: the checklist is read by a person, so every traceability reference says what it points to and links to the right spot (the "Readable references" section of `.specify/presets/backlog/knowledge/pbi-writing/rules.md`). Use these references in checklist items instead of the generic ones above; the links are relative to the checklist file in `FEATURE_DIR/checklists/`:

| Generic reference above | Reference in this project |
|-------------------------|---------------------------|
| `[Spec §FR-001]` | `[US-001/AC-2 "Card declined"](../../../backlog/stories/US-001-card-payment.md#ac-2-card-declined)` — a Gherkin scenario with its title and heading link |
| A user story / user scenario | `US [US-001](../../../backlog/stories/US-001-card-payment.md) Card payment` — the permanent central story |
| A bounded capability | `FEATURE [FEATURE-001](../../../backlog/features/FEATURE-001-card-payment.md) Card payment` — the parent Feature's Outcome and Constraints |
| `[Spec §SC-001]` | `[SC-001 "First purchase in under 3 minutes"](../spec.md#measurable-outcomes)` — a Success Criterion with its short name |
| Edge cases section | the scenarios of the affected story, or `[Gap]` when missing |
| Non-functional section | `[the card payment Constraints](../../../backlog/features/FEATURE-001-card-payment.md#constraints)` or the relevant named constitution rule; do not invent a spec section |
| Scope / exclusions | `[the Out of Scope of US-001 "Card payment"](../../../backlog/stories/US-001-card-payment.md#out-of-scope)`, `[the Out of Scope of FEATURE-001 "Card payment"](../../../backlog/features/FEATURE-001-card-payment.md#out-of-scope)`, `[the Scope Boundaries of EPIC-001 "Checkout"](../../../backlog/epics/EPIC-001-checkout.md#scope-boundaries)` |
| Terminology | `[the Ubiquitous Language of the product](../../../.specify/memory/product.md#ubiquitous-language)` |

The quality-dimension and gap markers of the generic text above (`[Completeness]`, `[Clarity]`, `[Consistency]`, `[Gap]`, `[Ambiguity]`, …) stay as they are: they are words, not references. Before saving the checklist, run the self-check of the "Readable references" section on its items.

**Additional quality dimensions** worth checking in this project (as requirements-quality questions, never as implementation tests):

- Are personas in the Connextra sentences defined in product.md's Personas? [Consistency]
- Do asynchronous operations specify the full cycle (trigger, loading, outcome, error, retry)? [Completeness]
- Are the Out of Scope boundaries of neighbouring stories consistent with each other? [Consistency]
- Are Ubiquitous Language terms used consistently across PBIs? [Consistency]
- Does each Feature describe one Outcome with cross-story Constraints, distinct from Gherkin scenarios and constitution policy? [Clarity]
- Are dependency/rank constraints explicit enough to derive wave-based `[P]` scheduling and one-PR-per-US isolation without manual schedule assumptions? [Completeness]

The built-in `checklists/requirements.md` is maintained by `__SPECKIT_COMMAND_SPECIFY__` and `__SPECKIT_COMMAND_CLARIFY__`: do not overwrite it with a domain checklist.
