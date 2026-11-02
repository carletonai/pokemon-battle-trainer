"""Shared test configuration.

Tests marked ``@pytest.mark.showdown`` need a local Pokémon Showdown server. They are
skipped automatically when nothing is listening on localhost:8000, so ``pytest`` always
runs on a fresh clone. Start a server with ``scripts/start_showdown.sh`` to include them.
"""

from __future__ import annotations

import socket

import pytest

from battle_trainer.config import LOCAL_SERVER_HOST, LOCAL_SERVER_PORT


def _server_listening(host: str, port: int, timeout: float = 0.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if _server_listening(LOCAL_SERVER_HOST, LOCAL_SERVER_PORT):
        return
    skip = pytest.mark.skip(
        reason=f"no Showdown server on {LOCAL_SERVER_HOST}:{LOCAL_SERVER_PORT} "
        "(run scripts/start_showdown.sh)"
    )
    for item in items:
        if "showdown" in item.keywords:
            item.add_marker(skip)
