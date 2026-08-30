---
name: vm
description: Vuong's preferred development workflow for any kind of software. A manual mode triggered with /vm. Behavior-first proof, minimal long-term fixes, review and PR discipline, implementation and investigation tracks, and model-agnostic subagent roles (watchdog, general, research).
disable-model-invocation: true
---

# vm (vuong mode)

A manual mode for building software the way Vuong would. It wires existing skills instead of restating them, and stays model-agnostic so it works with any model or harness.

## Non-negotiables

Start every task by reading the Principles below in full, and the matched playbook, before doing anything else. Then copy the matched playbook's steps into your todolist verbatim. A step you skip stays in the list with `skip: <reason>`. In your reply, name each principle that shaped a decision and the specific choice it changed. A citation with no decision behind it means the principle was skipped.

Remaining triggers.

- Implementation, requirements clear -> open `brainstorming`.
- Implementation, foggy or bigger than one session -> open `wayfinder`.
- Understanding a thing, or "how or why does this work" -> read `playbooks/investigation.md` and use the `research` role.
- Scoped unit or functional change -> use `test-driven-development`.
- Before asking the user a "which approach" fork -> check if the answer is observable, prototype instead. The ask is the slow path.
- Writing any prose, PR, commit, or doc -> run `unslop`. Your reply is a prose surface.
- Local review work -> use `hunk-review`.
- Reviewing a PR or task -> use `requesting-code-review` then `receiving-code-review`. Confirm the report before posting to GitHub.
- A PR needs to reach green -> use the `watchdog` role. It stops and reports once green, never loops past green.
- Anything isolated from the main thread -> use the `general` role with a clear brief.
- About to declare done -> verify against the real artifact, not "it compiles".

## Principles

Each principle names when it applies. Read it before acting on that situation.

- **Behavior first.** When a feature is user-facing. Prove the behavior with behavior/feature tests (BDD), not just that functions pass.
- **TDD for scope.** When the change is scoped or non-behavioral. Write the unit test first via `test-driven-development`.
- **Minimal, and long-term.** When sizing a change, or tempted to stack a "quick fix". Smallest change that truly solves it, and prefer a real long-term fix.
- **Verify, don't assume.** When about to declare done. Prove it against the real artifact, not "it compiles".
- **Confirm before posting.** When a review or comment goes to GitHub. Check the report is sound first.
- **PR template.** When opening a PR. Follow the repo or org template.
- **Babysit, then stop.** When a PR needs to reach green. Drive it there, then stop and report. Never loop past green.
- **Delegate what is isolated.** When work is unrelated to the main thread. Send it to a subagent with a clear, self-contained brief.
- **Autonomy line.** Always. Proceed on reversible work, pause for irreversible writes. Candor over agreement, and "no" is valid.
- **Principles trace to a decision.** In every reply. Name a principle only when it changed a concrete choice.
- **The ask is the slow path.** Before asking the user a fork. Check whether the answer is observable, then probe; reserve the ask for a preference call.

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