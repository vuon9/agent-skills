---
name: install-favorite-skills
description: Install, refresh, and catalog the user's favorite agent skills from their upstream repositories using favorites.json (a repo + skill-name manifest) and wrapper scripts. Use when restoring or updating the user's global skill set, adding, removing, or changing the source of a favorite, or checking what skills are installed.
---

# Install Favorite Skills

Catalog the user's preferred skills in `favorites.json` (each entry has a `source` repo and a `name`), then install or refresh them all. This keeps a single, versioned list of every skill the user cares about instead of relying on the installed state alone.

## Files

- `favorites.json` — the manifest. Array of `{ "name", "source" }` entries.
- `scripts/manage.py` — list, add, remove, or change the source of entries.
- `scripts/install.sh` — installs or refreshes every entry. Idempotent.
- `scripts/update.sh` — runs `npx skills update -g` to refresh installed git-sourced skills.

## Manifest format

```json
{
  "skills": [
    { "name": "gh-workflows", "source": "vuon9/gh-workflows" },
    { "name": "bro", "source": "cursor/plugins" },
    { "name": "cua-driver", "source": "local", "note": "installed manually" }
  ]
}
```

- `name` — the skill name (must match the `name:` in its `SKILL.md`).
- `source` — an `owner/repo` GitHub source, or `local` for skills that are not re-installable from a repo.
- `note` — optional; only used for `local` entries.

## Manage the list

Use `scripts/manage.py` to edit the manifest deterministically instead of hand-editing JSON:

```bash
# see what's listed
python3 scripts/manage.py list

# add a favorite (or change its source if it already exists)
python3 scripts/manage.py add <name> --source <owner/repo>

# remove a favorite (stops it being (re)installed)
python3 scripts/manage.py remove <name>

# change only the source of an existing favorite
python3 scripts/manage.py set-source <name> <owner/repo>
```

Notes:

- `add` on an existing name updates its source (that is the "remove the old and add" swap).
- Removing from the manifest only prevents future installs. To remove the copy already on the machine, run `npx skills remove <name> -g -y`.
- Edits are sorted by name on save, keeping the file readable.

## Apply the list locally

After any change, re-apply the manifest, then optionally refresh:

```bash
bash scripts/install.sh    # install/refresh every listed skill (swaps sources as needed)
bash scripts/update.sh     # refresh installed git-sourced skills to latest
```

## How it behaves

- Every `source != "local"` entry is installed from its upstream repo, so it stays updateable.
- If a skill is installed from a **different** source than the manifest, `install.sh` removes the old one first so the manifest source wins (useful when switching e.g. `bro`/`teach` from one repo to another).
- `local` entries are skipped.
- `--full-depth` is always passed to `npx skills add` so nested skills (for example `cursor/plugins` under `pstack/skills/`) are found.

## Notes

- Not every skill is re-installable: a few (`cua-driver`, `hunk-review`) are `local` and must be kept manually.
- The manifest is the single source of truth for the desired set, not the global install state. Regenerate it from `npx skills list -g` (or `~/.agents/.skill-lock.json`) when the user's collection changes.
- After adding a skill here, also add it to `.claude-plugin/plugin.json` and the collection `README.md` to keep it grouped and documented.
