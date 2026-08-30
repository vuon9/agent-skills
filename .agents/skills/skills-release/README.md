# skills-release

Cut a release of this collection with `release-please` (the go-please flow). It
opens a single release PR whose description groups the changes since the last
release into typed lists, derived from conventional commit messages.

## Use it with a prompt

- "Open the next release PR" -> runs the release workflow, which diffs against the last release and opens the PR.
- "What's about to ship?" -> reads the existing release PR description, or derives the grouping from recent commits.
- "Make the commit messages release-ready" -> check the type prefixes so the next changelog is useful.

## What it does

1. Runs on push to `main` (or `workflow_dispatch`).
2. Reads conventional commits since the last release.
3. Opens or updates one release PR with a structural description: Features, Bug Fixes, Documentation, Chores, Breaking Changes.
4. Creates the tag and GitHub release when the PR merges.

## In CI

`.github/workflows/skills-release.yml` uses `googleapis/release-please-action@v4`
with `release-type: simple`. Config lives in `release-please-config.json` and
`.release-please-manifest.json`.
