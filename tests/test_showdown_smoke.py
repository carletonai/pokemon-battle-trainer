"""End-to-end check against a running local Showdown server (skipped if there is none)."""

import asyncio

import pytest

from battle_trainer.arena.bots import make_bot
from battle_trainer.arena.panel import run_panel

pytestmark = pytest.mark.showdown


def test_builtin_bots_finish_battles():
    player = make_bot("max_damage")
    opponent = make_bot("random")
    # Bounded so a misbehaving server fails loudly instead of hanging pytest.
    result = asyncio.run(asyncio.wait_for(run_panel(player, opponent, n_battles=3), timeout=180))
    assert result.n == 3
