"""Contract tests for the deterministic CLI, validation and generated indexes."""
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

import pytest
import yaml


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts/backlog.py"
FIXTURE = REPO / "tests/fixtures/valid"
SPEC = "specs/001-mvp-purchase"
module_spec = importlib.util.spec_from_file_location("backlog_engine", SCRIPT)
engine = importlib.util.module_from_spec(module_spec)
sys.modules[module_spec.name] = engine
module_spec.loader.exec_module(engine)


@pytest.fixture
def project(tmp_path):
    root = tmp_path / "shop"
    shutil.copytree(FIXTURE, root)
    return root


@pytest.fixture
def cli(capsys):
    def run(root, *args, expected=0):
        status = engine.main(["--root", str(root), *args])
        captured = capsys.readouterr()
        assert not captured.err
        result = json.loads(captured.out)
        assert status == expected, result
        return result
    return run


def pbi_path(root, identifier):
    return next((root / "backlog").glob(f"*/{identifier}-*.md"))


def read_pbi(root, identifier):
    text = pbi_path(root, identifier).read_text()
    _, frontmatter, body = text.split("---", 2)
    return yaml.safe_load(frontmatter), body


def write_pbi(root, identifier, data=None, body=None):
    old_data, old_body = read_pbi(root, identifier)
    data = old_data if data is None else data
    body = old_body if body is None else body
    pbi_path(root, identifier).write_text("---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n" + body.lstrip("\n"))


def change_body(root, identifier, before, after):
    data, body = read_pbi(root, identifier)
    assert before in body
    write_pbi(root, identifier, data, body.replace(before, after))


def add_relation(root, source, target, kind="BLOCKED_BY", canonical=True):
    data, body = read_pbi(root, source)
    target_data, _ = read_pbi(root, target)
    data.setdefault("relations", {})[target] = {
        "title": target_data["title"], "type": target_data["type"],
        "relationType": kind, "reason": f"Required by {data['title']}."}
    if canonical:
        data["relations"] = dict(sorted(data["relations"].items(), key=lambda pair: (
            engine.RELATION_ORDER.index(pair[1]["relationType"]),
            engine.PBI_TYPES.index(pair[1]["type"]), engine.numeric_id(pair[0]))))
    write_pbi(root, source, data, body)


def set_scope(root, value):
    path = root / SPEC / "spec.md"
    path.write_text(re.sub(r"^\*\*Scope\*\*:.*$", f"**Scope**: {value}", path.read_text(), flags=re.M))


def codes(result, key="errors"):
    return {entry["code"] for entry in result[key]}


def check_code(cli, root, code):
    result = cli(root, "check", expected=1)
    assert code in codes(result), result
    return result


def flattened(waves):
    return {item["id"]: {**item, "wave": wave["wave"]} for wave in waves for item in wave["items"]}


def refresh(cli, root):
    cli(root, "render-index")
    cli(root, "render-spec", SPEC)
    cli(root, "render-tasks", SPEC)


def test_valid_fixture_checks_without_errors_or_warnings(project, cli):
    result = cli(project, "check")
    assert result["errors"] == result["warnings"] == []
    assert result["checked_specs"] == [SPEC]
    assert result["pbis"] == {"MAP": 1, "EPIC": 2, "FEATURE": 3, "US": 3, "SPIKE": 1, "BUG": 1, "TASK": 10}


@pytest.mark.parametrize("document", ["plan.md", "data-model.md", "research.md", "quickstart.md"])
def test_modular_spec_companion_broken_links_are_checked(project, cli, document):
    path = project / SPEC / document
    path.write_text(path.read_text() + "\n[missing artifact](missing-artifact.md)\n")
    result = check_code(cli, project, "broken-link")
    assert any(entry["file"] == f"{SPEC}/{document}" for entry in result["errors"])


def test_contract_links_in_modular_spec_are_checked(project, cli):
    path = project / SPEC / "plan.md"
    path.write_text(path.read_text().replace("contracts/catalog-api.yaml", "contracts/missing-api.yaml"))
    result = check_code(cli, project, "broken-link")
    assert any(entry["file"] == f"{SPEC}/plan.md" and "missing-api.yaml" in entry["message"]
               for entry in result["errors"])


def test_adr_file_name_validation(project, cli):
    (project / "docs/adr/not-an-adr.md").write_text("# Not an ADR\n")
    check_code(cli, project, "adr-file-name")


def test_adr_duplicate_id_validation(project, cli):
    source = project / "docs/adr/0001-use-stripe-payment-intents.md"
    (source.parent / "0001-another-choice.md").write_text(source.read_text())
    check_code(cli, project, "adr-duplicate-id")


@pytest.mark.parametrize("status", [
    "Approved",
    "Superseded by [ADR-0002: Replace provider](0002-replace-provider.md)",
])
def test_adr_status_validation(project, cli, status):
    path = project / "docs/adr/0001-use-stripe-payment-intents.md"
    path.write_text(re.sub(r"(?m)^\| \*\*Status\*\* \|.*$", f"| **Status** | {status} |", path.read_text()))
    result = check_code(cli, project, "adr-status")
    assert any(entry["file"] == "docs/adr/0001-use-stripe-payment-intents.md"
               for entry in result["errors"])


def test_adr_requires_two_negative_consequences(project, cli):
    path = project / "docs/adr/0001-use-stripe-payment-intents.md"
    path.write_text(path.read_text().replace(
        "- Payment behavior depends on Stripe's API and account availability.\n", ""))
    check_code(cli, project, "adr-consequences")


def test_valid_fixture_scoped_check(project, cli):
    result = cli(project, "check", "--spec", SPEC)
    assert result["errors"] == result["warnings"] == []


@pytest.mark.parametrize("kind,expected", [
    ("MAP", "MAP-002"), ("EPIC", "EPIC-003"), ("FEATURE", "FEATURE-004"),
    ("US", "US-004"), ("SPIKE", "SPIKE-002"), ("BUG", "BUG-002"), ("TASK", "TASK-011")])
def test_next_id_all_seven_types(project, cli, kind, expected):
    result = cli(project, "next-id", kind.lower())
    assert result == {"ok": True, "type": kind, "next": expected, "ids": [expected]}


def test_next_id_count_and_four_digit_rollover(project, cli):
    path = pbi_path(project, "FEATURE-003")
    path.write_text(path.read_text().replace("id: FEATURE-003", "id: FEATURE-999"))
    assert cli(project, "next-id", "FEATURE", "--count", "3")["ids"] == ["FEATURE-1000", "FEATURE-1001", "FEATURE-1002"]


@pytest.mark.parametrize("args", [("next-id", "ALIEN"), ("next-id", "US", "--count", "0"),
                                  ("next-id", "US", "--count", "-1"),
                                  ("next-id", "US", "--count", "not-a-number"), ("not-a-command",)])
def test_json_usage_errors(project, cli, args):
    assert cli(project, *args, expected=2)["ok"] is False


def test_locate_and_spec_backreference(project, cli):
    result = cli(project, "locate", "TASK-002")
    assert result["type"] == "TASK"
    assert result["title"] == "Catalog list acceptance tests"
    assert result["rank"] == 10
    assert result["file"].startswith("backlog/tasks/TASK-002-")
    assert result["referenced_by"] == ["TASK-003"]
    assert result["specs"] == [SPEC]


def test_locate_descendants_breadth_first(project, cli):
    result = cli(project, "locate", "MAP-001", "--descendants")
    ids = result["descendants"]
    assert ids[:2] == ["EPIC-001", "EPIC-002"]
    assert ids.index("FEATURE-001") < ids.index("US-001") < ids.index("TASK-002")
    assert len(ids) == len(set(ids)) == 20


def test_locate_spec_reference_is_not_reverse_ancestor_match(project, cli):
    assert cli(project, "locate", "MAP-001")["specs"] == []
    assert cli(project, "locate", "US-003")["specs"] == []


def test_locate_unknown(project, cli):
    assert not cli(project, "locate", "US-999", expected=1)["ok"]


@pytest.mark.parametrize("mutation,code", [
    ("schema", "schema"), ("placeholder", "placeholder"), ("out-of-scope", "out-of-scope"),
    ("feature-sections", "feature-sections"), ("task-sections", "task-sections"),
    ("ac-id", "ac-id"), ("ac-sequence", "ac-sequence"), ("acceptance-criteria", "acceptance-criteria"),
    ("frontmatter-missing", "frontmatter-missing"), ("frontmatter-invalid", "frontmatter-invalid"),
    ("frontmatter-nonobject", "frontmatter-invalid")])
def test_document_validation_mutations(project, cli, mutation, code):
    if mutation == "schema":
        data, body = read_pbi(project, "FEATURE-001")
        data["invented"] = "forbidden"
        write_pbi(project, "FEATURE-001", data, body)
    elif mutation == "placeholder":
        change_body(project, "FEATURE-001", "Prices use", "{{currency}} prices use")
    elif mutation == "out-of-scope":
        change_body(project, "US-001", "## Out of Scope", "## Deferred")
    elif mutation == "feature-sections":
        change_body(project, "FEATURE-001", "## Constraints", "## Guidance")
    elif mutation == "task-sections":
        change_body(project, "TASK-003", "## Files", "## Paths")
    elif mutation == "ac-id":
        change_body(project, "US-001", "### AC-1:", "### Scenario:")
    elif mutation == "ac-sequence":
        change_body(project, "US-001", "### AC-2:", "### AC-3:")
    elif mutation == "acceptance-criteria":
        change_body(project, "EPIC-001", "## Acceptance Criteria", "## Checks")
    else:
        path = pbi_path(project, "US-001")
        if mutation == "frontmatter-missing":
            path.write_text("No frontmatter\n")
        elif mutation == "frontmatter-invalid":
            path.write_text("---\nid: [broken\n---\n")
        else:
            path.write_text("---\n- not-an-object\n---\n")
    check_code(cli, project, code)


def test_wrong_folder(project, cli):
    path = pbi_path(project, "FEATURE-001")
    path.rename(project / "backlog/stories" / path.name)
    check_code(cli, project, "wrong-folder")


def test_file_name(project, cli):
    pbi_path(project, "FEATURE-001").rename(project / "backlog/features/incorrect.md")
    check_code(cli, project, "file-name")


def test_duplicate_id(project, cli):
    source = pbi_path(project, "FEATURE-001")
    shutil.copyfile(source, source.with_name("FEATURE-001-copy.md"))
    check_code(cli, project, "duplicate-id")


def test_id_prefix_must_match_type(project, cli):
    data, body = read_pbi(project, "FEATURE-001")
    data["type"] = "US"
    write_pbi(project, "FEATURE-001", data, body)
    check_code(cli, project, "schema")


def test_relation_order_includes_feature_type(project, cli):
    add_relation(project, "US-001", "US-002", "RELATED")
    add_relation(project, "US-001", "FEATURE-002", "RELATED", canonical=False)
    check_code(cli, project, "relation-order")


def test_relation_parent_must_come_first(project, cli):
    data, body = read_pbi(project, "US-002")
    data["relations"] = dict(reversed(list(data["relations"].items())))
    write_pbi(project, "US-002", data, body)
    check_code(cli, project, "relation-order")


def test_unknown_relation_id(project, cli):
    data, body = read_pbi(project, "US-001")
    data["relations"]["US-999"] = {"title": "Missing", "type": "US", "relationType": "BLOCKED_BY", "reason": "Missing prerequisite."}
    write_pbi(project, "US-001", data, body)
    check_code(cli, project, "unknown-id")


def test_hierarchy(project, cli):
    data, body = read_pbi(project, "FEATURE-001")
    data.pop("relations")
    write_pbi(project, "FEATURE-001", data, body)
    add_relation(project, "FEATURE-001", "US-001", "PARENT")
    check_code(cli, project, "hierarchy")


def test_multiple_parents(project, cli):
    add_relation(project, "US-001", "FEATURE-002", "PARENT")
    check_code(cli, project, "multiple-parents")


def test_mutual_related_is_inverse_relation(project, cli):
    add_relation(project, "US-001", "US-002", "RELATED")
    add_relation(project, "US-002", "US-001", "RELATED")
    check_code(cli, project, "inverse-relation")


def test_self_reference(project, cli):
    add_relation(project, "US-001", "US-001", "RELATED")
    check_code(cli, project, "self-reference")


def test_relation_type_disagrees_with_target(project, cli):
    data, body = read_pbi(project, "US-001")
    data["relations"]["FEATURE-001"]["type"] = "EPIC"
    write_pbi(project, "US-001", data, body)
    check_code(cli, project, "relation-type")


def test_invalid_relation_enum(project, cli):
    data, body = read_pbi(project, "US-001")
    data["relations"]["FEATURE-001"]["relationType"] = "CHILD"
    write_pbi(project, "US-001", data, body)
    assert {"schema", "relation-type"} <= codes(check_code(cli, project, "schema"))


@pytest.mark.parametrize("warning", ["external-id", "relation-title", "connextra", "redundant-relation"])
def test_nonfatal_warnings(project, cli, warning):
    if warning == "external-id":
        data, body = read_pbi(project, "US-001")
        data["relations"]["JIRA-42"] = {"title": "External record", "type": "US", "relationType": "RELATED", "reason": "Customer context."}
        write_pbi(project, "US-001", data, body)
    elif warning == "relation-title":
        data, body = read_pbi(project, "US-001")
        data["relations"]["FEATURE-001"]["title"] = "Old title"
        write_pbi(project, "US-001", data, body)
    elif warning == "connextra":
        change_body(project, "US-001", "As a shopper,", "A shopper")
    else:
        add_relation(project, "TASK-003", "TASK-008")
        add_relation(project, "TASK-003", "TASK-009")
    refresh(cli, project)
    result = cli(project, "check")
    assert result["errors"] == []
    assert warning in codes(result, "warnings")


def test_blocking_cycle_and_schedule_termination(project, cli):
    add_relation(project, "US-002", "US-003")
    check_code(cli, project, "cycle")
    assert cli(project, "schedule")["ok"]


def test_parent_cycle_and_locate_termination(project, cli):
    add_relation(project, "MAP-001", "EPIC-001", "PARENT")
    check_code(cli, project, "cycle")
    assert len(cli(project, "locate", "MAP-001", "--descendants")["descendants"]) == 20


def test_rank_order_direct_siblings(project, cli):
    add_relation(project, "TASK-002", "TASK-003")
    check_code(cli, project, "rank-order")


def test_rank_order_transitive_siblings(project, cli):
    data, body = read_pbi(project, "TASK-003")
    data["relations"].pop("TASK-002")
    write_pbi(project, "TASK-003", data, body)
    add_relation(project, "TASK-002", "TASK-004")
    add_relation(project, "TASK-004", "TASK-003")
    result = check_code(cli, project, "rank-order")
    assert "cycle" not in codes(result)


def test_rank_order_different_parents_not_an_error(project, cli):
    add_relation(project, "TASK-002", "TASK-005")
    refresh(cli, project)
    result = cli(project, "check")
    assert "rank-order" not in codes(result)


def test_lane_order(project, cli):
    add_relation(project, "US-001", "US-003")
    check_code(cli, project, "lane-order")


def test_lane_missing(project, cli):
    change_body(project, "MAP-001", "  - US [US-001] Catalog list", "  - Catalog list to be assigned")
    check_code(cli, project, "lane-missing")


def test_lane_unknown_id(project, cli):
    change_body(project, "MAP-001", "US [US-001] Catalog list", "US [US-999] Missing catalog list")
    check_code(cli, project, "lane-unknown-id")


@pytest.mark.parametrize("location", ["pbi", "spec", "tasks"])
def test_broken_markdown_links(project, cli, location):
    path = {"pbi": pbi_path(project, "US-001"), "spec": project / SPEC / "spec.md", "tasks": project / SPEC / "tasks.md"}[location]
    with path.open("a") as handle:
        handle.write("\n[Missing design](missing-design.md#contracts)\n")
    check_code(cli, project, "broken-link")


def test_code_comments_and_external_links_are_not_broken(project, cli):
    path = pbi_path(project, "US-001")
    with path.open("a") as handle:
        handle.write("\n```md\n[Example](absent.md)\n```\n~~~md\n[Example](absent.md)\n~~~\n<!-- [Example](absent.md) -->\n[External](https://example.com/absent.md)\n[Anchor](#out-of-scope)\n")
    refresh(cli, project)
    assert cli(project, "check")["errors"] == []


def test_local_link_anchor_and_url_encoding(project, cli):
    path = pbi_path(project, "US-001")
    with path.open("a") as handle:
        handle.write("\n[Catalog acceptance](../tasks/TASK-002-catalog-list-acceptance.md#out-of-scope)\n")
    refresh(cli, project)
    assert cli(project, "check")["ok"]


def test_markdown_links_in_frontmatter_are_validated(project, cli):
    data, body = read_pbi(project, "US-001")
    data["relations"]["FEATURE-001"]["reason"] = "See [the design](missing-design.md)."
    write_pbi(project, "US-001", data, body)
    check_code(cli, project, "broken-link")


@pytest.mark.parametrize("scope", ["TASK-002", "SPIKE-001"])
def test_scope_invalid_type(project, cli, scope):
    set_scope(project, scope)
    check_code(cli, project, "scope-invalid-type")


def test_scope_unknown_id(project, cli):
    set_scope(project, "FEATURE-999")
    check_code(cli, project, "scope-unknown-id")


def test_scope_missing(project, cli):
    path = project / SPEC / "spec.md"
    path.write_text(path.read_text().replace("**Scope**:", "**Coverage**:"))
    check_code(cli, project, "scope-missing")


def test_scope_comment_is_not_scope(project, cli):
    set_scope(project, "`FEATURE-001`, FEATURE-002 *(exclude US-003 and FEATURE-999)*")
    assert cli(project, "schedule", "--spec", SPEC)["scope"] == ["FEATURE-001", "FEATURE-002"]


def test_spec_placeholder(project, cli):
    path = project / SPEC / "spec.md"
    path.write_text(path.read_text() + "\n{{success metric}}\n")
    check_code(cli, project, "placeholder")


def test_spec_missing(project, cli):
    (project / SPEC / "spec.md").unlink()
    result = cli(project, "check", "--spec", SPEC, expected=1)
    assert "spec-missing" in codes(result)


@pytest.mark.parametrize("marker", [engine.BEGIN, engine.END])
def test_spec_markers_required(project, cli, marker):
    path = project / SPEC / "spec.md"
    path.write_text(path.read_text().replace(marker, ""))
    check_code(cli, project, "spec-backlog-markers")
    assert not cli(project, "render-spec", SPEC, expected=2)["ok"]


@pytest.mark.parametrize("command,file,needle,code", [
    ("render-spec", "spec.md", "### Delivery Waves", "spec-backlog-stale"),
    ("render-tasks", "tasks.md", "## Summary", "tasks-index-stale"),
    ("render-index", "backlog/index.md", "## Hierarchy", "index-stale")])
def test_generated_artifacts_detect_staleness_and_repair(project, cli, command, file, needle, code):
    path = project / file if file.startswith("backlog/") else project / SPEC / file
    path.write_text(path.read_text().replace(needle, needle + " manually edited"))
    check_code(cli, project, code)
    cli(project, command, *([] if command == "render-index" else [SPEC]))
    assert cli(project, "check")["errors"] == []


def test_scoped_check_does_not_check_global_index_staleness(project, cli):
    (project / "backlog/index.md").write_text("stale\n")
    assert cli(project, "check", "--spec", SPEC)["ok"]


def test_ac_uncovered(project, cli):
    change_body(project, "TASK-002", ', US-001/AC-2 "Empty catalog"', "")
    refresh(cli, project)
    result = check_code(cli, project, "ac-uncovered")
    assert any("US-001/AC-2" in entry["message"] for entry in result["errors"])


AC1_BLOCK = """```gherkin
@US-001 @AC-1
Scenario: Available products listed
  Given available products
  When I open the catalog
  Then a loading indicator appears
  And the indicator disappears when processing completes
  And I see their names and prices
```"""


def replace_ac1(root, block):
    change_body(root, "US-001", AC1_BLOCK, block)


@pytest.mark.parametrize("block,code", [
    ("Given available products, When I open the catalog, Then I see their names and prices.", "ac-gherkin-missing"),
    ("```text\n" + AC1_BLOCK.split("\n", 1)[1], "ac-gherkin-missing"),
    (AC1_BLOCK + "\n\n" + AC1_BLOCK, "ac-gherkin-scenario"),
    (AC1_BLOCK.replace("  Given available products",
                       "  Given available products\n  When I open the catalog\n  Then I see prices\n\n"
                       "Scenario: Second behaviour\n  Given available products"), "ac-gherkin-scenario"),
    (AC1_BLOCK.replace("@US-001 @AC-1\n", "Feature: Catalog list\n@US-001 @AC-1\n"), "ac-gherkin-scenario"),
    (AC1_BLOCK.replace("Scenario:", "Scenario Outline:"), "ac-gherkin-scenario"),
    (AC1_BLOCK.replace("  When I open the catalog\n", ""), "ac-gherkin-steps"),
    (AC1_BLOCK.replace("@US-001 @AC-1", "@US-001"), "ac-gherkin-tags"),
    (AC1_BLOCK.replace("@US-001 @AC-1", "@US-002 @AC-1"), "ac-gherkin-tags"),
    (AC1_BLOCK.replace("@US-001 @AC-1", "@US-001 @AC-2"), "ac-gherkin-tags"),
    (AC1_BLOCK.replace("@US-001 @AC-1", "@US-001 @AC-1 @AC-2"), "ac-gherkin-tags"),
])
def test_gherkin_acceptance_criteria_validation(project, cli, block, code):
    replace_ac1(project, block)
    result = check_code(cli, project, code)
    assert any(entry["file"].endswith("US-001-catalog-list.md") and "AC-1" in entry["message"]
               for entry in result["errors"] if entry["code"] == code)


def test_gherkin_examples_without_outline_is_rejected(project, cli):
    replace_ac1(project, AC1_BLOCK.replace("  And I see their names and prices\n",
                                           "  And I see their names and prices\n\n  Examples:\n    | n |\n    | 1 |\n"))
    check_code(cli, project, "ac-gherkin-scenario")


def test_gherkin_scenario_outline_extra_tags_and_comments_are_valid(project, cli):
    replace_ac1(project, """```gherkin
# Prices follow the catalog currency
@US-001 @AC-1 @smoke
Scenario Outline: Available products listed
  Given <count> available products
  When I open the catalog
  Then a loading indicator appears
  And the indicator disappears when processing completes
  But I see <count> names and prices

  Examples:
    | count |
    | 1     |
    | 20    |
```""")
    result = cli(project, "check")
    assert result["errors"] == result["warnings"] == []


def test_gherkin_scenario_title_mismatch_is_a_warning(project, cli):
    replace_ac1(project, AC1_BLOCK.replace("Scenario: Available products listed", "Scenario: Products shown"))
    result = cli(project, "check")
    assert result["errors"] == []
    assert codes(result, "warnings") == {"ac-gherkin-title"}


def test_gherkin_headings_inside_blocks_keep_ac_ids_and_coverage(project, cli):
    replace_ac1(project, AC1_BLOCK.replace("  Given available products",
                                           "  Given available products\n  \"\"\"\n  ### AC-9: not a heading\n  \"\"\""))
    result = cli(project, "check")
    assert result["errors"] == result["warnings"] == []
    assert [c["number"] for c in engine.acceptance_blocks(read_pbi(project, "US-001")[1])] == [1, 2]


def test_export_features_writes_one_feature_per_story(project, cli, tmp_path):
    result = cli(project, "export-features", SPEC, "features")
    assert result["stories"] == 2
    assert result["files"] == ["features/US-001-catalog-list.feature", "features/US-002-card-payment.feature"]
    assert (project / "features/US-001-catalog-list.feature").read_text() == """Feature: Catalog list

  @US-001 @AC-1
  Scenario: Available products listed
    Given available products
    When I open the catalog
    Then a loading indicator appears
    And the indicator disappears when processing completes
    And I see their names and prices

  @US-001 @AC-2
  Scenario: Empty catalog
    Given no available products
    When I open the catalog
    Then a loading indicator appears
    And the indicator disappears when processing completes
    And I see that no products are available
"""


def test_export_features_refuses_invalid_scenarios(project, cli):
    replace_ac1(project, AC1_BLOCK.replace("@US-001 @AC-1", "@US-001"))
    result = cli(project, "export-features", SPEC, "features", expected=1)
    assert codes(result) == {"ac-gherkin-tags"}
    assert not (project / "features").exists()


def test_acceptance_tests_can_be_disabled_in_constitution(project, cli):
    constitution = project / ".specify/memory/constitution.md"
    constitution.parent.mkdir()
    constitution.write_text("# Constitution\n\n## Delivery Conventions\n\n- **Acceptance tests from Gherkin**: `off`\n")
    change_body(project, "TASK-002", "**Covers:**", "**Documents:**")
    refresh(cli, project)
    assert cli(project, "check")["errors"] == []
    assert "Acceptance tests from Gherkin: off" in (project / SPEC / "tasks.md").read_text()


def test_check_never_rewrites_files(project, cli):
    before = {p.relative_to(project): p.read_bytes() for p in project.rglob("*") if p.is_file()}
    cli(project, "check")
    after = {p.relative_to(project): p.read_bytes() for p in project.rglob("*") if p.is_file()}
    assert after == before


def test_schedule_packs_disjoint_stories_in_parallel(project, cli):
    result = cli(project, "schedule")
    stories = flattened(result["story_waves"])
    assert result["scope"] is None
    assert stories["US-001"]["wave"] == stories["US-002"]["wave"] == 1
    assert stories["US-001"]["parallel"] is stories["US-002"]["parallel"] is True
    assert stories["US-003"]["wave"] == 2
    assert stories["US-003"]["parallel"] is False
    assert "app/catalog.py" in stories["US-001"]["files"]


def test_schedule_scoped_descendants_and_blocking_spike(project, cli):
    result = cli(project, "schedule", "--spec", SPEC)
    assert set(flattened(result["story_waves"])) == {"US-001", "US-002"}
    assert "TASK-001" not in flattened(result["task_waves"])
    project_model = engine.Project(project)
    assert "SPIKE-001" in project_model.scoped_ids(["FEATURE-002"])


def test_parallel_tasks_with_disjoint_files(project, cli):
    tasks = flattened(cli(project, "schedule")["task_waves"])
    assert tasks["TASK-002"]["wave"] == tasks["TASK-004"]["wave"] == 1
    assert tasks["TASK-002"]["parallel"] and tasks["TASK-004"]["parallel"]
    assert tasks["TASK-002"]["done"] is True
    assert tasks["TASK-003"]["done"] is False


def test_independent_tasks_sharing_normalized_path_serialize(project, cli):
    change_body(project, "TASK-004", "`tests/acceptance/payment.feature`", "`./tests/acceptance/../acceptance/catalog.feature`")
    tasks = flattened(cli(project, "schedule")["task_waves"])
    assert tasks["TASK-002"]["wave"] < tasks["TASK-004"]["wave"]


def test_two_item_shared_file_wave_has_no_parallel_marker(project):
    model = engine.Project(project)
    a, b = model.pbis["TASK-002"], model.pbis["TASK-004"]
    waves = engine.pack_waves([a, b], {a.id: set(), b.id: set()}, {a.id: {"same.py"}, b.id: {"same.py"}})
    assert [wave["wave"] for wave in waves] == [1, 2]
    assert not any(wave["parallel"] or wave["items"][0]["parallel"] for wave in waves)


def test_story_file_conflicts_aggregate_child_task_files(project, cli):
    change_body(project, "TASK-004", "`tests/acceptance/payment.feature`", "`app/catalog.py`")
    stories = flattened(cli(project, "schedule")["story_waves"])
    assert stories["US-002"]["wave"] > stories["US-001"]["wave"]


def test_container_blockers_propagate_to_stories_and_tasks(project, cli):
    add_relation(project, "FEATURE-002", "FEATURE-001")
    result = cli(project, "schedule")
    stories, tasks = flattened(result["story_waves"]), flattened(result["task_waves"])
    assert stories["US-002"]["blockers"] == ["US-001"]
    assert stories["US-002"]["wave"] > stories["US-001"]["wave"]
    assert {"TASK-002", "TASK-003", "TASK-008", "TASK-009", "TASK-010"} <= set(tasks["TASK-004"]["blockers"])
    assert tasks["TASK-004"]["wave"] > tasks["TASK-010"]["wave"]


def test_story_dependency_maps_to_all_story_tasks(project, cli):
    tasks = flattened(cli(project, "schedule")["task_waves"])
    assert {"TASK-004", "TASK-005"} <= set(tasks["TASK-006"]["blockers"])
    assert tasks["TASK-006"]["wave"] > tasks["TASK-005"]["wave"]
    assert {"TASK-002", "TASK-003"} <= set(tasks["TASK-010"]["blockers"])


def test_child_spike_blocking_parent_does_not_self_inherit(project, cli):
    model = engine.Project(project)
    assert "SPIKE-001" not in model.raw_blockers(model.pbis["SPIKE-001"])
    assert "cycle" not in codes(cli(project, "check"))


def test_critical_path_includes_dependencies_and_file_serialization(project, cli):
    tasks = flattened(cli(project, "schedule")["task_waves"])
    result = cli(project, "schedule")
    path = result["critical_path"]
    assert len(path) >= 4
    assert all(tasks[a]["wave"] < tasks[b]["wave"] for a, b in zip(path, path[1:]))
    model = engine.Project(project)
    a, b = model.pbis["TASK-002"], model.pbis["TASK-004"]
    blockers, files = {a.id: set(), b.id: set()}, {a.id: {"shared.py"}, b.id: {"shared.py"}}
    waves = engine.pack_waves([a, b], blockers, files)
    assert engine.critical_path(waves, blockers, files) == [a.id, b.id]


def test_schedule_deterministic_and_rank_breaks_ties(project, cli):
    first = cli(project, "schedule")
    assert first == cli(project, "schedule")
    model = engine.Project(project)
    a, b = model.pbis["TASK-002"], model.pbis["TASK-004"]
    a.rank, b.rank = 20, 10
    waves = engine.pack_waves([a, b], {a.id: set(), b.id: set()}, {a.id: {"same"}, b.id: {"same"}})
    assert waves[0]["items"][0]["id"] == b.id


def test_render_index_functional_tree_task_counter_no_exploded_tasks(project, cli):
    result = cli(project, "render-index")
    text = (project / "backlog/index.md").read_text()
    assert result["story_waves"] == 2
    assert "- MAP [MAP-001](maps/" in text
    assert "  - EPIC [EPIC-001](epics/" in text
    assert "    - FEATURE [FEATURE-001](features/" in text
    assert "      - US [US-001](stories/" in text
    assert "tasks: 1/2" in text
    assert "TASK-001" in text
    for number in range(2, 11):
        assert f"TASK-{number:03d}" not in text
    assert "SPIKE [SPIKE-001]" in text
    assert "**Wave 1 [P]**" in text


def test_backbone_order_overrides_epic_rank(project, cli):
    data, body = read_pbi(project, "EPIC-002")
    data["rank"] = 1
    write_pbi(project, "EPIC-002", data, body)
    cli(project, "render-index")
    text = (project / "backlog/index.md").read_text()
    assert text.index("EPIC [EPIC-001]") < text.index("EPIC [EPIC-002]")


def test_render_spec_minimal_tree_links_waves_and_open_spikes(project, cli):
    result = cli(project, "render-spec", SPEC)
    text = (project / SPEC / "spec.md").read_text()
    assert result["stories"] == 2 and result["waves"] == 1
    assert "MAP [MAP-001]" in text and "EPIC [EPIC-002]" in text
    assert "FEATURE-003" not in text and "US-003" not in text
    assert "../../backlog/stories/US-001-catalog-list.md" in text
    assert "— Wave 1 [P]" in text
    assert "### Open Spikes" in text and "SPIKE [SPIKE-001]" in text
    assert "TASK-" not in text
    assert "BUG-" not in text
    assert "SC-001 — First purchase" in text


def test_closed_spikes_are_not_listed_as_open(project, cli):
    change_body(project, "SPIKE-001", "- [ ] Record sandbox", "- [x] Record sandbox")
    cli(project, "render-spec", SPEC)
    assert "### Open Spikes" not in (project / SPEC / "spec.md").read_text()


def test_render_tasks_phases_strict_lines_traceability_and_graph(project, cli):
    result = cli(project, "render-tasks", SPEC)
    text = (project / SPEC / "tasks.md").read_text()
    assert result == {"ok": True, "file": f"{SPEC}/tasks.md", "tasks": 8, "done": 1, "waves": 3}
    assert text.startswith("# Tasks: First online purchase\n")
    assert "specification](spec.md)" in text and "plan](plan.md)" in text
    for heading in ("Setup", "Walking Skeleton", "Foundational", "Story Wave 1 🎯 MVP", "Polish"):
        assert re.search(r"## Phase \d+: " + re.escape(heading), text)
    assert "### US [US-001] [P] Catalog list" in text
    assert "## Wave Schedule & Dependency Graph" in text
    assert "**Critical path:**" in text and "Implement catalog list" in text
    assert '| US [US-001]' in text and 'US-001/AC-2 "Empty catalog"' in text
    lines = re.findall(r"^- \[[ X]\] TASK-.*$", text, re.M)
    assert len(lines) == result["tasks"]
    pattern = r"^- \[[ X]\] TASK-\d{3,}(?: \[P\])?(?: \[US-\d{3,}\])? .+ → \[\.\./\.\./backlog/tasks/[^\]]+\]\(\.\./\.\./backlog/tasks/[^)]+\)$"
    assert all(re.fullmatch(pattern, line) for line in lines)
    assert any(line.startswith("- [X] TASK-002") for line in lines)
    assert all("[US-" not in line for line in lines if "TASK-001 " in line)


def test_release_lane_phases_when_multiple_lanes_populated(project, cli):
    set_scope(project, "MAP-001")
    result = cli(project, "render-tasks", SPEC)
    text = (project / SPEC / "tasks.md").read_text()
    assert result["tasks"] == 10
    assert "Release 1: First purchase by card 🎯 MVP" in text
    assert "Release 2: Returning shoppers purchase faster" in text
    assert "## Phase 4: Story Wave" not in text
    assert text.index("### US [US-002]") < text.index("### US [US-003]")


def test_release_lane_parser_keeps_heading_and_body_separate(project):
    model = engine.Project(project)
    lanes = model.lanes(model.pbis["MAP-001"])
    assert lanes == [
        ("Release 1: First purchase by card", ["EPIC-001", "FEATURE-001", "US-001", "EPIC-002", "FEATURE-002", "US-002"]),
        ("Release 2: Returning shoppers purchase faster", ["EPIC-002", "FEATURE-003", "US-003"])]


def test_container_task_blocked_by_walking_skeleton_is_foundational(project, cli):
    add_relation(project, "TASK-008", "TASK-001")
    cli(project, "render-tasks", SPEC)
    text = (project / SPEC / "tasks.md").read_text()
    assert "## Phase 1: Walking Skeleton" in text
    foundational = text.split("## Phase 2: Foundational", 1)[1].split("## Phase 3:", 1)[0]
    assert "TASK-008" in foundational and "TASK-009" in foundational


@pytest.mark.parametrize("section", ["Actions to complete", "Definition of Done"])
def test_rendered_done_state_uses_every_required_checkbox(project, cli, section):
    data, body = read_pbi(project, "TASK-002")
    if section == "Actions to complete":
        body = body.replace("- [x] Write", "- [ ] Write")
    else:
        body = body.replace("- [x] Both", "- [ ] Both")
    write_pbi(project, "TASK-002", data, body)
    result = cli(project, "render-tasks", SPEC)
    assert result["done"] == 0
    assert "- [ ] TASK-002" in (project / SPEC / "tasks.md").read_text()


def test_task_done_requires_dod_checkbox_not_just_actions(project):
    model = engine.Project(project)
    task = model.pbis["TASK-002"]
    task.body = "## Actions to complete\n- [x] Finished\n## Definition of Done\nNo checklist yet.\n"
    assert not engine.is_task_done(task)
    task.body += "- [X] Reviewed\n"
    assert engine.is_task_done(task)


def test_fenced_commented_checkboxes_and_files_ignored(project):
    model = engine.Project(project)
    task = model.pbis["TASK-002"]
    task.body += "\n<!-- - [ ] Ignored -->\n```md\n- [ ] Ignored\n```\n"
    assert engine.is_task_done(task)
    task.body = "## Files\n- `./app/../app/catalog.py`\n- `{{path}}`\n<!-- `hidden.py` -->\n```\n`example.py`\n```\n## Actions to complete\n- [ ] Work\n"
    assert engine.task_files(task) == {"app/catalog.py"}
    assert engine.task_files(model.pbis["SPIKE-001"]) == set()


def test_done_counts_refresh_from_task_sources(project, cli):
    data, body = read_pbi(project, "TASK-003")
    write_pbi(project, "TASK-003", data, body.replace("- [ ]", "- [x]"))
    refresh(cli, project)
    assert "tasks: 2/2" in (project / "backlog/index.md").read_text()
    assert "- [X] TASK-003" in (project / SPEC / "tasks.md").read_text()
    assert cli(project, "check")["errors"] == []


def test_all_renderers_idempotent(project, cli):
    paths = [project / "backlog/index.md", project / SPEC / "spec.md", project / SPEC / "tasks.md"]
    before = [path.read_bytes() for path in paths]
    refresh(cli, project)
    assert [path.read_bytes() for path in paths] == before
    refresh(cli, project)
    assert [path.read_bytes() for path in paths] == before


def test_no_pbis_and_missing_backlog_render_index(project, cli):
    shutil.rmtree(project / "backlog")
    assert cli(project, "render-index")["story_waves"] == 0
    assert cli(project, "next-id", "FEATURE")["next"] == "FEATURE-001"
    assert cli(project, "schedule")["critical_path"] == []


@pytest.mark.parametrize("args", [("render-spec", "specs/missing"), ("render-tasks", "specs/missing"),
                                  ("schedule", "--spec", "specs/missing"), ("check", "--spec", "specs/missing")])
def test_missing_spec_directory_is_json_usage_error(project, cli, args):
    assert not cli(project, *args, expected=2)["ok"]


def test_missing_root_is_json_usage_error(tmp_path, cli):
    assert not cli(tmp_path / "missing", "schedule", expected=2)["ok"]


def test_default_root_nearest_ancestor_and_real_executable(project):
    result = subprocess.run([sys.executable, str(SCRIPT), "locate", "US-001"], cwd=project / SPEC,
                            text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["specs"] == [SPEC]
    assert SCRIPT.stat().st_mode & 0o111


def test_default_root_without_markers_is_json_error(tmp_path):
    result = subprocess.run([sys.executable, str(SCRIPT), "schedule"], cwd=tmp_path,
                            text=True, capture_output=True, check=False)
    assert result.returncode == 2
    assert not json.loads(result.stdout)["ok"]


def test_missing_dependency_returns_json_exit_two(project):
    result = subprocess.run([sys.executable, "-S", str(SCRIPT), "--root", str(project), "schedule"],
                            text=True, capture_output=True, check=False)
    assert result.returncode == 2
    assert "Missing dependency" in json.loads(result.stdout)["error"]


def test_cli_help_is_also_json(project):
    result = subprocess.run([sys.executable, str(SCRIPT), "schedule", "--help"], cwd=project,
                            text=True, capture_output=True, check=False)
    assert result.returncode == 0
    assert "--spec" in json.loads(result.stdout)["help"]


def test_unicode_titles_emitted_as_unicode(project, cli, capsys):
    data, body = read_pbi(project, "US-001")
    data["title"] = "Catalogo — caffè ☕"
    write_pbi(project, "US-001", data, body)
    engine.main(["--root", str(project), "locate", "US-001"])
    raw = capsys.readouterr().out
    assert "caffè ☕" in raw
    assert json.loads(raw)["title"] == data["title"]
