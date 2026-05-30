#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
INSTALLER="$ROOT/scripts/install-harness.sh"
PLUGIN="python-pyqt5-business-mis-erp"
TMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/allthat-harness-installer.XXXXXX")"

trap 'rm -rf "$TMP_ROOT"' EXIT

fail() {
  printf 'FAIL %s\n' "$*" >&2
  exit 1
}

assert_file() {
  [ -f "$1" ] || fail "expected file: $1"
}

assert_no_path() {
  [ ! -e "$1" ] || fail "expected no path: $1"
}

assert_contains() {
  grep -Fq -- "$2" "$1" || fail "expected $1 to contain: $2"
}

assert_exact() {
  local actual
  actual="$(cat "$1")"
  [ "$actual" = "$2" ] || fail "expected $1 to equal '$2', got '$actual'"
}

assert_marker_once() {
  local count
  count="$(grep -c 'claude-harness:start' "$1")"
  [ "$count" = "1" ] || fail "expected one marker in $1, got $count"
}

empty_target="$TMP_ROOT/empty"
mkdir -p "$empty_target"
"$INSTALLER" --target "$empty_target" --plugin "$PLUGIN" --dry-run > "$TMP_ROOT/empty-dry.out"
assert_contains "$TMP_ROOT/empty-dry.out" "Dry run only; no files were written."
assert_no_path "$empty_target/.claude"

"$INSTALLER" --target "$empty_target" --plugin "$PLUGIN" --apply > "$TMP_ROOT/empty-apply.out"
assert_file "$empty_target/.claude/skills/karpathy-guidelines/SKILL.md"
assert_file "$empty_target/scripts/claude-harness/verify.py"
assert_file "$empty_target/.claude/active-target-plugin"
assert_exact "$empty_target/.claude/active-target-plugin" "$PLUGIN"
assert_contains "$empty_target/CLAUDE.md" "claude-harness:start"
assert_contains "$empty_target/.gitignore" "claude-harness:start"

"$INSTALLER" --target "$empty_target" --plugin "$PLUGIN" --apply > "$TMP_ROOT/empty-rerun.out"
assert_marker_once "$empty_target/CLAUDE.md"
assert_marker_once "$empty_target/.gitignore"

conflict_target="$TMP_ROOT/conflict"
mkdir -p "$conflict_target/.claude/skills/karpathy-guidelines"
printf 'custom skill\n' > "$conflict_target/.claude/skills/karpathy-guidelines/SKILL.md"

if "$INSTALLER" --target "$conflict_target" --plugin "$PLUGIN" --dry-run > "$TMP_ROOT/conflict-dry.out" 2>&1; then
  fail "expected dry-run with default conflict policy to fail"
fi
assert_contains "$TMP_ROOT/conflict-dry.out" "No files were written because conflicts were found."
assert_contains "$TMP_ROOT/conflict-dry.out" "--apply --conflicts numbered"
assert_exact "$conflict_target/.claude/skills/karpathy-guidelines/SKILL.md" "custom skill"
assert_no_path "$conflict_target/.claude/hooks"

if "$INSTALLER" --target "$conflict_target" --plugin "$PLUGIN" --apply --conflicts abort > "$TMP_ROOT/conflict-apply.out" 2>&1; then
  fail "expected apply with abort conflict policy to fail"
fi
assert_exact "$conflict_target/.claude/skills/karpathy-guidelines/SKILL.md" "custom skill"
assert_no_path "$conflict_target/.claude/hooks"

numbered_target="$TMP_ROOT/numbered"
mkdir -p "$numbered_target/.claude/skills/karpathy-guidelines" "$numbered_target/.claude"
printf 'custom skill\n' > "$numbered_target/.claude/skills/karpathy-guidelines/SKILL.md"
printf 'other-plugin\n' > "$numbered_target/.claude/active-target-plugin"
printf 'reserved\n' > "$numbered_target/.claude/active-target-plugin.harness-1"

"$INSTALLER" --target "$numbered_target" --plugin "$PLUGIN" --apply --conflicts numbered > "$TMP_ROOT/numbered-apply.out"
assert_exact "$numbered_target/.claude/skills/karpathy-guidelines/SKILL.md" "custom skill"
assert_file "$numbered_target/.claude/skills/karpathy-guidelines/SKILL.md.harness-1"
assert_contains "$numbered_target/.claude/skills/karpathy-guidelines/SKILL.md.harness-1" "name: karpathy-guidelines"
assert_exact "$numbered_target/.claude/active-target-plugin" "other-plugin"
assert_exact "$numbered_target/.claude/active-target-plugin.harness-2" "$PLUGIN"
assert_contains "$TMP_ROOT/numbered-apply.out" "Manual follow-up"

printf 'PASS install-harness temp-target tests\n'
