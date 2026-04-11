# cli-anyweb-xiaohongshu

Standalone site harness for xiaohongshu.

## Install

```bash
cd sites/xiaohongshu/agent-harness
pip install -e .
```

## Run

```bash
cli-anyweb-xiaohongshu --help
cli-anyweb-xiaohongshu open https://www.xiaohongshu.com
```

## Local Assets

- `site.env`: site-specific browser flags
- `cli_anyweb/xiaohongshu/skills/references/`: site references
- `cli_anyweb/xiaohongshu/skills/evals/`: replay and validation assets

## Current Notes

- xiaohongshu can block the default headless browser fingerprint
- prefer a real desktop Chrome user agent before probing the public home page
