"""Turn a raw replay log into per-turn (battle state, chosen action) pairs.

A replay log is the Showdown protocol stream as a spectator saw it: ``|switch|``,
``|move|``, ``|-damage|`` and so on. To imitate a player we need the state *they* saw
when they chose, which means:

  * tracking their own six Pokémon fully (the spectator log reveals them only as they
    appear, so some early-turn information must be back-filled from later turns);
  * tracking the opponent's team as it was revealed up to that turn, and nothing more;
  * recovering the action from the next turn's events (a ``|move|`` or ``|switch|`` by
    that player), including forced switches after a faint.

poke-env's ``Battle`` object already parses protocol lines and tracks revealed
information for the connected player. Reusing it for one side of a replay is the
shortest path to one state encoder shared with the Player.

TODO(ghosts): implement ``parse_replay``.
  1. Split the log into turns; feed lines through a ``Battle`` for the chosen side.
  2. At each decision point emit ``(observation, action)`` using the Player's encoder
     (``battle_trainer.player.encoder``) and poke-env's action indices
     (``SinglesEnv.order_to_action``) so ghosts and the Player share one action space.
  3. Validate on a handful of hand-checked replays before scaling up.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any


def parse_replay(log_path: Path, side: str = "p1") -> Iterator[tuple[Any, int]]:
    """Yield ``(observation, action)`` pairs for ``side`` of one replay. Not implemented."""
    raise NotImplementedError("TODO(ghosts): see module docstring")
