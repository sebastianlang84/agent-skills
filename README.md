# Agent skills

Nine portable workflows for agents working with code, context and each other.

Agent sessions often lose decisions, carry too much context, repeat weak review loops, or collide
when several workers edit the same repository. This collection makes those workflows explicit:
retrieve what matters, scope the work, gather evidence, verify the result and preserve useful knowledge.

> **Agent-maintained.** All code, documentation, commits and pushes in this repository come from AI coding agents
> (Claude Code and Codex). I contribute ideas, set the direction and review the output; I don't write code, commit or push.

## Skills

| Skill | Problem it solves |
| --- | --- |
| [autoresearch](autoresearch/SKILL.md) | Improves a system through fixed evaluations, one controlled change and a keep/discard decision. |
| [call-doctor](call-doctor/SKILL.md) | Diagnoses a failed agent session using redacted transcript and loaded-context evidence reviewed by another vendor. |
| [context-engineering](context-engineering/SKILL.md) | Places instructions, memory, tools and documentation in layers that agents can find and use. |
| [git-workflow](git-workflow/SKILL.md) | Guides safe Git operations, branch and worktree choices, conflict resolution and task closeout. |
| [improving-code-quality](improving-code-quality/SKILL.md) | Finds unnecessary complexity, duplicated rules and wasted work across an affected processing flow. |
| [parallel-agents](parallel-agents/SKILL.md) | Coordinates file ownership and concurrent writers with worktree observations and cooperative leases. |
| [peer-debate](peer-debate/SKILL.md) | Tests a contestable question through opposed model roles and explicit adjudication. |
| [using-brain](using-brain/SKILL.md) | Retrieves and preserves durable knowledge in a configurable Git-backed Markdown knowledge base. |
| [using-harnesses](using-harnesses/SKILL.md) | Runs contained headless reviews and scoped Codex worker or scout calls. |

## How it works

Each directory follows the Agent Skills format: `SKILL.md` contains YAML `name` and `description`
fields plus the workflow. References and templates load when needed. Python and shell helpers
handle deterministic work such as process control, evidence collection and write leases.

The skills can be used individually. Keep these dependencies together:

- `call-doctor` calls the sibling `using-harnesses/scripts/review.py`.
- Codex turns in `peer-debate` call the sibling `using-harnesses/scripts/codex_call.py`.
- `using-brain` uses `parallel-agents` for concurrent writes and `git-workflow` for Git operations.

There is no hosted service, automatic scheduler, bundled knowledge corpus or required task board.

## Install

Clone this repository into a stable location:

```bash
git clone https://github.com/sebastianlang84/agent-skills.git "$HOME/agent-skills"
cd "$HOME/agent-skills"
```

Symlink the skill directories into the discovery directory used by your harness. Choose one
location for a given harness to avoid duplicate registrations:

```bash
skills_repo="$PWD"
skills_target="$HOME/.claude/skills"   # Claude Code
# skills_target="$HOME/.codex/skills"  # Codex user skills
# skills_target="$HOME/.agents/skills" # Shared skills, for harnesses that discover this path
mkdir -p "$skills_target"
for skill in autoresearch call-doctor context-engineering git-workflow improving-code-quality \
             parallel-agents peer-debate using-brain using-harnesses; do
  ln -s "$skills_repo/$skill" "$skills_target/$skill"
done
```

`ln -s` leaves an existing destination in place and reports the conflict; inspect it before
replacing anything. Restart or reload your harness if needed to discover the skills.
On Windows, use native directory symlinks or copy all nine directories into the selected location;
keep siblings together. Script commands use `python` where `python3` is unavailable.

## Requirements and quickstart

The written workflows need an agent that can load Agent Skills. Scripted workflows require
Python 3.9+ (standard library only at runtime). Git is needed for Git and worktree helpers.
Provider calls require the selected authenticated Codex CLI or Claude Code; `peer-debate` also
supports `agy` for Gemini. Model access and CLI flag support depend on your installed versions.

From the clone, a contained review can be started as follows:

```bash
# One-time Codex reviewer/worker login; keep it separate from your normal Codex home.
CODEX_HOME="$HOME/.codex-review" codex login --device-auth
chmod 600 "$HOME/.codex-review/auth.json"  # POSIX; use private ACLs on Windows

work=$(mktemp -d)   # private to you; holds unpublished changes
printf '%s\n' 'Review the intended behavior and identify concrete failures.' > "$work/brief.md"
git diff > "$work/change.diff"
review_dir=$(python3 using-harnesses/scripts/review.py codex "$work/brief.md" "$work/change.diff")
python3 using-harnesses/scripts/review.py wait "$review_dir"   # repeat while it exits 75
rm -r "$work"
```

Pass a real source file or document instead of an empty diff when reviewing unchanged work.
For a Claude reviewer, replace `codex` with `claude` and authenticate Claude Code normally.
Review wait status 75 means still running. See [using-harnesses](using-harnesses/SKILL.md) for
worker calls, cancellation, custom rubrics, error statuses and input checks.

Other entry points:

```bash
# Read-only scout; write a scoped job file first.
python3 using-harnesses/scripts/codex_call.py new --cwd /path/to/repo /path/to/job.md
# Diagnose one recorded session; prepare the linked doctor brief first.
bash call-doctor/scripts/doctor.sh --session /path/to/transcript.jsonl /path/to/doctor-brief.md
# Check debate setup with a Codex selection; init/round make live calls.
PEER_DEBATE_MODEL=codex:gpt-6.1-sol python3 peer-debate/scripts/debate.py check
```

The [doctor brief](call-doctor/references/brief.md),
[Brain schema](using-brain/references/architecture.md),
[Git hook installation](git-workflow/references/guardrails.md) and
[debate walkthrough](peer-debate/README.md) describe their setup in detail. Hooks are opt-in;
copying a skill does not register a hook or change your agent's global instructions.

## Configuration

Review defaults live in
`${XDG_CONFIG_HOME:-$HOME/.config}/using-harnesses/models.conf`:

```bash
mkdir -p "${XDG_CONFIG_HOME:-$HOME/.config}/using-harnesses"
# Copy the example only if you have not already configured this file.
cp -n using-harnesses/references/models.conf.example \
  "${XDG_CONFIG_HOME:-$HOME/.config}/using-harnesses/models.conf"
python3 using-harnesses/scripts/review.py --print-config
```

The file is parsed as data. Configure model IDs and accepted effort levels for your account.
Codex workers use `CODEX_CALL_MODEL` / `CODEX_CALL_EFFORT` or per-call flags. Their login and
state paths use `CODEX_CALL_HOME`, `CODEX_CALL_USER_HOME` and `CODEX_CALL_ROOT`.

Set `BRAIN_DIR` to your knowledge-base repository (default `$HOME/.agents/brain`). The collection
supplies a minimal schema, and lint or staleness tools are optional. `BRAIN_LOCK_ROOT` can override
the lease helper's Brain path. Debate configuration uses `PEER_DEBATE_*`; model, effort, timeout,
state directory and wrapper-path settings are documented in [peer-debate](peer-debate/SKILL.md).
Local state defaults to per-user directories under `$HOME/.agents/state`, `$HOME/.cache` or the
system temporary directory. Prompts, transcripts and outputs can be sensitive; manage retention
and access on your machine.

## Status and limitations

This is a standalone export of working workflows, with offline regression tests for the retained
helpers. It does not include private data or machine setup. Provider output formats, available
models and supported flags can change; offline tests do not establish live provider compatibility.

Review inputs pass a pattern-based secret check and reviewers have tools disabled. Worker prompts
and debate questions do not get the review secret check. Codex workers default to read-only;
[debate turns](peer-debate/references/tool-policy.md) intentionally bypass interactive permissions
and run with broad access. Role instructions are not a sandbox.

`call-doctor` needs Bash and recognizes Claude Code/Codex transcript formats. Ownership observations
cover Claude sessions only and do not prove a worktree is free. The Brain lease helper requires
Linux advisory locks, `/proc` and abstract Unix sockets; all writers must cooperate. The duplicate
write hook covers only configured Claude events. Git hook proofs may write temporary Git objects;
they do not execute the requested Git operation.

## Offline tests

Install `pytest` in your own environment, then run from this directory:

```bash
python3 -m pytest -q using-harnesses/tests call-doctor/tests peer-debate/scripts/test_debate.py \
  parallel-agents/scripts/test_brain_lock.py parallel-agents/scripts/test_coordination.py
python3 git-workflow/scripts/test_block_dangerous_git.py
bash using-harnesses/tests/test_review.sh
```

Tests use synthetic records, fake provider CLIs and temporary repositories. They do not need
network access or provider credentials. The Linux lease and process tests need a local environment
that permits those operating-system primitives.

## License

[MIT](LICENSE). No vendor endorsement is implied.
