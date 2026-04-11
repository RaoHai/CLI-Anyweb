# <site> SiteMap

## SiteMap

```text
<entry-url>
`-- <main surface>
    |-- <primary navigation>
    |-- <content area>
    `-- <overlay or gate>
```

Use this first section to capture the validated site map in markdown / ASCII.
Prefer real entry URLs, major surfaces, redirects, and overlays over abstract descriptions.

## Logged-Out

- validated branches:
- observed gates:
- public entry points:

## Logged-In

- validated branches:
- pending branches:
- auth-only surfaces:

## Login State Reuse

- profile directory (absolute path):
- how it is set (for example, `CLI_ANYWEB_SITE_PROFILE_DIR`):
- how it is consumed (exported as `AGENT_BROWSER_PROFILE` for agent-browser):
- headed login tip (set `AGENT_BROWSER_HEADED=true` if the window is hidden):

## Main Chains Derived From The SiteMap

- public-first chains:
- auth-required chains:

## Proposed CLI Surface

- command groups to expose:
- auth split to preserve:
- flows still pending validation:
