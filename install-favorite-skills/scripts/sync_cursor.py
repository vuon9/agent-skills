#!/usr/bin/env python3
"""Refresh the vendored code-teach skill from cursor/plugins upstream.

Fetches cursor/plugins `pstack/skills/teach/SKILL.md`, renames `name: teach`
to `name: code-teach`, and writes it into `agent-skills/code-teach/SKILL.md`.
After syncing, commit and push, then run `npx skills update` (or install.py) to
pull the refreshed copy locally.
"""
import os
import re
import subprocess
import sys

UPSTREAM = "https://raw.githubusercontent.com/cursor/plugins/main/pstack/skills/teach/SKILL.md"
HERE = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(HERE, "..", "..", "code-teach", "SKILL.md")


def main():
    res = subprocess.run(["curl", "-fsSL", UPSTREAM], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"fetch failed: {res.stderr}", file=sys.stderr)
        sys.exit(1)

    content = res.stdout
    # Rename the frontmatter name so the skill installs as code-teach, not teach.
    content, n = re.subn(r"(?m)^name:\s*teach\s*$", "name: code-teach", content, count=1)
    if n != 1:
        print("warning: upstream SKILL.md frontmatter changed; code-teach name not rewritten.", file=sys.stderr)

    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    with open(DEST, "w") as fh:
        fh.write(content)
    print(f"synced code-teach -> {os.path.relpath(DEST)}")


if __name__ == "__main__":
    main()
