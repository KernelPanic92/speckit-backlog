"""Tests for scripts/validate_backlog.py.

Run from the repository root:
    uv run --no-project --with pytest --with pyyaml --with jsonschema pytest tests
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "validate_backlog.py"
FIXTURE = REPO / "tests" / "fixtures" / "valid"
SPEC = "specs/001-online-purchase"


def run(project: Path, *args: str) -> tuple[int, dict]:
    proc = subprocess.run([sys.executable, str(SCRIPT), *args], cwd=project, capture_output=True, text=True)
    return proc.returncode, json.loads(proc.stdout)


@pytest.fixture
def project(tmp_path: Path) -> Path:
    target = tmp_path / "project"
    shutil.copytree(FIXTURE, target)
    return target


def edit(project: Path, relative: str, old: str, new: str) -> None:
    path = project / SPEC / relative
    text = path.read_text()
    assert old in text, f"{old!r} not in {relative}"
    path.write_text(text.replace(old, new, 1))


def codes(result: dict) -> set:
    return {e["code"] for e in result["errors"]}


def test_valid_fixture_passes(project):
    code, result = run(project, "check", SPEC)
    assert code == 0, result
    assert result["errors"] == [] and result["warnings"] == []
    assert result["pbis"] == {"MAP": 1, "EPIC": 2, "US": 3, "SPIKE": 1, "TASK": 2}


def test_check_all(project):
    code, result = run(project, "check", "--all")
    assert code == 0 and result["checked"] == [SPEC]


def test_next_id(project):
    assert run(project, "next-id", "US")[1]["next"] == "US-004"
    assert run(project, "next-id", "task", "--count", "2")[1]["ids"] == ["TASK-003", "TASK-004"]
    assert run(project, "next-id", "EPIC")[1]["next"] == "EPIC-003"


def test_next_id_unknown_type(project):
    assert run(project, "next-id", "STORY")[0] == 2


def test_locate_descendants(project):
    code, result = run(project, "locate", "EPIC-002", "--descendants")
    assert code == 0 and not result["is_root"]
    assert [d["id"] for d in result["descendants"]] == ["US-002", "US-003", "SPIKE-001"]


def test_locate_unknown(project):
    assert run(project, "locate", "US-404")[0] == 1


MUTATIONS = [
    ("schema", "backlog/stories/US-001-catalog-list.md", "type: US", "type: US\nstatus: done"),
    ("placeholder", "backlog/epics/EPIC-001-discovery.md", "## Outcome\n", "## Outcome\n\n{{outcomeDescription}}\n"),
    ("relation-order", "backlog/stories/US-003-saved-card.md",
     '    "EPIC-002":\n        title: "Checkout"\n        type: EPIC\n        relationType: PARENT\n        reason: "Parent epic"\n    "US-002":\n        title: "Card payment"\n        type: US\n        relationType: BLOCKED_BY\n        reason: "A card can be saved only during a card payment"\n',
     '    "US-002":\n        title: "Card payment"\n        type: US\n        relationType: BLOCKED_BY\n        reason: "A card can be saved only during a card payment"\n    "EPIC-002":\n        title: "Checkout"\n        type: EPIC\n        relationType: PARENT\n        reason: "Parent epic"\n'),
    ("unknown-id", "backlog/stories/US-003-saved-card.md", '    "US-002":', '    "US-099":'),
    ("relation-type", "backlog/stories/US-001-catalog-list.md", "        type: EPIC\n", "        type: MAP\n"),
    ("hierarchy", "backlog/spikes/SPIKE-001-payment-provider.md",
     '    "US-002":\n        title: "Card payment"\n        type: US',
     '    "MAP-001":\n        title: "Online purchase"\n        type: MAP'),
    ("multiple-parents", "backlog/stories/US-001-catalog-list.md", '        reason: "Parent epic"\n',
     '        reason: "Parent epic"\n    "EPIC-002":\n        title: "Checkout"\n        type: EPIC\n        relationType: PARENT\n        reason: "Second parent"\n'),
    ("out-of-scope", "backlog/stories/US-003-saved-card.md", "## Out of Scope", "## Exclusions"),
    ("ac-id", "backlog/stories/US-001-catalog-list.md", "### AC-2: Empty catalog", "### Empty catalog"),
    ("ac-sequence", "backlog/stories/US-001-catalog-list.md", "### AC-2: Empty catalog", "### AC-3: Empty catalog"),
    ("lane-order", "spec.md", "  * US [US-002] Card payment\n", "  * US [US-003] Saved card\n"),
    ("lane-missing", "spec.md", "  * US [US-003] Saved card\n", ""),
    ("not-indexed", "spec.md", "- [US [US-003] Saved card](backlog/stories/US-003-saved-card.md)\n", ""),
    ("broken-link", "spec.md", "backlog/stories/US-003-saved-card.md", "backlog/stories/US-003-saved.md"),
    ("task-file-missing", "tasks.md", "## Parallel Example",
     "- [ ] TASK-003 Ghost task → [backlog/tasks/TASK-003-ghost.md](backlog/tasks/TASK-003-ghost.md)\n\n## Parallel Example"),
    ("task-not-listed", "tasks.md",
     "- [ ] TASK-002 [US-001] Catalog list query → [backlog/tasks/TASK-002-catalog-list-query.md](backlog/tasks/TASK-002-catalog-list-query.md)\n", ""),
    ("cycle", "backlog/stories/US-002-card-payment.md", '    "US-001":', '    "US-003":'),
    ("root-type", "spec.md", "type: MAP", "type: TASK"),
]


@pytest.mark.parametrize("expected, relative, old, new", MUTATIONS, ids=[m[0] for m in MUTATIONS])
def test_detects(project, expected, relative, old, new):
    edit(project, relative, old, new)
    code, result = run(project, "check", SPEC)
    assert code == 1
    assert expected in codes(result), result["errors"]


def test_checkbox_lines_that_are_not_tasks(project):
    edit(project, "tasks.md", "## Phase 2: Walking Skeleton",
         "## Task Completion Criteria\n\n- [ ] Unit tests for new code\n- [ ] Feature-flag wrapped when needed\n- [ ] API contract respected\n\n## Phase 2: Walking Skeleton")
    code, result = run(project, "check", SPEC)
    assert code == 0, result["errors"]


def test_duplicate_id_and_file_name(project):
    edit(project, "backlog/tasks/TASK-002-catalog-list-query.md", "id: TASK-002", "id: TASK-001")
    result = run(project, "check", SPEC)[1]
    assert {"duplicate-id", "file-name"} <= codes(result)


def test_wrong_folder(project):
    src = project / SPEC / "backlog/spikes/SPIKE-001-payment-provider.md"
    src.rename(project / SPEC / "backlog/tasks/SPIKE-001-payment-provider.md")
    edit(project, "spec.md", "backlog/spikes/SPIKE-001", "backlog/tasks/SPIKE-001")
    assert "wrong-folder" in codes(run(project, "check", SPEC)[1])


def test_mutual_related_is_an_error_but_spike_pattern_is_not(project):
    # US-002 BLOCKED_BY SPIKE-001 while SPIKE-001 has US-002 as PARENT: legitimate (valid fixture).
    edit(project, "backlog/stories/US-003-saved-card.md", '        reason: "A card can be saved only during a card payment"\n',
         '        reason: "A card can be saved only during a card payment"\n    "US-001":\n        title: "Catalog list"\n        type: US\n        relationType: RELATED\n        reason: "Same shopper journey"\n')
    edit(project, "backlog/stories/US-001-catalog-list.md", '        reason: "Parent epic"\n',
         '        reason: "Parent epic"\n    "US-003":\n        title: "Saved card"\n        type: US\n        relationType: RELATED\n        reason: "Same shopper journey"\n')
    assert "inverse-relation" in codes(run(project, "check", SPEC)[1])


def test_external_ids_are_warnings(project):
    edit(project, "backlog/stories/US-003-saved-card.md", '    "US-002":', '    "CU-86c1x2":')
    result = run(project, "check", SPEC)[1]
    assert "external-id" in {w["code"] for w in result["warnings"]}
    assert "unknown-id" not in codes(result)


# --- external references and sync planning ---------------------------------------------------

def test_sync_plan_initially_creates_everything_parents_first(project):
    code, result = run(project, "sync-plan", "clickup", SPEC)
    assert code == 0 and result["summary"] == {"create": 9, "update": 0, "unchanged": 0}
    order = [item["id"] for item in result["items"]]
    for item in result["items"]:
        if item["parent"]:
            assert order.index(item["parent"]) < order.index(item["id"]), item["id"]
    assert order[0] == "MAP-001"
    us2 = next(i for i in result["items"] if i["id"] == "US-002")
    assert us2["ancestors"] == ["EPIC-002", "MAP-001"]
    assert {r["id"] for r in us2["relations"]} == {"US-001", "SPIKE-001"}


def test_set_external_then_plan_is_unchanged_until_the_pbi_changes(project):
    code, result = run(project, "set-external", "US-001", "clickup", "--id", "86c1x2abc", "--key", "DE-14620",
                       "--url", "https://app.clickup.com/t/86c1x2abc", "--hash-current")
    assert code == 0 and result["external"]["clickup"]["key"] == "DE-14620"
    assert run(project, "check", SPEC)[0] == 0          # the schema accepts the external block
    plan = {i["id"]: i for i in run(project, "sync-plan", "clickup", SPEC)[1]["items"]}
    assert plan["US-001"]["action"] == "unchanged"
    assert plan["TASK-002"]["parent_external"]["id"] == "86c1x2abc"
    edit(project, "backlog/stories/US-001-catalog-list.md", "The catalog shows every product for sale.",
         "The catalog shows every product for sale, newest first.")
    plan = {i["id"]: i for i in run(project, "sync-plan", "clickup", SPEC)[1]["items"]}
    assert plan["US-001"]["action"] == "update"
    assert plan["US-001"]["external"]["id"] == "86c1x2abc"


def test_set_external_keeps_the_file_and_other_tools(project):
    path = project / SPEC / "backlog/stories/US-001-catalog-list.md"
    before_body = path.read_text().split("\n---\n", 1)[1]
    run(project, "set-external", "US-001", "clickup", "--id", "86c1x2abc")
    run(project, "set-external", "US-001", "multica", "--id", "0f8e5a1c-1111-4c2b-9d1e-0123456789ab", "--key", "MUL-12")
    run(project, "set-external", "US-001", "clickup", "--url", "https://app.clickup.com/t/86c1x2abc")
    text = path.read_text()
    assert text.split("\n---\n", 1)[1] == before_body
    assert text.count("external:") == 1
    located = run(project, "locate", "US-001")[1]
    assert located["external"]["clickup"] == {"id": "86c1x2abc", "url": "https://app.clickup.com/t/86c1x2abc"}
    assert located["external"]["multica"]["key"] == "MUL-12"
    run(project, "set-external", "US-001", "clickup", "--remove")
    assert set(run(project, "locate", "US-001")[1]["external"]) == {"multica"}
    assert run(project, "check", SPEC)[0] == 0


def test_set_external_needs_an_id_the_first_time(project):
    assert run(project, "set-external", "US-001", "clickup", "--key", "DE-1")[0] == 2


def test_hash_ignores_the_spec_envelope_of_the_root(project):
    run(project, "set-external", "MAP-001", "multica", "--id", "root-uuid", "--hash-current")
    edit(project, "spec.md", "- **SC-001**: Shoppers complete a first purchase in under 3 minutes",
         "- **SC-001**: Shoppers complete a first purchase in under 2 minutes")
    plan = {i["id"]: i for i in run(project, "sync-plan", "multica", SPEC)[1]["items"]}
    assert plan["MAP-001"]["action"] == "unchanged"


def test_sync_plan_only_a_subtree(project):
    result = run(project, "sync-plan", "multica", SPEC, "--only", "EPIC-002")[1]
    assert [i["id"] for i in result["items"]] == ["EPIC-002", "US-002", "SPIKE-001", "US-003"]


def test_external_block_must_follow_the_schema(project):
    edit(project, "backlog/stories/US-001-catalog-list.md", "type: US\n",
         'type: US\nexternal:\n    clickup:\n        id: "86c1x2abc"\n        status: "done"\n')
    assert "schema" in codes(run(project, "check", SPEC)[1])
