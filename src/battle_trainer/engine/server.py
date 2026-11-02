"""Connection settings for Showdown servers (tier 1: server + poke-env)."""

from __future__ import annotations

import os

from poke_env.ps_client import (
    AccountConfiguration,
    ServerConfiguration,
    ShowdownServerConfiguration,
)

from battle_trainer.config import LOCAL_SERVER_HOST, LOCAL_SERVER_PORT


def local_server(
    host: str = LOCAL_SERVER_HOST, port: int = LOCAL_SERVER_PORT
) -> ServerConfiguration:
    """The server started by ``scripts/start_showdown.sh``.

    With ``--no-security`` the local server needs no login, so players can use
    auto-generated usernames (pass no ``account_configuration``).
    """
    return ServerConfiguration(
        websocket_url=f"ws://{host}:{port}/showdown/websocket",
        authentication_url="https://play.pokemonshowdown.com/action.php?",
    )


def official_server() -> ServerConfiguration:
    """play.pokemonshowdown.com, for ladder runs against humans. Needs a registered account."""
    return ShowdownServerConfiguration


def ladder_account() -> AccountConfiguration:
    """The club's registered Showdown account, read from the environment.

    Set ``PS_USERNAME`` and ``PS_PASSWORD`` in your shell or a local ``.env`` file
    (which is git-ignored). One account for all ladder runs, so the rating history
    stays in one place. Never commit credentials.
    """
    username = os.environ.get("PS_USERNAME")
    password = os.environ.get("PS_PASSWORD")
    if not username or not password:
        raise RuntimeError("PS_USERNAME and PS_PASSWORD must be set for ladder runs")
    return AccountConfiguration(username, password)
