# xiaohongshu Starter Flow

## Scope

- target site: xiaohongshu
- target flow: `home_entry_with_real_ua`
- preconditions: set a real desktop browser UA through `CLI_ANYWEB_AGENT_BROWSER_FLAGS`

## Stable Anchors

- visible landmarks: top navigation, feed cards, search entry
- reliable labels or headings: search-related text, public feed text, modal copy
- persistent buttons or inputs: search entry, dismiss buttons for lightweight overlays

## Recommended Path

1. Open: `https://www.xiaohongshu.com`
2. Snapshot or inspect: capture the public surface and verify this is not a risk-intercept page
3. First interaction: identify whether search entry is visible
4. Follow-up interactions: dismiss any lightweight popups without logging in
5. Verify completion: confirm a normal public home surface is available for the next flow

## Suggested Harness Commands

```bash
cli-anyweb-xiaohongshu open https://www.xiaohongshu.com
cli-anyweb-xiaohongshu snapshot
cli-anyweb-xiaohongshu find "search"
cli-anyweb-xiaohongshu get url
```

## Common Failure Modes

- popup or cookie banner: lightweight overlays can hide the feed
- lazy-loading or delayed widgets: the home feed may render after initial load
- auth redirect: some entry points may bounce to login or a gated path
- duplicate labels: repeated labels can make text matching ambiguous

## Fallback Strategy

- if primary anchor fails: re-snapshot and inspect top-level visible refs before clicking
- if the page structure changes: fall back to URL and landmark validation instead of one label
- if text search is ambiguous: prefer persistent navigation or container-level refs

## Success Criteria

- page state that proves success: a normal public home surface, not a risk-gate or login-only intercept
- URL, title, or text that proves completion: URL remains under `www.xiaohongshu.com` and the snapshot shows public navigation or feed content
