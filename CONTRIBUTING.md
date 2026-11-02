# Contributing

Set up with the [quick start](README.md#quick-start), pick a workstream in [docs/WORKSTREAMS.md](docs/WORKSTREAMS.md), and say so in `#pokemon-battle-trainer`. Each stub under `src/battle_trainer/` lists numbered `TODO(<stream>)` steps; take the next unclaimed one. For anything bigger than an afternoon, open an issue with the Task template so others know it is taken.

## Branches and pull requests

- Branch from `main`, named `<stream>/<short-description>`, e.g. `arena/elo-ladder`. `main` only changes by pull request.
- Keep a PR to one change that can be reviewed in ten minutes.
- `make lint test` must pass (CI runs the same). One approving review, then the author merges.
- New dependency: `uv add <package>`, commit `pyproject.toml` and `uv.lock` together, and say why in the PR.

## Commits

[Conventional Commits](https://www.conventionalcommits.org/): `<type>(<scope>): <description>`.

- Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`, `ci`, `style`.
- Scope is the workstream or module: `arena`, `ghosts`, `player`, `coach`, `engine`, `tooling`, `ci`, `docs`.
- Subject in the imperative, lowercase, no period. Use the body for *why*.
- Commit as you go rather than one big commit at the end.
- `Co-authored-by` is for people you paired with. Never add trailers that credit AI tools as authors.

```
feat(arena): log replay links from ladder runs
fix(player): mask switches while trapped
```

## Rules

- Every reported win rate names the Showdown commit, the poke-env version and the panel size with its interval. `arena.panel.PanelResult` prints all of it; paste that.
- Panels are 500 battles. Fifty-battle numbers are luck.
- Replays, datasets, checkpoints and logs go in `data/`, `checkpoints/` and `runs/`, which are git-ignored. Nothing big in git.
- Ladder runs use the club's one Showdown account, never stall the timer and stay out of chat rooms. No Pokémon artwork in the repo or on the rating page.
- Showdown (`third_party/SHOWDOWN_COMMIT`) and poke-env (`pyproject.toml`) are pinned. Bump either in its own PR; results from before and after are not comparable.
- Tests that talk to Showdown are marked `@pytest.mark.showdown` and skip when no local server is running, so plain `pytest` always works.
