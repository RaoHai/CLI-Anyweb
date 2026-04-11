"""agent-browser CLI adapter for filesystem-style web automation.

This module wraps Vercel Labs' `agent-browser` CLI and preserves the backend
surface used by the harness.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


AGENT_BROWSER_CMD = "agent-browser"
_daemon_enabled = False

_SUBPROCESS_TIMEOUT = 90


def _kill_process_tree(pid: int) -> None:
    """Kill a process and all its descendants, non-blocking (fire-and-forget).

    On Windows, proc.kill() + proc.wait() hangs because npm/.cmd wrappers
    spawn Node/Chromium child processes that don't die automatically.
    Using Popen (no wait) for taskkill avoids that secondary hang.
    """
    if sys.platform == "win32":
        subprocess.Popen(
            ["taskkill", "/F", "/T", "/PID", str(pid)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        try:
            import signal
            os.killpg(os.getpgid(pid), signal.SIGKILL)
        except Exception:
            try:
                os.kill(pid, signal.SIGKILL)
            except Exception:
                pass


@dataclass
class SnapshotNode:
    role: str
    name: str = ""
    ref: str = ""
    line: str = ""
    meta: dict[str, Any] = field(default_factory=dict)
    children: list["SnapshotNode"] = field(default_factory=list)
    path: str = ""


def _run_agent_browser(*args: str, expect_json: bool = True) -> dict[str, Any]:
    executable = _find_agent_browser()
    command = [executable, *_default_agent_browser_flags(), *_extra_agent_browser_flags()]
    if expect_json:
        command.append("--json")
    command.extend(args)

    try:
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "agent-browser not found. Install it with `npm install -g agent-browser` "
            "and run `agent-browser install` once."
        ) from exc

    # Use a daemon thread + Event for timeout so that Event.wait() reliably
    # returns on Windows (unlike proc.communicate(timeout=N) whose cleanup
    # path calls proc.wait() which hangs when child processes inherit pipes).
    _result: list[tuple[str, str]] = []
    _done = threading.Event()

    def _reader() -> None:
        try:
            out, err = proc.communicate()
            _result.append((out or "", err or ""))
        except Exception:
            _result.append(("", ""))
        finally:
            _done.set()

    t = threading.Thread(target=_reader, daemon=True)
    t.start()

    if not _done.wait(timeout=_SUBPROCESS_TIMEOUT):
        _kill_process_tree(proc.pid)
        raise RuntimeError(f"agent-browser command timed out: {' '.join(command)}")

    stdout_raw, stderr_raw = _result[0] if _result else ("", "")
    stdout = stdout_raw.strip()
    stderr = stderr_raw.strip()

    if proc.returncode != 0:
        message = stderr or stdout or f"agent-browser exited with code {proc.returncode}"
        raise RuntimeError(message)

    if not expect_json:
        return {"output": stdout}

    if not stdout:
        return {"success": True}

    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return {"success": True, "data": {"raw": stdout}}


def _extract_data(payload: dict[str, Any]) -> dict[str, Any]:
    data = payload.get("data")
    return data if isinstance(data, dict) else payload


def _get_current_url() -> str:
    payload = _run_agent_browser("get", "url")
    data = _extract_data(payload)
    url = data.get("url") or data.get("value") or data.get("text") or data.get("raw")
    return url or ""


def _role_segment(role: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", role.lower()).strip("-")
    return cleaned or "node"


def _parse_snapshot_line(line: str) -> tuple[int, SnapshotNode] | None:
    if not line.strip().startswith("- "):
        return None

    indent = len(line) - len(line.lstrip(" "))
    content = line.strip()[2:]
    ref_match = re.search(r"\[ref=([^\]]+)\]", content)
    ref = ref_match.group(1) if ref_match else ""

    name_match = re.search(r'"([^"]*)"', content)
    name = name_match.group(1) if name_match else ""

    role_part = content
    if name_match:
        role_part = role_part[:name_match.start()]
    role_part = re.sub(r"\[[^\]]+\]", "", role_part).strip()
    role = role_part or "node"

    meta: dict[str, Any] = {}
    for key, value in re.findall(r"\[([a-zA-Z0-9_-]+)=([^\]]+)\]", content):
        meta[key] = value

    return indent, SnapshotNode(role=role, name=name, ref=ref, line=line.strip(), meta=meta)


def _build_snapshot_tree(snapshot_text: str, refs: dict[str, Any]) -> SnapshotNode:
    root = SnapshotNode(role="root", path="/")
    stack: list[tuple[int, SnapshotNode]] = [(-1, root)]

    for raw_line in snapshot_text.splitlines():
        parsed = _parse_snapshot_line(raw_line)
        if not parsed:
            continue
        indent, node = parsed
        if node.ref and node.ref in refs and isinstance(refs[node.ref], dict):
            node.meta.update(refs[node.ref])
            if not node.name:
                node.name = str(refs[node.ref].get("name") or "")
            if node.role == "node" and refs[node.ref].get("role"):
                node.role = str(refs[node.ref]["role"])

        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        parent.children.append(node)
        stack.append((indent, node))

    _assign_paths(root)
    return root


def _assign_paths(node: SnapshotNode) -> None:
    counters: dict[str, int] = {}
    for child in node.children:
        segment = _role_segment(child.role)
        index = counters.get(segment, 0)
        counters[segment] = index + 1
        child.path = f"/{segment}[{index}]" if node.path == "/" else f"{node.path}/{segment}[{index}]"
        _assign_paths(child)


def _flatten_tree(node: SnapshotNode) -> dict[str, SnapshotNode]:
    path_map = {node.path or "/": node}
    for child in node.children:
        path_map[child.path] = child
        path_map.update(_flatten_tree(child))
    return path_map


def _snapshot_state() -> tuple[SnapshotNode, dict[str, SnapshotNode]]:
    payload = _run_agent_browser("snapshot")
    data = _extract_data(payload)
    snapshot_text = str(data.get("snapshot") or data.get("raw") or "")
    refs = data.get("refs") if isinstance(data.get("refs"), dict) else {}
    tree = _build_snapshot_tree(snapshot_text, refs)
    return tree, _flatten_tree(tree)


def _node_to_entry(node: SnapshotNode) -> dict[str, Any]:
    return {
        "name": node.name,
        "role": node.role,
        "path": node.path,
        "ref": node.ref,
    }


def _resolve_selector(path_or_selector: str) -> tuple[str, str]:
    if path_or_selector.startswith("@"):
        return path_or_selector, path_or_selector
    if not path_or_selector.startswith("/"):
        return path_or_selector, path_or_selector

    _, path_map = _snapshot_state()
    node = path_map.get(path_or_selector)
    if node is None:
        raise RuntimeError(f"No element at path: {path_or_selector}")
    if not node.ref:
        raise RuntimeError(f"Element at path has no actionable ref: {path_or_selector}")
    return f"@{node.ref}", node.path


def _path_or_error(path: str) -> SnapshotNode:
    _, path_map = _snapshot_state()
    node = path_map.get(path)
    if node is None:
        raise RuntimeError(f"No element at path: {path}")
    return node


def _searchable_text(node: SnapshotNode) -> str:
    parts = [node.role, node.name, node.line]
    for value in node.meta.values():
        if isinstance(value, str):
            parts.append(value)
    return " ".join(parts).lower()


def is_available() -> tuple[bool, str]:
    executable = _find_agent_browser()
    if executable is None:
        return (
            False,
            "agent-browser not found. Install it with `npm install -g agent-browser` "
            "then run `agent-browser install`."
        )

    try:
        result = subprocess.run(
            [executable, "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except Exception as exc:
        return False, f"agent-browser check failed: {exc}"

    if result.returncode != 0:
        return False, (result.stderr or result.stdout or "agent-browser version check failed").strip()

    version = (result.stdout or result.stderr or "unknown").strip()
    return True, f"agent-browser {version} is available"


def _find_agent_browser() -> str | None:
    return (
        shutil.which("agent-browser.cmd")
        or shutil.which("agent-browser")
        or shutil.which("agent-browser.ps1")
    )


def _default_agent_browser_flags() -> list[str]:
    profile = (
        Path.cwd() / ".agent-browser-profile"
        if not (profile_env := _env_path("AGENT_BROWSER_PROFILE"))
        else profile_env
    )
    Path(profile).mkdir(parents=True, exist_ok=True)
    return ["--profile", str(profile)]


def _extra_agent_browser_flags() -> list[str]:
    raw = (os.environ.get("CLI_ANYWEB_AGENT_BROWSER_FLAGS") or "").strip()
    if not raw:
        return []
    return shlex.split(raw)


def _env_path(name: str) -> Path | None:
    value = (os.environ.get(name) or "").strip()
    return Path(value) if value else None


def daemon_started() -> bool:
    return _daemon_enabled


def ls(path: str = "/", use_daemon: bool = False) -> dict[str, Any]:
    node = _path_or_error(path)
    entries = [_node_to_entry(child) for child in node.children]
    return {"path": path, "entries": entries}


def cd(path: str, use_daemon: bool = False) -> dict[str, Any]:
    node = _path_or_error(path)
    return {"path": node.path or path, "element": _node_to_entry(node)}


def cat(path: str, use_daemon: bool = False) -> dict[str, Any]:
    node = _path_or_error(path)
    return {
        "name": node.name,
        "role": node.role,
        "text": node.name,
        "path": node.path,
        "ref": node.ref,
        "line": node.line,
        "attributes": node.meta,
        "children": [_node_to_entry(child) for child in node.children],
    }


def grep(pattern: str, use_daemon: bool = False) -> dict[str, Any]:
    _, path_map = _snapshot_state()
    needle = pattern.lower()
    matches = [
        path for path, node in path_map.items()
        if path != "/" and needle in _searchable_text(node)
    ]
    return {"matches": matches}


def snapshot(use_daemon: bool = False) -> dict[str, Any]:
    payload = _run_agent_browser("snapshot")
    data = _extract_data(payload)
    return {
        "snapshot": data.get("snapshot") or data.get("raw") or "",
        "refs": data.get("refs") if isinstance(data.get("refs"), dict) else {},
    }


def get_value(field: str, use_daemon: bool = False) -> dict[str, Any]:
    normalized = field.strip().lower()
    if normalized == "url":
        return {"field": "url", "value": _get_current_url()}
    if normalized == "html":
        payload = _run_agent_browser("get", "html", "html")
        data = _extract_data(payload)
        html = data.get("html") or data.get("text") or data.get("value") or data.get("raw")
        return {"field": "html", "value": html or ""}
    raise ValueError(f"Unsupported field: {field}")


def find(pattern: str, use_daemon: bool = False) -> dict[str, Any]:
    result = grep(pattern, use_daemon=use_daemon)
    matches = result.get("matches", [])
    return {
        "query": pattern,
        "matches": matches,
        "count": len(matches),
    }


def eval_js(script: str, use_daemon: bool = False) -> dict[str, Any]:
    payload = _run_agent_browser("eval", script, expect_json=False)
    return {"output": payload.get("output", "")}


def wait_ms(ms: int, use_daemon: bool = False) -> dict[str, Any]:
    payload = _run_agent_browser("wait", str(ms), expect_json=False)
    return {"output": payload.get("output", "")}


def click(path: str, use_daemon: bool = False) -> dict[str, Any]:
    selector, resolved_path = _resolve_selector(path)
    _run_agent_browser("click", selector)
    return {"action": "click", "path": resolved_path, "selector": selector, "status": "success"}


def open_url(url: str, use_daemon: bool = False) -> dict[str, Any]:
    _run_agent_browser("open", url)
    current_url = _get_current_url() or url
    return {"url": current_url, "status": "loaded"}


def reload(use_daemon: bool = False) -> dict[str, Any]:
    _run_agent_browser("reload")
    return {"status": "reloaded", "url": _get_current_url()}


def back(use_daemon: bool = False) -> dict[str, Any]:
    _run_agent_browser("back")
    return {"status": "navigated", "url": _get_current_url()}


def forward(use_daemon: bool = False) -> dict[str, Any]:
    _run_agent_browser("forward")
    return {"status": "navigated", "url": _get_current_url()}


def type_text(path: str, text: str, use_daemon: bool = False) -> dict[str, Any]:
    selector, resolved_path = _resolve_selector(path)
    _run_agent_browser("type", selector, text)
    return {"action": "type", "path": resolved_path, "selector": selector, "text": text, "status": "success"}


def start_daemon() -> bool:
    global _daemon_enabled
    _daemon_enabled = True
    return True


def stop_daemon() -> None:
    global _daemon_enabled
    _daemon_enabled = False
