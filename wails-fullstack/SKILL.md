---
name: wails-fullstack
description: Use when building or maintaining Wails v3 desktop applications with a Go backend, web frontend, app packaging, or release workflows.
---

# Wails Fullstack Development

Use this skill for Wails v3 apps. Keep framework-specific build logic in the app repository, keep reusable signing/notarization concerns in release workflows, and verify through Wails before claiming a desktop change is ready.

## Prerequisites

```bash
go version
bun --version
npm --version
wails3 version
wails3 doctor
```

If prerequisites are missing, stop and report the missing tool. Do not install global toolchains unless the user asked you to set up the machine.

## Project Shape

Prefer the app's existing structure. For new or growing apps, keep Wails bindings thin:

- `main.go`: app/window setup and service registration.
- `internal/<feature>/`: domain logic with no Wails dependency.
- `service/<feature>.go`: Wails-facing wrapper around internal packages.
- `frontend/`: UI, routes, state, generated bindings consumption.
- `build/`: Wails build metadata and packaging resources.

## Create New Project

```bash
wails3 init -n myapp -t react-ts
```

After generation, follow the created template first. Add `internal/` and `service/` only when the first real backend feature needs that separation.

## Feature Pattern

For backend-backed features:

1. Put pure Go logic and tests under `internal/<feature>/`.
2. Add a thin Wails service method that validates inputs, calls internal logic, and returns structured results.
3. Register the service in `main.go` using the current Wails v3 registration pattern in the app.
4. Regenerate bindings through the app's existing Wails command.
5. Consume generated bindings from the frontend.

Return explicit error fields or typed errors according to the app's existing convention. Do not panic for user-input failures.

For frontend-only tools, avoid adding Go services. Keep the feature in `frontend/` and use browser tests or component tests already present in the app.

## Development Checks

Use the repository's scripts when present. Otherwise start with:

```bash
go test ./...
wails3 doctor
wails3 dev
```

For packaging or release readiness, run the app's package command and verify the expected `.app` exists:

```bash
find . -name "*.app" -maxdepth 6
codesign --verify --deep --strict --verbose=2 path/to/App.app
```

Test desktop-only behavior in desktop mode: tray menus, native dialogs, global shortcuts, file associations, auto-update hooks, and window lifecycle.

## Release Boundary

- Keep Wails build commands, asset generation, and frontend package-manager choices in the app repository.
- Use a reusable macOS release workflow only after the app job uploads a `.tar.gz` containing the built `.app`.
- Do not move app-specific Wails build assumptions into shared release workflows.

## Common Failures

- Missing service binding: regenerate bindings and verify the service is registered.
- Frontend cannot connect: check the Wails dev server URL and generated bindings path.
- Browser test passes but desktop fails: retest native-only behavior in desktop mode.
- Packaging succeeds but release fails: inspect signing, entitlements, nested code, and hardened runtime separately from Wails.
- Old docs or examples disagree with the installed CLI: prefer `wails3 <command> --help` and the current docs at `https://v3.wails.io/`.
