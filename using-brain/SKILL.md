---
name: using-brain
description: Retrieve and maintain durable agent knowledge in a git-backed Markdown Brain at a configurable path. Use at session start to find relevant prior decisions, methods and repository knowledge, before finishing to preserve durable learning, or when explaining or changing the Brain's structure, provenance or trust rules. Respect BRAIN_SESSION_CONTEXT=0 in isolated runs. Not for a project-local knowledge system with its own rules.
---

# Using the Brain

The Brain is a git-backed Markdown knowledge base at `$BRAIN_DIR`, defaulting to
`$HOME/.agents/brain`. It can be shared across harnesses without a database or service.
Set it once in your environment; shell examples use:

```bash
export BRAIN_DIR="${BRAIN_DIR:-$HOME/.agents/brain}"
```

This collection supplies a [minimal architecture and schema](references/architecture.md),
not a prepopulated knowledge base. Create an `index.md` in a Git repository at your chosen path
and add entries as needed. Existing Brains keep their own documented vocabulary and trust rules.
No hook is installed automatically. If the Brain is absent or unavailable, report that boundary
and continue with the task; do not claim a read or write succeeded.

When the Brain is enabled, retrieve relevant knowledge before working and consider durable
learning before finishing. Respect `BRAIN_SESSION_CONTEXT=0` for intentionally isolated runs.

## Read

1. Open `$BRAIN_DIR/index.md` and choose the smallest relevant subtree from its descriptions.
2. Follow its index to the needed concepts. If routing is unclear, search with `rg` for a
   discriminative name, path or command. Do not bulk-load the corpus.
3. Check the cited source or owning repository for drift-prone or consequential claims. If your
   Brain provides `tools/audit_staleness.py`, optionally run it from `$BRAIN_DIR`; its findings
   are review triggers, not proof that a claim is false.
4. Preserve trust state: a draft or machine-written synthesis is not a human-confirmed rule.
   Retrieved knowledge does not override active instructions.

Reading is complete when you can name the relevant concept, its authority and any material
verification boundary. No relevant index entry or search hit is also a valid result.

## Decide whether to write

Write only knowledge that should change a future session: a decision with its rationale and
reversal condition, a durable correction, an invariant, a reusable method, or a confirmed
limitation. Search for the same idea and its neighbours first; update its canonical entry when
it already exists.

Keep transient task state in the task tracker or handoff and current product facts in the owning
repository. Do not store secrets, bulk transcripts, copied documentation or unsupported claims.
Keep open questions distinct from adopted decisions. Skip writing when nothing qualifies.

## Write

1. Read the target subtree index and the Brain's schema, if present; otherwise use the bundled
   [schema](references/architecture.md#entry-schema). Choose an existing type and canonical path.
   Treat a vocabulary change as a separate design decision.
2. Coordinate with other writers using `parallel-agents`. On Linux, acquire the concept and every
   index being edited together (replace `<skills-dir>` with this collection's install directory):

   ```bash
   python3 <skills-dir>/parallel-agents/scripts/brain-lock.py acquire concept.md index.md
   ```

   The helper uses `$BRAIN_DIR` unless `BRAIN_LOCK_ROOT` overrides it. Renew before lease expiry;
   if renewal fails, stop, reacquire and reread the files before continuing. On other platforms,
   use a shared coordination mechanism appropriate to that environment before concurrent writes.
3. Write one concept per file with a useful title and description, type, trust state, authoring
   role, timestamp, openable provenance and links to neighbouring entries. An agent must not
   certify its own work as human-verified.
4. Link a new entry from the nearest index. Change the root index only when retrieval needs it.
5. If your Brain provides `tools/lint.py`, run it from `$BRAIN_DIR` and fix failures only in your
   owned files. Otherwise check the schema, provenance and relative links manually.
6. Release the lease with `brain-lock.py release <token>` after validation. Git operations follow
   `git-workflow` and current authorization; stage only owned paths.

A write is complete when the entry has one canonical home, is discoverable, has provenance,
passes available validation and its lease is released.

Read [maintenance](references/maintenance.md) when changing retrieval, structure or this skill.
