"""Battle two random agents on a local Pokémon Showdown server.

    python random_battle.py

Start the server first: see "Run a battle" in the README. Each agent picks a random
legal move every turn. The script prints who won and saves a replay to data/battles/
that you can open in a browser.
"""

from __future__ import annotations

import asyncio
import socket
import sys
from pathlib import Path

from poke_env.player import RandomPlayer

FORMAT = "gen1randombattle"
OUT = Path("data/battles")


def server_is_up() -> bool:
    try:
        socket.create_connection(("localhost", 8000), timeout=2).close()
    except OSError:
        return False
    return True


async def main() -> None:
    if not server_is_up():
        sys.exit('No Showdown server on localhost:8000. See "Run a battle" in the README.')

    one = RandomPlayer(battle_format=FORMAT)
    two = RandomPlayer(battle_format=FORMAT)
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
