---
name: install-favorite-skills
description: Install, refresh, and catalog the user's favorite agent skills from their upstream repositories using favorites.json (a repo + skill-name manifest) and a wrapper script. Use when restoring or updating the user's global skill set, adding or removing a favorite, or checking what skills are installed.
---

# Install Favorite Skills

Catalog the user's preferred skills in `favorites.json` (each entry has a `source` repo and a `name`), then install or refresh them all with one script. This keeps a single, versioned list of every skill the user cares about instead of relying on the installed state alone.

## Files

- `favorites.json` — the manifest. Array of `{ "name", "source" }` entries.
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

## How it behaves

From this skill directory, run:

```bash
bash scripts/install.sh
```

- Every `source != "local"` entry is installed from its upstream repo, so they stay updateable.
- If a skill is currently installed from a **different** source than the manifest says, the script removes the old one first so the manifest source wins (useful when switching e.g. `bro`/`teach` from one repo to another).
- `local` entries are skipped.

Refresh all existing git-sourced skills:

```bash
bash scripts/update.sh
```

## Adding or removing a favorite

1. Edit `favorites.json`: add `{ "name", "source" }` or delete an entry.
2. Re-run `scripts/install.sh`.

Remember to keep `favorites.json` in sync with the `.claude-plugin/plugin.json` `skills` array and the collection `README.md` if you want the skill grouped and documented.

## Notes

- `--full-depth` is always passed to `npx skills add` so skills nested outside the default search dirs (for example `cursor/plugins` under `pstack/skills/`) are found.
- Not every installed skill is re-installable: a few (`cua-driver`, `hunk-review`) are `local` and must be kept manually.
- The manifest is the single source of truth for the desired set, not the global install state. Regenerate it from `npx skills list -g` (or `~/.agents/.skill-lock.json`) when the user's collection changes.
