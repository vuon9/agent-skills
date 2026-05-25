---
name: github-reusable-workflows
description: Use when creating, reviewing, or applying GitHub Actions reusable workflows, workflow_call contracts, thin caller wrappers, workflow secrets, or versioned CI/release automation.
---

# GitHub Reusable Workflows

Use this skill to keep reusable GitHub Actions simple, versioned, and safe for public or cross-repository use.

## Guardrails

- Keep product repositories thin: app-specific wrappers call reusable workflows; shared logic lives in the workflow repo.
- Do not reference private project names, local machine paths, personal secrets, or real credentials in public workflow examples.
- Pin callers to a tag or major version, not `main`, unless intentionally testing a branch.
- Prefer additive inputs. Breaking changes require a new major version.
- Never echo secrets. Use GitHub Actions secret masking, temp files, and minimal permissions.

## Reusable Workflow Contract

Use `workflow_call` for shared workflows:

```yaml
on:
  workflow_call:
    inputs:
      dry-run:
        type: boolean
        default: true
    secrets:
      APP_SECRET:
        required: false
```

Caller wrapper:

```yaml
jobs:
  release:
    uses: owner/workflows/.github/workflows/release.yml@v1
    with:
      dry-run: true
    secrets: inherit
```

Prefer explicit, documented inputs over hidden repository assumptions.

## Local Preflight

Use `act` only for workflow wiring checks:

```bash
act workflow_dispatch --validate -W .github/workflows/release.yml
act workflow_dispatch --dryrun -W .github/workflows/release.yml
```

`act` does not prove hosted-runner images, macOS signing, Xcode behavior, cloud credentials, or external service uploads.

## Remote Verification

Verify in this order:

1. YAML parses.
2. Dry-run workflow succeeds on GitHub Actions.
3. Real workflow succeeds on the intended runner.
4. Logs show the expected external effect.

For reusable workflows, inspect logs for:

- Called workflow tag and commit.
- Runner image and version.
- Input values, excluding secrets.
- Key success marker or exact failure reason.

## Versioning

Pilot with `v0.x` tags. After real usage succeeds across at least one caller, create a stable major tag:

```bash
git tag v1
git push origin v1
```

Move `v1` only after backward-compatible fixes are verified. Use `v2` for contract changes that require caller edits.
