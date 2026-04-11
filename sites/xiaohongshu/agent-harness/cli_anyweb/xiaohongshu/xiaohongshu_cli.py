#!/usr/bin/env python3
"""Standalone wrapper for cli-anyweb-xiaohongshu."""

import os
import sys
from pathlib import Path


def _import_runtime_cli():
    try:
        from cli_anyweb.cli_anyweb_cli import cli as imported_cli
        return imported_cli
    except ModuleNotFoundError:
        for parent in Path(__file__).resolve().parents:
            if (parent / "cli_anyweb" / "cli_anyweb_cli.py").exists():
                repo_root_str = str(parent)
                if repo_root_str not in sys.path:
                    sys.path.insert(0, repo_root_str)
                import cli_anyweb as namespace_pkg

                runtime_pkg_dir = str(parent / "cli_anyweb")
                if runtime_pkg_dir not in namespace_pkg.__path__:
                    namespace_pkg.__path__.append(runtime_pkg_dir)
                break
        from cli_anyweb.cli_anyweb_cli import cli as imported_cli
        return imported_cli


def _load_site_env():
    site_root = Path(__file__).resolve().parents[2]
    env_file = site_root / "site.env"
    if not env_file.exists():
        return

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value

    os.environ.setdefault("CLI_ANYWEB_SITE_ROOT", str(site_root))


def main():
    _load_site_env()
    runtime_cli = _import_runtime_cli()
    runtime_cli(prog_name="cli-anyweb-xiaohongshu")


if __name__ == "__main__":
    main()
