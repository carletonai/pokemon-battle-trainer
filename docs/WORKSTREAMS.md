# Workstreams: where to start

Pick one, say so in `#pokemon-battle-trainer`, and take the first unclaimed task. Every stub in `src/battle_trainer/` carries a `TODO(<stream>)` list that goes into more detail than this page; `grep -rn "TODO(" src/` shows all of them.

Before anything else, get the stack running on your laptop ([README: Getting started](../README.md#getting-started)). The smoke battle proving the server, poke-env and the bots all talk to each other is the first thing every stream needs.

## Arena

*Runs the battles and keeps score. The best first stream for new members.*

Package: `battle_trainer.arena`. Already there: the built-in bots (`bots.py`), Elo (`elo.py`), panels with confidence intervals (`panel.py`).

1. Battle every built-in bot against every other over 500-battle panels and publish the table and Elo standings in `docs/` (the first "ladder v0").
2. Make `run_panel` run several battles concurrently (`max_concurrent_battles`) and measure battles per minute through the server. That number is the Engine stream's baseline too.
3. Implement `ladder.run_ladder` (`ladder.py`): play ranked games on the official server under the club account, log rating and replay links to JSONL.
4. The rating page on carletonai.com: a static JSON the page fetches, then a weekly job.

Week-4 milestone: ladder v0 with the built-in bots, rating page live.

## Ghosts

*Imitation copies of human players, one per rating band.*

Package: `battle_trainer.ghosts`. Pipeline: `scrape.py` → `parse.py` → `dataset.py` → `imitation.py`.

1. Read Metamon's replay-parsing code and dataset first; decide what to reuse.
2. Scrape a few thousand Gen 1 random-battle replays with ratings into `data/replays/`.
3. Parse one side of a replay into `(observation, action)` pairs with poke-env's `Battle` parser, using the Player's encoder and action indices so ghosts and Player share one action space.
4. Train a first ghost with cross-entropy over legal actions; evaluate it as a `GhostPlayer` on a 500-battle panel against the heuristic bot.

Week-4 milestone: one ghost that beats the heuristic bot.

## Player

*The bot we train.*

Package: `battle_trainer.player`. Already there: a Gen 1 `SinglesEnv` with a tiny v0 observation (`env.py`), action masking (`policy.mask_logits`), and a network skeleton.

1. Run `make_env(make_bot("random", start_listening=False))` against the local server and step it with random legal actions to see observations (`obs["observation"]`), masks (`obs["action_mask"]`) and rewards flow.
2. Decide hand-rolled PPO versus a library (`ppo.py` has the trade-off); say which in the channel.
3. Build the real state encoder (`encoder.py`): species, HP, status, boosts and revealed flags for all twelve slots, known moves with PP, field state. Use Showdown's random-battle sets as a prior for unrevealed species.
4. Train against the random bot, then the max-damage bot, from scratch. Report 500-battle panels with intervals.

Week-4 milestone: beats the max-damage bot from scratch. Week 8: the heuristic bot.

## Coach

*Decides what the Player practises.*

Package: `battle_trainer.coach`. Already there: the uniform baseline and the 50% uniform floor (`curriculum.py`).

1. Build the held-out exam panel: a fixed set of opponents and seeds the Coach can never sample from. Everything the Coach does is judged on it.
2. Implement `WeaknessSampler` with its guardrails (500-battle evidence, floor, move on once fixed).
3. Run the experiment: uniform mix versus Coach mix, same budget, same exam. Through week 8 uniform is the baseline; the Coach stays only if it wins.
4. Later: starting positions (resume battles from saved states), and for OU, `teambuilder.py`.

Week-4 milestone: random sparring mix matches the fixed-opponent win rate.

## Engine speed

*Training never waits on a server.*

Package: `battle_trainer.engine`. Already there: server configuration (`server.py`), the pinned Showdown commit, and the protocol notes for the headless CLI (`headless.py`).

1. Measure battles per second through the server tier (with the Arena stream) so there is a baseline.
2. Implement `HeadlessBattle` over `pokemon-showdown simulate-battle` and a runner that drives many subprocesses in parallel.
3. Get `oak` (libpkmn) installed and running a Gen 1 battle on a Linux laptop; cross-check seeded battles against headless Showdown for parity.
4. Expose both tiers behind the same interface the Player's env uses, and publish the throughput table.

Week-4 milestone: training runs with no server in the loop.

## Reading, by stream

- All: [poke-env docs](https://poke-env.readthedocs.io/), especially the getting-started and RL examples.
- Ghosts and Player: [Metamon paper](https://arxiv.org/abs/2504.04395) and [repo](https://github.com/UT-Austin-RPL/metamon).
- Player: PPO (Schulman et al., 2017), and any clear single-file PPO implementation with action masking.
- Coach: [AlphaStar](https://deepmind.google/research/breakthroughs/alphastar/) league training; curriculum learning surveys.
- Engine: [SIMULATOR.md](https://github.com/smogon/pokemon-showdown/blob/master/sim/SIMULATOR.md), [libpkmn design notes](https://github.com/pkmn/engine/blob/main/docs/DESIGN.md), [oak](https://github.com/pokemon-labs/oak).
