# xiaohongshu Entry Risk Gate

## Scope

- target site: `https://www.xiaohongshu.com`
- target flow: detect site-side risk gate on entry and stop deeper flow execution
- preconditions: none

## Stable Anchors

- URL fragment: `website-login/error`
- reliable code anchor: `300012`
- page shape: very short error-state snapshot with only a few clickable items

## Recommended Path

1. Open `https://www.xiaohongshu.com`
2. Capture a fresh snapshot
3. Confirm that the entry page is a gated error surface, not the normal homepage
4. Confirm the presence of `300012` or an equivalent risk marker
5. Mark the site as blocked for this environment
6. Stop normal content-flow execution and report the gating condition

## Suggested Harness Commands

```bash
cli-anyweb-xiaohongshu open https://www.xiaohongshu.com
cli-anyweb-xiaohongshu snapshot
cli-anyweb-xiaohongshu find 300012
cli-anyweb-xiaohongshu get url
```

## Common Failure Modes

- the risk page may be reworded while keeping the same behavior
- the error code may change even if the site remains blocked
- the entry page may redirect again before the snapshot is captured

## Fallback Strategy

- if `300012` is missing, inspect the URL for `website-login/error`
- if the URL check is inconclusive, inspect whether the snapshot is a short error-state page instead of a normal homepage
- if the site no longer blocks entry, switch to validating the next starter flow instead of this gate flow

## Success Criteria

- the page clearly indicates entry is blocked by a site-side restriction
- the flow exits without pretending that normal homepage exploration succeeded
- the agent records that a reliable network is required before deeper public-flow references are validated
