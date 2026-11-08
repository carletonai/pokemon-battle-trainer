# AI Pokémon Battle Trainer

A [Carleton AI Society](https://carletonai.com) project: teach an AI to battle Pokémon from scratch, then put it on the real [Pokémon Showdown](https://pokemonshowdown.com) ladder against people. We start with Gen 1 random battles.

We haven't started building yet. For now, the one thing to do here is get some real battles onto your laptop and look at them.

## Join

Everything happens in `#pokemon-battle-trainer` on the CAIS Discord. React ⚡ in `#roles` to get meeting pings, and ask Jeremy there to add you to this repo.

## Get the data

You need Python 3.10 or newer. There is nothing to install.

```bash
git clone https://github.com/carletonai/pokemon-battle-trainer
cd pokemon-battle-trainer
python download_replays.py
```

That saves 100 recent public Gen 1 random-battle replays to `data/replays/`, one JSON file each. The battle is in the `log` field. Run `python download_replays.py --help` to get more, filter by rating, or pick another format. The `data/` folder is git-ignored, so downloads never end up in a commit.

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

Branch from `main`, open a pull request, and get one review before merging. Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/), for example `feat(data): add a rating filter`.

## License

[MIT](LICENSE). A student project with no affiliation to Nintendo, Game Freak or The Pokémon Company.
