# Agent Skills

A collection of skills for AI coding agents.

## Install

Install this repository with the open agent skills CLI:

```bash
npx skills add -g vuon9/agent-skills
```

The `skills` tool opens an interactive flow where you can choose which skills
and agents to install. The collection is managed and refreshed by
[install-vm-skills](./install-vm-skills/SKILL.md) (`favorites.json` is the
single source of truth for what gets installed).

## Skills

### Written by me

- [vm](./vm/SKILL.md). vuong mode, the manual development-workflow mode (behavior-first, review and PR discipline, watchdog/general/research roles)
- [install-vm-skills](./install-vm-skills/SKILL.md). Install and refresh this collection from `favorites.json`
- [shipping-darwin-apps](./shipping-darwin-apps/SKILL.md). Build and ship iOS/macOS apps (signing, notarization, TestFlight, DMG)
- [gh-workflows](https://github.com/vuon9/gh-workflows). Reusable GitHub Actions workflows

### Copied from cursor/plugins, adjusted for editor-agnostic use

- [bro](./bro/SKILL.md). Restate the last message in plain language (as-is)
- [code-teach](./code-teach/SKILL.md). Explain a body of work, cursor's `teach` renamed (as-is)
- [how](./how/SKILL.md). Explain how a subsystem works (edited: Cursor-specific wording normalized)
- [unslop](./unslop/SKILL.md). Remove AI tells from writing (as-is)
- [why](./why/SKILL.md). Explain why a change (edited: Cursor-specific wording normalized)

### From other authors, installed from their repos

- [mattpocock/skills](https://github.com/mattpocock/skills)
  - diagnosing-bugs
  - grill-me
  - grill-with-docs
  - grilling
  - handoff
  - prototype
  - teach
  - to-prd
  - to-spec
  - wayfinder
- [obra/superpowers](https://github.com/obra/superpowers)
  - brainstorming
  - dispatching-parallel-agents
  - executing-plans
  - receiving-code-review
  - requesting-code-review
  - subagent-driven-development
  - systematic-debugging
  - test-driven-development
  - verification-before-completion
  - writing-plans
  - writing-skills
- [emilkowalski/skills](https://github.com/emilkowalski/skills)
  - apple-design
- [vercel-labs/skills](https://github.com/vercel-labs/skills)
  - find-skills
- [trycua/cua](https://github.com/trycua/cua)
  - cua-driver
- [modem-dev/hunk](https://github.com/modem-dev/hunk)
  - hunk-review

Each skill folder includes a `README.md` with human-facing use cases. `SKILL.md`
stays focused on instructions that agents should load at runtime.

## License

MIT
