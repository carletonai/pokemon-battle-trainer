"""Prove the stack works: battle poke-env's built-in bots on a local Showdown server.

Usage::

    scripts/start_showdown.sh            # in another terminal
    uv run python scripts/smoke_battle.py --battles 10

Exits non-zero if the battles do not finish, so CI can use it as a smoke test.
"""

from __future__ import annotations

import argparse
import asyncio
import sys

from battle_trainer.arena.bots import BUILTIN_BOTS, make_bot
from battle_trainer.arena.panel import run_panel
from battle_trainer.config import BATTLE_FORMAT
from battle_trainer.engine.server import local_server


async def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--battles", type=int, default=10)
    parser.add_argument("--format", default=BATTLE_FORMAT)
    parser.add_argument("--player", default="max_damage", choices=sorted(BUILTIN_BOTS))
    parser.add_argument("--opponent", default="random", choices=sorted(BUILTIN_BOTS))
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args(argv)

    server = local_server(port=args.port)
    player = make_bot(args.player, battle_format=args.format, server=server)
    opponent = make_bot(args.opponent, battle_format=args.format, server=server)

    print(f"{args.player} vs {args.opponent}: {args.battles} x {args.format}")
    print(f"server: {server.websocket_url}")
    result = await run_panel(player, opponent, n_battles=args.battles)
    print(result)

    if result.n != args.battles:
        print(f"error: expected {args.battles} finished battles, got {result.n}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
