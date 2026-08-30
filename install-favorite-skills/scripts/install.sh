#!/usr/bin/env bash
#
# Install every skill listed in favorites.json from its upstream source.
# Idempotent: rerunning it refreshes git-sourced skills. If a skill is already
# installed from a different source, it is removed first so the new source wins.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="$SCRIPT_DIR/../favorites.json"

if [ ! -f "$MANIFEST" ]; then
  echo "Manifest not found: $MANIFEST" >&2
  exit 1
fi

python3 - "$MANIFEST" <<'PY'
import json, os, sys, subprocess

manifest = json.load(open(sys.argv[1]))
lock_path = os.path.expanduser("~/.agents/.skill-lock.json")
lock = {}
try:
    lock = json.load(open(lock_path)).get("skills", {})
except Exception:
    lock = {}

def current_source(name):
    entry = lock.get(name) or {}
    return entry.get("source") or entry.get("sourceType") or None

ok, failed = [], []
for entry in manifest["skills"]:
    name = entry["name"]
    source = entry.get("source")

    if source in (None, "", "local"):
        note = entry.get("note", "no repo source")
        print(f"[skip] {name}: local/manual ({note})")
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
        failed.append((name, (res.stderr or res.stdout or b"").decode(errors="replace").strip()))
        print(f"[FAILED] {name}:\n{res.stderr.decode(errors='replace').strip()}")

print()
print(f"Installed/refreshed: {len(ok)}  |  Failed: {len(failed)}")
for name, err in failed:
    print(f"  - {name}: {err[:200]}")
PY
