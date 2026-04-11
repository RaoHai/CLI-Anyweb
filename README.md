# gui-agent-harness

Turn human-oriented websites into reusable, agent-native tools.

`gui-agent-harness` is a standalone repository for turning ordinary websites into agent-usable tools through a structured CLI built around Vercel Labs `agent-browser`.

It focuses on three layers:

- a runnable browser harness built on `agent-browser`
- skill-driven guidance for GUI navigation and decision making
- per-site references and evaluation workflows for discovering best paths

## The Pain Point

Modern frontier models already have strong GUI operation ability, and tools like `agent-browser` make browser interaction much more accessible.

But raw capability is not the same thing as stable agent tooling.

In practice, many models still end up "random walking" through the web:

- they rediscover the same navigation path every run
- they spend tokens and time re-finding buttons, menus, and flows they have effectively solved before
- they may succeed on easy tasks, but they are often not operating in the most efficient or reusable way

For SOTA models this may be acceptable in some cases. For smaller, cheaper, or more task-specific models, that inefficiency matters a lot more.

What is missing is not just browser control. What is missing is a reusable, agent-native interaction layer that makes the web feel less like an unstructured environment and more like a dependable tool surface.

## Vision

`gui-agent-harness` aims to help build an agent-native web ecosystem:

- No-barrier access: any website can become immediately operable by an agent through a structured CLI.
- Seamless integration: no dedicated API, no visual-channel GUI driving, no codebase refactor, and no heavy adaptation layer required.
- Future-oriented: with a single command, a web experience designed for humans can become a native tool for agents.

## Why Not Just Use `agent-browser` Directly?

`agent-browser` is the foundation here, and it already provides strong browser control.

But direct browser control alone does not solve the higher-level agent problem:

- control is not the same as reusable workflow structure
- successful interaction is not the same as stable path discovery
- a one-off run is not the same as an accumulated, improving web operation layer

`gui-agent-harness` adds the missing layer on top:

- structured CLI commands that are easier for agents to call repeatedly
- snapshot-oriented inspection primitives that are cheaper and more stable than pure visual driving
- per-site references so solved navigation patterns can be reused instead of rediscovered
- eval and replay scaffolding so the system can improve over time rather than starting from scratch each run

In short: `agent-browser` gives browser capability, while `gui-agent-harness` is trying to turn that capability into reusable agent infrastructure.

## Core Idea

The core loop is simple:

1. open and inspect a website through a structured browser harness
2. discover a workable interaction path
3. save that path as reusable agent knowledge
4. replay, evaluate, and refine it over time

That turns web interaction from repeated exploration into an accumulative system.

## Workflow

```text
Open -> Inspect -> Act -> Capture -> Reuse -> Evaluate
```

Or more concretely:

- `open`: load the target page
- `snapshot` / `ls` / `cat` / `grep` / `find`: inspect the interaction surface
- `click` / `type`: execute the path
- references: save what worked
- evals: replay and score those paths when the site changes

## Install

```bash
pip install -e .
npm install -g agent-browser
agent-browser install
```

## Quick Start

```bash
gui-agent-harness open https://example.com
gui-agent-harness snapshot
gui-agent-harness find Example
gui-agent-harness get url
```

The CLI now uses a flat command surface such as `open`, `snapshot`, `ls`, `click`, and `find` instead of the older grouped shell.

## Repository Layout

- [setup.py](/Y:/gui-agent-harness/setup.py)
- [agent_harness/README.md](/Y:/gui-agent-harness/agent_harness/README.md)
- [agent_harness/skills/SKILL.md](/Y:/gui-agent-harness/agent_harness/skills/SKILL.md)
- [agent_harness/skills/references](/Y:/gui-agent-harness/agent_harness/skills/references)
- [agent_harness/skills/evals](/Y:/gui-agent-harness/agent_harness/skills/evals)
- [agent_harness/tests/TEST.md](/Y:/gui-agent-harness/agent_harness/tests/TEST.md)
- [HARNESS.md](/Y:/gui-agent-harness/HARNESS.md)

## Roadmap

- decide whether to rename the internal package directory from `agent_harness` to `gui_agent_harness`
- clean up remaining legacy naming around `CLI_ANYTHING_ANYWEB_*` and older filesystem-oriented wording
- add real site references beyond `example.com`
- build the replay/eval loop for model-driven path discovery
- expand backend-focused tests such as executable resolution, snapshot parsing, and path-to-ref translation

## Configuration

- Preferred package name: `gui-agent-harness`
- Preferred CLI command: `gui-agent-harness`
- Preferred env vars: `CLI_ANYTHING_ANYWEB_*`
- Legacy `CLI_ANYTHING_BROWSER_*` env vars are still accepted for compatibility

## Why This Repo Exists

This repository splits the browser harness out of the larger `CLI-Anything` monorepo so it can evolve independently as a focused GUI agent project.

The Python package now lives in the root-level `agent_harness/` directory instead of the deeper `cli_anything/anyweb/` path.

## Attribution

This project is derived from and inspired by:

- [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything)
- the harness methodology described in `cli-anything-plugin/HARNESS.md`
- the existing browser harness work inside the original repository
- the browser harness packaging layout, REPL conventions, and backend integration approach later adapted here to `agent-browser`

`gui-agent-harness` is a derivative work prepared from the `CLI-Anything` repository structure and harness approach.

This repository should preserve upstream attribution in documentation, release notes, mirrors, and announcements.
