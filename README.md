# Agent Skills

A collection of skills for AI coding agents.

## Install

This repository can be installed with the open agent skills CLI:

```bash
npx skills add vuon9/agent-skills
```

List available skills before installing:

```bash
npx skills add vuon9/agent-skills --list
```

Install one or more specific skills:

```bash
npx skills add vuon9/agent-skills --skill macos-release
npx skills add vuon9/agent-skills --skill apple-platform-readiness --skill ios-testflight-release
```

Install for specific agents:

```bash
npx skills add vuon9/agent-skills --agent codex
npx skills add vuon9/agent-skills --agent claude-code --agent cursor
```

Install globally instead of into the current project:

```bash
npx skills add vuon9/agent-skills --global --agent codex --skill macos-release --yes
```

Install all skills to all detected agents without prompts:

```bash
npx skills add vuon9/agent-skills --all
```

Full GitHub URLs work too:

```bash
npx skills add https://github.com/vuon9/agent-skills
```

Useful flags:

- `--skill <name>`: install specific skills.
- `--agent <agent>`: install to specific agents such as `codex`, `claude-code`, or `cursor`.
- `--global`: install at user scope instead of project scope.
- `--yes`: skip confirmation prompts.
- `--copy`: copy files instead of symlinking.
- `--all`: shorthand for installing all skills to all agents without prompts.

## Skills

| Skill | Description |
|-------|-------------|
| [apple-platform-readiness](./apple-platform-readiness/SKILL.md) | Apple platform environment, Xcode project, signing, simulator, archive, and App Store Connect readiness checks |
| [github-reusable-workflows](./github-reusable-workflows/SKILL.md) | GitHub Actions reusable workflow contracts, thin wrappers, secrets, local preflight, and versioning guardrails |
| [ios-testflight-release](./ios-testflight-release/SKILL.md) | iOS TestFlight release setup and upload guardrails using GitHub Actions and App Store Connect |
| [macos-release](./macos-release/SKILL.md) | macOS Developer ID signing, notarization, DMG Gatekeeper checks, and GitHub Actions release artifacts |
| [wails-fullstack](./wails-fullstack/SKILL.md) | Wails v3 desktop app development - Go backend with React/Vue/Svelte frontend |

Each skill folder includes a `README.md` with human-facing use cases. `SKILL.md`
stays focused on instructions that agents should load at runtime.

## License

MIT
