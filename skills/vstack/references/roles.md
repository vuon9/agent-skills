# Roles

Three model-agnostic capabilities. Reusable, not one-role-one-task. Each runs on whatever model the harness gives you.

**You own every subagent's work.** Review the diff. Write your own summary. Don't pass through what the subagent said. Fire a fresh subagent with consolidated scope rather than trusting a "done" summary.

## watchdog

**When.** A PR must reach green, or the user asks to babysit a PR.
**Ask.** Drive it to green. Poll status, resolve conflicts, address review comments, then stop and report. Never loop past green.
The PR body follows the repo or org PR template.
<!-- EDIT: pr-template --> Replace this with the repo or org PR template reference.

## general

**When.** Isolated or unrelated work that can leave the main thread.
**Ask.** Give a clear, self-contained brief. Let it do its best.
**Returns.** The result plus a short summary. The main thread keeps the picture.

## research

**When.** An investigation or understanding question.
**Ask.** Gather context, find clues, form the picture, flag ambiguities, state confidence.
**Returns.** A cited report. No fabrication. Link only what was actually read.