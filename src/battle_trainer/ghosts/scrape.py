"""Download public Gen 1 random-battle replays.

Sources:
  * replay.pokemonshowdown.com has a JSON search API (``/search.json?format=gen1randombattle``)
    and serves each replay's log at ``/<id>.log``. Be polite: one request at a time, a
    small delay, and cache everything to ``data/replays/`` (git-ignored).
  * Metamon's parsed-replay dataset: https://huggingface.co/datasets/jakegrigsby/metamon-parsed-replays
    (reconstructed player-view trajectories; check which formats are covered).

TODO(ghosts): implement ``scrape_replays``.
  1. Page through the search API for the target format, newest first, and store
     ``(id, uploadtime, rating, players)`` metadata in a CSV or parquet file.
  2. Download the raw ``.log`` for each id into ``data/replays/<format>/<id>.log``.
  3. Keep the player ratings when the replay has them; ghosts are built per rating band.
"""

from __future__ import annotations

from pathlib import Path


def scrape_replays(battle_format: str, out_dir: Path, limit: int | None = None) -> int:
    """Download replays for ``battle_format`` into ``out_dir``; return how many. Not implemented."""
    raise NotImplementedError("TODO(ghosts): see module docstring")
