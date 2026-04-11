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

## Your First Site Integration

Start with a real website:

```bash
/cli-anyweb xiaohongshu
```

The intended workflow is:

1. inspect the site with the generic browser runtime
2. identify candidate flows
3. scaffold starter assets
4. validate one minimal reusable flow
5. save references, path artifacts, and eval cases

## Initialize The Starter Structure

You can also initialize the starter scaffold directly:

```bash
bash scripts/setup-cli-anyweb.sh xiaohongshu
```

This creates the baseline structure for a new site integration.

**Output roots:**

- `references/xiaohongshu/`
- `agent_harness/skills/references/`
- `agent_harness/skills/evals/`

## What The Setup Script Creates

For a site like `xiaohongshu`, the setup script creates:

```text
references/xiaohongshu/
├── README.md
└── site.env

agent_harness/skills/references/
├── xiaohongshu.site-profile.md
└── xiaohongshu.starter-flow.md

agent_harness/skills/evals/
├── xiaohongshu.starter.eval.yaml
└── xiaohongshu.starter.path.yaml
```

This is the closest equivalent to the initialized project structure that `cli-anything` produces for a GUI-app harness.

The important difference is:

- in `cli-anything`, the generated structure comes from the `/cli-anything <software>` build workflow
- in `cli-anyweb`, the site scaffold currently comes from `setup-cli-anyweb.sh` plus the subsequent site-onboarding workflow

## Probe The Site

After setup, use the runtime directly:

```bash
cli-anyweb open https://www.xiaohongshu.com
cli-anyweb snapshot
cli-anyweb find 搜索
cli-anyweb get url
```

## Save The First Real Flow

Once you have one validated starter flow, update:

- `agent_harness/skills/references/<site>.site-profile.md`
- `agent_harness/skills/references/<site>.starter-flow.md`
- `agent_harness/skills/evals/<site>.starter.eval.yaml`
- `agent_harness/skills/evals/<site>.starter.path.yaml`

## Test And Validate

```bash
/cli-anyweb:test xiaohongshu
/cli-anyweb:validate xiaohongshu
```

## Common Workflow

```bash
bash scripts/setup-cli-anyweb.sh xiaohongshu
cli-anyweb open https://www.xiaohongshu.com
cli-anyweb snapshot
/cli-anyweb:validate xiaohongshu
```

## Next Steps

1. read [HARNESS.md](./HARNESS.md)
2. inspect an existing site asset under `agent_harness/skills/references/`
3. add a real starter flow
4. replay and refine it
