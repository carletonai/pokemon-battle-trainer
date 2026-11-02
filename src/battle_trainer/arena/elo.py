"""Elo ratings for the offline ladder of bots and ghosts.

Offline Elo only says who beats whom on our ladder. It is not on the same scale as the
official Showdown rating, which is anchored to the whole player base (a new account
starts at 1000). Ghosts cloned from rated humans are the bridge between the two.
"""

from __future__ import annotations

from dataclasses import dataclass, field

DEFAULT_RATING = 1000.0
DEFAULT_K = 32.0


def expected_score(rating: float, opponent_rating: float) -> float:
    """Probability that ``rating`` beats ``opponent_rating`` under the Elo model."""
    return 1.0 / (1.0 + 10.0 ** ((opponent_rating - rating) / 400.0))


def update(rating: float, opponent_rating: float, score: float, k: float = DEFAULT_K) -> float:
    """New rating after one game. ``score`` is 1 for a win, 0.5 for a tie, 0 for a loss."""
    if not 0.0 <= score <= 1.0:
        raise ValueError(f"score must be in [0, 1], got {score}")
    return rating + k * (score - expected_score(rating, opponent_rating))


@dataclass
class EloLadder:
    """Ratings for a pool of named players, updated one result at a time."""

    k: float = DEFAULT_K
    ratings: dict[str, float] = field(default_factory=dict)

    def rating(self, name: str) -> float:
        return self.ratings.setdefault(name, DEFAULT_RATING)

    def record(self, player_a: str, player_b: str, score_a: float) -> None:
        """Record one game. ``score_a`` is A's result: 1 win, 0.5 tie, 0 loss."""
        ra, rb = self.rating(player_a), self.rating(player_b)
        self.ratings[player_a] = update(ra, rb, score_a, self.k)
        self.ratings[player_b] = update(rb, ra, 1.0 - score_a, self.k)

    def standings(self) -> list[tuple[str, float]]:
        """Players sorted best first."""
        return sorted(self.ratings.items(), key=lambda kv: kv[1], reverse=True)
