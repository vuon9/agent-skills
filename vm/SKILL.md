---
name: vm
description: Vuong's preferred development workflow for any kind of software. A manual mode triggered with /vm. Behavior-first proof, minimal long-term fixes, review and PR discipline, implementation and investigation tracks, and model-agnostic subagent roles (watchdog, general, research).
disable-model-invocation: true
---

# vm (vuong mode)

A manual mode for building software the way Vuong would. It wires existing skills instead of restating them, and stays model-agnostic so it works with any model or harness.

## Start here

When vm is invoked, read the Principles in full first. Then match the task to a playbook and read it in full. Copy the playbook steps into your todolist verbatim before reasoning about the task. A step you skip stays in the list with `skip: <reason>`.

## Principles

Read these before acting. Each one is a non-negotiable.

- **Behavior first.** For user-facing features, prove the behavior with behavior/feature tests (BDD). Unit and functional tests via TDD apply to scoped, non-behavioral work. Use the superpowers `test-driven-development` skill for that part.
- **Minimal, and long-term.** Smallest change that truly solves the problem. Prefer a real long-term fix over stacking "just another short fix". Lazy and simple, but root-cause.
- **Verify, don't assume.** Prove the work is done against the real artifact, not "it compiles". A review report must be sound and confirmed before anything is posted to GitHub.
- **PR body follows the repo or org template.** Always.
- **Babysit, then stop.** Drive the PR to green, then stop and report. Never loop past green.
- **Delegate what is isolated.** Anything unrelated to the main thread goes to a subagent with a clear, self-contained brief. Let it do its best.
- **Autonomy line.** Proceed on reversible work. Pause for irreversible writes, such as force-push to shared branches, deploys, data deletion, and external messages. Candor over agreement; "no" is a valid answer.
- **Principles trace to a decision.** Name a principle only when it changed a concrete choice. A citation with no decision behind it means the principle was skipped.
- **The ask is the slow path.** Before asking the user a "which approach" or "what should this do" fork, check if the answer is observable. Sketch or run a cheap probe and let the result decide. Reserve the ask for a genuine preference call no experiment can settle.

## Work model

Two tracks. Match the task, open the playbook, copy its steps.

| Situation | Route |
|-----------|-------|
| Implementation, requirements clear | `playbooks/implementation.md` and brainstorming |
| Implementation, foggy or bigger than one session | `playbooks/implementation.md` and wayfinder |
| Investigation, or understand a thing | `playbooks/investigation.md` and the research role |
| PR needs driving to green | watchdog role in `references/roles.md` |
| Unrelated or isolated work | general role in `references/roles.md` |
| PR or task review | request and receive code review, confirm before posting |

## Roles

Three model-agnostic capabilities. Read `references/roles.md` for when to use each and what to ask.

- **watchdog** drives a PR to green, then stops with a report.
- **general** handles isolated work with a clear brief.
- **research** builds the picture for an investigation and returns a cited report.

## Adapt me

Edit only these spots to fit your stack and tools. Everything else is style, not stack.

- The behavior-test step in `playbooks/implementation.md`. Marker `<!-- EDIT: behavior-test -->`.
- The PR template reference in `references/roles.md`. Marker `<!-- EDIT: pr-template -->`.
- The description above, to name the person or project.