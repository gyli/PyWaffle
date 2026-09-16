#!/bin/bash
# Pre-release check. Publishing itself happens in CI: create a GitHub release and
# .github/workflows/publish.yml uploads to PyPI via trusted publishing.
set -euo pipefail

MPLBACKEND=Agg python3 -m pytest tests
MPLBACKEND=Agg python3 -m examples.generate_plots

rm -rf dist build pywaffle.egg-info
python3 -m build
python3 -m twine check dist/*

echo
echo "Artifacts built and checked. To publish:"
echo "  1. bump __version__ in pywaffle/_version.py and add a CHANGELOG.md entry"
echo "  2. git tag v\$(python3 -c 'import pywaffle; print(pywaffle.__version__)')"
echo "  3. git push --tags, then create the GitHub release"
