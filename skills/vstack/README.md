# vstack

A manual development-workflow mode that encodes Vuong's preferred way of
building software. Model-agnostic and stack-agnostic.

## Use it with a prompt

Say what you want in plain words. Prompts come first; the scripts below are
only the fallback.

- "Work in vstack mode" -> activates `/vstack`. vstack checks its required skills; if
  any is missing, it runs `setup-vstack --required`.
- "How does the auth flow work?" -> investigation playbook with the `research`
  role. Returns a cited answer, not a summary.
- "Why was this table added?" -> investigation. Ends in a cited answer or a
  proposed fix.
- "Build the export feature" -> implementation playbook. Clear scope goes
  through `brainstorming`; foggy or big scope goes through `wayfinder`.
- "Babysit PR #123 until it's green" -> the `watchdog` role. It drives the PR
  to green, then stops and reports.
- "Handle this small thing separately" -> the `general` role with a clear,
  self-contained brief.

## What happens on /vstack

1. vstack checks its required skills. Missing one? It runs
   `setup-vstack --required` first.
2. It reads the Principles in full, then the matched playbook.
3. It copies the playbook steps into the todolist verbatim. A skipped step
   stays with `skip: <reason>`.

## Roles

- **watchdog** drives a PR to green, then stops and reports.
- **general** handles isolated work with a clear brief.
- **research** builds the picture and returns a cited report.

Full details live in `references/roles.md`.

## Why the rules live in two layers

vstack follows poteto-mode's shape: triggers and principles.

- **Triggers** (Non-negotiables) are moment-of-recognition routing. The agent
  scans them while working; the moment a situation appears, the matching line
  fires.
- **Principles** are read-first grounding. The opener forces the agent to read
  them in full at the start, and the reply rule says to name each principle
  that shaped a decision. A rule must exist as a principle, or the citation
  rule can't reference it.

That's why a rule like "keep generated docs local" appears twice: once as a
trigger (fires at the moment) and once as a principle (the standing rule read
up front and cited). If you change such a rule, edit both places.

## Scripts (additional)

Only needed when you want the underlying commands directly.

- `python3 skills/setup-vstack/scripts/install.py --all` installs everything.
- `python3 skills/setup-vstack/scripts/install.py --required` installs just what
  vstack needs.
- `npx skills update -g` refreshes installed skills to latest.

## Making it yours

Fork the repo and edit only the two marked spots.

- The behavior-test step in `playbooks/implementation.md`.
- The PR template reference in `references/roles.md`.

Everything else is style, not stack.
