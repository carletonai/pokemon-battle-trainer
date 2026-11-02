"""PPO via Stable-Baselines3: ``MaskablePPO`` from sb3-contrib.

Decided by the project lead on Nov 2, 2026: use Stable-Baselines3 rather than a hand-rolled
PPO. ``MaskablePPO`` owns the rollouts, GAE, the clipped objective and action masking. Our
job is the environment, the state encoder and the opponent pool.

How the pieces connect::

    from dataclasses import asdict
    from sb3_contrib import MaskablePPO
    from battle_trainer.arena.bots import make_bot
    from battle_trainer.player.ppo import PPOConfig, make_maskable_env

    env = make_maskable_env(make_bot("random", start_listening=False))
    model = MaskablePPO("MlpPolicy", env, verbose=1, tensorboard_log="runs", **asdict(PPOConfig()))
    model.learn(total_timesteps=100_000)

``make_maskable_env`` flattens poke-env's ``{"observation", "action_mask"}`` dict into the
plain observation ``MaskablePPO`` expects and exposes the mask through sb3-contrib's
``ActionMasker``, which MaskablePPO queries before every action.

TODO(player):
  1. Run the snippet above against the random bot for a few thousand steps with the local
     server up; check the rollout runs end to end and TensorBoard shows a reward curve.
  2. Plug in the real encoder: ``policy_kwargs=dict(features_extractor_class=StateEncoder)``
     (``encoder.py``). The observation then has to carry the features the encoder wants.
  3. Evaluate with ``arena.panel.run_panel`` on 500-battle panels, not SB3's episode reward.
  4. Hand the opponent choice to ``self_play`` (a callback swaps the opponent between rollouts).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import gymnasium
import numpy as np
from poke_env.player import Player
from poke_env.ps_client import ServerConfiguration
from sb3_contrib.common.wrappers import ActionMasker

from battle_trainer.config import BATTLE_FORMAT, NUM_ACTIONS
from battle_trainer.player.env import make_env


@dataclass
class PPOConfig:
    """Keyword arguments for ``MaskablePPO``. Names match SB3's, so ``**asdict(cfg)`` works."""

    learning_rate: float = 3e-4
    n_steps: int = 2048
    batch_size: int = 256
    n_epochs: int = 4
    gamma: float = 0.99
    gae_lambda: float = 0.95
    clip_range: float = 0.2
    ent_coef: float = 0.01
    vf_coef: float = 0.5


class _FlattenObservation(gymnasium.ObservationWrapper):
    """Return ``obs["observation"]`` and remember ``obs["action_mask"]`` for ``ActionMasker``."""

    def __init__(self, env: gymnasium.Env) -> None:
        super().__init__(env)
        self.observation_space = env.observation_space["observation"]
        # Everything legal until the first observation arrives (MaskablePPO asks after reset).
        self.last_action_mask = np.ones(NUM_ACTIONS, dtype=np.int8)

    def observation(self, observation: dict[str, Any]) -> np.ndarray:
        self.last_action_mask = np.asarray(observation["action_mask"], dtype=np.int8)
        return observation["observation"]


def _action_mask_fn(env: gymnasium.Env) -> np.ndarray:
    return env.get_wrapper_attr("last_action_mask")


def make_maskable_env(
    opponent: Player,
    *,
    battle_format: str = BATTLE_FORMAT,
    server_configuration: ServerConfiguration | None = None,
    **kwargs: Any,
) -> gymnasium.Env:
    """``player.env.make_env`` prepared for ``MaskablePPO``: flat observation plus action masks.

    Same arguments as ``make_env``. The result also answers ``action_masks()``, which is
    what sb3-contrib's ``get_action_masks`` and ``MaskablePPO`` look for.
    """
    env = make_env(
        opponent, battle_format=battle_format, server_configuration=server_configuration, **kwargs
    )
    return ActionMasker(_FlattenObservation(env), _action_mask_fn)


def train() -> None:
    """Self-play training entry point. Not implemented yet; see the module docstring."""
    raise NotImplementedError("TODO(player): see module docstring")
