---
name: rodney
description: Use when navigating web pages, filling forms, extracting data, making assertions, or automating browser interactions via command line. Triggers on web scraping, form submission, page screenshots, element waits, checking visibility/presence, and JavaScript evaluation in Chrome.
---

# rodney

A CLI for Chrome automation using the rod library. Each command connects to a persistent headless Chrome instance - start once, run multiple commands, stop when done.

## Prerequisites

⚠️ **STOP if prerequisites are missing.**

Verify Go is installed:

```bash
go version
```

If Go is not installed, install it from https://go.dev/dl/ before proceeding.

---

**Install Rodney:**

```bash
go install github.com/simonw/rodney@latest
```

This installs rodney to `$HOME/go/bin/`. Ensure it's in your PATH:

```bash
export PATH="$HOME/go/bin:$PATH"
```

Or download pre-built binaries from: https://github.com/simonw/rodney/releases

---

**Verify installation:**

```bash
rodney version
```

Do not proceed with any rodney commands until verified.

## When to Use

- Opening URLs and navigating (back, forward, reload)
- Filling forms, clicking buttons, interacting with elements
- Extracting text, HTML, attributes from pages
- Waitingfor elements or page stability
- Making assertions for testing (exists, visible, equality)
- Taking screenshots
- Running JavaScript in browser context

## Quick Start

| Command | Description |
|---------|-------------|
| `rodney start` | Launch headless Chrome |
| `rodney start --show` | Launch with visible window |
| `rodney stop` | Shut down Chrome |
| `rodney status` | Show browser info |

```bash
rodney start
rodney open https://example.com
rodney title
rodney stop
```

## Navigate

| Command | Description |
|---------|-------------|
| `rodney open <url>` | Navigate to URL |
| `rodney back` | Go back in history |
| `rodney forward` | Go forward |
| `rodney reload` | Reload page |
| `rodney reload --hard` | Reload bypassing cache |
| `rodney clear-cache` | Clear browser cache |

## Interact

| Command | Description |
|---------|-------------|
| `rodney click <selector>` | Click element |
| `rodney input <selector> <text>` | Type into input field |
| `rodney clear <selector>` | Clear input field |
| `rodney file <selector> <path>` | Set file on file input |
| `rodney select <selector> <value>` | Select dropdown option |
| `rodney submit <selector>` | Submit form |
| `rodney hover <selector>` | Hover over element |
| `rodney focus <selector>` | Focus element |

## Extract

| Command | Description |
|---------|-------------|
| `rodney url` | Print current URL |
| `rodney title` | Print page title |
| `rodney html [selector]` | Print HTML (page or element) |
| `rodney text <selector>` | Print element text content |
| `rodney attr <selector> <name>` | Print attribute value |
| `rodney js <expression>` | Evaluate JavaScript |

```bash
rodney js 'document.querySelector("h1").textContent'
rodney js '[1,2,3].map(x => x * 2)'  # Returns pretty-printed JSON
```

## Wait

| Command | Description |
|---------|-------------|
| `rodney wait <selector>` | Wait for element to appear and be visible |
| `rodney waitload` | Wait for page load event |
| `rodney waitstable` | Wait forDOM to stop changing |
| `rodney waitidle` | Wait for network to be idle |
| `rodney sleep <seconds>` | Sleep for N seconds |

Use `waitstable` for dynamic pages, `waitidle` for AJAX-heavy sites.

## Check

| Command | Description |
|---------|-------------|
| `rodney exists <selector>` | Exit 0 if exists, 1 if not |
| `rodney visible <selector>` | Exit 0 if visible, 1 if not |
| `rodney count <selector>` | Print number of matching elements |
| `rodney assert <expr> [expected]` | Exit 0 if truthy/equal, 1 if not |

```bash
# Truthy check
rodney assert 'document.querySelector(".loaded")'

# Equality check
rodney assert 'document.title' 'Expected Title'

# With custom message
rodney assert '.logged-in' -m "User should be logged in"
```

## Screenshots

| Command | Description |
|---------|-------------|
| `rodney screenshot [file]` | Save page screenshot |
| `rodney screenshot -w 1280 -h 720 out.png` | With viewport size |
| `rodney screenshot-el <selector> [file]` | Screenshot specific element |

## Tabs

| Command | Description |
|---------|-------------|
| `rodney pages` | List all tabs (* marks active) |
| `rodney page <index>` | Switch to tab by index |
| `rodney newpage [url]` | Open new tab |
| `rodney closepage [index]` | Close tab |

## Debug Workflow

When something isn't working:

1. **Check current state** - `rodney url`, `rodney title`
2. **Inspect DOM** - `rodney html`, `rodney html "selector"`, `rodney text "selector"`
3. **Visual check** - `rodney screenshot`
4. **Timing issues** - `rodney wait ".element"`, `rodney waitstable`

## Not Yet Supported

*Last checked: Rodney v0.4.0*

Rodney doesn't yet support these go-rod features:

- **Special keyboard keys** (Enter, Tab, Escape, Arrow keys) - `rodney input` only types text
- **iframe targeting** - Cannot target elements inside iframes
- **Console log capture** - Cannot capture browser console output
- **Network request logging** - Cannot list network requests
- **Shadow DOM targeting** - Cannot target elements inside shadow DOM
- **Dialog handling** - Cannot accept/dismiss alert/confirm dialogs
- **Request interception** - Cannot block/modify network requests
- **Cookie management** - Cannot get/set cookies directly
- **Local storage** - Cannot get/set localStorage

## Advanced

For accessibility tree commands (`ax-tree`, `ax-find`, `ax-node`), PDF output, proxy configuration, and `--local` sessions:

```bash
rodney --help
```

## Common Patterns

**Scrape data from page:**
```bash
rodney start
rodney open https://example.com
rodney waitstable
title=$(rodney title)
content=$(rodney text "article")
rodney stop
```

**Fill and submit form:**
```bash
rodney start
rodney open https://example.com/login
rodney input "#email" "user@example.com"
rodney input "#password" "secret"
rodney click "button[type=submit]"
rodney wait ".dashboard"
rodney stop
```

**Run assertions in CI:**
```bash
rodney start
rodney open https://example.com
rodney waitstable
rodney exists "h1" || exit 1
rodney visible "#main-content" || exit 1
rodney assert 'document.title' 'Home' || exit 1
rodney stop
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Check failed (condition not met) |
| 2 | Error (bad args, no browser, timeout) |