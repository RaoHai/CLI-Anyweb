#!/usr/bin/env bash
set -euo pipefail

SITE_NAME="${1:-}"

if [[ -z "${SITE_NAME}" ]]; then
  echo "Usage: bash scripts/setup-cli-anyweb.sh <site-name>"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SITE_DIR="${ROOT_DIR}/references/${SITE_NAME}"
REF_DIR="${ROOT_DIR}/agent_harness/skills/references"
EVAL_DIR="${ROOT_DIR}/agent_harness/skills/evals"

mkdir -p "${SITE_DIR}" "${REF_DIR}" "${EVAL_DIR}"

ENV_FILE="${SITE_DIR}/site.env"
SITE_README="${SITE_DIR}/README.md"
SITE_PROFILE="${REF_DIR}/${SITE_NAME}.site-profile.md"
STARTER_FLOW="${REF_DIR}/${SITE_NAME}.starter-flow.md"
STARTER_EVAL="${EVAL_DIR}/${SITE_NAME}.starter.eval.yaml"
STARTER_PATH="${EVAL_DIR}/${SITE_NAME}.starter.path.yaml"

if [[ ! -f "${ENV_FILE}" ]]; then
  cat > "${ENV_FILE}" <<'EOF'
# Site-specific browser flags for cli-anyweb.
# Example:
# CLI_ANYWEB_AGENT_BROWSER_FLAGS='--user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"'
EOF
fi

if [[ ! -f "${SITE_README}" ]]; then
  cat > "${SITE_README}" <<EOF
# ${SITE_NAME}

This directory stores site-specific setup notes for ${SITE_NAME}.

## Files

- \`site.env\`: environment overrides such as browser flags or real user agent settings

## Usage

\`\`\`bash
source "${ENV_FILE}"
\`\`\`
EOF
fi

if [[ ! -f "${SITE_PROFILE}" ]]; then
  cat > "${SITE_PROFILE}" <<EOF
# ${SITE_NAME} Site Profile

## Site Summary

- domain:
- site type:
- public or gated:
- auth requirements:

## Entry Points

- primary entry URL:
- alternate entry URLs:

## Main Surfaces

- primary navigation:
- search surface:
- detail surface:
- account surface:

## Stable Anchors

- labels:
- buttons:
- headings:
- landmarks:

## Risks

- anti-bot or risk controls:
- login walls:
- dynamic content:
- localization issues:

## Candidate Flows

- starter flow:
- next likely flow:
- risky flow to avoid first:
EOF
fi

if [[ ! -f "${STARTER_FLOW}" ]]; then
  cat > "${STARTER_FLOW}" <<EOF
# ${SITE_NAME} Starter Flow

## Scope

- target site: ${SITE_NAME}
- target flow:
- preconditions:

## Stable Anchors

- visible landmarks:
- reliable labels or headings:
- persistent buttons or inputs:

## Recommended Path

1. Open:
2. Snapshot or inspect:
3. First interaction:
4. Follow-up interactions:
5. Verify completion:

## Suggested Harness Commands

\`\`\`bash
cli-anyweb open <url>
cli-anyweb --json ls /
cli-anyweb --json grep "<key text>"
\`\`\`

## Common Failure Modes

- popup or cookie banner:
- lazy-loading or delayed widgets:
- auth redirect:
- duplicate labels:

## Fallback Strategy

- if primary anchor fails:
- if the page structure changes:
- if text search is ambiguous:

## Success Criteria

- page state that proves success:
- URL, title, or text that proves completion:
EOF
fi

if [[ ! -f "${STARTER_EVAL}" ]]; then
  cat > "${STARTER_EVAL}" <<EOF
id: ${SITE_NAME}.starter
site: ${SITE_NAME}
flow: starter
entry_url: https://${SITE_NAME}
inputs: {}
expect:
  page_type:
  contains_text: []
metrics:
  track:
    - success
    - step_count
    - fallback_used
EOF
fi

if [[ ! -f "${STARTER_PATH}" ]]; then
  cat > "${STARTER_PATH}" <<EOF
site: ${SITE_NAME}
flow: starter
entry_url: https://${SITE_NAME}
steps:
  - action: open
    target: https://${SITE_NAME}
  - action: snapshot
success:
  page_type:
fallbacks: []
EOF
fi

echo "Initialized cli-anyweb site scaffold:"
echo "  ${SITE_DIR}"
echo "  ${SITE_PROFILE}"
echo "  ${STARTER_FLOW}"
echo "  ${STARTER_EVAL}"
echo "  ${STARTER_PATH}"
