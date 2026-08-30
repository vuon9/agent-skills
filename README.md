# Agent Skills

A collection of skills for AI coding agents.

## Install

Install this repository with the open agent skills CLI:

```bash
npx skills add -g vuon9/agent-skills
```

The `skills` tool opens an interactive flow where you can choose which skills
and agents to install.

## Skills

| Skill | Description |
|-------|-------------|
| [github-reusable-workflows](./github-reusable-workflows/SKILL.md) | GitHub Actions reusable workflow contracts, thin wrappers, secrets, local preflight, and versioning guardrails |
| [shipping-darwin-apps](./shipping-darwin-apps/SKILL.md) | Build and ship iOS/macOS apps (native, Wails, Tauri, Electron, Go/Rust): readiness, build, signing, notarization, TestFlight, App Store, DMG |

Each skill folder includes a `README.md` with human-facing use cases. `SKILL.md`
stays focused on instructions that agents should load at runtime.

## License

MIT
