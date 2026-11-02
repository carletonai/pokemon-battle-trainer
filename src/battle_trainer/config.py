"""Project-wide constants.

Anything a reported result depends on belongs here or in a config file, never
hard-coded in a script, so that a number in a write-up can be reproduced.
"""

# First target format. The code is format-agnostic; what changes between formats is
# where the team comes from and the size of the embeddings (docs/PLAN.md, "Formats").
BATTLE_FORMAT = "gen1randombattle"
GEN = 1

# Evaluation: win rates are reported over panels of this many battles. Luck is large in
# Pokémon, so 50-battle numbers are noise (docs/PLAN.md, "What will hurt").
PANEL_SIZE = 500

# Local Showdown server started by scripts/start_showdown.sh.
LOCAL_SERVER_HOST = "localhost"
LOCAL_SERVER_PORT = 8000

# Action space, from poke-env's SinglesEnv for a generation with no gimmicks:
# actions 0-5 switch to team slot, 6-9 use move 1-4. Gen 1 has no mega/Z/dynamax/tera.
NUM_SWITCH_ACTIONS = 6
NUM_MOVE_ACTIONS = 4
NUM_ACTIONS = NUM_SWITCH_ACTIONS + NUM_MOVE_ACTIONS
