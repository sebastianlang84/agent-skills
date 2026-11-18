# peer-debate — for humans

`SKILL.md` is written for the agent and says what to do. This file says why it is built the way it
is, and is deliberately not referenced from `SKILL.md`, so it costs the agent nothing.

See the [control-flow diagram](https://sebastianlang84.github.io/agent-skills/peer-debate/docs/debate-flow.html) (source: `docs/debate-flow.html`).

## What it is

Two model instances — one model twice, or two vendors among Gemini via `agy`, GPT via `codex` and Claude via `claude` — argue one
contestable question under opposed roles. The orchestrating
agent carries every turn between them and judges the result. The point is not to get two answers —
it is to make each side attack the other's reasoning, which surfaces errors that neither would find
alone and that the orchestrator, sharing the question but not the work, would not find either.

## Three decisions worth knowing

**Nobody is running between turns.** Each turn starts a fresh `agy --print`, `claude -p` or `using-harnesses`' `codex_call.py` process
that exits once it has answered; what survives is a conversation or thread id, not a resident
agent. There is no separate
judge — judging happens inside the orchestrator. The two sides run concurrently only in blind round
0; later turns are relayed in order.

That is also why there is no lock file and none is missing. Nothing polls and nothing can be woken,
so two debaters sharing a file would sit waiting for a writer that never runs. The orchestrator is
the transport.

**The roles are asymmetric on purpose.** Two instances of one model at one temperature agree after
about one round, and that agreement is an artefact of the symmetry rather than a signal of quality.
One side proposes and defends; the other is told to break it. Open dissent is a valid outcome.

**Convergence is not correctness.** Models can share blind spots, including across vendors.
Where they agree on something the judge cannot independently break, the correct move is not another
round — it is a reviewer from a different vendor. That is the third exit in the diagram.

## Usage record

Each Agy result reports cumulative input, output, thinking, cache-read and total tokens for that
side; each Codex turn reports its own input, cached, reasoning and output tokens. The driver stamps
those counters into `transcript.md`. Neither cli reports a monetary cost, so the transcript makes
no cost claim.

## Requirements

Python 3.9+ and the selected CLI(s): `agy`, `codex` or `claude`, authenticated with the requested
models available. Codex calls use the sibling `using-harnesses` worker wrapper and its separate
login. `debate.py check` checks local setup; the first provider call establishes model availability.
See [SKILL.md](SKILL.md) for configuration and [tool policy](references/tool-policy.md) for
the broad permissions granted to debate turns.

## Where things live

| | |
|---|---|
| Skill and role prompts | this directory |
| Run directories | `~/.agents/state/peer-debates/<date>-<slug>/` — transcript, result, and one `A/` and `B/` working directory per side |
| Session state | Provider conversation or thread IDs in `conversation-A.txt` and `conversation-B.txt`; the selected CLI keeps its history |
