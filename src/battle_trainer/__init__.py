"""AI Pokémon Battle Trainer.

A self-play reinforcement-learning bot for Pokémon Showdown, built by CAIS.
The package is split by workstream; each subpackage's docstring says what it
owns and where to start.

    engine   the three simulator tiers (Showdown server, headless CLI, libpkmn)
    arena    battle runner, 500-battle panels, Elo among bots, the ladder runner
    ghosts   replay scraping and parsing, imitation bots per rating band
    player   the bot we train: state encoder, masked policy, PPO self-play
    coach    sparring curriculum and, later, the team builder

See docs/PLAN.md for the plan and docs/WORKSTREAMS.md for first tasks.
"""

__version__ = "0.1.0"
