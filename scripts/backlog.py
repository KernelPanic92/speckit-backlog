#!/usr/bin/env python3
"""Deterministic, project-local backlog validation and delivery indexes.

Only YAML frontmatter, PARENT/BLOCKED_BY edges and declared task files are
inputs. Renderers are pure functions; check compares their output without
writing anything. Invalid documents are retained as diagnostics, not crashes.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import posixpath
import re
import sys
import textwrap
from urllib.parse import unquote, urlsplit

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError as exc:
    print(json.dumps({"ok": False, "error": f"Missing dependency: {exc.name}"}))
    raise SystemExit(2)


PBI_TYPES = ("MAP", "EPIC", "FEATURE", "US", "SPIKE", "BUG", "TASK")
RELATION_ORDER = ("PARENT", "BLOCKED_BY", "RELATED")
BACKLOG_DIRS = {"maps": "MAP", "epics": "EPIC", "features": "FEATURE",
                "stories": "US", "spikes": "SPIKE", "tasks": "TASK", "bugs": "BUG"}
ALLOWED_PARENTS = {"MAP": ("EPIC",), "EPIC": ("MAP",), "FEATURE": ("EPIC",),
                   "US": ("FEATURE", "EPIC"), "BUG": ("FEATURE", "EPIC"),
                   "TASK": ("US", "FEATURE", "EPIC"),
                   "SPIKE": ("US", "FEATURE", "EPIC")}
ID_PATTERN = r"(?:MAP|EPIC|FEATURE|US|SPIKE|BUG|TASK)-\d{3,}"
ID_RE = re.compile(rf"\b{ID_PATTERN}\b")
BEGIN, END = "<!-- BEGIN BACKLOG -->", "<!-- END BACKLOG -->"
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas/pbi-frontmatter.schema.json"


def numeric_id(value):
    match = re.search(r"-(\d+)$", value)
    return int(match[1]) if match else 0


def clean_markdown(text):
    """Remove comments and fenced blocks while preserving line boundaries."""
    text = re.sub(r"<!--.*?(?:-->|\Z)", "", text, flags=re.S)
    lines, fence = [], None
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence) and not match[2].strip():
                fence = None
            lines.append("")
        elif match:
            fence = match[1]
            lines.append("")
        else:
            lines.append(line)
    return "\n".join(lines)


def sections(body):
    result, current = {}, None
    for line in clean_markdown(body).splitlines():
        match = re.match(r"^##\s+(.+?)\s*#*\s*$", line)
        if match:
            current = match[1]
            result.setdefault(current, [])
        elif current is not None:
            result[current].append(line)
    return {key: "\n".join(value) for key, value in result.items()}


def checkboxes(text):
    return re.findall(r"^\s*-\s*\[([ xX])\]", clean_markdown(text), re.M)


FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})(.*)$")
SCENARIO_RE = re.compile(r"^(Scenario Outline|Scenario Template|Scenario|Example)\s*:\s*(.*)$")
STEP_RE = re.compile(r"^(Given|When|Then|And|But|\*)(?:\s|$)")


def acceptance_blocks(body):
    """Return each `### AC-n: Title` of ## Acceptance Criteria with its fenced blocks."""
    text = re.sub(r"<!--.*?(?:-->|\Z)", "", body, flags=re.S)
    result, in_section, current, fence, info, lines = [], False, None, None, "", []
    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence) and not match[2].strip():
                if current is not None:
                    current["blocks"].append((info, "\n".join(lines)))
                fence = None
            else:
                lines.append(line)
        elif match:
            fence, info, lines = match[1], (match[2].split() or [""])[0].lower(), []
        elif heading := re.match(r"^(#{2,3})\s+(.+?)\s*#*\s*$", line):
            if heading[1] == "##":
                in_section, current = heading[2] == "Acceptance Criteria", None
            elif in_section:
                criterion = re.match(r"AC-(\d+):\s*(.+)$", heading[2])
                current = {"number": int(criterion[1]), "title": criterion[2].strip(),
                           "blocks": []} if criterion else None
                if current:
                    result.append(current)
    return result


def gherkin_issues(story_id, criterion):
    """Validate the single fenced gherkin block of one acceptance criterion."""
    label = f"AC-{criterion['number']}"
    blocks = [content for info, content in criterion["blocks"] if info == "gherkin"]
    if not blocks:
        return [("ac-gherkin-missing", f"{label} needs one fenced ```gherkin block", False)]
    if len(blocks) > 1:
        return [("ac-gherkin-scenario", f"{label} must hold exactly one ```gherkin block", False)]
    tags, headers, containers, steps, examples, docstring = [], [], [], set(), 0, None
    for line in (raw.strip() for raw in blocks[0].splitlines()):
        if docstring:
            docstring = None if line.startswith(docstring) else docstring
            continue
        if line.startswith(('"""', "```")):
            docstring = line[:3]
        elif line.startswith("@"):
            if not headers:
                tags.extend(token for token in line.split() if token.startswith("@"))
        elif scenario := SCENARIO_RE.match(line):
            headers.append(scenario)
        elif re.match(r"^(Feature|Rule|Background)\s*:", line):
            containers.append(line.split(":")[0])
        elif re.match(r"^(Examples|Scenarios)\s*:", line):
            examples += 1
        elif step := STEP_RE.match(line):
            steps.add(step[1])
    issues = []
    if len(headers) != 1 or containers:
        found = ", ".join([h[1] for h in headers] + containers) or "none"
        issues.append(("ac-gherkin-scenario", f"{label} must hold exactly one Scenario or Scenario Outline (found: {found})", False))
    elif headers[0][1] in ("Scenario Outline", "Scenario Template") and not examples:
        issues.append(("ac-gherkin-scenario", f"{label} Scenario Outline needs Examples", False))
    elif headers[0][1] not in ("Scenario Outline", "Scenario Template") and examples:
        issues.append(("ac-gherkin-scenario", f"{label} Examples require a Scenario Outline", False))
    if not {"When", "Then"} <= steps:
        issues.append(("ac-gherkin-steps", f"{label} needs at least a When and a Then step", False))
    expected = {f"@{story_id}", f"@{label}"}
    trace = {tag for tag in tags if re.fullmatch(rf"@(?:{ID_PATTERN}|AC-\d+)", tag)}
    if trace != expected:
        issues.append(("ac-gherkin-tags", f"{label} scenario tags must be @{story_id} @{label} (found: {' '.join(sorted(trace)) or 'none'})", False))
    if len(headers) == 1 and headers[0][2].strip() != criterion["title"]:
        issues.append(("ac-gherkin-title", f"{label} scenario title differs from its heading: {criterion['title']}", True))
    return issues


def feature_text(pbi):
    """Render a story's acceptance scenarios as one Gherkin .feature document."""
    scenarios = []
    for criterion in acceptance_blocks(pbi.body):
        content = next(content for info, content in criterion["blocks"] if info == "gherkin")
        scenarios.append(textwrap.indent(textwrap.dedent(content).strip("\n"), "  "))
    return f"Feature: {pbi.title}\n\n" + "\n\n".join(scenarios) + "\n"


@dataclass
class Pbi:
    path: Path
    text: str
    body: str
    data: dict
    id: str
    type: str
    title: str
    rank: int | None = None
    relations: dict = field(default_factory=dict)

    @property
    def parent(self):
        return next((key for key, rel in self.relations.items()
                     if rel.get("relationType") == "PARENT"), None)

    @property
    def blockers(self):
        return {key for key, rel in self.relations.items()
                if rel.get("relationType") == "BLOCKED_BY"}


def is_task_done(pbi):
    sec = sections(pbi.body)
    dod = [value for name, value in sec.items() if name.startswith("Definition of Done")]
    required = [box for value in dod for box in checkboxes(value)]
    all_boxes = required + checkboxes(sec.get("Actions to complete", ""))
    return bool(required) and all(box.lower() == "x" for box in all_boxes)


def task_files(pbi, pbis=None):
    if pbi.type == "US":
        return set().union(*(task_files(task) for task in (pbis or {}).values()
                             if task.type == "TASK" and task.parent == pbi.id))
    if pbi.type != "TASK":
        return set()
    return {posixpath.normpath(path.strip().replace("\\", "/"))
            for path in re.findall(r"`([^`\n]+)`", sections(pbi.body).get("Files", ""))
            if path.strip() and "{{" not in path}


def sort_key(pbi):
    return (pbi.rank if pbi.rank is not None else 999999,
            PBI_TYPES.index(pbi.type) if pbi.type in PBI_TYPES else 999,
            numeric_id(pbi.id), pbi.id)


@dataclass
class Report:
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

    def add(self, code, file, message, warning=False):
        (self.warnings if warning else self.errors).append(
            {"code": code, "file": str(file), "message": message})


class UsageError(Exception):
    pass


class Project:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.pbis = {}
        self.documents = []
        self.report = Report()
        self.validator = Draft202012Validator(json.loads(SCHEMA_PATH.read_text()))
        for directory in BACKLOG_DIRS:
            for path in sorted((self.root / "backlog" / directory).glob("*.md")):
                self.load(path, BACKLOG_DIRS[directory])

    def rel(self, path):
        return Path(os.path.relpath(path, self.root)).as_posix()

    def load(self, path, expected_type):
        text = path.read_text(encoding="utf-8")
        name = self.rel(path)
        if "{{" in text:
            self.report.add("placeholder", name, "Unresolved template placeholder")
        match = re.match(r"\A---[ \t]*\r?\n(.*?)^---[ \t]*\r?$(?:\n|\Z)", text, re.S | re.M)
        if not match:
            self.report.add("frontmatter-missing", name, "Expected YAML frontmatter delimiters")
            self.documents.append((path, text))
            return
        body = text[match.end():].lstrip("\n")
        self.documents.append((path, text))
        try:
            data = yaml.safe_load(match[1])
        except yaml.YAMLError as exc:
            self.report.add("frontmatter-invalid", name, str(exc))
            return
        if not isinstance(data, dict):
            self.report.add("frontmatter-invalid", name, "Frontmatter must be an object")
            return
        errors = sorted(self.validator.iter_errors(data), key=lambda error: str(error.path))
        if errors:
            self.report.add("schema", name, "; ".join(error.message for error in errors))
        identifier, kind = data.get("id"), data.get("type")
        if not isinstance(identifier, str) or not isinstance(kind, str):
            return
        if not identifier.startswith(kind + "-"):
            self.report.add("schema", name, "id prefix must match type")
        if kind != expected_type:
            self.report.add("wrong-folder", name, f"Expected {expected_type}, found {kind}")
        if not re.fullmatch(re.escape(identifier) + r"-[a-z0-9]+(?:-[a-z0-9]+)*\.md", path.name):
            self.report.add("file-name", name, "Expected ID-lowercase-slug.md")
        relations = data.get("relations", {})
        relations = {key: value for key, value in relations.items()
                     if isinstance(key, str) and isinstance(value, dict)} if isinstance(relations, dict) else {}
        pbi = Pbi(path, text, body, data, identifier, kind,
                  str(data.get("title", identifier)),
                  data.get("rank") if type(data.get("rank")) is int else None, relations)
        if identifier in self.pbis:
            self.report.add("duplicate-id", name, f"Duplicate {identifier}")
        else:
            self.pbis[identifier] = pbi

    def counts(self):
        counts = Counter(pbi.type for pbi in self.pbis.values())
        return {kind: counts[kind] for kind in PBI_TYPES}

    def children(self, identifier):
        return sorted((pbi for pbi in self.pbis.values() if pbi.parent == identifier), key=sort_key)

    def descendants(self, identifier):
        seen, result, queue = {identifier}, [], deque([identifier])
        while queue:
            for child in self.children(queue.popleft()):
                if child.id not in seen:
                    seen.add(child.id)
                    result.append(child.id)
                    queue.append(child.id)
        return result

    def ancestors(self, identifier):
        seen, result = {identifier}, []
        while identifier in self.pbis:
            identifier = self.pbis[identifier].parent
            if identifier is None or identifier in seen or identifier not in self.pbis:
                break
            seen.add(identifier)
            result.append(identifier)
        return result

    def raw_blockers(self, pbi):
        result = set(pbi.blockers)
        for ancestor in self.ancestors(pbi.id):
            descendants = set(self.descendants(ancestor))
            result.update(target for target in self.pbis[ancestor].blockers
                          if target != pbi.id and target not in descendants)
        return result

    def effective_blockers(self, items):
        ids = {pbi.id for pbi in items}
        result = {}
        for pbi in items:
            mapped = set()
            for target in self.raw_blockers(pbi):
                if target in ids:
                    mapped.add(target)
                else:
                    mapped.update(ids.intersection(self.descendants(target)))
            result[pbi.id] = mapped
        return result

    def spec_path(self, directory):
        path = Path(directory)
        path = path if path.is_absolute() else self.root / path
        path = path.resolve()
        if not path.is_dir():
            raise UsageError(f"Missing spec directory: {path}")
        return path

    def read_spec(self, directory):
        directory = self.spec_path(directory)
        path = directory / "spec.md"
        if not path.is_file():
            raise UsageError(f"Missing specification: {self.rel(path)}")
        text = path.read_text(encoding="utf-8")
        scope_line = re.search(r"^\*\*Scope\*\*\s*:\s*(.*)$", clean_markdown(text), re.M)
        scope = list(dict.fromkeys(ID_RE.findall(re.split(r"\*\(", scope_line[1])[0]))) if scope_line else None
        title = re.search(r"^# Feature Specification:\s*(.+)$", text, re.M)
        return directory, text, scope, title[1].strip() if title else directory.name

    def scoped_ids(self, scope):
        if scope is None:
            return set(self.pbis)
        ids = {identifier for identifier in scope if identifier in self.pbis}
        for identifier in list(ids):
            ids.update(self.descendants(identifier))
        while True:
            spikes = {target for identifier in ids for target in self.raw_blockers(self.pbis[identifier])
                      if target in self.pbis and self.pbis[target].type == "SPIKE"}
            if spikes <= ids:
                return ids
            ids.update(spikes)

    def schedule_items(self, items):
        blockers = self.effective_blockers(items)
        files = {pbi.id: task_files(pbi, self.pbis) for pbi in items}
        waves = pack_waves(items, blockers, files)
        return waves, critical_path(waves, blockers, files)

    def schedule(self, scope=None):
        ids = self.scoped_ids(scope)
        stories, story_path = self.schedule_items([p for p in self.pbis.values() if p.id in ids and p.type == "US"])
        tasks, task_path = self.schedule_items([p for p in self.pbis.values() if p.id in ids and p.type == "TASK"])
        return {"ok": True, "scope": scope, "story_waves": stories, "task_waves": tasks,
                "critical_path": task_path or story_path}

    def lanes(self, pbi):
        content = sections(pbi.body).get("Release Lanes", "")
        result = []
        for match in re.finditer(r"^###[ \t]+([^\n]+)\n(.*?)(?=^###[ \t]|\Z)", content + "\n", re.M | re.S):
            ids = re.findall(r"\b(?:EPIC|FEATURE|US)\s+\[(" + ID_PATTERN + r")\]", match[2])
            result.append((match[1].strip(), list(dict.fromkeys(ids))))
        return result

    def skeleton_ids(self, map_pbi):
        return ID_RE.findall(sections(map_pbi.body).get("Walking Skeleton", ""))

    def link(self, pbi, directory):
        path = Path(os.path.relpath(pbi.path, directory)).as_posix()
        return f"{pbi.type} [{pbi.id}]({path}) {pbi.title}"

    def tree(self, ids, directory, waves, task_counts=False):
        chosen = {identifier for identifier in ids if identifier in self.pbis}
        wave_lookup = {item["id"]: (wave["wave"], wave["parallel"]) for wave in waves for item in wave["items"]}
        lines, visited = [], set()

        def visit(pbi, depth):
            if pbi.id in visited:
                return
            visited.add(pbi.id)
            label = self.link(pbi, directory)
            if pbi.id in wave_lookup:
                number, parallel = wave_lookup[pbi.id]
                label += f" — Wave {number}" + (" [P]" if parallel else "")
            tasks = [p for p in self.children(pbi.id) if p.type == "TASK"]
            if task_counts and pbi.type == "US" and tasks:
                label += f" · tasks: {sum(is_task_done(p) for p in tasks)}/{len(tasks)}"
            lines.append("  " * depth + "- " + label)
            children = [p for p in self.children(pbi.id) if p.id in chosen]
            if pbi.type == "MAP":
                backbone = ID_RE.findall(sections(pbi.body).get("Backbone", ""))
                children.sort(key=lambda p: (backbone.index(p.id) if p.id in backbone else 999999, sort_key(p)))
            else:
                children.sort(key=lambda p: (0 if p.type in ("TASK", "SPIKE") else 1,
                                              wave_lookup.get(p.id, (0, False))[0], sort_key(p)))
            for child in children:
                visit(child, depth + 1)

        roots = sorted((self.pbis[i] for i in chosen if self.pbis[i].parent not in chosen), key=sort_key)
        for pbi in roots:
            visit(pbi, 0)
        # Still render useful output for cyclic input; check reports the cycle.
        for pbi in sorted((self.pbis[i] for i in chosen - visited), key=sort_key):
            visit(pbi, 0)
        return lines

    def wave_lines(self, waves, directory):
        return [f"- **Wave {wave['wave']}{' [P]' if wave['parallel'] else ''}**: " +
                ", ".join(self.link(self.pbis[item["id"]], directory) for item in wave["items"])
                for wave in waves]

    def index_text(self):
        waves = self.schedule()["story_waves"]
        ids = {p.id for p in self.pbis.values() if p.type != "TASK"}
        ids.update(target for p in self.pbis.values() if p.type == "MAP" for target in self.skeleton_ids(p)
                   if target in self.pbis)
        return "\n".join(["# Product Backlog", "",
                          "Generated by `scripts/backlog.py render-index`; do not edit by hand.", "",
                          "## Hierarchy", "", *self.tree(ids, self.root / "backlog", waves, True), "",
                          "## Story Waves", "", *self.wave_lines(waves, self.root / "backlog"), ""])

    def spec_text(self, directory):
        directory, text, scope, title = self.read_spec(directory)
        if scope is None or not scope:
            raise UsageError("spec.md requires a **Scope**: line containing PBI IDs")
        if text.count(BEGIN) != 1 or text.count(END) != 1 or text.index(BEGIN) >= text.index(END):
            raise UsageError("spec.md requires ordered BEGIN BACKLOG / END BACKLOG markers")
        ids = {i for i in self.scoped_ids(scope)
               if self.pbis[i].type in ("MAP", "EPIC", "FEATURE", "US", "SPIKE")}
        for identifier in list(ids):
            ids.update(self.ancestors(identifier))
        waves = self.schedule(scope)["story_waves"]
        content = self.tree(ids, directory, waves)
        content += ["", "### Delivery Waves", "", *self.wave_lines(waves, directory)]
        spikes = self.open_spikes(scope)
        if spikes:
            content += ["", "### Open Spikes", "", *("- " + self.link(p, directory) for p in spikes)]
        start, end = text.index(BEGIN) + len(BEGIN), text.index(END)
        return text[:start] + "\n\n" + "\n".join(content) + "\n\n" + text[end:]

    def open_spikes(self, scope):
        ids = self.scoped_ids(scope)
        targets = {target for identifier in ids if self.pbis[identifier].type == "US"
                   for target in self.raw_blockers(self.pbis[identifier])}
        result = []
        for identifier in targets:
            pbi = self.pbis.get(identifier)
            if pbi is not None and pbi.type == "SPIKE":
                boxes = checkboxes(sections(pbi.body).get("Exit Criteria", ""))
                if not boxes or not all(box.lower() == "x" for box in boxes):
                    result.append(pbi)
        return sorted(result, key=sort_key)

    def acceptance_tests_on(self):
        path = self.root / ".specify/memory/constitution.md"
        text = clean_markdown(path.read_text(encoding="utf-8")) if path.exists() else ""
        return not re.search(r"Acceptance tests from Gherkin[^\w\n]*(?:[:=][^\w\n]*)?off\b", text, re.I)

    def task_selection(self, scope):
        ids = self.scoped_ids(scope)
        stories = [p for p in self.pbis.values() if p.id in ids and p.type == "US"]
        context = ids | {a for i in ids for a in self.ancestors(i)}
        maps = sorted((self.pbis[i] for i in context if self.pbis[i].type == "MAP"), key=sort_key)
        skeleton = set()
        for map_pbi in maps:
            for target in self.skeleton_ids(map_pbi):
                pbi = self.pbis.get(target)
                if pbi and pbi.type == "TASK" and (map_pbi.id in scope or
                        bool(ids.intersection(self.descendants(pbi.parent)))):
                    skeleton.add(target)
        tasks = sorted((p for p in self.pbis.values() if p.type == "TASK" and
                        (p.id in ids or p.id in skeleton)), key=sort_key)
        return stories, tasks, skeleton, maps

    def covers(self, pbi):
        lines = re.findall(r"^\s*\*\*Covers(?::\*\*|\*\*:)\s*(.*)$", clean_markdown(pbi.body), re.M)
        return set(re.findall(r"US-\d{3,}/AC-\d+\b", " ".join(lines)))

    def acceptance_criteria(self, pbi):
        return re.findall(r"^###\s+AC-(\d+):\s*(.+)$", sections(pbi.body).get("Acceptance Criteria", ""), re.M)

    def tasks_text(self, directory):
        directory, _, scope, title = self.read_spec(directory)
        if not scope:
            raise UsageError("spec.md requires a **Scope**: line containing PBI IDs")
        stories, tasks, skeleton, maps = self.task_selection(scope)
        global_waves, path = self.schedule_items(tasks)
        story_waves, _ = self.schedule_items(stories)
        story_ids = {p.id for p in stories}
        story_tasks = {p.id for p in tasks if p.parent in story_ids}

        def depends_on_story(pbi):
            todo, seen = list(self.raw_blockers(pbi)), set()
            while todo:
                identifier = todo.pop()
                if identifier in seen:
                    continue
                seen.add(identifier)
                if identifier in story_ids | story_tasks:
                    return True
                if identifier in self.pbis:
                    todo.extend(self.raw_blockers(self.pbis[identifier]))
            return False

        containers = [p for p in tasks if p.id not in story_tasks | skeleton]
        polish = [p for p in containers if depends_on_story(p)]
        pre = [p for p in containers if p not in polish]
        setup_ids = {item["id"] for wave in global_waves if wave["wave"] == 1 for item in wave["items"]}
        phase_groups = []
        for name, group in [("Setup", [p for p in pre if p.id in setup_ids]),
                            ("Walking Skeleton", [p for p in tasks if p.id in skeleton]),
                            ("Foundational", [p for p in pre if p.id not in setup_ids])]:
            if group:
                phase_groups.append((name, group, None))
        story_lookup = {item["id"]: wave for wave in story_waves for item in wave["items"]}
        populated_lanes, assigned = [], set()
        for map_pbi in maps:
            for heading, lane_ids in self.lanes(map_pbi):
                lane_story_ids = set(lane_ids)
                for identifier in lane_ids:
                    if identifier in self.pbis and self.pbis[identifier].type in ("FEATURE", "US"):
                        lane_story_ids.update(self.descendants(identifier))
                group = sorted((p for p in stories if p.id in lane_story_ids - assigned),
                               key=lambda p: (story_lookup[p.id]["wave"], sort_key(p)))
                if group:
                    populated_lanes.append((heading, group))
                    assigned.update(p.id for p in group)
        if len(populated_lanes) >= 2:
            for number, (heading, group) in enumerate(populated_lanes):
                phase_groups.append((heading + (" 🎯 MVP" if number == 0 else ""), [], group))
            unassigned = [p for p in stories if p.id not in assigned]
            if unassigned:
                phase_groups.append(("Other scoped stories", [], unassigned))
            mvp = populated_lanes[0][0]
        else:
            for wave in story_waves:
                group = [self.pbis[item["id"]] for item in wave["items"]]
                phase_groups.append((f"Story Wave {wave['wave']}" + (" 🎯 MVP" if wave["wave"] == 1 else ""), [], group))
            mvp = "Story Wave 1" if story_waves else "none"
        if polish:
            phase_groups.append(("Polish", polish, None))
        done = sum(is_task_done(p) for p in tasks)
        parallel = sum(item["parallel"] for wave in global_waves for item in wave["items"])
        lines = [f"# Tasks: {title}", "", f"**Spec**: [{title} specification](spec.md) | **Plan**: [{title} implementation plan](plan.md)", "",
                 "Generated by `scripts/backlog.py render-tasks`; do not edit by hand.", "",
                 f"**Tests**: Acceptance tests from Gherkin: {'on' if self.acceptance_tests_on() else 'off'}", "",
                 "## Summary", "", f"**Total tasks:** {len(tasks)} | **Completed:** {done} | **Parallelizable:** {parallel} [P] | **Waves:** {len(global_waves)} | **MVP:** {mvp}", ""]

        def task_line(pbi, is_parallel):
            link = Path(os.path.relpath(pbi.path, directory)).as_posix()
            flags = (" [P]" if is_parallel else "") + (f" [{pbi.parent}]" if pbi.parent in story_ids else "")
            return f"- [{'X' if is_task_done(pbi) else ' '}] {pbi.id}{flags} {pbi.title} → [{link}]({link})"

        for number, (heading, group_tasks, group_stories) in enumerate(phase_groups, 1):
            lines += [f"## Phase {number}: {heading}", ""]
            if group_stories is not None:
                for story in group_stories:
                    story_waves_local, _ = self.schedule_items([p for p in tasks if p.parent == story.id])
                    lines += [f"### US [{story.id}]" + (" [P]" if story_lookup[story.id]["parallel"] else "") + f" {story.title}", ""]
                    for wave in story_waves_local:
                        lines.extend(task_line(self.pbis[item["id"]], item["parallel"]) for item in wave["items"])
                    lines.append("")
            else:
                phase_waves, _ = self.schedule_items(group_tasks)
                for wave in phase_waves:
                    lines.extend(task_line(self.pbis[item["id"]], item["parallel"]) for item in wave["items"])
                lines.append("")
        lines += ["## Wave Schedule & Dependency Graph", "", "| Wave | Tasks | Dependencies and parallelism |",
                  "| --- | --- | --- |"]
        for wave in global_waves:
            labels = ", ".join(self.link(self.pbis[item["id"]], directory) for item in wave["items"])
            blockers = sorted({blocker for item in wave["items"] for blocker in item["blockers"]})
            dependencies = ", ".join(self.link(self.pbis[i], directory) for i in blockers) or "No blockers"
            lines.append(f"| {wave['wave']}{' [P]' if wave['parallel'] else ''} | {labels} | {dependencies} |")
        lines += ["", "**Critical path:** " + (" → ".join(self.link(self.pbis[i], directory) for i in path) or "none"), "",
                  "## Traceability Matrix", "", "| User Story | Acceptance Criterion | Test tasks | Implementation tasks |",
                  "| --- | --- | --- | --- |"]
        for story in sorted(stories, key=lambda p: (story_lookup[p.id]["wave"], sort_key(p))):
            for number, ac_title in self.acceptance_criteria(story):
                reference = f"{story.id}/AC-{number}"
                test_tasks = [p for p in tasks if reference in self.covers(p)]
                implementation = [p for p in tasks if p.parent == story.id and not self.covers(p)]
                labels = lambda group: ", ".join(self.link(p, directory) for p in group) or "—"
                lines.append(f'| {self.link(story, directory)} | {reference} "{ac_title}" | {labels(test_tasks)} | {labels(implementation)} |')
        return "\n".join(lines) + "\n", tasks, global_waves


def pack_waves(items, blockers_map, files_map):
    by_id = {pbi.id: pbi for pbi in items}
    depths, visiting = {}, set()

    def depth(identifier):
        if identifier in depths:
            return depths[identifier]
        if identifier in visiting:
            return 0  # Invalid cycles are diagnosed by check, never hang renderers.
        visiting.add(identifier)
        value = 1 + max((depth(b) for b in sorted(blockers_map.get(identifier, set())) if b in by_id), default=0)
        visiting.remove(identifier)
        depths[identifier] = value
        return value

    for identifier in sorted(by_id):
        depth(identifier)
    waves, assigned = {}, {}
    for pbi in sorted(items, key=lambda p: (depths[p.id], sort_key(p))):
        wave = max([1] + [assigned[b] + 1 for b in blockers_map[pbi.id] if b in assigned])
        while any(not files_map[pbi.id].isdisjoint(files_map[other.id]) for other in waves.get(wave, [])):
            wave += 1
        waves.setdefault(wave, []).append(pbi)
        assigned[pbi.id] = wave
    return [{"wave": number, "parallel": len(group) >= 2,
             "items": [{"id": p.id, "type": p.type, "title": p.title, "rank": p.rank, "parent": p.parent,
                        "done": is_task_done(p) if p.type == "TASK" else False,
                        "parallel": len(group) >= 2, "files": sorted(files_map[p.id]),
                        "blockers": sorted(blockers_map[p.id])} for p in group]}
            for number, group in sorted(waves.items())]


def critical_path(waves, blockers, files):
    order = [(wave["wave"], item["id"]) for wave in waves for item in wave["items"]]
    chains = {}
    for wave, identifier in order:
        previous = {other for earlier, other in order if earlier < wave and
                    (other in blockers[identifier] or not files[identifier].isdisjoint(files[other]))}
        candidates = [chains[other] for other in sorted(previous) if other in chains]
        best = max(candidates, key=lambda chain: (len(chain), tuple(chain)), default=[])
        chains[identifier] = best + [identifier]
    return max(chains.values(), key=lambda chain: (len(chain), tuple(chain)), default=[])


def has_cycle(graph):
    visiting, complete = set(), set()

    def visit(node):
        if node in visiting:
            return True
        if node in complete:
            return False
        visiting.add(node)
        if any(visit(target) for target in sorted(graph.get(node, set())) if target in graph):
            return True
        visiting.remove(node)
        complete.add(node)
        return False

    return any(visit(node) for node in sorted(graph) if node not in complete)


def reachable(graph, source, target):
    todo, seen = list(graph.get(source, set())), set()
    while todo:
        node = todo.pop()
        if node == target:
            return True
        if node not in seen:
            seen.add(node)
            todo.extend(graph.get(node, set()))
    return False


def validate_links(project, path, text):
    for target in re.findall(r"\[[^\]\n]*\]\(\s*<?([^\s)>]+)>?(?:\s+[^)]*)?\)", clean_markdown(text)):
        parsed = urlsplit(target)
        if (parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith("/")
                or "{{" in target or "}}" in target):
            continue
        local = unquote(parsed.path)
        target_path = (path.parent / local).resolve()
        try:
            target_path.relative_to(project.root)
        except ValueError:
            continue
        if not target_path.exists():
            project.report.add("broken-link", project.rel(path), f"Missing local target: {target}")


ADR_DIRS = ("docs/architecture/adr", "docs/decisions", "doc/adr", "adr")
ADR_FILENAME_RE = re.compile(r"^\d{4}-[a-z0-9-]+\.md$")
ADR_STATUS_RE = re.compile(r"^\|\s*\*\*Status\*\*\s*\|\s*(.*?)\s*\|\s*$", re.M)
ADR_SUPERSEDES_RE = re.compile(r"^Superseded by \[ADR-(\d{4}):[^\]]+\]\(([^)]+)\)$")


def validate_adrs(project):
    """Validate names, unique IDs, statuses and explicit negative consequences."""
    entries = []
    for relative_dir in ADR_DIRS:
        directory = project.root / relative_dir
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.md")):
            if path.name.lower() in {"readme.md", "index.md"}:
                continue
            if not ADR_FILENAME_RE.fullmatch(path.name):
                project.report.add("adr-file-name", project.rel(path),
                                   "Expected NNNN-kebab-slug.md")
                continue
            entries.append(path)

    by_id = {}
    for path in entries:
        identifier = path.name[:4]
        by_id.setdefault(identifier, []).append(path)
    for identifier, paths in sorted(by_id.items()):
        if len(paths) > 1:
            for path in paths:
                project.report.add("adr-duplicate-id", project.rel(path),
                                   f"Duplicate ADR ID {identifier}")

    valid_statuses = {"Proposed", "Accepted", "Rejected", "Deprecated"}
    for path in entries:
        name = project.rel(path)
        text = clean_markdown(path.read_text(encoding="utf-8"))
        status_match = ADR_STATUS_RE.search(text)
        status = status_match[1].strip() if status_match else ""
        if status not in valid_statuses:
            supersedes = ADR_SUPERSEDES_RE.fullmatch(status)
            if not supersedes:
                project.report.add("adr-status", name,
                                   "Status must be Proposed, Accepted, Rejected, Deprecated, or a valid Superseded by ADR link")
            else:
                target_id, target = supersedes.groups()
                target_path = (path.parent / unquote(target)).resolve()
                same_id = target_path.name.startswith(target_id + "-")
                if not same_id or not target_path.is_file():
                    project.report.add("adr-status", name,
                                       f"Superseding ADR target does not exist: {target}")

        negative = re.search(r"^###\s+Negative\s*$([\s\S]*?)(?=^#{1,3}\s|\Z)", text, re.M)
        bullets = re.findall(r"^\s*-\s+\S", negative[1], re.M) if negative else []
        if len(bullets) < 2:
            project.report.add("adr-consequences", name,
                               "### Negative must contain at least two concrete bullet items")


def validate_spec_documents(project, directory):
    """Check links in modular companion artifacts and contract Markdown files."""
    names = ("plan.md", "research.md", "data-model.md", "quickstart.md")
    paths = [directory / name for name in names]
    contracts = directory / "contracts"
    if contracts.is_dir():
        paths.extend(contracts.rglob("*.md"))
    for path in paths:
        if path.is_file():
            validate_links(project, path, path.read_text(encoding="utf-8"))


def validate_adr_links(project):
    for relative_dir in ADR_DIRS:
        directory = project.root / relative_dir
        if directory.is_dir():
            for path in sorted(directory.glob("*.md")):
                validate_links(project, path, path.read_text(encoding="utf-8"))


def validate_pbis(project):
    pbis, report = project.pbis, project.report
    for path, body in project.documents:
        validate_links(project, path, body)
    for pbi in pbis.values():
        file = project.rel(pbi.path)
        add = lambda code, message, warning=False: report.add(code, file, message, warning)
        parents = [key for key, rel in pbi.relations.items() if rel.get("relationType") == "PARENT"]
        if len(parents) > 1:
            add("multiple-parents", "At most one PARENT is allowed")
        relation_keys = []
        for target, rel in pbi.relations.items():
            relation, kind = rel.get("relationType"), rel.get("type")
            relation_keys.append((RELATION_ORDER.index(relation) if relation in RELATION_ORDER else 999,
                                  PBI_TYPES.index(kind) if kind in PBI_TYPES else 999, numeric_id(target), target))
            if relation not in RELATION_ORDER:
                add("relation-type", f"Invalid relationType for {target}: {relation}")
            if target == pbi.id:
                add("self-reference", f"Self relation: {target}")
            if target not in pbis:
                is_pbi = bool(re.fullmatch(r"(?:MAP|EPIC|FEATURE|US|SPIKE|BUG|TASK)-\d+", target))
                add("unknown-id" if is_pbi else "external-id", f"Unknown relation target: {target}", not is_pbi)
                continue
            other = pbis[target]
            if kind != other.type:
                add("relation-type", f"{target} is {other.type}, not {kind}")
            if rel.get("title") != other.title:
                add("relation-title", f"Title does not match {target}: {other.title}", True)
            if relation == "PARENT" and other.type not in ALLOWED_PARENTS.get(pbi.type, ()):
                add("hierarchy", f"{pbi.type} cannot have a {other.type} parent")
            if relation == "RELATED" and other.relations.get(pbi.id, {}).get("relationType") == "RELATED":
                add("inverse-relation", f"Declare RELATED only once: {target}")
            if relation == "RELATED" and target in project.ancestors(pbi.id):
                add("redundant-relation", f"{target} is already an ancestor", True)
        if relation_keys != sorted(relation_keys):
            add("relation-order", "Use PARENT, BLOCKED_BY, RELATED; then PBI type and numeric ID")
        sec = sections(pbi.body)
        required_scope = "Scope Boundaries" if pbi.type == "EPIC" else "Out of Scope"
        if pbi.type != "BUG" and required_scope not in sec:
            add("out-of-scope", f"Missing ## {required_scope}")
        if pbi.type == "FEATURE" and not {"Outcome", "Constraints"} <= sec.keys():
            add("feature-sections", "FEATURE requires ## Outcome and ## Constraints")
        if pbi.type == "TASK" and (not {"Files", "Actions to complete"} <= sec.keys() or
                                     not any(name.startswith("Definition of Done") for name in sec)):
            add("task-sections", "TASK requires Files, Actions to complete and Definition of Done")
        if pbi.type in ("US", "EPIC"):
            criteria = project.acceptance_criteria(pbi)
            if "Acceptance Criteria" not in sec:
                add("acceptance-criteria", "Missing ## Acceptance Criteria")
            headings = re.findall(r"^###\s+(.+)$", sec.get("Acceptance Criteria", ""), re.M)
            if not criteria or len(criteria) != len(headings):
                add("ac-id", "Each acceptance scenario needs ### AC-n: Title")
            if criteria and [int(number) for number, _ in criteria] != list(range(1, len(criteria) + 1)):
                add("ac-sequence", "Acceptance criteria must be numbered from AC-1 without gaps")
            if pbi.type == "US":
                for criterion in acceptance_blocks(pbi.body):
                    for code, message, warning in gherkin_issues(pbi.id, criterion):
                        add(code, message, warning)
        if pbi.type in ("MAP", "EPIC", "FEATURE", "US") and not re.match(r"As (?:a|an) ", clean_markdown(pbi.body).lstrip()):
            add("connextra", "Body should start with As a / As an", True)
    parent_graph = {p.id: {p.parent} if p.parent else set() for p in pbis.values()}
    graph = {p.id: project.raw_blockers(p) for p in pbis.values()}
    if has_cycle(parent_graph):
        report.add("cycle", "backlog", "PARENT cycle")
    effective_cycles = has_cycle(graph)
    for kind in ("US", "TASK"):
        effective_cycles |= has_cycle(project.effective_blockers([p for p in pbis.values() if p.type == kind]))
    if effective_cycles:
        report.add("cycle", "backlog", "Effective BLOCKED_BY cycle")
    for pbi in pbis.values():
        for target in sorted(graph[pbi.id]):
            other = pbis.get(target)
            if other and pbi.type == other.type and pbi.parent == other.parent and pbi.rank is not None and other.rank is not None and pbi.rank < other.rank:
                report.add("rank-order", project.rel(pbi.path), f"Higher priority {pbi.id} waits for lower priority {target}")
        for other in pbis.values():
            if other.id in graph[pbi.id] or other.id == pbi.id:
                continue
            if other.type == pbi.type and other.parent == pbi.parent and pbi.rank is not None and other.rank is not None and pbi.rank < other.rank and reachable(graph, pbi.id, other.id):
                report.add("rank-order", project.rel(pbi.path), f"Transitively waits for lower priority {other.id}")
        for target in sorted(pbi.blockers):
            if any(reachable(graph, blocker, target) for blocker in pbi.blockers - {target}):
                report.add("redundant-relation", project.rel(pbi.path), f"Transitively implied blocker: {target}", True)
        if pbi.type != "MAP":
            continue
        positions = {}
        for number, (_, ids) in enumerate(project.lanes(pbi)):
            for identifier in ids:
                if identifier not in pbis:
                    report.add("lane-unknown-id", project.rel(pbi.path), f"Unknown lane PBI: {identifier}")
                    continue
                positions.setdefault(identifier, number)
        for identifier in project.descendants(pbi.id):
            if pbis[identifier].type == "US" and identifier not in positions:
                report.add("lane-missing", project.rel(pbi.path), f"No Release Lane for {identifier}")
        candidates = [pbis[i] for i in positions if pbis[i].type in ("US", "FEATURE")]
        mapped = project.effective_blockers(candidates)
        for identifier, blockers in mapped.items():
            if any(positions[b] > positions[identifier] for b in blockers):
                report.add("lane-order", project.rel(pbi.path), f"{identifier} is in a lane before its blocker")


def check_project(project, spec=None):
    validate_pbis(project)
    report = project.report
    validate_adrs(project)
    validate_adr_links(project)
    if spec is not None:
        directories = [project.spec_path(spec)]
    else:
        directories = sorted(path.parent for path in (project.root / "specs").glob("*/spec.md"))
    checked = []
    for directory in directories:
        path = directory / "spec.md"
        name = project.rel(path)
        checked.append(project.rel(directory))
        if not path.is_file():
            report.add("spec-missing", name, "Missing spec.md")
            continue
        _, text, scope, _ = project.read_spec(directory)
        validate_links(project, path, text)
        validate_spec_documents(project, directory)
        if "{{" in text:
            report.add("placeholder", name, "Unresolved template placeholder")
        if not scope:
            report.add("scope-missing", name, "Missing **Scope**: PBI IDs")
        for identifier in scope or []:
            if identifier not in project.pbis:
                report.add("scope-unknown-id", name, f"Unknown scope: {identifier}")
            elif project.pbis[identifier].type in ("TASK", "SPIKE"):
                report.add("scope-invalid-type", name, f"Scope cannot directly contain {identifier}")
        try:
            expected = project.spec_text(directory)
        except UsageError:
            if text.count(BEGIN) != 1 or text.count(END) != 1 or text.find(BEGIN) >= text.find(END):
                report.add("spec-backlog-markers", name, "Missing or unordered backlog markers")
        else:
            if expected != text:
                report.add("spec-backlog-stale", name, "Run render-spec")
        tasks_path = directory / "tasks.md"
        if tasks_path.is_file():
            tasks_text = tasks_path.read_text(encoding="utf-8")
            validate_links(project, tasks_path, tasks_text)
            if scope:
                expected_tasks, tasks, _ = project.tasks_text(directory)
                if expected_tasks != tasks_text:
                    report.add("tasks-index-stale", project.rel(tasks_path), "Run render-tasks")
                if project.acceptance_tests_on():
                    covered = set().union(*(project.covers(p) for p in tasks))
                    for identifier in sorted(project.scoped_ids(scope)):
                        pbi = project.pbis[identifier]
                        if pbi.type == "US":
                            for number, title in project.acceptance_criteria(pbi):
                                if f"{identifier}/AC-{number}" not in covered:
                                    report.add("ac-uncovered", project.rel(tasks_path), f'{identifier}/AC-{number} "{title}" has no Covers task')
    index = project.root / "backlog/index.md"
    if spec is None and index.is_file() and index.read_text(encoding="utf-8") != project.index_text():
        report.add("index-stale", "backlog/index.md", "Run render-index")
    return {"ok": not report.errors, "checked_specs": checked, "pbis": project.counts(),
            "errors": report.errors, "warnings": report.warnings}


def export_features(project, spec_dir, out_dir):
    """Write one .feature file per scoped US; write nothing while any scenario is invalid."""
    _, _, scope, _ = project.read_spec(spec_dir)
    if not scope:
        raise UsageError("spec.md requires a **Scope**: line containing PBI IDs")
    stories = sorted((project.pbis[i] for i in project.scoped_ids(scope) if project.pbis[i].type == "US"),
                     key=lambda pbi: (numeric_id(pbi.id), pbi.id))
    errors = []
    for pbi in stories:
        criteria = acceptance_blocks(pbi.body)
        if not criteria:
            errors.append({"code": "ac-id", "file": project.rel(pbi.path), "message": "No ### AC-n: Title scenarios"})
        for criterion in criteria:
            errors.extend({"code": code, "file": project.rel(pbi.path), "message": message}
                          for code, message, warning in gherkin_issues(pbi.id, criterion) if not warning)
    if errors:
        return {"ok": False, "errors": errors, "files": []}
    out = Path(out_dir)
    out = (out if out.is_absolute() else project.root / out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    files = []
    for pbi in stories:
        path = out / (pbi.path.stem + ".feature")
        path.write_text(feature_text(pbi), encoding="utf-8")
        files.append(project.rel(path))
    return {"ok": True, "files": files, "stories": len(files)}


class JsonParser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)

    def print_help(self, file=None):
        print(json.dumps({"ok": True, "help": self.format_help()}, ensure_ascii=False, indent=2), file=file)


def find_root(explicit=None):
    if explicit is not None:
        root = Path(explicit).resolve()
        if not root.is_dir():
            raise UsageError(f"Missing project directory: {root}")
        return root
    current = Path.cwd().resolve()
    for root in (current, *current.parents):
        if (root / ".specify").is_dir() or (root / "backlog").is_dir():
            return root
    raise UsageError("No project root found (expected .specify/ or backlog/); use --root")


def main(argv=None):
    parser = JsonParser(description=__doc__)
    parser.add_argument("--root")
    sub = parser.add_subparsers(dest="command", required=True)
    next_parser = sub.add_parser("next-id")
    next_parser.add_argument("type", type=str.upper)
    next_parser.add_argument("--count", type=int, default=1)
    locate = sub.add_parser("locate")
    locate.add_argument("id")
    locate.add_argument("--descendants", action="store_true")
    for name in ("schedule", "check"):
        sub.add_parser(name).add_argument("--spec")
    sub.add_parser("render-index")
    for name in ("render-spec", "render-tasks"):
        sub.add_parser(name).add_argument("spec_dir")
    export = sub.add_parser("export-features")
    export.add_argument("spec_dir")
    export.add_argument("out_dir")
    try:
        args = parser.parse_args(argv)
        project = Project(find_root(args.root))
        if args.command == "next-id":
            if args.type not in PBI_TYPES or args.count < 1:
                raise UsageError("Expected a known PBI type and --count >= 1")
            maximum = max((numeric_id(p.id) for p in project.pbis.values()
                           if re.fullmatch(re.escape(args.type) + r"-\d+", p.id)), default=0)
            ids = [f"{args.type}-{number:03d}" for number in range(maximum + 1, maximum + 1 + args.count)]
            result = {"ok": True, "type": args.type, "next": ids[0], "ids": ids}
        elif args.command == "locate":
            pbi = project.pbis.get(args.id)
            if pbi is None:
                result = {"ok": False, "error": f"Unknown ID: {args.id}"}
            else:
                specs = []
                family = {pbi.id, *project.ancestors(pbi.id)}
                for path in sorted((project.root / "specs").glob("*/spec.md")):
                    _, _, scope, _ = project.read_spec(path.parent)
                    if family.intersection(scope or []):
                        specs.append(project.rel(path.parent))
                result = {"ok": True, "id": pbi.id, "type": pbi.type, "title": pbi.title, "rank": pbi.rank,
                          "file": project.rel(pbi.path), "referenced_by": sorted(p.id for p in project.pbis.values() if pbi.id in p.relations), "specs": specs}
                if args.descendants:
                    result["descendants"] = project.descendants(pbi.id)
        elif args.command == "schedule":
            scope = project.read_spec(args.spec)[2] if args.spec else None
            result = project.schedule(scope)
        elif args.command == "render-index":
            path = project.root / "backlog/index.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(project.index_text(), encoding="utf-8")
            result = {"ok": True, "file": "backlog/index.md", "pbis": project.counts(), "story_waves": len(project.schedule()["story_waves"])}
        elif args.command == "render-spec":
            directory, _, scope, _ = project.read_spec(args.spec_dir)
            (directory / "spec.md").write_text(project.spec_text(directory), encoding="utf-8")
            waves = project.schedule(scope)["story_waves"]
            result = {"ok": True, "file": project.rel(directory / "spec.md"), "scope": scope,
                      "stories": sum(len(w["items"]) for w in waves), "waves": len(waves)}
        elif args.command == "render-tasks":
            directory = project.spec_path(args.spec_dir)
            text, tasks, waves = project.tasks_text(directory)
            (directory / "tasks.md").write_text(text, encoding="utf-8")
            result = {"ok": True, "file": project.rel(directory / "tasks.md"), "tasks": len(tasks),
                      "done": sum(is_task_done(p) for p in tasks), "waves": len(waves)}
        elif args.command == "export-features":
            result = export_features(project, args.spec_dir, args.out_dir)
        else:
            result = check_project(project, args.spec)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 1
    except (UsageError, OSError, UnicodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
