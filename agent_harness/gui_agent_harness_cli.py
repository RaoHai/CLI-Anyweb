#!/usr/bin/env python3
"""cli-anyweb - a command-line interface for browser automation via agent-browser.

This CLI uses a flat command surface that maps closely to browser actions while
still exposing snapshot-tree inspection helpers for exploration.

Usage:
    # Direct browser commands
    cli-anyweb open https://example.com
    cli-anyweb reload
    cli-anyweb back
    cli-anyweb forward
    cli-anyweb info

    # Snapshot inspection
    cli-anyweb snapshot
    cli-anyweb ls /
    cli-anyweb cat /heading[0]
    cli-anyweb find login
    cli-anyweb get url

    # Actions
    cli-anyweb click @12
    cli-anyweb type @15 "hello"

    # Interactive REPL
    cli-anyweb
"""

import json
import shlex
import sys
from typing import Optional

import click

from agent_harness.core import fs as fs_mod
from agent_harness.core import page as page_mod
from agent_harness.core.session import Session
from agent_harness.utils import agent_browser_backend as backend

_session: Optional[Session] = None
_json_output = False
_repl_mode = False
_availability_cached: Optional[tuple[bool, str]] = None


def get_session() -> Session:
    global _session
    if _session is None:
        _session = Session()
    return _session


def output(data, message: str = ""):
    if _json_output:
        click.echo(json.dumps(data, indent=2, default=str))
        return
    if message:
        click.echo(message)
    if isinstance(data, dict):
        _print_dict(data)
    elif isinstance(data, list):
        _print_list(data)
    else:
        click.echo(str(data))


def _print_dict(d: dict, indent: int = 0):
    prefix = "  " * indent
    for k, v in d.items():
        if isinstance(v, dict):
            click.echo(f"{prefix}{k}:")
            _print_dict(v, indent + 1)
        elif isinstance(v, list):
            click.echo(f"{prefix}{k}:")
            _print_list(v, indent + 1)
        else:
            click.echo(f"{prefix}{k}: {v}")


def _print_list(items: list, indent: int = 0):
    prefix = "  " * indent
    for i, item in enumerate(items):
        if isinstance(item, dict):
            click.echo(f"{prefix}[{i}]")
            _print_dict(item, indent + 1)
        else:
            click.echo(f"{prefix}- {item}")


def _print_matches(pattern: str, result: dict):
    matches = result.get("matches", [])
    if not matches:
        click.echo(f"No matches for '{pattern}'")
        return
    click.echo(f"Matches for '{pattern}':")
    for match in matches:
        click.echo(f"  {match}")


def _print_ls_result(path: str, result: dict, session: Session):
    entries = result.get("entries", [])
    if not entries:
        click.echo(f"No elements at {path or session.working_dir}")
        return
    click.echo(f"{'NAME':<40} {'ROLE':<20} {'PATH'}")
    click.echo("-" * 80)
    for entry in entries:
        click.echo(
            f"{entry.get('name', ''):<40} "
            f"{entry.get('role', ''):<20} "
            f"{entry.get('path', '')}"
        )


def _snapshot_text_message(result: dict) -> str:
    snapshot = str(result.get("snapshot") or "").rstrip()
    return snapshot or "(empty snapshot)"


def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RuntimeError as e:
            if _json_output:
                click.echo(json.dumps({"error": str(e), "type": "runtime_error"}))
            else:
                click.echo(f"Error: {e}", err=True)
            if not _repl_mode:
                sys.exit(1)
        except (ValueError, IndexError) as e:
            if _json_output:
                click.echo(json.dumps({"error": str(e), "type": type(e).__name__}))
            else:
                click.echo(f"Error: {e}", err=True)
            if not _repl_mode:
                sys.exit(1)

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


@click.group(invoke_without_command=True)
@click.option("--json", "use_json", is_flag=True, help="Output as JSON")
@click.option("--daemon", "use_daemon", is_flag=True, help="Use persistent daemon mode")
@click.pass_context
def cli(ctx, use_json, use_daemon):
    """cli-anyweb - browser automation harness via agent-browser."""
    global _json_output, _session, _availability_cached
    _json_output = use_json

    if "--help" not in sys.argv and "--version" not in sys.argv:
        if _availability_cached is None:
            _availability_cached = backend.is_available()
        available, msg = _availability_cached
        if not available:
            if _json_output:
                click.echo(json.dumps({"error": msg, "type": "dependency_error"}))
            else:
                click.echo(f"Error: {msg}", err=True)
                click.echo(
                    "\nInstall agent-browser:\n"
                    "  npm install -g agent-browser\n"
                    "  agent-browser install"
                )
            sys.exit(1)

    _session = get_session()
    if use_daemon:
        try:
            backend.start_daemon()
            _session.enable_daemon()
            if not _json_output:
                click.echo("Daemon mode: persistent MCP connection active")
        except RuntimeError as e:
            if _json_output:
                click.echo(json.dumps({"error": str(e), "type": "daemon_error"}))
            else:
                click.echo(f"Daemon start failed: {e}", err=True)
                click.echo("Falling back to per-command mode", err=True)

    if ctx.invoked_subcommand is None:
        ctx.invoke(repl)


@cli.command("open")
@click.argument("url")
@handle_error
def open_command(url):
    """Open a URL in the browser."""
    sess = get_session()
    result = page_mod.open_page(sess, url)
    output(result, f"Opened: {url}")


@cli.command("reload")
@handle_error
def reload_command():
    """Reload the current page."""
    sess = get_session()
    result = page_mod.reload_page(sess)
    output(result, "Page reloaded")


@cli.command("back")
@handle_error
def back_command():
    """Navigate back in history."""
    sess = get_session()
    result = page_mod.go_back(sess)
    output(result, result.get("error", "Navigated back"))


@cli.command("forward")
@handle_error
def forward_command():
    """Navigate forward in history."""
    sess = get_session()
    result = page_mod.go_forward(sess)
    output(result, result.get("error", "Navigated forward"))


@cli.command("info")
@handle_error
def info_command():
    """Show current page information."""
    output(page_mod.get_page_info(get_session()))


@cli.command("snapshot")
@handle_error
def snapshot_command():
    """Print the current accessibility snapshot."""
    sess = get_session()
    result = backend.snapshot(use_daemon=sess.daemon_mode)
    if _json_output:
        output(result)
    else:
        click.echo(_snapshot_text_message(result))


@cli.command("ls")
@click.argument("path", default="", required=False)
@handle_error
def ls_command(path):
    """List elements at a path in the accessibility tree."""
    sess = get_session()
    result = fs_mod.list_elements(sess, path)
    if _json_output:
        output(result)
    else:
        _print_ls_result(path, result, sess)


@cli.command("cd")
@click.argument("path")
@handle_error
def cd_command(path):
    """Change directory in the accessibility tree."""
    sess = get_session()
    result = fs_mod.change_directory(sess, path)
    if "error" in result:
        output(result, result["error"])
    else:
        output(result, f"Changed to: {sess.working_dir}")


@cli.command("cat")
@click.argument("path", default="", required=False)
@handle_error
def cat_command(path):
    """Read element content from the accessibility tree."""
    output(fs_mod.read_element(get_session(), path))


@cli.command("grep")
@click.argument("pattern")
@click.argument("path", default="", required=False)
@handle_error
def grep_command(pattern, path):
    """Search for pattern in the accessibility tree."""
    sess = get_session()
    result = fs_mod.grep_elements(sess, pattern, path)
    if _json_output:
        output(result)
    else:
        _print_matches(pattern, result)


@cli.command("pwd")
@handle_error
def pwd_command():
    """Print current working directory in accessibility tree."""
    click.echo(get_session().working_dir)


@cli.command("click")
@click.argument("target")
@handle_error
def click_command(target):
    """Click a path or @ref."""
    sess = get_session()
    result = backend.click(target, use_daemon=sess.daemon_mode)
    output(result, f"Clicked: {target}")


@cli.command("type")
@click.argument("target")
@click.argument("text")
@handle_error
def type_command(target, text):
    """Type text into a path or @ref."""
    sess = get_session()
    result = backend.type_text(target, text, use_daemon=sess.daemon_mode)
    output(result, f"Typed into: {target}")


@cli.command("get")
@click.argument("field")
@handle_error
def get_command(field):
    """Get a simple browser value such as the current URL."""
    sess = get_session()
    result = backend.get_value(field, use_daemon=sess.daemon_mode)
    if _json_output:
        output(result)
    else:
        click.echo(result.get("value", ""))


@cli.command("find")
@click.argument("pattern")
@handle_error
def find_command(pattern):
    """Find matching nodes in the current snapshot."""
    sess = get_session()
    result = backend.find(pattern, use_daemon=sess.daemon_mode)
    if _json_output:
        output(result)
    else:
        _print_matches(pattern, result)


@cli.command("status")
@handle_error
def status_command():
    """Show current session status."""
    output(get_session().status())


@cli.command("daemon-start")
@handle_error
def daemon_start_command():
    """Start persistent daemon mode."""
    try:
        backend.start_daemon()
        get_session().enable_daemon()
        output({"daemon": "started"}, "Daemon mode started")
    except RuntimeError as e:
        output({"error": str(e)}, str(e))


@cli.command("daemon-stop")
@handle_error
def daemon_stop_command():
    """Stop persistent daemon mode."""
    backend.stop_daemon()
    get_session().disable_daemon()
    output({"daemon": "stopped"}, "Daemon mode stopped")


@cli.command()
@handle_error
def repl():
    """Start interactive REPL session."""
    from agent_harness.utils.repl_skin import ReplSkin

    global _repl_mode
    _repl_mode = True

    skin = ReplSkin("cli-anyweb", version="1.0.0")
    skin.print_banner()
    pt_session = skin.create_prompt_session()

    repl_commands = {
        "open": "<url>",
        "reload": "Reload current page",
        "back": "Go back in history",
        "forward": "Go forward in history",
        "info": "Show current page info",
        "snapshot": "Show current accessibility snapshot",
        "ls": "[path]",
        "cd": "<path>",
        "cat": "[path]",
        "grep": "<pattern> [path]",
        "pwd": "Show current snapshot path",
        "click": "<path-or-@ref>",
        "type": "<path-or-@ref> <text>",
        "get": "url",
        "find": "<text>",
        "status": "Show session state",
        "daemon-start": "Enable daemon mode flag",
        "daemon-stop": "Disable daemon mode flag",
        "help": "Show this help",
        "quit": "Exit REPL",
    }

    while True:
        try:
            sess = get_session()
            context = sess.working_dir if sess.working_dir != "/" else "/"
            if sess.current_url:
                url_display = sess.current_url[:40] + "..." if len(sess.current_url) > 40 else sess.current_url
                context = f"{url_display} {context}"

            line = skin.get_input(pt_session, context=context)
            if not line:
                continue
            if line.lower() in ("quit", "exit", "q"):
                skin.print_goodbye()
                break
            if line.lower() == "help":
                skin.help(repl_commands)
                continue

            try:
                args = shlex.split(line)
            except ValueError:
                args = line.split()
            try:
                cli.main(args, standalone_mode=False)
            except SystemExit:
                pass
            except click.exceptions.UsageError as e:
                skin.warning(f"Usage error: {e}")
            except Exception as e:
                skin.error(f"{e}")
        except (EOFError, KeyboardInterrupt):
            skin.print_goodbye()
            break

    _repl_mode = False


def main():
    cli()


if __name__ == "__main__":
    main()
