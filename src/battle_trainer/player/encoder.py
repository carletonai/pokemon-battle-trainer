"""State encoder: turns a poke-env ``Battle`` into tensors for the policy.

Design notes (docs/PLAN.md, "What will hurt"):
  * Hidden information: the opponent's team appears one switch at a time and moves only
    as they are used. Encode exactly what has been revealed, plus a prior from Showdown's
    published random-battle sets for what an unrevealed species could carry.
  * Small vocab: Gen 1 is 151 species and a short move list, so learned embeddings are
    cheap. Keep the tables sized by generation so Gen 1 OU and Gen 9 reuse the code.
  * One encoder for everything: the Player, the ghosts and the headless/libpkmn tiers all
    go through this module, so a replay and a live battle produce the same tensors.

TODO(player): implement ``StateEncoder``.
  1. Per-slot features for 12 Pokémon: species id, HP fraction, status, boosts, fainted,
     active, revealed flag; per-move features for the active Pokémon: move id, PP, type.
  2. Embedding tables for species/moves/types/status, concatenated with scalar features,
     through a small MLP or a set-transformer over slots.
  3. A ``features(battle) -> dict[str, np.ndarray]`` function (no torch) that ``env.py``
     and ``ghosts.parse`` can call, and the ``nn.Module`` that consumes those arrays.
"""

from __future__ import annotations

import torch
from poke_env.battle import PokemonType, Status
from torch import nn

# Gen 1 vocabulary sizes with one slot spare for "unknown" (index 0).
GEN1_NUM_SPECIES = 151 + 1
GEN1_NUM_MOVES = 165 + 1
# Sized from poke-env's enums so later generations (Stellar, "???") fit without edits.
NUM_TYPES = len(PokemonType) + 1
NUM_STATUS = len(Status) + 1


class StateEncoder(nn.Module):
    """Battle state -> fixed-size vector. Not implemented yet."""

    def __init__(self, embed_dim: int = 32, out_dim: int = 256) -> None:
        super().__init__()
        self.species = nn.Embedding(GEN1_NUM_SPECIES, embed_dim)
        self.moves = nn.Embedding(GEN1_NUM_MOVES, embed_dim)
        self.out_dim = out_dim

    def forward(self, features: dict[str, torch.Tensor]) -> torch.Tensor:
        raise NotImplementedError("TODO(player): see module docstring")
