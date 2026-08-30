---
name: skills-release
description: "Use when cutting a new release of this collection, when you want release-please to open the release PR, or when you need a structured PR description that groups the changes since the last release into concise lists. Runs from GitHub Actions on every push to main."
---

# Skills Release

Cut a release of this collection with `release-please` (the go-please flow). It opens a release PR whose description groups the changes since the last release into concise, typed lists (Features, Bug Fixes, Documentation, Chores) and drives version bumps. You do not write the release notes by hand; the tool derives them from conventional commit messages.

## When

- You merged a batch of commits and want the next version PR opened automatically.
- You want to see what is about to ship before tagging.
- A release PR already exists and you need to know its shape, or nudge a bumped version.

## How it works

- `release-please` runs on push to `main` via `.github/workflows/release.yml`.
- It reads the conventional commits since the last release tag/version, rolls them into a typed changelog, and opens a single release PR (for example `chore(main): release vX.Y.Z`).
- The PR description is the changelog: a `## What's Changed` list grouped under type headings. Because it is derived from commit prefixes, the quality of the notes depends on the commit messages, so keep them conventional.

## Conventional commits that drive it

For the notes to be useful, commit with a type prefix:

- `feat: ...` -> Features
- `fix: ...` -> Bug Fixes
- `docs: ...` -> Documentation
- `refactor:`, `perf:`, `chore:`, `build:`, `ci:` -> Chores / Maintenance
- `breaking:` or a `!` after the type (for example `feat:!`) -> Breaking Changes

Use the repo's existing convention (this collection uses `feat(vm):`, `docs:`, `refactor:`). Keep each subject under about 70 characters so the list stays readable.

## Release trigger

- **Automatic.** Push to `main`. The action diffs against the last release and opens or updates the release PR.
- **Manual.** `workflow_dispatch` is enabled. Use `gh workflow run release.yml` to open one on demand.

## Permissions and token

The action needs `contents: write` and `pull-requests: write`. It must use a **PAT**, not the built-in `GITHUB_TOKEN`: on a push-to-`main` run GitHub blocks `GITHUB_TOKEN` from creating the pull request (the error is `GitHub Actions is not permitted to create or approve pull requests`), and a PAT also lets the resulting release PR trigger CI on its own commits.

- Create a fine-grained PAT with **Contents: Read/Write** and **Pull requests: Read/Write** (and **Workflows: Read/Write** if you want the release PR to run the collection's workflows).
- Store it as the `RELEASE_PLEASE_TOKEN` secret; the workflow passes it as `token`.

## Config

- `release-please-config.json`. `release-type: simple` (this collection has no package manifest), package name `agent-skills`, `include-component-in-tag: false`.
- `.release-please-manifest.json`. Tracks the current version (`"."`).
- Bump strategy. Default `simple` bumps `minor` on feature or breaking commits and `patch` otherwise.

## After the PR merges

When the release PR merges, `release-please` creates the tag and the GitHub release. If you need to publish that version elsewhere (for example a README badge or a dependent repo pinning a tag), point it at the new tag. This collection needs no extra build step; the release is the tag plus the notes.

## Notes

- Do not rename the release PR title or strip the changelog. The action owns both and may rewrite them when new commits land.
- Keep commits shaped for the notes, not for prose. Notes are only as good as the prefixes, and the short report in the verify job reads the same set.
- If a release PR is already open and you push more commits to `main`, `release-please` updates the existing PR instead of opening another.
