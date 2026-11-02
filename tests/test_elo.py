import pytest

from battle_trainer.arena.elo import DEFAULT_RATING, EloLadder, expected_score, update


def test_equal_ratings_expect_half():
    assert expected_score(1500, 1500) == pytest.approx(0.5)


def test_higher_rating_expects_more():
    assert expected_score(1600, 1400) > 0.75


def test_update_moves_toward_result():
    assert update(1500, 1500, 1.0) == pytest.approx(1516)
    assert update(1500, 1500, 0.0) == pytest.approx(1484)
    assert update(1500, 1500, 0.5) == pytest.approx(1500)


def test_update_rejects_bad_score():
    with pytest.raises(ValueError):
        update(1500, 1500, 1.5)


def test_ladder_is_zero_sum_and_sorted():
    ladder = EloLadder()
    ladder.record("max_damage", "random", 1.0)
    ladder.record("max_damage", "random", 1.0)
    total = sum(ladder.ratings.values())
    assert total == pytest.approx(2 * DEFAULT_RATING)
    assert [name for name, _ in ladder.standings()] == ["max_damage", "random"]
