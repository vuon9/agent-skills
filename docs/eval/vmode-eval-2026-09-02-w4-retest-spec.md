# W4 re-evaluation spec: parallel dispatch and merge

Status: EXERCISED and PASSED on 2026-09-02.
Purpose: a repeatable task that forces vmode's concurrent-dispatch path so the
merge behavior can be evaluated. Local doc, not committed.

## Result (2026-09-02)

Run in /tmp/vmode-sim3/parallel. All success criteria met:

1. Parent ran the feature playbook and the throughput checkpoint. PASS.
2. Checkpoint identified 2 disjoint workstreams (area vs temp). PASS.
3. Two children dispatched concurrently. PASS. Two worker transcripts captured
   (subagent-artifacts/ in the session dir): first events 47ms apart
   (18:52:51.515Z and 18:52:51.562Z), ~43s overlapping windows.
4. Parent reconciled both diffs itself (one docstring fix) and did not pass
   through child claims. PASS.
5. Both test files pass on the real artifact (4/4, exit 0). PASS.
6. Collision reasoning only needed if serialized; not triggered. N/A.

Failure modes watched: no serialization despite disjoint targets (not
observed); no overlapping writes (each child confined to its own files and
said so); parent merged and re-verified (observed); no cross-breaking changes
(4/4 pass).

Each child independently noted the sibling's concurrent edits in the shared
working tree, confirming real overlap rather than sequential execution.

W4 is now EXERCISED. See vmode-eval-2026-09-02-retest-results.md.

## What W4 claims

feature.md step 3/4 says: if 2+ independent workstreams have strictly disjoint
write targets, dispatch them concurrently and reconcile the diffs. If targets
overlap or share mutable state, serialize and state the collision reason.

The serial half was observed and works. The concurrent half (dispatch two
children in parallel, then parent merge) has never run.

## Task design (one parent, two disjoint files)

Seed a repo with two independent modules that share no mutable state and a test
runner that imports both:

```
src/area.py      (pure functions, area of rectangle/circle)
src/temp.py      (pure functions, C to F and F to C)
tests/test_area.py
tests/test_temp.py
```

Prompt (single headless pi session, vmode mode):

"Work in vmode mode. Add two features in this repo: (1) a rectangle perimeter
function in src/area.py with tests, (2) a kelvin-to-celsius conversion in
src/temp.py with tests. The two files and their tests are independent and do
not overlap. Follow vmode's rules: read the feature playbook, run the
throughput checkpoint, and dispatch the two workstreams concurrently if the
checkpoint finds disjoint targets. Verify both test files pass. Name the
principles that shaped your decisions."

## Success criteria

1. Parent runs the feature playbook and the throughput checkpoint.
2. Checkpoint identifies 2 disjoint workstreams (area vs temp).
3. Two children dispatched concurrently (evidence: overlapping/async subagent
   calls or two distinct child results in the transcript).
4. Parent reconciles both diffs itself and does not pass through child claims.
5. Both test files pass on the real artifact.
6. Parent reports the collision reasoning only if it serialized instead.

## Failure modes to watch

- Parent serializes despite disjoint targets (no concurrency attempted).
- Two children write overlapping files (checkpoint missed a shared target).
- Parent merges without re-verifying (accepts child claims).
- One child's change breaks the other's tests (merge conflict missed).

## Recording

The run that exercised this spec is in /tmp/vmode-sim3/parallel (run.log plus
child transcripts under the session's subagent-artifacts/). It was scored
against this spec and passed; W4 was flipped to EXERCISED in
vmode-eval-2026-09-02-retest-results.md on 2026-09-02. Re-run the same task if
vmode's dispatch rules change again.
