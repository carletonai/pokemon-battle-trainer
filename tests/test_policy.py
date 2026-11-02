import pytest

from battle_trainer.config import NUM_ACTIONS

torch = pytest.importorskip("torch")
policy = pytest.importorskip("battle_trainer.player.policy")


def test_mask_logits_zeroes_illegal_probabilities():
    logits = torch.zeros(2, NUM_ACTIONS)
    mask = torch.zeros(2, NUM_ACTIONS, dtype=torch.int8)
    mask[0, 6] = 1  # only move 1 legal
    mask[1, [0, 1, 7]] = 1
    probs = torch.softmax(policy.mask_logits(logits, mask), dim=-1)
    assert probs[0, 6] == pytest.approx(1.0)
    assert probs[0].sum() == pytest.approx(1.0)
    assert probs[1, [0, 1, 7]].sum() == pytest.approx(1.0)
    assert probs[1, 6] == 0.0


def test_mask_logits_rejects_all_illegal_row():
    with pytest.raises(ValueError):
        policy.mask_logits(torch.zeros(1, NUM_ACTIONS), torch.zeros(1, NUM_ACTIONS))


def test_actor_critic_shapes():
    net = policy.MaskedActorCritic(in_dim=14)
    obs = torch.randn(5, 14)
    mask = torch.ones(5, NUM_ACTIONS)
    logits, value = net(obs, mask)
    assert logits.shape == (5, NUM_ACTIONS)
    assert value.shape == (5,)
