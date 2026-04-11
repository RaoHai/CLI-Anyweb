# cli-anyweb:list

List known site integrations, generated assets, or published wrappers in the current workspace.

## Usage

```text
/cli-anyweb:list [--path <directory>] [--depth <n>] [--json]
```

## Options

- `--path <directory>`: directory to search for integrations, default `.` 
- `--depth <n>`: maximum recursion depth, default unlimited
- `--json`: emit machine-readable output

## What This Command Should Look For

When this command is implemented, it should combine information from:

1. published wrappers matching the `cli-anyweb-*` naming pattern
2. local site setup directories such as `references/<site>/`
3. local reference and eval assets that indicate a site has already been onboarded

## Typical Output

Default table output should include:

- site name
- status such as `published`, `local`, or `partial`
- source path
- optional wrapper executable

JSON output should contain the same fields plus summary counts.

## Typical Examples

```text
/cli-anyweb:list
/cli-anyweb:list --depth 2
/cli-anyweb:list --path ./references --json
```

## Notes

- prefer deduplicating by site name
- prefer published wrapper data when both published and local assets exist
- keep local source paths whenever they are available
