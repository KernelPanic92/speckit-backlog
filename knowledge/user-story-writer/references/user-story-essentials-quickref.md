---
name: user-story-essentials-quickref
description: >-
  Read when you are unsure whether something is a story or a delivery task, when a title does not stand on its own (people refer to the story by its number), or when you need to decide how much detail to put on the card versus the conversation and the acceptance criteria. Patton's 3C model.
source: https://jeffpatton.wpengine.com/wp-content/uploads/2015/03/story_essentials_quickref.pdf
---

# User Story Essentials (Jeff Patton)

## Core idea: stories are for telling, not for specifying

User stories get their name from **how they are used**, not from how they are written.
Kent Beck's original insight (late '90s): solve the problem of communicating the
details of what to build **by getting together and "telling stories"** to build a
**shared understanding** in the minds of everyone involved.

In the conversation the focus is not only on *what* to build, but on **who** will use the software
and **why**. The goal: identify the most valuable thing that can be built in the
cheapest way.

> A shared document is NOT shared understanding. Reading the same text,
> different people imagine different things. Shared understanding comes from describing
> your own ideas with words and drawings, and then combining and refining them together.

## The 3 C model (and beyond)

A story is a **token for a conversation**, not the conversation itself.

- **Card** — Write product ideas on cards, one per card. The card is like a library catalog
  card: it contains *just enough* to find the details when they are needed.
  It serves to organize, prioritize and plan.
- **Conversation** — Discuss the idea with others. Let them ask lots of questions. Work together
  to arrive at ideal solutions. Goal: build shared understanding.
- **Confirmation** — Bring models, personas, UI sketches or anything useful into the
  conversation. Identify the ideal solutions, reach agreement on what to build and
  **record that agreement as a set of confirmation tests** (acceptance criteria).

The cycle continues beyond the 3 Cs:

- **Construction** — Developers, testers and others, equipped with the information and the shared
  understanding born from the conversations, build and test the software.
- **Consequences** — Now there is working software to learn from. Those who asked for it and those who
  built it evaluate it; it must also be tested with real users to verify whether it meets their
  needs. Goal: **learning**. The improvement ideas restart the cycle.

## What's on the card

On a typical card you find:

- **Short title** — easy to read in backlogs and to say in standup. If you notice you are
  referring to the story by its number, stop: it is the signal that the title does not work.
- **Description** — if the title is not enough. Always include **who, what and why**
  (this is where the template `As a [Persona], I want [Action/Goal], so that [Value]` comes in handy).
- **Meta-information** — estimated development time, estimated value, dependencies, status.

## Before building, agree on what to build

Before the team commits to building the software described by a story, agree on the
**acceptance criteria**. Record the answers to:

- What will we test to confirm that this story is **done**?
- How will we demonstrate this software at a product review?

When you write a story's tests, **use examples** (cf. *Specification by Example* by Gojko Adzic).

## "Talk & Doc": talk and document

You will have many discussions around stories with different roles. While you talk, **draw and annotate**:

- Bring models (workflows, use cases, UI designs) that help explain the story, but be ready
  to change them during the conversation.
- Draw on whiteboards, model with post-its, record on flipchart paper.
- Keep the models as **"vacation photos"**: reminders that help *those who were there*
  remember the details. Those who weren't there won't remember them — just like with other people's photos.

## From concept to delivery: progressive splitting and refinement

Stories are split and refined progressively as they move from vague idea to
working software:

1. **Opportunities** — backlog of opportunities from product ideas and requests from customers/users/stakeholders.
2. **Discovery** — elaborate, design and validate the ideas; goal: find the **minimum viable
   product (MVP)**. It produces the product backlog.
3. **Delivery** — design, decompose and describe the backlog items.
4. **Validation** — review the finished software with the team and the stakeholders; validate with customers and users.
5. **Release** — after the release, keep measuring performance against the target outcomes.
   The most valuable opportunities come after seeing the product in use.

Aggregation thresholds:

- **Enough to test with users** — a single story in a sprint may seem
  insignificant; aggregate enough finished and tested parts for the user to reach a
  meaningful goal before testing.
- **Enough to release** — aggregate validated parts that together add up to a valuable release.

## Splitting: "think about the cake", not horizontal slices

Every story must describe **a piece of software you can "taste"**: once built,
it must teach you something. This is the **vertical** split.

- **Stories** describe something you can **deliver and evaluate**.
- **Delivery tasks** are the "recipe": the work needed to make the story (they are NOT stories).
- Decompose stories into **smaller stories that are still deliverable**: they have similar recipes, just
  with less of each ingredient (e.g. less testing because they are smaller).
- A whole feature has value for customers/users, but it often takes several stories to make it up.
- If the software has no UI, find another way to demonstrate that it works.

## Release strategy: work like Da Vinci, finish on time

To manage a release budget, split the big stories into opening / mid / end game:

- **Opening Game** — the first stories emphasize iteration and learning: making sure you build
  the **right** product. Aim to have the "big picture" as soon as possible:
  complete but immature versions enable early functional/performance testing and validation.
- **Mid Game** — once you are confident about the "shape" of the product, you accumulate value.
- **End Game** — over time the value of new stories decreases: it is the signal that it is time to release.

## Story Workshop & story map

- **Story Workshop** — members of the product team regularly meet the delivery team to
  work on the details and agree on the acceptance criteria.
- **Story map** — lay out the cards as a map to see the **big picture**, mapping an
  entire process that spans several types of users. Use it to slice a feature into
  opening/mid/end game and to slice the product into a series of viable releases, each
  tied to a **target outcome** (outcome-centric roadmap).
