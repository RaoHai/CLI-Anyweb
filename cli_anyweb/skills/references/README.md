# References

This directory stores shared reference examples for the generic cli-anyweb runtime.

## Purpose

Each reference should explain how to interact with a website or product surface in a way that is:

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

1. Explore the site with `cli-anyweb`
2. Identify the shortest reliable path
3. For a real site integration, write the reference inside the generated site harness under `sites/<site>/agent-harness/`
4. Use [_template.md](./_template.md) only for shared examples or generic patterns
