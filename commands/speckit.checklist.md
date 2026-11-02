## Preset `backlog` addendum

> This project uses the `backlog` preset. The rules below **refine the steps above**; where they conflict with the generic wording above, these rules win.

**What "the spec" is here** — `spec.md` is the root PBI (MAP, EPIC or US) followed by the spec envelope (Spec Context, Backlog Index, Success Criteria, Key Entities, NFR, External Dependencies, Security & Compliance Checklist, Open Questions, Clarifications); every child PBI lives in its own file under `FEATURE_DIR/backlog/`. Read the root PBI, the envelope and the child PBIs relevant to the checklist's domain.

**Requirement identifiers** — there are no `FR-###` items. Use these references in checklist items instead:

| Generic reference above | Reference in this project |
|-------------------------|---------------------------|
| `[Spec §FR-001]` | `[US-001/AC-2]` — a Gherkin scenario of a story |
| A user story / user scenario | `[US-001]` — the story file in `backlog/stories/` |
| `[Spec §SC-001]` | `[Spec §SC-001]` — Success Criteria of the envelope (unchanged) |
| Edge cases section | the scenarios of the affected story, or `[Gap]` when missing |
| Non-functional section | `[Spec §NFR]` — Non-Functional Requirements of the envelope |
| Scope / exclusions | `[US-001 §Out of Scope]`, `[EPIC-001 §Scope Boundaries]` |
| Terminology | `[Product §Ubiquitous Language]` — `.specify/memory/product.md` |

**Additional quality dimensions** worth checking in this project (as requirements-quality questions, never as implementation tests):

- Are personas in the Connextra sentences defined in product.md's Personas? [Consistency]
- Do asynchronous operations specify the full cycle (trigger, loading, outcome, error, retry)? [Completeness]
- Are the Out of Scope boundaries of neighbouring stories consistent with each other? [Consistency]
- Are Ubiquitous Language terms used consistently across PBIs? [Consistency]

The built-in `checklists/requirements.md` is maintained by `__SPECKIT_COMMAND_SPECIFY__` and `__SPECKIT_COMMAND_CLARIFY__`: do not overwrite it with a domain checklist.
