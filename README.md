# AI Pokémon Battle Trainer

A [Carleton AI Society](https://carletonai.com) project: teach an AI to battle Pokémon from scratch, then put it on the real [Pokémon Showdown](https://pokemonshowdown.com) ladder against people. We start with Gen 1 random battles.

## Join

Everything happens in `#pokemon-battle-trainer` on the [CAIS Discord](https://discord.gg/gCs3v653de). Ask Jeremy there to add you to this repo, and react ⚡ in `#roles` for meeting pings.

## Setup

You need [Git](https://git-scm.com), [Python](https://www.python.org) 3.10+ and [Node.js](https://nodejs.org) 22.18+. On Windows, use Command Prompt. On macOS and Linux, type `python3` instead of `python`.

```bash
git clone https://github.com/carletonai/pokemon-battle-trainer
cd pokemon-battle-trainer
```

## Download real battles

```bash
python download_replays.py
```

This saves 100 recent Gen 1 random-battle replays to `data/replays/`. Watch one at `https://replay.pokemonshowdown.com/<file name without .json>`.

## Run a battle

Start the battle server and leave it running:

```bash
git clone --depth 1 https://github.com/smogon/pokemon-showdown
cd pokemon-showdown
node pokemon-showdown start --no-security
```

The first start takes a couple of minutes. It is ready when it prints `Worker 1 now listening on 0.0.0.0:8000`. Ignore the npm warnings and any REPL errors.

Then open a second terminal and `cd` into the `pokemon-battle-trainer` folder:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python random_battle.py
```

Two bots play one battle with random moves. You get the winner and a replay in `data/battles/` to open in your browser.

## Run the arena

```bash
python arena.py
```

The three built-in bots play 500 battles per pair, which takes about a minute. You get every bot's win rate. Add your own bot to `BOTS` in `arena.py` to rank it.

## The plan

- **Arena** runs battles and keeps score.
- **Ghosts** are bots that copy strong human players, learned from replays.
- **Player** is the bot we train by having it battle itself.
- **Coach** picks what the Player practises.

Good first reading:

- [Showdown's battle protocol](https://github.com/smogon/pokemon-showdown/blob/master/sim/SIM-PROTOCOL.md): how to read a replay.
- [poke-env](https://poke-env.readthedocs.io/): the Python library our bots use.
- [Metamon](https://github.com/UT-Austin-RPL/metamon): the prior work we build on.

## Contributing

Branch from `main`, open a pull request and get one review. Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/), like `feat(data): add a replay parser`.

[MIT](LICENSE) license. Not affiliated with Nintendo, Game Freak or The Pokémon Company.
