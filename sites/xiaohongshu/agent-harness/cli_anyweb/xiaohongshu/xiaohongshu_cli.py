#!/usr/bin/env python3
"""Standalone wrapper for cli-anyweb-xiaohongshu."""

import os
import re
import sys
import json
import urllib.request
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
                # Extract note ID and xsec_token from cover ref href (via snapshot refs dict)
                note_id = ""
                xsec_token = ""
                cover_ref_m = re.search(r"\[ref=([^\]]+)\]", line)
                if cover_ref_m and refs:
                    ref_data = refs.get(cover_ref_m.group(1)) or {}
                    href = ref_data.get("href") or ""
                    m = re.search(r"/(?:explore|search_result)/([a-zA-Z0-9]+)", href)
                    if m:
                        note_id = m.group(1)
                    xt = re.search(r"[?&]xsec_token=([^&]+)", href)
                    if xt:
                        xsec_token = xt.group(1)
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
                        results.append({"title": title, "author": author, "likes": likes, "note_id": note_id, "xsec_token": xsec_token})
                        i = j
                        _advanced = True
                        break
                else:
                    if title:
                        results.append({"title": title, "author": author, "likes": likes, "note_id": note_id, "xsec_token": xsec_token})
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
        xt = card.get("xsec_token") or ""
        click.echo(
            _cjk_ljust(_cjk_trunc(nid, W_ID), W_ID) + "  "
            + _cjk_ljust(_cjk_trunc(card["title"], W_TITLE), W_TITLE) + "  "
            + _cjk_ljust(_cjk_trunc(card["author"], W_AUTHOR), W_AUTHOR) + "  "
            + card["likes"].rjust(W_LIKES)
            + (f"  xsec={xt}" if xt else "")
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
        "var p=aa[i].pathname;"
        "var id=null;"
        "if(p.indexOf('/search_result/')===0)id=p.slice(15);"
        "else if(p.indexOf('/explore/')===0)id=p.slice(9);"
        "if(id&&r.indexOf(id)<0)r.push(id);"
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


def _extract_note_xsec_tokens_from_js() -> dict[str, str]:
    """Return {note_id: xsec_token} for search-result note links on the current page.

    Xiaohongshu search result covers link to /search_result/<noteId>?xsec_token=...
    """
    script = (
        "var r={};"
        "var aa=document.links;"
        "for(var i=0;i<aa.length;i++){"
        "var p=aa[i].pathname;"
        "var q=aa[i].search;"
        "var id=null;"
        "if(p.indexOf('/search_result/')===0)id=p.slice(15);"
        "else if(p.indexOf('/explore/')===0)id=p.slice(9);"
        "if(id){"
        "var m=q.match(/[?&]xsec_token=([^&]+)/);"
        "if(m&&!r[id])r[id]=decodeURIComponent(m[1]);"
        "}"
        "}"
        "JSON.stringify(r)"
    )
    try:
        raw = _get_backend().eval_js(script).get("output", "").strip()
        if not raw:
            return {}
        if raw.startswith('"') and raw.endswith('"'):
            raw = json.loads(raw)
        data = json.loads(raw)
        if isinstance(data, str):
            data = json.loads(data)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


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
    video_urls = _all(r"\"masterUrl\":\"(http[^\"]+\.mp4[^\"]*)\"")
    if not video_urls:
        # fallback: older notes may use a plain "url" field
        video_urls = _all(r"\"url\":\"(http[^\"]+\.mp4[^\"]*)\"")

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
        # eval_js on Windows may double-serialise: unwrap if result is a string
        if isinstance(data, str):
            data = json.loads(data)
    except json.JSONDecodeError:
        return {}
    if not isinstance(data, dict):
        return {}
    first = next(iter(data.values()), {})
    note = first.get("note") if isinstance(first, dict) else {}
    interact = note.get("interactInfo", {}) if isinstance(note, dict) else {}
    images = note.get("imageList", []) if isinstance(note, dict) else []
    image_default = [img.get("urlDefault", "") for img in images if isinstance(img, dict)]
    image_pre = [img.get("urlPre", "") for img in images if isinstance(img, dict)]
    # Extract video masterUrls from note.video.media.stream.h264[]
    video = note.get("video", {}) if isinstance(note, dict) else {}
    video_urls = []
    if isinstance(video, dict):
        media = video.get("media", {})
        if isinstance(media, dict):
            stream = media.get("stream", {})
            if isinstance(stream, dict):
                h264 = stream.get("h264", [])
                video_urls = [
                    s.get("masterUrl", "")
                    for s in h264
                    if isinstance(s, dict) and s.get("masterUrl")
                ]
    return {
        "title": note.get("title", ""),
        "desc": note.get("desc", ""),
        "commentCount": interact.get("commentCount", ""),
        "imageDefaultUrls": image_default,
        "imagePreviewUrls": image_pre,
        "videoUrls": video_urls,
    }


def _build_note_url(note_url: str | None, note_id: str | None, xsec_token: str | None) -> str:
    if note_url:
        return note_url
    if xsec_token:
        return f"https://www.xiaohongshu.com/explore/{note_id}?xsec_token={xsec_token}"
    return f"https://www.xiaohongshu.com/explore/{note_id}"


# ---------------------------------------------------------------------------
# Shared helpers for note-* commands
# ---------------------------------------------------------------------------

def _open_note_if_needed(
    note_url: str | None, note_id: str | None, xsec_token: str | None
) -> None:
    """Navigate to the note only when a URL/ID is supplied; otherwise keep the current page."""
    if note_url or note_id:
        _open(_build_note_url(note_url, note_id, xsec_token))
        _get_backend().wait_ms(1500)


def _get_note_detail() -> dict:
    """Return parsed noteDetailMap from the current page, raising ClickException on failure."""
    html = _get_html()
    if html:
        data = _extract_note_detail(html)
        if data:
            return data
    try:
        data = _extract_note_detail_from_state()
        if data:
            return data
    except Exception:
        pass
    raise click.ClickException("No noteDetailMap found in HTML or state")


_DOWNLOAD_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/146.0.0.0 Safari/537.36"
)


def _download_file(url: str, dest: Path, referer: str = "https://www.xiaohongshu.com") -> None:
    """Download *url* to *dest* with browser-like headers to avoid CDN 403s."""
    req = urllib.request.Request(url, headers={
        "User-Agent": _DOWNLOAD_UA,
        "Referer": referer,
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        dest.write_bytes(resp.read())


def _safe_filename(title: str, max_len: int = 40) -> str:
    """Sanitise a note title for use as a filename fragment."""
    safe = re.sub(r'[^\w\u4e00-\u9fff]+', '_', title).strip('_')
    return safe[:max_len] or "note"


def _parse_comments_from_snapshot(snap: str, limit: int = 20) -> list[dict]:
    """Extract visible comments from an accessibility-tree snapshot.

    Heuristic: scan listitem blocks; each comment item has an author link
    followed by a non-trivial StaticText body.  Tries to start from the
    comment section heading ("评论") to skip the note header area.
    """
    lines = snap.splitlines()
    n = len(lines)
    nav = frozenset({
        "发现", "直播", "发布", "通知", "我", "登录",
        "创作中心", "业务合作", "更多", "搜索小红书",
    })
    results: list[dict] = []

    # Seek the comment-section heading so we skip the note title/author block.
    start = 0
    for idx, line in enumerate(lines):
        if "评论" in line and ("StaticText" in line or "heading" in line.lower()):
            start = idx
            break

    i = start
    while i < n and len(results) < limit:
        line = lines[i]
        if "listitem" not in line:
            i += 1
            continue

        ind = len(line) - len(line.lstrip())
        author = ""
        content = ""
        j = i + 1
        while j < n:
            jl = lines[j]
            ji = len(jl) - len(jl.lstrip())
            if ji <= ind:
                break

            if not author and 'link "' in jl:
                m = re.search(r'link "([^"]+)"', jl)
                if m and m.group(1) not in nav:
                    author = m.group(1)

            # Collect content only after we have an author (avoids the note title).
            if author and not content and 'StaticText "' in jl:
                m = re.search(r'StaticText "([^"]+)"', jl)
                if m:
                    text = m.group(1)
                    if (text != author
                            and len(text) > 1
                            and text not in nav
                            and not re.fullmatch(r'[\d万千百]+', text)):
                        content = text
            j += 1

        if author and content:
            results.append({"nickname": author, "content": content})
        i += 1

    return results


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
    # Fill in xsec_tokens from /explore/ links on the page
    xsec_map = _extract_note_xsec_tokens_from_js()
    if xsec_map:
        for card in cards:
            if not card.get("xsec_token") and card.get("note_id"):
                card["xsec_token"] = xsec_map.get(card["note_id"], "")
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


# ---------------------------------------------------------------------------
# Note detail commands
# ---------------------------------------------------------------------------

_NOTE_URL_OPTIONS = [
    click.option("--url", "note_url", required=False, help="Full note URL"),
    click.option("--note-id", "note_id", required=False, help="Note ID"),
    click.option("--xsec-token", "xsec_token", required=False, help="xsec token"),
]


def _add_note_url_options(cmd):
    for opt in reversed(_NOTE_URL_OPTIONS):
        cmd = opt(cmd)
    return cmd


@site_cli.command("note-content")
@click.option("--url", "note_url", required=False, help="Full note URL")
@click.option("--note-id", "note_id", required=False, help="Note ID")
@click.option("--xsec-token", "xsec_token", required=False, help="xsec token")
@click.option("--json", "as_json", is_flag=True, default=False, help="Output raw JSON")
def note_content(note_url: str | None, note_id: str | None, xsec_token: str | None, as_json: bool) -> None:
    """Display note title, description, comment count, and media URLs."""
    _open_note_if_needed(note_url, note_id, xsec_token)
    data = _get_note_detail()
    if as_json:
        click.echo(json.dumps(data, ensure_ascii=False, indent=2))
        return
    click.echo(f"标题: {data.get('title', '')}")
    desc = data.get("desc", "")
    click.echo(f"正文: {desc[:300]}{'…' if len(desc) > 300 else ''}")
    click.echo(f"评论数: {data.get('commentCount', '-')}")
    imgs = data.get("imageDefaultUrls", [])
    vids = data.get("videoUrls", [])
    click.echo(f"图片: {len(imgs)} 张")
    for i, u in enumerate(imgs, 1):
        click.echo(f"  [{i}] {u}")
    click.echo(f"视频: {len(vids)} 个")
    for i, u in enumerate(vids, 1):
        click.echo(f"  [{i}] {u}")


@site_cli.command("note-comments")
@click.option("--url", "note_url", required=False, help="Full note URL")
@click.option("--note-id", "note_id", required=False, help="Note ID")
@click.option("--xsec-token", "xsec_token", required=False, help="xsec token")
@click.option("--count", default=20, show_default=True, help="Max number of comments to show")
@click.option("--json", "as_json", is_flag=True, default=False, help="Output raw JSON")
def note_comments(
    note_url: str | None, note_id: str | None, xsec_token: str | None,
    count: int, as_json: bool,
) -> None:
    """List visible comments from a note detail page."""
    _open_note_if_needed(note_url, note_id, xsec_token)
    _get_backend().wait_ms(2000)  # let comment section render
    snap_data = _get_backend().snapshot()
    snap = snap_data.get("snapshot", "")
    comments = _parse_comments_from_snapshot(snap, limit=count)
    if as_json:
        click.echo(json.dumps(comments, ensure_ascii=False, indent=2))
        return
    if not comments:
        click.echo("(no comments found — page may require login or comments haven't loaded)")
        return
    W_NO, W_NICK, W_CONTENT = 4, 14, 44
    header = (
        _cjk_ljust("No.", W_NO) + "  "
        + _cjk_ljust("昵称", W_NICK) + "  "
        + "内容"
    )
    click.echo(header)
    click.echo("─" * (W_NO + W_NICK + W_CONTENT + 4))
    for i, c in enumerate(comments, 1):
        click.echo(
            _cjk_ljust(str(i), W_NO) + "  "
            + _cjk_ljust(_cjk_trunc(c["nickname"], W_NICK), W_NICK) + "  "
            + _cjk_trunc(c["content"], W_CONTENT)
        )


@site_cli.command("note-download-images")
@click.option("--url", "note_url", required=False, help="Full note URL")
@click.option("--note-id", "note_id", required=False, help="Note ID")
@click.option("--xsec-token", "xsec_token", required=False, help="xsec token")
@click.option("--output-dir", "-o", default=".", show_default=True, help="Directory to save images")
@click.option("--preview", is_flag=True, default=False, help="Download preview size instead of full resolution")
def note_download_images(
    note_url: str | None, note_id: str | None, xsec_token: str | None,
    output_dir: str, preview: bool,
) -> None:
    """Download all images from a note to a local directory."""
    _open_note_if_needed(note_url, note_id, xsec_token)
    data = _get_note_detail()
    key = "imagePreviewUrls" if preview else "imageDefaultUrls"
    urls = data.get(key, [])
    if not urls:
        raise click.ClickException("No images found in note")
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_title = _safe_filename(data.get("title", ""))
    failed = 0
    for i, url in enumerate(urls, 1):
        path_part = url.split("?")[0].rsplit("/", 1)[-1]
        ext = path_part.rsplit(".", 1)[-1] if "." in path_part else "jpg"
        dest = out_dir / f"{safe_title}_{i:02d}.{ext}"
        try:
            _download_file(url, dest)
            click.echo(f"[{i}/{len(urls)}] {dest.name}")
        except Exception as exc:
            click.echo(f"[{i}/{len(urls)}] FAILED: {exc}", err=True)
            failed += 1
    if failed:
        click.echo(f"{failed}/{len(urls)} downloads failed", err=True)


@site_cli.command("note-download-video")
@click.option("--url", "note_url", required=False, help="Full note URL")
@click.option("--note-id", "note_id", required=False, help="Note ID")
@click.option("--xsec-token", "xsec_token", required=False, help="xsec token")
@click.option("--output-dir", "-o", default=".", show_default=True, help="Directory to save the video")
@click.option("--index", default=0, show_default=True, help="Which video to download (0 = first)")
def note_download_video(
    note_url: str | None, note_id: str | None, xsec_token: str | None,
    output_dir: str, index: int,
) -> None:
    """Download the video from a note to a local directory."""
    _open_note_if_needed(note_url, note_id, xsec_token)
    data = _get_note_detail()
    urls = data.get("videoUrls", [])
    if not urls:
        raise click.ClickException("No video found in note (image-only post?)")
    if index >= len(urls):
        raise click.ClickException(f"--index {index} out of range; note has {len(urls)} video(s)")
    url = urls[index]
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_title = _safe_filename(data.get("title", ""))
    dest = out_dir / f"{safe_title}.mp4"
    click.echo(f"Downloading video → {dest}")
    _download_file(url, dest)
    click.echo(f"Saved: {dest} ({dest.stat().st_size // 1024} KB)")


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
