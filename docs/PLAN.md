# AI Pokémon Battle Trainer: the plan

From the CAIS planning notes of October 28 to November 2, 2026. This is the agreed framework; change it by PR with a reason.

## One line

We teach an AI to battle Pokémon from scratch and put it on the real Pokémon Showdown ladder against people.

## Why this game

Most members already know how to play, so everyone can judge whether the bot is any good, and the ladder gives an honest score against humans. An earlier plan around a Kaggle game nobody knew was dropped for exactly that reason.

This is a known research testbed, and we say so: Metamon (UT Austin, 2025) trained transformers of up to 200M parameters by imitation and offline RL on 3.5M reconstructed human battles and reached the top 10% of players. Our edge is laptop scale, live self-play, a coach that picks sparring and builds teams, and a bot members can battle at the showcase.

## The six lines

| Line | AI Pokémon Battle Trainer |
| --- | --- |
| Objective | Beats the built-in bots by week 4, holds a winning record against humans by week 8, reaches the top 10% of the Gen 1 random-battle ladder by week 12; stretch: a coach-built team that wins in Gen 1 OU |
| Arena & data | Pokémon Showdown (open-source simulator; headless for training, the server for the ladder) through poke-env (Python, MIT, Gymnasium API); libpkmn for fast Gen 1 training; public replays plus Metamon's open dataset of reconstructed human battles |
| Baseline | poke-env's built-in bots (random, max damage, simple heuristics), then Metamon's released agents on our local server, then humans. Published bars: top 10% of active players (Metamon, Gens 1-4 OU) and rank 8 at 1693 Elo (MIT thesis, Gen 4 random battles) |
| Metric | Win rate over 500-battle panels against each bot and ghost; Elo and GXE on the official ladder, tracked weekly under one CAIS account |
| Deliverable | The bot live on the ladder; a rating page with replay links on carletonai.com; the ghost pack released; code on the carletonai GitHub; a showcase night where members battle it |
| Roles | Five workstreams: Arena, Ghosts, Player, Coach, Engine speed |

## Four parts

- **Ghosts.** Imitation copies of strong human players, learned from public Showdown replays. They set the bar and let us test against "a 1400 human" offline.
- **Player.** The bot we build. It learns by battling itself millions of times on a simulator we run on our own laptops.
- **Coach.** A second, simpler learner that picks the Player's sparring partners and starting situations and, in team formats, builds its team. The research bet.
- **Arena.** Runs the battles, keeps an Elo ladder of bots, and tracks the real rating. The human ladder is the final exam.

## Workstreams

| Stream | Builds | Week-4 milestone | Good for |
| --- | --- | --- | --- |
| Arena | Local Showdown servers, battle runner, 500-battle panels, Elo among bots, a ladder runner that logs rating and replay links to a carletonai.com page | Ladder v0 with the built-in bots, rating page live | Python + web; the best first stream for new members |
| Ghosts | Replay scraper and parser (Metamon's reconstruction pipeline) → (battle state, move) dataset → one imitation bot per rating band | One ghost that beats the heuristic bot | Supervised learning, pandas, PyTorch |
| Player | State encoder over both teams and what the opponent has revealed; action masking over 4 moves plus switches; PPO self-play against a pool of past selves, ghosts and bots | Beats the max-damage bot from scratch; the heuristic bot by week 8 | RL, PyTorch |
| Coach | Sparring curriculum (which opponents and starting positions); for OU, a team builder scored by the Player's win rate | Random sparring mix matches the fixed-opponent win rate | RL reading; runs the experiments |
| Engine speed | libpkmn through the oak Python package for throughput, Showdown's headless CLI for validation, the server only for the ladder | Training runs with no server in the loop | Systems, C or Zig, profiling |

Each milestone stands on its own if the others slip. Code lives in the matching subpackage of `src/battle_trainer/`; see [WORKSTREAMS.md](WORKSTREAMS.md) for first tasks.

## Term plan

Twelve weeks in three phases. A phase ends when its gate is met.

1. **Weeks 1-4, stand up.** Server and poke-env on every laptop, replay parser and first ghost, Player beating the built-in bots. *Gate: beats the built-in bots.*
2. **Weeks 5-8, beat the ghosts.** Opponent pool of past selves, Coach v0 (random sparring mix as the baseline), fast engine, first ladder runs. *Gate: a winning record against humans.*
3. **Weeks 9-12, climb and showcase.** Weekly ladder runs, rating page, OU stretch, write-up and showcase night. *Gate: top 10% of the Gen 1 random-battle ladder; a coach-built team that wins in OU as the stretch.*

Assumptions: a 12-week term, 8-15 members, members' laptops plus Kaggle Notebooks for compute, one registered Showdown account for ladder runs, and a pinned Showdown commit and poke-env version behind every reported result.

## Engine tiers

Nobody plays games by hand. Pokémon Showdown is the engine; the "server" is a wrapper around it so humans and bots can connect. Three tiers, fastest last:

| Tier | What it is | Used for |
| --- | --- | --- |
| Showdown server + poke-env | The public simulator's server run locally with rate limits off; poke-env hands a Python bot the battle state and takes back a move. Ships three built-in bots | Development, the bot ladder, and the official ladder against humans |
| Headless Showdown | `pokemon-showdown simulate-battle`: the same simulator over stdin/stdout, one subprocess per battle, reproducible with a seed, no server | Validation and training without websocket round trips |
| libpkmn via oak | A Zig battle engine that, with one build flag, matches Showdown's Gen 1 behaviour exactly; oak wraps it in Python | Training throughput. Gen 1 only, wheels only for x86-64 Linux (glibc 2.34+), and libpkmn builds only against the Zig master release, so budget a week of toolchain work |

## Formats, in order

The code is the same; what changes is where the team comes from and the size of the embeddings.

1. **Gen 1 random battles.** Showdown hands each player six random Pokémon from the original 151 with set moves. Small roster, no team building, long battles with lots of hidden information, a live human ladder, and the only generation with a tensor-speed engine.
2. **Gen 1 OU.** Bring your own six from the allowed tier, so the Coach starts building teams. Metamon's dataset, team sets and checkpoints make it the best-benchmarked format there is.
3. **Gen 9.** Next semester. About a thousand species, abilities, items and Terastallization, and the busiest ladder on the site.

## The Coach

The Coach does not play; it decides what the Player practises. Plain self-play is a boxer sparring only his own clone. The Coach watches where the Player loses and picks drills on three knobs: which opponent (a past self, a ghost, a bot), which situation (start battles from spots the Player keeps losing), and which team (OU only). Under the hood it is a scoreboard of loss rates and a rule like "sample what we lose to most", not a neural net. The idea is curriculum learning; the lineage is AlphaStar's league with its exploiter agents. Metamon's self-play was deliberately plain, so applying this to Pokémon, and using it to build teams, is the part nobody has published.

Guardrails:

- The Coach controls at most half the training diet; the other half stays uniform.
- Progress is measured on a held-out panel the Coach can never pick from, plus the human ladder. If the drilled matchup improves while the exam drops, dial it back.
- A weakness has to show over 500 battles before the Coach acts, and it moves on once fixed.
- Random sparring is the baseline through week 8. The Coach stays only if it beats random by then. The project still succeeds on bots, ghosts and the ladder without it.

## What will hurt

In the order the team will hit them.

- **Throughput, not GPUs.** Showdown is JavaScript, and through the server every move is a websocket round trip. Train on libpkmn or the headless CLI with many battles in parallel and batched inference; keep the server for ladder runs. Otherwise a million-battle run takes weeks.
- **Hidden information.** In random battles the opponent's team appears one switch at a time and moves only as they are used. Track what has been revealed, and use Showdown's published random-battle sets to narrow what each species can carry.
- **Simultaneous moves and luck.** Both players choose at once; damage rolls, critical hits and accuracy add noise. Evaluate on 500-battle panels, not 50.
- **Small action space, large state space.** At most nine legal actions (4 moves, up to 5 switches), but species, moves, items and abilities need learned embeddings. Gen 1 keeps that to 151 species and a short move list.
- **Imitation's limits.** A ghost copies a human's moves without their reasoning, and a replay shows only the spectator's view; rebuilding the player's view is the hard part, which is why Metamon's pipeline exists.
- **Self-play traps.** Pure self-play drifts into habits that exploit its own weaknesses, not humans'. Keep a pool of past selves, ghosts and bots, and check against the ladder early.
- **Ladder etiquette and IP.** One registered account, no stalling the turn timer, keep the bot out of chat rooms. Bots are permitted on Showdown because they have no advantage over human players; the permission rests on that. The public page shows the bot's name, rating and replay links, never Pokémon artwork or sprites.
- **The Coach may not pay off.** A sparring curriculum sometimes loses to uniform sampling. The project still succeeds without it.

## Offline and online Elo

Offline Elo is our own ladder on our laptops: bots, ghosts and Metamon's agents ranking each other over thousands of cheap battles. Online Elo is the official Showdown number against real people. The scales are not comparable: local Elo only says who beats whom on our ladder; the online one is anchored to the whole player base, and a new account starts at 1000. Ghosts cloned from 1400-rated humans bridge the two.

## Sources

- poke-env: [docs](https://poke-env.readthedocs.io/), [GitHub](https://github.com/hsahovic/poke-env)
- Pokémon Showdown: [GitHub](https://github.com/smogon/pokemon-showdown), [SIMULATOR.md](https://github.com/smogon/pokemon-showdown/blob/master/sim/SIMULATOR.md)
- libpkmn: [pkmn/engine](https://github.com/pkmn/engine), [design notes](https://github.com/pkmn/engine/blob/main/docs/DESIGN.md); oak: [GitHub](https://github.com/pokemon-labs/oak), [PyPI](https://pypi.org/project/oak-lab/)
- Stable-Baselines3: [docs](https://stable-baselines3.readthedocs.io/), [MaskablePPO in sb3-contrib](https://sb3-contrib.readthedocs.io/en/master/modules/ppo_mask.html)
- Metamon: [GitHub](https://github.com/UT-Austin-RPL/metamon), [paper (RLJ 2025)](https://arxiv.org/abs/2504.04395), [parsed replays on Hugging Face](https://huggingface.co/datasets/jakegrigsby/metamon-parsed-replays)
- [MIT thesis: RL agent at rank 8 on the Gen 4 random-battles ladder](https://dspace.mit.edu/handle/1721.1/153888)
- [AlphaStar](https://deepmind.google/research/breakthroughs/alphastar/), the league and exploiter agents behind the Coach
- Bots on the ladder: [Smogon staff answer](https://www.smogon.com/forums/goto/post?id=10189991)
