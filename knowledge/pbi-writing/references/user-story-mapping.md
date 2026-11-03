---
name: user-story-mapping
description: >-
  Read when the user asks to map, prioritize or plan the releases of a set of stories or of an epic (Phase 3 of `../rules.md`): backbone, ribs, release lanes, walking skeleton, how to find the gaps.
source: https://jpattonassociates.com/the-new-backlog/
---

# User Story Mapping ("The New Backlog")

Jeff Patton's technique for replacing the flat backlog (prioritized list)
with a **two-dimensional map** of the stories. The map preserves context,
tells what the system does and makes release planning natural.

## The problem with the flat backlog

A prioritized list of stories destroys structure and meaning.

- **The big picture is lost.** Patton's metaphor: "we pull all the leaves off the
  tree, put them in a bag and then cut down the tree". What is left is
  dozens/hundreds of decontextualized cards, "compost without context".
- **You cannot see whether something is missing.** Staring at a flat list it is impossible
  to verify that you have covered all the necessary functionality. The gaps emerge
  from talking together, not from reviewing cards alone.
- **Planning releases is tedious.** Deciding "in/out" on 100+ stories
  one at a time is inefficient and there is no natural way to group
  related functionality into a coherent release.

## The structure of the map

The map has two dimensions: **narrative flow** (horizontal) and **priority**
(vertical).

### Backbone — User activities (horizontal axis, at the top)

- The big things users do: e.g. "manage email", "send promotional
  mailers". They are the **essential capabilities** of the system.
- They are like the vertebrae of the spine: they form the load-bearing structure.
- **Backbone activities are NOT prioritized against each other** — they are all
  essential. What gets prioritized instead are the *characteristics* of each activity.

### User tasks (the "ribs" under each activity)

- Under each activity sit the **tasks**: the smaller steps to complete it
  (e.g. under "manage email": "write message", "read message",
  "delete message").
- They are "story-sized" and hang from the backbone like ribs.

### Narrative flow (left → right)

- Lay out activities and tasks in **temporal/narrative order**: "the order in which
  you would tell the behavior of the system is the correct order".
- The map reads like a story, not like an arbitrary hierarchy.

### Priority (top → bottom)

- Higher = more necessary; lower = less necessary.
- Each card is slid up/down in its column to express how
  indispensable that variant/characteristic is.

## Slicing into releases (the horizontal swim lanes)

- Take a strip of **masking tape** and divide the map into **horizontal
  lanes**, one per release.
- Move the stories up and down across the lanes; vary the height within the lane to
  show the priority *within* that release.
- The first lane, at the top, is the minimum release (see Walking Skeleton).

### Build order

- Work is selected **from left to right and from top to bottom**.
- You move along the whole backbone, gradually going down the priorities of each
  rib.
- Key effect: **build all the main functionality a little at a
  time**, NOT one complete feature at a time. Every iteration touches the whole
  system.

## Walking Skeleton (minimum end-to-end release)

- It is "the smallest possible system that delivers end-to-end functionality".
- It must be built **first**: it establishes the viability of the system and validates
  the whole user path early.
- **Car analogy:** you don't ask "do we prioritize the engine or the transmission?"
  — they are backbone, non-negotiable. The variants sit *underneath*: "4- or 6-cylinder
  engine? brakes with or without ABS?". Asking "do we release without brakes and
  add them later?" is a meaningless question.
- So: the backbone defines what must always be there; the vertical priority
  only decides the level of refinement of each piece per release.

## How the map helps find the gaps and prioritize

- **Walking the map reveals the missing steps.** Going through the map in order
  with users/stakeholders, they often correct you: "you skipped a couple of steps here".
  Immediate feedback on completeness.
- **Information radiator.** Hung on the wall, the map becomes a constant point of
  discussion about the product: it reminds everyone of the big picture and of how much has
  been done. It works both as a planning board and as a reference during
  the sprints.
- **System perspective during the build.** It avoids the "one feature
  at a time" myopia: it makes cross-cutting dependencies visible and prevents forgetting
  critical functionality.
- **Annotations.** Mark on the map, in the right spot, the pain points, insights
  and opportunities that emerged from talking with users.

## Quick glossary

- **Activity:** a large user goal/workflow.
- **Task:** a discrete, story-sized step within an activity.
- **Backbone:** the essential, non-negotiable capabilities (the vertebrae).
- **Ribs:** the supporting stories that hang from the activities.
- **Walking Skeleton:** MVP with end-to-end functionality across all the main
  features, at the lowest level of fidelity.
