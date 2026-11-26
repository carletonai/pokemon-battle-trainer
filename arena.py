"""Battle the built-in bots against each other and print each one's win rate.

Start the server first: see "Run a battle" in the README.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from itertools import combinations

from poke_env import AccountConfiguration
from poke_env.player import MaxBasePowerPlayer, RandomPlayer, SimpleHeuristicsPlayer

from random_battle import FORMAT, server_is_up

# Add your own bot here to rank it.
BOTS = {
    "random": RandomPlayer,
    "max-damage": MaxBasePowerPlayer,
    "heuristics": SimpleHeuristicsPlayer,
}


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--battles", type=int, default=500, help="battles per pair of bots")
    n = parser.parse_args().battles
    if not server_is_up():
        sys.exit('No Showdown server on localhost:8000. See "Run a battle" in the README.')

    players = {
        name: bot(
            # A new name each run, or Showdown puts us back into an old unfinished battle.
            AccountConfiguration.generate(name, rand=True),
            battle_format=FORMAT,
            max_concurrent_battles=10,
            log_level=logging.ERROR,  # hide poke-env's harmless warnings about Gen 1 moves
        )
        for name, bot in BOTS.items()
    }

    score = {name: {} for name in BOTS}  # score[a][b]: a's wins over b, a tie is half a win
    for a, b in combinations(BOTS, 2):
        print(f"{a} vs {b}: ", end="", flush=True)
        one, two = players[a], players[b]
        await one.battle_against(two, n_battles=n)
        wins, losses, ties = one.n_won_battles, one.n_lost_battles, one.n_tied_battles
        print(f"{wins} wins, {losses} losses, {ties} ties")
        score[a][b], score[b][a] = wins + ties / 2, losses + ties / 2
        one.reset_battles()
        two.reset_battles()

    rate = {name: sum(score[name].values()) / (n * (len(BOTS) - 1)) for name in BOTS}
    print(f"\n{FORMAT}, {n} battles per pair\n")
    print(f"{'':3}{'bot':12}{'win rate':>10}" + "".join(f"{'vs ' + b:>16}" for b in BOTS))
    for rank, a in enumerate(sorted(BOTS, key=rate.get, reverse=True), 1):
        cells = ["-" if a == b else f"{score[a][b] / n:.1%}" for b in BOTS]
        print(f"{rank:<3}{a:12}{rate[a]:>10.1%}" + "".join(f"{cell:>16}" for cell in cells))


if __name__ == "__main__":
    asyncio.run(main())
