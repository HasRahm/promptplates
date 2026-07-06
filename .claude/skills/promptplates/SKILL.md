---
name: promptplates
description: Use when writing or editing ANY agent system prompt, subagent definition, agents.md/AGENTS.md role file, or SKILL.md behavioral rules. Applies the nine frontier-lab prompt-engineering patterns (numeric limits, ordered checklists, banned-phrase lists, priority ordering, injection defenses) and the module library in this repo.
---

# promptplates — write agent prompts like frontier labs do

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
