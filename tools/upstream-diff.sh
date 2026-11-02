#!/usr/bin/env bash
# Show what changed in Spec Kit, between the version this preset is based on (BASE) and a newer
# tag, in the upstream files the preset replaces or composes. Port the relevant changes by hand.
#   tools/upstream-diff.sh v1.3.0            # diff BASE..v1.3.0
#   BASE=v1.2.5 tools/upstream-diff.sh v1.3.0
set -euo pipefail

BASE="${BASE:-v1.2.5}"
TARGET="${1:?usage: tools/upstream-diff.sh <spec-kit tag, e.g. v1.3.0>}"
FILES=(
  templates/commands/constitution.md templates/commands/specify.md templates/commands/clarify.md
  templates/commands/plan.md templates/commands/tasks.md templates/commands/analyze.md
  templates/commands/implement.md templates/commands/checklist.md templates/commands/converge.md
  templates/constitution-template.md templates/spec-template.md templates/plan-template.md
  templates/tasks-template.md
)

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
for ref in "$BASE" "$TARGET"; do
  mkdir -p "$tmp/$ref"
  curl -fsSL "https://github.com/github/spec-kit/archive/refs/tags/$ref.tar.gz" | tar -xz -C "$tmp/$ref" --strip-components=1
done

changed=0
for f in "${FILES[@]}"; do
  if ! diff -u --label "$BASE/$f" --label "$TARGET/$f" "$tmp/$BASE/$f" "$tmp/$TARGET/$f"; then
    changed=$((changed + 1))
  fi
done
echo "# $changed of ${#FILES[@]} upstream files changed between $BASE and $TARGET" >&2
