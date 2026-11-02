"""The built-in baseline bots. These are the first opponents the Player must beat."""

from __future__ import annotations

from typing import Any

from poke_env.player import MaxBasePowerPlayer, Player, RandomPlayer, SimpleHeuristicsPlayer
from poke_env.ps_client import ServerConfiguration

from battle_trainer.config import BATTLE_FORMAT
from battle_trainer.engine.server import local_server

# Name -> poke-env player class. Order is roughly weakest to strongest.
BUILTIN_BOTS: dict[str, type[Player]] = {
    "random": RandomPlayer,
    "max_damage": MaxBasePowerPlayer,
    "heuristic": SimpleHeuristicsPlayer,
}


def make_bot(
    name: str,
    *,
    battle_format: str = BATTLE_FORMAT,
    server: ServerConfiguration | None = None,
    max_concurrent_battles: int = 1,
    **player_kwargs: Any,
) -> Player:
    """Instantiate a built-in bot connected to ``server`` (default: the local server).

    Extra keyword arguments go to the poke-env ``Player`` constructor. To use a bot as the
    opponent inside ``player.env.make_env`` pass ``start_listening=False``: the wrapper
    drives it directly and it needs no connection of its own.
    """
    try:
        cls = BUILTIN_BOTS[name]
    except KeyError as exc:
        raise ValueError(f"unknown bot {name!r}; choose from {sorted(BUILTIN_BOTS)}") from exc
    return cls(
        battle_format=battle_format,
        server_configuration=server or local_server(),
        max_concurrent_battles=max_concurrent_battles,
        **player_kwargs,
    )
