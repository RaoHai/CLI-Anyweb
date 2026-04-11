# cli-anyweb:validate

Validate whether a site integration meets plugin standards.

## Usage

```text
/cli-anyweb:validate <site-name-or-domain>
```

## What This Command Should Check

This command should verify that a site integration is structurally complete enough to be useful to another contributor or agent.

## Validation Targets

- site profile exists
- starter flow exists
- path artifact exists
- eval case exists
- setup requirements are documented
- the assets point to a coherent starter flow rather than unrelated fragments

## Example

```text
/cli-anyweb:validate xiaohongshu
```

## Pass Criteria

A minimal passing integration should provide:

- one site setup directory
- one site profile
- one replayable starter flow
- one eval case for that starter flow
- one path artifact for that starter flow

## Failure Examples

Examples of a failing integration:

- setup exists but no validated flow has been saved
- references exist but no eval artifact exists
- eval exists but the referenced flow is undocumented
- site requires a real UA but `site.env` does not mention it
