---
name: skills-verify
description: "Use when a pull request changes this skills collection (favorites.json or vm), when asked to check the collection matches vm's required skills, or when you need to reconcile the favorites list with what vm depends on. Posts a short GitHub comment report and updates it (upsert) on each re-run."
---

# Skills Verify

Check that this skills collection is internally consistent and good enough for `vm` to run. The two sources of truth are the manifest (`install-vm-skills/favorites.json`) and `vm/SKILL.md`. Every required skill `vm` declares must be present in the manifest as `required: true`, and every manifest entry marked `required: true` must be declared by `vm`. A PR that adds or drops a skill, or edits `vm`, must keep those two in lockstep.

## When

- A PR touches `install-vm-skills/favorites.json` or `vm/**`.
- You are asked to verify the collection, or `vm` complains a required skill is missing.
- You are adding a skill here and want it quality-checked before it is merged.

## What to check

Run these in order. Stop and fix the first thing you find; then re-run.

### 1. Required-skills match (bidirectional)

`vm/SKILL.md` has a section `## Required skills` listing every skill `vm` depends on. The manifest marks the same set with `"required": true`. They must match both directions:

- Every skill listed in `vm/SKILL.md` `## Required skills` exists in `favorites.json` with `"required": true`.
- Every manifest entry with `"required": true` is listed in `vm/SKILL.md` `## Required skills`.
- No typo in either list. A skill that exists but is not marked `required` on both sides is the usual drift.

### 2. Manifest entry validity

For each entry in `favorites.json`:

- `name` matches the `name:` field in that skill's `SKILL.md` frontmatter (and matches the folder name when the skill lives in this repo).
- `source` is an `owner/repo`, a full GitHub tree URL to a nested skill, or `local` (for manifest-only entries). Anything else is invalid.
- `scope` is `mine` or `external`. A `mine` skill must have a `vuon9/*` source (this repo or `vuon9/gh-workflows`).
- `required` is present only when true; omit it otherwise.

### 3. Quality of a skill in this repo

For a `mine` skill (or any skill folder checked out in this repo):

- `SKILL.md` has valid frontmatter with `name` and `description`.
- `name` uses letters, numbers, and hyphens only. No parentheses or special characters.
- `description` starts with `Use when` and states when to use, not what it does.
- A `README.md` exists next to `SKILL.md` with the human-facing use cases.

### 4. vm integrity

`vm/SKILL.md` parses. Its `## Required skills` list resolves to real skills. `vm/playbooks/*.md` and `vm/references/*.md` exist and are referenced. If `vm` was edited, confirm the same rule is updated in both the trigger ("Non-negotiables") and the principle, per the two-layer design described in `vm/README.md`.

## Reconcile

When the two lists diverge, fix the manifest and `vm` together, not just one.

- Prefer `install-vm-skills/scripts/manage.py` over hand-editing JSON:
  - Add a missing required skill: `python3 install-vm-skills/scripts/manage.py add <name> --source <owner/repo> --scope <mine|external> --required`
  - Drop an unneeded skill: `python3 install-vm-skills/scripts/manage.py remove <name>`
  - Switch a required flag: `python3 install-vm-skills/scripts/manage.py set-required <name> true`
  - Re-point a source: `python3 install-vm-skills/scripts/manage.py set-source <name> <owner/repo>`
- Add the skill to `vm/SKILL.md` `## Required skills` if it is a dependency, and remove it if it no longer is.
- Re-run `python3 install-vm-skills/scripts/install.py --required` locally to confirm the set installs cleanly.
- If a new skill is added, also add it to `.claude-plugin/plugin.json` and the collection `README.md` per the notes in `install-vm-skills/SKILL.md`.

## CI behavior

A GitHub Actions workflow (`skills-verify`) runs this on every pull request that changes `favorites.json` or `vm/**`. It uses `opencode/muse-spark-1.2-contributor-free` to do the check and post a short comment report on the PR.

- **Trigger.** `pull_request` with types `opened`, `synchronize`, `reopened`, `ready_for_review`, filtered to the two paths above. A new commit to the branch (`synchronize`) re-runs it.
- **Upsert, not append.** The agent edits its own previous comment on re-runs instead of posting a fresh one. Do not post multiple comments; keep one authoritative report.
- **Report.** Keep it short, around 6 to 12 lines. State what the PR changed (added, removed, or re-scoped skills), any mismatch found and how it was reconciled (or the exact command the author should run), and the pass or fail verdict.
- **Fixing vs reporting.** If the runner can safely edit the branch, apply the reconcile and update the comment to say so. Otherwise list the exact `manage.py` commands and the `vm/SKILL.md` edit needed, and mark the verdict as needing the author's fix.

## Notes

- The manifest is the single source of truth for intent, not the machine's installed state. Verify against `favorites.json` and `vm`, not against `~/.agents`.
- A skill that is required by `vm` but missing from the manifest is a hard fail. A manifest entry marked `required` that `vm` does not declare is also a hard fail (a phantom dependency).
- Keep the report factual. Name the mismatched skill, the mismatch, and the fix. Do not restate the whole manifest.
