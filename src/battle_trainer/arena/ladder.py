"""Ladder runner: play ranked games on the official server and log rating + replays.

The human ladder is the project's final exam. Rules of the road (docs/PLAN.md):
one registered CAIS account, never stall the turn timer, stay out of chat rooms, and
the public page shows the bot's name, rating and replay links only (no artwork).

TODO(arena): implement ``run_ladder``.
  1. Build the player with ``engine.server.official_server()`` and
     ``engine.server.ladder_account()``; set ``save_replays`` to a run folder.
  2. Call ``player.ladder(n_games)``; after each battle append a row to a JSONL log in
     ``runs/``. Two Showdown details that cost real debugging time if missed:
       * poke-env only saves a local replay HTML (``save_replays=<folder>``); it never
         publishes replays. A public link needs ``/savereplay`` sent *during* the battle:
         poke-env sends ``/leave`` the moment it sees ``|win|`` or ``|tie|``, and Showdown
         refuses commands sent to a room you have left. So in the player's ``choose_move``
         (make it ``async``; poke-env awaits an awaitable result) send, once per battle,
         ``await self.ps_client.send_message("/savereplay", battle.battle_tag)``. Showdown
         re-uploads the complete replay at battle end, and the URL is deterministic:
         ``https://replay.pokemonshowdown.com/<battle_tag without the "battle-" prefix>``.
         The server answers with a ``|popup|`` that poke-env logs as a warning; ignore it.
       * ``battle.rating`` is parsed from ``|raw|`` lines the server sends only after an
         async ladder update, so after the early ``/leave`` it can be ``None``. Log it when
         present and plan a fallback (query the account's ladder rating separately).
  3. Export the log to the rating page on carletonai.com (format to be agreed with the
     web team; a static JSON file the page fetches is the simplest start).
  4. Schedule weekly runs and keep the model checkpoint used for each one.
"""

from __future__ import annotations

from poke_env.player import Player


async def run_ladder(player: Player, n_games: int) -> None:
    """Play ``n_games`` ranked battles and log the results. Not implemented yet."""
    raise NotImplementedError("TODO(arena): see module docstring")
