"""Shared test configuration.

Tests marked ``@pytest.mark.showdown`` need a local Pokémon Showdown server. They are
skipped automatically when no Showdown server answers on localhost:8000, so ``pytest``
always runs on a fresh clone. Start a server with ``scripts/start_showdown.sh`` to include
them. Set ``SHOWDOWN_REQUIRED=1`` (CI does) to fail instead of skipping.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

import pytest

from battle_trainer.config import LOCAL_SERVER_HOST, LOCAL_SERVER_PORT


def _showdown_server_up(host: str, port: int, timeout: float = 1.0) -> bool:
    """True only for a Showdown server, not just anything on the port.

    Showdown serves its websocket through sockjs, which answers ``/showdown/info`` with
    JSON that includes ``"websocket": true``. A plain TCP probe would also match a web
    dev server on 8000, and poke-env then waits forever for a login that never comes.
    """
    try:
        with urllib.request.urlopen(f"http://{host}:{port}/showdown/info", timeout=timeout) as r:
            return bool(json.load(r).get("websocket"))
    except (urllib.error.URLError, OSError, ValueError):
        return False


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if os.environ.get("SHOWDOWN_REQUIRED") == "1":
        return
    if _showdown_server_up(LOCAL_SERVER_HOST, LOCAL_SERVER_PORT):
        return
    skip = pytest.mark.skip(
        reason=f"no Showdown server on {LOCAL_SERVER_HOST}:{LOCAL_SERVER_PORT} "
        "(run scripts/start_showdown.sh)"
    )
    for item in items:
        if "showdown" in item.keywords:
            item.add_marker(skip)
