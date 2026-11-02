"""Headless Showdown (tier 2): drive ``pokemon-showdown simulate-battle`` directly.

Why: through the server every move is a websocket round trip. The headless CLI runs the
same simulator over a subprocess's stdin/stdout, accepts a seed, and needs no server,
so many battles can run in parallel on one laptop.

Protocol sketch (see sim/SIMULATOR.md in the Showdown repo for the full version)::

    >start {"formatid":"gen1randombattle","seed":[1,2,3,4]}
    >player p1 {"name":"Alice"}
    >player p2 {"name":"Bob"}
    >p1 move 1
    >p2 switch 3

The process answers with ``update`` blocks (what both players see), ``sideupdate``
blocks (what one side sees, including the ``|request|`` JSON that lists legal
choices), and ``end`` with the result.

TODO(engine): implement ``HeadlessBattle`` and a batched runner.
  1. Spawn ``node pokemon-showdown simulate-battle`` from ``showdown_dir()``.
  2. Parse ``sideupdate`` ``|request|`` messages into legal-action sets for each side.
  3. Feed the request logs into poke-env's ``Battle`` parser so the Player sees the
     same state here as it does over the websocket (one state encoder, two tiers).
  4. Benchmark battles/second against the server tier and record it in docs/.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SHOWDOWN_DIR = REPO_ROOT / "third_party" / "pokemon-showdown"


def showdown_dir() -> Path:
    """Location of the Showdown checkout made by ``scripts/setup_showdown.sh``."""
    path = DEFAULT_SHOWDOWN_DIR
    if not (path / "pokemon-showdown").exists():
        raise FileNotFoundError(
            f"Pokémon Showdown not found at {path}. Run scripts/setup_showdown.sh first."
        )
    return path


def pinned_showdown_commit() -> str:
    """The Showdown commit every result must be reported against."""
    return (REPO_ROOT / "third_party" / "SHOWDOWN_COMMIT").read_text().strip()


class HeadlessBattle:
    """One battle driven over ``simulate-battle``. Not implemented yet."""

    def __init__(self, battle_format: str, seed: list[int] | None = None) -> None:
        self.battle_format = battle_format
        self.seed = seed
        raise NotImplementedError("TODO(engine): see module docstring")
