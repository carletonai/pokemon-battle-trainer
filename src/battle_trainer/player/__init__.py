"""The Player: the bot we train (workstream: Player).

    env        a poke-env ``SinglesEnv`` for Gen 1 with our observation and reward
    encoder    the state encoder: both teams, what the opponent has revealed, the field
    policy     action-mask helper for code outside SB3 (imitation loss, evaluation)
    ppo        MaskablePPO (Stable-Baselines3) entry point and the env adapter it needs
    self_play  the opponent pool (past selves, ghosts, bots) and the training loop

Week-4 milestone: beats the max-damage bot from scratch. Week 8: beats the heuristic bot.
"""
