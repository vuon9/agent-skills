#!/usr/bin/env bash
#
# Refresh all installed git-sourced skills to their latest published versions.
#
set -euo pipefail

exec npx -y skills update -g
