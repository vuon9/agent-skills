# Wails Fullstack

Use this skill when an agent is building or maintaining a Wails v3 desktop app
with a Go backend and web frontend.

## Good Use Cases

- Add a frontend-only, backend-only, or full-stack feature to a Wails app.
- Keep domain logic in Go packages while exposing thin Wails service bindings.
- Run Wails development checks such as `wails3 doctor`, local dev mode, Go
  tests, and package verification.
- Decide which behavior must be tested in desktop mode instead of only in a
  browser.
- Keep Wails-specific build steps in the app repository while shared signing and
  notarization stay in release workflows.

## Not For

- Generic web apps that do not use Wails.
- Developer ID signing and notarization details; use `macos-release`.
- Browser automation tooling recommendations.
