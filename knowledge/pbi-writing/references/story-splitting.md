---
name: story-splitting
description: >-
  Read when a story is too big and the heuristics of the "Scope and splitting" constraints in `../rules.md` are not enough, or when you need to fill in "Split pattern" in the Micro-Scope: Lawrence's 9 patterns with examples, the meta-pattern and the two checks to choose the winning split.
source: https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/
---

# Splitting User Stories

Operational guide for dividing user stories that are too big into smaller pieces while preserving value. Based on the guide by Richard Lawrence / Humanizing Work.

## Fundamental principle: VERTICAL slice, not horizontal

A user story must be a **vertical slice**: a change in the system's behavior that brings value visible to the user and that, as a rule, crosses several architectural layers (UI, logic, data) all together.

- **Vertical slice (right):** "The user can search for a flight on an exact date." It touches front-end, backend and DB, but it is demonstrable and releasable.
- **Horizontal slice (wrong):** "Build the DB table", "make the API endpoint", "make the UI". Small pieces, but NOT independent and WITHOUT observable value on their own.

Why vertical:
- It makes value explicit in the backlog and enables conversations about real value.
- It reduces accidental low-value work (80/20: most of the value lies in a few features).
- Faster feedback cycles and greater predictability through working software.

> Splitting by architectural layer satisfies the INVEST "Small" criterion but violates "Independent" and "Valuable". Avoid it.

## The 9 splitting patterns

The guide lists **nine patterns** (plus a meta-pattern). Try more than one on the same story: often one fits better than the others. They are ordered roughly from most useful to least useful.

### 1. Workflow Steps
A story that covers an entire workflow can be split into the individual steps the user performs. Build the core step end-to-end first (even with shortcuts on the others), then add the other steps as separate stories.
*Example:* publishing an article → first "publish directly", then add editorial review, staging preview, etc.

### 2. Business Rule Variations
A story often hides several business rules. Extract them as distinct stories: first the base rule, then the variants.
*Example:* flight search → base version, then "max stops", "nearby airports", "flexible dates".

### 3. Major Effort
Sometimes a story is big only because of one part. Do that part first, the one that establishes the infrastructure/the bulk of the work; the following stories that leverage it become much cheaper.
*Example:* credit card payment → the first card requires the whole integration; adding the second and third card networks are small stories.

### 4. Simple/Complex
When many complications pop up while discussing the story, ask yourself: "what is the simplest version that can work?" Implement the simple core now, defer the complications as separate stories.

### 5. Variations in Data
The complexity is driven by the variety of the data. Start from the simplest subset/structure and add variants just-in-time.
*Example:* geographic search → first regions, then cities, then neighborhoods. Or localization: first one language, then the others.

### 6. Data Entry Methods
The complexity lies in the input interface, not in the core behavior. First the simplest possible input, then the refined variants.
*Example:* date entry → first a plain text field, then a calendar date-picker as a separate story.

### 7. Defer Performance
"First make it work, then make it fast." A first story makes the feature work correctly but slowly; a later story optimizes it.
*Example:* working "product search", then "product search < 100ms".

### 8. Operations (e.g. CRUD)
Split by the operations performed on an entity: Create, Read, Update, Delete (and variants such as sort/filter). Each operation is a story.

### 9. Break Out a Spike
**Last resort.** When the solution is so unknown that you cannot even estimate it, separate a time-boxed research/investigation story from the implementation story.
*Example:* "Investigate the integration with the payment gateway" (AC = questions that have been answered) + "Implement card payment".

> **Meta-pattern — "Find the Complexity & Reduce the Variations":** find where the complexity really lies (human behavior, new integrations, unknowns) and list all its variations; every split comes from reducing those variations to a complete slice that crosses the core of the complexity.

> Note: the acronym **SPIDR** (Spike, Paths, Interface, Data, Rules) is a related but distinct model, by **Mike Cohn**, not from this guide. It is a more compact mnemonic that covers a subset of the same cuts.

## Decision flow to choose the split

### Step 1 — Prepare the input story
- Verify that the story respects INVEST (except the "Small" criterion, which is what we want to fix).
- **Value check:** is it really a story with value? Tasks or components are not stories and cannot be split into value. Merge the non-stories until together they represent value.
- Ask: "Is the slice too big?" If yes, proceed with the split.

### Step 2 — Apply the patterns
Go through the nine patterns and try to generate several alternative splits for the same story, starting from the meta-pattern (find the core complexity, list the variants, reduce to a complete slice).

### Step 3 — Choose the winning split with TWO checks

**Check 1 — Is the split VALID (does it reveal value that can be eliminated)?**
Choose the split that lets you **deprioritize or throw away** one of the resulting stories. A good split surfaces low-value functionality you can eliminate (80/20 principle). If all the splits hide the waste in the same way, change pattern.

**Check 2 — Are the pieces ROUGHLY EQUAL in size?**
Choose the split that produces more small stories of similar size. Four 2-point stories are better than one 5-point and one 3-point story: more independent prioritization options for the Product Owner and lower estimation variance → greater predictability.

## The two key checks on every piece

1. **Does every piece bring visible value?** Every story must add an increment of value observable by the user. For Lawrence it does not have to be releasable on its own, but several stories accumulate into a Minimum Marketable Feature (MMF). If a piece does not move the needle for the user, it is not a story. (*Choice of our rules, stricter:* every story must be deployable and usable on its own, see `../rules.md`, constraint (I) Independent in "I.N.V.E.S.T. constraints" and "Releasability" in "Scope and splitting". The MMF concession does NOT apply: a form without submission or a drag without saving are not stories, even if the MMF would complete them.)
2. **Are the pieces roughly equal in size and small?** Rule of thumb: when a story reaches the top of the backlog, 6-10 of them should fit in a sprint. Similar sizes reduce estimation variance and increase predictability.

## Notes on context (Cynefin)

- **Obvious / Complicated:** find all the stories; prioritize the valuable and risky ones first.
- **Complex:** find one or two stories that deliver value AND learning; use the results to discover the others. Do not simulate predictability by listing all the stories.
- **Chaotic:** splitting is secondary; handle the crisis first.

## Operational summary

1. Start from a story with real value (vertical slice).
2. If it is too big, apply the 9 patterns (Spike as last resort).
3. Generate several splits, then choose the one that (a) lets you throw something away and (b) produces small, similar pieces.
4. Verify that each piece brings visible value and that 6-10 of them fit in a sprint.
