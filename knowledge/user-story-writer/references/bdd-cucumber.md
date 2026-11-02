---
name: bdd-cucumber
description: >-
  Read when a story exceeds 5 scenarios only because of data variants (use Scenario Outline with Examples), when a scenario exceeds 5 steps, when you need to rewrite an imperative scenario (clicks, fields, buttons) in declarative form, or when the story contains an asynchronous operation (saving, loading a list, synchronizing): the two cases, asynchronous action and resource loading, and the declarative retry. Complete Gherkin reference.
source: https://cucumber.io/docs/bdd/
---

# BDD and Gherkin — Reference for writing scenarios

Behaviour-Driven Development (BDD) closes the gap between business and technical team:
it encourages collaboration across roles to build a shared understanding of the
problem, and produces system documentation that is automatically verified against the
real behavior. The ultimate goal is not tests or documentation (side
effects), but working, valuable software.

Guiding principles:
- Work in small, rapid iterations to maximize feedback and the flow of value.
- Use concrete, real examples to guide development from concept to implementation.
- Treat documented examples as team assets that enable safe future changes.

## The three practices

1. **Discovery — what the system *could* do**
   Structured conversations using real examples to build a shared understanding
   of user needs and system boundaries. "The hardest part of building
   a software system is deciding precisely what to build."

2. **Formulation — what the system *should* do**
   Documenting the examples as executable specifications, in a format readable by both
   humans and machines, establishing a shared language that uses the terminology
   of the problem domain.

3. **Automation — what the system *actually* does**
   Connecting the examples to the system as tests, then developing the implementation guided
   by the failing tests. The automated examples work as "guardrails" that
   keep development on track.

## Gherkin structure

A feature file is structured like this:

```gherkin
Feature: Feature title
  High-level description (free text, optional)

  Rule: A specific business rule (Gherkin 6+, optional)

    Background:
      Given a context common to all scenarios

    Scenario: Scenario title
      Given a known initial context
      And an additional precondition
      When an action or event occurs
      Then I expect an observable outcome
      But this other thing must not happen

    Scenario Outline: Same behavior with different data
      Given a cart with <items> items
      When I apply the discount
      Then the total is <total>

      Examples:
        | items | total |
        | 1     | 10    |
        | 3     | 27    |
```

## Keywords

- **Feature**: high-level description of a piece of functionality; groups related
  scenarios. Only one `Feature` per file.
- **Rule** (Gherkin 6+): organizes scenarios around a specific business rule.
- **Scenario** / **Example**: a concrete case that illustrates a rule, made of
  steps following the Given-When-Then pattern.
- **Given**: puts the system in a known state (preconditions), before the interaction.
- **When**: describes the action or event — what the user does or what the system triggers.
- **Then**: specifies the expected outcome through assertions. It verifies a result
  **observable by the user**.
- **And** / **But**: chain several steps of the same type, for readability, without
  repeating Given/When/Then.
- **\*** (asterisk): replaces Given/When/Then, useful to express the steps as a
  bulleted list.
- **Background**: shared setup steps, run before each scenario; reduces the
  repetition of common preconditions. Keep it short and vivid.
- **Scenario Outline**: template to run the same scenario with several data sets,
  using `<parameter>` placeholders.
- **Examples**: table of test values for the parameters of the Scenario Outline.

### Step arguments
- **Doc Strings**: multi-line text blocks between triple quotes or backticks,
  passed as the last argument of the step.
- **Data Tables**: tables delimited by pipes `|` to pass lists to the steps.

## Rules for Given / When / Then

- **Given** = context that already exists, not user actions. It puts the system in a
  known state.
- **When** = a single action/event that triggers the behavior under examination.
- **Then** = an outcome **observable by the user**, never an inspection of the database or of the
  internal state.
- Do not repeat the step text across different keywords: use `And`/`But` to
  chain.

## What makes a good scenario

- **One behavior per scenario**: each scenario illustrates a single rule.
  Ideally a single `When` (the action under examination).
- **Concise**: 3-5 steps. If you need more, you are probably mixing behaviors.
- **Declarative, not imperative**: describe *what* the user wants to achieve, not the
  mechanical steps (clicks, fields, buttons) to achieve it.
- **No UI mechanics**: no "click", "fill in the field", "press the button".
  Speak in terms of intent and domain.
- **Business-readable**: use the terminology of the problem domain, not the technical
  one (domain terms come from the Ubiquitous Language section of `.specify/memory/product.md`).
  "Imagine it's 1922": avoid technology-specific language.
- **Observable outcomes**: verify results visible to the user, not the internal state.

### Imperative (to avoid)

```gherkin
When I enter "alice@example.com" in the email field
And I enter "secret" in the password field
And I click the "Login" button
Then I see the text "Welcome" in the header
```

### Declarative (preferred)

```gherkin
When I log in with valid credentials
Then I am welcomed into my personal area
```

## Scenarios for asynchronous operations

An asynchronous operation (a save, the loading of a list, a synchronization)
must be described the way the user experiences it: from the initial trigger to the final outcome, through
the wait. A scenario that skips the wait ("When the user confirms the submission, Then they see the success")
leaves the developer to choose what to show in the meantime, and often the choice is
"nothing": the user gets the impression that nothing is happening.

### Principles

- **Full cycle in every outcome scenario.** Every scenario that ends with an outcome
  (success, error, no data) goes through the entire cycle: trigger, appearance
  of the loading indicator, its disappearance at the end, outcome. Do not isolate the
  "in progress" state in a scenario of its own: the wait is not a behavior, it is a phase of all
  behaviors. The failure goes in the `Given` ("the system is unable to..."), the
  `When` remains the user's action.
- **No explicit waits.** Never `And I wait 5 seconds`. The automation framework
  handles the wait: use a semantic trigger such as `And once processing
  is complete...` or `And once the attempt is over...`.
- **UI agnosticism.** "Loading indicator", not "spinner" or "skeleton";
  "the submit action is available again", not "the button turns blue again". It is the
  "no UI mechanics" rule applied to the wait.
- **Visual reset and interactivity.** The indicator must disappear before the
  outcome occurs. In case of error the scenario says how the interface gets ready for a new
  attempt, and the answer depends on the case (below).
- **Length.** Error scenarios reach 6-7 steps: this is the allowed exception to the
  3-5 rule, because the waiting steps are not additional behaviors but phases of a single
  one. There is still a single `When`.

### Case 1: asynchronous action (active trigger)

The user triggers the operation: confirms a form, saves, deletes, synchronizes. During
the wait the command is locked, to prevent double submissions. If the operation fails **no
new command appears**: the system shows the error and re-enables the original command,
with the entered data still present.

```gherkin
Feature: Submitting the data of a form

  Scenario: The submission succeeds
    Given the user has filled in the form
    When they confirm the submission
    Then they see the loading indicator
    And once processing is complete the indicator disappears
    And they see the success message "Data saved"

  Scenario: The submission fails
    Given the user has filled in the form
    And the system is unable to save the data
    When they confirm the submission
    Then they see the loading indicator
    And once the attempt is over the indicator disappears
    And they see the message "Unable to save the data"
    And the submit action is available again
```

### Case 2: resource loading (passive trigger)

The operation starts on its own: a navigation, the opening of a page, an applied
filter. If it fails, the system ends up in an empty error state: there is no
original command to re-enable, so **a dedicated action to retry must
appear**. The absence of data (empty state) is a third outcome of the same cycle: same
indicator, same disappearance, then the empty-state message.

```gherkin
Feature: Loading the list of Todos

  Scenario: The loading succeeds
    When the user opens the "My Todos" page
    Then they see the loading indicator
    And once data retrieval is complete the indicator disappears
    And they see the list of their Todos

  Scenario: The loading fails
    Given the system is unable to retrieve the data
    When the user opens the "My Todos" page
    Then they see the loading indicator
    And once the attempt is over the indicator disappears
    And they see the message "Unable to load the data"
    And the "Retry" action is available
```

### Restore (retry) in declarative form

When the user retries (confirms the submission again in Case 1, uses the "Retry" action
in Case 2) **do not rewrite the complete flows** "retries and succeeds" and "retries and
fails": success and error are already covered by the scenarios above, and repeating them doubles
the tests without adding a rule. One scenario is enough to verify that the attempt
restarts the asynchronous cycle, that is, brings the interface back to the loading state.

```gherkin
  Scenario: The restore attempt restarts the asynchronous cycle
    Given the user sees the loading error on the "My Todos" page
    When they retry the loading
    Then the system starts a new attempt
    And they see the loading indicator again
```

For Case 1 the scenario is the same, with `Given the user sees the submission error`
and `When they confirm the submission again`. If the behavior changed on the second attempt
(a limit on attempts, a different message), that is a new business rule and
deserves its own scenario.
