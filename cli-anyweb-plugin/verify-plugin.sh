#!/usr/bin/env bash
# Verify cli-anyweb plugin structure

echo "Verifying cli-anyweb plugin structure..."
echo ""

ERRORS=0

check_file() {
    if [ -f "$1" ]; then
        echo "[OK] $1"
    else
        echo "[MISSING] $1"
        ERRORS=$((ERRORS + 1))
    fi
}

echo "Required files:"
check_file ".claude-plugin/plugin.json"
check_file "HARNESS.md"
check_file "README.md"
check_file "LICENSE"
check_file "PUBLISHING.md"
check_file "QUICKSTART.md"
check_file "commands/cli-anyweb.md"
check_file "commands/list.md"
check_file "commands/refine.md"
check_file "commands/test.md"
check_file "commands/validate.md"
check_file "scripts/setup-cli-anyweb.sh"
check_file "scripts/setup-cli-anyweb.ps1"

echo ""
echo "Checking plugin.json validity..."
if python3 -c "import json; json.load(open('.claude-plugin/plugin.json'))" 2>/dev/null; then
    echo "[OK] plugin.json is valid JSON"
else
    echo "[FAIL] plugin.json is invalid JSON"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "Checking script permissions..."
if [ -x "scripts/setup-cli-anyweb.sh" ]; then
    echo "[OK] setup-cli-anyweb.sh is executable"
else
    echo "[FAIL] setup-cli-anyweb.sh is not executable"
    ERRORS=$((ERRORS + 1))
fi

echo ""
if [ "$ERRORS" -eq 0 ]; then
    echo "[OK] All checks passed! Plugin is ready."
    exit 0
else
    echo "[FAIL] $ERRORS error(s) found. Please fix before publishing."
    exit 1
fi
