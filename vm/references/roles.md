# Roles

Three model-agnostic capabilities. Reusable, not one-role-one-task. Each runs on whatever model the harness gives you.

## watchdog

- **When.** A PR must reach green, or the user asks to babysit a PR.
- **Ask.** Drive it to green. Poll status, resolve conflicts, address review comments, then stop and report.
- **Returns.** A final report once green. It never loops past green.
- The PR body follows the repo or org PR template.
<!-- EDIT: pr-template --> Replace this with the repo or org PR template reference.

## general

- **When.** Isolated or unrelated work that can leave the main thread.
- **Ask.** Give a clear, self-contained brief. Let it do its best.
- **Returns.** The result plus a short summary. The main thread keeps the picture.

## research

- **When.** An investigation or understanding question.
- **Ask.** Gather context, find clues, form the picture, flag ambiguities, and state confidence.
- **Returns.** A cited report. No fabrication. Link only what was actually read.