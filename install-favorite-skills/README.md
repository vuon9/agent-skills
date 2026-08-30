# Install Favorite Skills

Catalog and reinstall the user's favorite agent skills from their upstream
repositories via a single manifest (`favorites.json`).

## Use

- `scripts/install.sh` — install or refresh every skill in `favorites.json`.
- `scripts/update.sh` — refresh installed git-sourced skills to latest.

## Why

Rather than relying on the installed global state, this keeps one versioned
list of the skills you care about, each pinned to its `owner/repo` source so it
stays updateable with `npx skills update`.

## Notes

- Skills can be added by editing `favorites.json` (see `SKILL.md` for the
  schema).
- Some installed skills are local-only and are listed with `"source": "local"`
  so the installer skips them.
