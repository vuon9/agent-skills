# Install Favorite Skills

Catalog and reinstall the user's favorite agent skills from their upstream
repositories via a single manifest (`favorites.json`).

## Use

- `python3 scripts/manage.py` — list, add, remove, or change the source of favorites.
- `python3 scripts/install.py` — install or refresh every skill in `favorites.json`.
- `python3 scripts/update.py` — refresh installed git-sourced skills to latest.
- `python3 scripts/sync_cursor.py` — refresh the vendored `code-teach` skill from cursor/plugins.

## Why

Rather than relying on the installed global state, this keeps one versioned
list of the skills you care about, each pinned to its `owner/repo` source so it
stays updateable with `npx skills update`.

## Notes

- `python3 scripts/manage.py add <name> --source <repo>` adds a favorite (or
  changes its source). `python3 scripts/manage.py remove <name>` removes it.
- After any change, run `python3 scripts/install.py` to apply it locally.
- `code-teach`, `how`, and `why` are vendored from cursor/plugins. `code-teach` is
  refreshed with `python3 scripts/sync_cursor.py`. `how` and `why` are
  normalized for editor-agnostic use, so refresh them manually and re-apply
  the edits.
- Some installed skills are local-only and are listed with `"source": "local"`.
  They are skipped by the installer and must be kept manually.
