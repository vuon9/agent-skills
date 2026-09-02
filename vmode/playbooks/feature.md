### Feature

**You own the design. Plan, review, verify.** Delegate implementation to subagents or execute in-process; stay in the lead.

Use when building or adding new behavior.

1. **Clarify requirements and design first.**
   Requirements clear? Open `brainstorming` and drive it to a concrete design.
   Scope foggy or spans multiple sessions? Open `wayfinder` and resolve the tickets before coding.
2. **Design before code.**
   Name the data shape and boundary first. Model the domain with clear state structures rather than scattered conditionals.
3. **Throughput checkpoint.**
   Before implementation, write the throughput checkpoint as four items:
   - **Blocking first steps.** Gates and foundation work that must complete before any parallel slices.
   - **Independent workstreams.** Work that can proceed concurrently without overlapping write targets.
   - **Shared mutable state.** Boundaries where concurrent writes would collide. Separate targets first.
   - **Smallest safe decomposition.** The minimal safe chunking for this task.
4. **Implementation and delegation.**
   For scoped units, use `test-driven-development`.
   When delegating to a subagent, provide:
   - Clear scope and exact target paths.
   - Named data shape and boundary invariants.
   - Verification command or criteria.
   - Capability role brief (`mechanical` for precise edits, `reasoning` for architectural balance).
   Review the resulting diff yourself; do not pass through subagent claims unverified.
5. **Prove the behavior.**
   For user-facing features, run behavior/feature tests. Prove it against the real artifact, not just "it compiles".
   <!-- EDIT: behavior-test --> Replace this line with your behavior-test command or approach.
6. **Local review.**
   Run `hunk-review` on the local diff before opening a PR. Check adherence to comments and prose rules.
