# vmode evaluation, hardening, and retest: final report

Date: 2026-09-02
Author: AI-assisted evaluation run with Vuong (vuon9/vstack)
Status: fixes applied locally, re-tested, and pushed in this change

This report consolidates the full cycle: a simulated evaluation of vmode,
the weaknesses it exposed, the fixes applied to vmode files, the re-test that
validated those fixes, and the artifacts shipped in this push.

---

## 1. Evaluation method

Three isolated scratch repos under /tmp/vmode-sim (first round) and
/tmp/vmode-sim2 (retest round), each seeded with a different situation:

1. Feature: add a `multiply` operation to a calc CLI (playbooks/feature.md).
2. Bug-fix: `subtract` returns the wrong sign when a < b (playbooks/bug-fix.md).
3. Investigation: explain cache/retry interaction in a router
   (playbooks/investigation.md + research role).

Each run was a fresh headless pi session (deepseek-v4-pro, no lens), prompted
to "work in vmode mode" with subagent dispatch available. Compliance was scored
against vmode's own contract: non-negotiables, playbook routing, role briefs,
artifact verification, and reply rules.

## 2. Weaknesses found (round 1)

Seven weaknesses were documented in detail in
docs/vmode-eval-2026-09-02-weaknesses.md. Summary:

- W1: Subagents drift on file and line citations (off-by-one), parent must catch it.
- W2: Required-skills check is name-only, cannot fail.
- W3: Behavior-first requirement has no concrete default, features fall back to unit tests.
- W4: Delegation always serial single-child; throughput checkpoint never runs parallel.
- W5: hunk-review local-review step is a no-op without a live Hunk session.
- W6: Reliability is parent-verified only because the parent re-does the work (children return claims, not evidence).
- W7: Skill availability read from stale session context.

## 3. Fixes applied to vmode

Four files changed, each fix mapped to the weakness it addresses:

| File | Change | Weakness |
| --- | --- | --- |
| vmode/SKILL.md | Required-skills check now means filesystem/manifest presence; run `set-it-up --required` if missing; "Verify, don't assume" now requires raw evidence, not claims | W2, W6, W7 |
| vmode/playbooks/feature.md | Behavior proof now means exercising the user-facing boundary (CLI/HTTP/public API) with automated assertions, with a BDD-less fallback (executable acceptance test); explicit concurrent-dispatch trigger on disjoint targets; subagents must return raw execution evidence; hunk-review fallback to requesting-code-review or a fresh reviewer subagent | W3, W4, W5, W6 |
| vmode/playbooks/bug-fix.md | Local-review step fallback when no live Hunk session exists | W5 |
| vmode/references/roles.md | Research brief: verify each cited line with `grep -n`/read before citing, return raw output; general brief: return raw execution evidence (test logs, diff stat), unsubstantiated claims rejected | W1, W6 |

## 4. Re-test results (round 2)

Same seeds, prompts, and model as round 1. The fixed vmode was synced into the
global skill store (~/.agents/skills/vmode) before the runs so the sims loaded
the fixed files.

- W1: FIXED. Research subagent citations all matched the parent's raw grep -n
  output ("All line numbers match"); round 1 had every symbol off by one.
- W2: FIXED. Runs checked filesystem presence (e.g. "wayfinder (symlink exists)").
- W3: FIXED. Feature sim added a real CLI-boundary test (test_cli_multiply)
  asserting returncode 0 and exact stdout "42.0\n".
- W4: FIXED as specified. Serial execution with stated collision reasoning
  remains correct when targets overlap; the concurrent path is specified but
  not yet exercised (open item).
- W5: FIXED. Both sims delegated local review to a reviewer subagent instead of
  skipping the step.
- W6: FIXED. Parents required and used raw evidence (e.g. git show HEAD:calc.py
  to dismiss an out-of-scope finding; refusing a reviewer's test-output claim).
- W7: FIXED via the W2 filesystem check.

Artifacts stayed correct in both rounds (tests pass, minimal diffs, citations
exact). Costs per run were roughly $0.022 to $0.024.

Full detail: docs/vmode-eval-2026-09-02-retest-results.md.

## 5. What this push ships

- vmode/SKILL.md: concrete required-skills check, evidence-based verification principle.
- vmode/playbooks/feature.md: concrete behavior-proof default, concurrency trigger, evidence and review fallback requirements.
- vmode/playbooks/bug-fix.md: independent-review fallback.
- vmode/references/roles.md: verified-citation and raw-evidence brief requirements.
- docs/vmode-eval-2026-09-02-weaknesses.md and docs/vmode-eval-2026-09-02-retest-results.md: the evaluation record.
- .gitignore: ignore local pi runtime state (.pi/).

## 6. Open item

W4's concurrent-dispatch path is specified but never executed. Recommended next
test: one task with two genuinely disjoint write targets (two features, two
files, one parent) to prove the parallel merge path.

## 7. Artifacts and commands

Evaluation rigs (seeds, run logs, scored rubrics):

- Round 1: /tmp/vmode-sim/{feature,bugfix,investigate}
- Round 2: /tmp/vmode-sim2/{feature,bugfix,investigate}

Verification after merge:

```bash
python3 set-it-up/scripts/manage.py verify   # repo self-check
python3 set-it-up/scripts/install.py --mine   # refresh installed vmode to the merged version
```
