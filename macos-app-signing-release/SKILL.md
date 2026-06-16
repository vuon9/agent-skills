---
name: macos-app-signing-release
description: Use when signing, notarizing, packaging, or releasing macOS apps with Developer ID and GitHub Actions.
---

# macOS App Signing Release

Use this for macOS desktop apps distributed outside the Mac App Store, especially when CI builds a `.app`, packages a `.dmg`, signs with Developer ID, notarizes with Apple, and verifies Gatekeeper acceptance.

For general Xcode, Apple account, or App Store Connect setup, use `apple-development`. For reusable `workflow_call` design, use `github-reusable-workflows`.

## Guardrails

- Never print certificate passwords, app-specific passwords, API keys, base64 certificate payloads, private keys, temporary keychain passwords, or notarization credentials.
- Do not commit `.p12` files, certificates, private keys, provisioning profiles, exported app bundles, DMGs, or notarization logs containing sensitive paths.
- Ask before changing Apple Developer account settings, revoking certificates, rotating secrets, publishing releases, or deleting release assets.
- If the matching private key is missing, stop. A downloaded Developer ID certificate alone cannot produce a usable signing identity.

## Inputs

Collect these without exposing secrets:

- Apple Developer Team ID.
- Developer ID Application identity or exported `.p12` with matching private key.
- Notarization auth: App Store Connect API key or Apple ID app-specific password.
- Bundle identifier, app display name, and hardened runtime or entitlement needs.
- Artifact target: `.app`, `.zip`, `.dmg`, or a combination.
- Release mode: branch artifact, draft release, tag release, or manual upload.

## Certificate Prep

Inspect local signing identities:

```bash
security find-identity -v -p codesigning
```

Confirm the expected identity is `Developer ID Application: ...` and has a matching private key in Keychain Access. Export a password-protected `.p12`, then base64 encode it for CI:

```bash
base64 -i DeveloperIDApplication.p12 | pbcopy
```

Use a strong random export password and store it separately from the encoded certificate.

## GitHub Secrets

Use consistent secret names in app repositories and reusable workflows:

- `APPLE_DEVELOPER_ID_APPLICATION_CERTIFICATE_P12_BASE64`
- `APPLE_DEVELOPER_ID_APPLICATION_CERTIFICATE_PASSWORD`
- `APPLE_TEAM_ID`
- `APPLE_BUNDLE_ID`
- `APPLE_ID` and `APPLE_APP_SPECIFIC_PASSWORD`, if using Apple ID auth.
- `APPLE_API_KEY_ID`, `APPLE_API_ISSUER_ID`, and `APPLE_API_PRIVATE_KEY`, if using App Store Connect API auth.

Prefer App Store Connect API keys for automation when the workflow supports them.

## CI Keychain Pattern

Create a temporary keychain, import the `.p12`, unlock it, restrict key access, and clean it up at the end of the job.

```bash
CERT_PATH="$RUNNER_TEMP/developer-id.p12"
KEYCHAIN_PATH="$RUNNER_TEMP/app-signing.keychain-db"

echo "$APPLE_DEVELOPER_ID_APPLICATION_CERTIFICATE_P12_BASE64" | base64 --decode > "$CERT_PATH"
security create-keychain -p "$KEYCHAIN_PASSWORD" "$KEYCHAIN_PATH"
security set-keychain-settings -lut 21600 "$KEYCHAIN_PATH"
security unlock-keychain -p "$KEYCHAIN_PASSWORD" "$KEYCHAIN_PATH"
security import "$CERT_PATH" -P "$APPLE_DEVELOPER_ID_APPLICATION_CERTIFICATE_PASSWORD" -A -t cert -f pkcs12 -k "$KEYCHAIN_PATH"
security list-keychain -d user -s "$KEYCHAIN_PATH"
security set-key-partition-list -S apple-tool:,apple:,codesign: -s -k "$KEYCHAIN_PASSWORD" "$KEYCHAIN_PATH"
security find-identity -v -p codesigning "$KEYCHAIN_PATH"
```

## Signing Checks

After building the app bundle:

```bash
codesign --force --deep --options runtime --timestamp \
  --sign "Developer ID Application: Example Team (TEAMID1234)" \
  path/to/App.app

codesign --verify --deep --strict --verbose=2 path/to/App.app
spctl --assess --type execute --verbose=4 path/to/App.app
```

Sign nested helpers, frameworks, login items, and extensions according to the app's packaging tool requirements. Do not rely on `--deep` as a substitute for fixing an incorrect bundle signing order.

## Notarization

Use `xcrun notarytool`, not legacy `altool`:

```bash
xcrun notarytool submit path/to/App.dmg \
  --apple-id "$APPLE_ID" \
  --team-id "$APPLE_TEAM_ID" \
  --password "$APPLE_APP_SPECIFIC_PASSWORD" \
  --wait

xcrun stapler staple path/to/App.dmg
xcrun stapler validate path/to/App.dmg
```

For API key auth, use the repository's supported `notarytool` API key flags or a stored notarytool profile.

## Gatekeeper Verification

Assess the app bundle:

```bash
spctl --assess --type execute --verbose=4 path/to/App.app
```

For signed DMGs, verify the primary signature context instead of treating `--type install` failures as definitive:

```bash
spctl --assess --type open --context context:primary-signature --verbose=4 path/to/App.dmg
```

When practical, test the user path: mount the DMG, copy the app to `/Applications`, and assess or launch the copied app on a clean macOS environment.

## GitHub Actions Notes

- Pin third-party actions and tools to stable versions. For `go-task`, use a known-good version such as `v3.49.0` unless the repo intentionally moves forward.
- Separate branch artifact runs from tag release runs. A branch run can prove sign/notarize is green while release asset upload is skipped because there is no tag.
- Upload signed and notarized artifacts on manual branch runs so they can be inspected before tagging.
- Keep reusable workflow inputs small: app name, bundle id, artifact paths, certificate secret names, and release mode.

## Troubleshooting

- `no identity found`: the `.p12` may not include the private key, or CI imported it into the wrong keychain.
- `User interaction is not allowed`: unlock the keychain and run `security set-key-partition-list`.
- `The specified item could not be found in the keychain`: confirm the signing command sees the same keychain used for import.
- Notarization rejected: fetch the notary log and inspect hardened runtime, unsigned nested code, entitlements, invalid bundle IDs, or embedded archives.
- DMG `spctl` mismatch: verify both the `.app` and DMG with the correct assessment type and context.
- Release upload skipped: check whether the workflow is running on a tag and whether publishing is gated by `github.ref_type == 'tag'`.

## Completion Checklist

Before reporting the release pipeline ready:

1. GitHub Actions run completed successfully.
2. `codesign` verification passed for the app bundle.
3. Notarization completed and stapling validation passed.
4. DMG Gatekeeper assessment used `context:primary-signature` when applicable.
5. The artifact exists, with branch artifact versus tag release asset clearly stated.
6. The report includes the workflow run URL and artifact name without revealing secrets.
