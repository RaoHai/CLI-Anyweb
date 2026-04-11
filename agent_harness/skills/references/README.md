# References

This directory stores per-site best practices for the GUI harness.

## Purpose

Each reference should explain how to interact with a specific website or product surface in a way that is:

- robust across small UI changes
- easy for a model to replay
- explicit about success checks and fallbacks

## Suggested Naming

- `example.com.md`
- `github.com-login.md`
- `notion.so-editor.md`
- `aws-console-s3.md`

## What A Good Reference Contains

- task scope
- stable page anchors
- best initial command sequence
- recommended click/type order
- common failure states
- retry and fallback strategy
- observable success criteria

## Workflow

1. Explore the site with `gui-agent-harness`
2. Identify the shortest reliable path
3. Write a reference using [_template.md](Y:\CLI-Anything\CLI-anyweb\agent_harness\skills\references\_template.md)
4. Add or update eval coverage in [../evals/EVALS.md](Y:\CLI-Anything\CLI-anyweb\agent_harness\skills\evals\EVALS.md)
