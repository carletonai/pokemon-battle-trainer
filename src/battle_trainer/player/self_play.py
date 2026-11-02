"""Self-play: the opponent pool and the training loop.

Pure self-play drifts into habits that exploit its own weaknesses, not humans'. The pool
therefore holds three kinds of opponent, and the Coach decides the mix:

    past selves   frozen checkpoints of the Player, added every K updates
    ghosts        imitation bots per rating band (``battle_trainer.ghosts``)
    bots          the built-in baselines (``battle_trainer.arena.bots``)

TODO(player): implement ``OpponentPool`` and ``train``.
  1. ``OpponentPool.add(name, make_player)`` and ``sample(sampler)`` where ``sampler`` is a
     ``battle_trainer.coach.curriculum`` sampler (uniform is the baseline).
  2. A training loop: build ``player.env.make_env(opponent)``, collect a rollout,
     ``ppo.ppo_update``, evaluate on a held-out panel the Coach cannot pick from.
  3. Checkpoints to ``checkpoints/`` (git-ignored) with the Showdown commit and poke-env
     version written alongside, so every result is reproducible.
  4. Pick the experiment tracker (W&B, TensorBoard or JSONL in ``runs/``; open decision)
     and log the opponent mix and panel results of every run with it.
"""

from __future__ import annotations

from collections.abc import Callable

from poke_env.player import Player


class OpponentPool:
    """Minimal registry of named opponents and how to build them.

    TODO(player): ``sample(sampler)`` and checkpoint-backed past selves.
    """

    def __init__(self) -> None:
        self._makers: dict[str, Callable[[], Player]] = {}

    def add(self, name: str, make_player: Callable[[], Player]) -> None:
        self._makers[name] = make_player

    @property
    def names(self) -> list[str]:
        return list(self._makers)

    def make(self, name: str) -> Player:
        return self._makers[name]()


def train() -> None:
    """Self-play training loop. Not implemented yet."""
    raise NotImplementedError("TODO(player): see module docstring")
