"""Every module imports cleanly, so a broken stub is caught before anyone builds on it."""

import importlib
import pkgutil

import pytest

import battle_trainer

MODULES = sorted(
    m.name for m in pkgutil.walk_packages(battle_trainer.__path__, prefix="battle_trainer.")
)


@pytest.mark.parametrize("name", MODULES)
def test_module_imports(name: str):
    try:
        importlib.import_module(name)
    except ModuleNotFoundError as exc:
        if exc.name == "torch":
            pytest.skip("torch is not installed")
        raise


def test_all_workstreams_present():
    for stream in ("engine", "arena", "ghosts", "player", "coach"):
        assert f"battle_trainer.{stream}" in MODULES
