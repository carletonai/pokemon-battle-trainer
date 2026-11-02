# Contributing

Set up with the [quick start](README.md#quick-start) and pick a task in [docs/WORKSTREAMS.md](docs/WORKSTREAMS.md). For anything bigger than an afternoon, open an issue with the Task template so others know it is taken.

## Branches and pull requests

- Branch from `main`, named `<stream>/<short-description>`, e.g. `arena/elo-ladder`. `main` only changes by pull request.
- Keep a PR to one change that can be reviewed in ten minutes.
- `make lint test` must pass (`make format` fixes most lint). CI also runs the smoke battle and the `showdown` tests against a real server, so run `make smoke test` with your server up if you touched anything that talks to it.
- One approving review, then the author merges.
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

- Every reported win rate comes from a 500-battle panel (fifty-battle numbers are luck) and names the Showdown commit, the poke-env version and the interval. `arena.panel.PanelResult` prints all of it; paste that.
- Replays, datasets, checkpoints and logs go in `data/`, `checkpoints/` and `runs/`, which are git-ignored. Nothing big in git.
- No Pokémon artwork in the repo or on the rating page. Ladder etiquette is in `arena/ladder.py`.
- Showdown (`third_party/SHOWDOWN_COMMIT`) and poke-env (`uv.lock`) are pinned. Bump either in its own PR; results from before and after are not comparable.
- Type hints on public functions; pure logic gets a fast unit test in `tests/`; one-off experiments go in `scripts/` or a notebook.
- Mark tests that need Showdown `@pytest.mark.showdown`; `tests/conftest.py` handles the skip.
