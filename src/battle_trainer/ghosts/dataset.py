"""Imitation dataset: the parsed (state, action) pairs, bucketed by rating band.

TODO(ghosts): implement ``ReplayDataset`` (a ``torch.utils.data.Dataset``).
  1. Load parsed pairs from ``data/parsed/<format>/`` (parquet or ``.npz`` shards).
  2. Filter by rating band and by minimum battle length.
  3. Hold out whole battles, never individual turns, for validation.
"""

from __future__ import annotations

from pathlib import Path


class ReplayDataset:
    """(observation, action) pairs from parsed replays. Not implemented yet."""

    def __init__(self, root: Path, rating_band: tuple[int, int] | None = None) -> None:
        self.root = root
        self.rating_band = rating_band
        raise NotImplementedError("TODO(ghosts): see module docstring")
