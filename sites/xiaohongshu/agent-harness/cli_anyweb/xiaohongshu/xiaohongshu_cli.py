#!/usr/bin/env python3
"""Standalone wrapper for cli-anyweb-xiaohongshu."""

import os
import re
import sys
import json
from pathlib import Path
from urllib.parse import quote

import click


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


def _get_backend():
    from cli_anyweb.utils import agent_browser_backend as imported_backend

    return imported_backend


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

    _apply_site_profile_dir()
    os.environ.setdefault("CLI_ANYWEB_SITE_ROOT", str(site_root))


def _apply_site_profile_dir() -> None:
    profile_dir = (os.environ.get("CLI_ANYWEB_SITE_PROFILE_DIR") or "").strip()
    if not profile_dir or os.environ.get("AGENT_BROWSER_PROFILE"):
        return
    os.environ["AGENT_BROWSER_PROFILE"] = profile_dir


def _open(url: str) -> None:
    result = _get_backend().open_url(url)
    click.echo(f"Opened: {result.get('url') or url}")


def _click_first(label: str) -> None:
    backend = _get_backend()
    matches = backend.find(label).get("matches", [])
    if not matches:
        raise click.ClickException(f"No match for '{label}' in the current snapshot")
    last_error: str | None = None
    for match in matches:
        try:
            backend.click(match)
            click.echo(f"Clicked: {label} ({match})")
            return
        except RuntimeError as exc:
            last_error = str(exc)
            continue
    raise click.ClickException(last_error or f"No actionable match for '{label}'")


def _find_search_filter_tab_ref(
    label: str, snap_data: dict | None = None
) -> tuple[str | None, str, dict]:
    """Find the search-filter tab ref (全部/图文/视频/用户).

    Returns (ref_or_None, snapshot_text, refs_dict) so callers can reuse the
    snapshot instead of issuing a second snapshot request.

    More reliable than a plain text search because the page may also render
    a user-profile panel with identical tab labels.  Confirms the candidate by
    verifying that at least two sibling filter labels appear within ±8 lines,
    then walks up to the nearest parent clickable line to get the ref.
    """
    if snap_data is None:
        snap_data = _get_backend().snapshot()
    snapshot = snap_data.get("snapshot", "")
    refs = snap_data.get("refs") or {}
    lines = snapshot.splitlines()
    siblings = {"全部", "图文", "视频", "用户"} - {label}
    for idx, line in enumerate(lines):
        if label not in line:
            continue
        window = "\n".join(lines[max(0, idx - 8): idx + 8])
        if sum(1 for s in siblings if s in window) < 2:
            continue
        ref_match = re.search(r"\[ref=([^\]]+)\]", line)
        if ref_match:
            return f"@{ref_match.group(1)}", snapshot, refs
        for offset in range(1, 4):
            if idx - offset < 0:
                break
            prev = lines[idx - offset]
            if "clickable" not in prev:
                continue
            ref_match = re.search(r"\[ref=([^\]]+)\]", prev)
            if ref_match:
                return f"@{ref_match.group(1)}", snapshot, refs
    return None, snapshot, refs


_SEARCH_TAB_LABELS: dict[str, str] = {
    "video": "视频",
    "notes": "图文",
    "users": "用户",
}


def _click_search_tab(label: str) -> None:
    """Click a search filter tab."""
    ref, _snap, _refs = _find_search_filter_tab_ref(label)
    if ref:
        _get_backend().click(ref)
        click.echo(f"Clicked: {label} ({ref})")
    else:
        _click_first(label)


def _cjk_width(s: str) -> int:
    return sum(2 if ord(c) > 0x2E7F else 1 for c in s)


def _cjk_ljust(s: str, width: int) -> str:
    return s + " " * max(0, width - _cjk_width(s))


def _cjk_trunc(s: str, max_width: int) -> str:
    out, w = [], 0
    for c in s:
        cw = 2 if ord(c) > 0x2E7F else 1
        if w + cw > max_width:
            out.append("…")
            break
        out.append(c)
        w += cw
    return "".join(out)


def _parse_search_cards(snap: str, refs: dict | None = None) -> list[dict]:
    """Extract (title, author, likes, note_id) from a flat search-result snapshot.

    Each card is a group of 4 siblings at the same indent level:
      cover  : link [ref=...] (no label) + image child at indent+2
      title  : link "TITLE"  (no image child at indent+2)
      author : link "AUTHOR" (has image child at indent+2; first StaticText = name)
      likes  : generic clickable (numeric StaticText child)

    note_id is extracted from the cover link's href via the refs dict
    (e.g. /explore/<noteId>?xsec_token=...).
    """
    lines = snap.splitlines()
    n = len(lines)
    results: list[dict] = []
    nav = frozenset({"发现", "直播", "发布", "通知", "我", "登录", "创作中心", "业务合作", "更多", "搜索小红书"})
    bad_kw = ("ICP", "许可", "举报", "执照", "经营", "电话", "地址", "算法", "©", "公网", "行吟")

    i = 0
    while i < n:
        line = lines[i]
        # Cover: un-labelled link with ref
        if "link \"" not in line and re.search(r"link\s+\[ref=", line):
            ind = len(line) - len(line.lstrip())
            if (i + 1 < n and "image" in lines[i + 1] and
                    len(lines[i + 1]) - len(lines[i + 1].lstrip()) == ind + 2):
                title = author = likes = ""
                # Extract note ID from cover ref href (via snapshot refs dict)
                note_id = ""
                cover_ref_m = re.search(r"\[ref=([^\]]+)\]", line)
                if cover_ref_m and refs:
                    ref_data = refs.get(cover_ref_m.group(1)) or {}
                    href = ref_data.get("href") or ""
                    m = re.search(r"/(?:explore|search_result)/([a-zA-Z0-9]+)", href)
                    if m:
                        note_id = m.group(1)
                j = i + 2
                _advanced = False
                while j < n:
                    jl = lines[j]
                    ji = len(jl) - len(jl.lstrip())
                    if ji < ind and jl.strip().startswith("-"):
                        break
                    if ji == ind:
                        if "link \"" in jl:
                            lm = re.search(r'link "([^"]+)"', jl)
                            if lm:
                                cand = lm.group(1)
                                skip = cand in nav or any(k in cand for k in bad_kw)
                                nxt_ind = len(lines[j + 1]) - len(lines[j + 1].lstrip()) if j + 1 < n else 0
                                has_img = nxt_ind == ind + 2 and j + 1 < n and "image" in lines[j + 1]
                                if not skip:
                                    if not title and not has_img:
                                        title = cand
                                    elif title and has_img and not author:
                                        for k in range(j + 1, min(j + 6, n)):
                                            if (len(lines[k]) - len(lines[k].lstrip()) == ind + 2
                                                    and "StaticText \"" in lines[k]):
                                                sm = re.search(r'StaticText "([^"]+)"', lines[k])
                                                if sm:
                                                    author = sm.group(1)
                                                    break
                        elif "generic" in jl and "clickable" in jl and title and author and not likes:
                            for k in range(j + 1, min(j + 5, n)):
                                if (len(lines[k]) - len(lines[k].lstrip()) == ind + 2
                                        and "StaticText \"" in lines[k]):
                                    vm = re.search(r'StaticText "([^"]+)"', lines[k])
                                    if vm:
                                        val = vm.group(1)
                                        if re.match(r"^\d[\d.万千百]*$|^赞$", val):
                                            likes = val
                                            break
                    j += 1
                    if title and author and likes:
                        results.append({"title": title, "author": author, "likes": likes, "note_id": note_id})
                        i = j
                        _advanced = True
                        break
                else:
                    if title:
                        results.append({"title": title, "author": author, "likes": likes, "note_id": note_id})
                if not _advanced:
                    i += 1
                continue
        i += 1
    return results


def _print_results_table(cards: list[dict]) -> None:
    if not cards:
        click.echo("(no results)")
        return
    W_ID, W_TITLE, W_AUTHOR, W_LIKES = 24, 28, 14, 6
    header = (
        _cjk_ljust("帖子ID", W_ID) + "  "
        + _cjk_ljust("标题", W_TITLE) + "  "
        + _cjk_ljust("作者", W_AUTHOR) + "  "
        + "点赞".rjust(W_LIKES)
    )
    click.echo(header)
    click.echo("─" * (W_ID + W_TITLE + W_AUTHOR + W_LIKES + 6))
    for card in cards:
        nid = card.get("note_id") or "-"
        click.echo(
            _cjk_ljust(_cjk_trunc(nid, W_ID), W_ID) + "  "
            + _cjk_ljust(_cjk_trunc(card["title"], W_TITLE), W_TITLE) + "  "
            + _cjk_ljust(_cjk_trunc(card["author"], W_AUTHOR), W_AUTHOR) + "  "
            + card["likes"].rjust(W_LIKES)
        )


def _extract_note_ids_from_js() -> list[str]:
    """Extract search-result note IDs from the DOM via eval_js.

    Uses single-quote-only JS to stay safe under Windows list2cmdline wrapping.
    Selects links whose pathname starts with /search_result/ and returns the
    ID segment (the hex note ID, without the query string).
    """
    script = (
        "var r=[];"
        "var aa=document.links;"
        "for(var i=0;i<aa.length&&r.length<60;i++){"
        "var h=aa[i].pathname;"
        "if(h.indexOf('/search_result/')===0){"
        "var id=h.slice(15);"
        "if(id&&r.indexOf(id)<0)r.push(id);"
        "}"
        "}"
        "r.join('|')"
    )
    try:
        raw = _get_backend().eval_js(script).get("output", "").strip()
        if not raw:
            return []
        # agent-browser may wrap the eval result in JSON string quotes
        if raw.startswith('"') and raw.endswith('"'):
            raw = raw[1:-1]
        return [nid for nid in raw.split("|") if nid]
    except Exception:
        return []


def _echo_current_url() -> str:
    url = _get_backend().get_value("url").get("value", "")
    if url:
        click.echo(f"Current URL: {url}")
    return url


def _get_html() -> str:
    return _get_backend().get_value("html").get("value", "")


def _extract_note_detail(html: str) -> dict:
    match = re.search(r"\"noteDetailMap\":\\{(.+?)\\},\"serverRequestInfo\"", html, re.DOTALL)
    chunk = match.group(1) if match else ""
    if not chunk:
        return {}

    def _first(pattern: str) -> str:
        m = re.search(pattern, chunk)
        return m.group(1) if m else ""

    def _all(pattern: str) -> list[str]:
        return [m.group(1) for m in re.finditer(pattern, chunk)]

    title = _first(r"\"title\":\"([^\"]*)\"")
    desc = _first(r"\"desc\":\"([^\"]*)\"")
    comment_count = _first(r"\"commentCount\":\"([^\"]*)\"")
    image_defaults = _all(r"\"urlDefault\":\"([^\"]+)\"")
    image_previews = _all(r"\"urlPre\":\"([^\"]+)\"")
    video_urls = _all(r"\"url\":\"(http[^\"]+\\.mp4[^\"]*)\"")

    def _clean(value: str) -> str:
        return (
            value.replace("\\u002F", "/")
            .replace("\\n", "\n")
            .replace("\\t", "\t")
        )

    return {
        "title": _clean(title),
        "desc": _clean(desc),
        "commentCount": _clean(comment_count),
        "imageDefaultUrls": [_clean(u) for u in image_defaults],
        "imagePreviewUrls": [_clean(u) for u in image_previews],
        "videoUrls": [_clean(u) for u in video_urls],
    }


def _extract_note_detail_from_state() -> dict:
    script = (
        "var s=window.__INITIAL_STATE__||{};"
        "var note=(s.note&&s.note.noteDetailMap)||{};"
        "JSON.stringify(note)"
    )
    raw = _get_backend().eval_js(script).get("output", "").strip()
    if not raw or raw == "{}":
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    first = next(iter(data.values()), {})
    note = first.get("note") if isinstance(first, dict) else {}
    interact = note.get("interactInfo", {}) if isinstance(note, dict) else {}
    images = note.get("imageList", []) if isinstance(note, dict) else []
    image_default = [img.get("urlDefault", "") for img in images if isinstance(img, dict)]
    image_pre = [img.get("urlPre", "") for img in images if isinstance(img, dict)]
    return {
        "title": note.get("title", ""),
        "desc": note.get("desc", ""),
        "commentCount": interact.get("commentCount", ""),
        "imageDefaultUrls": image_default,
        "imagePreviewUrls": image_pre,
        "videoUrls": [],
    }


def _build_note_url(note_url: str | None, note_id: str | None, xsec_token: str | None) -> str:
    if note_url:
        return note_url
    if xsec_token:
        return f"https://www.xiaohongshu.com/explore/{note_id}?xsec_token={xsec_token}"
    return f"https://www.xiaohongshu.com/explore/{note_id}"


@click.group()
def site_cli() -> None:
    """xiaohongshu site-specific commands."""


@site_cli.command("home")
def home() -> None:
    """Open the public home surface."""
    _open("https://www.xiaohongshu.com/explore")


@site_cli.command("search")
@click.option("--query", required=True, help="Search keyword")
@click.option(
    "--type", "result_type",
    type=click.Choice(["all", "video", "notes", "users"], case_sensitive=False),
    default="all",
    show_default=True,
    help="Content-type filter: all (default), video, notes, users",
)
def search(query: str, result_type: str) -> None:
    """Open search and optionally switch to a content-type tab."""
    url = f"https://www.xiaohongshu.com/search_result?keyword={quote(query)}"
    _open(url)
    _get_backend().wait_ms(2500)  # let the SPA card grid render before snapshotting
    if result_type != "all":
        _click_search_tab(_SEARCH_TAB_LABELS[result_type])
        _get_backend().wait_ms(1500)  # let the tab filter apply
    _echo_current_url()
    snap_data = _get_backend().snapshot()
    snap = snap_data.get("snapshot", "")
    refs = snap_data.get("refs") or {}
    cards = _parse_search_cards(snap, refs)
    # Supplement missing note IDs from DOM (snapshot refs don't expose href)
    js_ids = _extract_note_ids_from_js()
    if js_ids:
        for i, card in enumerate(cards):
            if not card.get("note_id") and i < len(js_ids):
                card["note_id"] = js_ids[i]
    _print_results_table(cards)


@site_cli.command("open-note")
@click.option("--url", "note_url", required=False, help="Full note URL")
@click.option("--note-id", "note_id", required=False, help="Note ID")
@click.option("--xsec-token", "xsec_token", required=False, help="xsec token")
@click.option("--extract", is_flag=True, default=False, help="Extract and print structured note data as JSON")
def open_note(note_url: str | None, note_id: str | None, xsec_token: str | None, extract: bool) -> None:
    """Open a note detail page. Add --extract to print title, desc, and media URLs as JSON."""
    if not note_url and not note_id:
        raise click.ClickException("Provide --url or --note-id")
    _open(_build_note_url(note_url, note_id, xsec_token))
    if not extract:
        return
    _get_backend().wait_ms(1500)
    html = _get_html()
    if not html:
        raise click.ClickException("Empty HTML from note detail page")
    data = _extract_note_detail(html)
    if not data:
        try:
            data = _extract_note_detail_from_state()
        except RuntimeError:
            pass
    if not data:
        raise click.ClickException("No noteDetailMap found in HTML or state")
    click.echo(json.dumps(data, ensure_ascii=False, indent=2))


@site_cli.command("login")
def login() -> None:
    """Open home and attempt to click the login entry."""
    _open("https://www.xiaohongshu.com/explore")
    try:
        _click_first("登录")
        _echo_current_url()
    except click.ClickException as exc:
        click.echo(f"Login entry not found: {exc}")


@site_cli.command("publish")
def publish() -> None:
    """Open home and attempt to click publish."""
    _open("https://www.xiaohongshu.com/explore")
    _click_first("发布")
    url = _echo_current_url()
    if url and "creator.xiaohongshu.com" not in url:
        click.echo("Warning: publish did not land on creator.xiaohongshu.com")


@site_cli.command("notifications")
def notifications() -> None:
    """Open home and attempt to click notifications."""
    _open("https://www.xiaohongshu.com/explore")
    _click_first("通知")
    url = _echo_current_url()
    if url and "creator.xiaohongshu.com" in url:
        click.echo("Warning: notifications appears to route to creator flow")


@site_cli.command("profile")
def profile() -> None:
    """Open home and attempt to click the profile entry."""
    _open("https://www.xiaohongshu.com/explore")
    _click_first("我")
    url = _echo_current_url()
    if url and "creator.xiaohongshu.com" in url:
        click.echo("Warning: profile appears to route to creator flow")


def main():
    _ensure_utf8_stdout()
    _load_site_env()
    runtime = _import_runtime_cli()
    cli = click.CommandCollection(sources=[site_cli, runtime])
    cli(prog_name="cli-anyweb-xiaohongshu")


def _ensure_utf8_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        return


if __name__ == "__main__":
    main()
