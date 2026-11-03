#!/usr/bin/env bash
# ==============================================================================
# Local PR Checks Runner
# Runs formatting, syntax checks, and the full test suite locally.
# ==============================================================================

set -e

echo "=========================================="
echo " Running Local PR Checks"
echo "=========================================="

# 1. Check Python syntax
echo "--> 1. Checking Python syntax..."
python3 -m py_compile relationship_messages.py app.py test_relationship_messages.py test_app.py
echo "✓ Syntax OK"

# 2. Run Unit & Integration Tests
echo ""
echo "--> 2. Running Automated Test Suite..."
python3 -m unittest discover -v
echo "✓ All tests passed!"

echo ""
echo "=========================================="
echo " ✅ All local PR checks passed!"
echo "=========================================="

