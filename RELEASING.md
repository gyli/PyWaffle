# Releasing

How a release is cut. Developer-facing; users do not need any of this.

Publishing is done by CI, not from a laptop. Creating a GitHub release triggers
`.github/workflows/publish.yml`, which builds the artifacts and uploads them to PyPI using
[trusted publishing](https://docs.pypi.org/trusted-publishers/). No API token is stored anywhere.

Throughout, `X.Y.Z` stands for the version being released.

## One-time setup

Only needed once per project, or if the PyPI configuration is ever reset.

1. **Configure the PyPI trusted publisher.** On PyPI, open the project's
   *Settings -> Publishing* page and add a GitHub publisher with the owner and repository of this
   project, workflow filename `publish.yml`, and environment name `pypi`.
2. **Create the `pypi` environment** in the repository's *Settings -> Environments*. The publish
   job declares `environment: pypi`, so the job will not start without it.

Without both, the workflow runs and fails at the upload step. Everything before that point still
works, so a misconfiguration is visible but not destructive.

## Before releasing

`./release.sh` runs the core checks: the test suite, the example generator, a build, and
`twine check`. CI runs considerably more on every pull request, so a green `master` already covers
most of this.

Two things are worth doing by hand anyway, because neither is covered by simply running the suite.

**Check the built artifacts actually work when installed.** The suite imports the working tree, so
it cannot catch a packaging mistake such as a missing file or a wrong dependency. Install each
artifact into a throwaway environment and draw a chart:

```bash
python -m build
for artifact in dist/*.whl dist/*.tar.gz; do
  for extra in "" "[icons]"; do
    rm -rf /tmp/relcheck && python -m venv /tmp/relcheck
    /tmp/relcheck/bin/pip install -q "${artifact}${extra}"
    MPLBACKEND=Agg /tmp/relcheck/bin/python -c "
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, pywaffle
from pywaffle import Waffle
fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[30, 20])
assert len(fig.axes[0].patches) == 50
print(pywaffle.__version__, 'ok')"
  done
done
```

Both install modes matter. Font Awesome is an optional extra, so a plain install must draw
rectangles and must refuse `icons=` with a message naming the extra, while an `[icons]` install must
draw icons. A release that gets this backwards is only visible from a clean environment.

**Check the changelog against reality.** Entries are written while the work is fresh and can drift
before the release goes out. Confirm that anything the changelog claims to add is actually exported,
and that any constant it quotes still holds that value. This has caught a stale number more than
once.

## Releasing

1. **Make sure `master` is green and has no open pull requests** that belong in the release.

2. **Set the version.** Edit `__version__` in `pywaffle/_version.py`. Everything else reads it from
   there: `pyproject.toml` declares it dynamic, and `pywaffle.__version__` re-exports it, so this is
   the only place it is written.

3. **Date the changelog.** The top heading is kept as `vX.Y.Z (unreleased)` while work accumulates.
   Change it to `vX.Y.Z (YYYY-MM-DD)`. Check that every user-visible change since the last release
   has an entry, and mark anything breaking under its own `Breaking` heading.

   Steps 2 and 3 go in their own pull request, so the release commit is reviewed like any other.

4. **Tag the merge commit and push the tag.**

   ```bash
   git checkout master && git pull
   python -c "import pywaffle; print(pywaffle.__version__)"   # confirm it matches
   head -1 CHANGELOG.md                                        # confirm the date is set
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```

5. **Create the GitHub release.** This is the step that publishes.

   ```bash
   gh release create vX.Y.Z --title vX.Y.Z --notes "..."
   ```

   Use the changelog's top section as the notes. Lead with anything breaking: release notes are
   skimmed, and an upgrade that stops working is what people need to see first.

6. **Watch the publish run.**

   ```bash
   gh run watch "$(gh run list --workflow=publish.yml --limit 1 --json databaseId --jq '.[0].databaseId')"
   ```

## After

```bash
pip download --no-deps -d /tmp/pypi-check pywaffle==X.Y.Z
```

Downloading from PyPI confirms the upload rather than assuming it. Then open the project page and
check the rendered description, which comes from `README_pypi.rst` and is rendered by PyPI rather
than by GitHub, so it can fail there and nowhere else. `twine check` catches most of this earlier.

Finally, add a new `vNEXT (unreleased)` heading to the changelog so the next change has somewhere to
go.

## Notes

**A version cannot be replaced on PyPI.** A file uploaded under a version number is permanent, even
if deleted. A mistake means releasing the next patch version, not re-uploading. This is why the
artifacts are exercised from a clean environment before the tag is pushed rather than after.

**The tag is what people trust, so tag the merge commit.** Tagging a branch tip that never reached
`master` produces a release whose source nobody can find.

**`workflow_dispatch` is enabled on the publish workflow** for the case where a release was created
but the run failed for an unrelated reason, such as a transient network error. It builds from
whatever `master` currently holds, so only use it when `master` is still at the tagged commit.
