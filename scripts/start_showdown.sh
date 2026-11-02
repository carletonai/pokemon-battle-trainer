#!/usr/bin/env bash
# Start a local Pokémon Showdown server for bots to connect to.
#
# Usage:  scripts/start_showdown.sh [port]
#
# --no-security turns off rate limits and login requirements, which is what poke-env
# expects from a local training server. Never run a public server with this flag.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SHOWDOWN_DIR="${SHOWDOWN_DIR:-$REPO_ROOT/third_party/pokemon-showdown}"
PORT="${1:-8000}"

if [ ! -f "$SHOWDOWN_DIR/pokemon-showdown" ]; then
  echo "error: Showdown not found at $SHOWDOWN_DIR. Run scripts/setup_showdown.sh first." >&2
  exit 1
fi

# Usage per the launcher: pokemon-showdown start [--skip-build] [PORT]
cd "$SHOWDOWN_DIR"
exec node pokemon-showdown start --no-security "$PORT"
