"""Ladder runner: play ranked games on the official server and log rating + replays.

The human ladder is the project's final exam. Rules of the road (docs/PLAN.md):
one registered CAIS account, never stall the turn timer, stay out of chat rooms, and
the public page shows the bot's name, rating and replay links only (no artwork).

TODO(arena): implement ``run_ladder``.
  1. Build the player with ``engine.server.official_server()`` and
     ``engine.server.ladder_account()``; set ``save_replays`` to a run folder.
  2. Call ``player.ladder(n_games)``; after each battle read ``battle.rating`` and append
     a row to a JSONL log in ``runs/``. poke-env only saves a local replay HTML
     (``save_replays=<folder>``); it does not publish replays. For a public link, once
     ``battle.finished`` send ``await player.ps_client.send_message("/savereplay",
     battle.battle_tag)`` and build ``https://replay.pokemonshowdown.com/<battle_tag
     without the "battle-" prefix>``.
  3. Export the log to the rating page on carletonai.com (format to be agreed with the
     web team; a static JSON file the page fetches is the simplest start).
  4. Schedule weekly runs and keep the model checkpoint used for each one.
"""

from __future__ import annotations

from poke_env.player import Player


async def run_ladder(player: Player, n_games: int) -> None:
    """Play ``n_games`` ranked battles and log the results. Not implemented yet."""
    raise NotImplementedError("TODO(arena): see module docstring")
