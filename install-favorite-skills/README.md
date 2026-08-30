# Install Favorite Skills

Catalog and reinstall the user's favorite agent skills from their upstream
repositories via a single manifest (`favorites.json`).

## Use

- `scripts/manage.py` — list, add, remove, or change the source of favorites.
- `scripts/install.py` — install or refresh every skill in `favorites.json`.
- `scripts/update.py` — refresh installed git-sourced skills to latest.

## Why

Rather than relying on the installed global state, this keeps one versioned
list of the skills you care about, each pinned to its `owner/repo` source so it
stays updateable with `npx skills update`.

## Notes

- `python3 scripts/manage.py add <name> --source <repo>` adds a favorite (or
  changes its source). `python3 scripts/manage.py remove <name>` removes it.
- After any change, run `python3 scripts/install.py` to apply it locally.
- Some installed skills are local-only and are listed with `"source": "local"`.
  They are skipped by the installer and must be kept manually.
