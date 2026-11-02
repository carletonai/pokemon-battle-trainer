# Contributing

Thanks for joining. This page is the short version of how we work; when in doubt, ask in `#pokemon-battle-trainer`.

## Set up

Follow [Getting started](README.md#getting-started) in the README. `uv run pre-commit install` once, and the linter and formatter run on every commit.

## Pick work

1. Choose a workstream in [docs/WORKSTREAMS.md](docs/WORKSTREAMS.md) and say so in the channel.
2. Open the package for your stream under `src/battle_trainer/`. Each stub lists numbered `TODO(<stream>)` steps; take the next one that is not already claimed.
3. If the task is bigger than an afternoon, open an issue with the **Task** template so others can see it is taken.

## Branches

Branch from `main`, named `<stream>/<short-description>`:

```
arena/elo-ladder
ghosts/replay-parser
player/state-encoder
coach/weakness-sampler
engine/headless-runner
tooling/pin-ruff
```

`main` is protected: changes land by pull request.

## Commits

We use [Conventional Commits](https://www.conventionalcommits.org/): `<type>(<scope>): <description>`.

| Type | When |
| --- | --- |
| `feat` | New feature or module |
| `fix` | Bug fix |
| `refactor` | Restructuring with no behaviour change |
| `test` | Tests only |
| `docs` | Documentation only |
| `chore` | Build, config, tooling, dependencies |
| `perf` | Performance improvement |
| `ci` | CI pipeline |
| `style` | Formatting only |

The scope is the workstream or module: `arena`, `ghosts`, `player`, `coach`, `engine`, `tooling`, `ci`, `docs`.

```
feat(arena): log replay links from ladder runs
fix(player): mask switches while trapped
perf(engine): batch headless battles across processes
```

Subject in the imperative, lowercase, no period, about 72 characters. Use the body to say *why*. Commit as you go rather than one commit for everything, and do not add `Co-authored-by` or `Signed-off-by` trailers.

## Pull requests

- Keep a PR to one change that can be reviewed in ten minutes. Several small PRs beat one large one.
- CI must be green: `ruff check`, `ruff format --check` and `pytest` (run `make lint test` locally first).
- One approving review from another member, then the author merges.
- Fill in the PR template: what changed, which workstream, how you tested it.

## Code

- Python 3.12+, type hints on public functions, docstrings that explain *why* and point at the plan where it matters.
- `ruff` lints and formats (`make format`). Line length is 100.
- No new top-level dependency without a line in the PR saying why. `uv add <package>` updates `pyproject.toml` and `uv.lock` together; commit both.
- `uv.lock` is not committed yet (the environment that made the scaffold could not reach the PyTorch index). The first person whose `uv sync` succeeds commits the `uv.lock` it produced, and CI then switches to `uv sync --locked`.
- Shared code goes in the package; one-off experiments go in `scripts/` or a notebook, and notebooks are cleared of outputs before commit.

## Tests

- Pure logic (ratings, intervals, parsing, masking) gets unit tests in `tests/`. Fast, no network.
- Anything that talks to Showdown is marked `@pytest.mark.showdown`. Those tests run when a local server is up (`scripts/start_showdown.sh`) and are skipped otherwise, so plain `pytest` always works on a fresh clone. CI runs them against a real server in the `showdown-smoke` job.

## Experiments and results

- A number in a write-up or the channel comes with: the Showdown commit (`third_party/SHOWDOWN_COMMIT`), the poke-env version, the opponent, and the panel size with its interval. `arena.panel.PanelResult` prints all of this; paste its output.
- Panels are 500 battles unless there is a stated reason.
- Replays, datasets, checkpoints and logs live in `data/`, `checkpoints/` and `runs/`, all git-ignored. Share large files through the channel or a shared drive, not git.

## Bumping Showdown or poke-env

Showdown is pinned in `third_party/SHOWDOWN_COMMIT`; poke-env in `pyproject.toml`. Bump either in its own PR (`chore(engine): bump showdown to <sha>`), run the smoke battle, and say in the PR what changed upstream. Results measured before and after a bump are not comparable.
