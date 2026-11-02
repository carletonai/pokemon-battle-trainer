"""Action masking for code outside Stable-Baselines3.

During RL training, masking is SB3's job: ``MaskablePPO`` reads the legal-action mask from
``ActionMasker`` (see ``ppo.make_maskable_env``) and never samples an illegal move. This
module serves everything else that needs the same rule: the ghosts' imitation loss
(cross-entropy over legal actions only) and evaluation code that turns logits into an order.

The mask is poke-env's: ``obs["action_mask"]`` is an ``np.int8`` vector of length
``NUM_ACTIONS`` with 1 where an action is legal (``SinglesEnv.get_action_mask``). At most
nine of the ten entries are ever legal (4 moves, up to 5 switches).
"""

from __future__ import annotations

import torch


def mask_logits(logits: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    """Set logits of illegal actions to ``-inf``. ``mask`` is 1/True where legal.

    Every row must have at least one legal action, otherwise the softmax is undefined.
    """
    mask = mask.to(dtype=torch.bool)
    if not bool(mask.any(dim=-1).all()):
        raise ValueError("every row of the action mask must have at least one legal action")
    return logits.masked_fill(~mask, float("-inf"))
