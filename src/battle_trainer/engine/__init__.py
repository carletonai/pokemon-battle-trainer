"""Simulator backends (workstream: Engine speed).

Three tiers, fastest last. The code that trains and evaluates should not care which
one is underneath.

    server    Pokémon Showdown's server run locally + poke-env over a websocket.
              Convenient; one round trip per move. Development, the bot ladder, and
              the official ladder against humans.
    headless  ``pokemon-showdown simulate-battle``: the same simulator over
              stdin/stdout, one subprocess per battle, seedable, no server.
              Validation and training without websocket overhead.
    libpkmn   A Zig engine that matches Showdown's Gen 1 behaviour exactly, wrapped
              in Python by ``oak``. Training throughput. Gen 1 and Linux only.

Week-4 milestone: training runs with no server in the loop.
"""
