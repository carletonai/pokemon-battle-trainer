"""Battle two random agents on a local Pokémon Showdown server.

Start the server first: see "Run a battle" in the README.
"""

from __future__ import annotations

import asyncio
import socket
import sys
from pathlib import Path

from poke_env import AccountConfiguration
from poke_env.player import RandomPlayer

FORMAT = "gen1randombattle"
OUT = Path("data/battles")


def new_player() -> RandomPlayer:
    # A new name each run, or Showdown puts us back into an old unfinished battle.
    name = AccountConfiguration.generate("RandomPlayer", rand=True)
    return RandomPlayer(name, battle_format=FORMAT)


def server_is_up() -> bool:
    try:
        socket.create_connection(("localhost", 8000), timeout=2).close()
    except OSError:
        return False
    return True


async def main() -> None:
    if not server_is_up():
        sys.exit('No Showdown server on localhost:8000. See "Run a battle" in the README.')

    one, two = new_player(), new_player()
    await one.battle_against(two, n_battles=1)

    (battle,) = one.battles.values()
    if battle.won is None:
        print(f"Tie after {battle.turn} turns.")
    else:
        winner, loser = (one, two) if battle.won else (two, one)
        print(f"{winner.username} beat {loser.username} in {battle.turn} turns.")
    print(f"Watch it: {battle.save_replay(OUT / f'{battle.battle_tag}.html')}")


if __name__ == "__main__":
    asyncio.run(main())
