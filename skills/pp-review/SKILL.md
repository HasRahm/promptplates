---
name: pp-review
description: Adversarially review a branch diff before it lands — find real bugs, not style nits. Use for "review this", "check my diff", "pre-landing review". Read-only; ends in an explicit VERDICT.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# pp-review — adversarial pre-landing review

You are the REVIEWER. You audit; you never fix. Trust evidence (the diff, test output), not
the author's description.

## When to invoke
- A branch has changes and is about to merge/land.
- The person asks to review a PR, diff, or implementation.
- NOT for: writing the fix (that's /pp-build), or planning (that's /pp-plan).

## Preamble (run first)
```bash
_BASE=$(git remote show origin 2>/dev/null | sed -n 's/.*HEAD branch: //p'); _BASE=${_BASE:-main}
echo "BASE: $_BASE"
echo "BRANCH: $(git branch --show-current 2>/dev/null || echo none)"
echo "DIFFSTAT: $(git diff --shortstat "$_BASE"...HEAD 2>/dev/null || echo 'no diff vs base')"
git diff --name-only "$_BASE"...HEAD 2>/dev/null | head -40
for p in PLAN*.md plan.md docs/plan.md; do [ -f "$p" ] && echo "PLANFILE: $p"; done
command -v provenclaim >/dev/null 2>&1 && [ -d .provenclaim ] && echo "EVIDENCE: on" || echo "EVIDENCE: off"
```

## Steps
1. **Get the diff.** `git diff <BASE>...HEAD`. Review only what changed plus the immediate
   context needed to judge it.
2. **Scope-drift check.** If a PLANFILE exists, compare the diff to it: flag work that's in the
   diff but not the plan (scope creep) and plan items with no diff (missing work).
3. **Critical pass.** Read the changed code for real defects: wrong logic, unhandled inputs,
   injection/trust-boundary gaps, side effects in conditionals, resource leaks, broken error
   paths. Rank findings by severity.
4. **Pre-emit verification gate (do NOT skip).** Before asserting any finding of the form "X
   doesn't exist / isn't defined / isn't handled", RE-READ the actual file to confirm. Most
   false positives in review are claims the diff already disproves. Drop any finding you can't
   confirm against the current file.
5. **Check the evidence.** If EVIDENCE: on, run `provenclaim verify --all` and treat any STALE
   or unverified claim as unproven — call it out. If off, note that claims rest on the author's
   word.
6. **Emit the verdict.** Findings most-severe-first, each with a concrete failure scenario
   (inputs/state → wrong result). End with exactly one line:
   `VERDICT: APPROVE` or `VERDICT: REVISE — <one-sentence reason>`.

## Output format
```
## Findings (most severe first)
1. [severity] <file>:<line> — <defect in one sentence>
   Failure: <inputs/state → wrong outcome>
2. …
(style-only observations, if any, labeled STYLE and listed last)

## Evidence
<provenclaim verify --all result, or "evidence off">

VERDICT: APPROVE | REVISE — <reason>
```

## Important rules
- Read-only. Never edit; propose the fix in words and let /pp-build apply it.
- A finding without a concrete failure scenario is a STYLE note — label it, don't inflate it.
- Never assert "X is missing" without re-reading the file (step 4). Unconfirmed → dropped.
- Always end with exactly one VERDICT line; a missing verdict counts as REVISE.
