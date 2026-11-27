# Notice and provenance

speckit-backlog is MIT-licensed (see `LICENSE`). It contains material derived from two MIT-licensed projects. This file must travel with every copy of the preset, including the copy installed in `.specify/presets/backlog/`.

## Sources

| Source | License | Used for |
|--------|---------|----------|
| [github/spec-kit](https://github.com/github/spec-kit) v1.2.5 — Copyright GitHub, Inc. | MIT | Command files (structure, wording, hook sections kept verbatim), plan/tasks/spec/constitution template structure |
| [popoloni/non-deterministic-sdd](https://github.com/popoloni/non-deterministic-sdd) — Copyright (c) 2026 Enrico Papalini, companion of the book *Non-Deterministic Spec-Driven Development* | MIT | Constitution, plan, research, tasks and spec template sections |
| [google-labs-code/design.md](https://github.com/google-labs-code/design.md) — DESIGN.md format, spec version alpha | Apache-2.0 | Structure followed by `design-template.md` (front matter token groups, section names and order). No text of the specification is copied |

## Provenance per template

Legend: **U** = Spec Kit v1.2.5, **P** = Papalini, **N** = new in this preset.

### constitution-template.md
| Section | From |
|---------|------|
| Title, Core Principles (placeholder convention `[ALL_CAPS]`) | U |
| Project Identity, Technology Stack, Three-Tier Rules (MUST/SHOULD/MAY), Quality Standards, Security Posture + Compliance, Exceptions Process, Review Schedule | P (constitution-template.md) |
| Agent Boundaries (Always / Ask First / Never), Performance Baselines | P (memory/constitution.md) |
| Governance | U, without versioning policy |
| Delivery Conventions (Acceptance tests from Gherkin, Story isolation, Readable references) | N |
| Removed: Version, Ratified / Effective Date, Last Amended, Approved By, Amendment History / Changelog | — |

### product-template.md
| Section | From |
|---------|------|
| All (Vision, Problem, Personas, Goals, Scope, Key User Journeys, Constraints, Stakeholders, Ubiquitous Language) | N (Ubiquitous Language table: Term / Business definition / Dev definition) |

### spec-template.md (four-block specification)
| Section | From |
|---------|------|
| Header (Feature Specification, Feature Branch, Status, Input), Key Entities, Success Criteria (`SC-###`) | U (derived from Spec Kit's specification structure) |
| Scope selector and `## Backlog` block rendered from the central `backlog/` | N |
| Removed: FR-###, Edge Cases (represented in PBIs), Open Questions, Feature ID / Created / Author | — |

### plan-template.md
| Section | From |
|---------|------|
| Technical Context (`NEEDS CLARIFICATION`), Constitution Check gate, Project Structure + Structure Decision, Complexity Tracking | U |
| Summary, modular architecture & project structure, feature-specific resilience/migration/rollout deltas | N |
| Delivery Slices aligned to the deterministic `render-tasks` wave schedule; conditional `data-model.md`, `contracts/`, and `quickstart.md`; links to PBIs and ADRs | N |
| Removed: the 18-section single-file monolith, including embedded data model/contracts/operations boilerplate; modular upstream-compatible artifacts support progressive disclosure | N |
| Removed: Created, Author | — |

### research-template.md
| Section | From |
|---------|------|
| Feature-scoped empirical findings, questions, validity/refresh triggers, and conditional TDD trade-off matrix with stress tests and poison pills | N |
| Separation of empirical research and architectural evaluation from durable atomic ADRs in `docs/architecture/adr/` | N |
| Removed: decisions-as-ADR substitutes, routine-feature alternative theater, dates, authors, and changelogs | N |

### adr-template.md
| Section | From |
|---------|------|
| Context, decision drivers, considered options, decision, consequences, validation | N (MADR/Nygard-style atomic project-wide decision record) |
| Status, supersession, mandatory concrete negative trade-offs, no dates/authors | N |

### tasks-template.md
| Section | From |
|---------|------|
| Checkbox line format, phases with Goal / Independent Test / Checkpoint, Phase Dependencies, Parallel Example, Implementation Strategy | U |
| Summary, Task Completion Criteria, Dependency Graph, Risk Assessment, Traceability Matrix | P |
| TASK PBI files linked from each line, phases by spec scope (Walking Skeleton, Release Lanes), AC coverage, deterministic `render-tasks` wave schedule and computed `[P]` markers | N |
| Removed: Created, Author | — |

### design-template.md
| Section | From |
|---------|------|
| Front matter token groups, the eight canonical sections and their order | DESIGN.md format (Google Labs, alpha) |
| Extension sections (Responsive Behavior, Motion, Accessibility, Sources & Sync, Known Gaps), guidance | N |

### PBI templates
| Template | From |
|----------|------|
| `pbi-map-template.md` | N |
| `pbi-epic-template.md` | N |
| `pbi-feature-template.md` | N |
| `pbi-story-template.md` | N |
| `pbi-task-template.md` | N; task Files from P's tasks template |
| `pbi-spike-template.md` | N |

## Spec Kit license

```text
MIT License

Copyright GitHub, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Non-Deterministic SDD license

```text
MIT License

Copyright (c) 2026 Enrico Papalini

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
