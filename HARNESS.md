# Browser Harness: agent-browser Integration

## Purpose

This harness provides browser automation using [Vercel Labs agent-browser](https://github.com/vercel-labs/agent-browser).

Its role is not only to expose browser control, but to give agents a structured operating surface for interacting with websites and gradually turning repeated web exploration into reusable workflow assets.

Compared with the earlier browser harness lineage, this project now:

- uses `agent-browser` as the backend
- exposes a flat CLI command surface
- reconstructs a snapshot-derived tree for inspection and pathing
- aims to support references, replay, and evaluation over time

## Architecture

```text
CLI Commands
  -> agent_harness/gui_agent_harness_cli.py
  -> core/page.py, core/fs.py, core/session.py
  -> utils/agent_browser_backend.py
  -> subprocess calls to `agent-browser --json ...`
  -> Chrome / Chromium managed by agent-browser
```

## Backend Model

The current backend is CLI-driven:

- backend: `agent-browser`
- transport: subprocess calls
- inspection source: `snapshot --json`
- action model: direct CLI commands such as `open`, `click`, `type`, and `reload`
- browser lifecycle: agent-browser's own daemon/client architecture

The Python package no longer depends on:

- the `mcp` SDK
- a DOMShell extension
- stdio transport to an external MCP server

## Command Surface

The user-facing CLI is flat:

- navigation: `open`, `reload`, `back`, `forward`, `info`
- inspection: `snapshot`, `ls`, `cd`, `cat`, `grep`, `pwd`, `find`, `get`
- actions: `click`, `type`
- session utilities: `status`, `daemon-start`, `daemon-stop`

Internally:

- navigation commands map directly to `agent-browser`
- action commands resolve a synthetic snapshot path to an `@ref`
- inspection commands reconstruct a local tree from snapshot output

## Synthetic Filesystem

`agent-browser` gives us an accessibility snapshot and deterministic refs, but it does not expose a built-in hierarchical path tree in the same form as the older harness.

To preserve an inspectable and agent-friendly operating model, this repository reconstructs that tree locally.

Flow:

1. call `agent-browser snapshot --json`
2. parse the snapshot text and refs map
3. build an in-memory node tree
4. assign stable-looking paths such as `/button[0]` or `/main[0]/link[2]`
5. use those paths for `ls`, `cd`, `cat`, `grep`, and path-based `click` or `type`

This keeps the harness ergonomic for agents while switching the underlying browser backend.

## Session State

The local `Session` object still tracks:

- `current_url`
- `working_dir`
- `history`
- `forward_stack`
- `daemon_mode`

Notes:

- navigation state is maintained locally for `info` and `status`
- `daemon-start` and `daemon-stop` are lightweight local toggles
- agent-browser already owns the real browser daemon lifecycle

## Command Mapping

| Harness command | Backend command |
|---|---|
| `open <url>` | `agent-browser open <url>` |
| `reload` | `agent-browser reload` |
| `back` | `agent-browser back` |
| `forward` | `agent-browser forward` |
| `ls` | `agent-browser snapshot --json` + local tree listing |
| `cat` | `agent-browser snapshot --json` + local node lookup |
| `grep` | `agent-browser snapshot --json` + local text search |
| `click <path>` | `agent-browser click @ref` |
| `type <path> <text>` | `agent-browser type @ref <text>` |

## Harness Method

The long-term purpose of this harness is not only "automate a page once."
It is to support a repeatable progression:

1. inspect a site
2. discover a workable path
3. save what worked
4. replay it
5. evaluate it
6. improve it over time

That is the bridge between browser control and agent-native web infrastructure.

## Unknown Site Onboarding

The most important long-term problem is not how to automate a site we already know.
It is how to start useful work on a site we have never seen before.

For an unknown site, the agent should not begin by assuming a flow.
It should begin by turning the site from an unknown environment into a modeled, replayable, and evaluable asset.

### Primary Objective

When facing a brand-new site, the first task is not:

- complete every possible business action

The first task is:

- identify one minimal, reusable, and replayable flow

The first successful onboarding should ideally produce:

- a basic site profile
- several candidate flows
- one selected starter flow
- a replayable path artifact
- an eval case for that flow

### Onboarding Pipeline

The first-contact workflow for an unknown site should follow a standard pipeline.

#### 1. Open

Inputs:

- `entry_url`
- optional `task_hint`

Actions:

- `open <url>`
- `snapshot`

Goals:

- capture the initial page structure
- identify major navigation regions
- detect whether the page appears public, gated, or task-oriented

#### 2. Surface Scan

Actions:

- inspect the main navigation and primary content areas
- search for common anchors such as `login`, `search`, `publish`, `home`, `profile`, and `help`
- inspect visible inputs, buttons, cards, and major landmarks

Goals:

- estimate the site type
- identify likely high-value interaction surfaces
- collect candidate stable anchors

Useful early site categories include:

- content consumption sites
- search and information sites
- form or back-office systems
- e-commerce sites
- community or feed-based sites

#### 3. Generate Flow Hypotheses

Before taking action, the agent should propose several candidate flows.

Examples:

- `browse_content`
- `search_content`
- `open_detail`
- `login`
- `create_item`
- `submit_form`
- `navigate_to_profile`

Each candidate flow should include:

- flow name
- why the flow is believed to exist
- likely entry anchors
- likely risks
- whether it is suitable as the first reusable reference

#### 4. Pick One Minimal Flow

The first selected flow should usually be:

- low side effect
- low privilege
- short
- easy to validate
- likely to survive small site changes

Preferred selection criteria:

- does not require login
- does not require upload
- has clear success conditions
- reflects a real interaction pattern on the site

The first goal is not "most important business flow."
The first goal is "smallest real flow that can be validated and reused."

#### 5. Execute And Record

After selecting a candidate flow, execute it and capture:

- actual steps taken
- anchors used
- where path resolution succeeded
- where ambiguity appeared
- fallback actions
- terminal success state

This is the point where the first reusable site asset begins to exist.

## Persisted Assets

When an unknown site is first explored successfully, the result should not remain a one-off run.
It should be persisted as layered assets.

### 1. Site Profile

This describes what the site is.

Suggested contents:

- site type
- entry points
- main navigation regions
- common anchor vocabulary
- auth requirements
- dynamic behavior
- obvious risks

### 2. Flow Reference

This describes how a specific flow works.

Suggested contents:

- flow name
- entry point
- preconditions
- main steps
- stable anchors
- success criteria
- fallback path

### 3. Replayable Path Artifact

This describes how a machine should replay the flow.

Suggested contents:

- action sequence
- target resolution hints
- variables
- success assertions
- fallback branches

### 4. Eval Case

This describes how the flow should be re-checked later.

Suggested contents:

- flow id
- entry point
- input values
- terminal expectations
- scoreable assertions

Together these assets let the second run begin from knowledge instead of from zero.

## Evaluation Model

Evaluation should begin as soon as the first successful flow exists.

At first, evaluation should not try to score the whole site.
It should score one flow at a time.

### Minimum Eval Structure

Each flow should produce at least one eval case containing:

- `entry_url`
- `flow_name`
- `inputs`
- expected terminal state
- expected anchor or text checks

Example shape:

```yaml
id: site_flow_001
flow: open_first_content_detail
entry_url: https://example.com
inputs: {}
expect:
  page_type: detail
  contains_text:
    - comments
```

### Minimum Eval Metrics

The first useful metrics are:

- `success`
- `step_count`
- `fallback_used`
- `terminal_page_type`
- `terminal_anchor_match`

At the start, evaluation should answer:

- can the flow still be completed
- does it still land on the right page type
- is it getting more expensive
- is fallback becoming more common

## Installation

```bash
pip install -e .
npm install -g agent-browser
agent-browser install
```

## Testing

### Unit Tests

- mock backend functions at the Python boundary
- test path resolution and session behavior
- avoid requiring a real browser where possible

### E2E Tests

- require `agent-browser`
- opt in with `AGENT_BROWSER_E2E=1`
- verify CLI startup, JSON output, status, and live interactions

## Tradeoffs

Benefits:

- simpler runtime dependency model
- official JSON output from the browser backend
- richer future surface area: screenshots, semantic locators, sessions, and network tools
- a cleaner path from one-off browser control toward reusable agent workflows

Costs:

- filesystem-like paths are synthesized, not backend-native
- large pages may require repeated snapshots
- path stability depends on accessibility snapshot structure
- the accumulation layer for references and replay is still incomplete

## Future Work

- add snapshot caching to reduce repeated backend calls
- expose more of `agent-browser`'s semantic locator and screenshot features
- add higher-level workflow helpers for forms, extraction, and waiting
- implement durable replay/eval loops for real site references
- make path reuse a first-class default instead of a manual convention

## Practical Principle

For unknown sites, the first mission is not to solve the whole product.

The first mission is to convert the site into something that is:

- partially understood
- partially replayable
- partially evaluable
- more reusable next time than it was this time

That is the shortest path from browser automation to agent-native web infrastructure.

## References

- [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)
- [CLI-Anything](https://github.com/HKUDS/CLI-Anything)
