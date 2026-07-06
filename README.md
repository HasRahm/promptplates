# promptplates

**A four-agent coding pipeline for Claude Code — plan, build with evidence, adversarially
review, independently verify — that refuses to call anything "done" without a command that
proves it.**

Most agent setups take the model's word for it. It says "tests pass" and you believe it.
promptplates is built on the opposite bet: every claim of completion has to survive a command
that was actually run, and the reviewer trusts the evidence, not the author. Four slash
commands, all Markdown, no telemetry, no lock-in.

```
/pp-plan    → turns a task into ≤10 concrete steps ending in a VERIFY command
/pp-build   → implements them, running the proof command after each claim (records evidence
              via provenclaim when present)
/pp-review  → diffs against base, finds real bugs with a false-positive gate, ends in a VERDICT
/pp-verify  → re-runs the proof independently, flags stale/unproven claims, ends in PASS/FAIL
```

## Install — 30 seconds

Paste this into Claude Code:

> Install promptplates: run `git clone --depth 1 https://github.com/HasRahm/promptplates ~/.claude/skills/promptplates`. Then I can use /pp-plan, /pp-build, /pp-review, and /pp-verify.

That's it. The four skills are now available. Optionally `pip install
git+https://github.com/HasRahm/provenclaim` to turn on evidence recording (the pipeline works
without it — it just leans on live command output instead of a ledger).

## Use it

```
/pp-plan add rate limiting to the POST /login endpoint
/pp-build            # implements the plan, proving each step
/pp-review           # adversarial pass on the diff → VERDICT: APPROVE | REVISE
/pp-verify           # independent re-run → PASS | FAIL
```

Each skill runs a small bash **preamble** first that reads real repo state — current branch,
diff stat vs. base, detected test runner, whether a plan file or `.provenclaim/` ledger exists —
so its behavior is grounded in your actual repo, not assumptions. Then it walks numbered steps
with a defined output format. `/pp-review`'s signature move is a **pre-emit verification gate**:
before it claims "X doesn't exist," it re-reads the file — killing the most common class of
review false positive.

## Why it holds up: the prompt library underneath

The four skills are built on a library of composable system-prompt **modules** (`modules/`),
each written to the anatomy that production frontier-model prompts actually use — not just
rules, but the four things that make rules *stick*:

- **RULES** — numeric limits and ordered checklists, never adverbs ("under 15 words", not "be brief")
- **WHY** — the rationale, because models comply better when they know the reason
- **EXAMPLES** — worked good/bad pairs (a bad example teaches more than three rules)
- **EXPECTED + SELF-CHECK** — what correct output looks like, and a runtime checklist to hit it

Assemble any agent's full system prompt from them:

```bash
python build_prompt.py --role reviewer --set agent_name=MyBot --set host_surface="a CI rig"
python build_prompt.py --role mechanical --exclude 30,40   # headless agent: drop human-interaction modules
python build_prompt.py --list                              # modules, roles, skills
```

The design rationale — the nine patterns distilled from studying a production system prompt —
lives in [modules/ARCHITECTURE.md](modules/ARCHITECTURE.md).

## Composes with

- [relaycrew](https://github.com/HasRahm/relaycrew) — run these same roles across *different
  vendors'* CLIs (Claude builds, Codex reviews).
- [provenclaim](https://github.com/HasRahm/provenclaim) — the evidence ledger `/pp-build` and
  `/pp-verify` record to and check against.

## Scope (honest)

No telemetry, no auto-update, no phone-home — by design; these run entirely local off Markdown +
a zero-dependency assembler. Not included: specialist sub-agent fan-out and cross-model review
(that's relaycrew's job), and any hosted service. Apache-2.0.
