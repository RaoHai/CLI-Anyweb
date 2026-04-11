# ROADMAP

## Goal

`gui-agent-harness` is not trying to be only a browser control wrapper.

The long-term goal is to turn ordinary websites into reusable, agent-native tools:

- agents can operate sites through a stable structured CLI
- successful paths do not need to be rediscovered every run
- site knowledge can be captured, replayed, evaluated, and improved over time

## Current Assessment

If we measure against that vision:

- browser harness foundation: mostly in place
- flat CLI surface: in place
- snapshot-based inspection primitives: in place
- reusable site knowledge: early
- replay/eval automation: early
- accumulating path intelligence: largely missing

In short:

- we already have a usable harness
- we do not yet have a full agent-native web operating layer

## What Is Done

- `agent-browser` is integrated as the backend
- flat top-level commands are available, including `open`, `snapshot`, `ls`, `click`, `type`, `get`, and `find`
- snapshot parsing and path-to-ref resolution exist
- skills, references, and eval docs have been scaffolded
- the grouped compatibility CLI surface has been removed
- core tests and CLI surface tests are in place

## Main Gaps

### 1. Reference Coverage Is Too Thin

Right now the project has the structure for reusable site knowledge, but almost no real coverage.

What is missing:

- real site references beyond `example.com`
- references for common, high-value workflows
- guidance on failure modes and fallback paths grounded in real sites

Why it matters:

- without real references, the model still has to rediscover paths from scratch on most websites

### 2. Replay/Eval Is Still Mostly Documentation

The repository already describes candidate paths, replay, and scoring, but does not yet provide a practical automated loop.

What is missing:

- a concrete path artifact format
- a replay runner
- a scoring mechanism
- a way to compare candidate paths over time

Why it matters:

- without replay/eval, successful runs do not turn into durable operational knowledge

### 3. Path Knowledge Does Not Yet Compound

The most important missing capability is accumulation.

What is missing:

- a mechanism to capture useful paths from successful runs
- a place to persist them in a structured way
- a strategy for preferring known-good paths before fresh exploration
- invalidation and refresh behavior when sites change

Why it matters:

- this is the difference between a browser harness and an agent-native web layer

### 4. Product Surface Is Still More "Tooling" Than "System"

The current CLI is clean, but the project still feels like a good developer tool rather than a complete agent operating substrate.

What is missing:

- stronger end-to-end workflows
- clearer primitives for extraction, waiting, retries, and reusable actions
- a stronger story for how agents discover, save, and reuse knowledge by default

## Priorities

### P0: Make Reuse Real

This is the most important stage.

Deliverables:

- define a concrete path artifact format
- build a replay runner for saved paths
- build a scoring model for path quality
- add structured persistence for path knowledge
- allow the harness to prefer known-good paths before exploring again

Success looks like:

- the same site flow gets faster and more stable after it has been solved once

### P1: Build Real Site Coverage

Once reuse exists, the next highest-leverage step is coverage.

Deliverables:

- add 5 to 10 real site references
- focus on common and representative workflows
- document stable anchors, primary path, fallback path, and success criteria
- test that references can be replayed

Suggested early targets:

- GitHub login and repository navigation
- Google search flows
- Notion workspace navigation
- common cloud console entry flows
- internal CRUD-style admin panels

Success looks like:

- the repository contains real examples of reusable web knowledge, not just scaffolding

### P2: Improve the Agent Operating Surface

After reuse and coverage, improve ergonomics and reliability.

Deliverables:

- add higher-level commands or patterns for waiting and extraction
- improve snapshot and path stability on dynamic pages
- improve error reporting and retry behavior
- make the REPL and CLI friendlier for long-running workflows

Success looks like:

- agents can complete more realistic workflows with less prompt-level orchestration

### P3: Move Toward a True Agent-Native Web Substrate

This is the longer-term stage implied by the README vision.

Deliverables:

- continuous path evaluation against changing sites
- automatic refresh of stale references
- ranking and selection of candidate paths based on prior outcomes
- stronger default behavior for "reuse first, explore second"

Success looks like:

- websites increasingly behave like stable tools from the agent's perspective

## Near-Term Execution Plan

### Phase 1

- define the path artifact schema
- implement replay for a saved path
- implement scoring for success/failure and basic quality metrics

### Phase 2

- persist best-known paths into site references or a structured path store
- add path selection logic that checks known-good paths first
- add regression tests around replay and path selection

### Phase 3

- write several real references
- validate them with replay/eval
- refine the authoring pattern for future references

## Suggested Definition Of Done For The Vision

The README vision starts to become true when all of the following are normal:

- an agent can operate a site through a stable CLI
- successful paths are captured after use
- those paths are reused before fresh exploration
- paths can be replayed and scored automatically
- stale paths can be detected and refreshed
- multiple real websites have maintained references that demonstrably save time and tokens

## Summary

The project is already a credible browser harness.

The biggest remaining step is not more raw browser control. It is building the accumulation layer:

- capture what worked
- replay it
- score it
- reuse it
- improve it over time

That is the shortest path from "browser automation tool" to "agent-native web infrastructure."
