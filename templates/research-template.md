# Research: [FEATURE]

**Spec**: [[Feature name] specification](spec.md) | **Plan**: [[Feature name] implementation plan](plan.md) | **ADRs**: [crystallized decisions as [ADR-NNNN: title](../../docs/architecture/adr/...) or none]

<!-- Git owns history; do not add dates, authors, versions, or changelogs for this document. Follow the [Readable references rules](../../knowledge/pbi-writing/rules.md#readable-references). -->

## Questions & Scope

| Question | Mode | Source | Outcome |
|----------|------|--------|---------|
| [Question] | Fact-finding / Trade-off | [Technical Context](plan.md#technical-context) or SPIKE [id](../../backlog/spikes/...) title | [Finding](research.md#topic) and [ADR-NNNN: title](../../docs/architecture/adr/NNNN-slug.md), if applicable |

## Technical Findings

<!-- Fact-finding questions and desk-research Spikes: concise empirical facts, constraints, versions, and evidence. No prose padding. -->

### [Topic]

- **Finding**: [verified fact or result]
- **Constraint / version**: [bound, compatibility, or version]
- **Evidence**: [named source and link]
- **Implication**: [effect on this feature]

## Architectural Trade-offs *(include only for genuine Trade-off forks; omit when existing stack and ADRs settle the design)*

### [Topic]

#### Assumptions & Latent Gaps

| Assumption / Constraint | Type | What changes if false |
|-------------------------|------|-----------------------|
| [scale, latency/SLO, team/stack, compliance, or other input] | [known / assumption / open] | [verdict or option change] |

#### Decision Matrix

| Driver | [Option 1: status quo, if meaningful] | [Option 2] | [Option 3] |
|--------|--------------------------------------|------------|------------|
| Latency / 10x scale | [evidence and bottleneck] | [comparison] | [comparison] |
| Failure mode / blast radius | [comparison] | [comparison] | [comparison] |
| Operability / developer velocity (6/18m) | [comparison] | [comparison] | [comparison] |
| Security / lock-in | [comparison] | [comparison] | [comparison] |
| **Effort** | [Xh @ Y% risk] | [Xh @ Y% risk] | [Xh @ Y% risk] |
| **Poison pill** | [structural flaw accepted] | [structural flaw accepted] | [structural flaw accepted] |

#### Options, Stress Test & Poison Pills

- **[Option 1]** — 10x bottleneck: [limit]; failure mode: [impact]; velocity: [6/18-month effect]. **Poison pill**: [structural flaw accepted].
- **[Option 2]** — 10x bottleneck: [limit]; failure mode: [impact]; velocity: [6/18-month effect]. **Poison pill**: [structural flaw accepted].
- **[Option 3]** — 10x bottleneck: [limit]; failure mode: [impact]; velocity: [6/18-month effect]. **Poison pill**: [structural flaw accepted].

#### Verdict

**Choose [one option].** [Explain why it beats the runner-up and name the assumption that would flip the verdict and the expected alternative.] For a durable project-wide choice, record [ADR-NNNN: title](../../docs/architecture/adr/NNNN-slug.md).

## Validity & Refresh Triggers

| Dependency / Assumption | Current Version / Bound | Refresh Trigger |
|-------------------------|-------------------------|-----------------|
| [dependency, API, or assumption] | [verified version, limit, or bound] | [specific change or threshold] |
