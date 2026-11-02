# AI Pokémon Battle Trainer

Teach an AI to battle Pokémon from scratch and put it on the real [Pokémon Showdown](https://pokemonshowdown.com) ladder against people. A [Carleton AI Society](https://carletonai.com) reinforcement-learning project. Gen 1 random battles first.

> **Status: scaffold.** The structure, tooling and plan are here. The parts are stubs with `TODO(<workstream>)` notes that say what to build and how. Pick a workstream in [docs/WORKSTREAMS.md](docs/WORKSTREAMS.md) and start.

## The idea

The bot learns by battling itself millions of times on a simulator we run on our own laptops. The public ladder is the final exam. Four parts:

- **Ghosts** are imitation copies of strong human players, learned from public Showdown replays. They set the bar and let us test against "a 1400 human" offline.
- **Player** is the bot we build. It learns by PPO self-play against a pool of past selves, ghosts and bots.
- **Coach** is a second, simpler learner that picks the Player's sparring partners and starting situations and, in team formats, builds its team. This is the research bet.
- **Arena** runs the battles, keeps an Elo ladder of bots, and tracks the real rating.

Opponents go built-in bots, then ghosts, then Metamon's released agents, then real people. The full plan, with the week-by-week gates and the list of what will hurt, is in [docs/PLAN.md](docs/PLAN.md).

## Getting started

You need:

- **Python 3.12+** and [uv](https://docs.astral.sh/uv/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`, or `pip install uv`)
- **Node.js 22.18+** to run the simulator ([nodejs.org](https://nodejs.org))
- **git**

Then, from a clone of this repo:

```bash
# 1. Python environment and git hooks
uv sync
uv run pre-commit install

# 2. Pokémon Showdown, built at the commit pinned in third_party/SHOWDOWN_COMMIT
scripts/setup_showdown.sh

# 3. A local server, in its own terminal. Leave it running.
scripts/start_showdown.sh

# 4. Two built-in bots battle on it. If this prints a win rate, the stack works.
uv run python scripts/smoke_battle.py --battles 10

# 5. Tests. Those that need the server are skipped when it is not running.
uv run pytest
```

`make help` lists the same steps as Make targets (`make setup`, `make showdown`, `make server`, `make smoke`, `make test`, `make lint`, `make format`).

To watch bots battle live, open `https://play.pokemonshowdown.com/~~localhost:8000` in a browser: the official client connecting to your local server.

**Windows:** the shell scripts need Git Bash or WSL. The Python side runs natively.

**GPU:** on Linux, `uv sync` installs CPU-only PyTorch (a tenth of the size, and training here is bound by simulator speed, not GPUs). For a CUDA build, change the `[tool.uv.sources]` block in `pyproject.toml` to a CUDA index per [uv's PyTorch guide](https://docs.astral.sh/uv/guides/integration/pytorch/), or use Kaggle Notebooks for free GPU hours, which is the plan.

**libpkmn (fast Gen 1 engine):** `uv sync --extra engine` installs `oak`. Linux only; see `src/battle_trainer/engine/libpkmn.py`.

## Repository map

```
src/battle_trainer/
  config.py        constants a result depends on: format, panel size, action space
  engine/          simulator tiers: server (poke-env), headless CLI, libpkmn via oak
  arena/           built-in bots, 500-battle panels, Elo ladder, official-ladder runner
  ghosts/          replay scraping and parsing, imitation dataset, GhostPlayer
  player/          Gen 1 env, state encoder, masked actor-critic, PPO, self-play pool
  coach/           opponent sampling (uniform baseline, weakness-weighted), team builder
scripts/           setup_showdown.sh, start_showdown.sh, smoke_battle.py
tests/             unit tests; tests marked `showdown` need the local server
docs/              PLAN.md (the plan), WORKSTREAMS.md (where to start)
third_party/       SHOWDOWN_COMMIT pin; the Showdown checkout lives here, git-ignored
```

Every stub says what it is for and lists numbered TODO steps. `grep -rn "TODO(" src/` is the backlog.

## Workstreams

| Stream | Package | Week-4 milestone | Good for |
| --- | --- | --- | --- |
| Arena | `battle_trainer.arena` | Ladder v0 with the built-in bots, rating page live | Python + web; the best first stream for new members |
| Ghosts | `battle_trainer.ghosts` | One ghost that beats the heuristic bot | Supervised learning, pandas, PyTorch |
| Player | `battle_trainer.player` | Beats the max-damage bot from scratch | RL, PyTorch |
| Coach | `battle_trainer.coach` | Random sparring mix matches the fixed-opponent win rate | RL reading; runs the experiments |
| Engine speed | `battle_trainer.engine` | Training runs with no server in the loop | Systems, C or Zig, profiling |

Details and first tasks per stream: [docs/WORKSTREAMS.md](docs/WORKSTREAMS.md). How to contribute: [CONTRIBUTING.md](CONTRIBUTING.md).

## Rules we hold ourselves to

- **Reproducible numbers.** Every reported result names the Showdown commit (`third_party/SHOWDOWN_COMMIT`) and the poke-env version (`uv.lock`) it was measured with.
- **500-battle panels.** Luck is large in Pokémon. Win rates come with a confidence interval (`arena.panel`), never from 50 battles.
- **One ladder account.** Ladder runs use the club's registered Showdown account, never stall the timer, and stay out of chat rooms. Bots are allowed on the ladder because they see what a human sees; keep it that way.
- **No artwork.** The public rating page shows the bot's name, rating and replay links. No Pokémon sprites or art in this repo or on the page.
- **Nothing big in git.** Replays, datasets, checkpoints and run logs go in the git-ignored `data/`, `checkpoints/` and `runs/` folders.

## Reading

- [poke-env documentation](https://poke-env.readthedocs.io/) and [repo](https://github.com/hsahovic/poke-env): the Python layer between a bot and Showdown
- [Pokémon Showdown](https://github.com/smogon/pokemon-showdown), especially [sim/SIMULATOR.md](https://github.com/smogon/pokemon-showdown/blob/master/sim/SIMULATOR.md) for the headless protocol
- [Metamon](https://github.com/UT-Austin-RPL/metamon) ([paper](https://arxiv.org/abs/2504.04395)): the prior work this project builds on and measures against
- [libpkmn](https://github.com/pkmn/engine) and [oak](https://github.com/pokemon-labs/oak): the fast Gen 1 engine
- [AlphaStar](https://deepmind.google/research/breakthroughs/alphastar/): the league and exploiter agents the Coach idea comes from

## Community

Everything about the project lives in `#pokemon-battle-trainer` on the CAIS Discord. React ⚡ in `#roles` to get pinged for meetings. Ping Jeremy in the channel for access to this repo.

This is a student project with no affiliation to Nintendo, Game Freak or The Pokémon Company. Pokémon Showdown and poke-env are MIT-licensed open-source projects.
