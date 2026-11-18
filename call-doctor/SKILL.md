---
name: call-doctor
description: Have the other vendor diagnose why an agent session worked badly - guessing, ignoring rules, missing knowledge, wrong tools - by examining its transcript and the context it was loaded with (instruction files, memory, skills, hooks). Use when the user asks for a doctor, a context diagnosis or "why does the agent know nothing", or when repeated corrections in a session point to a context problem. Not for reviewing a work product (adversarial review) or for making the fix (context-engineering).
---

# Call the doctor

The doctor is a different vendor from the patient session, at effort `medium`: a Claude Code
session gets Codex, a Codex session gets Claude Code. Model defaults come from `models.conf`.
`doctor.sh` reads the vendor from the transcript. It judges from redacted evidence with tools
disabled through `using-harnesses`' `review.py` and changes nothing. The call runs detached; keep
working and talking with the user while it runs.
From the collection root, set `D=call-doctor/scripts`; for an installed copy, use the absolute
path to that skill's `scripts` directory. Keep `using-harnesses` beside `call-doctor`.

1. **Name the patient and the symptoms.** The patient is the calling session unless the user names
   another one (session id or transcript path). Collect the user's complaints verbatim and the
   concrete incidents, with transcript line numbers where you know them. Do not write your own
   theory of the cause into the brief.
2. **Write the brief** from [`references/brief.md`](references/brief.md) into a private scratch
   file. If the session should have used a document it was not given (a system map, a skill it
   skipped), pass that file with `--extra`; the doctor sees nothing else.
3. **Start the round**:
   ```bash
   $D/doctor.sh [--session <id|path>] [--focus <from>-<to>]... [--extra <file>]... <brief-file>
   ```
   Pass each incident's transcript lines as `--focus` (call and result together): they are kept
   whole, while the rest of a large session is cut and partly omitted to fit 300 KB.
   It collects the evidence ([`collect.py`](scripts/collect.py): loaded context as recorded,
   timeline with `L<n>` = transcript line and compaction boundaries, secrets, e-mail addresses, IBANs and phone numbers
   redacted, subagent sidechains left out) and hands it to
   `using-harnesses`' `review.py`, which returns at once and prints the call directory.
4. **Collect** with `python3 "$D/../../using-harnesses/scripts/review.py" wait <dir>` (Windows:
   `python`) as a background command; exit 75 means still running, so wait again. Other exit codes are `review.py`'s: 3 = the
   payload hit a secret pattern before launch (redact the inputs, drop the `--extra` file or
   narrow `--focus`; no call directory is retained), 2 = setup, for example a missing reviewer login.
5. **Check before you relay.** Open every cited `L<n>` (`sed -n '<n>p' <transcript>`) and every
   cited file, and mark each cause confirmed or rejected with the reason. Report to the user:
   diagnosis, prioritized therapy, and what is model behaviour rather than context.
6. **Therapy is a separate step.** Apply agreed corrections with `context-engineering`, one canonical home per rule; the doctor's text is a proposal.

If `review.py` is missing or the other vendor is unreachable, say so and stop; never let the same
vendor be its own doctor.
