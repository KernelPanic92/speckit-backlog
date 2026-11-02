#!/usr/bin/env bash
# Check a project initialized with the backlog preset (Claude integration, skills mode).
#   tests/check_install.sh /path/to/project
# Needs SPECKIT_PYTHON_EXECUTABLE (or python3) with PyYAML, for spec-kit's template resolver.
set -euo pipefail

PROJ="${1:?usage: tests/check_install.sh <project dir>}"
cd "$PROJ"
fail=0
ok() { printf '  ok    %s\n' "$1"; }
ko() { printf '  FAIL  %s\n' "$1"; fail=1; }

echo "Templates resolve from the preset"
# name|marker (no associative arrays: macOS ships bash 3.2)
for pair in \
  "constitution-template|## Delivery Conventions" \
  "product-template|## Ubiquitous Language" \
  "design-template|version: alpha" \
  "spec-template|SPEC ENVELOPE" \
  "plan-template|## Delivery Slices" \
  "research-template|## Validity" \
  "tasks-template|execution index" \
  "sync-clickup-template|tool: clickup" \
  "sync-multica-template|tool: multica" \
  "pbi-map-template|type: MAP" \
  "pbi-epic-template|type: EPIC" \
  "pbi-story-template|### AC-1:" \
  "pbi-task-template|type: TASK" \
  "pbi-spike-template|type: SPIKE"; do
  name="${pair%%|*}" marker="${pair#*|}"
  content="$(bash .specify/scripts/bash/resolve-template.sh "$name" --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["TEMPLATE_CONTENT"])' 2>/dev/null || true)"
  if [[ "$content" == *"$marker"* ]]; then ok "$name"; else ko "$name (marker '$marker' not found)"; fi
done

echo "Skills are registered"
for skill in constitution specify clarify plan tasks analyze implement checklist converge split merge sync; do
  file=".claude/skills/speckit-$skill/SKILL.md"
  [[ -f "$file" ]] && ok "speckit-$skill" || ko "speckit-$skill missing"
done
grep -q "## Working mode" .claude/skills/speckit-specify/SKILL.md && ok "specify is the preset version" || ko "specify is not the preset version"
grep -q "hooks.before_specify" .claude/skills/speckit-specify/SKILL.md && ok "specify keeps the before_specify hook" || ko "specify lost the before_specify hook"
for skill in implement checklist converge; do
  file=".claude/skills/speckit-$skill/SKILL.md"
  if grep -q 'Preset `backlog` addendum' "$file" && grep -q "check-prerequisites" "$file"; then ok "$skill = core + addendum"; else ko "$skill composition"; fi
done
if grep -l "__SPECKIT_COMMAND_\|{SCRIPT}\|@@UPSTREAM" .claude/skills/speckit-*/SKILL.md; then ko "unresolved tokens in the files above"; else ok "no unresolved tokens"; fi
if grep -h "\.specify/\.specify/\|\.specify/presets/backlog/\.specify" .claude/skills/speckit-*/SKILL.md; then ko "mangled preset paths"; else ok "preset paths intact"; fi

echo "Installed preset files"
for path in knowledge/user-story-writer/rules.md knowledge/user-story-writer/examples.md schemas/pbi-frontmatter.schema.json scripts/validate_backlog.py NOTICE.md LICENSE; do
  [[ -f ".specify/presets/backlog/$path" ]] && ok "$path" || ko "$path missing"
done
for path in tests tools .github catalog.json; do
  [[ -e ".specify/presets/backlog/$path" ]] && ko "$path should be excluded by .presetignore" || ok "$path excluded"
done
grep -q "## Delivery Conventions" .specify/memory/constitution.md && ok "constitution seeded from the preset template" || ko "constitution not seeded from the preset template"

echo "Validator runs from the installed preset"
out="$(uv run --no-project --quiet --with pyyaml --with jsonschema python .specify/presets/backlog/scripts/validate_backlog.py next-id US)"
[[ "$out" == *'"ok": true'* ]] && ok "next-id: $out" || ko "next-id: $out"

exit $fail
