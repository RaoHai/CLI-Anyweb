# cli-anyweb Plugin Harness

This file is the source of truth for how to turn an arbitrary website into a reusable, site-specific CLI on top of `cli-anyweb`.

It intentionally follows the role and layout of `cli-anything-plugin/HARNESS.md`, but the target here is the web:

- `cli-anything` turns GUI applications into CLIs
- `cli-anyweb` turns websites into reusable web CLIs for agents

## Purpose

This harness provides browser automation for `cli-anyweb` using [Vercel Labs agent-browser](https://github.com/vercel-labs/agent-browser).

Its role is not only to expose browser control, but to give agents a structured operating surface for interacting with websites and gradually turning repeated web exploration into reusable workflow assets.

## Architecture

```text
CLI Commands
  -> cli_anyweb/cli_anyweb_cli.py
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

`agent-browser` gives an accessibility snapshot and deterministic refs, but it does not expose the same inspectable hierarchy that the older harness lineage used.

To preserve an agent-friendly operating model, this repository reconstructs a local tree:

1. call `agent-browser snapshot --json`
2. parse the snapshot text and refs map
3. build an in-memory node tree
4. assign stable-looking paths such as `/button[0]` or `/main[0]/link[2]`
5. use those paths for `ls`, `cd`, `cat`, `grep`, and path-based `click` or `type`

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

## Plugin Output Contract

Each site integration should aim to produce a small but reusable asset set:

- a site setup entry point
- a sitemap reference
- one or more path artifacts
- one or more eval cases
- optional site wrappers for browser flags, auth prerequisites, or launch behavior

The first valid integration for a new site does not need to be large.
It does need to be replayable.

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

- a basic sitemap reference
- several candidate flows
- a replayable path artifact
- an eval case for that flow

### Onboarding Pipeline

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

#### 3. Generate Flow Hypotheses

Before taking action, propose several candidate flows.

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

## Site-Specific Setup

Some websites require browser settings that should not be hardcoded globally.

Examples:

- real user agent strings
- custom browser flags
- custom profile behavior
- network or auth prerequisites

For these sites, prefer per-site setup via:

- plugin setup scripts
- per-site environment files
- wrapper commands that export site-specific flags before invoking the harness

### Real UA Example

For sites such as Xiaohongshu that may reject the default headless browser fingerprint, use:

- `CLI_ANYWEB_AGENT_BROWSER_FLAGS`

```bash
export CLI_ANYWEB_AGENT_BROWSER_FLAGS='--user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"'
```

The exact flag support depends on `agent-browser`, but the harness forwards extra browser flags from this environment variable.

### Reusing Login State

If a site requires login, persist a browser profile directory and reuse it across sessions:

- set `CLI_ANYWEB_SITE_PROFILE_DIR` in `site.env`
- the wrapper will export it as `AGENT_BROWSER_PROFILE`
- `agent-browser` will reuse the profile automatically
- use an absolute path so the profile is resolved consistently

This keeps the login state consistent without hardcoding credentials.

### Manual Login Tip

If the browser window is not visible during login, set:

- `AGENT_BROWSER_HEADED=true` in `site.env`

This forces a headed browser so a human can complete the login once, then reuse the profile.

## Persisted Assets

When an unknown site is first explored successfully, the result should not remain a one-off run.
It should be persisted as layered assets.

### 1. SiteMap Reference

Describes the reachable information architecture of the site.

Suggested contents:

- a markdown or ASCII `SiteMap`
- a `Logged-Out` branch based on validated observations
- a `Logged-In` branch, marked as validated or pending validation
- the major surfaces and gates visible from each auth state
- the main chains that can be derived from the map
- the proposed CLI surface that should be built from those chains

Keep this artifact lean.
It should help future agents extract the site's main chains, not read a long narrative report.

### 2. Replayable Path Artifact

Describes how the machine should attempt replay.

Suggested contents:

- action sequence
- target resolution hints
- variables
- success assertions
- fallback branches

### 3. Eval Case

Describes how the saved flow should be checked later.

Suggested contents:

- flow id
- entry URL
- inputs
- expected terminal state
- expected anchor matches

## Evaluation Model

Evaluation should focus on flows, not on vague whole-site correctness.

Each eval run should aim to answer:

- did the flow still succeed
- how many steps did it take
- did fallback trigger
- did it land on the expected terminal page type
- did expected anchors still appear

The main point is not to prove the site is perfect.
The main point is to know whether the saved flow still works, whether it got more expensive, and whether the failure mode changed.

## Recommended Plugin Commands

Keep the plugin-facing command set close to the upstream `cli-anything-plugin` shape:

- `/cli-anyweb <site-or-url>`
- `/cli-anyweb:refine <site>`
- `/cli-anyweb:test <site>`
- `/cli-anyweb:validate <site>`
- `/cli-anyweb:list`

## Recommended Directory Shape

```text
cli-anyweb-plugin/
|-- .claude-plugin/
|-- commands/
|-- guides/
|-- scripts/
|-- templates/
|-- tests/
|-- HARNESS.md
|-- README.md
|-- QUICKSTART.md
|-- PUBLISHING.md
|-- repl_skin.py
|-- skill_generator.py
`-- verify-plugin.sh
```

The point of this similarity is practical:

- contributors can move between `cli-anything` and `cli-anyweb` without relearning the layout
- command docs and SOP material have predictable homes
- future plugin distribution can follow a familiar shape
