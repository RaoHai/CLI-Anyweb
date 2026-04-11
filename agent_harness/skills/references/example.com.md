# example.com

## Scope

- target site: `https://example.com`
- target flow: verify the harness can open a page, inspect the snapshot, and follow the canonical outbound link
- preconditions: none

## Stable Anchors

- heading: `Example Domain`
- link text: `Learn more`
- page is intentionally minimal and stable

## Recommended Path

1. Open `https://example.com`
2. Inspect the root snapshot
3. Confirm the heading exists
4. Search for `Learn more`
5. Click the matching link

## Suggested Harness Commands

```bash
gui-agent-harness open https://example.com
gui-agent-harness --json ls /
gui-agent-harness --json cat /heading[0]
gui-agent-harness --json grep "Learn more"
gui-agent-harness --json click /paragraph[1]/link[0]
```

## Common Failure Modes

- the link path may change if snapshot grouping changes
- `info` may lag behind click-triggered navigation if session state is not refreshed yet

## Fallback Strategy

- if the stored path changes, re-run `grep "Learn more"` and click the returned path
- if the heading path changes, search for `Example Domain` instead of relying on `/heading[0]`

## Success Criteria

- the page opens successfully
- the heading `Example Domain` is readable
- the outbound link is discoverable and clickable
