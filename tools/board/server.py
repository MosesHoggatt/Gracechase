"""Gracechase owner task board.

Serves the LAN only (loopback and private addresses) on 0.0.0.0:8790.
No login. HTML is server-rendered. JSON routes share the form posts.

  GC_BOARD_PORT          default 8790
  GC_BOARD_ROOT          redirect data files (tests)
  GC_BOARD_NO_PING=1     do not run ping-owner.ps1
  GC_BOARD_SYNC_SECONDS  default 20; 0 disables the background sync
"""
from __future__ import annotations

import html
import json
import mimetypes
import os
import re
import sys
import threading
import time
import traceback
import urllib.parse
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import board_core  # noqa: E402

MAX_UPLOAD = 4 * 1024 ** 3
MAX_OVERHEAD = 8 * 1024 * 1024
MAX_FORM = 2 * 1024 * 1024
MAX_FILES = 40
ICON_PATH = os.path.join(board_core.REPO, "social", "tiktok", "gracechase-posts-icon-1024.png")

mimetypes.add_type("video/mp4", ".mp4")
mimetypes.add_type("video/webm", ".webm")
mimetypes.add_type("video/quicktime", ".mov")
mimetypes.add_type("audio/mp4", ".m4a")
mimetypes.add_type("audio/mpeg", ".mp3")
mimetypes.add_type("audio/wav", ".wav")
mimetypes.add_type("image/webp", ".webp")

_NETS = None


def _networks():
    global _NETS
    if _NETS is None:
        import ipaddress

        _NETS = (
            ipaddress.ip_network("127.0.0.0/8"),
            ipaddress.ip_network("10.0.0.0/8"),
            ipaddress.ip_network("172.16.0.0/12"),
            ipaddress.ip_network("192.168.0.0/16"),
        )
    return _NETS


def client_allowed(ip_text: str) -> bool:
    """True for loopback and RFC1918. Ignores forwarded headers; pass the socket address."""
    import ipaddress

    if not ip_text:
        return False
    text = ip_text.strip()
    if text.startswith("[") and "]" in text:
        text = text[1 : text.index("]")]
    if "%" in text:
        text = text.split("%", 1)[0]
    try:
        ip = ipaddress.ip_address(text)
    except ValueError:
        return False
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
        ip = ip.ipv4_mapped
    if ip.version == 6:
        return ip == ipaddress.ip_address("::1")
    return any(ip in network for network in _networks())


def png_size(path: str):
    try:
        with open(path, "rb") as handle:
            header = handle.read(24)
    except OSError:
        return None
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        return None
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    if width <= 0 or height <= 0:
        return None
    return width, height


def esc(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def status_label(status: str) -> str:
    return {
        "open": "Open",
        "done": "Done",
        "on_hold": "On hold",
        "noted": "Note",
        "blocked": "With the team",
    }.get(status or "", status or "")


def friendly_time(value: str) -> str:
    if not value:
        return ""
    try:
        moment = datetime.fromisoformat(value)
    except ValueError:
        return value
    return moment.strftime("%b %d, %Y, %I:%M %p").replace(" 0", " ")


def human_size(size: int) -> str:
    size = int(size or 0)
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    if size < 1024 ** 3:
        return f"{size / 1024 / 1024:.1f} MB"
    return f"{size / 1024 ** 3:.2f} GB"


def safe_next(value: str) -> str:
    if not value or not value.startswith("/") or value.startswith("//") or "\\" in value or "\n" in value:
        return "/"
    return value


def render_inline(text: str) -> str:
    safe = esc(text)
    safe = re.sub(r"`([^`]+)`", r"<code>\1</code>", safe)

    def link_image(match):
        label, url = match.group(1), match.group(2)
        if not (url.startswith("http://") or url.startswith("https://")):
            return match.group(0)
        return f'<a href="{esc(url)}">{label}</a>'

    safe = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", link_image, safe)
    safe = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", safe)
    safe = re.sub(r"(?<![\"'>])(https?://[^\s<]+)", r'<a href="\1">\1</a>', safe)
    return safe


def render_markdown(text: str) -> str:
    if not text:
        return "<p class=\"muted\">No instructions.</p>"
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    parts = re.split(r"```", text)
    chunks = []
    for index, part in enumerate(parts):
        if index % 2 == 1:
            chunks.append("<pre><code>" + esc(part.strip("\n")) + "</code></pre>")
        else:
            chunks.append(_render_blocks(part))
    return "\n".join(chunks)


def _render_blocks(text: str) -> str:
    lines = text.split("\n")
    out = []
    paragraph = []
    bullets = []
    numbered = []

    def flush_paragraph():
        if paragraph:
            out.append("<p>" + render_inline(" ".join(paragraph)) + "</p>")
            paragraph.clear()

    def flush_bullets():
        if bullets:
            items = "".join(f"<li>{render_inline(item)}</li>" for item in bullets)
            out.append("<ul>" + items + "</ul>")
            bullets.clear()

    def flush_numbered():
        if numbered:
            start = numbered[0][0]
            items = "".join(f"<li>{render_inline(item)}</li>" for _, item in numbered)
            out.append(f'<ol start="{start}">' + items + "</ol>")
            numbered.clear()

    for line in lines:
        number = re.match(r"^\s*(\d+)[.)]\s+(.*)$", line)
        if number:
            flush_paragraph()
            flush_bullets()
            numbered.append((int(number.group(1)), number.group(2)))
        elif re.match(r"^\s*[-*]\s+", line):
            flush_paragraph()
            flush_numbered()
            bullets.append(re.sub(r"^\s*[-*]\s+", "", line))
        elif not line.strip():
            flush_bullets()
            flush_numbered()
            flush_paragraph()
        else:
            flush_bullets()
            flush_numbered()
            paragraph.append(line.strip())
    flush_bullets()
    flush_numbered()
    flush_paragraph()
    return "\n".join(out)


CSS = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
body { margin: 0; font: 18px/1.45 "Segoe UI", system-ui, sans-serif; background: #f4f1ea; color: #1d1a16; }
a { color: #1a4f86; }
main { padding: 4px 14px 40px; }
.app { display: flex; align-items: stretch; min-height: 100vh; }
.side { width: 210px; flex: none; background: #fff; border-right: 1px solid #e4ddd0; padding: 12px; }
.side a.home { display: block; margin: 0 0 12px; padding: 8px 10px; background: #24384c; color: #fff; border-radius: 10px; text-align: center; text-decoration: none; font-weight: 800; }
.side .pc { margin: 0 0 4px; font-size: 13px; font-weight: 700; color: #4a433b; }
.side .status { margin: 0 0 8px; font-size: 15px; font-weight: 700; }
.side .check { margin: 10px 0 0; font-size: 14px; color: #4a433b; }
.side form { display: flex; gap: 6px; align-items: center; margin: 0 0 6px; }
.side select { flex: 1; min-height: 32px; font: inherit; font-size: 14px; padding: 4px; border-radius: 8px; border: 1px solid #cfc6b8; background: #fff; }
.side button { min-height: 32px; min-width: 0; padding: 4px 8px; font-size: 14px; }
.side a.more { display: block; margin-top: 14px; font-size: 15px; }
.content { flex: 1; min-width: 0; max-width: 100%; }
.menu { display: none; }
@media (max-width: 720px) {
  .app { display: block; }
  .menu { display: inline-flex; align-items: center; margin: 8px 14px 0; min-height: 40px; min-width: 40px; padding: 6px 10px; }
  .side { display: none; width: auto; border-right: 0; border-bottom: 1px solid #e4ddd0; }
  .side.open { display: block; }
}
.banner { padding: 12px 14px 14px; background: #e5f0e2; }
.banner.on { background: #f8d6d2; }
.banner p { margin: 0 0 8px; }
.hostscreen { padding: 8px 14px 10px; background: #f7f4ee; border-bottom: 1px solid #e4ddd0; font-size: 15px; }
.hostscreen p { margin: 0 0 6px; }
.hostscreen button { min-height: 36px; min-width: 0; padding: 6px 10px; font-size: 15px; }
.hours { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.hours form { display: flex; gap: 8px; align-items: center; margin: 0; }
button, .btn { min-height: 48px; min-width: 48px; padding: 10px 14px; font: inherit; border: 0; border-radius: 12px; background: #24384c; color: #fff; touch-action: manipulation; }
button.ghost { background: #efe8dc; color: #1d1a16; }
button.wide { width: 100%; background: #1f6b3a; }
button:disabled { background: #d9d3c7; color: #4a433b; }
button.danger { background: #8d2d2d; }
input[type="number"] { width: 5.5rem; min-height: 48px; font: inherit; padding: 8px; border-radius: 12px; border: 1px solid #cfc6b8; }
input[type="text"], textarea, input[type="file"] { width: 100%; font: inherit; padding: 12px; border-radius: 12px; border: 1px solid #cfc6b8; background: #fff; }
textarea { min-height: 120px; }
h1 { font-size: 1.6rem; margin: 12px 0 4px; overflow-wrap: anywhere; }
p, li, h2 { overflow-wrap: anywhere; }
h2 { font-size: 1.15rem; margin: 18px 0 8px; }
.muted { color: #4a433b; }
.saved { background: #e5f0e2; padding: 10px 12px; border-radius: 12px; }
.row { display: block; background: #fff; border-radius: 14px; padding: 14px; margin: 10px 0; text-decoration: none; color: inherit; }
.row .title { display: block; font-weight: 700; overflow-wrap: anywhere; }
.row .meta, .meta { display: block; color: #4a433b; margin-top: 4px; font-size: 16px; overflow-wrap: anywhere; }
.why { display: block; margin-top: 6px; font-size: 16px; color: #1d1a16; overflow-wrap: anywhere; }
.why.missing { color: #a11d1d; font-weight: 700; }
.overdue { box-shadow: inset 6px 0 0 #a11d1d; }
.overdue .title, .overdue .meta { color: #a11d1d; }
.today { background: #fff3c4; }
.card { background: #fff; border-radius: 14px; padding: 14px; margin: 12px 0; overflow-wrap: anywhere; }
.prose p { margin: 0.4em 0; }
.preview img, .preview video, video { max-width: 100%; height: auto; border-radius: 10px; }
.textpreview, pre { white-space: pre-wrap; background: #f6f3ee; padding: 10px; border-radius: 10px; overflow: auto; }
code { font-family: Consolas, ui-monospace, monospace; font-size: 15px; }
details { margin: 14px 0 8px; }
summary { min-height: 48px; display: flex; align-items: center; font-weight: 700; cursor: pointer; }
label { display: block; margin: 10px 0; font-weight: 600; }
form.stack { margin: 12px 0 20px; }
ul, ol { padding-left: 1.4em; }
ol li, ul li { margin: 8px 0; }
.progress { background: #fff; border-radius: 14px; padding: 12px 14px; margin: 8px 0 12px; font-weight: 800; }
.badge { display: inline-block; margin: 8px 0; padding: 10px 14px; border-radius: 12px; font-weight: 800; font-size: 1.05rem; background: #efe8dc; }
.badge.ok { background: #1f6b3a; color: #fff; }
.badge.bad { background: #8d2d2d; color: #fff; }
article.chosen { outline: 3px solid #1f6b3a; background: #e7f6ec; }
article.declined { outline: 3px solid #8d2d2d; background: #fdeceb; }
details.change { margin-top: 12px; }
details.change > summary { min-height: 48px; padding: 12px 14px; background: #efe8dc; border-radius: 12px; }
.saved { font-weight: 800; font-size: 1.05rem; }
.pri { display: inline-block; margin-right: 8px; padding: 2px 8px; border-radius: 8px; font-size: 14px; font-weight: 800; letter-spacing: 0.02em; vertical-align: middle; }
.pri.high { background: #8d2d2d; color: #fff; }
.pri.medium { background: #c47b12; color: #fff; }
.pri.low { background: #d9d3c7; color: #1d1a16; }
.band { margin: 18px 0 8px; }
.retry { display: inline-block; margin-right: 8px; padding: 2px 8px; border-radius: 8px; background: #1f6b3a; color: #fff; font-size: 14px; font-weight: 800; vertical-align: middle; }
button.stuck { background: #8d2d2d; }
.row.waiting { background: #f7f1e4; }
.row.teamlate { box-shadow: inset 6px 0 0 #a11d1d; }
.late { display: block; margin-top: 6px; color: #a11d1d; font-weight: 800; }
.notequote { display: block; margin-top: 6px; overflow-wrap: anywhere; }
.tabs { display: flex; gap: 8px; margin: 12px 0 4px; }
.tabs a { flex: 1 1 0; min-width: 0; text-align: center; padding: 12px 8px; min-height: 48px; background: #efe8dc; border-radius: 12px; text-decoration: none; color: #1d1a16; font-weight: 800; overflow-wrap: anywhere; }
.tabs a.on { background: #24384c; color: #fff; }
"""


_SCREEN_TICK = """<script>
(function () {
  var el = document.getElementById("screenleft");
  if (!el) return;
  var end = Date.parse(el.getAttribute("data-until"));
  function tick() {
    var ms = end - Date.now();
    if (!(ms > 0)) { el.textContent = "(time is up)"; return; }
    el.textContent = "(" + Math.ceil(ms / 60000) + " min left)";
  }
  tick();
  setInterval(tick, 15000);
})();
</script>"""


def _screen_button(next_path: str, action: str, hours: str | None, label: str, stop: bool = False) -> str:
    nxt = esc(safe_next(next_path))
    hidden_hours = ""
    if hours is not None:
        hidden_hours = f'<input type="hidden" name="hours" value="{esc(hours)}">'
    klass = "stop" if stop else ""
    return (
        f'<form method="post" action="/api/host-screen">'
        f'<input type="hidden" name="redirect" value="1">'
        f'<input type="hidden" name="next" value="{nxt}">'
        f'<input type="hidden" name="action" value="{action}">'
        f"{hidden_hours}"
        f'<button class="{klass}" type="submit">{label}</button></form>'
    )


def screen_status_line() -> str:
    if not board_core.hands_off.host_screen_allowed():
        return "Agents: not allowed"
    moment = board_core.hands_off.screen_deadline()
    if moment is None:
        return "Agents: allowed (no limit)"
    return f"Agents: allowed until {board_core.hands_off.format_clock(moment)}"


def last_team_line() -> str:
    latest = ""
    for task in board_core.list_tasks():
        stamp = board_core.latest_note_time(task, "agent")
        if stamp > latest:
            latest = stamp
    if not latest:
        return ""
    try:
        moment = datetime.fromisoformat(latest)
    except ValueError:
        return ""
    clock = moment.strftime("%I:%M %p").lstrip("0")
    if moment.date() == board_core.today_mt():
        return f"Last team check: {clock}"
    day = moment.strftime("%b %d").replace(" 0", " ")
    return f"Last team check: {day}, {clock}"


def screen_control_html(next_path: str) -> str:
    """Compact sidebar control. Allowed only while host-screen.json says so."""
    nxt = esc(safe_next(next_path))
    allow = (
        f'<form class="allow" method="post" action="/api/host-screen">'
        f'<input type="hidden" name="redirect" value="1">'
        f'<input type="hidden" name="next" value="{nxt}">'
        f'<input type="hidden" name="action" value="on">'
        f'<select name="hours" aria-label="Allow">'
        f'<option value="1">1 hour</option>'
        f'<option value="2">2 hours</option>'
        f'<option value="4">4 hours</option>'
        f'<option value="">Until I turn it off</option>'
        f"</select>"
        f'<button type="submit">Allow</button></form>'
    )
    stop = ""
    if board_core.hands_off.host_screen_allowed():
        stop = (
            f'<form method="post" action="/api/host-screen">'
            f'<input type="hidden" name="redirect" value="1">'
            f'<input type="hidden" name="next" value="{nxt}">'
            f'<input type="hidden" name="action" value="off">'
            f'<button class="stop" type="submit">Stop</button></form>'
        )
    return f'<p class="status">{esc(screen_status_line())}</p>{allow}{stop}'


def saved_location(path: str, message: str) -> str:
    text = re.sub(r"\s+", " ", message or "").strip()[:180]
    join = "&" if "?" in path else "?"
    return f"{path}{join}saved={urllib.parse.quote(text)}"


def saved_html(saved) -> str:
    """Banner after a save. False/empty hides it. True or '1' is the generic line."""
    if saved is True or saved == "1":
        text = "Saved."
    elif not saved:
        return ""
    else:
        text = str(saved).strip()
        if not text:
            return ""
    return f'<p class="saved" role="status">{esc(text)}</p>'


_MENU = """<script>
document.querySelector(".menu").addEventListener("click", function () {
  var side = document.getElementById("side");
  var open = side.classList.toggle("open");
  this.setAttribute("aria-expanded", open ? "true" : "false");
});
</script>"""


def layout(title: str, body: str, next_path: str, show_home: bool = False) -> bytes:
    del show_home
    check = last_team_line()
    check_html = f'<p class="check">{esc(check)}</p>' if check else ""
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#3d3428">
<meta name="robots" content="noindex">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Board">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="apple-touch-icon" href="/icon.png">
<link rel="icon" href="/icon.png">
<title>{esc(title)}</title>
<style>{CSS}</style>
</head>
<body>
<div class="app">
<aside id="side" class="side">
<a class="home" href="/">Home</a>
<p class="pc">PC screen</p>
{screen_control_html(next_path)}
{check_html}
<a class="more" href="/schedule">Next 21 days</a>
</aside>
<div class="content">
<button type="button" class="menu" aria-expanded="false" aria-controls="side">\u2630</button>
<main>
{body}
</main>
</div>
</div>
{_MENU}
</body>
</html>
"""
    return page.encode("utf-8")


def priority_tag(task: dict) -> str:
    level = str(task.get("priority") or "")
    if level not in ("high", "medium", "low"):
        return ""
    label = {"high": "High", "medium": "Medium", "low": "Low"}[level]
    return f'<span class="pri {level}">{label}</span>'


def _note_bits(note: dict | None) -> tuple[str, str]:
    if not note:
        return "", ""
    text = " ".join(str(note.get("text") or "").split())
    when = friendly_time(str(note.get("time") or ""))
    return text, when


def row_html(task: dict, today: str, emphasize: bool) -> str:
    due = task.get("due") or ""
    classes = ["row"]
    try:
        today_date = datetime.strptime(today, "%Y-%m-%d").date()
    except ValueError:
        today_date = board_core.today_mt()
    due_text = board_core.due_phrase(due or None, today_date)
    retry = ""
    extra = ""
    if board_core.with_the_team(task):
        classes.append("waiting")
        due_text = board_core.waiting_phrase(task)
        note = board_core.latest_note(task, "owner") or board_core.latest_note(task, "agent")
        text, when = _note_bits(note)
        if text:
            extra += f'<span class="notequote">{esc(text)}</span>'
        if when:
            extra += f'<span class="meta">Sent {esc(when)}</span>'
        if board_core.reply_overdue(task):
            classes.append("teamlate")
            extra += '<span class="late">Overdue for a reply</span>'
    else:
        if emphasize and due and due < today:
            classes.append("overdue")
        elif emphasize and due and due == today:
            classes.append("today")
        if board_core.show_fixed(task):
            label = "Back from the team" if board_core.is_review_task(task) else "Back from the team — see note"
            retry = f'<span class="retry">{label}</span>'
            text, _when = _note_bits(board_core.latest_note(task, "agent"))
            if text:
                extra += f'<span class="notequote">{esc(text)}</span>'
    if task.get("status") == "done" and task.get("completed_at"):
        due_text = f"Done {friendly_time(task.get('completed_at'))}"
    meta = f"{due_text} · {task.get('id')}"
    why = str(task.get("why_owner") or "").strip()
    if why and not board_core.with_the_team(task):
        why_html = f'<span class="why">Why you: {esc(why)}</span>'
    elif board_core.why_missing(task):
        why_html = '<span class="why missing">Missing why only you can do this</span>'
    else:
        why_html = ""
    return (
        f'<a class="{" ".join(classes)}" href="/task/{esc(task.get("id"))}">'
        f'<span class="title">{priority_tag(task)}{retry}{esc(task.get("title"))}</span>'
        f'<span class="meta">{esc(meta)}</span>{extra}{why_html}</a>'
    )


def home_body(tasks: list[dict], saved: bool, tab: str = "mine") -> str:
    if tab not in ("mine", "team"):
        tab = "mine"
    today = board_core.today_mt().isoformat()
    today_label = board_core.today_mt().strftime("%A, %B %d, %Y").replace(" 0", " ")
    team = [task for task in tasks if board_core.with_the_team(task)]
    team.sort(
        key=lambda task: (
            0 if board_core.reply_overdue(task) else 1,
            board_core.unanswered_since(task) or board_core.latest_note_time(task, "agent") or task.get("id") or "",
        )
    )
    own = [task for task in tasks if board_core.team_own_work(task)]
    own.sort(key=lambda task: task.get("due") or "9999-99-99")
    mine_tasks = [task for task in tasks if board_core.adam_visible(task) and not board_core.with_the_team(task)]
    open_tasks = [task for task in mine_tasks if task.get("status") == "open"]
    held = [task for task in mine_tasks if task.get("status") == "on_hold"]
    done = [task for task in mine_tasks if task.get("status") == "done"]
    today_date = board_core.today_mt()
    open_tasks.sort(key=lambda task: board_core.urgency_key(task, today_date))
    held.sort(key=lambda task: board_core.urgency_key(task, today_date))
    done.sort(key=lambda task: (task.get("completed_at") or "", task.get("id") or ""), reverse=True)
    parts = []
    banner = saved_html(saved)
    if banner:
        parts.append(banner)
    parts.append(f"<h1>Gracechase</h1><p class=\"muted\">Mountain time today: {esc(today_label)}</p>")
    mine_on = " on" if tab == "mine" else ""
    team_on = " on" if tab == "team" else ""
    parts.append(
        f'<div class="tabs"><a class="{mine_on.strip()}" href="/">My tasks</a>'
        f'<a class="{team_on.strip()}" href="/?tab=team">With the team ({len(team)})</a></div>'
    )
    if tab == "team":
        if not team:
            parts.append('<p class="muted">Nothing is with the team.</p>')
        else:
            parts.append('<p class="muted">Grace is working on this.</p>')
            parts.extend(row_html(task, today, False) for task in team)
        parts.append(f'<details><summary>Team\'s own work ({len(own)})</summary>')
        parts.append('<p class="muted">Work Adam has not touched.</p>')
        parts.extend(row_html(task, today, False) for task in own)
        if not own:
            parts.append('<p class="muted">Nothing else.</p>')
        parts.append("</details>")
        return "\n".join(parts)
    if not open_tasks:
        parts.append('<p class="muted">Nothing open.</p>')
    else:
        bands = (
            ("do_now", "Do now", "Overdue, due within 2 days, or high priority."),
            ("this_week", "This week", "Due in the next 7 days."),
            ("later", "Later", "No rush, or no deadline."),
        )
        for key, heading, blurb in bands:
            group = [task for task in open_tasks if board_core.task_band(task, today_date) == key]
            if not group:
                continue
            parts.append(f'<h2 class="band">{esc(heading)} ({len(group)})</h2>')
            parts.append(f'<p class="muted">{esc(blurb)}</p>')
            parts.extend(row_html(task, today, True) for task in group)
    parts.append(f"<details><summary>On hold ({len(held)})</summary>")
    parts.extend(row_html(task, today, False) for task in held)
    if not held:
        parts.append('<p class="muted">Nothing on hold.</p>')
    parts.append("</details>")
    parts.append(f"<details><summary>Done ({len(done)})</summary>")
    parts.extend(row_html(task, today, False) for task in done)
    if not done:
        parts.append('<p class="muted">Nothing done.</p>')
    parts.append("</details>")
    return "\n".join(parts)


def preview_html(kind: str, value: str) -> str:
    if kind in ("image", "video", "audio"):
        src = "/media?path=" + urllib.parse.quote(value or "", safe="")
        if kind == "image":
            return f'<div class="preview"><img src="{esc(src)}" alt=""></div>'
        if kind == "video":
            return f'<video controls preload="metadata" src="{esc(src)}"></video>'
        return f'<audio controls preload="none" src="{esc(src)}"></audio>'
    if kind == "link":
        if value.startswith("http://") or value.startswith("https://"):
            return f'<p><a href="{esc(value)}">{esc(value)}</a></p>'
        return f"<p>{esc(value)}</p>"
    return f'<div class="textpreview">{esc(value)}</div>'


def approval_progress(items: list, decisions: dict) -> str:
    counts = board_core.review_counts({"approval_items": items, "approvals": decisions})
    line = f"{counts['answered']} of {counts['total']} answered"
    return f'<p class="progress">{esc(line)}</p>'


def _review_sentence(counts: dict, task: dict | None = None) -> str:
    plan = (task or {}).get("workflow") == "plan"
    if counts["answered"] < counts["total"]:
        if plan:
            return "Answer each plan. Nothing is made until you approve the plan."
        return "Answer each section. Nothing goes live until you approve everything."
    changes = counts["changes"]
    if changes == 0:
        if plan:
            return (
                "Approving the plan turns this into Make, still on your list. "
                "You make the files. Nothing is generated unless you tap a help button."
            )
        return "Agents will publish this after you tap the button. Nothing goes live before that."
    word = "plan" if plan and changes == 1 else "plans" if plan else "section" if changes == 1 else "sections"
    verb = "needs" if changes == 1 else "need"
    return (
        f"The team will fix the {changes} {word} that {verb} changes and send it back for another look. "
        "Nothing goes live until you approve everything."
    )


def _review_label(counts: dict, task: dict | None = None) -> tuple[str, bool]:
    if counts["answered"] < counts["total"]:
        return f"Answer every section first ({counts['answered']} of {counts['total']} done)", True
    if counts["changes"] == 0:
        if (task or {}).get("workflow") == "plan":
            return "Approve plan", False
        return "Approve all — agents publish it", False
    return "Send my notes to the team", False


def review_panel(task: dict) -> str:
    if not board_core.is_review_task(task):
        return ""
    if task.get("status") == "done" or board_core.with_the_team(task) or (task.get("owner") or "") == "agent":
        return ""
    counts = board_core.review_counts(task)
    label, disabled = _review_label(counts, task)
    disabled_attr = " disabled" if disabled else ""
    return (
        f'<p class="why">{esc(_review_sentence(counts, task))}</p>'
        f'<form method="post" action="/api/task/{esc(task.get("id"))}/review">'
        f'<input type="hidden" name="redirect" value="1">'
        f'<button class="wide" type="submit"{disabled_attr}>{esc(label)}</button></form>'
    )


def _section_forms(task_id: str, key: str, comment: str, approve_label: str = "Looks good") -> str:
    looks = (
        f'<form method="post" action="/api/task/{esc(task_id)}/approve">'
        f'<input type="hidden" name="redirect" value="1">'
        f'<input type="hidden" name="key" value="{esc(key)}">'
        f'<input type="hidden" name="decision" value="approve">'
        f'<button type="submit">{esc(approve_label)}</button></form>'
    )
    changes = (
        f'<form class="stack" method="post" action="/api/task/{esc(task_id)}/approve">'
        f'<input type="hidden" name="redirect" value="1">'
        f'<input type="hidden" name="key" value="{esc(key)}">'
        f'<input type="hidden" name="decision" value="reject">'
        f'<label>What should change? <textarea name="comment" maxlength="2000" required>'
        f'{esc(comment)}</textarea></label>'
        f'<button type="submit">Save this section</button></form>'
    )
    return looks + changes


def section_controls(task: dict, key: str, choice: str, comment: str) -> str:
    if task.get("status") in ("done", "blocked") or board_core.with_the_team(task) or (task.get("owner") or "") == "agent":
        return ""
    if task.get("workflow") == "make":
        return ""
    approve_label = "Approve plan" if task.get("workflow") == "plan" else "Looks good"
    forms = _section_forms(task.get("id") or "", key, comment if choice == "reject" else "", approve_label)
    if not choice:
        looks, changes = forms.split("</form>", 1)
        return (
            looks
            + "</form>"
            + f'<details class="change"><summary>Needs changes</summary>{changes}</details>'
        )
    return f'<details class="change"><summary>Change your mind</summary>{forms}</details>'


def task_body(task: dict, saved) -> str:
    section = task.get("section") or ""
    bits = [
        task.get("id"),
        status_label(task.get("status")),
        board_core.due_phrase(task.get("due"), board_core.today_mt()),
    ]
    if section:
        bits.append(section)
    parts = []
    banner = saved_html(saved)
    if banner:
        parts.append(banner)
    parts.append(f"<h1>{priority_tag(task)}{esc(task.get('title'))}</h1>")
    if board_core.with_the_team(task):
        note = board_core.latest_note(task, "owner") or board_core.latest_note(task, "agent")
        text, when = _note_bits(note)
        parts.append(f'<p class="why">{esc(board_core.waiting_phrase(task))}</p>')
        if text:
            parts.append(f'<p class="notequote">{esc(text)}</p>')
        if when:
            parts.append(f'<p class="meta">Sent {esc(when)}</p>')
        if board_core.reply_overdue(task):
            parts.append('<p class="late">Overdue for a reply</p>')
    elif board_core.show_fixed(task):
        label = "Back from the team" if board_core.is_review_task(task) else "Back from the team — see note"
        parts.append(f'<p><span class="retry">{label}</span></p>')
        text, _when = _note_bits(board_core.latest_note(task, "agent"))
        if text:
            parts.append(f'<p class="notequote">{esc(text)}</p>')
    parts.append(f'<p class="meta">{esc(" · ".join(bits))}</p>')
    why = str(task.get("why_owner") or "").strip()
    if why:
        parts.append(f'<p class="why">Why you: {esc(why)}</p>')
    elif board_core.why_missing(task):
        parts.append('<p class="why missing">Missing why only you can do this</p>')
    if (task.get("owner") or "") == "agent" and not board_core.with_the_team(task):
        parts.append('<p class="muted">Agents are doing this. It is not on your list.</p>')
    if task.get("status") == "done":
        who = task.get("completed_by") or ""
        when = friendly_time(task.get("completed_at") or "")
        parts.append(f'<p class="muted">Completed {esc(when)} {esc(who)}</p>')
    parts.append('<div class="card prose">' + render_markdown(task.get("instructions") or "") + "</div>")
    links = task.get("links") or []
    if links:
        items = []
        for link in links:
            if isinstance(link, str) and (link.startswith("http://") or link.startswith("https://")):
                items.append(f'<li><a href="{esc(link)}">{esc(link)}</a></li>')
        if items:
            parts.append("<h2>Links</h2><ul>" + "".join(items) + "</ul>")
    items = task.get("approval_items") or []
    decisions = task.get("approvals") or {}
    if items:
        if task.get("workflow") != "make":
            parts.insert(2 if banner else 1, approval_progress(items, decisions))
        parts.append("<h2>Plan</h2>" if task.get("workflow") in ("plan", "make") else "<h2>Approval</h2>")
        for item in items:
            key = str(item.get("key") or "")
            kind = str(item.get("kind") or "text")
            caption = item.get("caption") or key
            decision = decisions.get(key) or {}
            choice = str(decision.get("decision") or "")
            badge = ""
            klass = "card"
            note = ""
            if choice == "approve":
                klass = "card chosen"
                word = "Plan approved" if task.get("workflow") == "plan" else "Looks good"
                badge = (
                    f'<p><span class="badge ok">{word} ({esc(friendly_time(decision.get("time") or ""))})</span></p>'
                )
            elif choice == "reject":
                klass = "card declined"
                badge = (
                    f'<p><span class="badge bad">Needs changes ({esc(friendly_time(decision.get("time") or ""))})</span></p>'
                )
            else:
                badge = '<p><span class="badge">Not answered yet</span></p>'
            if choice == "reject" and decision.get("comment"):
                note = f'<p>What should change? {esc(decision.get("comment"))}</p>'
            parts.append(
                f'<article class="{klass}"><p><strong>{esc(caption)}</strong></p>'
                f"{badge}"
                f"{preview_html(kind, str(item.get('path_or_text') or ''))}{note}"
                f"{section_controls(task, key, choice, str(decision.get('comment') or ''))}</article>"
            )
        parts.append(review_panel(task))
    notes = list(task.get("notes") or [])
    show_notes = not board_core.is_review_task(task) or bool(notes)
    if show_notes:
        parts.append("<h2>Notes</h2>")
    if show_notes and not notes:
        parts.append('<p class="muted">No notes yet.</p>')
    for note in reversed(notes):
        who = note.get("by") or ""
        parts.append(
            f'<article class="card"><p class="muted">{esc(friendly_time(note.get("time") or ""))} {esc(who)}</p>'
            f'<div class="textpreview">{esc(note.get("text") or "")}</div></article>'
        )
    if not board_core.is_review_task(task):
        parts.append(
            f'<form class="stack" method="post" action="/api/task/{esc(task["id"])}/note">'
            f'<input type="hidden" name="redirect" value="1">'
            f'<label for="note">Add a note</label>'
            f'<textarea id="note" name="text" maxlength="8000"></textarea>'
            f'<button type="submit">Save note</button></form>'
        )
    if (
        not board_core.is_review_task(task)
        and task.get("status") != "done"
        and (task.get("owner") or "adam") != "agent"
    ):
        parts.append(
            f'<form class="stack" method="post" action="/api/task/{esc(task["id"])}/stuck" enctype="multipart/form-data">'
            f'<input type="hidden" name="redirect" value="1">'
            f'<label for="happened">What happened?</label>'
            f'<textarea id="happened" name="text" maxlength="8000" required></textarea>'
            f'<label>A screenshot, if you have one'
            f'<input type="file" name="file" accept="image/*"></label>'
            f'<button class="stuck" type="submit">I\'m stuck</button></form>'
        )
    parts.append("<h2>Files</h2>")
    files = task.get("files") or []
    if not files:
        parts.append('<p class="muted">No files yet.</p>')
    else:
        for item in files:
            name = item.get("name") or ""
            href = f"/files/{task['id']}/{urllib.parse.quote(name)}"
            parts.append(
                f'<p><a href="{esc(href)}">{esc(name)}</a> '
                f'<span class="muted">{esc(human_size(item.get("size") or 0))} · '
                f'{esc(friendly_time(item.get("time") or ""))}</span></p>'
            )
    parts.append(
        f'<form class="stack" method="post" action="/api/task/{esc(task["id"])}/upload" enctype="multipart/form-data">'
        f'<input type="hidden" name="redirect" value="1">'
        f'<label>Add photos, videos, or other files'
        f'<input type="file" name="file" multiple></label>'
        f'<button type="submit">Upload</button></form>'
    )
    if task.get("status") != "done" and not board_core.is_review_task(task) and task.get("workflow") != "make":
        parts.append(
            f'<form method="post" action="/api/task/{esc(task["id"])}/complete" '
            f'onsubmit="return confirm(\'Mark this task done?\');">'
            f'<input type="hidden" name="redirect" value="1">'
            f'<button class="wide" type="submit">Complete</button></form>'
        )
    parts.append(make_panel(task))
    return "\n".join(parts)


def make_panel(task: dict) -> str:
    if task.get("workflow") != "make":
        return ""
    if task.get("status") == "done" or board_core.with_the_team(task) or (task.get("owner") or "") == "agent":
        return ""
    task_id = esc(task.get("id") or "")
    asked = task.get("help_request") or ""
    if asked == "starter_clips":
        asked_line = "<p>You asked for starter clips. The team has that.</p>"
    elif asked == "premiere":
        asked_line = (
            "<p>You asked for a Premiere project. The team will use an organized folder plus an XML or EDL import, "
            "and will say which.</p>"
        )
    else:
        asked_line = ""
    return (
        "<h2>Help, only if you want it</h2>"
        "<p>Nothing is generated until you tap one of these.</p>"
        + asked_line
        + f'<form method="post" action="/api/task/{task_id}/help">'
        f'<input type="hidden" name="redirect" value="1">'
        f'<input type="hidden" name="kind" value="starter_clips">'
        f'<button type="submit">Generate starter clips</button></form>'
        f'<form method="post" action="/api/task/{task_id}/help">'
        f'<input type="hidden" name="redirect" value="1">'
        f'<input type="hidden" name="kind" value="premiere">'
        f'<button type="submit">Make a Premiere project</button></form>'
        "<p>A Premiere project for these batches is an organized folder plus an XML or EDL import. "
        "A .prproj is not built for them.</p>"
        "<h2>Ready to post</h2>"
        "<p>Upload the finished file in Files above, or type its path. "
        "Ready to post schedules it on the planned dates. This counts as approved creative.</p>"
        f'<form class="stack" method="post" action="/api/task/{task_id}/ready">'
        f'<input type="hidden" name="redirect" value="1">'
        f'<label>File path, if it is already on this PC <input name="path" maxlength="500"></label>'
        f'<button class="wide" type="submit">Ready to post</button></form>'
    )


def schedule_body(saved=False) -> str:
    rows, problem = board_core.load_schedule()
    today = board_core.today_mt()
    end = today.fromordinal(today.toordinal() + 20)
    parts = []
    banner = saved_html(saved)
    if banner:
        parts.append(banner)
    parts.extend(
        [
            "<h1>Schedule</h1>",
            f'<p class="muted">Next 21 days, Mountain time ({esc(today.isoformat())} through {esc(end.isoformat())}). Read only.</p>',
        ]
    )
    if problem == "missing":
        parts.append('<p class="muted">No schedule file yet (social/schedule.json).</p>')
        return "\n".join(parts)
    if problem:
        parts.append('<p class="muted">The schedule file could not be read.</p>')
        return "\n".join(parts)
    if not rows:
        parts.append('<p class="muted">Nothing scheduled in the next 21 days.</p>')
        return "\n".join(parts)
    for row in rows:
        approval = row.get("approval_needed")
        if approval is True:
            flag = "approval needed"
        elif approval is False:
            flag = "no approval"
        elif approval in (None, ""):
            flag = ""
        else:
            flag = f"approval: {approval}"
        meta = " · ".join(bit for bit in (row["date"] + " MT", row["platform"], row["status"], flag) if bit)
        parts.append(
            f'<article class="row"><span class="title">{esc(row["title"] or "(no title)")}</span>'
            f'<span class="meta">{esc(meta)}</span></article>'
        )
    return "\n".join(parts)


class UploadRejected(Exception):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status


def _disposition(header: str):
    name = None
    filename = None
    starred = re.search(r"filename\*=UTF-8''([^;]+)", header, re.I)
    if starred:
        filename = urllib.parse.unquote(starred.group(1).strip().strip('"'))
    else:
        quoted = re.search(r'filename="([^"]*)"', header, re.I)
        if quoted:
            filename = quoted.group(1)
        else:
            plain = re.search(r"filename=([^;]+)", header, re.I)
            if plain:
                filename = plain.group(1).strip().strip('"')
    named = re.search(r'\bname="([^"]*)"', header, re.I)
    if named:
        name = named.group(1)
    else:
        plain_name = re.search(r"\bname=([^;]+)", header, re.I)
        if plain_name:
            name = plain_name.group(1).strip().strip('"')
    return name, filename


def _open_unique(directory: str, filename: str):
    os.makedirs(directory, exist_ok=True)
    safe = board_core.safe_filename(filename)
    stem, ext = os.path.splitext(safe)
    for number in range(1, 10000):
        name = safe if number == 1 else f"{stem}-{number}{ext}"
        path = os.path.join(directory, name)
        try:
            descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_BINARY)
        except FileExistsError:
            continue
        return name, path, os.fdopen(descriptor, "wb")
    raise UploadRejected("could not pick a file name")


class _Limited:
    def __init__(self, raw, limit: int):
        self.raw = raw
        self.left = limit

    def read(self, size: int) -> bytes:
        if self.left <= 0 or size <= 0:
            return b""
        chunk = self.raw.read(min(size, self.left))
        if not chunk:
            self.left = 0
            return b""
        self.left -= len(chunk)
        return chunk


def _find_marker(buf: bytes, delim: bytes):
    crlf = b"\r\n" + delim
    lf = b"\n" + delim
    pos_crlf = buf.find(crlf)
    pos_lf = buf.find(lf)
    if pos_crlf < 0 and pos_lf < 0:
        return -1, None
    if pos_crlf < 0:
        return pos_lf, lf
    if pos_lf < 0 or pos_crlf <= pos_lf:
        return pos_crlf, crlf
    return pos_lf, lf


def parse_multipart(stream, content_type: str, content_length: int, dest_dir: str):
    """Stream a multipart body to dest_dir. Returns (fields, files)."""
    match = re.search(r"boundary=([^;]+)", content_type or "", re.I)
    if not match:
        raise UploadRejected("missing multipart boundary")
    boundary = match.group(1).strip().strip('"')
    if not boundary:
        raise UploadRejected("missing multipart boundary")
    if content_length > MAX_UPLOAD + MAX_OVERHEAD:
        raise UploadRejected("upload is over 4 GB", 413)
    delim = b"--" + boundary.encode("utf-8", "replace")
    reader = _Limited(stream, content_length)
    buf = b""

    def pull(size: int = 1024 * 1024) -> int:
        nonlocal buf
        chunk = reader.read(size)
        buf += chunk
        return len(chunk)

    while True:
        stripped = None
        for prefix in (delim, b"\r\n" + delim, b"\n" + delim):
            if buf.startswith(prefix):
                stripped = buf[len(prefix) :]
                break
        if stripped is None and len(buf) > 128:
            found = buf.find(delim)
            if 0 <= found <= 64:
                stripped = buf[found + len(delim) :]
        if stripped is not None:
            buf = stripped
            break
        if pull() == 0:
            raise UploadRejected("multipart boundary not found")

    fields = {}
    files = []
    file_bytes = 0
    created = []
    try:
        while True:
            while len(buf) < 4:
                if pull() == 0:
                    break
            if buf.startswith(b"--") or buf == b"":
                break
            if buf.startswith(b"\r\n"):
                buf = buf[2:]
            elif buf.startswith(b"\n"):
                buf = buf[1:]
            else:
                raise UploadRejected("malformed multipart body")
            while b"\r\n\r\n" not in buf and b"\n\n" not in buf:
                if pull() == 0:
                    raise UploadRejected("truncated multipart headers")
            separator = b"\r\n\r\n" if b"\r\n\r\n" in buf else b"\n\n"
            header_bytes, buf = buf.split(separator, 1)
            try:
                header_text = header_bytes.decode("utf-8", "replace")
            except Exception as exc:
                raise UploadRejected("bad multipart headers") from exc
            disposition = ""
            for header_line in header_text.splitlines():
                if header_line.lower().startswith("content-disposition:"):
                    disposition = header_line.split(":", 1)[1].strip()
            name, filename = _disposition(disposition)
            keep = len(b"\r\n" + delim) - 1
            if filename:
                if len(files) >= MAX_FILES:
                    raise UploadRejected("too many files")
                stored_name, path, handle = _open_unique(dest_dir, filename)
                created.append(path)
                try:
                    while True:
                        pos, marker = _find_marker(buf, delim)
                        if pos >= 0:
                            data = buf[:pos]
                            buf = buf[pos + len(marker) :]
                            file_bytes += len(data)
                            if file_bytes > MAX_UPLOAD:
                                raise UploadRejected("upload is over 4 GB", 413)
                            if data:
                                handle.write(data)
                            break
                        if len(buf) > keep:
                            data = buf[:-keep]
                            buf = buf[-keep:]
                            file_bytes += len(data)
                            if file_bytes > MAX_UPLOAD:
                                raise UploadRejected("upload is over 4 GB", 413)
                            if data:
                                handle.write(data)
                        if pull() == 0:
                            raise UploadRejected("truncated upload")
                finally:
                    handle.close()
                files.append(
                    {
                        "name": stored_name,
                        "path": board_core.display_path(path),
                        "size": os.path.getsize(path),
                        "abs": path,
                    }
                )
            else:
                chunks = []
                while True:
                    pos, marker = _find_marker(buf, delim)
                    if pos >= 0:
                        chunks.append(buf[:pos])
                        buf = buf[pos + len(marker) :]
                        break
                    if len(buf) > keep:
                        chunks.append(buf[:-keep])
                        buf = buf[-keep:]
                    if pull() == 0:
                        raise UploadRejected("truncated multipart field")
                raw = b"".join(chunks)
                if len(raw) > MAX_FORM:
                    raise UploadRejected("form field is too large")
                if name:
                    fields[name] = raw.decode("utf-8", "replace")
    except Exception:
        for path in created:
            try:
                os.remove(path)
            except OSError:
                pass
        raise
    return fields, files


def parse_range(header: str, size: int):
    if not header:
        return None
    if not header.startswith("bytes="):
        return "bad"
    spec = header.split("=", 1)[1].split(",")[0].strip()
    if "-" not in spec:
        return "bad"
    start_text, end_text = spec.split("-", 1)
    try:
        if start_text == "":
            length = int(end_text)
            if length <= 0:
                return "bad"
            start = max(0, size - length)
            end = size - 1
        else:
            start = int(start_text)
            end = int(end_text) if end_text else size - 1
    except ValueError:
        return "bad"
    if start < 0 or start >= size or end < start:
        return "bad"
    return start, min(end, size - 1)


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "GracechaseBoard/1.0"

    def setup(self):
        super().setup()
        try:
            self.connection.settimeout(3600)
        except OSError:
            pass

    def log_message(self, fmt, *args):
        try:
            board_core.log_line(f"{self.address_string()} {fmt % args}")
        except Exception:
            pass

    def handle_one_request(self):
        try:
            super().handle_one_request()
        except Exception:
            board_core.log_line("request crashed\n" + traceback.format_exc())

    def _blocked(self) -> bool:
        host = self.client_address[0] if self.client_address else ""
        if client_allowed(host):
            return False
        body = b"This board is only available on the home network."
        self.send_response(403)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
        return True

    def _send(self, status: int, body: bytes, content_type: str, extra=None):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        for key, value in extra or []:
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def _html(self, status: int, title: str, body: str, next_path: str = "/", show_home: bool = False):
        self._send(status, layout(title, body, next_path, show_home), "text/html; charset=utf-8")

    def _json(self, status: int, payload):
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._send(status, raw, "application/json; charset=utf-8")

    def _redirect(self, location: str):
        self.send_response(303)
        self.send_header("Location", location)
        self.send_header("Content-Length", "0")
        self.send_header("Connection", "close")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def _error(self, status: int, message: str, as_json: bool):
        if as_json:
            self._json(status, {"error": message})
        else:
            self._html(status, "Board", f"<h1>{esc(message)}</h1>", show_home=True)

    def do_GET(self):
        if self._blocked():
            return
        try:
            self._get()
        except board_core.BoardError as exc:
            self._error(self._status_for(exc), str(exc), self.path.startswith("/api/"))
        except Exception:
            board_core.log_line(traceback.format_exc())
            self._error(500, "Something went wrong.", self.path.startswith("/api/"))

    def do_POST(self):
        if self._blocked():
            return
        try:
            self._post()
        except UploadRejected as exc:
            self._error(exc.status, str(exc), self._wants_json())
        except board_core.BoardError as exc:
            self._error(self._status_for(exc), str(exc), self._wants_json())
        except Exception:
            board_core.log_line(traceback.format_exc())
            self._error(500, "Something went wrong.", self._wants_json())

    def _wants_json(self) -> bool:
        return (self.headers.get("Content-Type") or "").startswith("application/json")

    def _status_for(self, exc: Exception) -> int:
        text = str(exc)
        if text.startswith("no task") or text.startswith("no event"):
            return 404
        return 400

    def _get(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        raw_saved = query.get("saved", [""])[0]
        if raw_saved == "1":
            saved = "Saved."
        elif raw_saved:
            saved = "Saved: " + raw_saved[:180]
        else:
            saved = ""
        if path == "/":
            tasks = board_core.list_tasks()
            tab = query.get("tab", ["mine"])[0]
            self._html(200, "Gracechase board", home_body(tasks, saved, tab), "/")
            return
        if path == "/schedule":
            self._html(200, "Schedule", schedule_body(saved), "/schedule", show_home=True)
            return
        if path == "/manifest.webmanifest":
            size = png_size(ICON_PATH) or (1024, 1024)
            payload = {
                "name": "Gracechase Board",
                "short_name": "Board",
                "start_url": "/",
                "scope": "/",
                "display": "standalone",
                "background_color": "#f4f1ea",
                "theme_color": "#3d3428",
                "icons": [
                    {
                        "src": "/icon.png",
                        "sizes": f"{size[0]}x{size[1]}",
                        "type": "image/png",
                        "purpose": "any",
                    }
                ],
            }
            raw = json.dumps(payload).encode("utf-8")
            self._send(200, raw, "application/manifest+json")
            return
        if path in ("/icon.png", "/favicon.ico"):
            self._serve_path(ICON_PATH, "image/png", cache=True)
            return
        match = re.fullmatch(r"/task/(T\d+)", path)
        if match:
            task = board_core.get_task(match.group(1))
            self._html(200, task.get("title") or "Task", task_body(task, saved), self.path, show_home=True)
            return
        match = re.fullmatch(r"/files/(T\d+)/([^/]+)", path)
        if match:
            name = urllib.parse.unquote(match.group(2))
            target = board_core.resolve_upload(match.group(1), name)
            if not target:
                self._error(404, "File not found.", False)
                return
            self._serve_path(target, None, download_name=name)
            return
        if path == "/media":
            target = board_core.resolve_media_path(query.get("path", [""])[0])
            if not target:
                self._error(404, "Preview not available.", False)
                return
            self._serve_path(target, None, download_name=os.path.basename(target))
            return
        if path == "/api/tasks":
            self._json(200, {"version": 1, "tasks": board_core.list_tasks()})
            return
        match = re.fullmatch(r"/api/task/(T\d+)", path)
        if match:
            self._json(200, board_core.get_task(match.group(1)))
            return
        if path == "/api/hands-off":
            self._json(200, board_core.hands_off.public_state())
            return
        if path == "/api/host-screen":
            self._json(200, board_core.hands_off.host_public_state())
            return
        self._error(404, "Not found.", path.startswith("/api/"))

    def _post(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        match = re.fullmatch(r"/api/task/(T\d+)/upload", path)
        if match:
            self._upload(match.group(1))
            return
        match = re.fullmatch(r"/api/task/(T\d+)/stuck", path)
        if match:
            self._stuck(match.group(1))
            return
        fields, as_json = self._read_small()
        redirect = str(fields.get("redirect") or "") == "1" and not as_json
        match = re.fullmatch(r"/api/task/(T\d+)/note", path)
        if match:
            task = board_core.add_note(match.group(1), str(fields.get("text") or ""), by="owner", ping=True)
            self._done(redirect, saved_location(f"/task/{task['id']}", "Note saved"), task)
            return
        match = re.fullmatch(r"/api/task/(T\d+)/complete", path)
        if match:
            task = board_core.complete_task(match.group(1), by="owner (board)")
            self._done(redirect, saved_location(f"/task/{task['id']}", "Marked done"), task)
            return
        match = re.fullmatch(r"/api/task/(T\d+)/review", path)
        if match:
            task = board_core.submit_review(match.group(1))
            if task.get("review_action") == "sent":
                self._done(redirect, saved_location("/?tab=team", "Sent to the team"), task)
            elif task.get("review_action") == "plan":
                self._done(redirect, saved_location(f"/task/{task['id']}", "Plan approved. This is now Make."), task)
            else:
                self._done(redirect, saved_location("/", "Approved. Agents will publish it."), task)
            return
        match = re.fullmatch(r"/api/task/(T\d+)/help", path)
        if match:
            kind = str(fields.get("kind") or "")
            task = board_core.request_help(match.group(1), kind)
            label = "starter clips" if kind == "starter_clips" else "a Premiere project"
            self._done(redirect, saved_location(f"/task/{task['id']}", f"The team will make {label}"), task)
            return
        match = re.fullmatch(r"/api/task/(T\d+)/ready", path)
        if match:
            task = board_core.ready_to_post(match.group(1), str(fields.get("path") or ""))
            self._done(redirect, saved_location("/", "Ready to post. Agents will schedule it."), task)
            return
        match = re.fullmatch(r"/api/task/(T\d+)/approve", path)
        if match:
            key = str(fields.get("key") or "")
            decision = str(fields.get("decision") or "")
            task = board_core.decide(match.group(1), key, decision, str(fields.get("comment") or ""))
            caption = key
            for item in task.get("approval_items") or []:
                if str(item.get("key") or "") == key:
                    caption = str(item.get("caption") or key)
                    break
            if decision.strip().lower() == "approve" and task.get("workflow") == "plan":
                verb = "Approve plan"
            elif decision.strip().lower() == "approve":
                verb = "Looks good"
            else:
                verb = "Needs changes"
            self._done(
                redirect,
                saved_location(f"/task/{task['id']}", f"{verb} {caption}"),
                {"approvals": task.get("approvals")},
            )
            return
        if path == "/api/hands-off":
            state = self._set_hands_off(fields)
            nxt = safe_next(str(fields.get("next") or "/"))
            action = str(fields.get("action") or "").strip().lower()
            hours = str(fields.get("hours") or "").strip()
            if action == "off":
                message = "Hands-off is off"
            elif hours:
                message = f"Hands-off is on for {hours} hours"
            else:
                message = "Hands-off is on until you turn it off"
            self._done(redirect, saved_location(nxt, message), state)
            return
        if path == "/api/host-screen":
            state = self._set_host_screen(fields)
            nxt = safe_next(str(fields.get("next") or "/"))
            action = str(fields.get("action") or "").strip().lower()
            hours = str(fields.get("hours") or "").strip()
            if action == "off":
                message = "Agents will not touch this PC's mouse or screen"
            elif str(fields.get("hours") or "").strip() == "":
                message = "Agents can use your PC screen until you click Stop now"
            else:
                message = f"Agents can use this PC's mouse and screen for {hours} hours"
            self._done(redirect, saved_location(nxt, message), state)
            return
        self._error(404, "Not found.", True)

    def _done(self, redirect: bool, location: str, payload):
        if redirect:
            self._redirect(location)
        else:
            self._json(200, payload)

    def _set_hands_off(self, fields: dict) -> dict:
        action = str(fields.get("action") or "").strip().lower()
        reason = str(fields.get("reason") or "")
        if action == "off":
            board_core.hands_off.set_off(reason or "off", by="owner (board)")
        elif action == "on":
            raw = fields.get("hours")
            hours = None
            if raw not in (None, ""):
                try:
                    hours = float(raw)
                except (TypeError, ValueError) as exc:
                    raise board_core.BoardError("hours must be a number") from exc
            board_core.hands_off.set_on(hours, reason, by="owner (board)")
        else:
            raise board_core.BoardError("action must be on or off")
        return board_core.hands_off.public_state()

    def _set_host_screen(self, fields: dict) -> dict:
        action = str(fields.get("action") or "").strip().lower()
        reason = str(fields.get("reason") or "")
        try:
            if action == "off":
                board_core.hands_off.set_host_deny(reason or "off", by="board")
            elif action == "on":
                raw = fields.get("hours")
                if raw in (None, ""):
                    board_core.hands_off.set_host_allow(None, reason or "allow until turned off", by="board")
                else:
                    try:
                        hours = float(raw)
                    except (TypeError, ValueError) as exc:
                        raise board_core.BoardError("hours must be a number") from exc
                    board_core.hands_off.set_host_allow(hours, reason, by="board")
                board_core.hands_off.set_off("screen allowed", by="board")
            else:
                raise board_core.BoardError("action must be on or off")
        except ValueError as exc:
            raise board_core.BoardError(str(exc)) from exc
        state = board_core.hands_off.host_public_state()
        board_core.log_line(
            "host-screen allow={allow} active={active} until={until} by=board".format(
                allow=state.get("allow"),
                active=state.get("active"),
                until=state.get("until"),
            )
        )
        return state

    def _read_small(self):
        length = self.headers.get("Content-Length")
        if length is None:
            raise board_core.BoardError("Content-Length required")
        try:
            size = int(length)
        except ValueError as exc:
            raise board_core.BoardError("bad Content-Length") from exc
        if size < 0 or size > MAX_FORM:
            raise board_core.BoardError("form is too large")
        raw = self.rfile.read(size) if size else b""
        ctype = self.headers.get("Content-Type") or ""
        if ctype.startswith("application/json"):
            try:
                data = json.loads(raw.decode("utf-8") or "{}")
            except json.JSONDecodeError as exc:
                raise board_core.BoardError("bad JSON") from exc
            if not isinstance(data, dict):
                raise board_core.BoardError("JSON body must be an object")
            return {key: "" if value is None else value for key, value in data.items()}, True
        if ctype.startswith("multipart/"):
            raise board_core.BoardError("this action does not take a file upload")
        parsed = urllib.parse.parse_qs(raw.decode("utf-8", "replace"), keep_blank_values=True)
        return {key: values[-1] for key, values in parsed.items()}, False

    def _upload(self, task_id: str):
        if not re.fullmatch(r"T\d+", task_id):
            raise board_core.BoardError("bad task id")
        board_core.get_task(task_id)
        ctype = self.headers.get("Content-Type") or ""
        if not ctype.startswith("multipart/form-data"):
            raise board_core.BoardError("upload must be multipart")
        length = self.headers.get("Content-Length")
        if length is None:
            raise UploadRejected("Content-Length required", 411)
        try:
            size = int(length)
        except ValueError as exc:
            raise UploadRejected("bad Content-Length") from exc
        fields, files = parse_multipart(self.rfile, ctype, size, board_core.task_file_dir(task_id))
        if not files:
            raise board_core.BoardError("choose at least one file")
        stored = [{"path": item["path"], "name": item["name"], "size": item["size"]} for item in files]
        try:
            task = board_core.register_files(task_id, stored)
        except Exception:
            for item in files:
                try:
                    os.remove(item["abs"])
                except OSError:
                    pass
            raise
        redirect = str(fields.get("redirect") or "") == "1"
        self._done(redirect, saved_location(f"/task/{task['id']}", "File uploaded"), {"files": task.get("files")})

    def _stuck(self, task_id: str):
        if not re.fullmatch(r"T\d+", task_id):
            raise board_core.BoardError("bad task id")
        board_core.get_task(task_id)
        ctype = self.headers.get("Content-Type") or ""
        if not ctype.startswith("multipart/form-data"):
            raise board_core.BoardError("stuck report must be multipart")
        length = self.headers.get("Content-Length")
        if length is None:
            raise UploadRejected("Content-Length required", 411)
        try:
            size = int(length)
        except ValueError as exc:
            raise UploadRejected("bad Content-Length") from exc
        fields, files = parse_multipart(self.rfile, ctype, size, board_core.task_file_dir(task_id))
        text = str(fields.get("text") or "").strip()
        if not text:
            for item in files:
                try:
                    os.remove(item["abs"])
                except OSError:
                    pass
            raise board_core.BoardError("say what happened")
        stored = [{"path": item["path"], "name": item["name"], "size": item["size"]} for item in files]
        try:
            task = board_core.report_stuck(task_id, text, stored)
        except Exception:
            for item in files:
                try:
                    os.remove(item["abs"])
                except OSError:
                    pass
            raise
        redirect = str(fields.get("redirect") or "") == "1"
        self._done(redirect, saved_location(f"/task/{task['id']}", "Grace will fix this"), {"status": task.get("status")})

    def _serve_path(self, path: str, content_type: str | None, download_name: str | None = None, cache: bool = False):
        if not path or not os.path.isfile(path):
            self._error(404, "File not found.", False)
            return
        size = os.path.getsize(path)
        guessed = content_type or mimetypes.guess_type(path)[0] or "application/octet-stream"
        ranged = parse_range(self.headers.get("Range"), size)
        name = download_name or os.path.basename(path)
        if guessed.startswith(("image/", "audio/", "video/", "text/")):
            disposition = "inline"
        else:
            disposition = "attachment"
        if ranged == "bad":
            body = b"Range not satisfiable"
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(body)
            return
        if isinstance(ranged, tuple):
            start, end = ranged
            length = end - start + 1
            self.send_response(206)
            self.send_header("Content-Type", guessed)
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.send_header("Content-Length", str(length))
        else:
            start, length = 0, size
            self.send_response(200)
            self.send_header("Content-Type", guessed)
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", str(size))
        self.send_header("Content-Disposition", f'{disposition}; filename="{name}"')
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Connection", "close")
        if cache:
            self.send_header("Cache-Control", "public, max-age=86400")
        else:
            self.send_header("Cache-Control", "no-store")
        self.end_headers()
        remaining = length
        with open(path, "rb") as handle:
            handle.seek(start)
            while remaining > 0:
                chunk = handle.read(min(1024 * 1024, remaining))
                if not chunk:
                    break
                self.wfile.write(chunk)
                remaining -= len(chunk)


class BoardServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True
    request_queue_size = 32


def _sync_loop():
    raw = os.environ.get("GC_BOARD_SYNC_SECONDS", "20")
    try:
        seconds = float(raw)
    except ValueError:
        seconds = 20
    if seconds <= 0:
        return
    while True:
        time.sleep(seconds)
        try:
            board_core.sync()
        except Exception as exc:
            board_core.log_line(f"sync loop: {exc}")


def main():
    port = int(os.environ.get("GC_BOARD_PORT", "8790"))
    try:
        board_core.sync()
    except Exception as exc:
        board_core.log_line(f"startup sync: {exc}")
    threading.Thread(target=_sync_loop, daemon=True).start()
    board_core.log_line(f"starting on 0.0.0.0:{port}")
    try:
        server = BoardServer(("0.0.0.0", port), Handler)
    except OSError as exc:
        board_core.log_line(f"could not listen on {port}: {exc}")
        raise SystemExit(1)
    board_core.log_line(f"listening on 0.0.0.0:{port}")
    try:
        if sys.stdout:
            print(f"Gracechase board at http://127.0.0.1:{port}/", flush=True)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        board_core.log_line("stopped")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
