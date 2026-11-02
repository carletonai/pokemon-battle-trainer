import asyncio

import pytest

from battle_trainer.arena.panel import PanelResult, run_panel, wilson_interval


class _FakePlayer:
    """Stands in for a poke-env Player: cumulative counters, like the real thing."""

    def __init__(self, name: str, wins_per_battle: bool) -> None:
        self.username = name
        self.n_won_battles = 0
        self.n_lost_battles = 0
        self.n_tied_battles = 0
        self._wins = wins_per_battle

    async def battle_against(self, opponent, n_battles: int = 1) -> None:
        for _ in range(n_battles):
            if self._wins:
                self.n_won_battles += 1
                opponent.n_lost_battles += 1
            else:
                self.n_lost_battles += 1
                opponent.n_won_battles += 1


def test_run_panel_counts_only_this_panel():
    player, opponent = _FakePlayer("p", wins_per_battle=True), _FakePlayer("o", False)
    first = asyncio.run(run_panel(player, opponent, n_battles=3))
    second = asyncio.run(run_panel(player, opponent, n_battles=5))
    assert (first.n, first.wins) == (3, 3)
    assert (second.n, second.wins) == (5, 5)


def test_win_rate_counts_ties_as_half():
    r = PanelResult("a", "b", wins=6, losses=2, ties=2)
    assert r.n == 10
    assert r.win_rate == pytest.approx(0.7)


def test_empty_panel():
    r = PanelResult("a", "b", wins=0, losses=0)
    assert r.win_rate == 0.0
    assert r.confidence_interval() == (0.0, 1.0)


def test_wilson_interval_shrinks_with_more_battles():
    lo50, hi50 = wilson_interval(30, 50)
    lo500, hi500 = wilson_interval(300, 500)
    assert hi50 - lo50 > hi500 - lo500
    assert lo500 < 0.6 < hi500


def test_wilson_interval_stays_in_unit_range():
    assert wilson_interval(0, 10) == pytest.approx((0.0, 0.2775), abs=1e-3)
    lo, hi = wilson_interval(10, 10)
    assert lo > 0.7 and hi == 1.0


def test_str_mentions_both_players_and_count():
    s = str(PanelResult("max_damage", "random", wins=7, losses=3))
    assert "max_damage vs random" in s and "10 battles" in s
