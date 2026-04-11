# TEST.md

## Test Inventory Plan

- `test_core.py`: 25 unit tests planned for session, page, and filesystem behavior
- `test_security.py`: 25 unit tests planned for URL validation and DOM sanitization
- `test_full_e2e.py`: 8 E2E tests planned for CLI startup, JSON output, session commands, and live agent-browser workflows

## Unit Test Plan

### `core/session.py`

- test initial session state
- test URL history and forward stack updates
- test working directory changes
- test daemon mode toggling

Expected test count: 10

### `core/page.py`

- test URL validation before navigation
- test open updates session state
- test reload, back, and forward behavior
- test page info output

Expected test count: 8

### `core/fs.py`

- test path resolution for absolute and relative paths
- test `.` and `..` handling
- test working directory updates after successful `cd`
- test list, cat, and grep pass-through behavior

Expected test count: 7

### `utils/security.py`

- test blocked schemes
- test allowed schemes override
- test explicit-scheme requirement
- test private network blocking
- test DOM text sanitization and injection flagging

Expected test count: 25

## E2E Test Plan

- verify CLI help renders without crashing
- verify JSON session output is parseable
- verify daemon start/stop paths return structured output
- verify live navigation against a real page when `AGENT_BROWSER_E2E=1`

## Realistic Workflow Scenarios

### Read-and-click flow

- Simulates: opening a page, finding a target element, and clicking it
- Operations chained: `open` -> `ls` -> `grep` -> `click`
- Verified: commands succeed and return structured output

### Form fill flow

- Simulates: locating inputs and typing values
- Operations chained: `open` -> `grep` -> `type` -> `click`
- Verified: live interaction path works under agent-browser

### Interactive session flow

- Simulates: repeated exploratory browsing inside the REPL
- Operations chained: REPL start -> `session daemon-start` -> `fs cd` -> `fs pwd`
- Verified: stateful path handling and daemon mode response

## Test Results

Not appended yet in this scaffold. Run the test commands in `README.md`, then paste the full `pytest -v --tb=no` output here once the local agent-browser environment is available.
