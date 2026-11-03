# Research: [FEATURE]

**Plan**: [[Feature] implementation plan](plan.md) | **Spec**: [[Feature] specification](spec.md)

**Purpose**: [Why this research was needed: the unknowns of the Technical Context and the Spikes of the backlog]

<!-- History of this document is git history: no "last updated", author or changelog fields.
     References follow the "Readable references" rules of the backlog preset: questions and decisions are named by their topic, never numbered ("R1"), so that the plan, the tasks and the Spikes can link them as [the payment provider decision](research.md#payment-provider). -->

## Research Questions

<!-- One line per question. Sources: every NEEDS CLARIFICATION in the plan's Technical Context, every SPIKE in backlog/spikes/, every best-practice question for a chosen dependency. The Decision column links the block below by its heading. -->

| Question | Source | Decision |
|----------|--------|----------|
| [Question?] | [Storage, marked NEEDS CLARIFICATION in the Technical Context of the plan](plan.md#technical-context) | [[Topic]](#topic) |
| [Question?] | [SPIKE [SPIKE-001] Title](backlog/spikes/SPIKE-001-[slug].md) | [[Topic]](#topic) |

## Decisions

<!-- The core of this document: one block per question, in the upstream Decision / Rationale / Alternatives format. -->

### [Topic]

- **Decision**: [what was chosen]
- **Rationale**: [why chosen]
- **Alternatives considered**: [what else was evaluated and why it was rejected]
- **Spike closed**: [[SPIKE [SPIKE-001] Title](backlog/spikes/SPIKE-001-[slug].md) — Exit Criteria met | n/a]

## Key Findings

### Finding 1: [Title]

**Summary:** [One sentence]

**Details:** [Explanation with context]

**Code Example:**
```text
// Example demonstrating the finding
```

**Source:** [[What the source is, in words](URL of the page or section)]

**Implications for this feature:**
- [How this affects the plan]

## Version Information

<!-- Versions of the libraries and services this research is based on (not versions of this document). -->

| Component | Version | Release Date | EOL Date |
|-----------|---------|--------------|----------|
| [Library/Framework] | [X.Y.Z] | [Date] | [Date or N/A] |

**Compatibility notes:**
- [Framework X]: compatible with versions [range]
- [Known conflicts]: [list]

## Migration Notes *(if applicable)*

| Change | Old Approach | New Approach |
|--------|--------------|--------------|
| [Change 1] | [Old pattern] | [New pattern] |

## Performance Considerations *(if applicable)*

| Scenario | Benchmark | Notes |
|----------|-----------|-------|
| [Scenario] | [X ms/ops] | [Context] |

## Security Considerations *(if applicable)*

- [ ] [Security concern]: [Mitigation]

## Open Questions

- [ ] [Question needing resolution] — owner: [who]

## Validity

<!-- When this research must be re-checked. Tie it to library versions and events, not to dates: the date of the research is in git history. -->

This research is valid for the versions listed in Version Information.

**Refresh trigger**: [e.g., "next major version of [library]", "before choosing a new payment provider"]

Before relying on it:
- [ ] Check whether the library versions have changed significantly
- [ ] Review the changelogs for breaking changes since those versions
- [ ] Verify the code examples still work
