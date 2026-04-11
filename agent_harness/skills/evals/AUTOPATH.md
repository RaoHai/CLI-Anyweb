# Automatic Path Discovery

## Goal

Use a model plus the harness to discover the most reliable browser path for a task, then turn that path into a reusable site reference.

## Discovery Loop

1. Start with a task definition
2. Explore the target site with `gui-agent-harness`
3. Save the observed anchors, labels, and intermediate states
4. Ask a model to propose several candidate paths
5. Replay each path against the live site
6. Score each path for robustness, brevity, and clarity
7. Promote the best path into `skills/references/<site>.md`

## Inputs To Give The Model

- target task
- current URL
- snapshot output
- known stable anchors
- known failure states
- constraints such as auth, rate limits, or anti-bot surfaces

## What The Model Should Produce

- a primary path
- one or two fallback paths
- expected success signals
- specific points where the flow is fragile
- suggestions for what to evaluate repeatedly

## Recommended Output Shape

```text
Task
Primary path
Fallback path A
Fallback path B
Success checks
Known risks
```

## Promotion Rule

Only promote a path into a site reference if it:

- succeeds repeatedly
- uses readable anchors
- avoids brittle positional guesses when possible
- has a clear fallback when the primary route fails
