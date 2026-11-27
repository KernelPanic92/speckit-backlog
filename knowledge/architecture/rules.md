# Architecture and Research Rules

## Artifact Boundaries

Keep evidence, durable decisions, and execution design separate:

- `specs/NNN-slug/research.md` is feature-scoped empirical research and option evaluation: facts, constraints, benchmarks, Spike findings, and trade-offs. Do not silently bury durable project-wide governance in a feature folder.
- `docs/architecture/adr/NNNN-slug.md` records one durable, project-wide architectural decision and why it was made.
- `specs/NNN-slug/plan.md`, `data-model.md`, `contracts/`, and `quickstart.md` describe how to execute the feature. Keep them modular and aligned with upstream Spec Kit `AVAILABLE_DOCS`, enabling progressive disclosure for reviewers and parallel sub-agents. Do not create a separate `docs/tdd/TDD-*.md`: this modular spec folder is the execution design.

## Research Modes

Record questions and evidence in `research.md`; do not create process theater.

- **Fact-finding (default):** use when `constitution.md` and existing ADRs settle the architecture. Concisely verify library versions, API limits, codebase conventions, and desk-research Spikes. Do not invent 3–4 architectural alternatives for routine features.
- **Trade-off:** use only for genuine architectural forks, new subsystems, storage/protocol/boundary choices, or architectural Spikes. Apply the analysis below.

### Trade-off Analysis

1. **Expose latent gaps.** Check scale (RPS/volume), latency/SLOs, team and stack constraints, and compliance. Ask one targeted user question only when a missing variable could flip the verdict. Otherwise state the assumption and what changes if it is false.
2. **Compare 3–4 distinct options.** Include “extend existing / status quo” where meaningful; cosmetic variants are not distinct options.
3. **Stress-test and compare.** The decision matrix covers latency, 10x scalability/bottleneck, failure mode/blast radius, operability, developer velocity at 6/18 months, security, lock-in, and effort as `Xh @ Y% risk` (never bare hours). Name each option's **Poison Pill**: its structural flaw accepted if chosen.
4. **Give one verdict.** Name one recommendation, explain why it beats the runner-up, and state the assumption that would flip the verdict and the expected alternative. “It depends” without that variable and changed verdict is not a recommendation.

Put the matrix, stress test, and verdict in `research.md`. Link the feature research from an ADR when the evaluation yields a durable project-wide decision.

## ADR Lifecycle

Create an ADR only when a feature introduces or changes a durable, cross-feature architectural, technology, protocol, data-boundary, or pattern choice not already governed by `constitution.md` or an existing ADR. Do not record local implementation details as ADRs.

- **Discovery and numbering:** search `docs/architecture/adr/` first; if absent, search `docs/decisions/`, `doc/adr/`, then `adr/`. Default new records to `docs/architecture/adr/`. Use continuous four-digit numbering (`0001`, `0002`, …) and `NNNN-kebab-slug.md` names of at most six words.
- **Atomicity and title:** one decision per ADR. If the title needs “and”, split it. Use a decision verb, such as “Adopt X for Y” or “Use X instead of Y”.
- **Trade-offs:** keep an ADR concise (at most two pages). List 2–4 options in 2–4 lines each and link to `research.md` for the full matrix and stress tests. Include at least two concrete negative consequences and neutral re-evaluation triggers.
- **Statuses:** `Proposed`, `Accepted`, `Rejected`, `Deprecated`, or `Superseded by [ADR-NNNN: title](NNNN-slug.md)`.
- **Immutability:** never rewrite an `Accepted` ADR body. To reverse or replace it, create a new ADR with `Supersedes: [ADR-MMMM: title](MMMM-slug.md)` and edit only the `Status` row of the superseded ADR.

## Delta-Only Execution Design

Use tables and bullets over prose. Define no standard terms. Omit document versions, dates, authors, and changelogs: Git owns history; ADRs carry lifecycle status, not revision logs.

Never repeat `constitution.md` or `docs/architecture/adr/` in `plan.md`, `data-model.md`, `contracts/`, or `quickstart.md`. Omit generic security, logging, and testing boilerplate. Document only feature-specific deltas, such as idempotency keys, network-boundary retry/backpressure, migration reversibility, and an explicit point of no return.

- **`plan.md` (~80–130 lines):** Summary, Technical Context, Constitution Check, Architecture & Project Structure, Delivery Slices, and Complexity Tracking only when there are violations.
- **`data-model.md` (only when entities or state are added or changed):** Ubiquitous Language entities, fields, validation rules from `AC-n`, relationships, state transitions, indexes, and migration strategy.
- **`contracts/` (only when external interfaces are exposed or changed):** one file per boundary/slice, using OpenAPI, `.proto`, `.graphql`, JSON Schema, or a CLI/UI schema. This lets sub-agents load only the relevant contract.
- **`quickstart.md` (~20–40 lines):** runnable verification runbook with prerequisites/environment, the exact Gherkin acceptance-test command, and 1–2 smoke commands linked to stories/contracts. Do not duplicate Gherkin scenarios.

## Readable References

Every reference must tell a reader what it is and land at the relevant source. Link to the named topic and heading, for example `[ADR-0001: Adopt Stripe PaymentIntents](../../docs/architecture/adr/0001-stripe-payment-intents.md)` or `[the Order entity](data-model.md#order)`. For local sections, use the actual heading anchor. Avoid bare IDs, paths, URLs, invented abbreviations, and section numbers without titles. Apply the full [Readable references rules](../pbi-writing/rules.md#readable-references) throughout these artifacts.
