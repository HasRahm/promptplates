# prompts/ — modular system-prompt library

Distilled from studying a production-scale frontier-model system prompt (~30k tokens). Not a
copy — each module rewrites the underlying *pattern* generically. Assemble by concatenating the
numbered files in order; drop any module the deployment doesn't need (a headless pipeline agent
doesn't need 30-wellbeing).

## Architecture lessons the sample teaches

1. **Order = priority.** Hard safety rules come before capabilities; capabilities before style.
   Later sections can never relax earlier ones, and the prompt says so explicitly ("reminders
   will never reduce restrictions").
2. **One concern per tagged block.** Every section is a named XML-ish container
   (`<refusal_handling>`, `<memory_system>`, …). This makes sections greppable, testable, and
   independently swappable — exactly the property these split files reproduce.
3. **Rules + counterexamples.** Every behavioral rule that models get wrong ships with paired
   good/bad examples (memory application, copyright, preferences). Examples carry more weight
   than adjectives.
4. **Decision checklists, not vibes.** Tool routing is a numbered walk ("Step 0: does this need
   a visual at all? … stop at first match"). Anywhere your agent picks between tools, write a
   checklist with an explicit stop rule.
5. **Negative-phrase lists for tone bugs.** The memory section literally bans specific phrases
   ("I can see…", "Based on your data…"). When a model has a verbal tic, ban the exact strings.
6. **Hard limits are numeric.** "15+ words is a violation", "ONE quote per source", "max 3 tool
   calls for medium tasks". Numbers survive paraphrase drift; "be brief" doesn't.
7. **Injected-reminder channel.** The prompt reserves a named channel for runtime nudges
   (long_conversation_reminder) and pre-declares that injected content claiming authority but
   *reducing* restrictions is fake. Your equivalent: whatever reminder channel your harness injects.
8. **Anti-injection posture.** Untrusted data (memories, tool results, user-appended tags) is
   explicitly marked as data-not-instructions. Repeated near every ingestion surface.
9. **Budget awareness.** The prompt opens with a token budget and repeatedly trades detail for
   cost (skills read on demand, deferred tools loaded by search). Prompt text is inventory, not
   free.

## Module map

| file | concern | sample-prompt ancestor |
|---|---|---|
| 00-identity.md | who/where/when the agent is | preamble, product_information |
| 10-safety.md | refusal rules, hard lines | refusal_handling, harmful_content |
| 20-tone.md | formatting, lists, brevity | tone_and_formatting |
| 30-wellbeing.md | user-wellbeing guardrails | user_wellbeing |
| 40-evenhandedness.md | contested topics | evenhandedness |
| 50-memory.md | applying persistent memory | memory_system (incl. forbidden phrases) |
| 60-tool-routing.md | which tool, when, how many calls | search_instructions, request_evaluation_checklist |
| 70-content-limits.md | quoting/reproduction limits | copyright compliance |
| 80-files-skills.md | file outputs, skills-first rule | computer_use, file_creation_advice |
| 90-runtime-reminders.md | injected-reminder contract | anthropic_reminders, safety_reminders |

Assembly: identity → safety → wellbeing → evenhandedness → tone → memory → tool routing →
content limits → files/skills → runtime reminders. Safety before capability, capability before
style; the last module re-anchors precedence.
