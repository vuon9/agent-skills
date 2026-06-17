# macOS Release

Use this skill when an agent needs to sign, notarize, staple, package, or
release a macOS app distributed outside the Mac App Store.

## Good Use Cases

- Prepare Developer ID Application signing and notarization credentials.
- Verify a `.app` or `.dmg` with `codesign`, `notarytool`, `stapler`, and
  Gatekeeper assessment.
- Create a thin caller workflow that uploads a built `.app` archive and calls a
  reusable macOS release workflow.
- Troubleshoot missing private keys, locked keychains, notarization rejection,
  nested unsigned code, or DMG assessment confusion.
- Report release evidence without leaking certificates, keys, or notarization
  credentials.

## Not For

- Mac App Store uploads.
- App-specific build logic such as Wails, Electron, or Xcode packaging commands.
- iOS TestFlight release automation.
