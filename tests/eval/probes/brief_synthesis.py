"""Level 3: targeted micro-probes for synthesis boundaries (opt-in, minimal LLM).

The plan allows <20% LLM only where deterministic parsing is insufficient.
These probes are NOT run by the standard unittest discovery (no test_ prefix
and no default case in main) so CI stays 0% LLM and 0 API cost. Run them
explicitly when a semantic answer is needed:

  python3 tests/eval/probes/brief_synthesis.py <trace.json> --probe brief-disjointness

Probe inputs come from an extracted trace JSON (see trace_extractor.py). The
probe questions are binary YES/NO so a cheap single-turn model call suffices;
parse the first word of the reply, never an essay.

Both probes degrade gracefully: without a configured LLM endpoint they print
SKIP and exit 0, so an unconfigured environment never hard-fails CI.
"""

import argparse
import json
import os
from pathlib import Path

# Optional LLM client. Only used when a provider/model is configured via env.
# Leave unset to run the deterministic pre-checks and skip the LLM turn.
LLM_API = os.environ.get("EVAL_LLM_API", "")
LLM_MODEL = os.environ.get("EVAL_LLM_MODEL", "")


def _yes_no(prompt: str) -> str:
    """One binary question to the configured LLM. Returns YES / NO / SKIP."""
    if not LLM_API or not LLM_MODEL:
        return "SKIP"
    # Placeholder transport: subclasses/providers override. Kept provider-free
    # so the module stays stdlib-only; wire your endpoint at call time.
    return "SKIP"


def probe_brief_disjointness(trace: dict) -> str:
    """If the parent delegated multiple children, does each brief restrict
    writes to strictly disjoint targets? Deterministic pre-check first."""
    subs = [s for s in trace.get("subagents", []) if s.get("tool_calls")]
    if len(subs) < 2:
        return "SKIP: fewer than two dispatched children to judge"
    # Deterministic part: distinct children should name distinct target files.
    seen_targets = []
    for s in subs:
        files = set()
        for tc in s.get("tool_calls", []):
            cmd = str(tc.get("input", {}).get("command") or tc.get("input", {}).get("argsSummary") or "")
            for token in cmd.replace("/", " ").split():
                if token.endswith((".py", ".ts", ".js", ".go", ".rs", ".md")):
                    files.add(token.split("/")[-1])
        seen_targets.append(files)
    overlapping = False
    for i in range(len(seen_targets)):
        for j in range(i + 1, len(seen_targets)):
            if seen_targets[i] & seen_targets[j]:
                overlapping = True
    if not overlapping:
        return "YES: child tool streams touch disjoint target files"
    if LLM_API and LLM_MODEL:
        return _yes_no("Do the dispatched briefs restrict writes to disjoint targets? Answer YES/NO.")
    return "NEEDS-LLM: overlapping file tokens found; configure EVAL_LLM_API to judge briefs"


def probe_dismissal_evidence(trace: dict) -> str:
    """When a finding is dismissed, the explanation must cite repo facts."""
    text = " ".join(
        [str(s.get("final_output", "")) for s in trace.get("subagents", [])]
        + [str(trace.get("final_response", ""))]
    )
    low = text.lower()
    dismissed = "dismiss" in low or "not a bug" in low or "out of scope" in low
    if not dismissed:
        return "SKIP: no dismissal found to judge"
    has_facts = any(marker in text for marker in ("git show", "HEAD:", "line", "grep", "commit", "test"))
    if has_facts:
        return "YES: dismissal cites observable repo facts"
    if LLM_API and LLM_MODEL:
        return _yes_no("Does the dismissal explanation cite observable repo facts? Answer YES/NO.")
    return "NEEDS-LLM: dismissal without obvious factual citation; configure EVAL_LLM_API to judge"


def main():
    parser = argparse.ArgumentParser(description="Level-3 semantic micro-probes.")
    parser.add_argument("trace_json", help="extracted trace JSON (trace_extractor output)")
    parser.add_argument("--probe", choices=["brief-disjointness", "dismissal-evidence"], default="brief-disjointness")
    args = parser.parse_args()
    trace = json.loads(Path(args.trace_json).read_text(encoding="utf-8"))
    if args.probe == "brief-disjointness":
        print(probe_brief_disjointness(trace))
    else:
        print(probe_dismissal_evidence(trace))


if __name__ == "__main__":
    main()
