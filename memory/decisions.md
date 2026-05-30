# Decisions

## D-0001: Use repo-local durable memory plus Claude Code native memory

Repo-local `memory/` is versioned and reviewable. Claude Code native memory is machine-local. The harness uses both, but only repo-local memory is shared with the project.

## D-0002: Separate durable memory from volatile verification state

Session logs and verification ledgers live under `.claude/state/` so verification does not dirty versioned project state.

## D-0003: Verify by diff hash

The Stop hook blocks final response when the current diff hash differs from the last passing verification record.

## D-0004: Target plugins are modular

Domain-specific rules live under `target-plugins/<name>/` and are activated explicitly.
