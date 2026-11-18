# Brain architecture and schema

A Brain is a Git repository of linked Markdown concepts. Markdown is the write authority;
indexes route readers to small relevant subsets. Git records changes and enables review.
Search and optional derived indexes help retrieval but do not become a second knowledge store.

## Layout and retrieval

Start with `index.md`: a short map of topics with relative links and one-line descriptions.
Add subtree indexes only as the collection grows. Keep one durable claim, decision or method
per file; link related entries instead of copying them. Directory names reflect your subject
areas, not a required private taxonomy.

Read root index → relevant subtree → concept → original source when verification matters.
Use exact lexical search when the route is unclear. Load only the needed concepts into an
agent's context. This design does not promise automatic clustering, contradiction detection,
semantic retrieval or factual freshness checks.

## Entry schema

Use YAML frontmatter with these fields, or document an equivalent schema in your Brain:

```yaml
---
title: Prefer one canonical entry per concept
description: Update an existing concept rather than creating competing versions.
type: decision
status: draft
authored_by: agent
updated: 2026-01-01
sources:
  - ./index.md
---
```

The example illustrates the shape; it is not an established decision. Replace its source with
evidence that supports your actual claim, such as an openable repository file, decision record,
public document or consented conversation reference. Include enough detail to locate the passage.

Keep a small documented type vocabulary. A starter set is `decision` (choice, rationale and
reversal condition), `method` (repeatable steps and completion criteria), `reference` (durable
facts and their authority), and `check` (an executable or repeatable verification procedure).
Use `## Open questions` for unresolved knowledge; track actionable work separately.

## Provenance and trust

`draft` means unconfirmed synthesis. `adopted` means accepted for use within its stated scope;
record who or what authorized that transition. Verification records identify an independent
reviewer, time and evidence. An agent's own successful edit is not independent verification.
A source link records provenance, not proof: inspect the source for consequential claims.

Do not retain credentials, personal dossiers or unconsented transcripts. Record the minimal
knowledge needed for future work and preserve uncertainty rather than inventing authority.

## Optional tooling

A Brain may provide `tools/lint.py` for schema and link validation and
`tools/audit_staleness.py` for review dates or moved local sources. Neither is bundled here or
required to start. A staleness report cannot establish whether prose is still true.
The sibling `parallel-agents` skill supplies Linux cooperative write leases; writers must all
participate. Git history and leases serve different purposes and neither replaces content review.
