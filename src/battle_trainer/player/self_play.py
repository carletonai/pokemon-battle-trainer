"""Self-play: the opponent pool and the training loop.

Pure self-play drifts into habits that exploit its own weaknesses, not humans'. The pool
therefore holds three kinds of opponent, and the Coach decides the mix:

    past selves   frozen checkpoints of the Player, added every K updates
    ghosts        imitation bots per rating band (``battle_trainer.ghosts``)
    bots          the built-in baselines (``battle_trainer.arena.bots``)

TODO(player): implement ``OpponentPool.sample`` and ``train``.
  1. ``OpponentPool.sample(sampler)`` where ``sampler`` is a ``battle_trainer.coach.curriculum``
     sampler (uniform is the baseline).
  2. An SB3 callback (``BaseCallback._on_rollout_end``) that swaps the environment's
     opponent between rollouts (``env.set_wrapper_attr("opponent", ...)`` on the
     ``SingleAgentWrapper``); ``CheckpointCallback`` adds past selves to the pool every K
     updates. ``ppo.py`` has the ``MaskablePPO`` call this wraps.
  3. Checkpoints to ``checkpoints/`` (git-ignored) with the Showdown commit and poke-env
     version written alongside, so every result is reproducible.
  4. Evaluate on the held-out panel with ``arena.panel.run_panel`` and log the opponent
     mix and panel results of every run. SB3 writes TensorBoard logs out of the box
     (``tensorboard_log=``), the default tracker until someone argues for another.
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
