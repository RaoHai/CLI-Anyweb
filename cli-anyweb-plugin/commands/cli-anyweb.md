# cli-anyweb

Build or scaffold a site-specific web CLI on top of `cli-anyweb`.

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
2. initialize the starter scaffold if it does not exist yet
3. inspect the site with the generic `cli-anyweb` runtime
4. identify candidate flows
5. validate one minimal reusable starter flow
6. write or update the starter assets

## Starter Assets

The initialized structure should come from the site setup scaffold plus follow-up discovery work.

At minimum, the command should expect or create:

```text
references/<site>/
├── README.md
└── site.env

cli_anyweb/skills/references/
├── <site>.site-profile.md
└── <site>.starter-flow.md

cli_anyweb/skills/evals/
├── <site>.starter.eval.yaml
└── <site>.starter.path.yaml
```

## Implementation Sequence

The intended sequence is:

1. run `bash scripts/setup-cli-anyweb.sh <site>`
2. inspect the live site with `cli-anyweb open`, `snapshot`, `find`, and `get`
3. update the site profile with entry points, anchors, and risks
4. update the starter flow with one validated path
5. update the eval and path artifact to match the validated flow

## Example

```text
/cli-anyweb xiaohongshu
```

## Expected Output

After a successful first run, the repository should contain:

- a site setup directory under `references/<site>/`
- a site profile
- a starter flow reference
- a starter eval case
- a starter path artifact

The first run does not need to solve the whole website.
It needs to create one replayable starting point.
