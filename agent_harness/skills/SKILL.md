---
name: "gui-agent-harness"
description: "GUI agent harness built on agent-browser. Use harness commands, site references, and eval guidance to discover robust browser paths."
---

# gui-agent-harness

Use this harness when you need a browser-oriented command interface that an agent can drive and improve over time.

## Install

```bash
pip install -e .
npm install -g agent-browser
agent-browser install
```

## Harness Goal

This project is meant to:

- provide a stable local browser harness on top of `agent-browser`
- accumulate per-site best practices in `skills/references/`
- support model-driven path discovery, iteration, and evals

## Preferred Commands

- `gui-agent-harness open <url>`
- `gui-agent-harness info`
- `gui-agent-harness snapshot`
- `gui-agent-harness ls [path]`
- `gui-agent-harness cat [path]`
- `gui-agent-harness grep <pattern> [path]`
- `gui-agent-harness click <path-or-ref>`
- `gui-agent-harness type <path-or-ref> <text>`
- `gui-agent-harness status`

## Agent Guidance

- Start with the generic harness commands and `--json` output.
- Before solving a site-specific task, check whether a matching reference exists in `skills/references/`.
- If a reference exists, follow its recommended navigation order, pitfalls, and success checks.
- If no reference exists, use the harness to explore the page and then write back a new reference.
- Prefer `--json` when another tool or model will parse the result.
- Use the REPL for multi-step workflows that rely on current URL or working directory state.
- `daemon-start` is just a local mode toggle; agent-browser already manages its own daemon.

## Reference System

- Reference index: [references/README.md](Y:\CLI-Anything\CLI-anyweb\agent_harness\skills\references\README.md)
- Site template: [references/_template.md](Y:\CLI-Anything\CLI-anyweb\agent_harness\skills\references\_template.md)
- Example site reference: [references/example.com.md](Y:\CLI-Anything\CLI-anyweb\agent_harness\skills\references\example.com.md)

Each site reference should capture:

- page landmarks and stable anchors
- recommended interaction order
- selectors or refs that tend to be robust
- failure modes and fallback plans
- what “success” looks like for that site flow

## Path Discovery And Evals

- Discovery workflow: [evals/AUTOPATH.md](Y:\CLI-Anything\CLI-anyweb\agent_harness\skills\evals\AUTOPATH.md)
- Eval workflow: [evals/EVALS.md](Y:\CLI-Anything\CLI-anyweb\agent_harness\skills\evals\EVALS.md)

The intended loop is:

1. Explore a site with the harness
2. Let a model propose multiple candidate paths
3. Replay and score those paths
4. Save the best practice as a site reference
5. Re-evaluate when the site changes

## Examples

```bash
gui-agent-harness open https://example.com
gui-agent-harness ls /
gui-agent-harness grep "Learn more"
gui-agent-harness --json status
```

## Security

- Only `http` and `https` are allowed by default.
- `file:`, `javascript:`, `data:` and browser-internal schemes are blocked.
- Set `CLI_ANYTHING_ANYWEB_BLOCK_PRIVATE=true` to block localhost and private network targets.
- Legacy `CLI_ANYTHING_BROWSER_*` env vars still work during migration.
