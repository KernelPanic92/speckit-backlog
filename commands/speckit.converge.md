## Preset `backlog` addendum

> This project uses the `backlog` preset. The rules below **refine the steps above**; where they conflict with the generic wording above, these rules win.

**Artifacts** — `spec.md` is the root PBI (MAP, EPIC or US) plus the spec envelope; the stories, epics, spikes and TASK PBIs live under `FEATURE_DIR/backlog/`. Load the stories (Connextra, Acceptance Criteria, Out of Scope) as part of the spec. There is no data-model.md or contracts/: Data Model and API Design / Contracts are sections of plan.md. Terms follow `.specify/memory/product.md` › Ubiquitous Language.

**Source references** — map the generic keys above to this project's keys:

| Generic key above | Key in this project |
|-------------------|---------------------|
| `FR-###` | `US-xxx/AC-n` — a Gherkin scenario of a story |
| `US1/AC2` | `US-001/AC-2` |
| `SC-###` | `SC-###` — Success Criteria of the envelope (unchanged); lane Metrics of a MAP count as Success Criteria of that lane |
| "P1 user story" | a story of the first Release Lane (map), the first story in release order (epic), the root US (story) |
| — | `US-xxx §Out of Scope` — code that builds an Out of Scope item is an `unrequested` finding |

**Appending tasks** — every appended task is a TASK PBI, so step 7 writes more than tasks.md:

1. Get the first free id with `uv run --no-project --quiet --with pyyaml --with jsonschema python .specify/presets/backlog/scripts/validate_backlog.py next-id TASK` instead of `T{M+1:03d}`.
2. For each finding, write a TASK file under `FEATURE_DIR/backlog/tasks/<ID>-<slug>.md` from the `pbi-task-template` template (resolve it with `.specify/scripts/bash/resolve-template.sh pbi-task-template --json`, or the PowerShell equivalent). Set `PARENT` to the story the finding traces to (none for constitution or plan findings), put the `<source-ref>` and `<gap-type>` in the Outcome, and list the Files observed as evidence.
3. Append the `## Phase N: Convergence` section to tasks.md with lines in the index format:

   ```markdown
   - [ ] TASK-042 [US-003] <imperative title> per US-003/AC-2 (partial) → [backlog/tasks/TASK-042-<slug>.md](backlog/tasks/TASK-042-<slug>.md)
   ```

4. Creating these TASK files is the only write allowed besides tasks.md: existing PBIs, spec.md and plan.md stay untouched.
5. Run `… validate_backlog.py check FEATURE_DIR` after appending; fix only the files you created. Run it as a standalone command (not chained with `;`, `&&` or pipes) so that it can be allow-listed in the agent's permissions.
