# Tool policy

Debaters run through `agy`, `codex` or `claude` with their configured tool surface. A Codex side
uses the sibling `using-harnesses/scripts/codex_call.py` with `--sandbox danger-full-access`,
`--search` and hooks off. Agy and Claude receive `--dangerously-skip-permissions` so headless
turns do not require interactive approval. None of these paths provides sandbox containment.

This lets the debaters calculate, write scripts and inspect local sources. Run only with data,
credentials and local access appropriate for that grant, for example in an isolated environment.
The role prompts constrain artifacts to each side's `A/` or `B/` directory as a behavioral rule;
they cannot enforce filesystem isolation.

The effective tools depend on each CLI's configuration. Agy does not expose a per-invocation
allowlist. `debate.py check` checks executable and model selection, not all remote credentials
or tool behavior. Codex workers use the separate home configured by `CODEX_CALL_HOME`, so they
inherit that home's integrations rather than the ordinary Codex configuration.

Agy receives the side directory through `--add-dir` and absolute paths to keep file operations
in the debate record. The two working directories keep blind round 0 separate; they are not
security boundaries.
