# Design spec: `vstack` mode

Date: 2026-08-30
Status: Approved for review

## 1. Purpose

`vstack` is a manual, model-agnostic "mode" skill that encodes Vuong's preferred way
of working across any kind of software. It is not tied to a specific agent,
editor, or set of model names. The goal is a small forkable surface: another
person can copy the repo, change a handful of clearly-marked spots, and have a
working version of their own.

## 2. Core decisions

- **Trigger:** manual. Use `disable-model-invocation: true` so the skill stays
  out of the model's auto-invocation; the user calls it via `/skill:vstack`. No
  always-on mode, no auto-reminder.
- **Model-agnostic:** the skill never names a model. Roles describe a *job*;
  the model is whatever the harness (or the user) provides. Let each model do
  its best for its conditions.
- **No config file.** Dropped in favor of a short "Adapt me" section inside
  `SKILL.md`. Fewer moving parts beats a `vstack.yaml`.
- **Modular files.** `SKILL.md` is a concise overview; deeper content lives in
  `playbooks/` (workflows) and `references/` (role detail). Thin index, fat
  leaves; reference leaves by name, never inline them.
- **Extendable, not generic.** New stacks, tools, or languages are handled by
  editing the "Adapt me" spots or adding a small playbook, not by a plugin
  system.

## 3. File layout

```
vstack/
├── SKILL.md                      # trigger, principles, work model, routing, roles summary, "Adapt me"
├── playbooks/
│   ├── implementation.md         # clear reqs → brainstorm; foggy/big → wayfinder; else clarify
│   └── investigation.md          # understand → clues → picture → confirm → confidence loop → propose fix
└── references/
    └── roles.md                  # watchdog / general / research, model-agnostic and reusable
```

## 4. `SKILL.md`

The identity file. Its sections, in order:

1. **Frontmatter** with `name: vstack`, a description that hooks `/vstack`, and
   `disable-model-invocation: true` (manual trigger only).
2. **What vstack is**, one or two sentences.
3. **Principles**, the non-negotiables (below).
4. **Work model**, the two tracks and their entry points, pointing at the
   playbooks.
5. **Routing**, a short "situation → do this" table.
6. **Roles**, one line each for watchdog / general / research, pointing at
   `references/roles.md`.
7. **Adapt me**, the marked spots to edit for a fork.

### Principles

- **Behavior first.** For user-facing features, prove the behavior with
  behavior/feature tests (BDD). Unit/functional tests via TDD apply to scoped,
  non-behavioral work. This maps to the superpowers
  `test-driven-development` skill where relevant.
- **Minimal, and long-term.** Smallest change that truly solves the problem;
  prefer a real long-term fix over stacking "just another short fix". Lazy and
  simple, but root-cause.
- **Verify, don't assume.** Prove work is done against the real artifact, not
  "it compiles". A review report must be sound and confirmed before anything
  is posted to GitHub.
- **PR body follows the repo/org template.** Always.
- **Babysit, then stop.** Drive the PR to green, then stop and emit a report.
  Never keep looping past green.
- **Delegate what's isolated.** Anything unrelated to the main thread goes to a
  subagent with a clear, self-contained brief. Let it do its best.
- **Autonomy line.** Proceed on reversible work; pause for irreversible writes
  (force-push to shared branches, deploys, data deletion, external messages).
  Candor over agreement; "no" is a valid answer.
- **Principles must trace to a decision.** Name a principle only when it
  changed a concrete choice. A citation with no decision behind it means the
  principle was skipped.
- **Read before you reason.** When `/vstack` fires, read the Principles in full and
  the matched playbook before reasoning about the task. No silent assumptions.
- **The ask is the slow path.** Before asking the user a "which approach" or
  "what should this do" fork, check if the answer is observable. Sketch or run
  a cheap probe and let the result decide. Reserve the ask for a genuine
  preference call no experiment can settle.

Nice-to-have: when a repeating pattern appears, suggest distilling it into a
skill, and ask the harness user before doing so.

### Work model + routing

| Situation | Route |
| ----------- | ------- |
| Implementation, requirements clear | `playbooks/implementation.md` and brainstorming |
| Implementation, foggy or too big for one session | `playbooks/implementation.md` and wayfinder |
| Investigation / understand a thing | `playbooks/investigation.md` and the research role |
| PR needs driving to green | watchdog role |
| Unrelated / isolated work | general role |
| PR/task review | request/receive code review, confirm before posting |

Playbook steps are copied verbatim into the todolist before any task reasoning.
A step chosen to skip stays in the list with a one-line `skip: reason`; skipping
silently is not allowed.

## 5. `playbooks/implementation.md`

- Requirements clear: open brainstorming and run it to a design.
- Foggy or larger than one session: open wayfinder (issue-tracker map of
  decision tickets) and resolve tickets until the route is clear.
- Otherwise: clarify with the user until requirements are clear enough to start.

## 6. `playbooks/investigation.md`

The loop for understanding/checks, with the research role:

1. Understand the context.
2. Find clues.
3. Think bigger: form the picture.
4. Confirm ambiguities.
5. Check confidence; loop until it is enough.
6. Propose the fix (or a cited answer).

## 7. `references/roles.md`

Three model-agnostic, reusable capabilities. No model names, no fixed
one-role-one-task silo. Each entry answers: when to use it, what to ask, and
what it returns.

- **watchdog**: takes a PR to green. Polls status, resolves conflicts, addresses
  comments, then stops with a final report. Never loops past green.
- **general**: a flexible, do-your-best subagent for isolated work. The caller
  writes a clear, self-contained brief; the role runs it without extra forcing.
- **research**: builds a picture for an investigation or understanding question.
  Context, clues, a formed view, open ambiguities, and a confidence read,
  returned as a cited report.

## 8. Extendability model

A fork adapts by editing the "Adapt me" spots in `SKILL.md` (and, rarely,
adding a playbook). Expected edit points:

- project/tool preference (e.g. the behavior-test command or approach)
- PR template reference (repo/org)
- any stack-specific step in the playbooks

No config, no plugins, no model names to change.

## 9. Non-goals

- No model names or per-role model config.
- No `vstack.yaml` config file.
- No auto-reminder / always-on mode.
- No Cursor-specific machinery (`subagent_type`, MCP, `cursor-team-kit`).
- No huge principle taxonomy or a `scripts/` directory (add later only if a
  real need appears).
