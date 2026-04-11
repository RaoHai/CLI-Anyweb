# cli-anyweb Runtime

This directory is the repository-level entry point for the execution layer of `cli-anyweb`.

The actual Python package still lives in [`../agent_harness/`](../agent_harness/) for now, but conceptually this is the runtime layer:

- browser commands
- `agent-browser` backend integration
- snapshot parsing and synthetic paths
- session state
- runtime tests

## Runtime Sources

- package README: [../agent_harness/README.md](../agent_harness/README.md)
- core modules: [../agent_harness/core](../agent_harness/core)
- utils: [../agent_harness/utils](../agent_harness/utils)
- skills: [../agent_harness/skills](../agent_harness/skills)
- tests: [../agent_harness/tests](../agent_harness/tests)

## Why This Exists

At the repository level we want the split to be obvious:

- `runtime/` is the generic execution engine
- `cli-anyweb-plugin/` is the onboarding methodology and plugin scaffold
- `references/` holds site-specific setup material

This keeps the repo easier to understand without forcing an immediate Python package rename.
