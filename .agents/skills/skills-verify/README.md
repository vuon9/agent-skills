# skills-verify

Verify that this collection is good enough for `vm`: the required-skills list in
`vm/SKILL.md` and the `required: true` set in `favorites.json` must match, and
every skill in this repo must be well-formed.

## Use it with a prompt

- "Verify the skills collection" -> runs the check in the SKILL, reports drift and reconciliation.
- "I added a skill, is it good enough?" -> checks the new skill's frontmatter, README, and whether `vm` needs it.
- "Does the manifest match what vm requires?" -> confirms the bidirectional required-skills match.

## What it does

1. Compares `vm/SKILL.md` required skills with `favorites.json` entries marked `required`.
2. Validates each manifest entry (name, source, scope, required).
3. Quality-checks skills that live in this repo (frontmatter, name, README).
4. Reconciles drift using `install-vm-skills/scripts/manage.py`, then updates `vm/SKILL.md`.

## In CI

`.github/workflows/skills-verify.yml` runs it on every PR touching
`install-vm-skills/favorites.json` or `vm/**`. It uses
`opencode/muse-spark-1.2-contributor-free` and posts a short comment report on the
PR. Re-runs update that one comment instead of adding new ones.
