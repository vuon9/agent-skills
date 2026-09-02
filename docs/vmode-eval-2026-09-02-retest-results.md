# vmode re-test after fixes: results

Date: 2026-09-02 (second round)
Compared against the first evaluation (docs/vmode-eval-2026-09-02-weaknesses.md, sims in /tmp/vmode-sim).
Second round sims: /tmp/vmode-sim2/{feature,bugfix,investigate}. Same seeds, same prompts, same model
(deepseek-v4-pro, headless pi, no lens). The only change: vmode/SKILL.md, playbooks, and roles.md fixes
(synced from local working tree into ~/.agents/skills/vmode before testing).

## Fix-to-weakness map (what the user changed)

- W1 line-citation drift -> roles.md research brief: verify each line with `grep -n`, return raw output
- W2 name-only skills check -> SKILL.md: filesystem/manifest presence check, run set-it-up --required if missing
- W3 no behavior default -> feature.md step 5: exercise user-facing boundary with automated assertions
- W4 no parallel trigger -> feature.md step 3: dispatch concurrently if disjoint targets, else serialize with reason
- W5 hunk-review no-op -> feature.md + bug-fix.md: fallback to requesting-code-review or fresh reviewer subagent
- W6 parent re-reads everything -> roles.md briefs: child must return raw execution evidence, claims rejected
- W7 stale context -> covered by W2 filesystem check

## Results per weakness

### W1 (line citations) - FIXED

Investigate sim. Parent dispatched a read-only `reviewer` subagent with the roles.md research brief
("verify each cited line using grep -n or read output"). Parent then cross-checked every citation
against its own raw `grep -n` output. Outcome quote: "All line numbers match."

- v1: subagent cited file as 43 lines, every symbol off by one. Parent: "The subagent's line numbers are WRONG (off by one)".
- v2: every cited line verified correct (spot-checked 24-25, 35-45 against the file: all exact).

### W2 (required-skills check) - FIXED

All three runs checked filesystem/listing presence instead of trusting the session list. Bug-fix sim
explicitly: "wayfinder (symlink exists)". The check now has a concrete method and set-it-up --required
is reachable if a check fails. (No run needed remediation since all skills present.)

### W3 (behavior-first default) - FIXED

Feature sim added a real CLI-boundary test (W3 target): `test_cli_multiply` runs the actual CLI via
subprocess and asserts returncode 0 and exact stdout "42.0\n". The agent also fixed its own first test
to match the real artifact (expected 42, CLI prints 42.0) instead of bending the artifact to the test.

### W4 (parallel dispatch trigger) - FIXED as specified

No sim had genuinely disjoint parallel workstreams, so per the new rule ("if targets overlap or share
mutable state, serialize and state the collision reason") serial execution remains correct. The rule
gave the agent the right decision procedure; the concurrency path itself still needs a dedicated
parallelizable test task to prove the merge path (open item).

### W5 (hunk-review no-op) - FIXED

Feature sim: instead of "skip: no live Hunk session" (v1), the agent delegated local review to a
`reviewer` subagent with a self-contained brief over the diff, incorporated its finding (stale
docstring), and re-verified. Bug-fix sim: same, reviewer returned approve; parent did not accept the
reviewer's test-output claim at face value and ran the test itself.

### W6 (raw evidence, not claims) - FIXED

Parent no longer trusts child summaries. Feature sim: parent used `git show HEAD:calc.py` as proof to
dismiss an out-of-scope finding (triage with evidence). Bug-fix sim: parent explicitly would not accept
the reviewer's statement about test output and ran the test itself. Roles.md briefs now require the
child to return raw output; the parent spot-checks rather than re-reading everything.

### W7 (stale context) - FIXED (by W2)

Not directly observable in these runs (all skills present); the filesystem check removes dependence on
session context.

## Artifact outcomes (unchanged quality)

- feature: 4/4 tests pass (3 unit + 1 CLI behavior), clean minimal diff. Cost ~$0.024.
- bugfix: test passes, one-file diff (-5/+2), docstring corrected. Cost ~$0.023.
- investigate: answer correct, all citations exact, fact/inference separated, confidence calibrated. Cost ~$0.022.

Reply discipline held: no em dashes in any final reply, principles named to decisions, consumer named first.

## Remaining open item

W4's concurrent-dispatch path is specified but never executed. To prove it, run one task with two
genuinely disjoint workstreams (two features in two files, one parent) and verify the merge. Nothing
else outstanding from the weakness list.
