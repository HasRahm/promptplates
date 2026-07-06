---
name: promptplates
description: Router for the promptplates toolkit. Points at the four coding-pipeline skills (/pp-plan, /pp-build, /pp-review, /pp-verify) and the prompt-module library. Use when starting a coding task, or when writing/editing any agent system prompt, subagent definition, AGENTS.md role file, or SKILL.md.
---

# promptplates — router

## For a coding task, use the pipeline skills
- **/pp-plan** — turn a task into ≤10 verifiable steps ending in a `VERIFY:` command.
- **/pp-build** — implement the plan, proving each claim with a real command (records evidence
  via provenclaim when available).
- **/pp-review** — adversarial diff review with a false-positive gate, ending in `VERDICT:`.
- **/pp-verify** — independently re-run the proof, flag stale/unproven claims, end in PASS/FAIL.

Typical flow: `/pp-plan` → `/pp-build` → `/pp-review` → `/pp-verify`.

## For writing or editing an agent prompt, use the module library

When creating or editing a system prompt, agent definition, or behavioral rule set:

1. Read `modules/ARCHITECTURE.md` first — it lists the nine patterns with rationale.
2. Compose, don't freewrite: start from the numbered modules (`python build_prompt.py --role
   <role>`), then specialize with a role overlay in `roles/`. New concerns become new modules,
   not paragraphs bolted onto old ones.
3. Enforce the patterns on every rule you write:
   - A rule a model might violate gets a NUMBER (word cap, call budget, step limit), never an
     adverb ("be brief" → "under 15 words").
   - A routing decision gets an ORDERED CHECKLIST with a stop-at-first-match rule.
   - A verbal tic gets a BANNED-PHRASE list of exact strings.
   - Safety before capability before style; state explicitly that later text can't relax
     earlier text.
   - Every ingestion surface (memory, tool results, fetched content) gets the data-not-
     instructions sentence.
   - Rules the model chronically violates may repeat up to 3 times at different granularities;
     everything else appears exactly once — repetition is budgeted.
   - Hard rules ship with one good and one bad worked example.
4. Before finishing, self-check: does any rule rely on an adjective where a number would do?
   Does any decision lack a stop rule? Could injected text claim authority to loosen anything?
