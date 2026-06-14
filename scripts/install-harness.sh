#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
TARGET=""
PLUGIN=""
APPLY=0
DRY_RUN=0
CONFLICTS="abort"

CLAUDE_BLOCK='<!-- claude-harness:start -->
## Claude Engineering Harness

Read `memory/MEMORY.md`, `memory/active-plan.md`, `CONTEXT.md`, and the active target plugin before code changes.

Active target plugin is stored in `.claude/active-target-plugin`.

Use `karpathy-guidelines` as core coding behavior: think before coding, choose the simplest sufficient solution, make surgical changes, and define verifiable success criteria.

Use one semantic change at a time. Verify the exact diff with `python3 scripts/claude-harness/verify.py --profile <profile>` before final response. Authorize push only after verification with `python3 scripts/claude-harness/authorize-push.py`.
<!-- claude-harness:end -->'

GITIGNORE_BLOCK='# claude-harness:start
.claude/state/
__pycache__/
*.pyc
*.pyo
# claude-harness:end'

usage() {
  cat <<'EOF'
Usage:
  install-harness.sh --target /path/to/repo [--plugin generic] --dry-run [--conflicts abort|numbered]
  install-harness.sh --target /path/to/repo [--plugin generic] --apply [--conflicts abort|numbered]

Conflict modes:
  abort     Stop before writing anything when an existing different file is found. Default.
  numbered  Keep existing files and write harness files beside them as path.harness-1, path.harness-2, ...

Deprecated:
  --backup-existing is accepted as an alias for --conflicts numbered.
EOF
}

say() { printf '%s\n' "$*"; }

quote_arg() {
  printf '%q' "$1"
}

target_rel() {
  case "$1" in
    "$TARGET"/*) printf '%s' "${1#$TARGET/}" ;;
    *) printf '%s' "$1" ;;
  esac
}

root_rel() {
  case "$1" in
    "$ROOT"/*) printf '%s' "${1#$ROOT/}" ;;
    *) printf '%s' "$1" ;;
  esac
}

while [ $# -gt 0 ]; do
  case "$1" in
    --target) TARGET="${2:-}"; shift 2 ;;
    --plugin) PLUGIN="${2:-}"; shift 2 ;;
    --apply) APPLY=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    --conflicts) CONFLICTS="${2:-}"; shift 2 ;;
    --backup-existing)
      say "WARN --backup-existing is deprecated; using --conflicts numbered"
      CONFLICTS="numbered"
      shift
      ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 2 ;;
  esac
done

[ -n "$TARGET" ] || { echo "--target required" >&2; exit 2; }
[ -d "$TARGET" ] || { echo "target directory does not exist: $TARGET" >&2; exit 2; }
[ -n "$PLUGIN" ] || PLUGIN="generic"
[ -d "$ROOT/target-plugins/$PLUGIN" ] || { echo "plugin not found: $PLUGIN" >&2; exit 2; }
[ "$APPLY" -ne "$DRY_RUN" ] || { echo "choose exactly one of --dry-run or --apply" >&2; exit 2; }
case "$CONFLICTS" in
  abort|numbered) ;;
  *) echo "--conflicts must be abort or numbered" >&2; exit 2 ;;
esac

PLAN_KIND=()
PLAN_SRC=()
PLAN_DEST=()
PLAN_TEXT=()
PLAN_NOTE=()
CONFLICT_NOTES=()
MANUAL_NOTES=()

add_plan() {
  PLAN_KIND+=("$1")
  PLAN_SRC+=("$2")
  PLAN_DEST+=("$3")
  PLAN_TEXT+=("$4")
  PLAN_NOTE+=("$5")
}

add_conflict() {
  CONFLICT_NOTES+=("$1")
}

add_manual_note() {
  MANUAL_NOTES+=("$1")
}

planned_dest_exists() {
  local candidate="$1"
  local existing
  [ "${#PLAN_DEST[@]}" -gt 0 ] || return 1
  for existing in "${PLAN_DEST[@]}"; do
    [ "$existing" = "$candidate" ] && return 0
  done
  return 1
}

next_numbered_dest() {
  local dest="$1"
  local n=1
  local candidate
  while :; do
    candidate="$dest.harness-$n"
    if [ ! -e "$candidate" ] && ! planned_dest_exists "$candidate"; then
      printf '%s' "$candidate"
      return 0
    fi
    n=$((n + 1))
  done
}

record_existing_different() {
  local src="$1"
  local dest="$2"
  local src_label="$3"
  local numbered_dest
  local message
  message="CONFLICT keep existing: $(target_rel "$dest") differs from $src_label"
  add_conflict "$message"
  if [ "$CONFLICTS" = "numbered" ]; then
    numbered_dest="$(next_numbered_dest "$dest")"
    add_plan "copy" "$src" "$numbered_dest" "" "NUMBERED $src_label -> $(target_rel "$numbered_dest")"
  fi
}

record_copy() {
  local src="$1"
  local dest="$2"
  local src_label
  src_label="$(root_rel "$src")"
  if planned_dest_exists "$dest"; then
    record_existing_different "$src" "$dest" "$src_label"
    return 0
  fi
  if [ -e "$dest" ]; then
    if [ -f "$dest" ] && cmp -s "$src" "$dest"; then
      add_plan "skip" "$src" "$dest" "" "SKIP same: $(target_rel "$dest")"
      return 0
    fi
    record_existing_different "$src" "$dest" "$src_label"
    return 0
  fi
  add_plan "copy" "$src" "$dest" "" "COPY $src_label -> $(target_rel "$dest")"
}

record_copy_dir() {
  local src_dir="$1"
  local dest_dir="$2"
  local src
  local rel
  while IFS= read -r src; do
    rel="${src#$src_dir/}"
    record_copy "$src" "$dest_dir/$rel"
  done < <(
    find "$src_dir" -type f \
      ! -path '*/__pycache__/*' \
      ! -path '*/.pytest_cache/*' \
      ! -name '*.pyc' \
      ! -name '*.pyo' \
      ! -name '.DS_Store' \
      -print | LC_ALL=C sort
  )
}

record_text_file() {
  local dest="$1"
  local text="$2"
  local label="$3"
  local numbered_dest
  if [ -e "$dest" ]; then
    if [ -f "$dest" ] && printf '%s\n' "$text" | cmp -s - "$dest"; then
      add_plan "skip" "" "$dest" "" "SKIP same: $(target_rel "$dest")"
      return 0
    fi
    add_conflict "CONFLICT keep existing: $(target_rel "$dest") differs from $label"
    if [ "$CONFLICTS" = "numbered" ]; then
      numbered_dest="$(next_numbered_dest "$dest")"
      add_plan "write_text" "" "$numbered_dest" "$text" "NUMBERED $label -> $(target_rel "$numbered_dest")"
      add_manual_note "Review $(target_rel "$numbered_dest") and decide whether to replace $(target_rel "$dest")."
    fi
    return 0
  fi
  add_plan "write_text" "" "$dest" "$text" "WRITE $label: $(target_rel "$dest")"
}

record_append_block() {
  local dest="$1"
  local marker="$2"
  local block="$3"
  local label="$4"
  local numbered_dest
  if [ -e "$dest" ] && [ ! -f "$dest" ]; then
    add_conflict "CONFLICT cannot append $label because $(target_rel "$dest") is not a file"
    if [ "$CONFLICTS" = "numbered" ]; then
      numbered_dest="$(next_numbered_dest "$dest")"
      add_plan "write_text" "" "$numbered_dest" "$block" "NUMBERED $label block -> $(target_rel "$numbered_dest")"
      add_manual_note "Review $(target_rel "$numbered_dest") and decide how to merge it with $(target_rel "$dest")."
    fi
    return 0
  fi
  if [ -f "$dest" ] && grep -q "$marker" "$dest"; then
    add_plan "skip" "" "$dest" "" "SKIP block already present: $(target_rel "$dest")"
    return 0
  fi
  add_plan "append" "" "$dest" "$block" "APPEND $label block to $(target_rel "$dest")"
}

execute_plan() {
  local i
  local kind
  local src
  local dest
  local text
  for i in "${!PLAN_KIND[@]}"; do
    kind="${PLAN_KIND[$i]}"
    src="${PLAN_SRC[$i]}"
    dest="${PLAN_DEST[$i]}"
    text="${PLAN_TEXT[$i]}"
    case "$kind" in
      skip)
        ;;
      copy)
        mkdir -p "$(dirname "$dest")"
        cp "$src" "$dest"
        ;;
      write_text)
        mkdir -p "$(dirname "$dest")"
        printf '%s\n' "$text" > "$dest"
        ;;
      append)
        mkdir -p "$(dirname "$dest")"
        {
          [ -f "$dest" ] && printf '\n'
          printf '%s\n' "$text"
        } >> "$dest"
        ;;
      *)
        echo "internal error: unknown plan kind $kind" >&2
        return 2
        ;;
    esac
  done
}

print_plan() {
  local i
  local conflict_count="${#CONFLICT_NOTES[@]}"
  say "Preflight summary"
  say "  target: $TARGET"
  say "  plugin: $PLUGIN"
  say "  mode: $([ "$DRY_RUN" -eq 1 ] && printf dry-run || printf apply)"
  say "  conflicts: $CONFLICTS"
  say "  planned actions: ${#PLAN_KIND[@]}"
  say "  conflicts found: $conflict_count"
  say ""
  say "Planned actions:"
  for i in "${!PLAN_NOTE[@]}"; do
    say "  - ${PLAN_NOTE[$i]}"
  done
  if [ "$conflict_count" -gt 0 ]; then
    say ""
    say "Conflicts:"
    for i in "${!CONFLICT_NOTES[@]}"; do
      say "  - ${CONFLICT_NOTES[$i]}"
    done
  fi
  if [ "${#MANUAL_NOTES[@]}" -gt 0 ]; then
    say ""
    say "Manual follow-up:"
    for i in "${!MANUAL_NOTES[@]}"; do
      say "  - ${MANUAL_NOTES[$i]}"
    done
  fi
}

record_copy_dir "$ROOT/.claude/skills" "$TARGET/.claude/skills"
record_copy_dir "$ROOT/.claude/hooks" "$TARGET/.claude/hooks"
record_copy "$ROOT/.claude/settings.example.json" "$TARGET/.claude/settings.harness.example.json"
record_copy "$ROOT/.claude/verify.toml" "$TARGET/.claude/verify.toml"
record_copy "$ROOT/.claude/gitignore-snippet" "$TARGET/.claude/gitignore-snippet"
record_copy_dir "$ROOT/scripts" "$TARGET/scripts/claude-harness"
record_copy_dir "$ROOT/memory" "$TARGET/memory"
record_copy_dir "$ROOT/docs" "$TARGET/docs/claude-harness"
record_copy_dir "$ROOT/target-plugins/$PLUGIN" "$TARGET/target-plugins/$PLUGIN"
record_copy_dir "$ROOT/target-plugins/$PLUGIN/skills" "$TARGET/.claude/skills"
record_text_file "$TARGET/.claude/active-target-plugin" "$PLUGIN" "active target plugin"
record_append_block "$TARGET/CLAUDE.md" "claude-harness:start" "$CLAUDE_BLOCK" "CLAUDE.md"
record_append_block "$TARGET/.gitignore" "claude-harness:start" "$GITIGNORE_BLOCK" ".gitignore"

print_plan

if [ "${#CONFLICT_NOTES[@]}" -gt 0 ] && [ "$CONFLICTS" = "abort" ]; then
  say ""
  say "No files were written because conflicts were found."
  say "To continue by writing numbered harness files beside existing files, run:"
  say "  $0 --target $(quote_arg "$TARGET") --plugin $(quote_arg "$PLUGIN") --apply --conflicts numbered"
  exit 1
fi

if [ "$DRY_RUN" -eq 1 ]; then
  say ""
  say "Dry run only; no files were written."
  exit 0
fi

execute_plan
say ""
say "Done. Review .claude/settings.harness.example.json and merge into .claude/settings.json manually."
