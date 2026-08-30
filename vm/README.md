# vm (vuong mode)

A manual development-workflow mode that encodes Vuong's preferred way of
building software. Model-agnostic and stack-agnostic.

## How to use

1. **Trigger it.** Type `/vm` (or `/skill:vm`) in your agent. It is manual; it
   never auto-applies.
2. **Let it check readiness.** vm verifies its required skills are installed.
   If any is missing, it routes to `install-vm-skills --required` first.
3. **Read, then route.** vm reads its Principles, matches your task to a
   playbook, and copies the playbook's steps into the todolist verbatim.
4. **Pick a playbook.**
   - **Implementation.** Building or changing behavior. Clear requirements go
     through `brainstorming`; foggy or bigger-than-one-session work goes
     through `wayfinder`.
   - **Investigation.** Understanding a thing, or answering "how or why does
     this work". Uses the `research` role and ends in a cited answer or a
     proposed fix.
5. **Delegate what is isolated.** Anything unrelated to the main thread goes to
   a subagent role: `watchdog` (drive a PR to green), `general` (clear brief,
   let it do its best), or `research` (build the picture).

## Roles

- **watchdog** drives a PR to green, then stops and reports.
- **general** handles isolated work with a clear brief.
- **research** builds the picture and returns a cited report.

Full details, including when to use each and what to ask, live in
`references/roles.md`.

## Install and update

- Install everything, or just what vm needs:
  `python3 install-vm-skills/scripts/install.py --all` or `--required`.
- Refresh installed skills to their latest: `npx skills update -g`.

## Making it yours

Fork the repo and edit only the two marked spots.

- The behavior-test step in `playbooks/implementation.md`.
- The PR template reference in `references/roles.md`.

Everything else is style, not stack.