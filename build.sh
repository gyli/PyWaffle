#!/bin/bash
# Local development environment and example regeneration.
# Releases are built and published by .github/workflows/publish.yml, not from here.
set -euo pipefail

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements_dev.txt
pip install -e .

# Regenerate the example charts used by the README and the docs
MPLBACKEND=Agg python3 -m examples.generate_plots

# Build the docs
# cd docs && python3 -m sphinx -T -E -b html -d _build/doctrees -D language=en . _build/html

deactivate
