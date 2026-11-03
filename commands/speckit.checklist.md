## Preset `backlog` addendum

> This project uses the `backlog` preset. The rules below **refine the steps above**; where they conflict with the generic wording above, these rules win.

**What "the spec" is here** — `spec.md` is the root PBI (MAP, EPIC or US) followed by the spec envelope (Spec Context, Backlog Index, Success Criteria, Key Entities, NFR, External Dependencies, Security & Compliance Checklist, Open Questions, Clarifications); every child PBI lives in its own file under `FEATURE_DIR/backlog/`. Read the root PBI, the envelope and the child PBIs relevant to the checklist's domain.

**Requirement identifiers** — there are no `FR-###` items, and no `§` markers: the checklist is read by a person, so every traceability reference says what it points to and links to the right spot (the "Readable references" section of `.specify/presets/backlog/knowledge/user-story-writer/rules.md`). Use these references in checklist items instead of the generic ones above; the links are relative to the checklist file in `FEATURE_DIR/checklists/`:

| Generic reference above | Reference in this project |
|-------------------------|---------------------------|
| `[Spec §FR-001]` | `[US-001/AC-2 "Card declined"](../backlog/stories/US-001-card-payment.md#ac-2-card-declined)` — a Gherkin scenario: its id, its title, a link to its heading |
| A user story / user scenario | `[US [US-001] Card payment](../backlog/stories/US-001-card-payment.md)` — the story file in `backlog/stories/` |
| `[Spec §SC-001]` | `[SC-001 "First purchase in under 3 minutes"](../spec.md#measurable-outcomes)` — a Success Criterion of the envelope, with its short name |
| Edge cases section | the scenarios of the affected story, or `[Gap]` when missing |
| Non-functional section | `[the Non-Functional Requirements of the spec](../spec.md#non-functional-requirements)` — anchor taken from the heading as it is written in spec.md |
| Scope / exclusions | `[the Out of Scope of US-001 "Card payment"](../backlog/stories/US-001-card-payment.md#out-of-scope)`, `[the Scope Boundaries of EPIC-001 "Checkout"](../backlog/epics/EPIC-001-checkout.md#scope-boundaries)` |
| Terminology | `[the Ubiquitous Language of the product](../../../.specify/memory/product.md#ubiquitous-language)` |

The quality-dimension and gap markers of the generic text above (`[Completeness]`, `[Clarity]`, `[Consistency]`, `[Gap]`, `[Ambiguity]`, …) stay as they are: they are words, not references. Before saving the checklist, run the self-check of the "Readable references" section on its items.

**Additional quality dimensions** worth checking in this project (as requirements-quality questions, never as implementation tests):

- Are personas in the Connextra sentences defined in product.md's Personas? [Consistency]
- Do asynchronous operations specify the full cycle (trigger, loading, outcome, error, retry)? [Completeness]
- Are the Out of Scope boundaries of neighbouring stories consistent with each other? [Consistency]
- Are Ubiquitous Language terms used consistently across PBIs? [Consistency]

The built-in `checklists/requirements.md` is maintained by `__SPECKIT_COMMAND_SPECIFY__` and `__SPECKIT_COMMAND_CLARIFY__`: do not overwrite it with a domain checklist.
