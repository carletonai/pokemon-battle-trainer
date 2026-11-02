"""The Coach: decides what the Player practises (workstream: Coach).

The Coach does not play. It watches where the Player loses and picks drills on three knobs:
which opponent (a past self, a ghost, a bot), which situation (start battles from spots the
Player keeps losing), and, in team formats, which team. Under the hood it is a scoreboard
of loss rates and a rule like "sample what we lose to most", not a neural net.

Guardrails, agreed in planning (docs/PLAN.md, "Coach"):
  * the Coach controls at most half the training diet; the other half stays uniform;
  * progress is measured on a held-out panel the Coach can never pick from, plus the ladder;
  * a weakness must show over 500 battles before the Coach acts, and it moves on once fixed;
  * uniform sampling is the baseline through week 8; the Coach stays only if it beats it.

Week-4 milestone: the random sparring mix matches the fixed-opponent win rate.
"""
