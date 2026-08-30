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
| [bro](./bro/SKILL.md) | Restate the last message in plain human language with no jargon |
| [code-teach](./code-teach/SKILL.md) | Vendored alias of cursor/plugins' `teach`: explain a body of work plainly so a person understands it |
| [how](./how/SKILL.md) | Explain how a subsystem works; code walkthroughs, placement/layering questions |
| [why](./why/SKILL.md) | Explain why a change: design rationale, regressions, postmortems via cited evidence |
| [install-vm-skills](./install-vm-skills/SKILL.md) | Catalog and reinstall Vuong's skills (written + preferred) via a `favorites.json` manifest with scope/required flags and install/update scripts |
| [shipping-darwin-apps](./shipping-darwin-apps/SKILL.md) | Build and ship iOS/macOS apps (native, Wails, Tauri, Electron, Go/Rust): readiness, build, signing, notarization, TestFlight, App Store, DMG |
| [unslop](./unslop/SKILL.md) | The AI tells and write with human voice |
| [vm](./vm/SKILL.md) | Vuong's manual development-workflow mode: behavior-first, review and PR discipline, subagent roles (watchdog, general, research) |

Each skill folder includes a `README.md` with human-facing use cases. `SKILL.md`
stays focused on instructions that agents should load at runtime.

## License

MIT
