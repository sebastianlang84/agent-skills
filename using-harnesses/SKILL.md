---
name: using-harnesses
description: Run headless Codex or Claude Code for cross-vendor reviews, scoped worker or scout calls, and follow-ups. Use for a second opinion or delegated CLI work, and to collect, cancel or inspect a running call. Reviews use contained execution, secret checks and a deadline; Codex workers select an explicit sandbox. Use peer-debate for two-sided debates.
---

# Using harnesses

Requires Python 3.9+ and the selected CLI, installed and authenticated. Run from the collection
root below, or replace paths with your installed skill paths. Choose a reviewer from a different
vendor when independent review is the goal. Configure model and effort defaults for your account.

## Review

Write a brief stating intended use, scope, known constraints and the question to resolve. Pass
complete, scoped UTF-8 artifacts (diffs, source excerpts or command output). Reviewers see only
this payload and have tools disabled. Binary input, binary patches, `.env` files and recognized
secret patterns are refused before launch. Redact inputs yourself too: pattern checks cannot
identify every secret.

For Codex, first create a separate login; do not copy a rotating credential from another home:

```bash
CODEX_HOME="$HOME/.codex-review" codex login --device-auth
chmod 600 "$HOME/.codex-review/auth.json"   # POSIX; Windows uses private ACLs
```

Keep that home free of instruction files and user skills. Claude reviews use the ordinary Claude
login, safe mode and an empty tool list. The CLIs must support the flags used by the scripts.

```bash
S=using-harnesses/scripts
D=$(python3 "$S/review.py" codex /path/to/brief.md /path/to/change.diff)
python3 "$S/review.py" wait "$D"
# Use claude instead of codex for a Claude reviewer.
# Follow-up: review.py <vendor> --resume <session-id> <brief> <artifacts>...
# Custom rubric: add --rules /path/to/rules.md
python3 "$S/review.py" cancel "$D"
```

Start returns the call directory immediately. `wait` prints the session ID and answer; exit 75
means still running. The default deadline is 1800 seconds (`REVIEW_TIMEOUT=1..1800`); each wait
is at most 540 seconds. Other statuses: 2 setup/configuration, 3 refused input, 4 missing answer
or session, 5 missing completion marker, 124 deadline, 137 forced deadline termination,
143 cancellation. `--foreground` blocks when needed by a non-interactive caller.
Resume accepts only sessions started by this script. Verify findings against the actual artifacts
before acting; additional rounds should resolve a specific uncertainty.

The fixed [prompt frame](references/review-prompt.md) separates instructions from artifact data.
The call directory contains `payload.md`, `out.md`, `session`, logs and status. Keep these private
and remove them when no longer needed; no automatic retention policy is installed.

## Codex worker or scout

```bash
S=using-harnesses/scripts
D=$(python3 "$S/codex_call.py" new --detach --cwd /path/to/repo \
  --sandbox read-only --label scout /path/to/job.md)
python3 "$S/codex_call.py" wait "$D" --timeout 540
python3 "$S/codex_call.py" list -n 5
# Follow-up in the same thread:
python3 "$S/codex_call.py" resume <thread-id> --allow-resume /path/to/follow-up.md
python3 "$S/codex_call.py" cancel "$D"
```

The default sandbox is `read-only`; use `workspace-write` for an authorized edit and set `--cwd`
to the intended workspace. `--search` enables native web search; `--network` enables command
network access in a workspace-write sandbox. `danger-full-access` removes sandbox containment.
Workers have tools, so state scope and stopping conditions in the job. Worker waits return 3
while running; the wait timeout bounds collection, not execution. Cancel a worker to stop it.
Worker prompts do not receive the review payload's secret check.

Workers default to the separate Codex home above, with hooks and repository instruction loading
disabled. `--user-home` selects the ordinary Codex home with its configured integrations.
Resume requires `--allow-resume` because it carries prior thread history; a fresh call with a
short handoff often fits a new task better. Usage and step summaries accompany the answer.
`selftest` makes live provider calls; it is not an offline test.

## Configuration and state

Copy [models.conf.example](references/models.conf.example) to
`${XDG_CONFIG_HOME:-$HOME/.config}/using-harnesses/models.conf` for review model and effort defaults.
It is parsed as data, never executed. Inspect with `python3 using-harnesses/scripts/review.py --print-config`.
Workers use `CODEX_CALL_MODEL` / `CODEX_CALL_EFFORT`, or `--model` / `--effort` per call.

| Setting | Default | Purpose |
| --- | --- | --- |
| `CODEX_CALL_ROOT` | `$HOME/.agents/state/codex-call` | Worker metadata, prompts, outputs and usage log |
| `CODEX_CALL_HOME` | `$HOME/.codex-review` | Worker login and isolated configuration |
| `CODEX_CALL_USER_HOME` | `$HOME/.codex` | Ordinary home selected by `--user-home` |
| `TMPDIR` | System temporary directory | Private review call directories |

Claude review working files use `$HOME/.cache/using-harnesses/claude-review`. These are local
per-user paths; the scripts require no service, board, scheduler or background daemon.
