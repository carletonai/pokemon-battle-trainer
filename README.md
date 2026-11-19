# AI Pokémon Battle Trainer

A [Carleton AI Society](https://carletonai.com) project: teach an AI to battle Pokémon from scratch, then put it on the real [Pokémon Showdown](https://pokemonshowdown.com) ladder against people. We start with Gen 1 random battles.

We are just getting started. There are two things to do here: get some real battles onto your laptop and look at them, then run a battle of your own.

## Join

Everything happens in `#pokemon-battle-trainer` on the [CAIS Discord](https://discord.gg/gCs3v653de). React ⚡ in `#roles` to get meeting pings, and ask Jeremy in the project channel to add you to this repo.

## Get the data

You need Git and Python 3.10 or newer (on macOS and Linux the command is `python3`). There is nothing else to install.

```bash
git clone https://github.com/carletonai/pokemon-battle-trainer
cd pokemon-battle-trainer
python download_replays.py
```

That saves 100 recent public Gen 1 random-battle replays to `data/replays/`, one JSON file each. The battle is in the `log` field; watch the same battle at `https://replay.pokemonshowdown.com/<id>`, where `<id>` is the file name without `.json`. Run `python download_replays.py --help` to get more, filter by rating, or pick another format. The `data/` folder is git-ignored, so downloads never end up in a commit.

## Run a battle

Battles run on a local [Pokémon Showdown](https://github.com/smogon/pokemon-showdown) server, and bots play on it through [poke-env](https://poke-env.readthedocs.io/). You also need [Node.js](https://nodejs.org) 22.18 or newer.

Start the server from this folder and leave it running:

```bash
git clone --depth 1 https://github.com/smogon/pokemon-showdown
cd pokemon-showdown
node pokemon-showdown start --no-security
```

The first start installs what it needs and takes a couple of minutes. It is ready when it prints `Worker 1 now listening on 0.0.0.0:8000`. `--no-security` lets bots log in without an account, which is fine on your own machine.

Then open a second terminal in this folder:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python random_battle.py
```

Two bots that pick random moves play one Gen 1 random battle. The script prints who won and saves a replay to `data/battles/` that you can open in a browser.

## The plan in one minute

- **Arena** runs battles and keeps score.
- **Ghosts** are bots that copy strong human players, learned from replays like these.
- **Player** is the bot we train by having it battle itself.
- **Coach** picks what the Player practises.

Good first reading:

- [Showdown's battle protocol](https://github.com/smogon/pokemon-showdown/blob/master/sim/SIM-PROTOCOL.md) explains how to read a replay's `log`.
- [poke-env](https://poke-env.readthedocs.io/) is the Python library bots use to play on Showdown.
- [Metamon](https://github.com/UT-Austin-RPL/metamon) is the prior work we build on.

## Contributing

Branch from `main`, open a pull request, and get one review before merging. Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/), for example `feat(data): add a replay parser`.

## License

[MIT](LICENSE). A student project with no affiliation to Nintendo, Game Freak or The Pokémon Company.
