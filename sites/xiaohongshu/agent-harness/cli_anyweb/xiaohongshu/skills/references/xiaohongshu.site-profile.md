# xiaohongshu Site Profile

## Site Summary

- domain: `www.xiaohongshu.com`
- site type: social content discovery
- public or gated: partially public, but entry is sensitive to browser fingerprinting
- auth requirements: public home and search may be visible without login, but some detail flows can redirect or risk-gate

## Entry Points

- primary entry URL: `https://www.xiaohongshu.com`
- alternate entry URLs: `https://www.xiaohongshu.com/explore`, direct note URLs, search result URLs

## Main Surfaces

- primary navigation: home feed, search, creator/account entry points
- search surface: global search entry and search results
- detail surface: note detail page
- account surface: profile and login-related pages

## Stable Anchors

- labels: search-related text, note titles, creator names
- buttons: search entry, login-related actions, modal dismiss buttons
- headings: page titles and section headings on public surfaces
- landmarks: top navigation, feed cards, note detail container

## Risks

- anti-bot or risk controls: high; default headless UA can trigger a risk page
- login walls: medium; some flows are login-gated
- dynamic content: high; feed and search results are heavily dynamic
- localization issues: medium; public text is primarily Chinese

## Candidate Flows

- starter flow: open the public home page with a real desktop UA and verify a normal public surface
- next likely flow: search for a query and open one note detail
- risky flow to avoid first: login, posting, image upload, or creator-side actions
