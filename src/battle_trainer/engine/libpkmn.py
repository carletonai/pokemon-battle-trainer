"""libpkmn via oak (tier 3): tensor-speed Gen 1 battles for training throughput.

libpkmn (https://github.com/pkmn/engine) is a Zig battle engine that, built with the
Showdown-compatibility flag, matches Pokémon Showdown's Gen 1 behaviour exactly. ``oak``
(https://github.com/pokemon-labs/oak, PyPI ``oak-lab``) wraps it for Python. Install with
``uv sync --extra engine``. Wheels exist only for x86-64 Linux with glibc 2.34+ (Ubuntu
22.04 or newer); there are no ARM or macOS builds.

Known costs, from the planning notes: Gen 1 only, Linux wheels only, and libpkmn builds
only against the Zig master release, so budget a week for toolchain work.

TODO(engine): implement a ``LibpkmnBackend`` with the same interface as the headless tier.
  1. Confirm ``oak`` installs and runs a random Gen 1 battle on a club laptop.
  2. Map libpkmn's state and choice representation to the Player's observation and
     action space (``battle_trainer.player.env``). Keep one state encoder for all tiers.
  3. Cross-check a few hundred seeded battles against headless Showdown to prove parity.
  4. Measure battles/second; this number is the workstream's headline.
"""

from __future__ import annotations


class LibpkmnBackend:
    """Gen 1 battles on libpkmn. Not implemented yet."""

    def __init__(self) -> None:
        raise NotImplementedError("TODO(engine): see module docstring")
