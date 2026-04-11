# xiaohongshu SiteMap

## Logged-Out

```text
https://www.xiaohongshu.com
`-- /explore
    |-- top bar
    |   |-- logo / home
    |   |-- search textbox
    |   |-- search action
    |   |-- creator center
    |   `-- business
    |-- left navigation
    |   |-- discover
    |   |-- live
    |   |-- publish
    |   |-- notifications
    |   `-- login
    |-- category tabs
    |   |-- recommended
    |   |-- fashion
    |   |-- food
    |   |-- beauty
    |   |-- media
    |   |-- career
    |   |-- relationships
    |   |-- home
    |   |-- gaming
    |   |-- travel
    |   `-- fitness
    |-- public feed cards
    |   |-- cover link
    |   |-- title link
    |   |-- author link
    |   `-- like / count
    `-- tourist overlay
        `-- login recommendation overlay

https://www.xiaohongshu.com/search_result?keyword=<query>
`-- /search_result?keyword=<query>&type=51
    |-- search tabs
    |   |-- all
    |   |-- posts
    |   |-- videos
    |   `-- users
    |-- result list
    `-- search login gate

overlay dismiss fallback
`-- /explore?source=tourist_search
```

Validated:

- real desktop UA is required to avoid the initial risk page
- public home resolves to `/explore`
- public search URL shape exists, but result access can be gated
- feed cards are visible in tourist mode, but note-detail navigation is not yet validated

## Logged-In

```text
/explore
|-- home feed
|-- search
|   |-- all
|   |-- posts
|   |-- videos
|   `-- users
|-- note detail (logged-in)
|   |-- content
|   |-- comments
|   `-- author profile
|-- publish
|-- notifications
`-- profile
```

Validated (session):

- left navigation includes a profile entry instead of a login entry
- home feed renders with user-linked content in the main grid
- search textbox is present in the top bar
- publish navigates to `https://creator.xiaohongshu.com/publish/publish?source=official`
- notifications navigates to `https://www.xiaohongshu.com/notification`
- profile navigates to `https://www.xiaohongshu.com/user/profile/<id>`
- open-first-note can navigate to `https://www.xiaohongshu.com/explore/<note-id>?xsec_token=<token>`
- note detail shows author block, content text, and a comment list in the snapshot
- inline media appears as clickable images inside the detail surface
- note detail HTML embeds `noteDetailMap` with `title`, `desc`, `commentCount`, and `imageList`
- image assets expose `urlDefault` and `urlPre` in the embedded data

Login tip:

- set `AGENT_BROWSER_HEADED=true` in `site.env` for a visible login window

Login state reuse:

- set `CLI_ANYWEB_SITE_PROFILE_DIR` in `site.env` (absolute path)
- wrapper exports it as `AGENT_BROWSER_PROFILE` for agent-browser

## Main Chains Derived From The SiteMap

Public-first:

- `home`: open `/explore` and verify the tourist home surface
- `search`: open the direct search URL shape and determine whether the query is usable before gating
- `search-video`: open search and switch to the "视频" tab to filter video posts
- `open-note`: open a detail URL once a reachable path is validated (logged-in: `https://www.xiaohongshu.com/explore/<note-id>?xsec_token=<token>`)

Pending validation:

- clicking the first note-like link from `/explore` can remain on `/explore` in some cases
- clicking video results in the search tab did not navigate to a detail URL in this session

Auth-required:

- `login`: establish an authenticated browser session
- `publish`: enter creator flow and start a new post
- `notifications`: open the notifications surface
- `profile`: open the user profile surface
- `note-detail`: open a detail page and parse content + comments

## Golden Path (agent-browser)

Flow: `home -> first-note -> detail`

```text
1) open https://www.xiaohongshu.com/explore
2) snapshot
3) choose a note card ref:
   - prefer a link node that contains an image child (cover)
   - avoid nav items like discover/live/publish/notifications/profile/login
   - avoid footer/legal links
4) click the chosen ref
5) get url
```

Success criteria:

- URL contains `/explore/`
- URL includes `?xsec_token=` when logged-in

Replay (example command skeleton):

```bash
agent-browser open https://www.xiaohongshu.com/explore
agent-browser snapshot
agent-browser click @<ref>
agent-browser get url
```

Ref selection heuristic (from snapshot text):

- scan for `link` nodes that do not have a quoted label (cover cards often appear as `link [ref=...]` followed by `image`)
- if multiple, pick the first one that is followed by an `image` line within 3 lines
- skip any link whose label matches nav items (discover/live/publish/notifications/profile/login)

## Golden Paths (from CLI experiments)

Flow: `search --type video`

```bash
cli-anyweb-xiaohongshu search --query <keyword> --type video
```

Filter tab group structure in snapshot:

```text
- generic
  - generic [ref=eN]   clickable  StaticText "全部"
  - generic [ref=eN+1] clickable  StaticText "图文"
  - generic [ref=eN+2] clickable  StaticText "视频"   ← clicked by --type video
  - generic [ref=eN+3] clickable  StaticText "用户"
```

Notes:

- the page may also render a user-profile panel with its own "视频" tab — clicking it navigates to the profile instead of filtering results
- `_find_search_filter_tab_ref` disambiguates by verifying "全部", "图文", "用户" appear within ±8 lines
- URL does not change when the tab is switched; success is the result list updating to video cards
- a 2500ms `wait` after `open` is required before snapshot — the SPA card grid renders asynchronously after page load
- the snapshot is taken before the tab click and reused for card parsing; a second post-click snapshot is avoided because it hangs on dynamic pages
- snapshot `refs` dict does not expose `href` for link nodes — cover card note IDs cannot be extracted this way; `帖子ID` column shows `-`

Validated:

- `search --query 穿搭 --type video`: filter tab at `generic [ref=e15]`, 25-card table with title/author/likes printed (2026-04-12)

Flow: `open-note --extract`

```bash
cli-anyweb-xiaohongshu open-note --url <detail-url> --extract
cli-anyweb-xiaohongshu open-note --note-id <id> --xsec-token <token> --extract
```

Notes:

- `--extract` waits 1500 ms then parses `noteDetailMap` from the page HTML
- falls back to `window.__INITIAL_STATE__` via eval_js (not available on Windows)
- outputs JSON: `title`, `desc`, `commentCount`, `imageDefaultUrls`, `imagePreviewUrls`, `videoUrls`

Pending:

- SPA link navigation (cover cards / title links in search or explore) does not reliably change the URL when clicked via agent-browser — obtain detail URLs from HTML or external sources instead
- video asset URLs in `videoUrls` need a video-type note to validate
- direct image downloads can use `imageDefaultUrls` or `imagePreviewUrls`
