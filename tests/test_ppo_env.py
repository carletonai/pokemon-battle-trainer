"""The MaskablePPO adapter around the Gen 1 env, checked offline (no server needed)."""

import numpy as np
import pytest
from gymnasium.spaces import Box, Discrete

from battle_trainer.config import NUM_ACTIONS
from battle_trainer.player.env import OBS_SIZE_V0

sb3_contrib = pytest.importorskip("sb3_contrib")
ppo = pytest.importorskip("battle_trainer.player.ppo")
from battle_trainer.arena.bots import make_bot  # noqa: E402


def _offline_env():
    # start_listening=False on both the opponent and the env: nothing connects to a server.
    return ppo.make_maskable_env(make_bot("random", start_listening=False), start_listening=False)


def test_spaces_are_what_maskable_ppo_expects():
    env = _offline_env()
    assert isinstance(env.observation_space, Box)
    assert env.observation_space.shape == (OBS_SIZE_V0,)
    assert env.action_space == Discrete(NUM_ACTIONS)


def test_action_masks_available_before_reset():
    from sb3_contrib.common.maskable.utils import get_action_masks

    env = _offline_env()
    mask = get_action_masks(env)
    assert mask.shape == (NUM_ACTIONS,)
    assert mask.dtype == np.int8
    assert mask.all()


def test_maskable_ppo_accepts_the_env():
    from dataclasses import asdict

    from sb3_contrib import MaskablePPO

    cfg = ppo.PPOConfig(n_steps=8, batch_size=8)
    model = MaskablePPO("MlpPolicy", _offline_env(), **asdict(cfg))
    assert model.policy is not None
