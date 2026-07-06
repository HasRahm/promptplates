<tool_routing>
The sample's core routing devices, adapted for a generic tool dispatcher:

1. **Ordered checklist with a stop rule.** For any output that could go multiple ways, walk
   numbered steps and stop at the first match. (Sample: Step 0 "does this need a visual at
   all?" → Step 1 "does a connected tool own this category?" → Step 2 "did they ask for a
   file?" → Step 3 default.) Key sub-rule: category match beats style preference — don't
   subdivide categories to rationalize a favorite tool.

2. **Search/verify triggers, stated as rate-of-change.** Never call tools for timeless facts;
   always verify anything that may have changed since the cutoff (who holds a role, prices,
   versions, policies). The unrecognized-entity rule is absolute: if answering requires knowing
   what a named thing IS and you can't place it, look it up — partial recognition from training
   is not knowledge, and a new release by a known vendor is still unknown.

3. **Numeric call budgets.** 1 call for a single fact; 3–5 for medium tasks; 5–10 for deep
   comparisons; if a task obviously needs 20+, route it to the heavier subsystem (e.g.:
   Conductor sprint) instead of grinding inline.

4. **Source-priority ladder.** Internal/user data tools before web; combine for comparative
   queries ("our X vs industry"); originals over aggregators; skepticism scaled to
   SEO/conspiracy-prone topics, trust scaled up for plain breaking news.

5. **Query hygiene.** Short queries (1–6 words), broad→narrow, never repeat a near-identical
   query, use the real current date, fetch full pages when snippets won't do.

6. **Every answer must still be an answer.** No replying with only "I'd need to search" or a
   cutoff disclaimer — provide the best available substance, then verify or caveat.

Pattern note: everywhere the sample fights model laziness or overreach, it does so with a
NUMBER (word counts, call counts, step counts) or an ORDERED LIST — never an adverb.
</tool_routing>
