"""Actor-critic policy with action masking.

At most nine legal actions a turn (4 moves, up to 5 switches) out of a fixed space of
ten (``config.NUM_ACTIONS``). Illegal actions get probability zero by setting their
logits to ``-inf`` before the softmax. The mask arrives in every observation as
``obs["action_mask"]`` (``np.int8``, length ``NUM_ACTIONS``), computed by poke-env's
``SinglesEnv.get_action_mask``.

TODO(player): implement ``MaskedActorCritic``.
  1. Shared trunk from ``encoder.StateEncoder``; a policy head of ``NUM_ACTIONS`` logits
     and a value head of one scalar.
  2. ``act(obs, mask)`` returning action, log-prob, value, entropy for rollouts.
  3. ``evaluate(obs, mask, actions)`` for the PPO update.
"""

from __future__ import annotations

import torch
from torch import nn

from battle_trainer.config import NUM_ACTIONS


def mask_logits(logits: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    """Set logits of illegal actions to ``-inf``. ``mask`` is 1/True where legal.

    Every row must have at least one legal action, otherwise the softmax is undefined.
    """
    mask = mask.to(dtype=torch.bool)
    if not bool(mask.any(dim=-1).all()):
        raise ValueError("every row of the action mask must have at least one legal action")
    return logits.masked_fill(~mask, float("-inf"))


class MaskedActorCritic(nn.Module):
    """Policy and value heads over an encoded state. Not implemented yet."""

    def __init__(self, in_dim: int, hidden: int = 256, num_actions: int = NUM_ACTIONS) -> None:
        super().__init__()
        self.trunk = nn.Sequential(nn.Linear(in_dim, hidden), nn.ReLU())
        self.policy_head = nn.Linear(hidden, num_actions)
        self.value_head = nn.Linear(hidden, 1)

    def forward(self, obs: torch.Tensor, mask: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """Returns (masked logits, value)."""
        h = self.trunk(obs)
        return mask_logits(self.policy_head(h), mask), self.value_head(h).squeeze(-1)
