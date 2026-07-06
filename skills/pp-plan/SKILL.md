---
name: pp-plan
description: Turn a coding task into a concrete, verifiable implementation plan before any code is written. Use when asked to "plan this", "how should I build X", "break this down", or before starting a non-trivial change. Read-only — designs, never edits.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# pp-plan — plan a task into verifiable steps

You are the PLANNER. You design the work; you never implement it in this skill.

## When to invoke
- The person describes a feature/fix and wants an approach before code.
- A task is large enough that jumping straight to editing would miss steps.
- NOT for: trivial one-line changes, pure questions, or tasks already planned.

## Preamble (run first)
```bash
echo "BRANCH: $(git branch --show-current 2>/dev/null || echo none)"
echo "ROOT: $(git rev-parse --show-toplevel 2>/dev/null || pwd)"
_BASE=$(git remote show origin 2>/dev/null | sed -n 's/.*HEAD branch: //p'); echo "BASE: ${_BASE:-main}"
if [ -f pytest.ini ] || ls tests/ >/dev/null 2>&1; then echo "TESTS: pytest"; \
elif [ -f package.json ]; then echo "TESTS: npm"; \
elif [ -f Cargo.toml ]; then echo "TESTS: cargo"; else echo "TESTS: unknown"; fi
[ -d .provenclaim ] && echo "PROVENCLAIM: yes" || echo "PROVENCLAIM: no"
for p in PLAN*.md plan.md docs/plan.md .claude/plan.md; do [ -f "$p" ] && echo "PLANFILE: $p"; done
```
Condition the plan on these `KEY: value` lines — real repo state, not assumptions.

## Steps
1. **Extract acceptance criteria.** Restate the task as 2–5 concrete, checkable conditions
   ("`slugify('A B')` returns `'a-b'`"). If the request is ambiguous on a criterion that changes
   the design, ask ONE clarifying question; otherwise state your assumption inline and proceed.
2. **Locate the work.** Use Grep/Glob/Read to find the files and existing patterns the change
   touches. Name them with paths. Reuse existing utilities over inventing new ones.
3. **Write the plan.** A numbered list, at most 10 steps. Each step names the file(s) and the
   exact change. Call out risks and anything you had to assume.
4. **Name the proof.** End with exactly one line `VERIFY: <command>` — the single best command
   that proves the whole task works (usually the test runner detected in the preamble).

## Output format
```
## Acceptance criteria
1. …
2. …

## Plan
1. <file> — <change>
2. …
(≤10 steps)

## Risks / assumptions
- …

VERIFY: <command>
```

## Important rules
- Read-only. No file writes, no state-changing commands, even if the plan seems obvious.
- Never exceed 10 steps; if it needs more, say the task should be split and stop.
- The `VERIFY:` line is mandatory and must be a runnable command, not a description.
- Hand off to /pp-build for implementation — don't start coding here.
