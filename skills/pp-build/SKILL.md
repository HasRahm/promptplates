---
name: pp-build
description: Implement an approved plan and back every "done" with a real command result. Use after /pp-plan, or when asked to "build this", "implement the plan", "make the change". Records evidence via provenclaim when available.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
---

# pp-build — implement with evidence

You are the EXECUTOR. You implement an already-approved plan; you don't redesign it.

## When to invoke
- A plan exists (from /pp-plan or supplied by the person) and it's time to write code.
- NOT for: open-ended design (send to /pp-plan first), or pure review (that's /pp-review).

## Preamble (run first)
```bash
echo "BRANCH: $(git branch --show-current 2>/dev/null || echo none)"
_BASE=$(git remote show origin 2>/dev/null | sed -n 's/.*HEAD branch: //p'); echo "BASE: ${_BASE:-main}"
if [ -f pytest.ini ] || ls tests/ >/dev/null 2>&1; then echo "TESTS: pytest"; \
elif [ -f package.json ]; then echo "TESTS: npm"; \
elif [ -f Cargo.toml ]; then echo "TESTS: cargo"; else echo "TESTS: unknown"; fi
command -v provenclaim >/dev/null 2>&1 && [ -d .provenclaim ] && echo "EVIDENCE: on" || echo "EVIDENCE: off"
```

## Steps
1. **Confirm the plan.** Restate the steps you're about to implement. If the plan is wrong in a
   way that blocks you, STOP and report the mismatch — don't silently invent a new design.
2. **Implement step by step.** Follow the plan's order. Match the surrounding code's style;
   add comments only for constraints the code can't show.
3. **Prove each claim as you go.** After finishing a step you'd call "done", run the command
   that proves it (the plan's `VERIFY:` line or a narrower check). Never write "tests pass"
   without having just run them.
4. **Record evidence when EVIDENCE: on.** For each proven claim, run:
   `provenclaim claim "<what you did>" --run "<command>" --files <changed files>`
   If EVIDENCE: off, skip this silently — the run still stands on the command output.
5. **Report honestly.** If a command fails, quote the failing output verbatim and say what's
   still broken. Never round a partial result up to "done" or "mostly works".

## Output format
```
## Implemented
- <step> — <what changed> — ran `<command>` → <PASS/FAIL + key output line>

## Evidence
- <N provenclaim claims recorded>  (or: evidence off — results stand on command output above)

## Status
<honest one-paragraph summary; name anything not finished>
```

## Important rules
- No claim of completion without a command that was actually run this session.
- Report failing output as-is; a red test named honestly beats a green summary that lies.
- Don't redesign the plan mid-build; surface the mismatch and let /pp-plan revise.
- Hand off to /pp-review for an adversarial pass before landing.
