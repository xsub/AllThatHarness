#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
TARGET=""
PLUGIN=""
APPLY=0
DRY_RUN=0
BACKUP=0

usage() {
  cat <<'EOF'
Usage:
  install-harness.sh --target /path/to/repo --plugin python-pyqt5-business-mis-erp --dry-run
  install-harness.sh --target /path/to/repo --plugin python-pyqt5-business-mis-erp --apply --backup-existing
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --target) TARGET="${2:-}"; shift 2 ;;
    --plugin) PLUGIN="${2:-}"; shift 2 ;;
    --apply) APPLY=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    --backup-existing) BACKUP=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 2 ;;
  esac
done

[ -n "$TARGET" ] || { echo "--target required" >&2; exit 2; }
[ -d "$TARGET" ] || { echo "target directory does not exist: $TARGET" >&2; exit 2; }
[ -n "$PLUGIN" ] || PLUGIN="python-pyqt5-business-mis-erp"
[ -d "$ROOT/target-plugins/$PLUGIN" ] || { echo "plugin not found: $PLUGIN" >&2; exit 2; }
[ "$APPLY" -eq 1 ] || [ "$DRY_RUN" -eq 1 ] || { echo "choose --dry-run or --apply" >&2; exit 2; }

STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="$TARGET/.claude-harness-backups/$STAMP"

say() { printf '%s\n' "$*"; }
run() {
  if [ "$DRY_RUN" -eq 1 ]; then
    say "DRY: $*"
  else
    "$@"
  fi
}

backup_existing() {
  local dest="$1"
  if [ -e "$dest" ] && [ "$BACKUP" -eq 1 ]; then
    local rel="${dest#$TARGET/}"
    run mkdir -p "$BACKUP_DIR/$(dirname "$rel")"
    run cp -a "$dest" "$BACKUP_DIR/$rel"
  fi
}

copy_no_clobber() {
  local src="$1"
  local dest="$2"
  if [ -e "$dest" ]; then
    if cmp -s "$src" "$dest"; then
      say "SKIP same: ${dest#$TARGET/}"
      return 0
    fi
    if [ "$BACKUP" -eq 1 ]; then
      backup_existing "$dest"
      say "KEEP existing, wrote example instead: ${dest#$TARGET/}"
      local example="$dest.harness-example"
      run mkdir -p "$(dirname "$example")"
      run cp "$src" "$example"
    else
      say "CONFLICT keep existing: ${dest#$TARGET/} (use --backup-existing to write .harness-example)"
    fi
    return 0
  fi
  say "COPY ${src#$ROOT/} -> ${dest#$TARGET/}"
  run mkdir -p "$(dirname "$dest")"
  run cp "$src" "$dest"
}

copy_dir_no_clobber() {
  local src_dir="$1"
  local dest_dir="$2"
  find "$src_dir" -type f | while read -r src; do
    local rel="${src#$src_dir/}"
    copy_no_clobber "$src" "$dest_dir/$rel"
  done
}

append_block_once() {
  local file="$1"
  local marker="$2"
  local block="$3"
  if [ -f "$file" ] && grep -q "$marker" "$file"; then
    say "SKIP block already present: ${file#$TARGET/}"
    return 0
  fi
  backup_existing "$file"
  say "APPEND block to ${file#$TARGET/}"
  if [ "$DRY_RUN" -eq 0 ]; then
    mkdir -p "$(dirname "$file")"
    {
      [ -f "$file" ] && printf '\n'
      printf '%s\n' "$block"
    } >> "$file"
  fi
}

copy_dir_no_clobber "$ROOT/.claude/skills" "$TARGET/.claude/skills"
copy_dir_no_clobber "$ROOT/.claude/hooks" "$TARGET/.claude/hooks"
copy_no_clobber "$ROOT/.claude/settings.example.json" "$TARGET/.claude/settings.harness.example.json"
copy_no_clobber "$ROOT/.claude/verify.toml" "$TARGET/.claude/verify.toml"
copy_no_clobber "$ROOT/.claude/gitignore-snippet" "$TARGET/.claude/gitignore-snippet"
copy_dir_no_clobber "$ROOT/scripts" "$TARGET/scripts/claude-harness"
copy_dir_no_clobber "$ROOT/memory" "$TARGET/memory"
copy_dir_no_clobber "$ROOT/docs" "$TARGET/docs/claude-harness"
copy_dir_no_clobber "$ROOT/target-plugins/$PLUGIN" "$TARGET/target-plugins/$PLUGIN"
copy_dir_no_clobber "$ROOT/target-plugins/$PLUGIN/skills" "$TARGET/.claude/skills"

say "WRITE active target plugin: $PLUGIN"
if [ "$DRY_RUN" -eq 0 ]; then
  mkdir -p "$TARGET/.claude"
  printf '%s\n' "$PLUGIN" > "$TARGET/.claude/active-target-plugin"
fi

CLAUDE_BLOCK='<!-- claude-harness:start -->
## Claude Engineering Harness

Read `memory/MEMORY.md`, `memory/active-plan.md`, `CONTEXT.md`, and the active target plugin before code changes.

Active target plugin is stored in `.claude/active-target-plugin`.

Use `karpathy-guidelines` as core coding behavior: think before coding, choose the simplest sufficient solution, make surgical changes, and define verifiable success criteria.

Use one semantic change at a time. Verify the exact diff with `python3 scripts/claude-harness/verify.py --profile <profile>` before final response. Authorize push only after verification with `python3 scripts/claude-harness/authorize-push.py`.
<!-- claude-harness:end -->'
append_block_once "$TARGET/CLAUDE.md" "claude-harness:start" "$CLAUDE_BLOCK"

GITIGNORE_BLOCK='# claude-harness:start
.claude/state/
# claude-harness:end'
append_block_once "$TARGET/.gitignore" "claude-harness:start" "$GITIGNORE_BLOCK"

say "Done. Review .claude/settings.harness.example.json and merge into .claude/settings.json manually."
