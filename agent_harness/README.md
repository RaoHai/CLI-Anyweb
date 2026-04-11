# cli-anyweb runtime

`cli-anyweb` is a browser harness built on [Vercel Labs agent-browser](https://github.com/vercel-labs/agent-browser).

This package provides the generic runtime layer:

- browser commands
- snapshot inspection
- path resolution
- session state
- skill, reference, and eval scaffolding

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
cli-anyweb --help
```

## Harness Commands

One-shot commands:

```bash
cli-anyweb open https://example.com
cli-anyweb snapshot
cli-anyweb ls /
cli-anyweb grep "Login"
cli-anyweb click /paragraph[1]/link[0]
cli-anyweb --json status
```

Interactive REPL:

```bash
cli-anyweb
```

Core commands:

- navigation: `open`, `reload`, `back`, `forward`, `info`
- inspection: `snapshot`, `ls`, `cd`, `cat`, `grep`, `pwd`, `find`, `get`
- actions: `click`, `type`
- session utilities: `status`, `daemon-start`, `daemon-stop`

## Output

Every command supports `--json` for machine-readable output:

```bash
cli-anyweb --json ls /
```

## Environment

Preferred environment variables:

- `CLI_ANYWEB_AGENT_BROWSER_FLAGS`
- `CLI_ANYTHING_ANYWEB_ALLOWED_SCHEMES`
- `CLI_ANYTHING_ANYWEB_BLOCK_PRIVATE`

## Skills And References

- Core harness skill: [skills/SKILL.md](./skills/SKILL.md)
- Site references: [skills/references](./skills/references)
- Eval guidance: [skills/evals](./skills/evals)

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
