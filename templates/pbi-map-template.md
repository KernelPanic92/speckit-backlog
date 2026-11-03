---
# id: the next free project-wide id from the validator (e.g. MAP-001); it never changes. Tool ids are added in `external` by /speckit.sync
id: {{id}}
title: {{title}}
# PBI type, fixed for this template
type: MAP
# optional. The Backbone Epics declare THIS map as their PARENT, not the other way round. The map has a PARENT only in the "zoom" case: the macro-Epic this map breaks down
# BLOCKED_BY: the referenced PBI blocks this one | PARENT: the referenced PBI is the parent, at most one | RELATED: link without constraints
relations:
    "{{related id}}":
        title: "{{PBI title}}"
        type: US|TASK|BUG|EPIC|SPIKE|MAP
        relationType: BLOCKED_BY|PARENT|RELATED
        reason: "{{reason for the relation}}"
# optional: a photo of the whiteboard, the Miro or Figma board of the map. Only links really supplied by the user
media:
    "{{attachment name}}":
        url: {{attachment}}
        description: "{{description}}"
---

As a {{Persona}}, I want {{Global Goal}}, so that {{Value}}.

## Outcome

{{Elevator Pitch description}}

## Backbone
*The user's narrative flow from left to right, in time order. It is made of Macro-Activities (phases) and User Tasks (the specific steps). Every Macro-Activity is an Epic, written with the `pbi-epic-template` template and with this map as PARENT: reference it as `EPIC [id] title`. The User Tasks are the sticky notes that are candidates to become User Stories, children of that Epic.*

| Macro-Activities (Epics) | 1. EPIC [{{related id}}] {{title}} | 2. EPIC [{{related id}}] {{title}} | 3. EPIC [{{related id}}] {{title}} |
|:---|:---|:---|:---|
| **User Tasks (Actions)** | - {{user task}}<br>- {{user task}} | - {{user task}}<br>- {{user task}} | - {{user task}}<br>- {{user task}} |

<!--
Example
| Macro-Activities (Epics) | 1. EPIC [EPIC-001] Discovery | 2. EPIC [EPIC-002] Selection | 3. EPIC [EPIC-003] Checkout | 4. EPIC [EPIC-004] After-Sales |
|:---|:---|:---|:---|:---|
| **User Tasks (Actions)** | - Search for a product<br>- Browse categories | - See details<br>- Add to cart | - Enter shipping details<br>- Pay | - Receive confirmation<br>- Track order |
-->

## Walking Skeleton
*The thinnest possible end-to-end path. It often has no commercial value, but it lets the technical team test the architecture, database, APIs and deploy pipeline from start to finish. The items are not user stories: they are TASK (or SPIKE) PBIs, written with `pbi-task-template` / `pbi-spike-template`, with the Epic of their Macro-Activity as PARENT, and they are not subject to the INVEST and phantom-UI constraints of US. In spec-kit they become the "Walking Skeleton" phase of tasks.md.*

- [ ] **{{type}} [{{related id}}] {{title}}:** {{reason}}
- [ ] **{{type}} [{{related id}}] {{title}}:** {{reason}}
- [ ] **{{type}} [{{related id}}] {{title}}:** {{reason}}
- [ ] **{{type}} [{{related id}}] {{title}}:** {{reason}}

<!--
Example
- [ ] **SPIKE [SPIKE-001] Search:** Show a static list of 3 products from the DB
- [ ] **TASK [TASK-001] Selection:** "Buy" button that stores a record in the session
- [ ] **TASK [TASK-002] Checkout:** Fake form that prints "Success" on screen
- [ ] **TASK [TASK-003] After-sales:** Send a plain-text log email
-->

## Release Lanes
*The horizontal "slices" that cut the tasks vertically. Each lane is a working increment of value and is titled with the Outcome it unlocks (the business goal or user behaviour), never with a sterile label such as "Release 1", "MVP" or "v1.0": the title is the filter that decides what enters the lane. The description line says in one sentence what the user gets and which slicing pattern drew the line. Each item references a PBI in the format `{{type}} [{{related id}}] {{title}}`. Each lane takes stories from every Epic of the Backbone, in Backbone order: lanes slice the Epics, an Epic is never completed before starting the next one. Within each Epic the items are in priority order: the first is the most necessary, the last is the first to cut. Never two items with the same priority (gravity rule). In spec-kit each lane becomes one phase of tasks.md, the first lane being the MVP.*

### Release n: {{title}}
[description]
* **Goal:** [E.g. Enable the first purchase by credit card]
* **Metrics:** [E.g. 10 transactions completed without errors]
* **1. EPIC [{{related id}}] {{title}}**
  * {{type}} [{{related id}}] {{title}}
  * {{type}} [{{related id}}] {{title}}
* **2. EPIC [{{related id}}] {{title}}**
  * {{type}} [{{related id}}] {{title}}
  * {{type}} [{{related id}}] {{title}}
* **3. EPIC [{{related id}}] {{title}}**
  * {{type}} [{{related id}}] {{title}}

<!--
Example

There are 3 lanes here but it is only an example: there is no right number of releases,
you slice every time you get a cohesive increment. The first lane is always the MVP in the
sense of slicing by Outcome (the minimum that lets a target user complete the journey),
but its title is that Outcome, not the word "MVP". No lane is called "Release 1",
"Enhancements", "Delight" or "v1.0": the title describes what it unlocks and acts as a
filter ("is this story strictly necessary to reach [title]?"; if not, it moves down to
the next lane).

### Release 1: First purchase by credit card
*A visitor finds a product, puts it in the cart and pays by card, receiving the confirmation. Slicing by Outcome: only what is needed to complete the journey once.*
* **Goal:** Enable the first complete purchase by a real customer and validate the idea
* **Metrics:** 10 transactions completed without errors in the first week
* **1. EPIC [EPIC-001] Discovery**
  * US [US-001] Exact text search
  * US [US-002] Basic catalog
* **2. EPIC [EPIC-002] Selection**
  * US [US-003] Product page with price and photo
  * US [US-004] Basic cart
* **3. EPIC [EPIC-003] Checkout**
  * US [US-005] Credit card payment
* **4. EPIC [EPIC-004] After-Sales**
  * US [US-006] Confirmation email with summary

### Release 2: Higher average order value and product found at the first attempt
*Buyers find what they look for sooner and add more items to the same order. Slicing Necessity vs Richness: no new flow, the flows of the first lane get thicker.*
* **Goal:** Increase the average order value and reduce searches without results
* **Metrics:** Average order value +15%, searches without results below 5%
* **1. EPIC [EPIC-001] Discovery**
  * US [US-007] Price and colour filters
  * US [US-008] Search autocomplete
* **2. EPIC [EPIC-002] Selection**
  * US [US-009] Related products
  * US [US-010] Quantity management in the cart
* **3. EPIC [EPIC-003] Checkout**
  * US [US-011] Saving the card for later purchases
  * US [US-012] PayPal payment
* **4. EPIC [EPIC-004] After-Sales**
  * US [US-013] Shipment tracking
  * US [US-014] PDF invoice

### Release 3: The customer comes back to buy without being prompted
*Those who have already bought find the shop again on their own and close the second order in a few seconds. Slicing by Learning: tests the riskiest hypothesis, that loyalty comes from fast repurchase.*
* **Goal:** Loyalty and spontaneous repurchase
* **Metrics:** 20% of customers with a second order within 30 days
* **1. EPIC [EPIC-001] Discovery**
  * US [US-015] Suggestions based on previous purchases
* **2. EPIC [EPIC-002] Selection**
  * US [US-016] Video reviews
* **3. EPIC [EPIC-003] Checkout**
  * US [US-017] One-click payment with Apple Pay or Google Pay
* **4. EPIC [EPIC-004] After-Sales**
  * US [US-018] Push notifications on shipment status
-->

<!-- optional section, include it only when filled in and only when the product is split into several maps: a map that covers the whole product omits it -->
## Out of Scope

<!-- Activities, personas or flows this map does not cover, pointing to the other map or PBI that covers them. One bullet per item, with where it goes: the PBI that covers it (`type [id] title`) or "not planned". List only what a reader could reasonably assume is included, not everything this PBI does not do -->
- {{what is not included}}: {{where it goes}}

<!-- optional section, include it only when filled in -->
## Additional Notes

<!-- Bullet list of details that emerged during backlog refinement, technical constraints or business logic. Write every link as [topic in clear words](address that reaches the spot: section anchor, page, Figma frame), never a bare URL, an abbreviation or a section number without its title -->

## DoR (Definition of Ready) Check
- [ ] Narrative - [1 line only: the story of what the user does flows]
- [ ] Vertical - [1 line only: every Release Lane crosses all the Backbone Epics, it is a hamburger and not a stack of bread; no Epic is completed before the others]
- [ ] Gravity - [1 line only: stories are correctly ordered from the most to the least important, top to bottom]
- [ ] Functional - [1 line only: the map describes the experience, not the system]
- [ ] Walking Skeleton vs MVP - [1 line only: the Walking Skeleton is different from the MVP]
- [ ] Lane Outcomes - [1 line only: every lane is titled with the Outcome it unlocks, not a label ("Release 1", "MVP", "Delight"), and every story in the lane is strictly necessary to that Outcome]
- [ ] Elevator Pitch - [1 line only: the whole BASE product can be explained in under 60 seconds, otherwise the narrative constraint is broken]
