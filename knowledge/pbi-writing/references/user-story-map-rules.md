---
name: user-story-map-rules
description: >-
  Always read in Phase 3, before building a User Story Map: the 5 binding rules (narrative constraint on the X axis, hamburger rule for releases, gravity on the Y axis, no architecture in the Backbone, Walking Skeleton different from MVP), the release title as Outcome and ruthless filter, the 5 patterns for cutting the lanes (Walking Skeleton, Outcome, Persona, Necessity vs. Richness, Learning), the 3 ways the map and Epics coexist (the Backbone generates the Epics, the lanes slice them, the Epic as zoom) and the elevator pitch test to verify the finished map.
source: synthesis of Jeff Patton (User Story Mapping) and Kenneth Rubin (Essential Scrum)
---

# THE USER STORY MAP (Patton / Rubin)
Goal of the tool: Turn a flat backlog into a two-dimensional map that tells the user's journey (X axis) and defines incremental releases of value (Y axis).

Just as INVEST exists for individual User Stories, Jeff Patton (the creator of the technique) and Kenneth Rubin define **iron rules and structural constraints** for building a Story Map that works. If you violate these constraints, you are not doing Story Mapping, just making a pile of messy Post-its.

## Constraints
There is no famous acronym like INVEST, but the framework rests on **5 unambiguous Golden Rules (or Constraints)**:

### 1. The Narrative Constraint (X Axis: Time)

The Backbone (the top row) **must** tell a chronological story.

* **The Rule:** If you read the post-its from left to right out loud, they must sound like a smooth account of what the user does ("First they search, then they select, then they pay, then they wait for the email", so coherent and respecting the principle of causality - B happens because A happened, you cannot wait for the confirmation email if you have not paid first).
* **The Prohibition:** It is strictly forbidden to order the activities by "importance" on the horizontal axis. The X axis is exclusively for the *flow of time*.

### 2. The Slice Constraint (The "Hamburger Rule")

A Release Lane (the horizontal slice) must be a "complete hamburger", not a stack of bread.

* **The Rule:** Every release must cross **the entire** Backbone, from left to right. The user must be able to complete their journey, even if in a crude way.
* **The Prohibition:** You cannot make a Release 1 that contains "All the Perfect Search" and "All the Perfect Selection" but zero Checkout. A hamburger made only of three layers of excellent bread and zero meat (the value) is not edible.

### 3. The Gravity Constraint (Y Axis: Necessity)

The further down you go vertically in the map, the less fundamental things are.

* **The Rule:** Within the same column (under a macro-activity), the stories at the top are the "Must Have", those at the bottom are the "Nice to Have". If time or budget runs out, you cut from the bottom.
* **The Prohibition:** There can be no two stories with the exact same priority. The Story Map forces you to make a ruthless choice: which one goes above and which one goes below.

### 4. The Architectural Prohibition

The map describes the experience, not the system.

* **The Rule:** Every post-it must represent a user action or a piece of perceivable value.
* **The Prohibition:** It is forbidden to have columns in the Backbone called "Set up Database", "Create API" or "Configure Server". Those are *technical Tasks* (which will go inside the US or in the Walking Skeleton), they are not user actions. If the user does not see it or "feel" it, it does not go in the Backbone.

### 5. The Distinction Constraint (Walking Skeleton vs MVP)

These two concepts are often confused, but they have opposite rules:

* **Walking Skeleton:** It serves the *Technical Team*. It is the bare infrastructure (e.g. a clickable button that does nothing but crosses all the layers of the code down to the database and back). **Rule:** It may even make no sense to the end customer, but it must test the technical risk.
* **MVP (Minimum Viable Product):** It serves the *Business*. It is the minimum product you can actually sell or have a real customer use to test whether the idea has a market. **Rule:** It must have enough value to solve the user's problem.

## Splitting patterns (Release Slicing)

Unlike the splitting of individual User Stories (which divides a macro-requirement into smaller pieces), splitting in the Story Map consists of **drawing horizontal lines (Release Lanes)** to group the stories into incremental packages. There is no predetermined number of releases: you slice the map every time you get a cohesive increment to test or to bring to market.

### The Release Title (The Outcome as filter)

Never name a slice of the map with sterile labels like "Release 1", "Phase 2" or "v1.0". Every release **must have a title that describes a specific Outcome** (the business goal or the user behavior you want to unlock).

In practice, the title is written on a post-it placed at the far left of the cut line.
*   **Examples of valid titles:** "Basic checkout working", "Onboarding for Beta Testers", "Opening to the B2B market", "Increasing retention through notifications".
*   **The function of the title:** It acts as a *ruthless filter*. If during mapping a team member discusses a feature (a post-it), the deciding question is: *"Is this story strictly necessary to reach [Release Title]?"*. If the answer is no, the post-it is pushed down, below the line, and postponed to a later release.

### The 5 operational Patterns for cutting the Releases

The criteria for deciding "where to draw the line" follow Jeff Patton's heuristics. You can use one or more of these patterns to slice your map from top to bottom.

#### 1. "Walking Skeleton" Slicing (The technical-risk cut)
The very first line of all. It takes the crudest and most basic version of *every* single Backbone activity. It often does not have enough commercial value to be released to a real customer, but it lets the team prove that the end-to-end infrastructure (from the interface to the database) is connected and working.

#### 2. Slicing by Outcome (The MVP cut)
It groups the smallest possible number of post-its that allows a specific target user to reach a goal from start to finish.
*Example:* Outcome "Enable online purchasing". The MVP will include: *Exact text search* → *Add to cart* → *Payment (card only)*. Solutions like "PayPal" or "Search by category" are cut out and relegated below the line.

#### 3. Slicing by Persona (The target cut)
If the product serves several types of users, draw the releases enabling them in sequence, instead of building half a product for everyone.
*Example:* The top slice (Release 1) contains only the stories the end user (B2C) needs to make purchases. The slice below (Release 2) adds the dashboards, the reports and the inventory management for the business user (B2B).

#### 4. Necessity vs. Richness Slicing (The 80/20 cut)
Within each column (Y axis), the stories are ordered by importance. The release line is drawn by isolating at the top the solutions that are absolutely **necessary** to complete the task, confining below the line the **rich or rare** solutions (edge cases, graphic embellishments, alternative paths, automations). Later releases do not create new flows, but "thicken" the existing ones, making them richer.
*Example:* Slice 1 (Necessity): "Password recovery by sending a link via email". Slice 2 (Richness): "Password recovery via SMS or authenticator app".

#### 5. Slicing by Learning (The market-risk mitigation cut)
Use the chess analogy (Opening, Middlegame, Endgame). Cut an initial release including *only* the features needed to test the riskiest business hypothesis, ignoring the "safe" features you already know how to build. The goal of this slice is not revenue, but maximizing fast learning about how users react.

> **The Slicing meta-pattern — "The Hamburger Rule":** The worst mistake in User Story Mapping is creating a slice that completely empties a single Backbone column, leaving the others untouched (the classic Waterfall approach: "Let's do all the Perfect Search first"). A correct cut is **always horizontal**: it crosses the entire map taking a little of everything, sacrificing the depth of each single function in favor of completing the user's journey.

## Map and Epics: how they coexist

The Epic is an artifact, a "what" to build; the Story Map is the visual tool to understand how and when to build it. They are not in competition: the map is the territory, the Epic is a neighborhood of that territory.

| Dimension | The Epic | The User Story Map |
| --- | --- | --- |
| **Nature** | Logical container of requirements, a giant "folder". | Two-dimensional X-ray of the entire product. |
| **Focus** | Vertical: a single business macro-goal. | Horizontal and vertical: the entire user journey and the releases. |
| **Structure** | One-dimensional: a list of User Stories from top to bottom. | Two-dimensional: X axis for time, Y axis for priority. |
| **Problem it solves** | Avoids 500 micro-stories scattered across the backlog without a parent. | Avoids losing the big picture ("we can't see the forest for the trees"). |

They coexist in three ways:

* **The Backbone generates the Epics.** The top row of the map, the Macro-Activities, represents the big blocks of the user's journey. **These Macro-Activities become exactly the Epics in the backlog**, with the same title: *[Search] → [Configuration] → [Checkout]* on the map, three Epics in the tracker.
* **The Release Lanes slice the Epics.** The flaw of an Epic is the temptation to say "let's finish all of Search before starting Checkout": that is waterfall. The slice (Release 1, MVP) cuts horizontally across all the Epics: in the same sprint two Search stories, one Configuration story, two Checkout stories. The Epics stay open in parallel and a complete hamburger is released.
* **The Epic as zoom.** When the product is too big for a single map (it would take a ten-meter wall), the process is reversed: you start from a macro-Epic and the team creates a Story Map dedicated to it alone, to break it down into releases and smaller stories. The Macro-Activities of that map are sub-Epics.

> **Jeff Patton's golden rule:** "An Epic is just a User Story too big to be printed on a single post-it. The Story Map is the table we lay it on to break it into pieces and make sense of it."

> **The practical trick (The Elevator Pitch Test):**
> When you have finished the Story Map, call a person from outside the project. Pointing at the Backbone from left to right, and then reading only the stories of *Release 1 (MVP)*, you should be able to explain the entire base product to them in less than 60 seconds. If they get lost or don't get the point, the narrative constraint is broken.
