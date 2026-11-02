# Workstreams

Pick one, say so in `#pokemon-battle-trainer`, and take its first unclaimed task. Every stub in `src/battle_trainer/` carries a `TODO(<stream>)` list with more detail than this page; `grep -rn "TODO(" src/` shows them all. Get the [quick start](../README.md#quick-start) working first: every stream needs the smoke battle.

## Arena: run the battles and keep score

`battle_trainer.arena`. The built-in bots, Elo and 500-battle panels exist; what is missing is everything that runs battles at scale.

1. Battle every built-in bot against every other over 500-battle panels; publish the table and Elo standings (ladder v0).
2. Make `run_panel` run several battles concurrently and measure battles per minute.
3. Add Metamon's released agents as the opponent tier after the built-in bots.
4. Implement `ladder.run_ladder`: ranked games on the official server, with rating and replay links logged to JSONL, then a rating page on carletonai.com.

Week-4 milestone: ladder v0 with the built-in bots, rating page live. Read the [poke-env docs](https://poke-env.readthedocs.io/).

## Ghosts: imitation copies of human players

`battle_trainer.ghosts`. Pipeline: `scrape.py` → `parse.py` → `dataset.py` → `imitation.py`.

1. Read Metamon's replay-parsing code and decide what to reuse.
2. Scrape a few thousand Gen 1 random-battle replays with ratings into `data/replays/`.
3. Parse one side of each replay into (observation, action) pairs using the Player's encoder and action indices, so ghosts and Player share one action space.
4. Train a first ghost with cross-entropy over legal actions; evaluate it on a 500-battle panel against the heuristic bot.

Week-4 milestone: one ghost that beats the heuristic bot. Read [Metamon](https://github.com/UT-Austin-RPL/metamon) and its [paper](https://arxiv.org/abs/2504.04395).

## Player: the bot we train

`battle_trainer.player`. A Gen 1 env with a tiny v0 observation (`env.py`) and its `MaskablePPO` adapter (`ppo.py`) exist. PPO comes from Stable-Baselines3, which logs to TensorBoard.

1. Step `make_env(...)` against the local server with random legal actions and watch observations, masks and rewards flow.
2. Run the `MaskablePPO` snippet at the top of `ppo.py` against the random bot; confirm a reward curve shows up in TensorBoard.
3. Build the real state encoder (`encoder.py`): both teams, what the opponent has revealed, known moves, field state.
4. Train against the random bot, then the max-damage bot. Report 500-battle panels.

Week-4 milestone: beats the max-damage bot from scratch; week 8, the heuristic bot. Read [MaskablePPO](https://sb3-contrib.readthedocs.io/en/master/modules/ppo_mask.html) and Metamon.

## Coach: decides what the Player practises

`battle_trainer.coach`. The uniform baseline and the 50% uniform floor exist (`curriculum.py`).

1. Build the held-out exam panel: fixed opponents and seeds the Coach can never sample from.
2. Implement `WeaknessSampler` with its guardrails: 500-battle evidence, the floor, move on once fixed.
3. Run the experiment: uniform mix versus Coach mix, same budget, same exam. The Coach stays only if it wins.

Week-4 milestone: random sparring mix matches the fixed-opponent win rate. Read about [AlphaStar](https://deepmind.google/research/breakthroughs/alphastar/) league training.

## Engine: training without a server in the loop

`battle_trainer.engine`. Server configuration and the headless protocol notes exist.

1. Measure battles per second through the server (with Arena) as the baseline.
2. Implement `HeadlessBattle` over `pokemon-showdown simulate-battle` and a runner that drives many subprocesses in parallel.
3. Get `oak` (libpkmn) running a Gen 1 battle on x86-64 Linux (`uv sync --extra engine`) and check seeded battles for parity against headless Showdown.
4. Put both tiers behind the interface the Player's env uses; publish the throughput table.

Week-4 milestone: training runs with no server in the loop. Read [SIMULATOR.md](https://github.com/smogon/pokemon-showdown/blob/master/sim/SIMULATOR.md), [libpkmn](https://github.com/pkmn/engine) and [oak](https://github.com/pokemon-labs/oak).
