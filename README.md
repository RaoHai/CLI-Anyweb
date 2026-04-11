# cli-anyweb

Make any website more agent-usable through a structured CLI.

`cli-anyweb` is a browser harness and plugin-oriented workflow for turning ordinary websites into reusable, agent-native command surfaces on top of Vercel Labs `agent-browser`.

English | [ZH-CN README](./README.zh-cn.md)

One command line: turn web software built for humans into reusable tools for agents through browser control, site references, replayable paths, and evaluation.

## What It Is

`cli-anyweb` combines three layers:

- a generic runtime layer built on `agent-browser`
- a methodology for onboarding unknown websites and discovering reusable flows
- a plugin structure so each site can define its own setup, references, and eval assets

## Quick Links

- [Quick Start](#quick-start)
- [Why This Matters](#why-this-matters)
- [Why Not Just Use `agent-browser` Directly?](#why-not-just-use-agent-browser-directly)
- [Repository Layout](#repository-layout)
- [Roadmap](#roadmap)
- [cli-anyweb-plugin/HARNESS.md](./cli-anyweb-plugin/HARNESS.md)
- [ROADMAP.md](./ROADMAP.md)
- [cli-anyweb-plugin](./cli-anyweb-plugin)

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

`cli-anyweb` aims to help build an agent-native web ecosystem:

- No-barrier access: any website can become immediately operable by an agent through a structured CLI
- Seamless integration: no dedicated API, no visual-channel GUI driving, no codebase refactor, and no heavy adaptation layer required
- Future-oriented: a website built for humans can become a reusable tool surface for agents

## Why This Matters

If the web is going to become a real execution environment for agents, success cannot depend on rediscovering the same UI path every time.

The important shift is:

- from one-off browser control
- to reusable web workflows
- to evaluated and improving site knowledge

That is the layer this repository is trying to build.

## Why Not Just Use `agent-browser` Directly?

`agent-browser` is the foundation here, and it already provides strong browser control.

But direct browser control alone does not solve the higher-level agent problem:

- control is not the same as reusable workflow structure
- successful interaction is not the same as stable path discovery
- a one-off run is not the same as an accumulated, improving web operation layer

`cli-anyweb` adds the missing layer on top:

- structured CLI commands that are easier for agents to call repeatedly
- snapshot-oriented inspection primitives that are cheaper and more stable than pure visual driving
- per-site references so solved navigation patterns can be reused instead of rediscovered
- replay and eval scaffolding so the system can improve over time rather than starting from scratch each run
- a plugin structure so each site can define its own setup and browser requirements

In short: `agent-browser` gives browser capability, while `cli-anyweb` is trying to turn that capability into reusable web CLIs for agents.

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
- plugin setup: define site-specific requirements such as real UA or custom browser flags

## Install

```bash
pip install -e .
npm install -g agent-browser
agent-browser install
```

## Quick Start

```bash
cli-anyweb open https://example.com
cli-anyweb snapshot
cli-anyweb find Example
cli-anyweb get url
```

The CLI uses a flat command surface such as `open`, `snapshot`, `ls`, `click`, and `find`.

## What You Get

- Flat agent-friendly browser commands
- Snapshot-derived inspection and pathing
- A place to store site references and reusable flow knowledge
- A path toward replay, evaluation, and continuous improvement
- A plugin layout for site-specific setup and wrappers

## Repository Layout

- [setup.py](./setup.py)
- [cli_anyweb/README.md](./cli_anyweb/README.md)
- [cli_anyweb/skills/SKILL.md](./cli_anyweb/skills/SKILL.md)
- [cli_anyweb/skills/references](./cli_anyweb/skills/references)
- [cli_anyweb/skills/evals](./cli_anyweb/skills/evals)
- [cli_anyweb/tests/TEST.md](./cli_anyweb/tests/TEST.md)
- [cli-anyweb-plugin](./cli-anyweb-plugin)
- [references](./references)
- [cli-anyweb-plugin/HARNESS.md](./cli-anyweb-plugin/HARNESS.md)

## Roadmap

- clean up remaining legacy naming around `CLI_ANYTHING_ANYWEB_*` and older filesystem-oriented wording
- add real site references beyond `example.com`
- build the replay/eval loop for model-driven path discovery
- expand backend-focused tests such as executable resolution, snapshot parsing, and path-to-ref translation
- make site-specific plugin setup first-class for real-world websites

For the fuller execution plan, see [ROADMAP.md](./ROADMAP.md).

## Configuration

- Preferred package name: `cli-anyweb`
- Preferred CLI command: `cli-anyweb`
- Preferred extra browser flag env var: `CLI_ANYWEB_AGENT_BROWSER_FLAGS`
- Current internal Python package path: `cli_anyweb`

## Why This Repo Exists

This repository started as a focused browser harness extracted from the larger `CLI-Anything` ecosystem.

It is now being reshaped around a more specific goal:

- provide a generic runtime layer
- provide a plugin structure similar to `cli-anything-plugin`
- let contributors turn arbitrary websites into reusable site-specific CLIs

## Attribution

This project is derived from and inspired by:

- [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything)
- the harness methodology described in `cli-anything-plugin/HARNESS.md`
- the existing browser harness work inside the original repository
- the browser harness packaging layout, REPL conventions, and backend integration approach later adapted here to `agent-browser`

`cli-anyweb` is a derivative work prepared from the `CLI-Anything` repository structure and harness approach.

This repository should preserve upstream attribution in documentation, release notes, mirrors, and announcements.

