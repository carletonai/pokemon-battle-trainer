"""Gymnasium/PettingZoo environment for Gen 1 battles, built on poke-env's ``SinglesEnv``.

``SinglesEnv`` already handles the server connection, turn synchronisation and the
action mapping (0-5 switch to team slot, 6-9 use move 1-4; see ``get_action_mask``).
We supply two things: the observation (``embed_battle``) and the reward (``calc_reward``).

What ``reset()`` and ``step()`` hand back, per agent::

    obs = {"observation": np.float32[OBS_SIZE_V0], "action_mask": np.int8[NUM_ACTIONS]}
    info = {}

poke-env wraps the ``Box`` we set in ``observation_spaces`` into that ``gymnasium.spaces.Dict``
itself, and the legal-action mask always travels inside ``obs``, never in ``info``.

The observation here is a deliberately tiny v0 so that the stack runs end to end.
The real state encoder lives in ``battle_trainer.player.encoder`` and replaces it.
"""

from __future__ import annotations

from typing import Any

import gymnasium
import numpy as np
from gymnasium.spaces import Box
from poke_env.battle import AbstractBattle
from poke_env.environment import SingleAgentWrapper, SinglesEnv
from poke_env.player import Player
from poke_env.ps_client import ServerConfiguration

from battle_trainer.config import BATTLE_FORMAT
from battle_trainer.engine.server import local_server

# v0 observation: our 6 HP fractions, opponent's 6 HP fractions (unrevealed = 1.0),
# count of opponent Pokémon revealed / 6, turn / 100.
OBS_SIZE_V0 = 6 + 6 + 1 + 1


class Gen1Env(SinglesEnv):
    """Two-agent Gen 1 environment. Use ``make_env`` for the usual single-agent view."""

    def __init__(
        self,
        *,
        battle_format: str = BATTLE_FORMAT,
        server_configuration: ServerConfiguration | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            battle_format=battle_format,
            server_configuration=server_configuration or local_server(),
            **kwargs,
        )
        self.observation_spaces = {
            agent: Box(low=0.0, high=1.0, shape=(OBS_SIZE_V0,), dtype=np.float32)
            for agent in self.possible_agents
        }

    def embed_battle(self, battle: AbstractBattle) -> np.ndarray:
        """v0 embedding. TODO(player): replace with ``encoder.StateEncoder`` features.

        The real encoder needs, at least: species, HP, status and boosts for all twelve
        slots (opponent slots only as revealed); the active Pokémon's known moves with PP;
        Showdown's published random-battle sets to narrow what an unrevealed species can
        carry; and field state. Gen 1 keeps the vocab small: 151 species, ~165 moves.
        """
        own = [mon.current_hp_fraction for mon in battle.team.values()]
        own += [0.0] * (6 - len(own))
        opp = [mon.current_hp_fraction for mon in battle.opponent_team.values()]
        revealed = len(opp) / 6.0
        opp += [1.0] * (6 - len(opp))
        turn = min(battle.turn, 100) / 100.0
        return np.asarray([*own, *opp, revealed, turn], dtype=np.float32)

    def calc_reward(self, battle: AbstractBattle) -> float:
        """Sparse win/loss reward with small shaping for damage dealt and taken.

        TODO(player): revisit shaping once PPO trains; pure win/loss is the honest
        objective and shaping can teach the wrong habits.
        """
        return self.reward_computing_helper(
            battle, fainted_value=2.0, hp_value=1.0, victory_value=30.0
        )


class _Int64Actions(gymnasium.ActionWrapper):
    """Cast actions to ``np.int64`` before they reach poke-env.

    poke-env's ``action_to_order`` calls ``action.item()`` for move actions (6-9), so a
    plain Python ``int`` works for switches and crashes on moves. Casting here removes
    that intermittent failure.
    """

    def action(self, action: Any) -> np.int64:
        return np.int64(action)


def make_env(
    opponent: Player,
    *,
    battle_format: str = BATTLE_FORMAT,
    server_configuration: ServerConfiguration | None = None,
    **kwargs: Any,
) -> gymnasium.Env:
    """Single-agent Gymnasium view: we control agent 1, ``opponent`` plays agent 2.

    ``opponent`` does not need its own server connection; build it with
    ``start_listening=False`` (``arena.bots.make_bot(name, start_listening=False)``). The
    wrapper only calls its synchronous ``choose_move`` on the environment's copy of the
    battle and ``reset_battles()`` on each reset, so ``choose_move`` must return a
    ``BattleOrder``, not a coroutine.

    Actions can be ``int``, ``np.int64`` or a 0-d tensor; they are cast to ``np.int64``
    on the way in (see ``_Int64Actions``).
    """
    env = Gen1Env(battle_format=battle_format, server_configuration=server_configuration, **kwargs)
    return _Int64Actions(SingleAgentWrapper(env, opponent))
