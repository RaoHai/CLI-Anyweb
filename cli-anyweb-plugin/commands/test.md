# cli-anyweb:test

Test site-specific references, path artifacts, and evals.

## Usage

```text
/cli-anyweb:test <site-name-or-domain>
```

## What This Command Should Do

This command should replay the current saved site assets and report whether the integration is still healthy.

The command should:

1. load the current site profile and saved flow artifacts
2. replay the primary path
3. replay fallback paths when they exist
4. record failures, drift, and step inflation
5. summarize whether the current integration is still usable

## Core Metrics

The most useful starter metrics are:

- success
- step count
- fallback used
- terminal page type
- expected anchor match

## Example

```text
/cli-anyweb:test xiaohongshu
```

## Expected Output

The result should clearly say:

- which flow was replayed
- whether it succeeded
- where it failed if it did not succeed
- whether setup assumptions such as real UA requirements still matter
