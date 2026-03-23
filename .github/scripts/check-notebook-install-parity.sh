#!/bin/bash
# Check that notebook install guidance matches README install policy.
# Fails if any notebook contains bare "pip install qontos" without git+.
#
# Usage: bash check-notebook-install-parity.sh [repo-root]

set -euo pipefail

BASE="${1:-.}"
ERRORS=0

echo "Notebook Install Parity Check"
echo "=============================="

for nb in "$BASE"/notebooks/*.ipynb; do
    [ -f "$nb" ] || continue
    name=$(basename "$nb")

    # Check for bare pip install (no git+)
    BAD=$(grep -o 'pip install [^"\\]*' "$nb" 2>/dev/null | grep -v 'git+' || true)
    if [ -n "$BAD" ]; then
        echo "  ✗ $name: stale install → $BAD"
        ERRORS=$((ERRORS + 1))
    else
        echo "  ✓ $name"
    fi
done

echo ""
if [ "$ERRORS" -gt 0 ]; then
    echo "FAIL: $ERRORS notebook(s) have stale install guidance"
    echo "Fix: replace bare 'pip install qontos' with pinned git+https tag"
    exit 1
else
    echo "PASS: All notebooks match pre-release install policy"
fi
