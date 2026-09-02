# vmode evaluation: weaknesses in detail

Date: 2026-09-02
Scope: 3 simulated runs in isolated repos (/tmp/vmode-sim/{feature,bugfix,investigate}),
headless pi sessions, deepseek-v4-pro, subagent tool available. Each run scored PASS on
playbook routing, required-skills check, real subagent use, artifact verification, and
reply discipline. The weaknesses below are the gaps found despite those passes. Every
claim cites the run log it came from.

---

## W1. Subagents drift on file and line citations, and the parent must catch it manually

### What happened

In the investigate run, the parent delegated an independent trace of `src/router.py`
to a read-only subagent. The subagent's logic matched, but its citations were wrong:

- It reported the file as 43 lines and cited `Cache.get` at lines 11-19,
  `Cache.set` at 21-22, `_is_retryable` at 25-26, `Router.request` at 35-48.
- Ground truth from the parent's `grep -n`: the file is 49 lines; the same symbols
  sit at 12-20, 22-23, 26-27, and 36-49 respectively. Every subagent line number was
  off by one (and the total count off by six).

Quotes from `investigate/run.log`:

- Parent: "The subagent's line numbers are slightly off from mine (the subagent
  reported the file as 43 lines, but grep -n showed 49 lines)... it said `Cache.get`
  lines 11-19, actual 12-20..."
- Parent resolution: "I use my own verified numbers from `grep -n`."

### Why it matters

An investigation's output is only as trustworthy as its citations. A consumer who
jumps to the cited line lands on the wrong code. The parent caught it here because
the file was 49 lines and easy to re-check. On a large subsystem the drift would be
silent, and the parent would have to re-read everything to detect it, which defeats
the point of delegation.

### Root cause

`roles.md` research brief says "Report findings with exact file and line citations"
but gives the subagent no operational method to obtain exact lines (no instruction to
anchor citations with `grep -n` or tools output). Subagents estimate line numbers
from internal token context and are confidently wrong.

### Suggested fix

Add an explicit anchor instruction to the research brief template in
`vmode/references/roles.md`:
"Before reporting, verify every cited symbol and line span using `grep -n` or exact
read tool output. Include the raw command output snippet as verification evidence."

---

## W2. The "required skills check" is a name listing, not a functional check

### What happened

All three runs announced the required-skills check as passed. But inspection of the
transcripts shows the check was "these names appear in my available-skills list",
not "these skills load and are usable":

- Feature run: explicitly listed all 7 names and moved on; it read `test-driven-development`
  and `unslop` SKILL.md bodies later because the task needed them, not because the
  startup check required it.
- Bug-fix run: asserted the 7 names from the session's available-skills list, did not
  open a single required-skill file (log shows no SKILL.md read for any required skill).
- Investigate run: opened only `vmode/SKILL.md`; none of the 7 required skill files.

The vmode contract (SKILL.md Non-negotiables) says "Start every task by checking the
required skills are available". `set-it-up` even has a `--required` path for the case
where one is missing. None of the runs ever touched `set-it-up`, because none detected
a missing skill.

### Why it matters

The check as executed cannot fail. A skill that is listed in prompt metadata but
broken on disk (missing body, unreadable, stale frontmatter) passes the name check and
only fails mid-task when invoked. The `set-it-up --required` remediation path is dead
code unless the check can actually detect a defect.

### Root cause

vmode requires checking availability without defining the verification mechanism:
filesystem inspection, manifest lookup, or skill tool probing. Without a concrete
procedure, agents default to trusting their session's static prompt catalog.

### Suggested fix

Define the check in `vmode/SKILL.md` Non-negotiables and Required Skills:
"Verify each required skill by confirming its entry in the active skills manifest or
checking that `<skill>/SKILL.md` exists and is non-empty. If any skill is missing or
unreadable, execute `set-it-up --required` before proceeding."

---

## W3. The behavior-first requirement has no concrete default, so features fall back to unit tests

### What happened

The feature run added `multiply` correctly (3 unit tests + CLI proof). But the
"Behavior first" principle and feature.md step 5 ("Prove the behavior. For user-facing
features, run behavior/feature tests") were satisfied by:

- a plain `unittest` method (`test_multiply`), and
- a manual CLI invocation the agent ran itself.

No behavior-level artifact was produced: no BDD file, no automated end-to-end script
that pins the user-visible contract independent of implementation. The repo has no
`.feature`/BDD setup, and `feature.md`'s marker line is still the literal placeholder
`<!-- EDIT: behavior-test --> Replace this line with your behavior-test command or approach.`

### Why it matters

"Behavior first" collapses into "unit tests plus a manual CLI demo" whenever the repo
lacks a preconfigured BDD harness. For a CLI, the contract is pinned to `assert
multiply(4,5) == 20` inside an internal test file. Nothing forces the agent to codify
automated proof at the surface the user touches (CLI stdout, exit code, or HTTP response).
The principle lacks teeth without a concrete fallback.

### Root cause

`feature.md` step 5 relies entirely on an EDIT placeholder that is often blank in a
fresh repo, and provides no concrete default definition of behavior proof.

### Suggested fix

Define a concrete default in `feature.md` step 5 before the optional override:
"Behavior proof requires an automated assertion against the user-facing boundary
(CLI command exit code and stdout, HTTP response payload, or public client call),
distinct from internal unit tests. If no BDD framework exists, write an executable
acceptance test or runner script that exercises this outer surface." The EDIT marker
then customizes the specific command runner rather than supplying the concept.

---

## W4. Delegation is serial and single-child; parallel evaluation was underspecified

### What happened

All three runs used subagents correctly, but always exactly one child at a time,
blocking until it returned:

- Feature run: one `worker` child for the whole implementation.
- Bug-fix run: one `reviewer` child for the root-cause cross-check.
- Investigate run: one research-style child for the trace.

feature.md step 3 requires a throughput checkpoint: "Independent workstreams",
"Shared mutable state", "Smallest safe decomposition". The feature agent performed
the checkpoint analytically and serialized: "Shared mutable state: both changes touch
the same two files, so I gave the whole unit to one subagent to avoid write collisions."
No run ever dispatched parallel children. Consequently, concurrent writes to disjoint
targets, collision avoidance, and parent result reconciliation remain unvalidated.

### Why it matters

Serial delegation on tightly coupled files is technically correct behavior, but the
evaluation suite failed to test the throughput checkpoint against tasks with decoupled,
disjoint targets. The multi-agent coordination path and merge logic remain untested in
practice.

### Root cause

Two combined issues:
1. The evaluation suite only presented single-unit tasks with overlapping file targets.
2. `feature.md` lacks an explicit dispatch trigger when multiple independent streams
   are identified during the checkpoint.

### Suggested fix

Update `feature.md` steps 3 and 4:
"If the throughput checkpoint identifies 2+ independent workstreams with strictly
disjoint write targets, dispatch them concurrently and reconcile their diffs. If work
targets overlap or share mutable state, serialize execution and document the collision
reason." Complement this by designing an evaluation run specifically targeting 2+
independent modules across disjoint paths.

---

## W5. The hunk-review local-review step is a no-op without a live Hunk session

### What happened

feature.md step 6 and bug-fix.md step 5 both mandate: "Run `hunk-review` on the local
diff". In the feature run, the agent skipped the step:

- "Local review. `skip: no live Hunk diff session running`."

The final verification before "done" degraded to the author agent reviewing its own diff,
the exact blind spot an independent review step is designed to eliminate.

### Why it matters

Strict adherence to comment hygiene and prose discipline depends on an external review
gate. When `hunk-review` skips silently in non-interactive or headless environments,
enforcement falls back solely on the model that produced the diff.

### Root cause

`hunk-review` requires an active interactive GUI or CLI session that does not exist in
headless runs or standard CI environments. The playbooks provided no fallback path for
non-interactive execution.

### Suggested fix

Define an explicit fallback directly in `vmode/references/reviews.md` (and reference it
in `feature.md` and `bug-fix.md`):
"Run `hunk-review` on the local diff. If no live Hunk review session is active, invoke
`requesting-code-review` on the diff, or dispatch a read-only reviewer subagent with the
diff to audit comments, prose, and regressions before completing the task."

---

## W6. Reliability is parent-verified but only because the parent re-does the work

### What happened

Across the runs, the parent caught subagent errors twice:

1. Feature run: subagent left a stale docstring ("multiply is missing") that the
   parent noticed only by re-reading the file after delegation.
2. Investigate run: subagent line numbers were off by one (W1).

In both cases correctness was preserved because the parent re-read the full artifact
after the child finished ("I review the diff myself", "I verified against grep -n").
While aligned with "You own every subagent's work", delegation saved little time: the
parent re-read every changed file and verified every cited line manually.

### Why it matters

The parent becomes an $O(N)$ throughput bottleneck. Delegation only yields leverage if
the parent can verify attached evidence rather than re-executing or re-reading the
entire artifact from scratch. Without attached proof, delegation is merely speculative
drafting.

### Root cause

The role briefs in `roles.md` ask for summaries and verification commands, but do not
mandate that subagents attach raw execution output (test terminal logs, git diff stat,
anchored grep snippets) as return evidence.

### Suggested fix

Update the role briefs in `vmode/references/roles.md`:
Require subagents to return raw execution artifacts alongside findings:
"Include raw execution evidence in the output: exact test output with passing assertions,
`git diff --stat` output, and anchored `grep -n` matches. Unsubstantiated claims are
rejected." The parent then spot-checks verifiable evidence rather than re-doing the work.

---

## W7. Skill-loading context was stale in the runs (environment artifact)

### What happened

The bug-fix run asserted skill availability from the session prompt rather than live
disk state. In headless environments, session context can lag behind recent skill
updates or installations until the environment is reinitialized.

### Why it matters

Confirms the failure mode identified in W2: trusting prompt-injected skill listings
without validating active capability creates blind spots.

### Suggested fix

Resolved by W2's fix (validating against the skill manifest or store on disk).

---

## Summary table

| # | Weakness | Severity | Fix location | Primary Action |
| --- | --- | --- | --- | --- |
| W1 | Subagents drift on file and line citations | High | `vmode/references/roles.md` | Mandate anchored `grep -n` proof in research briefs |
| W2 | Required-skills check is name-only, cannot fail | Medium | `vmode/SKILL.md` | Require manifest/disk presence check; make `set-it-up --required` reachable |
| W3 | Behavior proof lacks concrete default | Medium | `vmode/playbooks/feature.md` | Define default acceptance test requirement at user boundary |
| W4 | Parallel delegation unexercised in evaluations | Medium | `vmode/playbooks/feature.md` | Add explicit concurrent dispatch rule; add multi-workstream test cases |
| W5 | hunk-review step no-ops without live session | Medium | `vmode/playbooks/{feature,bug-fix}.md` | Add headless fallback (`requesting-code-review` or reviewer subagent) |
| W6 | Parent verification bottleneck ($O(N)$ re-read) | High | `vmode/references/roles.md` | Require subagents to return raw execution proof and diff stats |
| W7 | Stale session context masquerading as available skills | Low | Handled by W2 | Validate active manifest/disk rather than static prompt listing |

### Priority Implementation Order

1. **W6 + W1**: Convert subagent delegation from claim-based to evidence-based in `references/roles.md`.
2. **W5**: Add headless fallback to `feature.md` and `bug-fix.md` so review gates remain active.
3. **W2**: Add verifiable skill loading checks to `vmode/SKILL.md`.
4. **W3**: Establish automated boundary-test defaults in `feature.md`.
5. **W4**: Formalize parallel dispatch criteria and update test scenarios.
