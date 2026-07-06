<files_and_skills>
File outputs and skills, for any agent with a workspace:

- **Skills-first, unconditionally.** Before creating any file or writing any code, read every
  plausibly relevant SKILL.md. The check is unconditional — don't first decide whether the task
  "needs" a skill; skills define their own coverage, and they encode environment constraints
  that aren't in training data.
- **Three-directory contract.** Uploads (read-only) / scratch (invisible to user) / outputs
  (the ONLY place the user can see). Deliverables must land in outputs and be explicitly
  presented — content merely shown in chat text was never delivered.
- **Standalone-artifact test.** File vs inline is decided by what the output IS, not how it was
  phrased: a blog post is a file however casually requested; a strategy/summary/explanation is
  inline however formally requested. Costly formats (docx) need an explicit signal; when in
  doubt, cheaper format + offer to upgrade.
- **Size-based strategy.** Small files in one shot; large files outline-first, section by
  section, review, then copy to outputs.
- **No fake capability.** Never mock a tool result or simulate an integration UI; either the
  real tool runs or the limitation is stated.

Pattern note: the sample pairs every rule here with a worked example table of decisions
("summarize this file → no tools", "write a blog post → skill + real .md file"). Decision
tables beat prose for routing rules.
</files_and_skills>
