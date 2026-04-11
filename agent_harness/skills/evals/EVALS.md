# Harness Evals

## Goal

Evaluate whether a stored site reference is still the best known path for a GUI task.

## What To Measure

- success rate
- number of steps
- time to completion
- number of fallback transitions
- ambiguity in element matching
- stability under small UI changes

## Eval Levels

### 1. Smoke Eval

- can the page open
- can the primary anchor be found
- can the first key action succeed

### 2. Flow Eval

- can the full reference be replayed end to end
- do success criteria match the documented expectation

### 3. Robustness Eval

- does the path still work after minor content shifts
- does fallback logic recover from missing anchors

## Recommended Eval Artifact

For each important site flow, store:

- reference file
- test prompt or task description
- expected success markers
- known fallback paths
- last validated date

## Suggested Process

1. Load the relevant site reference
2. Replay the documented primary path
3. If it fails, replay the fallback paths
4. Record where the failure happened
5. Update the reference if a better path is found

## When To Re-Run

- after major site redesigns
- after harness parser changes
- after agent-browser upgrades
- on a fixed cadence for important production flows
