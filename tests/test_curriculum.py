import pytest

from battle_trainer.coach.curriculum import mix_with_uniform, uniform


def test_uniform_sums_to_one():
    p = uniform(["a", "b", "c", "d"])
    assert sum(p.values()) == pytest.approx(1.0)
    assert all(v == pytest.approx(0.25) for v in p.values())


def test_uniform_rejects_empty_pool():
    with pytest.raises(ValueError):
        uniform([])


def test_mix_keeps_uniform_floor():
    # The Coach wants everything on "ghost"; the floor keeps half the diet uniform.
    p = mix_with_uniform({"random": 0.0, "max_damage": 0.0, "ghost": 1.0}, floor=0.5)
    assert sum(p.values()) == pytest.approx(1.0)
    assert p["random"] == pytest.approx(0.5 / 3)
    assert p["ghost"] == pytest.approx(0.5 / 3 + 0.5)


def test_mix_with_zero_weights_is_uniform():
    p = mix_with_uniform({"a": 0.0, "b": 0.0}, floor=0.5)
    assert p == pytest.approx({"a": 0.5, "b": 0.5})
