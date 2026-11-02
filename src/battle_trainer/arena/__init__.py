"""Battles, panels, Elo and the ladder (workstream: Arena).

The Arena runs battles and keeps score. It owns:

    bots     the built-in baselines from poke-env (random, max damage, heuristics)
    panel    N-battle evaluation panels with confidence intervals
    elo      an Elo ladder among our own bots and ghosts (offline rating)
    ladder   the runner that plays on the official ladder and logs rating + replays

Week-4 milestone: ladder v0 with the built-in bots, rating page live.
"""
