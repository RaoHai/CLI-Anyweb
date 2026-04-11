# xiaohongshu.com site profile

## Scope

- site: `https://www.xiaohongshu.com`
- onboarding status: first-contact profile
- observation date: `2026-04-11`
- observation environment: current workspace network using `agent-browser`

## Observed Entry Behavior

Opening `https://www.xiaohongshu.com` in the current environment does not land on the normal explore surface.

Observed redirect shape:

- `/website-login/error`
- query contains `error_code=300012`

Observed snapshot characteristics:

- a short error-state page instead of the normal homepage
- an error code anchor: `300012`
- two clickable controls that appear to be feedback and return-home actions

## Initial Site Assessment

Likely site type:

- consumer content platform
- feed and search driven
- mixed public content and account-gated surfaces

Likely high-value interaction surfaces:

- explore/feed browsing
- keyword search
- opening note detail pages
- creator/profile navigation
- login and account surfaces

## Important Constraints

- current environment is blocked by a site-side risk gate before normal homepage exploration
- public-flow references cannot yet be validated from this network alone
- normal-path discovery should resume only after access is possible from a reliable network environment

## Candidate Flows

### 1. detect_risk_gate_and_exit

Why it exists:

- it is the only currently validated real flow in this environment

Why it matters:

- it prevents the agent from pretending it has access to normal site content
- it provides an environment readiness check before deeper references run

### 2. search_and_open_note

Why it is a good future starter flow:

- likely low side effect
- likely does not require publishing permissions
- likely representative of the platform's primary information access pattern

Current status:

- not yet validated from the current network environment

### 3. open_note_detail_from_feed

Why it is useful:

- represents the feed-to-detail transition

Current status:

- blocked behind the current entry restriction

## Selected Starter Flow

Current validated starter flow:

- `detect_risk_gate_and_exit`

Next target flow once normal access is available:

- `search_and_open_note`

## Stable Anchors Seen So Far

- URL path fragment: `website-login/error`
- error code: `300012`
- short gated page with only a few clickables

## Suggested Next Onboarding Step

When a reliable network environment is available:

1. reopen `https://www.xiaohongshu.com`
2. confirm whether the site lands on `explore`, `search`, or another public home surface
3. collect top navigation anchors
4. generate candidate flows again
5. validate `search_and_open_note` as the first normal public reference
