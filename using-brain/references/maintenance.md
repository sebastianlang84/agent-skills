# Maintaining the Brain

Use the bundled [architecture and schema](architecture.md) when explaining or reproducing a
Brain. Report current implementation separately from desired capabilities. If the knowledge
base has its own schema, validate against that rather than silently replacing it.

## Improve retrieval through measurement

Use `autoresearch`: freeze representative questions, expected concepts, context cost and a
keep/discard rule; measure the baseline before changing one lever. Store raw runs outside the
knowledge base and preserve durable conclusions with their evidence.

Before adding an index, database projection, embedding layer or ranking strategy:

1. Freeze regression cases, held-out cases, primary metrics, integrity guardrails and result-log
   location before implementation.
2. Keep Markdown as the only write authority. Derived stores must preserve entries, links,
   sources, tags, trust states and verification records; detect stale data, build deterministically
   and survive deletion followed by a complete rebuild.
3. Measure answer sets, retrieval accuracy, latency and retrieved context size as appropriate.
   Test structured storage, lexical ranking and embeddings as separate levers.
4. Keep an addition only if integrity gates pass and measured benefit justifies its maintenance.

Growth succeeds when more useful knowledge is retrievable without increasing default context
load or weakening provenance and trust.

## Keep layers aligned

Change the skill when triggers, commands, step order or completion criteria change. Change the
Brain's own architecture docs when purpose, schema or capabilities change. Put mechanically
checkable rules in optional tools or CI and document what they enforce. Validate only owned files.

For trigger or routing changes, preserve representative intended-use and non-use prompts and
repeat checks on each supported harness. Literal skill invocation and successful retrieval are
different signals. Keep raw outputs out of the Brain; record conclusions and limitations there.
