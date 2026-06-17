# iOS TestFlight Release

Use this skill when an agent needs to set up, migrate, or run an iOS TestFlight
upload through GitHub Actions and App Store Connect API credentials.

## Good Use Cases

- Add a thin app-repo workflow wrapper around `ios-testflight.yml`.
- Verify required App Store Connect secrets without exposing secret values.
- Choose dry-run, export-only, upload, manual signing, or automatic signing
  paths.
- Bump build numbers and gather evidence from local tests, dry-runs, and real
  upload logs.
- Troubleshoot duplicate build numbers, SDK rejections, missing credentials, or
  reusable workflow checkout issues.

## Not For

- Public App Store release approval.
- General Xcode project readiness; use `apple-platform-readiness`.
- macOS Developer ID distribution; use `macos-release`.
