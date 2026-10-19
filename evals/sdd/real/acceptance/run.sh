#!/bin/sh
# Usage: run.sh <f1|f2|f3> <project dir> — run a hidden acceptance suite against a built mockshop.
HERE=$(cd "$(dirname "$0")" && pwd)
cd "$2" && uv run --no-project --with pytest --with hypothesis python -m pytest -q -p no:cacheprovider "$HERE/test_$1_acceptance.py" 2>&1 | tail -15
