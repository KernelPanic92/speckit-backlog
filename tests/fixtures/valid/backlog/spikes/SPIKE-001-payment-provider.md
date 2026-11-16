---
id: SPIKE-001
title: Payment provider
type: SPIKE
rank: 10
relations:
  US-002:
    title: Pay by card
    type: US
    relationType: PARENT
    reason: The provider investigation serves the first card payment story.
---

## Outcome

Does the provider support idempotent authorization and deterministic decline handling?

## Timebox

One working day.

## Expected Output

A written decision with sandbox evidence for success and decline behavior.

## Exit Criteria

- [ ] Record sandbox results for authorization retries and declines.

## Out of Scope

- Production payment code: US [US-002] Pay by card.
