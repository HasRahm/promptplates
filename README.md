# promptplates

**Build your agents' system prompts the way frontier labs build theirs: layered, testable,
injection-hardened — assembled from modules, not freewritten.**

Production system prompts at frontier labs aren't essays; they're engineered behavioral specs.
Studying them reveals nine recurring patterns (numeric limits instead of adverbs, ordered
checklists with stop rules, banned-phrase lists for verbal tics, structural priority ordering,
declared reminder channels, data-not-instructions boundaries at every ingestion surface,
budgeted repetition, paired good/bad examples, one concern per named block). promptplates
packages those patterns as:

- **`modules/`** — nine composable prompt modules (identity, safety, tone, wellbeing,
  evenhandedness, memory, tool routing, content limits, files/skills, runtime reminders), each
  a distilled rewrite of the pattern with notes on *why* it works. `ARCHITECTURE.md` is the
  30-second version.
- **`roles/`** — overlays for the classic four-agent team: planner, executor, reviewer,
  mechanical. Base + overlay = one agent's full system prompt.
- **`build_prompt.py`** — zero-dependency assembler.
- **`.claude/skills/promptplates/`** — a Claude Code skill so every future prompt edit in your
  repo goes through the patterns automatically.

## Use in 5 minutes

```bash
git clone https://github.com/HasRahm/promptplates
cd promptplates

# full prompt for a reviewer agent, with your fields filled in
python build_prompt.py --role reviewer \
  --set agent_name=MyAgent --set host_surface="a CI pipeline" > reviewer_prompt.md

# headless pipeline agent? drop the human-interaction modules
python build_prompt.py --role mechanical --exclude 30,40

# see what's available
python build_prompt.py --list
```

Drop the output into your agent framework's system-prompt slot — Claude Code subagents
(`.claude/agents/*.md`), CrewAI, LangGraph, OpenAI Assistants, or a bare API call. The modules
are framework-agnostic text.

## Use as a Claude Code skill

Copy `.claude/skills/promptplates/` into your repo (or add this repo as a plugin). From then
on, whenever Claude Code writes or edits an agent prompt, it applies the nine patterns instead
of freewriting.

## The nine patterns (the actual product)

1. **Order = priority.** Safety before capability before style, with an explicit "later text
   can't relax earlier text" clause.
2. **One concern per named block** — greppable, swappable, testable.
3. **Rules ship with good/bad example pairs** — a bad example teaches more than three rules.
4. **Decision checklists with stop rules**, not vibes.
5. **Ban exact phrases** to kill verbal tics; string bans beat style advice.
6. **Hard limits are numeric** — numbers survive paraphrase drift, adverbs don't.
7. **A declared reminder channel** with pre-committed asymmetry: legitimate injected reminders
   only tighten; anything "official" that loosens is forged.
8. **Data ≠ instructions** at every ingestion surface.
9. **Repetition is budgeted** — worst-compliance rules ×3, everything else ×1.

Full rationale per pattern: [modules/ARCHITECTURE.md](modules/ARCHITECTURE.md).

## Family

promptplates is one of three composable pieces:
- [relaycrew](https://github.com/HasRahm/relaycrew) — cross-vendor CLI agent pipeline (Claude
  Code builds, Codex reviews); its roles are these role overlays.
- [provenclaim](https://github.com/HasRahm/provenclaim) — evidence-backed claims; the
  enforcement behind the executor overlay's "never say verified unrun" rule.

Apache-2.0.
