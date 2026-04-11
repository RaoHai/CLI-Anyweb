# gui-agent-harness

`gui-agent-harness` is a GUI agent harness built on [Vercel Labs agent-browser](https://github.com/vercel-labs/agent-browser). It provides a stable local runtime for browser automation plus skill/reference scaffolding for site-specific navigation best practices.

## Install

Prerequisites:

- Python 3.10+
- Node.js
- `agent-browser` installed globally
- Chrome or Chromium available locally, or installed via `agent-browser install`

Install the package:

```bash
pip install -e .
npm install -g agent-browser
agent-browser install
```

Verify:

```bash
gui-agent-harness --help
```

## Harness Commands

One-shot commands:

```bash
gui-agent-harness open https://example.com
gui-agent-harness snapshot
gui-agent-harness ls /
gui-agent-harness grep "Login"
gui-agent-harness click /paragraph[1]/link[0]
gui-agent-harness --json status
```

Interactive REPL:

```bash
gui-agent-harness
```

Core commands:

- navigation: `open`, `reload`, `back`, `forward`, `info`
- inspection: `snapshot`, `ls`, `cd`, `cat`, `grep`, `pwd`, `find`, `get`
- actions: `click`, `type`
- session utilities: `status`, `daemon-start`, `daemon-stop`

## Output

Every command supports `--json` for machine-readable output:

```bash
gui-agent-harness --json ls /
```

## Environment

Preferred environment variables:

- `CLI_ANYTHING_ANYWEB_ALLOWED_SCHEMES`
- `CLI_ANYTHING_ANYWEB_BLOCK_PRIVATE`

Legacy `CLI_ANYTHING_BROWSER_*` variables are still accepted for compatibility.

## Skills And References

- Core harness skill: [skills/SKILL.md](Y:\CLI-Anything\CLI-anyweb\agent_harness\skills\SKILL.md)
- Site references: [skills/references](Y:\CLI-Anything\CLI-anyweb\agent_harness\skills\references)
- Eval guidance: [skills/evals](Y:\CLI-Anything\CLI-anyweb\agent_harness\skills\evals)

The intent is:

- keep the harness generic
- add per-site best practices as references
- use those references to guide model-driven path selection and evaluation

## Tests

```bash
pytest agent_harness/tests/test_core.py -v
pytest agent_harness/tests/test_security.py -v
```

Real browser E2E tests require `agent-browser` plus Chrome:

```bash
$env:AGENT_BROWSER_E2E = "1"
pytest agent_harness/tests/test_full_e2e.py -v
```
