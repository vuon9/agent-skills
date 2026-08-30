# Install VM Skills

Catalog and reinstall Vuong's agent skills (written + preferred from other
authors) via a single manifest (`favorites.json`).

## How to use

1. **Install everything** for a fresh setup: `python3 scripts/install.py --all`.
2. **Or install just what vm needs:** `python3 scripts/install.py --required` (vm routes here automatically when a required skill is missing).
3. **Edit the list** with `scripts/manage.py`, then re-run `install.py` to apply.
4. **Refresh to latest** anytime: `npx skills update -g`.

## Use

- `python3 scripts/manage.py`. List, add, remove, change source, mark required.
- `python3 scripts/install.py`. Install/refresh. Filters: `--mine`, `--external`,
  `--required`, `--all` (default).
- `python3 scripts/update.py`. Refresh installed git-sourced skills to latest.
- `python3 scripts/sync_cursor.py`. Refresh the vendored cursor skills
  (`code-teach`, `bro`, `unslop`).

## Why

Rather than relying on the installed global state, this keeps one versioned
list of the skills you care about, each pinned to its `owner/repo` source so it
stays updateable with `npx skills update`. The `vm` mode checks its required
skills and routes here when something is missing.

## Notes

- `python3 scripts/manage.py add <name> --source <repo> --scope mine` adds a
  favorite (or changes its source). `--required` marks it as needed by `vm`.
- After any change, run `python3 scripts/install.py` to apply it locally.
- Some skills are local-only and listed with `"source": "local"`. They are
  skipped by the installer and must be kept manually.
