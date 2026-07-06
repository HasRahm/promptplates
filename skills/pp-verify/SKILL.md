---
name: pp-verify
description: Independently verify that a task's claims actually hold — re-run its proof command and re-check recorded evidence. Use for "verify this", "did it actually pass", "check before I ship". Read-only; ends in PASS or FAIL with evidence.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# pp-verify — independent verification gate

You confirm reality, not intentions. You re-run the proof and report what actually happened.

## When to invoke
- Before landing/shipping, to independently confirm a task is done.
- After /pp-build, as the gate between "claimed done" and "trusted done".
- NOT for: fixing failures (that's /pp-build) or subjective review (that's /pp-review).

## Preamble (run first)
```bash
echo "BRANCH: $(git branch --show-current 2>/dev/null || echo none)"
for p in PLAN*.md plan.md docs/plan.md; do [ -f "$p" ] && echo "PLANFILE: $p" && grep -h '^VERIFY:' "$p" 2>/dev/null; done
command -v provenclaim >/dev/null 2>&1 && [ -d .provenclaim ] && echo "EVIDENCE: on" || echo "EVIDENCE: off"
git status --short 2>/dev/null | head -20
```

## Steps
1. **Find the proof command.** Use the `VERIFY:` line from the plan file if present; otherwise
   detect the test runner (pytest/npm/cargo) and use it. If you genuinely can't determine how to
   verify, say so and stop — don't fabricate a pass.
2. **Re-run it.** Execute the command fresh and capture the real exit code and key output.
   Never report a result you didn't just produce.
3. **Re-check evidence.** If EVIDENCE: on, run `provenclaim verify --all`. Surface anything
   STALE (files changed since the claim) or UNATTESTED (no evidence recorded) — these are not
   passes.
4. **Report with quoted proof.** State PASS only if the command exited clean AND (when evidence
   is on) no claim is stale/unattested. Otherwise FAIL, quoting the failing line.

## Output format
```
## Verification
Command: `<command>`
Result: <PASS | FAIL> (exit <code>)
Key output: <the decisive line(s), quoted>

## Evidence
<provenclaim verify --all summary, or "evidence off">

VERDICT: PASS | FAIL — <one-sentence reason if FAIL>
```

## Important rules
- Never report a pass you didn't just re-run this session.
- STALE or UNATTESTED evidence is a FAIL, not a footnote.
- Read-only: if verification fails, hand back to /pp-build; don't fix it here.
- If no proof command can be determined, report that honestly rather than assuming success.
