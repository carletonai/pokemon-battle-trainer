"""Evaluation panels: many battles between two players, with a confidence interval.

Luck is everywhere in Pokémon (damage rolls, crits, accuracy), so a win rate is only
meaningful with its uncertainty. The project reports panels of ``config.PANEL_SIZE``
battles; this module makes the size explicit and the interval visible.
"""

from __future__ import annotations

import importlib.metadata
import math
from dataclasses import dataclass

from poke_env.player import Player

from battle_trainer.config import PANEL_SIZE
from battle_trainer.engine.headless import pinned_showdown_commit


def provenance() -> str:
    """The simulator and client versions a result was measured with, for write-ups."""
    try:
        showdown = pinned_showdown_commit()[:10]
    except OSError:
        showdown = "unknown"
    return f"showdown {showdown}, poke-env {importlib.metadata.version('poke-env')}"


@dataclass(frozen=True)
class PanelResult:
    player: str
    opponent: str
    wins: int
    losses: int
    ties: int = 0

    @property
    def n(self) -> int:
        return self.wins + self.losses + self.ties

    @property
    def win_rate(self) -> float:
        """Wins over all battles; a tie counts as half a win."""
        return (self.wins + 0.5 * self.ties) / self.n if self.n else 0.0

    def confidence_interval(self, z: float = 1.96) -> tuple[float, float]:
        """Wilson score interval for the win rate (95% by default)."""
        return wilson_interval(self.wins + 0.5 * self.ties, self.n, z)

    def __str__(self) -> str:
        lo, hi = self.confidence_interval()
        return (
            f"{self.player} vs {self.opponent}: {self.win_rate:.1%} "
            f"[{lo:.1%}, {hi:.1%}] over {self.n} battles "
            f"({self.wins}W {self.losses}L {self.ties}T) | {provenance()}"
        )


def wilson_interval(successes: float, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion. Returns (low, high)."""
    if n <= 0:
        return (0.0, 1.0)
    p = successes / n
    denom = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


async def run_panel(player: Player, opponent: Player, n_battles: int = PANEL_SIZE) -> PanelResult:
    """Battle ``player`` against ``opponent`` ``n_battles`` times on a running server.

    Both players must point at the same server. poke-env's win/loss counters are
    cumulative over a player's lifetime, so this reads them before and after and reports
    only this panel's battles; one player can be panelled against many opponents in a row.
    """
    won, lost, tied = player.n_won_battles, player.n_lost_battles, player.n_tied_battles
    await player.battle_against(opponent, n_battles=n_battles)
    return PanelResult(
        player=player.username,
        opponent=opponent.username,
        wins=player.n_won_battles - won,
        losses=player.n_lost_battles - lost,
        ties=player.n_tied_battles - tied,
    )
