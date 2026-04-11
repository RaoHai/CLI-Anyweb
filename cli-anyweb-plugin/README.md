# cli-anyweb Plugin

Build reusable, site-specific web CLIs using the `cli-anyweb` harness methodology.

## Overview

The `cli-anyweb-plugin` directory plays the same role that `cli-anything-plugin` does upstream: it is the contributor-facing toolkit for turning a target surface into an agent-usable CLI.

Here the target is not a desktop GUI app.
It is a website.

## What It Does

This plugin structure helps contributors:

1. analyze an unknown website
2. identify candidate flows
3. validate one minimal reusable flow
4. generate a standalone site harness with its own CLI
5. save references, path artifacts, and eval cases inside that harness
6. define site-specific setup such as a real UA or custom browser flags

The result is not just one successful browser session.
The result is a replayable site integration with its own runnable CLI.

## Included Structure

- `.claude-plugin/plugin.json`: plugin metadata
- `HARNESS.md`: source-of-truth SOP
- `QUICKSTART.md`: first-use guide
- `PUBLISHING.md`: packaging and distribution notes
- `commands/`: plugin command definitions
- `guides/`: deeper implementation notes inherited from the upstream plugin shape
- `scripts/setup-cli-anyweb.sh`: bash site setup helper
- `scripts/setup-cli-anyweb.ps1`: PowerShell site setup helper
- `templates/`: reusable generation templates
- `tests/`: plugin-level tests
- `repl_skin.py`: shared REPL skin helper
- `skill_generator.py`: generator scaffold adapted from the upstream layout
- `verify-plugin.sh`: structure validation helper

## Commands

- `/cli-anyweb <site-or-url>`: onboard a new website into the harness workflow
- `/cli-anyweb:refine <site>`: expand or harden an existing site integration
- `/cli-anyweb:test <site>`: replay current eval assets
- `/cli-anyweb:validate <site>`: check whether a site integration meets plugin standards
- `/cli-anyweb:list`: list known site integrations or generated outputs

## Methodology

The canonical SOP lives in [HARNESS.md](./HARNESS.md).

At a high level:

1. scaffold a standalone site harness
2. inspect the site with the generic `cli-anyweb` runtime
3. model the site before assuming flows
4. save the first validated starter flow inside the generated harness
5. replay and score that flow
6. expand coverage incrementally

## Relationship To The Repository

- runtime package: [../cli_anyweb/README.md](../cli_anyweb/README.md)
- plugin SOP: [./HARNESS.md](./HARNESS.md)
- repo overview: [../README.md](../README.md)

Use the runtime when you need browser commands.
Use this plugin when you need a repeatable workflow for turning a site into a CLI surface.
