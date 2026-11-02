"""PPO: the update that turns rollouts into a better policy.

Open decision (ask in #pokemon-battle-trainer before building): hand-rolled PPO in plain
PyTorch (CleanRL style, ~300 lines, full control over masking and self-play) versus a
library such as Stable-Baselines3 with ``MaskablePPO`` from sb3-contrib (less code, less
control). The planning notes assume PyTorch + PPO + action masking but do not pick.

TODO(player): implement ``ppo_update`` once the decision is made.
  1. Rollout buffer of (obs, mask, action, log-prob, value, reward, done).
  2. GAE advantages; clipped surrogate objective; value loss; entropy bonus.
  3. Log win rate against the current opponent mix every N updates.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PPOConfig:
    learning_rate: float = 3e-4
    gamma: float = 0.99
    gae_lambda: float = 0.95
    clip_coef: float = 0.2
    entropy_coef: float = 0.01
    value_coef: float = 0.5
    update_epochs: int = 4
    minibatch_size: int = 256
    rollout_steps: int = 2048


def ppo_update(*args: object, **kwargs: object) -> None:
    """One PPO update over a rollout buffer. Not implemented yet."""
    raise NotImplementedError("TODO(player): see module docstring")
