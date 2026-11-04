#!/usr/bin/env python3
"""Deterministic checks for the backlog of a spec-kit project using the `backlog` preset.

Usage (from the project root):
    uv run --no-project --quiet --with pyyaml --with jsonschema \
        python .specify/presets/backlog/scripts/validate_backlog.py <command> [args]

Commands:
    check <feature-dir> | --all      validate PBIs, relations, spec.md and tasks.md
    next-id <TYPE> [--count N]       first free project-wide id(s) for a PBI type
    locate <ID> [--descendants]      where a PBI lives, who references it, its descendants
    sync-plan <tool> <feature-dir> | --all [--only ID]
                                     what a tracker extension must create, update or leave alone
                                     in an external tool, parents before children
    set-external <ID> <tool> [--id X] [--key K] [--url U] [--hash-current] [--remove]
                                     write (or remove) the PBI's reference to an external tool

Output is JSON on stdout. `check` exits 1 when errors are found, `locate` and
`set-external` when the id is unknown, every command exits 2 on usage or environment errors.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover - environment guard
    print(json.dumps({"ok": False, "error": f"missing dependency: {exc.name}. "
                      "Run through: uv run --no-project --with pyyaml --with jsonschema python ..."}))
    sys.exit(2)

PBI_TYPES = ("MAP", "EPIC", "US", "SPIKE", "BUG", "TASK")
RELATION_ORDER = ("PARENT", "BLOCKED_BY", "RELATED")
ROOT_TYPES = ("MAP", "EPIC", "US")
# child type -> allowed PARENT types (rules.md, "Hierarchy")
ALLOWED_PARENTS = {
    "MAP": ("EPIC",),            # "zoom" case only
    "EPIC": ("MAP",),
    "US": ("EPIC",),
    "BUG": ("EPIC",),
    "TASK": ("US", "EPIC"),      # EPIC for Walking Skeleton items
    "SPIKE": ("US", "EPIC"),     # EPIC for Walking Skeleton items
}
BACKLOG_DIRS = {"epics": "EPIC", "stories": "US", "spikes": "SPIKE", "tasks": "TASK"}
OUT_OF_SCOPE_HEADING = {"US": "## Out of Scope", "TASK": "## Out of Scope", "SPIKE": "## Out of Scope",
                        "MAP": "## Out of Scope", "EPIC": "## Scope Boundaries"}
MOCK_ID = re.compile(r"^(MAP|EPIC|US|SPIKE|BUG|TASK)-(\d+)$")
# a task line starts with an id (TASK-014, or a task-manager id such as CU-86c1x2); other
# checkbox lines of tasks.md (e.g. the Task Completion Criteria) are not tasks
TASK_LINE = re.compile(r"^\s*- \[[ xX]\] ([A-Z][A-Z0-9]*-[A-Za-z0-9]*\d[A-Za-z0-9]*)\b(.*)$")
LINK = re.compile(r"\]\(([^)\s]+\.md)\)")
LANE_ITEM = re.compile(r"\bUS \[([^\]]+)\]")

SCRIPT_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = SCRIPT_DIR.parent / "schemas" / "pbi-frontmatter.schema.json"


@dataclass
class Pbi:
    path: Path
    feature_dir: Path
    is_root: bool
    meta: dict
    body: str

    @property
    def id(self) -> str:
        return str(self.meta.get("id", ""))

    @property
    def type(self) -> str:
        return str(self.meta.get("type", ""))

    @property
    def title(self) -> str:
        return str(self.meta.get("title", ""))

    @property
    def relations(self) -> dict:
        rel = self.meta.get("relations") or {}
        return rel if isinstance(rel, dict) else {}

    @property
    def external(self) -> dict:
        ext = self.meta.get("external") or {}
        return ext if isinstance(ext, dict) else {}

    def parents(self) -> list[str]:
        return [str(k) for k, v in self.relations.items()
                if isinstance(v, dict) and v.get("relationType") == "PARENT"]


@dataclass
class Report:
    root: Path
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

    def _add(self, bucket: list, path: Path | None, code: str, message: str, pbi_id: str = "") -> None:
        entry = {"code": code, "message": message}
        if path is not None:
            entry["file"] = rel(path, self.root)
        if pbi_id:
            entry["id"] = pbi_id
        bucket.append(entry)

    def error(self, path, code, message, pbi_id=""):
        self._add(self.errors, path, code, message, pbi_id)

    def warn(self, path, code, message, pbi_id=""):
        self._add(self.warnings, path, code, message, pbi_id)


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def find_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / ".specify").is_dir():
            return candidate
    return start


def split_frontmatter(text: str) -> tuple[str | None, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        return None, text
    for i, line in enumerate(lines[1:], start=1):
        if line.rstrip("\r\n") == "---":
            return "".join(lines[1:i]), "".join(lines[i + 1:])
    return None, text


def section(body: str, heading: str) -> str:
    """Text of a `## ` section (without its heading), or '' when absent."""
    lines = body.splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == heading)
    except StopIteration:
        return ""
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return "\n".join(lines[start + 1:end])


def feature_dirs(specs_dir: Path) -> list[Path]:
    if not specs_dir.is_dir():
        return []
    return sorted(p.parent for p in specs_dir.glob("*/spec.md"))


def load_pbis(dirs: list[Path], report: Report | None) -> list[Pbi]:
    pbis = []
    for fdir in dirs:
        files = [(fdir / "spec.md", True)]
        files += [(p, False) for p in sorted((fdir / "backlog").rglob("*.md"))]
        for path, is_root in files:
            if not path.is_file():
                continue
            fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
            if fm is None:
                if report:
                    report.error(path, "frontmatter-missing", "no YAML frontmatter at the top of the file")
                continue
            try:
                meta = yaml.safe_load(fm) or {}
            except yaml.YAMLError as exc:
                if report:
                    report.error(path, "frontmatter-invalid", f"YAML error: {exc}")
                continue
            if not isinstance(meta, dict):
                if report:
                    report.error(path, "frontmatter-invalid", "frontmatter is not a mapping")
                continue
            pbis.append(Pbi(path, fdir, is_root, meta, body))
    return pbis


def relation_sort_key(item: tuple) -> tuple:
    pbi_id, rel_ = item
    rtype = rel_.get("relationType") if isinstance(rel_, dict) else None
    ptype = rel_.get("type") if isinstance(rel_, dict) else None
    m = MOCK_ID.match(str(pbi_id))
    id_key = (m.group(1), int(m.group(2))) if m else (str(pbi_id), 0)
    return (RELATION_ORDER.index(rtype) if rtype in RELATION_ORDER else 9,
            PBI_TYPES.index(ptype) if ptype in PBI_TYPES else 9,
            id_key)


def check_pbi(pbi: Pbi, by_id: dict, validator: Draft202012Validator, report: Report) -> None:
    text = pbi.path.read_text(encoding="utf-8")
    for err in sorted(validator.iter_errors(pbi.meta), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in err.path) or "(root)"
        report.error(pbi.path, "schema", f"{where}: {err.message}", pbi.id)
    if "{{" in text:
        report.error(pbi.path, "placeholder", "leftover {{...}} template placeholder", pbi.id)

    # file placement
    if not pbi.is_root:
        expected = BACKLOG_DIRS.get(pbi.path.parent.name)
        if expected and pbi.type != expected:
            report.error(pbi.path, "wrong-folder",
                         f"a {pbi.type} PBI does not belong in backlog/{pbi.path.parent.name}/", pbi.id)
        if pbi.id and not pbi.path.name.startswith(f"{pbi.id}-"):
            report.error(pbi.path, "file-name", f"file name must start with '{pbi.id}-'", pbi.id)
    elif pbi.type not in ROOT_TYPES:
        report.error(pbi.path, "root-type", f"spec.md root must be MAP, EPIC or US, found {pbi.type!r}", pbi.id)

    # relations
    parents = pbi.parents()
    if len(parents) > 1:
        report.error(pbi.path, "multiple-parents", f"more than one PARENT: {', '.join(parents)}", pbi.id)
    for ref_id, rel_ in pbi.relations.items():
        ref_id = str(ref_id)
        if not isinstance(rel_, dict):
            continue
        if ref_id == pbi.id:
            report.error(pbi.path, "self-reference", "a PBI cannot reference itself", pbi.id)
            continue
        target = by_id.get(ref_id)
        if target is None:
            if MOCK_ID.match(ref_id):
                report.error(pbi.path, "unknown-id", f"relation to {ref_id}, which does not exist in the project", pbi.id)
            else:
                report.warn(pbi.path, "external-id", f"relation to {ref_id} cannot be verified (not in the project)", pbi.id)
            continue
        if rel_.get("type") != target.type:
            report.error(pbi.path, "relation-type",
                         f"relation to {ref_id} says type {rel_.get('type')}, the PBI is a {target.type}", pbi.id)
        if rel_.get("title") and rel_.get("title") != target.title:
            report.warn(pbi.path, "relation-title",
                        f"relation to {ref_id} has title {rel_.get('title')!r}, the PBI is titled {target.title!r}", pbi.id)
        if rel_.get("relationType") == "PARENT" and target.type not in ALLOWED_PARENTS.get(pbi.type, ()):
            report.error(pbi.path, "hierarchy", f"a {pbi.type} cannot have a {target.type} as PARENT", pbi.id)
        back = target.relations.get(pbi.id)
        if isinstance(back, dict) and pbi.id < ref_id:
            # A PARENT one way and a BLOCKED_BY the other way is legitimate (a story blocked by its own
            # Spike). Same-type pairs are cycles (reported by check_cycles); RELATED is declared once.
            kinds = {rel_.get("relationType"), back.get("relationType")}
            if kinds == {"RELATED"}:
                report.error(pbi.path, "inverse-relation",
                             f"RELATED between {pbi.id} and {ref_id} is declared on both PBIs; declare it on one only", pbi.id)
            elif "RELATED" in kinds:
                report.warn(pbi.path, "redundant-relation",
                            f"{pbi.id} and {ref_id} are already linked by a PARENT/BLOCKED_BY relation; RELATED is redundant", pbi.id)
    items = list(pbi.relations.items())
    if items != sorted(items, key=relation_sort_key):
        report.error(pbi.path, "relation-order",
                     "relations are not in canonical order (relationType PARENT, BLOCKED_BY, RELATED; "
                     "then type MAP, EPIC, US, SPIKE, BUG, TASK; then ascending id)", pbi.id)

    # required sections
    heading = OUT_OF_SCOPE_HEADING.get(pbi.type)
    if heading and heading not in (l.strip() for l in pbi.body.splitlines()):
        report.error(pbi.path, "out-of-scope", f"missing '{heading}' section", pbi.id)
    if pbi.type in ("US", "EPIC"):
        ac = section(pbi.body, "## Acceptance Criteria")
        if not ac.strip():
            report.error(pbi.path, "acceptance-criteria", "missing or empty '## Acceptance Criteria' section", pbi.id)
        numbers = []
        for line in ac.splitlines():
            if line.startswith("### "):
                m = re.match(r"^### AC-(\d+): \S", line)
                if not m:
                    report.error(pbi.path, "ac-id", f"scenario heading without 'AC-n: ' id: {line.strip()!r}", pbi.id)
                else:
                    numbers.append(int(m.group(1)))
        if numbers and numbers != list(range(1, len(numbers) + 1)):
            report.error(pbi.path, "ac-sequence", f"AC ids must be AC-1..AC-{len(numbers)} in order, found {numbers}", pbi.id)
    if pbi.type in ("US", "EPIC", "MAP"):
        first = next((l.strip() for l in pbi.body.splitlines() if l.strip() and not l.startswith("<!--")), "")
        if not re.match(r"^As an? ", first):
            report.warn(pbi.path, "connextra", "body should start with the Connextra sentence 'As a …, I want …, so that …'", pbi.id)


def pbi_body(pbi: Pbi) -> str:
    """The PBI's own body: in spec.md the spec envelope after the root PBI is excluded."""
    lines = pbi.body.splitlines()
    if pbi.is_root:
        cut = next((i for i, l in enumerate(lines) if l.strip() == "## Spec Context"), len(lines))
        lines = lines[:cut]
    return "\n".join(lines).strip()


def content_hash(pbi: Pbi) -> str:
    """Hash of what a sync publishes: frontmatter without `external`, plus the PBI's own body."""
    meta = {k: v for k, v in pbi.meta.items() if k != "external"}
    payload = json.dumps(meta, sort_keys=True, ensure_ascii=False, default=str) + "\n" + pbi_body(pbi)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def check_cycles(pbis: list[Pbi], scope: set, report: Report) -> None:
    for relation_type in ("PARENT", "BLOCKED_BY"):
        _check_cycles(pbis, relation_type, scope, report)


def _check_cycles(pbis: list[Pbi], relation_type: str, scope: set, report: Report) -> None:
    graph = {p.id: [str(k) for k, v in p.relations.items()
                    if isinstance(v, dict) and v.get("relationType") == relation_type]
             for p in pbis}
    paths = {p.id: p.path for p in pbis}
    dirs = {p.id: p.feature_dir.resolve() for p in pbis}
    state: dict[str, int] = {}

    def visit(node: str, stack: list[str]) -> None:
        state[node] = 1
        for nxt in graph.get(node, []):
            if nxt not in graph:
                continue
            if state.get(nxt) == 1:
                cycle = stack[stack.index(nxt):] + [nxt] if nxt in stack else [node, nxt]
                if dirs[node] in scope:
                    report.error(paths[node], "cycle", f"{relation_type} cycle: {' -> '.join(cycle)}", node)
            elif state.get(nxt) is None:
                visit(nxt, stack + [nxt])
        state[node] = 2

    for node in graph:
        if state.get(node) is None:
            visit(node, [node])


def check_feature(fdir: Path, pbis: list[Pbi], by_id: dict, report: Report) -> None:
    spec = fdir / "spec.md"
    if not spec.is_file():
        report.error(spec, "spec-missing", "spec.md not found")
        return
    root = next((p for p in pbis if p.feature_dir == fdir and p.is_root), None)
    children = [p for p in pbis if p.feature_dir == fdir and not p.is_root]
    spec_text = spec.read_text(encoding="utf-8")

    # links from spec.md and Backlog Index coverage
    for target in LINK.findall(spec_text):
        if "://" in target:
            continue
        if not (fdir / target).resolve().is_file():
            report.error(spec, "broken-link", f"link to {target}, which does not exist")
    linked = {(fdir / t).resolve() for t in LINK.findall(spec_text) if "://" not in t}
    for child in children:
        if child.type != "TASK" and child.path.resolve() not in linked:
            report.error(child.path, "not-indexed", "child PBI not linked from the Backlog Index of spec.md", child.id)
        if child.type != "TASK" and not child.parents():
            report.warn(child.path, "orphan", "child PBI without a PARENT relation", child.id)
        for parent_id in child.parents():
            parent = by_id.get(parent_id)
            if parent is not None and parent.feature_dir != fdir:
                report.warn(child.path, "parent-elsewhere",
                            f"PARENT {parent_id} lives in {rel(parent.feature_dir, report.root)}: is the file in the right spec?",
                            child.id)

    # map: no story in a lane earlier than one of its blockers
    if root is not None and root.type == "MAP":
        lanes = re.split(r"^### ", section(root.body, "## Release Lanes"), flags=re.M)[1:]
        lane_of: dict[str, int] = {}
        for index, lane in enumerate(lanes):
            for story_id in LANE_ITEM.findall(lane):
                lane_of.setdefault(story_id, index)
        for story_id, index in lane_of.items():
            story = by_id.get(story_id)
            if story is None:
                if MOCK_ID.match(story_id):
                    report.error(spec, "lane-unknown-id", f"Release Lanes reference {story_id}, which does not exist", root.id)
                continue
            for ref_id, rel_ in story.relations.items():
                if not (isinstance(rel_, dict) and rel_.get("relationType") == "BLOCKED_BY" and rel_.get("type") == "US"):
                    continue
                blocker_lane = lane_of.get(str(ref_id))
                if blocker_lane is None:
                    report.error(spec, "lane-order",
                                 f"{story_id} is in a Release Lane but {ref_id}, which blocks it, is in none", root.id)
                elif blocker_lane > index:
                    report.error(spec, "lane-order",
                                 f"{story_id} is in an earlier lane than {ref_id}, which blocks it", root.id)
        for child in children:
            if child.type == "US" and child.id not in lane_of:
                report.error(child.path, "lane-missing", "story of a map not placed in any Release Lane", child.id)

    # tasks.md <-> TASK files
    tasks_md = fdir / "tasks.md"
    task_files = {p.id: p for p in children if p.type == "TASK"}
    if tasks_md.is_file():
        listed = set()
        _, tasks_body = split_frontmatter(tasks_md.read_text(encoding="utf-8"))
        in_fence = False
        for line in tasks_body.splitlines():
            if line.strip().startswith("```"):
                in_fence = not in_fence
            m = None if in_fence else TASK_LINE.match(line)
            if not m:
                continue
            task_id = m.group(1)
            listed.add(task_id)
            if task_id not in task_files:
                report.error(tasks_md, "task-file-missing", f"{task_id} is listed in tasks.md but has no TASK file in backlog/tasks/")
            for target in LINK.findall(m.group(2)):
                if not (fdir / target).resolve().is_file():
                    report.error(tasks_md, "broken-link", f"{task_id} links to {target}, which does not exist")
        for task_id, task in task_files.items():
            if task_id not in listed:
                report.error(task.path, "task-not-listed", "TASK file not listed in tasks.md", task_id)


def cmd_check(args, root: Path) -> int:
    report = Report(root)
    specs_dir = root / "specs"
    all_dirs = feature_dirs(specs_dir)
    if args.all:
        targets = all_dirs
    else:
        target = (Path.cwd() / args.feature_dir).resolve() if args.feature_dir else None
        if target is None or not target.is_dir():
            print(json.dumps({"ok": False, "error": f"feature directory not found: {args.feature_dir}"}))
            return 2
        targets = [target]
        if target not in [d.resolve() for d in all_dirs]:
            all_dirs = all_dirs + [target]
    target_set = {t.resolve() for t in targets}

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    every = load_pbis(all_dirs, None)
    scoped = load_pbis(targets, report)  # parse errors are reported only for the checked dirs
    by_id: dict[str, Pbi] = {}
    for pbi in every:
        if pbi.id in by_id and by_id[pbi.id].path != pbi.path:
            if pbi.feature_dir.resolve() in target_set or by_id[pbi.id].feature_dir.resolve() in target_set:
                report.error(pbi.path, "duplicate-id",
                             f"id also used by {rel(by_id[pbi.id].path, root)}", pbi.id)
            continue
        by_id[pbi.id] = pbi
    for pbi in scoped:
        check_pbi(pbi, by_id, validator, report)
    check_cycles([p for p in every if by_id.get(p.id) is p], target_set, report)
    for fdir in targets:
        check_feature(fdir, every, by_id, report)

    counts: dict[str, int] = {}
    for pbi in scoped:
        counts[pbi.type] = counts.get(pbi.type, 0) + 1
    print(json.dumps({
        "ok": not report.errors,
        "checked": [rel(t, root) for t in targets],
        "pbis": counts,
        "errors": report.errors,
        "warnings": report.warnings,
    }, indent=2))
    return 1 if report.errors else 0


def cmd_next_id(args, root: Path) -> int:
    pbi_type = args.type.upper()
    if pbi_type not in PBI_TYPES:
        print(json.dumps({"ok": False, "error": f"unknown type {args.type!r}, expected one of {', '.join(PBI_TYPES)}"}))
        return 2
    used = 0
    pattern = re.compile(rf"^{pbi_type}-(\d+)$")
    for pbi in load_pbis(feature_dirs(root / "specs"), None):
        m = pattern.match(pbi.id)
        if m:
            used = max(used, int(m.group(1)))
    ids = [f"{pbi_type}-{n:03d}" for n in range(used + 1, used + 1 + max(args.count, 1))]
    print(json.dumps({"ok": True, "type": pbi_type, "next": ids[0], "ids": ids}))
    return 0


def cmd_locate(args, root: Path) -> int:
    pbis = load_pbis(feature_dirs(root / "specs"), None)
    by_id = {p.id: p for p in pbis}
    pbi = by_id.get(args.id)
    if pbi is None:
        print(json.dumps({"ok": False, "error": f"{args.id} not found under specs/"}))
        return 1

    def brief(p: Pbi) -> dict:
        return {"id": p.id, "type": p.type, "title": p.title, "file": rel(p.path, root)}

    result = {"ok": True, **brief(pbi), "feature_dir": rel(pbi.feature_dir, root), "is_root": pbi.is_root,
              "external": pbi.external,
              "referenced_by": [{**brief(p), "relationType": p.relations[pbi.id].get("relationType")}
                                for p in pbis if isinstance(p.relations.get(pbi.id), dict)]}
    if args.descendants:
        children: dict[str, list[Pbi]] = {}
        for p in pbis:
            for parent_id in p.parents():
                children.setdefault(parent_id, []).append(p)
        found, queue = [], [pbi.id]
        while queue:
            for child in children.get(queue.pop(0), []):
                if child.id not in {f.id for f in found} and child.id != pbi.id:
                    found.append(child)
                    queue.append(child.id)
        result["descendants"] = [brief(p) for p in found]
    print(json.dumps(result, indent=2))
    return 0


def cmd_sync_plan(args, root: Path) -> int:
    all_dirs = feature_dirs(root / "specs")
    if args.all:
        targets = all_dirs
    else:
        target = (Path.cwd() / args.feature_dir).resolve() if args.feature_dir else None
        if target is None or not target.is_dir():
            print(json.dumps({"ok": False, "error": f"feature directory not found: {args.feature_dir}"}))
            return 2
        targets = [target]
        if target not in [d.resolve() for d in all_dirs]:
            all_dirs = all_dirs + [target]
    target_set = {t.resolve() for t in targets}
    every = load_pbis(all_dirs, None)
    by_id = {p.id: p for p in every}
    scoped = {p.id: p for p in every if p.feature_dir.resolve() in target_set}
    if args.only:
        if args.only not in by_id:
            print(json.dumps({"ok": False, "error": f"{args.only} not found under specs/"}))
            return 1
        keep, queue = {args.only}, [args.only]
        while queue:
            current = queue.pop(0)
            for p in every:
                if current in p.parents() and p.id not in keep:
                    keep.add(p.id)
                    queue.append(p.id)
        scoped = {i: by_id[i] for i in keep}

    def first_parent(p: Pbi) -> str | None:
        return p.parents()[0] if p.parents() else None

    def ancestors(p: Pbi) -> list[str]:
        chain, seen, current = [], {p.id}, first_parent(p)
        while current and current in by_id and current not in seen:
            chain.append(current)
            seen.add(current)
            current = first_parent(by_id[current])
        return chain

    def sort_key(p: Pbi):
        m = MOCK_ID.match(p.id)
        return (PBI_TYPES.index(p.type) if p.type in PBI_TYPES else 9,
                (m.group(1), int(m.group(2))) if m else (p.id, 0))

    children: dict[str | None, list[Pbi]] = {}
    for p in scoped.values():
        parent = first_parent(p)
        children.setdefault(parent if parent in scoped else None, []).append(p)
    ordered: list[Pbi] = []

    def walk(parent_id: str | None) -> None:
        for child in sorted(children.get(parent_id, []), key=sort_key):
            ordered.append(child)
            walk(child.id)

    walk(None)

    def ref(pbi_id: str) -> dict | None:
        target = by_id.get(pbi_id)
        return target.external.get(args.tool) if target else None

    items, summary = [], {"create": 0, "update": 0, "unchanged": 0}
    for p in ordered:
        ext = p.external.get(args.tool)
        current_hash = content_hash(p)
        action = "create" if not ext else ("unchanged" if ext.get("hash") == current_hash else "update")
        summary[action] += 1
        parent = first_parent(p)
        items.append({
            "id": p.id, "type": p.type, "title": p.title, "file": rel(p.path, root),
            "feature_dir": rel(p.feature_dir, root), "is_root": p.is_root,
            "parent": parent, "parent_external": ref(parent) if parent else None,
            "ancestors": ancestors(p),
            "relations": [{"id": str(k), "relationType": v.get("relationType"), "type": v.get("type"),
                           "title": v.get("title"), "external": ref(str(k))}
                          for k, v in p.relations.items() if isinstance(v, dict) and v.get("relationType") != "PARENT"],
            "external": ext, "hash": current_hash, "action": action,
        })
    print(json.dumps({"ok": True, "tool": args.tool, "summary": summary, "items": items}, indent=2, ensure_ascii=False))
    return 0


def cmd_set_external(args, root: Path) -> int:
    pbi = next((p for p in load_pbis(feature_dirs(root / "specs"), None) if p.id == args.pbi_id), None)
    if pbi is None:
        print(json.dumps({"ok": False, "error": f"{args.pbi_id} not found under specs/"}))
        return 1
    external = {tool: dict(ref_) for tool, ref_ in pbi.external.items() if isinstance(ref_, dict)}
    if args.remove:
        external.pop(args.tool, None)
    else:
        ref_ = external.get(args.tool, {})
        for key in ("id", "key", "url"):
            if getattr(args, key):
                ref_[key] = getattr(args, key)
        if args.hash_current:
            ref_["hash"] = content_hash(pbi)
        if "id" not in ref_:
            print(json.dumps({"ok": False, "error": f"--id is required: {args.pbi_id} has no {args.tool} reference yet"}))
            return 2
        external[args.tool] = {k: ref_[k] for k in ("id", "key", "url", "hash") if k in ref_}

    text = pbi.path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    close = next(i for i, l in enumerate(lines[1:], start=1) if l.rstrip("\r\n") == "---")
    fm = lines[1:close]
    start = next((i for i, l in enumerate(fm) if re.match(r"^external:\s*$", l)), None)
    if start is not None:
        end = start + 1
        while end < len(fm) and (fm[end].startswith((" ", "\t")) or not fm[end].strip()):
            end += 1
        fm = fm[:start] + fm[end:]
    if external:
        block = ["external:\n"]
        for tool in sorted(external):
            block.append(f"    {tool}:\n")
            for key, value in external[tool].items():
                block.append(f"        {key}: {json.dumps(value)}\n")
        fm = fm + block
    pbi.path.write_text("".join([lines[0], *fm, *lines[close:]]), encoding="utf-8")
    print(json.dumps({"ok": True, "id": pbi.id, "file": rel(pbi.path, root), "external": external}, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", help="project root (default: nearest parent with a .specify/ directory)")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check")
    check.add_argument("feature_dir", nargs="?")
    check.add_argument("--all", action="store_true")
    next_id = sub.add_parser("next-id")
    next_id.add_argument("type")
    next_id.add_argument("--count", type=int, default=1)
    locate = sub.add_parser("locate")
    locate.add_argument("id")
    locate.add_argument("--descendants", action="store_true")
    plan = sub.add_parser("sync-plan")
    plan.add_argument("tool")
    plan.add_argument("feature_dir", nargs="?")
    plan.add_argument("--all", action="store_true")
    plan.add_argument("--only", help="limit the plan to this PBI and its descendants")
    setext = sub.add_parser("set-external")
    setext.add_argument("id")
    setext.add_argument("tool")
    setext.add_argument("--id", dest="ext_id")
    setext.add_argument("--key")
    setext.add_argument("--url")
    setext.add_argument("--hash-current", action="store_true", help="store the PBI's current content hash")
    setext.add_argument("--remove", action="store_true", help="remove the reference to this tool")
    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else find_root(Path.cwd().resolve())
    if args.command in ("check", "sync-plan") and not args.all and not args.feature_dir:
        parser.error(f"{args.command} needs a feature directory or --all")
    if args.command == "set-external":
        args.pbi_id, args.id = args.id, args.ext_id
    commands = {"check": cmd_check, "next-id": cmd_next_id, "locate": cmd_locate,
                "sync-plan": cmd_sync_plan, "set-external": cmd_set_external}
    return commands[args.command](args, root)


if __name__ == "__main__":
    sys.exit(main())
