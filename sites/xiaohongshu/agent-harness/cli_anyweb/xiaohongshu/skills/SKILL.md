---
name: "cli-anyweb-xiaohongshu"
description: "Site harness for xiaohongshu (小红书). Use when working on xiaohongshu tasks: home feed, search (--type all|video|notes|users), open-note (--extract), login, publish, notifications, profile."
---

# cli-anyweb-xiaohongshu Skill

Use this site harness when working on xiaohongshu.

## Local Assets

- `skills/references/xiaohongshu.sitemap.md`
- `skills/evals/xiaohongshu.starter.eval.yaml`
- `skills/evals/xiaohongshu.starter.path.yaml`

## Commands

| Command | Description |
|---|---|
| `home` | Open `/explore` |
| `search --query Q [--type all\|video\|notes\|users]` | Search with optional content-type tab |
| `open-note --url URL \| --note-id ID [--xsec-token T] [--extract]` | Open a note; `--extract` prints JSON |
| `login` / `publish` / `notifications` / `profile` | Auth-required surfaces |

## Operating Principle

Prefer the standalone `cli-anyweb-xiaohongshu` command over the generic runtime when site-specific setup matters.

Always set a real desktop UA in `site.env` before validating public-page flows.
