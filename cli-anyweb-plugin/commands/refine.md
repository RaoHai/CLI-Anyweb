# cli-anyweb:refine

Refine an existing site integration.

## Usage

```text
/cli-anyweb:refine <site-name-or-domain> [focus]
```

## What This Command Should Do

Use this command after a site already has starter assets.

The command should:

1. read the existing site profile, starter flow, eval, and path artifact
2. identify obvious gaps, brittleness, or missing flows
3. focus on one improvement area at a time
4. update the relevant assets without discarding previously validated knowledge

## Typical Tasks

- add a new flow
- improve a brittle reference
- update setup for a changed browser requirement
- replace a weaker path artifact with a better one
- add a more robust fallback branch
- split a generic starter flow into a clearer named flow

## Typical Focus Inputs

```text
/cli-anyweb:refine xiaohongshu
/cli-anyweb:refine xiaohongshu "search and open note"
/cli-anyweb:refine github "issue search"
```

## Expected Output

The refinement pass should usually update one or more of:

- `references/<site>/README.md`
- `references/<site>/site.env`
- `cli_anyweb/skills/references/<site>.site-profile.md`
- `cli_anyweb/skills/references/<site>.*.md`
- `cli_anyweb/skills/evals/<site>.*.yaml`
