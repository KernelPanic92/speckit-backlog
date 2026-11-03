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
| Delivery Conventions | N |
| Removed: Version, Ratified / Effective Date, Last Amended, Approved By, Amendment History / Changelog | — |

### product-template.md
| Section | From |
|---------|------|
| All (Vision, Problem, Personas, Goals, Scope, Key User Journeys, Constraints, Stakeholders, Ubiquitous Language, Open Questions) | N (Ubiquitous Language table: Term / Business definition / Dev definition) |

### spec-template.md (spec envelope)
| Section | From |
|---------|------|
| Spec Context (Input line), Success Criteria (`SC-###`), Key Entities | U |
| Non-Functional Requirements, External Dependencies, Security & Compliance Checklist, Open Questions, References | P |
| Backlog Index, Clarifications log format | N / U (clarify's session log) |
| Root PBI (MAP / EPIC / US) that precedes the envelope | N |
| Removed: Summary / Key decisions, FR-###, Edge Cases (replaced by Gherkin scenarios), Feature ID / Created / Author | — |

### plan-template.md
| Section | From |
|---------|------|
| Technical Context (`NEEDS CLARIFICATION`), Constitution Check gate, Project Structure + Structure Decision, Complexity Tracking | U |
| Summary + Key technical decisions, New Dependencies, Architecture Overview, Data Model, API Design, Integration Points, Security, Performance, Error Handling, Observability, Testing Strategy, Migration Plan + Feature Flags, Patterns Established, Open Technical Questions, References | P |
| Delivery Slices, Gherkin scenarios as validation scenarios (instead of quickstart.md), links to PBIs | N |
| Removed: Created, Author | — |

### research-template.md
| Section | From |
|---------|------|
| Decisions in the Decision / Rationale / Alternatives considered format | U (plan command, Phase 0) |
| Research Questions, Key Findings, Version Information, Migration Notes, Performance / Security Considerations, Open Questions | P |
| Validity (refresh trigger tied to library versions) | P "Staleness Warning", without dates |
| Spike closure, question sources | N |
| Removed: Last Updated, Author, Next Review, Changelog | — |

### tasks-template.md
| Section | From |
|---------|------|
| Checkbox line format, phases with Goal / Independent Test / Checkpoint, Phase Dependencies, Parallel Example, Implementation Strategy | U |
| Summary, Task Completion Criteria, Dependency Graph, Risk Assessment, Traceability Matrix | P |
| TASK PBI files linked from each line, phases by spec mode (Walking Skeleton, Release Lanes), AC coverage | N |
| Removed: Created, Author | — |

### design-template.md
| Section | From |
|---------|------|
| Front matter token groups, the eight canonical sections and their order | DESIGN.md format (Google Labs, alpha) |
| Extension sections (Responsive Behavior, Motion, Accessibility, Sources & Sync, Known Gaps), guidance | N |

### sync-clickup-template.md, sync-multica-template.md
| Section | From |
|---------|------|
| All (settings, item and hierarchy mapping, relations, description, references, pull) | N |

### pbi-*-template.md
| Template | From |
|----------|------|
| pbi-map, pbi-epic, pbi-story, pbi-task, pbi-spike | N; task Files from P's tasks template |

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
