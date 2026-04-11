# Quick Start Guide

Get started with the `cli-anyweb` plugin in a few minutes.

## Installation

```bash
# Copy plugin to your plugin directory
cp -r /path/to/cli-anyweb-plugin ~/.claude/plugins/cli-anyweb

# Reload plugins
/reload-plugins

# Verify installation
/help cli-anyweb
```

## Your First Site Harness

Start with a real website:

```bash
/cli-anyweb xiaohongshu
```

The intended workflow is:

1. scaffold a standalone site harness
2. inspect the site with the generic browser runtime
3. identify candidate flows
4. validate one minimal reusable flow
5. save references, path artifacts, and eval cases inside that site harness

## Initialize The Site Harness

You can also initialize the standalone scaffold directly:

```bash
bash scripts/setup-cli-anyweb.sh xiaohongshu
```

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-cli-anyweb.ps1 xiaohongshu
```

This creates a standalone harness project under `sites/xiaohongshu/agent-harness/`.

## What The Setup Script Creates

For a site like `xiaohongshu`, the setup script creates:

```text
sites/xiaohongshu/agent-harness/
|- HARNESS.md
|- README.md
|- setup.py
|- site.env
`- cli_anyweb/
   |- __init__.py
   `- xiaohongshu/
      |- __init__.py
      |- __main__.py
      |- xiaohongshu_cli.py
      |- README.md
      |- skills/
      |  |- SKILL.md
      |  |- references/
      |  |  |- xiaohongshu.site-profile.md
      |  |  `- xiaohongshu.starter-flow.md
      |  `- evals/
      |     |- xiaohongshu.starter.eval.yaml
      |     `- xiaohongshu.starter.path.yaml
      `- tests/
         |- __init__.py
         `- TEST.md
```

This is the closest equivalent to the initialized project structure that `cli-anything` produces for a software-specific harness.

## Install And Run The Generated CLI

```bash
cd sites/xiaohongshu/agent-harness
pip install -e .
cli-anyweb-xiaohongshu --help
```

## Probe The Site

After setup, use the site-specific CLI directly:

```bash
cli-anyweb-xiaohongshu open https://www.xiaohongshu.com
cli-anyweb-xiaohongshu snapshot
cli-anyweb-xiaohongshu find "search"
cli-anyweb-xiaohongshu get url
```

## Save The First Real Flow

Once you have one validated starter flow, update:

- `sites/<site>/agent-harness/site.env`
- `sites/<site>/agent-harness/cli_anyweb/<site>/skills/references/<site>.site-profile.md`
- `sites/<site>/agent-harness/cli_anyweb/<site>/skills/references/<site>.starter-flow.md`
- `sites/<site>/agent-harness/cli_anyweb/<site>/skills/evals/<site>.starter.eval.yaml`
- `sites/<site>/agent-harness/cli_anyweb/<site>/skills/evals/<site>.starter.path.yaml`

## Common Workflow

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-cli-anyweb.ps1 xiaohongshu
cd .\sites\xiaohongshu\agent-harness
pip install -e .
cli-anyweb-xiaohongshu open https://www.xiaohongshu.com
cli-anyweb-xiaohongshu snapshot
```

## Next Steps

1. read [HARNESS.md](./HARNESS.md)
2. inspect the generated harness under `sites/<site>/agent-harness/`
3. add a real starter flow
4. replay and refine it
