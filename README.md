# AI Pokémon Battle Trainer

Teach an AI to battle Pokémon from scratch and put it on the real [Pokémon Showdown](https://pokemonshowdown.com) ladder against people. A [Carleton AI Society](https://carletonai.com) reinforcement-learning project, starting with Gen 1 random battles.

The repo is a scaffold: the structure and tooling are in place, and the parts are stubs with `TODO` notes that say what to build. Pick one and start.

## Quick start

You need Python 3.11+, [uv](https://docs.astral.sh/uv/) and [Node.js](https://nodejs.org) 22.18+.

```bash
uv sync && uv run pre-commit install    # Python environment and git hooks
scripts/setup_showdown.sh               # build the Pokémon Showdown simulator
scripts/start_showdown.sh               # local server; leave it running in its own terminal
uv run python scripts/smoke_battle.py   # two built-in bots battle on it. Prints a win rate? You're set.
uv run pytest                           # tests; the ones that need the server skip when it is down
```

`make help` lists the same steps as Make targets. Open http://localhost:8000 to watch bots battle in the browser (it redirects to the official client, pointed at your server).

Two notes: on Linux, `uv sync` downloads PyTorch with CUDA (about 3 GB; `pyproject.toml` has a CPU-only switch), and on Windows the scripts need Git Bash or WSL.

## Pick a task

Five workstreams, one package each under `src/battle_trainer/`:

- **Arena** runs the battles and keeps score. Python; the best place to start.
- **Ghosts** are imitation copies of human players, trained from public replays. Supervised learning, PyTorch.
- **Player** is the bot we train, by PPO self-play. RL, PyTorch.
- **Coach** picks what the Player practises. RL reading; runs the experiments.
- **Engine** takes the server out of the training loop so it runs fast. Systems, profiling.

First tasks for each are in [docs/WORKSTREAMS.md](docs/WORKSTREAMS.md); the full plan is [docs/PLAN.md](docs/PLAN.md). Say which stream you're taking in `#pokemon-battle-trainer` on the CAIS Discord (react ⚡ in `#roles` for meeting pings; ask Jeremy there for repo access), then follow [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE). A student project with no affiliation to Nintendo, Game Freak or The Pokémon Company.
