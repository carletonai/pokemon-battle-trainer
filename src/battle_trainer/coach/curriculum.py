"""Opponent sampling: the uniform baseline and the weakness-weighted Coach.

Both samplers return a probability over the names in an opponent pool. The training loop
draws the next sparring partner from that distribution.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

UNIFORM_FLOOR = 0.5  # the Coach never controls more than this share of the diet


def uniform(names: Sequence[str]) -> dict[str, float]:
    """The baseline: every opponent equally likely."""
    if not names:
        raise ValueError("opponent pool is empty")
    p = 1.0 / len(names)
    return dict.fromkeys(names, p)


def mix_with_uniform(weights: dict[str, float], floor: float = UNIFORM_FLOOR) -> dict[str, float]:
    """Blend Coach weights with the uniform distribution so uniform keeps at least ``floor``.

    ``weights`` need not be normalised. The result is a proper distribution.
    """
    if not 0.0 <= floor <= 1.0:
        raise ValueError("floor must be in [0, 1]")
    names = list(weights)
    base = uniform(names)
    total = float(sum(weights.values()))
    coach = {n: (weights[n] / total if total > 0 else base[n]) for n in names}
    return {n: floor * base[n] + (1.0 - floor) * coach[n] for n in names}


class WeaknessSampler:
    """Sample what we lose to most, with the guardrails from the package docstring.

    TODO(coach): implement.
      1. ``record(opponent, won)`` keeps a rolling window of results per opponent.
      2. ``probabilities()`` weights each opponent by its loss rate, but only once that
         opponent has at least ``min_battles`` results (default 500); below that it gets the
         uniform weight. Then ``mix_with_uniform``.
      3. Once a matchup's win rate crosses ``fixed_threshold``, drop its extra weight so
         the Coach moves on.
      4. Extend to starting positions (resume battles from saved states) and, for OU, teams
         (``coach.teambuilder``).
    """

    def __init__(self, names: Sequence[str], min_battles: int = 500, floor: float = UNIFORM_FLOOR):
        self.names = list(names)
        self.min_battles = min_battles
        self.floor = floor

    def record(self, opponent: str, won: bool) -> None:
        raise NotImplementedError("TODO(coach): see class docstring")

    def probabilities(self) -> dict[str, float]:
        raise NotImplementedError("TODO(coach): see class docstring")

    def sample(self, rng: np.random.Generator) -> str:
        p = self.probabilities()
        return str(rng.choice(list(p), p=list(p.values())))
