#!/bin/bash
# Run all scitex-audio examples
# Usage: bash examples/00_run_all.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== SciTeX Audio Examples ==="
echo

for script in "$SCRIPT_DIR"/[0-9][0-9]_*.py; do
    [ -f "$script" ] || continue
    name="$(basename "$script")"
    echo "--- Running: $name ---"
    python "$script"
    echo
done

echo "=== All examples completed ==="
