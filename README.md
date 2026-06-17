# Agent Skills

A collection of skills for AI coding agents.

## Install

Install this repository with the open agent skills CLI:

```bash
npx skills add vuon9/agent-skills
```

The `skills` tool opens an interactive flow where you can choose which skills
and agents to install.

## Skills

| Skill | Description |
|-------|-------------|
| [apple-platform-readiness](./apple-platform-readiness/SKILL.md) | Apple platform environment, Xcode project, signing, simulator, archive, and App Store Connect readiness checks |
| [github-reusable-workflows](./github-reusable-workflows/SKILL.md) | GitHub Actions reusable workflow contracts, thin wrappers, secrets, local preflight, and versioning guardrails |
| [ios-testflight-release](./ios-testflight-release/SKILL.md) | iOS TestFlight release setup and upload guardrails using GitHub Actions and App Store Connect |
| [macos-release](./macos-release/SKILL.md) | macOS Developer ID signing, notarization, DMG Gatekeeper checks, and GitHub Actions release artifacts |

Each skill folder includes a `README.md` with human-facing use cases. `SKILL.md`
stays focused on instructions that agents should load at runtime.

## License

MIT
