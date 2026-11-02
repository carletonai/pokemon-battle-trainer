"""Train one ghost per rating band, and wrap a trained ghost as a poke-env ``Player``.

TODO(ghosts):
  1. ``train_ghost``: cross-entropy over legal actions (mask illegal ones) on
     ``ReplayDataset``; report top-1 accuracy on held-out battles per band.
  2. ``GhostPlayer``: a ``poke_env.player.Player`` whose ``choose_move`` encodes the
     battle with the shared encoder, runs the model, and returns the argmax (or a
     temperature-sampled) legal action via ``SinglesEnv.action_to_order``.
  3. First milestone: a ghost that beats ``SimpleHeuristicsPlayer`` over a 500-battle panel.
"""

from __future__ import annotations

from poke_env.battle import AbstractBattle
from poke_env.player import BattleOrder, Player


class GhostPlayer(Player):
    """A bot that plays like the humans in one rating band. Not implemented yet."""

    def choose_move(self, battle: AbstractBattle) -> BattleOrder:
        raise NotImplementedError("TODO(ghosts): see module docstring")
