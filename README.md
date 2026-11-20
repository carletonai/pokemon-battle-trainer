# AI Pokémon Battle Trainer

A [Carleton AI Society](https://carletonai.com) project: teach an AI to battle Pokémon from scratch, then put it on the real [Pokémon Showdown](https://pokemonshowdown.com) ladder against people. We start with Gen 1 random battles.

## Join

Everything happens in `#pokemon-battle-trainer` on the [CAIS Discord](https://discord.gg/gCs3v653de). React ⚡ in `#roles` for meeting pings, and ask Jeremy there for repo access.

## Setup

You need Git, Python 3.10+ and [Node.js](https://nodejs.org) 22.18+. On macOS and Linux, type `python3` instead of `python`.

```bash
git clone https://github.com/carletonai/pokemon-battle-trainer
cd pokemon-battle-trainer
```

## Download real battles

```bash
python download_replays.py
```

This saves 100 recent Gen 1 random-battle replays to `data/replays/`. To watch one, open `https://replay.pokemonshowdown.com/<id>`, where `<id>` is the file name without `.json`.

## Run a battle

Start the battle server and leave it running:

```bash
git clone --depth 1 https://github.com/smogon/pokemon-showdown
cd pokemon-showdown
node pokemon-showdown start --no-security
```

The first start takes a couple of minutes. It is ready when it prints `Worker 1 now listening on 0.0.0.0:8000`. Warnings and `logs/repl` errors around that line are harmless.

Then open a second terminal in the `pokemon-battle-trainer` folder:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows (cmd): .venv\Scripts\activate
pip install -r requirements.txt
python random_battle.py
```

Two bots play one battle with random moves. You get the winner and a replay in `data/battles/` to open in your browser.

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

[MIT](LICENSE) license. A student project, not affiliated with Nintendo, Game Freak or The Pokémon Company.
