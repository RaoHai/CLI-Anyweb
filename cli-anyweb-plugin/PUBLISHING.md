# Publishing

This plugin scaffold is designed so site integrations can eventually be distributed in a form that feels similar to upstream `cli-anything-plugin` outputs.

## What A Published Site Integration Should Include

For each real site, prefer shipping:

- a setup wrapper or setup instructions
- site references
- path artifacts
- eval cases
- any required browser flags or environment notes
- optional helper commands for auth or preflight checks

## Minimum Release Checklist

- setup instructions are documented
- required browser flags are documented
- at least one real reference exists
- at least one replayable path artifact exists
- at least one eval case exists
- the site-specific wrapper is runnable end to end
- the integration can be revalidated by another contributor
