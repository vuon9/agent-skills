# GitHub Reusable Workflows

Use this skill when an agent is creating, reviewing, or applying reusable
GitHub Actions workflows with `workflow_call`.

## Good Use Cases

- Design a shared workflow contract with explicit inputs and secrets.
- Keep app repositories thin by calling versioned reusable workflows.
- Review whether a caller wrapper is pinned safely and passes only the config it
  should own.
- Decide when a workflow change is additive, breaking, or needs a new major tag.
- Plan local YAML checks and remote GitHub Actions verification.

## Not For

- General GitHub issue or PR operations.
- Product-specific release steps that belong in a narrower release skill.
- Treating `act` as proof of hosted macOS, Xcode, signing, or external upload
  behavior.
