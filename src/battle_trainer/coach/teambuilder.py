"""Team builder for Gen 1 OU (stretch goal): search for teams the Player wins with.

Only matters once we leave random battles. Gen 1 OU is the best-benchmarked format there
is (Metamon's dataset, team sets and checkpoints), which is why it is next.

TODO(coach): implement a ``poke_env.teambuilder.Teambuilder`` subclass.
  1. Start from Metamon's Gen 1 OU team sets and published Smogon sets as the candidate pool.
  2. Score a team by the Player's win rate over a 500-battle panel with that team.
  3. Simple search first (hill climbing over one slot at a time); fancier later if it pays.
"""

from __future__ import annotations

from poke_env.teambuilder import Teambuilder


class CoachTeambuilder(Teambuilder):
    """Teams chosen by the Coach. Not implemented yet."""

    def yield_team(self) -> str:
        raise NotImplementedError("TODO(coach): see module docstring")
