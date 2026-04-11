# cli-anyweb

Build or scaffold a standalone site-specific web CLI on top of `cli-anyweb`.

## Read First

Read [../HARNESS.md](../HARNESS.md) before doing any site work.

## Usage

```text
/cli-anyweb <site-name-or-domain>
```

## What This Command Should Do

When this command is invoked, it should drive the full first-contact workflow for an unknown website.

The command should:

1. normalize the target site name or domain
2. initialize a standalone site harness if it does not exist yet
3. inspect the site with the generic `cli-anyweb` runtime
4. identify candidate flows
5. validate one minimal reusable starter flow
6. write or update the starter assets inside that generated harness

## Starter Assets

At minimum, the command should expect or create:

```text
sites/<site>/agent-harness/
|- HARNESS.md
|- README.md
|- setup.py
|- site.env
`- cli_anyweb/
   |- __init__.py
   `- <site>/
      |- <site>_cli.py
      |- skills/
      |  |- references/
      |  |  |- <site>.site-profile.md
      |  |  `- <site>.starter-flow.md
      |  `- evals/
      |     |- <site>.starter.eval.yaml
      |     `- <site>.starter.path.yaml
      `- tests/
```

## Implementation Sequence

The intended sequence is:

1. run `bash scripts/setup-cli-anyweb.sh <site>` or `powershell -ExecutionPolicy Bypass -File .\scripts\setup-cli-anyweb.ps1 <site>`
2. install the generated harness under `sites/<site>/agent-harness/`
3. inspect the live site with the standalone CLI plus `open`, `snapshot`, `find`, and `get`
4. update the site profile with entry points, anchors, and risks
5. update the starter flow with one validated path
6. update the eval and path artifact to match the validated flow

## Example

```text
/cli-anyweb xiaohongshu
```

## Expected Output

After a successful first run, the repository should contain:

- a standalone site harness under `sites/<site>/agent-harness/`
- a site-specific console command such as `cli-anyweb-xiaohongshu`
- a site profile
- a starter flow reference
- a starter eval case
- a starter path artifact

The first run does not need to solve the whole website.
It needs to create one replayable starting point in an independent CLI project.
