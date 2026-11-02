# Examples — User Story Writer

Complete, high-fidelity examples adapted from real cases and anonymized: names, vendors and domains have been changed. Each example reports the user's input exactly as it arrived and the full output expected from the skill: macro-analysis, Micro-Scope Reasoning blocks, stories, final check and summary. They are the concrete reference for how to apply the rules in `rules.md`. Wherever the original output violated a rule now in force (multiple actions chained in the `When`, prescriptive UI, a persona outside the Connextra format, references to application layers), it has been corrected, so the examples teach only permitted behaviours.

PBIs follow the PBI templates (here `pbi-story-template`): metadata (`id`, `title`, `type`, `relations`, ...) in the YAML frontmatter, a body that starts with the Connextra sentence. The `US-00x` ids are mocked and valid only within the single example. A dependency between two stories is declared with `BLOCKED_BY` in the `relations` of the blocked story, never as an inverse property on the blocking story.

The input is shown in a `text` block, the expected output in a four-backtick `markdown` block, which in turn contains the three-backtick blocks of the individual stories.

---

## Example 1 — Draft with multiple sections ("Trash" system)

What it teaches: how to break down an already structured draft (Task Outcome, Additional Notes, Assumptions, Risks) into seven stories with the Operations and Variations in Data patterns, isolating reading from writing and business rules from the base flow.

### User input

```text
This is the draft I wrote:

<draft>
Task Outcome

Allow recovering any deleted courses or lessons. It is also useful to allow permanent deletion. So some kind of trash bin will be needed, from which courses or lessons can be recovered or permanently removed.

Additional Notes

The delete buttons in editing mode must change the state of a course or a lesson to a deleted state (not selectable from the dropdown of the entity form).
The profile menu must have a Trash entry for the relevant user roles
The Trash page hosts a simple list of the previously deleted courses or lessons under the role's responsibility and allows permanent removal or restore (depending on the role). The fields needed in the list are: course or lesson name, deletion date, any relation to existing courses (even just as a warning icon).

Assumptions

A standard user cannot delete courses or lessons
An editor user can delete a lesson under their responsibility
An editor user can recover a previously deleted lesson under their responsibility
A manager user can delete a lesson or a course under their responsibility
A manager user can recover a lesson or a course under their responsibility previously deleted by them or by an editor
An administrator user can delete and recover a lesson or a course previously deleted by any user
Only administrator and manager users can delete courses or lessons with active enrollments under their responsibility (after an alert)
Lesson sections have no trash
When Lessons are restored, if a related Course exists, the relation will be restored too.

Risks

Handling the relations between courses and lessons could create data integrity problems
Future tracking of user behaviour on courses or lessons must be preserved
</draft>
```

### Expected output

````markdown
# Phase 1: MACRO-ANALYSIS

* **Request:** Implementation of a "Trash" (Trash Bin) system for the `Course` and `Lesson` entities. The system must handle the complete lifecycle: moving to the trash (Soft delete), Viewing, Restore and permanent deletion. These capabilities are enabled for Editors, Managers and Admins, with more or fewer capabilities depending on the specific role.

* **Working criterion:** The fundamental principle is context integrity: in the absence of critical details about the business, the user persona or the system constraints, it is imperative to stop the process and ask for clarification rather than base the generation on assumptions. Every User Story produced must strictly adhere to the Connextra format, placing a real human or business actor at the centre — never a technical role — and articulating a value distinct from the action itself (`As a... I want... so that...`). To ensure release quality, stories must respect the INVEST criteria (independent, negotiable, valuable, estimable, testable), taking the shape of "vertical slices" of working software that can be completed in a single sprint. This requires an aggressive splitting strategy that sharply separates read operations from write operations and avoids any horizontal slicing based on architectural layers. The Acceptance Criteria must use exclusively the Gherkin syntax (`Given`, `When`, `Then`) to describe observable behaviours, ensuring holistic coverage that includes the standard path, the edge cases and the explicit handling of asynchronous states such as loading, errors or absence of data. Finally, there is an absolute ban on introducing "phantom UI" or prescriptive descriptions of the interface: every visual element mentioned must be fully functional within the current story and defined by the user's intent, not by the mechanics of the click (no `click the green button`, yes `confirm the operation`).

### Phase 2: ITERATIVE DRAFTING

**[START USER STORY ITERATION 1]**

#### Micro-Scope Reasoning for US-001

* **Value Focus:** Allow archiving (soft delete) of `Course`s from the operational flows without immediate data loss.
* **Technical Boundaries:** Scope limited to the delete action from the existing lists/forms. **OUT:** The Trash page, restore and permanent deletion.
* **Split pattern:** Operations, combined with Variations in Data. The draft describes an entire lifecycle (archiving, browsing, restore, permanent deletion): this slice is the archiving operation alone. The Course entity is separated from the Lesson entity because the two have different permissions (Manager/Admin versus Editor/Manager/Admin). It won over a "by role" split because each operation is releasable and testable on its own, while a by-role split would have produced nearly identical stories.
* **INVEST Criteria Check:**
  * **Independent:** Yes, the soft delete is functional even without the trash UI (the data disappears from the main view).
  * **Negotiable:** Yes.
  * **Valuable:** Immediate (cleanup of operational data).
  * **Estimable:** Yes.
  * **Small:** Focused on: a single domain entity, a single action and a single state change.
  * **Testable:** Yes, once the Course has been deleted it can no longer be found in the catalogue or through the search feature.
* **Constraints check:**
  * avoids generic conjunctions ("and", "or") in the `I want` clause: the user story handles only the `Course` entity and moves the further actions (blocking operations on active enrollments) to other user stories.
  * avoids criteria that prescribe the UI: it does not prescribe whether deletion will be a button, an icon or a menu item, it does not prescribe how the user is notified of the operation's success/failure, it does not prescribe how the user leaves editing (the notification could be a modal that confirms the deletion and shows a button to leave the page, or it could be a snackbar that appears while the user is forcibly moved to another page).

*In spec-kit this block is written to its own file under `backlog/` (or to `spec.md` when it is the root PBI); it is shown inline here for readability.*

```markdown
---
id: US-001
title: Course Archiving (Move to Trash)
type: US
---

As an **advanced content manager (Manager, Admin)**, I want **to move a Course to the trash**, so that I can remove it from the operational views and selection menus without losing the data history or risking accidental deletions.

## Outcome

Implementation of the "Soft Delete" logic on Courses. The action changes the entity's state, making it invisible in the standard forms but recoverable in the future.

## Acceptance Criteria

### AC-1: Deletion
**Given** a user with advanced content management permissions (Manager, Admin)
**And** they are editing a Course
**When** they perform the deletion
**Then** a loading indicator is shown
**And** editing is disabled while the operation is in progress
**And** when processing finishes the indicator disappears
**And** the successful deletion is notified
**And** the user leaves editing mode
**And** the Course disappears from the catalogue, from the associated Lessons and from the dropdowns of the related forms.

### AC-2: Missing permissions
**Given** a user WITHOUT advanced content management permissions
**When** they edit a Course
**Then** the deletion capability is not available

### AC-3: Error while moving to the trash
**Given** a user with advanced content management permissions (Manager, Admin)
**And** they are editing a Course
**And** the system is unable to delete it
**When** they perform the deletion
**Then** a loading indicator is shown
**And** editing is disabled while the operation is in progress
**And** when the attempt finishes the indicator disappears
**And** the error that occurred is notified
**And** editing is re-enabled and deletion is available again.

## Out of Scope
- Viewing the deleted items in the Trash page — US [US-005] Trash View (Browsing Interface)
- Restoring a Course from the Trash — US [US-006] Entity and Relation Restore (Un-delete)
- Permanently deleting a Course — US [US-007] Permanent Deletion (Hard Delete)
- Confirmation before deleting a Course with active enrollments — US [US-003] Deletion Confirmation for a Course in Use
- Moving a Lesson to the trash — US [US-002] Lesson Archiving (Move to Trash)

## Additional Notes
- Deletion must not be permanent but must move the entity to a state that regular users cannot access.
- It is assumed that non-editor users cannot access the editing page.

## Risks
- Risk that the entity remains selectable in old forms if the selection queries do not filter it out explicitly.
```

**[END USER STORY ITERATION 1]**

---

**[START USER STORY ITERATION 2]**

#### Micro-Scope Reasoning for US-002

* **Value Focus:** Allow archiving (soft delete) of `Lesson`s from the operational flows without immediate data loss.
* **Technical Boundaries:** Scope limited to the delete action from the existing lists/forms. **OUT:** The Trash page, restore and permanent deletion.
* **Split pattern:** Operations combined with Variations in Data, the same logic as US-001 applied to the Lesson entity, which has a wider set of roles (Editors too).
* **INVEST Criteria Check:**
  * **Independent:** Yes, the soft delete is functional even without the trash UI (the data disappears from the main view).
  * **Negotiable:** Yes.
  * **Valuable:** Immediate (cleanup of operational data).
  * **Estimable:** Yes.
  * **Small:** Focused on: a single domain entity, a single action and a single state change.
  * **Testable:** Yes, once the Lesson has been deleted it can no longer be found in the catalogue or through the search feature.
* **Constraints check:**
  * avoids generic conjunctions ("and", "or") in the `I want` clause: the user story handles only the `Lesson` entity and moves the further actions (blocking operations on active enrollments) to other user stories.
  * avoids criteria that prescribe the UI: it does not prescribe whether deletion will be a button, an icon or a menu item, it does not prescribe how the user is notified of the operation's success/failure, it does not prescribe how the user leaves editing.

```markdown
---
id: US-002
title: Lesson Archiving (Move to Trash)
type: US
---

As a **content manager (Editor, Manager, Admin)**, I want **to move a Lesson to the trash**, so that I can remove it from the operational views and selection menus without losing the data history or risking accidental deletions.

## Outcome

Implementation of the "Soft Delete" logic on Lessons. The action changes the entity's state, making it invisible in the standard forms but recoverable in the future.

## Acceptance Criteria

### AC-1: Deletion
**Given** a user with content management permissions (Editor, Manager, Admin)
**And** they are editing a Lesson
**When** they perform the deletion
**Then** a loading indicator is shown
**And** editing is disabled while the operation is in progress
**And** when processing finishes the indicator disappears
**And** the successful deletion is notified
**And** the user leaves editing mode
**And** the Lesson disappears from the catalogue, from the Courses and from the dropdowns of the related forms.

### AC-2: Error while moving to the trash
**Given** a user with content management permissions (Editor, Manager, Admin)
**And** they are editing a Lesson
**And** the system is unable to delete it
**When** they perform the deletion
**Then** a loading indicator is shown
**And** editing is disabled while the operation is in progress
**And** when the attempt finishes the indicator disappears
**And** the error that occurred is notified
**And** editing is re-enabled and deletion is available again.

## Out of Scope
- Viewing the deleted items in the Trash page — US [US-005] Trash View (Browsing Interface)
- Restoring a Lesson from the Trash — US [US-006] Entity and Relation Restore (Un-delete)
- Permanently deleting a Lesson — US [US-007] Permanent Deletion (Hard Delete)
- Confirmation (or block, for Editors) before deleting a Lesson with active enrollments — US [US-004] Deletion Confirmation for a Lesson in Use
- Moving a Course to the trash — US [US-001] Course Archiving (Move to Trash)

## Additional Notes
- Deletion must not be permanent but must move the entity to a state that regular users cannot access.
- The acceptance criteria do not handle the case where the user lacks permissions, since it is assumed that non-editor users cannot access the editing page.

## Risks
- Risk that the entity remains selectable in old forms if the selection queries do not filter it out explicitly.
```

**[END USER STORY ITERATION 2]**

---

**[START USER STORY ITERATION 3]**

#### Micro-Scope Reasoning for US-003

* **Value Focus:** Prevents the accidental removal of a Course with active enrollments.
* **Technical Boundaries:** Scope limited to the delete action from the existing lists/forms. **OUT:** The Trash page, restore and permanent deletion.
* **Split pattern:** Business Rule Variations. The "active enrollments" rule is a variant of the base archiving flow (US-001): it adds a condition and a warning without changing the operation. Extracted because US-001 remains releasable without it and because the rule has its own test (enrolling a user in a Course).
* **INVEST Criteria Check:**
  * **Independent:** Yes, once US-001 has been iterated, the check can be implemented without depending on further concepts.
  * **Valuable:** Immediate (it avoids inadvertently deleting Courses that are bringing value).
  * **Estimable:** Yes.
  * **Small:** Focused on a single action.
  * **Testable:** Yes, by enrolling a user in a course it is possible to verify that the check appears during the deletion phase.
* **Constraints check:** Handles the critical "active enrollments" rule for the enabled roles (Manager/Admin), who are shown a warning.

```markdown
---
id: US-003
title: Deletion Confirmation for a Course in Use
type: US
relations:
    "US-001":
        title: "Course Archiving (Move to Trash)"
        type: US
        relationType: BLOCKED_BY
        reason: "the confirmation plugs into the Course deletion flow introduced by US-001"
---

As an **advanced content manager (Manager, Admin)**, I want **to receive a confirmation request when I delete a Course with active enrollments**, so that I can remove it with full awareness.

## Outcome

Implementation of the check logic for Courses currently in use. The action prevents immediate deletion through a warning, ensuring that the user deletes only what they are sure must be removed.

## Acceptance Criteria

### AC-1: Warning
**Given** a user with advanced content management permissions (Manager, Admin)
**And** they are editing a Course with active enrollments
**When** they perform the deletion
**Then** a warning asking whether to proceed is shown

### AC-2: Confirmation
**Given** a user with advanced content management permissions (Manager, Admin)
**And** they have requested the deletion of a Course with active enrollments
**And** the warning asking whether to proceed is displayed
**When** they confirm the operation
**Then** the deletion workflow proceeds

### AC-3: Refusal
**Given** a user with advanced content management permissions (Manager, Admin)
**And** they have requested the deletion of a Course with active enrollments
**And** the warning asking whether to proceed is displayed
**When** they cancel the operation
**Then** the deletion workflow is interrupted

## Out of Scope
- Moving the Course to the trash (loading, success and error of the deletion) — US [US-001] Course Archiving (Move to Trash)
- Viewing the deleted items in the Trash page — US [US-005] Trash View (Browsing Interface)
- Restoring a Course from the Trash — US [US-006] Entity and Relation Restore (Un-delete)
- Permanently deleting a Course — US [US-007] Permanent Deletion (Hard Delete)
- The same confirmation for Lessons with active enrollments — US [US-004] Deletion Confirmation for a Lesson in Use

## Additional Notes
- The authorization constraints for using deletion are not altered
```

**[END USER STORY ITERATION 3]**

---

**[START USER STORY ITERATION 4]**

#### Micro-Scope Reasoning for US-004

* **Value Focus:** Prevents the accidental removal of a Lesson with active enrollments.
* **Technical Boundaries:** Scope limited to the delete action from the existing lists/forms. **OUT:** The Trash page, restore and permanent deletion.
* **Split pattern:** Business Rule Variations, like US-003, applied to the Lesson entity. Here the rule has one extra variant: the Editor can archive (US-002) but cannot proceed if there are active enrollments.
* **INVEST Criteria Check:**
  * **Independent:** Yes, once US-002 has been iterated, the check can be implemented without depending on further concepts.
  * **Valuable:** Immediate (it avoids inadvertently deleting Lessons that are bringing value).
  * **Estimable:** Yes.
  * **Small:** Focused on a single action.
  * **Testable:** Yes, by enrolling a user in a lesson or in a course that references the lesson it is possible to verify that the check appears during the deletion phase.
* **Constraints check:** Handles the critical "active enrollments" rule, differentiating between Editor (block) and Manager/Admin (alert).

```markdown
---
id: US-004
title: Deletion Confirmation for a Lesson in Use
type: US
relations:
    "US-002":
        title: "Lesson Archiving (Move to Trash)"
        type: US
        relationType: BLOCKED_BY
        reason: "the confirmation plugs into the Lesson deletion flow introduced by US-002"
---

As an **advanced content manager (Manager, Admin)**, I want **to receive a confirmation request when I delete a Lesson with active enrollments**, so that I can remove it with full awareness.

## Outcome

Implementation of the check logic for Lessons currently in use. The action prevents immediate deletion through a warning, ensuring that the user deletes only what they are sure must be removed.

## Acceptance Criteria

### AC-1: Warning
**Given** a user with advanced content management permissions (Manager, Admin)
**And** they are editing a Lesson with active enrollments
**When** they perform the deletion
**Then** a warning asking whether to proceed is shown

### AC-2: Confirmation
**Given** a user with advanced content management permissions (Manager, Admin)
**And** they have requested the deletion of a Lesson with active enrollments
**And** the warning asking whether to proceed is displayed
**When** they confirm the operation
**Then** the deletion workflow proceeds

### AC-3: Refusal
**Given** a user with advanced content management permissions (Manager, Admin)
**And** they have requested the deletion of a Lesson with active enrollments
**And** the warning asking whether to proceed is displayed
**When** they cancel the operation
**Then** the deletion workflow is interrupted

### AC-4: Low-privilege handling
**Given** a user without advanced content management permissions (Editor)
**And** they are editing a Lesson with active enrollments
**When** they perform the deletion
**Then** a warning is shown without the possibility to proceed

## Out of Scope
- Moving the Lesson to the trash (loading, success and error of the deletion) — US [US-002] Lesson Archiving (Move to Trash)
- Viewing the deleted items in the Trash page — US [US-005] Trash View (Browsing Interface)
- Restoring a Lesson from the Trash — US [US-006] Entity and Relation Restore (Un-delete)
- Permanently deleting a Lesson — US [US-007] Permanent Deletion (Hard Delete)
- The same confirmation for Courses with active enrollments — US [US-003] Deletion Confirmation for a Course in Use

## Additional Notes
- The authorization constraints for using deletion are not altered
```

**[END USER STORY ITERATION 4]**

---

**[START USER STORY ITERATION 5]**

#### Micro-Scope Reasoning for US-005

* **Value Focus:** Provide visibility on the deleted items for audit or possible recovery.
* **Technical Boundaries:** **Read** only (Read-Only). Creation of the Trash page and of the list. **OUT:** The restore or hard delete actions.
* **Split pattern:** Operations (Read). Browsing the Trash is isolated from the restore (US-006) and permanent deletion (US-007) actions, following the Read vs Write rule. It won over a "complete Trash page" split because that would have exceeded 5 scenarios and mixed three operations.
* **INVEST Criteria Check:**
  * **Independent:** Yes.
  * **Valuable:** Visibility and control.
  * **Small:** Only UI and data fetch.
  * **Testable:** Yes (verify the list rendering).
* **Constraints check:** Respects the read/write separation so as not to create a giant story. Does not impose the type of display (card, table, etc).

```markdown
---
id: US-005
title: Trash View (Browsing Interface)
type: US
relations:
    "US-001":
        title: "Course Archiving (Move to Trash)"
        type: US
        relationType: BLOCKED_BY
        reason: "the Trash lists the Courses archived by US-001"
    "US-002":
        title: "Lesson Archiving (Move to Trash)"
        type: US
        relationType: BLOCKED_BY
        reason: "the Trash lists the Lessons archived by US-002"
---

As a **content manager (Editor, Manager, Admin)**, I want **to access a "Trash" section**, so that I can view the list of deleted content and check what can be recovered or permanently removed.

## Outcome

Creation of the "Trash" page, containing a list filtered according to the permissions of the logged-in user.

## Acceptance Criteria

### AC-1: Access and Navigation
**Given** a content manager user (Editor/Manager/Admin)
**When** they open the application
**Then** the "Trash" entry is available in the navigation
**And** it leads to the list page of the deleted content.

### AC-2: Loading and List Filtered by Role (Data Privacy)
**Given** a content manager user (Editor/Manager/Admin)
**When** they access the Trash page
**Then** a loading indicator is shown in place of the list
**And** when data retrieval finishes the indicator disappears
**And** the **Editor** sees only the deleted Lessons under their responsibility
**And** the **Manager** sees the deleted Courses and Lessons under their responsibility (including those of their editors)
**And** the **Admin** sees all the deleted entities in the system.

### AC-3: Empty State
**Given** a user who has no items in the trash
**When** they access the Trash page
**Then** a loading indicator is shown in place of the list
**And** when data retrieval finishes the indicator disappears
**And** they see an empty-state illustration or text: "The trash is empty".

### AC-4: Loading error
**Given** a content manager user (Editor/Manager/Admin)
**And** the system is unable to retrieve the deleted content
**When** they access the Trash page
**Then** a loading indicator is shown in place of the list
**And** when the attempt finishes the indicator disappears
**And** an error message is shown in place of the list
**And** an action to retry the loading is available.

### AC-5: Loading retry
**Given** a user viewing the Trash loading error
**When** they retry the loading
**Then** the system starts a new attempt
**And** the loading indicator is shown again in place of the error.

## Out of Scope
- Restoring an item from the Trash — US [US-006] Entity and Relation Restore (Un-delete)
- Permanently deleting an item from the Trash — US [US-007] Permanent Deletion (Hard Delete)

## Additional Notes
- for each item the following data are shown
  - Name (Course or Lesson)
  - Type (distinctive Course/Lesson icon)
  - Deletion Date
  - **Enrollments**: Icon/Indicator if there are enrollments.
```

**[END USER STORY ITERATION 5]**

---

**[START USER STORY ITERATION 6]**

#### Micro-Scope Reasoning for US-006

* **Value Focus:** Restore.
* **Technical Boundaries:** Only the **Restore** action (Un-delete). Includes the complex re-association logic.
* **Split pattern:** Operations (Restore). A write action separated from the list (US-005) and from permanent deletion (US-007): each one has its own asynchronous states and its own role rules.
* **INVEST Criteria Check:**
  * **Independent:** Depends on the list (US-005) for the UI interaction.
  * **Valuable:** High (recovery from mistakes).
  * **Small:** Specific restore logic.
  * **Testable:** Yes.
* **Constraints check:** Must handle restoring the relations.

```markdown
---
id: US-006
title: Entity and Relation Restore (Un-delete)
type: US
relations:
    "US-005":
        title: "Trash View (Browsing Interface)"
        type: US
        relationType: BLOCKED_BY
        reason: "the restore action starts from the Trash list"
---

As an **Authorized User**, I want **to restore an item from the Trash**, so that it becomes available to users again and, in the case of Lessons, its links to the Courses are restored.

## Outcome

Implementation of the "Restore" action in the Trash list. Handles the inverse state change and referential integrity.

## Acceptance Criteria

### AC-1: Restore
**Given** an item in the Trash
**When** the user restores the item
**Then** a loading indicator is shown on the item
**And** the user cannot interact with the item while the operation is in progress
**And** when processing finishes the indicator disappears
**And** the item is removed from the Trash list
**And** it becomes visible again in the lists of the state it had before deletion
**And** the system notifies the successful restore

### AC-2: Restore error
**Given** an item in the Trash
**And** the system is unable to restore it
**When** the user restores the item
**Then** a loading indicator is shown on the item
**And** the user cannot interact with the item while the operation is in progress
**And** when the attempt finishes the indicator disappears
**And** error feedback is shown
**And** the user can interact with the item again and repeat the restore

## Out of Scope
- Browsing the Trash list the restore starts from — US [US-005] Trash View (Browsing Interface)
- Permanently deleting an item from the Trash — US [US-007] Permanent Deletion (Hard Delete)
- Choosing the state (draft or published) to restore the item into — future story, needed only if the state before deletion turns out not to be recoverable

## Additional Notes
- it is assumed that the state before deletion can be recovered
```

**[END USER STORY ITERATION 6]**

---

**[START USER STORY ITERATION 7]**

#### Micro-Scope Reasoning for US-007

* **Value Focus:** Cleanup and GDPR compliance (Right to be forgotten).
* **Technical Boundaries:** **Hard Delete**. Destruction of the data.
* **Split pattern:** Operations (permanent Delete). The last operation of the lifecycle, separated from restore because it is irreversible and has its own role rules.
* **INVEST Criteria Check:**
  * **Independent:** Yes.
  * **Valuable:** System maintenance.
  * **Small:** Delete action with confirmation.
  * **Testable:** Yes (the record must no longer exist either in the public lists or in the trash).
* **Constraints check:** "Allows permanent removal... depending on the role". I assume the Editor can do it on their own items (as per the draft: "An editor user can delete a lesson...").

```markdown
---
id: US-007
title: Permanent Deletion (Hard Delete)
type: US
relations:
    "US-005":
        title: "Trash View (Browsing Interface)"
        type: US
        relationType: BLOCKED_BY
        reason: "the permanent deletion action starts from the Trash list"
---

As an **Authorized User**, I want **to permanently delete an item from the Trash**, so that I can free up space and permanently remove obsolete or incorrect data.

## Outcome

Implementation of the final destructive action. The removed data will no longer be recoverable.

## Acceptance Criteria

### AC-1: Irreversibility Warning (Safety Net)
**Given** an item in the Trash list
**When** the user requests the permanent deletion
**Then** the system asks for an explicit confirmation that flags the operation as irreversible

### AC-2: Deletion Execution
**Given** the user has confirmed the permanent deletion of an item
**When** the process completes successfully
**Then** the item is permanently removed
**And** it disappears from the Trash list.

### AC-3: Visibility for Editor
**Given** an Editor user
**When** they access the trash
**Then** they can permanently delete ONLY the Lessons under their responsibility.

### AC-4: Visibility for Manager
**Given** a Manager user
**When** they access the trash
**Then** they can permanently delete their own Courses and Lessons and those of their Editors.

## Out of Scope
- Browsing the Trash list the deletion starts from — US [US-005] Trash View (Browsing Interface)
- Restoring an item instead of deleting it — US [US-006] Entity and Relation Restore (Un-delete)

## Additional Notes
- an editor user can permanently delete ONLY the Lessons under their responsibility.
- a Manager user can permanently delete their own Courses/Lessons and those of their Editors.
- an admin user can permanently delete anything.

## Risks
- **Relation Integrity:** If a Course is permanently deleted, make sure the associated Lessons are not left with broken references.
```

**[END USER STORY ITERATION 7]**

---

### [FINAL CHECK]

I split the draft into 7 INVEST User Stories.

1. US-001 Course Archiving
2. US-002 Lesson Archiving
3. US-003 Deletion Confirmation for a Course in Use
4. US-004 Deletion Confirmation for a Lesson in Use
5. US-005 Trash View (Browsing Interface)
6. US-006 Entity and Relation Restore (Un-delete)
7. US-007 Permanent Deletion (Hard Delete)

All the requirements of the draft (Buttons, Menu, List fields, Role assumptions, Integrity risks) have been mapped to specific Acceptance Criteria.

**Improvements:**

- US-005, US-006 and US-007 handle Courses and Lessons together because the user asked to manage them under a single "trash" page, but better US (smaller and better detailed) would be obtained by splitting the trash page into multiple tabs per entity or multiple sub-navigations for the entities (Variations in Data pattern, as for US-001/US-002); this way you would get:
  - course trash view
  - lesson trash view
  - course restore
  - lesson restore
  - course deletion
  - lesson deletion
- For US-006 the assumption was made that it is possible to trace back to the initial state. If that were not the case, US-006 could be split with these criteria:
  - option 1: restore with a choice of state (draft or published)
  - option 2: restore always in draft state
  - option 3: two US for restoring into the specific state

### [SUMMARY]

The following 7 User Stories are ready for the backlog and can be developed in parallel or sequentially in the same sprint, respecting the declared `BLOCKED_BY` relations. The `US-00x` ids are local and permanent; the ids of the task manager are linked to them by `/speckit.sync`.
````

---

## Example 2 — Dense requirement with temporal logic (Store-Rep reassignment)

What it teaches: how to break down a single sentence, dense with actors and with a temporal variable, separating the read-only interface from the action, and what the second actor can *see* from what they *can no longer do*. The effective date is handled in the scenarios, not in separate stories.

### User input

```text
as an area manager user, I want to be able to change the assignments of the stores to my reps. the rep will be able to consult the previous visits to the stores they no longer have in visibility, but will no longer be able to enter visits on them from the date I specify as the start of the new visibility
```

### Expected output

````markdown
# Phase 1: MACRO-ANALYSIS

* **Request:** An "Area Manager" user must be able to reassign "Stores" (retail outlets) among their own "Reps" (sales representatives), specifying a start-of-validity date for the new assignment. Following this reassignment, the original Rep must keep read-only access to the history of the visits made to that store, but the system must prevent them from recording new visits from the effective date of the reassignment.

* **Working criterion:** The fundamental principle is context integrity: in the absence of critical details about the business, the user persona or the system constraints, it is imperative to stop the process and ask for clarification rather than base the generation on assumptions. Every User Story produced must strictly adhere to the Connextra format, placing a real human or business actor at the centre — never a technical role — and articulating a value distinct from the action itself (`As a... I want... so that...`). To ensure release quality, stories must respect the INVEST criteria (independent, negotiable, valuable, estimable, testable), taking the shape of "vertical slices" of working software that can be completed in a single sprint. This requires an aggressive splitting strategy that sharply separates read operations from write operations and avoids any horizontal slicing based on architectural layers. The Acceptance Criteria must use exclusively the Gherkin syntax (`Given`, `When`, `Then`) to describe observable behaviours, ensuring holistic coverage that includes the standard path, the edge cases and the explicit handling of asynchronous states such as loading, errors or absence of data. Finally, there is an absolute ban on introducing "phantom UI" or prescriptive descriptions of the interface: every visual element mentioned must be fully functional within the current story and defined by the user's intent, not by the mechanics of the click (no `click the green button`, yes `confirm the operation`).

### Phase 2: ITERATIVE DRAFTING

**[START USER STORY ITERATION 1]**

#### Micro-Scope Reasoning for US-001

* **Value Focus:** Allow the Area Manager to consult the current distribution of Stores across Reps in order to make strategic reassignment decisions.
* **Technical Boundaries:** Exclusively **Read** (Read-Only). Display of the list of active assignments. **OUT:** Any edit or deletion action.
* **Split pattern:** Operations (Read), following the Read vs Write rule. Browsing the assignments is isolated from the reassignment action (US-002): it has its own asynchronous states (loading, empty, error) and can be released on its own as a territory analysis tool.
* **INVEST Criteria Check:**
  * Is it independent? Yes.
  * Is it negotiable? Yes, it does not prescribe whether it is a table, a tree or a card view.
  * Is it valuable? Yes, it provides the context needed to operate.
  * Is it estimable? Yes, a simple read of relational data.
  * Is it the right size? Yes.
  * Is it testable? Yes.
* **Constraints check:** Respects the rule of isolating the View from the Action.

```markdown
---
id: US-001
title: Store-Rep Assignments View
type: US
---

As an **Area Manager**, I want **to view the list of the current assignments between my Reps and the Stores**, so that I can assess the territory coverage before making changes.

## Outcome

Creation of an interface that lists the active relations between the Reps managed by the Area Manager and the Stores assigned to them.

## Acceptance Criteria

### AC-1: List Browsing
**Given** an Area Manager user
**When** they access the territory management section
**Then** a loading indicator is shown
**And** when data retrieval finishes the indicator disappears
**And** they see the list of the Reps under their responsibility
**And** for each Rep, they can see the Stores currently assigned.

### AC-2: No Data (Empty State)
**Given** an Area Manager user
**And** there are no assignments between Reps and Stores
**When** they access the territory management section
**Then** a loading indicator is shown
**And** when data retrieval finishes the indicator disappears
**And** they see an empty-state message indicating the absence of data ("No assignments found").

### AC-3: Loading Error
**Given** an Area Manager user
**And** the system is unable to retrieve the assignment matrix
**When** they access the territory management section
**Then** a loading indicator is shown
**And** when the attempt finishes the indicator disappears
**And** an error message is shown ("Unable to load the assignments")
**And** an action to retry the loading is present.

### AC-4: Loading retry
**Given** an Area Manager user viewing the assignments loading error
**When** they retry the loading
**Then** the system starts a new attempt
**And** the loading indicator is shown again in place of the error.

## Out of Scope
- Reassigning a Store to another Rep — US [US-002] Store Reassignment with Effective Date (Area Manager)
- Deleting an assignment — not planned
```

**[END USER STORY ITERATION 1]**

---

**[START USER STORY ITERATION 2]**

#### Micro-Scope Reasoning for US-002

* **Value Focus:** Allow the Area Manager to actually change the territories with forward-planning logic (Effective date).
* **Technical Boundaries:** Only **Write/Action** and input validation. Handling of the asynchronous save state.
* **Split pattern:** Operations (Update): the reassignment as a transactional action separate from reading (US-001). The effective date was not extracted with Business Rule Variations because it is a single rule, not a variant: without it the action makes no sense, so it lives in the scenarios of this story.
* **INVEST Criteria Check:**
  * Is it independent? It depends at UI level on US-001 for the trigger, but the business logic is isolated.
  * Is it valuable? Extremely, it is the core business of the request.
  * Is it testable? Yes, the time limits can be simulated in the tests.
* **Constraints check:** The BDD criteria explicitly map success, error and loading, as well as the temporal validation.

```markdown
---
id: US-002
title: Store Reassignment with Effective Date (Area Manager)
type: US
relations:
    "US-001":
        title: "Store-Rep Assignments View"
        type: US
        relationType: BLOCKED_BY
        reason: "the reassignment starts from the list of the current assignments"
---

As an **Area Manager**, I want **to move a Store from one Rep to another by specifying a start-of-validity date**, so that I can plan territory changes in advance without interrupting current operations.

## Outcome

Implementation of the transactional logic that historically closes the previous assignment and creates a new one with a start date (Effective Date).

## Acceptance Criteria

### AC-1: Reassignment Entry
**Given** an Area Manager user
**When** they choose to reassign a Store in the assignments list
**Then** the system requires the selection of the new destination Rep
**And** requires entering a "New visibility start date".

### AC-2: Date Validation
**Given** an Area Manager user
**When** they enter a "Start date" earlier than today's date
**Then** the system blocks the operation
**And** shows a validation error ("The start date cannot be in the past").

### AC-3: Transaction Success
**Given** an Area Manager user
**And** the reassignment form is filled in correctly
**When** they confirm the save
**Then** the system shows a loading indicator
**And** the form controls are disabled to prevent double submissions
**And** when processing finishes the indicator disappears
**And** the successful reassignment is notified
**And** the interface leaves edit mode
**And** the assignments list updates to reflect the future/current state.

### AC-4: Save error
**Given** an Area Manager user
**And** the reassignment form is filled in correctly
**And** the system is unable to save the reassignment
**When** they confirm the save
**Then** the system shows a loading indicator
**And** the form controls are disabled to prevent double submissions
**And** when the attempt finishes the indicator disappears
**And** an error notification is shown
**And** the form controls are re-enabled with the entered data, so that the Area Manager can correct them and confirm again.

## Out of Scope
- Browsing the current assignments the reassignment starts from — US [US-001] Store-Rep Assignments View
- The former Rep's access to the past visits to the reassigned Store — US [US-003] Visit History for Previously Assigned Stores (Rep)
- Blocking the former Rep from entering new visits after the effective date — US [US-004] Block on New Visits to Reassigned Stores (Rep)
- Notifying the Rep when a Store is reassigned — not planned (raised as an open question in the summary)
```

**[END USER STORY ITERATION 2]**

---

**[START USER STORY ITERATION 3]**

#### Micro-Scope Reasoning for US-003

* **Value Focus:** Guarantee information continuity for the Rep (history).
* **Technical Boundaries:** Only **Read** for the Rep, and only the history **list**: loading, search and filters. **OUT:** the detail of the single visit and opening it from the list, which are a functional capability of their own (the visit detail already exists and this request does not change it).
* **Split pattern:** Business Rule Variations on the Rep side, combined with Operations (Read). The request describes two consequences for the Rep: what they can still see (this story) and what they can no longer do (US-004). Separated because they have an identical persona but opposite intent (continuity versus restriction) and independent tests. The scenarios stay on the "list" capability: no scenario about the visit detail.
* **INVEST Criteria Check:**
  * Is it independent? Yes, it evaluates visibility based on the consolidated data.
  * Is it testable? Yes, by logging in with a Rep account.
* **Constraints check:** Avoids describing *how* the UI is built, describes only the behaviour.

```markdown
---
id: US-003
title: Visit History for Previously Assigned Stores (Rep)
type: US
---

As a **Rep (Sales Representative)**, I want **to be able to see, in the history of my visits, the visits to the Stores no longer assigned to me as well**, so that I do not lose track of my past work and I keep the history of my field activity.

## Outcome

Adjustment of the Rep's visit filters and searches, ensuring that the history lists include the Stores whose assignment has expired, provided that at least one past visit made by the Rep themselves exists.

## Acceptance Criteria

### AC-1: History Access
**Given** a Rep user
**When** they access their own visit archive or history
**Then** the list includes the visits made to the Stores currently assigned
**And** includes the visits made in the past to the Stores no longer assigned.

### AC-2: Search for Former Stores
**Given** a Rep user
**When** they use the history search or filters
**Then** they can search for and find the visits by the Store's name, even if the Store has been reassigned to someone else.

## Out of Scope
- Opening the detail of a historical visit from the list — not planned (the visit detail already exists and this request does not change it)
- Restricting the commands available on the visit detail — not planned
- Blocking new visits on the Stores no longer assigned — US [US-004] Block on New Visits to Reassigned Stores (Rep)

## Assumptions
- It is assumed that the Rep must see only the visits made *by them* in the past, not those made by the new Rep who took over the Store.
- The detail of the single visit already exists and does not change with this request: opening a historical visit from the list and any restriction of the commands on the detail are outside this story, which covers only browsing the list.
```

**[END USER STORY ITERATION 3]**

---

**[START USER STORY ITERATION 4]**

#### Micro-Scope Reasoning for US-004

* **Value Focus:** Data integrity (data governance). Prevent unauthorized actions on other people's territories.
* **Technical Boundaries:** **Action/Validation**. Change of the Store selection behaviour and validation of the visit date.
* **Split pattern:** Business Rule Variations: the temporal blocking rule ("from the date I specify as the start") extracted as a story of its own, because it has three cases (date reached, future date, visit beyond the date) with their own tests and no new UI.
* **INVEST Criteria Check:**
  * Is it independent? Yes, it applies to the logic for creating a new visit.
  * Is it testable? Absolutely, by testing the temporal transition.
* **Constraints check:** Handles the key temporal variable of the request ("from the date I specify as the start"). No phantom UI: the non-selectable Store simply does not appear, it is not shown as disabled.

```markdown
---
id: US-004
title: Block on New Visits to Reassigned Stores (Rep)
type: US
relations:
    "US-002":
        title: "Store Reassignment with Effective Date (Area Manager)"
        type: US
        relationType: BLOCKED_BY
        reason: "the block is based on the effective date of the reassignment introduced by US-002"
---

As a **Rep (Sales Representative)**, I want **to enter new visits only on the Stores currently assigned to me**, so that territorial and data integrity is guaranteed.

## Outcome

Restriction of the Store selection when creating a new visit based on the effective date of the assignment, with validation of the visit date.

## Acceptance Criteria

### AC-1: Store not selectable (Effective Date Reached)
**Given** a Rep user
**And** a Store reassigned to another Rep with an effective date already reached
**When** they plan a new visit
**Then** the Store does not appear among the selectable ones.

### AC-2: Store still selectable (Future Effective Date)
**Given** a Rep user
**And** a Store reassigned to another Rep with a future effective date
**When** they plan a new visit
**Then** the Store is regularly selectable
**And** the visit can be saved.

### AC-3: Block on entering a visit beyond the effective date
**Given** a Rep user
**And** a Store reassigned to another Rep with a future effective date
**And** they have selected the Store for a new visit
**When** they enter a visit date later than the effective date
**Then** the system rejects the request

## Out of Scope
- Reassigning the Store and setting the effective date — US [US-002] Store Reassignment with Effective Date (Area Manager)
- Browsing the past visits to the Stores no longer assigned — US [US-003] Visit History for Previously Assigned Stores (Rep)
- Showing reassigned Stores as disabled in the selection — not planned (they simply do not appear)
```

**[END USER STORY ITERATION 4]**

---

### [FINAL CHECK]

I broke down a dense, ambiguous requirement with temporal variables into 4 highly granular User Stories.

* I separated the Area Manager's visual interface (US-001) from the complex reassignment action (US-002).
* I isolated the Rep's experience, sharply dividing what they can *see* (US-003, browsing the history list) from what they *can no longer do* (US-004, blocking rules). The history story stays on the "list" capability: no scenario opens the visit detail, which is a functional capability of its own.
* The use of the effective date ("New visibility start date") has been mapped explicitly in the Acceptance Criteria through Gherkin, handling the cases where the date is past, today or future.
* There is no "phantom UI": in US-004 the Store simply does not appear among the selectable ones, avoiding fake disabled controls or unclear behaviours.

### [SUMMARY]

The following 4 User Stories are ready for technical refinement and insertion into the backlog. The `US-00x` ids are local and permanent; the ids of the task manager are linked to them by `/speckit.sync`.

1. **US-001**: Store-Rep Assignments View (Area Manager)
2. **US-002**: Store Reassignment with Effective Date (Area Manager)
3. **US-003**: Visit History for Previously Assigned Stores (Rep)
4. **US-004**: Block on New Visits to Reassigned Stores (Rep)

Do you agree with the temporal handling (edge case) described in US-004, where the future assignment lets the current Rep keep working until the day of the actual change? Do you need to extract further notification logic (e.g. sending a notification to the Rep when a store is reassigned)?
````

---

## Example 3 — Blocking rule (offline data synchronization)

What it teaches: how to separate the user's proactive intent (synchronizing) from the system's coercive intent (blocking), changing persona in the second story. The "3 days" variable is made measurable as 72 hours.

### User input

```text
as a salesperson, I must be able to start the synchronization of the application's offline-usable data, this way I can work with up-to-date data. the system must prevent me from carrying out my normal work when the data on my device is older than 3 days.
```

### Expected output

````markdown
# Phase 1: MACRO-ANALYSIS

* **Request:** Implement a manual synchronization feature for the offline data for salespeople, including a business rule that blocks the application's operations if the data stored on the device turns out to be older than 3 days.

* **Working criterion:** The fundamental principle is context integrity: in the absence of critical details about the business, the user persona or the system constraints, it is imperative to stop the process and ask for clarification rather than base the generation on assumptions. Every User Story produced must strictly adhere to the Connextra format, placing a real human or business actor at the centre — never a technical role — and articulating a value distinct from the action itself (`As a... I want... so that...`). To ensure release quality, stories must respect the INVEST criteria (independent, negotiable, valuable, estimable, testable), taking the shape of "vertical slices" of working software that can be completed in a single sprint. This requires an aggressive splitting strategy that sharply separates read operations from write operations and avoids any horizontal slicing based on architectural layers. The Acceptance Criteria must use exclusively the Gherkin syntax (`Given`, `When`, `Then`) to describe observable behaviours, ensuring holistic coverage that includes the standard path, the edge cases and the explicit handling of asynchronous states such as loading, errors or absence of data. Finally, there is an absolute ban on introducing "phantom UI" or prescriptive descriptions of the interface: every visual element mentioned must be fully functional within the current story and defined by the user's intent, not by the mechanics of the click (no `click the green button`, yes `confirm the operation`).

### Phase 2: ITERATIVE DRAFTING

**[START USER STORY ITERATION 1]**

#### Micro-Scope Reasoning for US-001

* **Value Focus:** Allow the salesperson to actively update their local database in order to work with reliable information.
* **Technical Boundaries:** Only the manual trigger of the synchronization, the handling of the loading (asynchronous) states and the success/error notification.
* **Split pattern:** Workflow Steps. The voluntary synchronization action is the core step of the flow and is releasable and useful on its own; the coercive rule on stale data is a subsequent step (US-002) that presupposes it. It won over "a single story" because that would have mixed two opposite intents and exceeded 5 scenarios.
* **INVEST Criteria Check:** Fully respects the criteria; it is a standalone feature, estimable and objectively verifiable by simulating the connection conditions.
* **Constraints check:** Compliant. Separates the update action from the blocking rules (which will go in the next US).

```markdown
---
id: US-001
title: Manual Offline Data Synchronization
type: US
---

As a **Salesperson**, I want **to be able to start the offline data synchronization manually**, so that I can be certain of working in the field with the most up-to-date information possible.

## Outcome

Implementation of the feature for manually starting the update of the local database, with the related handling of the UI's asynchronous states.

## Acceptance Criteria

### AC-1: Synchronization Completed Successfully
**Given** a Salesperson user
**When** they request to start the data synchronization
**Then** the system shows a loading indicator
**And** temporarily disables the synchronization command to avoid multiple starts
**And** when the update of the local database finishes the indicator disappears
**And** updates the "Last update date and time" visible to the user
**And** shows a success notification.

### AC-2: Synchronization error
**Given** a Salesperson user
**And** the system is unable to complete the synchronization
**When** they request to start the data synchronization
**Then** the system shows a loading indicator
**And** temporarily disables the synchronization command to avoid multiple starts
**And** when the attempt finishes the indicator disappears
**And** shows an error message ("Unable to synchronize the data. Try again later.")
**And** re-enables the synchronization command to allow a new attempt.

### AC-3: No Connection at Start
**Given** a Salesperson user without a connection (offline)
**When** they try to start the data synchronization
**Then** the system blocks the request instantly
**And** shows a warning ("No internet connection. Connect to synchronize").

## Out of Scope
- Blocking the app when the local data is older than 72 hours — US [US-002] Operations Block for Stale Data (Over 3 Days)
- Automatic synchronization started without the user's request — not planned
- Incremental synchronization — future story (to be evaluated, see Risks)

## Additional Notes
- The interface must always clearly show the label "Last update: [Date and Time]" to give the user context.

## Risks
- Possible bottlenecks if many salespeople synchronize large volumes of data at the same time (consider an incremental synchronization).
```

**[END USER STORY ITERATION 1]**

---

**[START USER STORY ITERATION 2]**

#### Micro-Scope Reasoning for US-002

* **Value Focus:** Guarantee data governance and prevent commercial errors caused by the use of stale data (e.g. old prices, stock levels that are not real).
* **Technical Boundaries:** Only the check of the date of the last synchronization and the consequent blocking/unblocking of the operational UI.
* **Split pattern:** Business Rule Variations. The 72-hour threshold is a rule extracted from the base action: it has a different persona (whoever imposes the constraint, not whoever synchronizes), a different intent (coercive) and its own tests (manipulating the date of the last update).
* **INVEST Criteria Check:** Independent of the manual trigger, provides compliance value, small and highly testable by manipulating the date of the last synchronization.
* **Constraints check:** Compliant. Explicitly handles the "3 days" temporal variable stated in the request, made measurable as 72 hours.

```markdown
---
id: US-002
title: Operations Block for Stale Data (Over 3 Days)
type: US
relations:
    "US-001":
        title: "Manual Offline Data Synchronization"
        type: US
        relationType: BLOCKED_BY
        reason: "unblocking requires the manual synchronization introduced by US-001"
---

As a **Sales Manager (or Compliance System)**, I want **to prevent the Salesperson from operating in the app if the local data is older than 3 days**, so that no contracts or orders are concluded on the basis of price lists, master data or availability that are no longer valid.

## Outcome

Implementation of a check, when the app is opened or resumed, that verifies the date of the last synchronization. If more than 72 hours have passed, the app is blocked (Hard Stop) until the update has been completed.

## Acceptance Criteria

### AC-1: Stale Data Detection (Hard Stop)
**Given** a Salesperson user who opens or resumes the application
**When** the system detects that the last data update happened more than 72 hours (3 days) ago
**Then** the standard operational interface is blocked in a way that cannot be dismissed
**And** a blocking message is shown ("Stale data. You must synchronize to keep working")
**And** a single possible action is offered: "Sync Now".

### AC-2: Unblock After Synchronization
**Given** a Salesperson user
**And** the application is blocked because of stale data
**When** they successfully perform the mandatory synchronization
**Then** the operational block is removed
**And** the user is redirected to the dashboard or to the standard workflow.

### AC-3: Valid Data (No Block)
**Given** a Salesperson user who opens the application
**When** the system detects that the last update happened within 72 hours
**Then** the user regularly accesses all the operational features without interruptions.

## Out of Scope
- The synchronization itself (trigger, loading, success, error and offline handling) — US [US-001] Manual Offline Data Synchronization
- Verifying the device clock against the network time — not planned (the device clock is assumed to be aligned with the network)

## Assumptions
- The calculation of the 3 days (72 hours) is based on the device's system time, which is assumed to be aligned with the network.
- The blocked state inhibits entering new orders/customers, but does not destroy any drafts previously saved locally.
```

**[END USER STORY ITERATION 2]**

---

### [FINAL CHECK]

I broke down the requirement into 2 distinct User Stories:

1. **US-001**: Focuses on the user's voluntary action of downloading the data, handling the feedback infrastructure (loading, success, error, offline).
2. **US-002**: Isolates the restrictive business rule. Had we merged everything, the story would have become too big, mixing the salesperson's proactive intent with the system's coercive intent.

The stories respect the INVEST and BDD criteria, sharply separating the update action from the interface blocking logic.

### [SUMMARY]

The following 2 User Stories are structured, deterministic and ready for the sprint backlog. The `US-00x` ids are local and permanent; the ids of the task manager are linked to them by `/speckit.sync`.

1. **US-001**: Manual Offline Data Synchronization
2. **US-002**: Operations Block for Stale Data (Over 3 Days)
````

---

## Example 4 — Horizontal slicing → request for clarification (newsletter library)

What it teaches: a purely architectural request is horizontal slicing. The skill stops (constraint 0), asks for the functional value and the persona, and only then produces a vertical slice, preserving the technical constraints in the Additional Notes instead of creating a technical story.

### User input (turn 1)

```text
🛠 Technical Specifications

1. Library Architecture (Abstraction Layer)
The library must follow the Provider/Adapter pattern. It must not contain logic tied to a specific vendor in its "core".
NewsletterProvider (Interface): Define a standard contract that every adapter will have to implement.
NewsletterService: A class that injects the provider and is used by the rest of the application.

2. Provider Implementation (Adapter)
Create a concrete implementation (e.g. AcmeMailNewsletterProvider or MailHubProvider).
The configuration (API Key, List ID) must be retrieved through environment variables (process.env) or a central config file.
```

### Expected output (turn 1) — DO NOT generate

````markdown
This request is a Horizontal Slicing strongly oriented towards architecture. Answer these questions so that I can proceed:

1. What is the functional value for which this technical solution was described?
2. Who is the User Persona? The Visitor User (for the subscription) or someone else?
````

### User input (turn 2)

```text
1. there is a section in the homepage that lets you subscribe to the newsletter
2. A user, it doesn't matter whether authenticated or not..
```

### Expected output (turn 2)

````markdown
# Phase 1: MACRO-ANALYSIS

* **Request:** Implementation of a specific section in the Homepage that allows subscribing to the newsletter. The feature must be accessible both to logged-in users and to anonymous visitors. The business goal is lead acquisition for commercial purposes.

* **Working criterion:** The fundamental principle is context integrity: in the absence of critical details about the business, the user persona or the system constraints, it is imperative to stop the process and ask for clarification rather than base the generation on assumptions. Every User Story produced must strictly adhere to the Connextra format, placing a real human or business actor at the centre — never a technical role — and articulating a value distinct from the action itself (`As a... I want... so that...`). To ensure release quality, stories must respect the INVEST criteria (independent, negotiable, valuable, estimable, testable), taking the shape of "vertical slices" of working software that can be completed in a single sprint. This requires an aggressive splitting strategy that sharply separates read operations from write operations and avoids any horizontal slicing based on architectural layers. The Acceptance Criteria must use exclusively the Gherkin syntax (`Given`, `When`, `Then`) to describe observable behaviours, ensuring holistic coverage that includes the standard path, the edge cases and the explicit handling of asynchronous states such as loading, errors or absence of data. Finally, there is an absolute ban on introducing "phantom UI" or prescriptive descriptions of the interface: every visual element mentioned must be fully functional within the current story and defined by the user's intent, not by the mechanics of the click (no `click the green button`, yes `confirm the operation`).

### Phase 2: ITERATIVE DRAFTING

**[START USER STORY ITERATION 1]**

#### Micro-Scope Reasoning for US-001

* **Value Focus:** Allow anyone browsing the Homepage to express commercial interest by leaving their contact.
* **Technical Boundaries:** **Vertical Slice UI + Logic.** Includes the visual section in the Homepage, the input validation and the submission to the subscription service.
* **Split pattern:** None. The original request was horizontal slicing (library, interface, adapter); once the functional value was recovered, a single vertical slice remains. The architectural constraints do not become a technical story: they go in the Additional Notes of this story.
* **INVEST Criteria Check:**
  * **Independent:** Yes, it is the entry point of the service.
  * **Valuable:** Real-time lead acquisition.
  * **Small:** Limited to subscribing from the Homepage.
  * **Testable:** Yes, by entering an email in the form and checking the response.
* **Constraints check:** Avoids prescriptive UI but defines the asynchronous behaviours.

```markdown
---
id: US-001
title: Newsletter Subscription on the Homepage
type: US
---

As a **Visitor (Anonymous or Logged-in)**, I want **to subscribe to the newsletter through the dedicated section on the Homepage**, so that I receive commercial communications and stay up to date on the offers.

## Outcome

Implementation of the "Newsletter" section on the Homepage.

## Acceptance Criteria

### AC-1: Display and Access
**Given** a user browsing the Homepage
**When** they scroll the page down to the newsletter section
**Then** they see a field for entering the email and a confirmation command.

### AC-2: Successful subscription
**Given** a user who has entered a valid email address
**When** they confirm the subscription
**Then** the system shows a loading indicator
**And** the confirmation command cannot be triggered again while the operation is in progress
**And** when processing finishes the indicator disappears
**And** a success message ("Thanks for subscribing!") is shown in place of the form.

### AC-3: Error handling
**Given** a user who has entered a valid email address
**And** the system is unable to register the subscription
**When** they confirm the subscription
**Then** the system shows a loading indicator
**And** the confirmation command cannot be triggered again while the operation is in progress
**And** when the attempt finishes the indicator disappears
**And** a temporary error notification is shown
**And** the confirmation command is available again, with the entered email, without reloading the page.

## Out of Scope
- A standalone technical story for the newsletter library (Provider/Adapter) — not planned (its architectural constraints live in the Additional Notes of this story)
- Subscribing from pages other than the Homepage — not planned

## Additional Notes

### 🛠 Backend architecture
The backend must not call the MailHub features directly, but build a library that acts as an abstraction. The library must follow the Adapter design pattern.
The configuration (API Key, List ID) of the concrete provider must be retrieved through environment variables (process.env) or a central config file.

## Assumptions
- It is assumed that the user must explicitly accept the privacy terms through a control (checkbox) before submitting.
```

**[END USER STORY ITERATION 1]**

---

### [FINAL CHECK]

I turned the business need (Homepage section) into:

1. **US-001** covers the user experience and the immediate value (registration).

This split avoids creating a pure "technical User Story" (horizontal slicing) and ensures that the frontend and backend teams have clear acceptance criteria on how the UI must interact with the abstraction service.

### [SUMMARY]

The final stories ready for the development cycle are (local id; the task manager's id is linked by `/speckit.sync`):

1. **US-001: Newsletter Subscription on the Homepage** (UX Focus and Business Value)
````

---

## Example 5 — Refinement with technical specifications to preserve ("Notify Me")

What it teaches: a refinement of an existing draft in which, despite 7 scenarios, the story is NOT split because the value atomicity exception applies (the "alien question"): separating the display of the form from the submission of the metadata would produce unreleasable pieces. The technical specifications given by the user remain, but the scenarios describe observable behaviours.

### User input

```text
Refine the "Notify Me" User Story for PDPs in Sold Out/Coming Soon state.

We need to integrate the form with MailHub (list: Newsletter).

Technical specifications:
1. Do not create new records if the email already exists, but add a product-specific Tag.
2. To let marketing rebuild the product card in the marketing email, send as metadata (merge fields): Product ID, Title, Image URL, Short Description, Category, Status (Sold out/Coming soon), Product URL.
3. The Price must be sent as a pure numeric value.
4. Mandatory privacy flag required.
5. Feedback: show a thank you message and hide the form when the operation succeeds.

<us>
User Story

As a user interested in an unavailable product I want to be able to leave my contact details to be notified when the product becomes available again or is launched, so as not to miss the opportunity to buy in the future.

Acceptance Criteria

[Signup box display]
Given that I am on the detail page of a "Sold out" or "Coming soon" product
When I view the side box (desktop) or the dedicated section (mobile)
Then the system must show the title "Sign up for updates" (or "Keep me updated") and the input fields "Name" and "Email".

[Validation and Privacy consent]
Given that I am entering my data in the update form
When I click on the "Keep me updated" button
Then the system must check that the fields are filled in, that the email is valid and that the mandatory Privacy Policy acknowledgement checkbox is selected.

[Subscription confirmation]
Given that I have submitted my data correctly
When the operation succeeds
Then the system must register the user's interest in that specific product in the marketing database and show a thank-you message (or close the popup on mobile).
</us>
```

### Expected output

````markdown
# Phase 1: MACRO-ANALYSIS

... (omitted for brevity: Request and Working criterion as in the previous examples) ...

### Phase 2: ITERATIVE DRAFTING

**[START USER STORY ITERATION 1]**

#### Micro-Scope Reasoning for US-001

* **Value Focus:** Converting a user interested in an unavailable product into a profiled lead.
* **Technical Boundaries:** Complete Vertical Slice: from the conditional display in the PDP to the submission of the data to the marketing provider.
* **Split pattern:** None, by value atomicity exception. A Workflow Steps split (form, then metadata submission) or a Business Rule Variations split (deduplication on its own) would produce engine parts that do not run: a form that does not submit or a submission that does not register the interest are not releasable. The 7 scenarios stay in a single story.
* **INVEST Criteria Check:** Respects independence and value.
* **Constraints check:** Despite the number of scenarios (7), the story is not split in order to preserve atomic integrity: separating the display of the form from the submission of the metadata would leave the story without releasable value.

```markdown
---
id: US-001
title: Subscription to "Notify Me" with Marketing Metadata Synchronization
type: US
---

As an **interested Visitor**, I want **to sign up to receive updates about an unavailable product**, so that I am contacted again with a personalized offer when it becomes purchasable again.

## Outcome

Implementation of the lead capture module in the PDP with automated submission of metadata and segmentation tags to the marketing provider.

## Acceptance Criteria

### AC-1: Conditional Display
**Given** a user on the product page
**When** the status is "Sold Out" or "Coming Soon"
**Then** the "Keep me updated" box appears with the Name, Email and Privacy fields.

### AC-2: Validation and Consent
**Given** the filled-in module
**When** the user confirms the submission without having accepted the Privacy Policy
**Then** the system prevents the submission and shows a validation error.

### AC-3: Metadata Synchronization
**Given** a submission in progress
**When** the system registers the interest with the marketing provider
**Then** it sends the email with the product Tags and the metadata: ID, Title, Image URL, Description, Category, Status and Product URL.

### AC-4: Price Formatting
**Given** the product metadata
**When** the price field is sent
**Then** the value must be transmitted as a pure number (without currency symbols).

### AC-5: Existing User Handling (Deduplication)
**Given** an email already present in the marketing database
**When** the user signs up for a new product
**Then** the system updates the existing record by adding the new Tag without overwriting the previous ones.

### AC-6: Success Feedback
**Given** valid data
**When** the user confirms the submission
**Then** a loading indicator is shown
**And** the module fields are disabled while the operation is in progress
**And** when processing finishes the indicator disappears
**And** the module disappears and a thank-you message appears.

### AC-7: Submission Error
**Given** valid data
**And** the system is unable to register the interest
**When** the user confirms the submission
**Then** a loading indicator is shown
**And** the module fields are disabled while the operation is in progress
**And** when the attempt finishes the indicator disappears
**And** an error message is shown
**And** the fields become editable again and the submission is available again.

## Out of Scope
- Sending the back-in-stock marketing email when the product becomes available again — not planned (marketing builds it from the metadata sent by this story)

## Additional Notes
- Use the existing "Newsletter" list on MailHub.
- Verify the correct mapping of the merge fields on the MailHub side before development.
```

**[END USER STORY ITERATION 1]**

---

### [FINAL CHECK]

The story exceeds the 2-5 scenario rule but is not split: every split tried produces an unreleasable piece (form without submission, submission without registration). This is the value atomicity exception case. The technical specifications provided by the user (provider, deduplication via tag, merge fields, numeric price) are preserved in the scenarios as observable behaviours and in the Additional Notes as integration constraints.

### [SUMMARY]

1. **US-001**: Subscription to "Notify Me" with Marketing Metadata Synchronization (local id; the task manager's id is linked by `/speckit.sync`)
````
