---
name: invest-criteria
description: >-
  Read when the INVEST Check in the Micro-Scope gives a "no" and you need to understand how to fix it (which letter is violated and Wake's tactic to correct it), or when you write a Task and need the SMART checklist. Source: Bill Wake.
source: https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/
---

# INVEST: criteria for good User Stories

The INVEST criteria (Bill Wake) describe the characteristics of a good user story.
They serve as a diagnostic checklist: when a story "doesn't work", it almost always
violates one of these six letters.

## Premise: the story is not the documentation

A user story lives on three dimensions (the "3 Cs"):
- **Card**: short text, it is only a *reminder*, not the complete specification.
- **Conversation**: the real detail emerges from talking between
  business/customer and developers.
- **Confirmation**: the tests/acceptance criteria that say when
  the story is "done".

Keeping this in mind avoids the most common mistake: trying to put everything on the card.
The card "promises a future conversation", it does not replace it.

---

## I — Independent

**What it means:** stories should be as self-contained as possible, without
conceptual overlaps or rigid dependencies between them.

**Why it matters:** if stories are independent, the customer can **reorder and
schedule them freely** based on value, and each one can be estimated on its own.
Dependencies create side effects on estimates and block prioritization.

**How to apply it:**
- When two stories "intertwine", try combining them into a single one, or
  cutting them along a different boundary.
- Perfect independence is not always achievable: manage the remaining dependencies
  explicitly. Classic example: "3 points for the first report, then 1 point for
  each of the following ones" — the first story carries the cost of the shared
  infrastructure, the others become incremental.

---

## N — Negotiable

**What it means:** a story **is not a contract** that fixes features
rigidly. It captures the *essence* of what is needed; the details are co-created by
customer and developer during development.

**Why it matters:** leaving room for negotiation makes it possible to find the best
solution instead of committing to an implementation decided too early and with little
information.

**How to apply it:**
- Write the card as a reminder, not as a locked-down spec. Details and test ideas
  are **added as notes over time**, but they are not needed to prioritize.
- If you notice you are writing extremely detailed requirements on the card, stop:
  that detail belongs to the conversation and to the acceptance criteria.

---

## V — Valuable

**What it means:** every story must deliver value to the **customer/user**, not internal
"technical" value for the developers.

**Why it matters:** it is the principle that drives **vertical splitting**. Cutting
stories by architectural layer (DB, then backend, then UI) produces pieces without value:
"a complete database layer has little value for the customer if there is no
presentation layer".

**How to apply it:**
- Split stories into **vertical slices**: each slice crosses all the layers and
  delivers a behavior observable by the user, however minimal.
- Rephrase technical/infrastructure stories in terms of the value they enable,
  or fold them into the first story that needs them (see the note on Independent).
- Test: "would a real user notice this story if I delivered it?". If not, it is probably
  a technical task, not a story.

---

## E — Estimable

**What it means:** a story must be estimable. An exact estimate is not needed, just
enough for the customer to be able to **order and schedule it**.

**What makes a story NOT estimable (and how to fix it):**
- Missing domain knowledge → more **conversation and negotiation** with the
  customer is needed.
- Missing skills or technical knowledge → more team experience is needed; when the
  gap prevents estimating, the tool is a **time-boxed spike** (a fixed-time
  exploration activity whose purpose is to produce enough knowledge to estimate
  the real story).
- The story is **too big** → split it (see Small).

For Wake, estimability therefore depends on three factors: **knowledge** (negotiation
and conversation), **size** (bigger stories are harder to estimate) and
**team experience**. (The spike is a common story-splitting technique to close
the knowledge gap, not a term used explicitly in this article.)

---

## S — Small

**What it means:** a story should be small — at most a few
person-weeks, ideally person-days.

**Why it matters:** big stories are hard to plan and their estimates are
inaccurate; the scope becomes vague. Small stories are easier to estimate and give
faster feedback.

**How to apply it (split tactics, keeping the vertical cut and the value):**
- By **flow/workflow**: separate the steps of the path (create / edit / delete).
- By **business rules**: simple case first, edge cases/exceptions later.
- By **data**: a subset of fields or input types first, the rest later.
- By **interface/device**: one variant (e.g. desktop) first, the others later.
- By **performance**: first "it works", then "it works fast".

A story that is too big (epic) must be split; remember that the short card is filled with
detail through the conversation, not by making the text longer.

---

## T — Testable

**What it means:** writing a story carries an implicit promise: "I understand what I
want well enough to write a test for it".

**Why it matters:** if you cannot imagine the test, you have not really understood the
requirement. Testability is directly tied to the **acceptance criteria**: the
customer's tests, defined *before* implementation, increase productivity
and clarify what "done" means.

**How to apply it:**
- For every story, write the acceptance criteria that prove its behavior. (*Our*
  rules in `../rules.md` standardize these criteria in the BDD/Gherkin Given/When/Then
  format; Wake's article does not prescribe a specific format.)
- **Non-functional requirements** (performance, usability, reliability) must be
  *operationalized*: turn them into concrete tests that define the real need
  — a measurable numeric threshold instead of a vague adjective like "it must be fast".
- If a story is not testable, it is usually also under-negotiated or too vague:
  go back to the conversation.

---

## Note: SMART for tasks

When a story is broken down into technical **tasks** internal to the team, the SMART
acronym applies instead (tasks are NOT stories: they are units of work for the developers):

- **Specific** — clear enough to understand what it involves and to avoid duplicated work.
- **Measurable** — there is a criterion to call it "complete" (it does what it must, tests
  included, code refactored).
- **Achievable** — whoever takes it on must be able to do it; anyone can ask for help.
- **Relevant** — every task contributes to its story; the customer understands its purpose.
- **Time-boxed** — it has a duration cap: if it overruns, the team must know and react
  (split the task, change person, ask for help).

---

## Operational summary

When you write or refine a story, run it through these questions:
- Can it be reordered without depending on others? (I)
- Is the card a reminder, not a locked-down contract? (N)
- Would the user notice the value? Is it a vertical slice? (V)
- Can I estimate it, or do I need a spike? (E)
- Is it small enough to estimate well and give fast feedback? (S)
- Do I already know how I would write its acceptance test? (T)

If even a single answer is "no", the story must be negotiated, re-cut or clarified.
