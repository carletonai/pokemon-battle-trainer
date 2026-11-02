#!/usr/bin/env bash
# Clone and build Pokémon Showdown at the pinned commit in third_party/SHOWDOWN_COMMIT.
#
# Usage:  scripts/setup_showdown.sh
#
# Requires Node >= 22.18 (https://nodejs.org). Safe to re-run: an existing clean checkout
# is moved to the pinned commit and rebuilt. If you have edited files inside the checkout,
# stash or discard them first (or set SHOWDOWN_FORCE=1 to throw them away).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SHOWDOWN_DIR="${SHOWDOWN_DIR:-$REPO_ROOT/third_party/pokemon-showdown}"
SHOWDOWN_REPO="${SHOWDOWN_REPO:-https://github.com/smogon/pokemon-showdown.git}"
SHOWDOWN_COMMIT="$(tr -d '[:space:]' < "$REPO_ROOT/third_party/SHOWDOWN_COMMIT")"

if ! command -v node >/dev/null 2>&1; then
  echo "error: node not found. Install Node >= 22.18 from https://nodejs.org and re-run." >&2
  exit 1
fi

NODE_MIN="22.18.0"
NODE_VERSION="$(node -p 'process.versions.node')"
if [ "$(printf '%s\n' "$NODE_MIN" "$NODE_VERSION" | sort -V | head -n1)" != "$NODE_MIN" ]; then
  echo "error: Node >= $NODE_MIN required, found $(node --version)." >&2
  exit 1
fi

echo "==> Pokémon Showdown @ $SHOWDOWN_COMMIT -> $SHOWDOWN_DIR"
if [ ! -d "$SHOWDOWN_DIR/.git" ]; then
  mkdir -p "$SHOWDOWN_DIR"
  git -C "$SHOWDOWN_DIR" init -q
  git -C "$SHOWDOWN_DIR" remote add origin "$SHOWDOWN_REPO"
fi
# A shallow fetch of just the pinned commit keeps the download small.
git -C "$SHOWDOWN_DIR" fetch -q --depth 1 origin "$SHOWDOWN_COMMIT"
if ! git -C "$SHOWDOWN_DIR" checkout -q --detach ${SHOWDOWN_FORCE:+--force} FETCH_HEAD; then
  echo "error: could not move $SHOWDOWN_DIR to $SHOWDOWN_COMMIT." >&2
  echo "       You probably have local edits there. Stash or discard them, or re-run with SHOWDOWN_FORCE=1." >&2
  exit 1
fi

echo "==> npm ci (dependencies from Showdown's lockfile; a few minutes the first time)"
(cd "$SHOWDOWN_DIR" && npm ci --no-audit --no-fund)

echo "==> node build (compiles the simulator so the first server start is quick)"
(cd "$SHOWDOWN_DIR" && node build)

if [ ! -f "$SHOWDOWN_DIR/config/config.js" ]; then
  cp "$SHOWDOWN_DIR/config/config-example.js" "$SHOWDOWN_DIR/config/config.js"
  echo "==> wrote config/config.js from config-example.js"
fi

echo "==> done. Start a local server with: scripts/start_showdown.sh"
