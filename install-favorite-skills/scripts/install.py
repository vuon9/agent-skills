#!/usr/bin/env python3
"""Install every skill in favorites.json from its upstream source.

Idempotent: rerunning it refreshes git-sourced skills. If a skill is already
installed from a different source, it is removed first so the new source wins.
"""
import json
import os
import subprocess
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(SKILL_DIR, "favorites.json")
LOCK_PATH = os.path.expanduser("~/.agents/.skill-lock.json")


def load_skills():
    with open(MANIFEST) as fh:
        return json.load(fh)["skills"]


def current_source(name):
    try:
        with open(LOCK_PATH) as fh:
            lock = json.load(fh).get("skills", {})
    except Exception:
        lock = {}
    entry = lock.get(name) or {}
    return entry.get("source") or entry.get("sourceType") or None


def main():
    skills = load_skills()
    ok, failed = [], []

    for entry in skills:
        name = entry["name"]
        source = entry.get("source")

        if source in (None, "", "local"):
            print(f"[skip] {name}: local/manual ({entry.get('note', 'no repo source')})")
            continue

        existing = current_source(name)
        if existing and existing != source and existing != "local":
            print(f"[swap] {name}: removing existing ({existing}) before installing from {source}")
            subprocess.run(
                ["npx", "-y", "skills", "remove", name, "-g", "-y"],
                check=False,
                capture_output=True,
            )

        print(f"[install] {name} <- {source}")
        res = subprocess.run(
            ["npx", "-y", "skills", "add", "-g", source, "--skill", name, "--full-depth", "-y"],
            check=False,
            capture_output=True,
        )
        if res.returncode == 0:
            ok.append(name)
        else:
            err = (res.stderr or res.stdout or b"").decode(errors="replace").strip()
            failed.append((name, err))
            print(f"[FAILED] {name}:\n{err}")

    print()
    print(f"Installed/refreshed: {len(ok)}  |  Failed: {len(failed)}")
    for name, err in failed:
        print(f"  - {name}: {err[:200]}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
