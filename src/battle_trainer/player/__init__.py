"""The Player: the bot we train (workstream: Player).

    env        a poke-env ``SinglesEnv`` for Gen 1 with our observation and reward
    encoder    the state encoder: both teams, what the opponent has revealed, the field
    policy     actor-critic network with action masking over 4 moves + up to 5 switches
    ppo        the PPO update
    self_play  the opponent pool (past selves, ghosts, bots) and the training loop

Week-4 milestone: beats the max-damage bot from scratch. Week 8: beats the heuristic bot.
"""
