"""Ghosts: imitation copies of human players (workstream: Ghosts).

A ghost is a bot trained by supervised learning on public Showdown replays to play like
the humans in one rating band (say 1100-1300, 1300-1500). Ghosts set the bar and let us
test against "a 1400 human" offline, thousands of times, for free.

Pipeline:  scrape -> parse -> dataset -> imitation

Know going in: a replay shows the spectator's view, not the player's. Rebuilding what the
player could see (their own team, what the opponent had revealed so far) is the hard part
of parsing. Metamon (UT Austin, 2025) published a reconstruction pipeline and a parsed
dataset on Hugging Face; read theirs before writing ours.

Week-4 milestone: one ghost that beats the heuristic bot.
"""
