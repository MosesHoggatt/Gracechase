"""Task board storage, markdown sync, and owner events.

social/tasks.json is the board. social/tasks.md is the owner's checklist.
social/agent-queue.json is work for agents. It is not shown on the phone.
This module is the only writer for both, so the server and the CLI stay in step.

An owner task (owner "adam") must carry why_owner: a sentence naming the
blocker only Adam can clear. Agent work uses owner "agent" and stays off
the phone list.

GC_BOARD_ROOT, when set, redirects tasks.json, tasks.md, agent-queue.json,
task-files, board-events.jsonl, hands-off.json, host-screen.json, and board.log.
The real social folder is left alone. Used by tests.
"""
from __future__ import annotations

import copy
import json
import os
import re
import subprocess
import sys
import threading
import time
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
REPO = os.path.dirname(TOOLS)
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

import hands_off  # noqa: E402

SACKBUTS_NOTE = "Sackbuts Christmas is on hold until end of week"
PUBLIC_BASE_DEFAULT = "http://192.168.1.59:8790"
LOG_MAX = 5 * 1024 * 1024
_LOG_LOCK = threading.Lock()

_CHECK = re.compile(r"^(\s*- \[)([ xX])(\] )(.*)$")
_MARKER = re.compile(r"^(.*?)(?: <!-- id:(T\d+) -->)?$")
_MARKER_PRESENT = re.compile(r"<!--\s*id:T\d+\s*-->\s*$")
_MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}
_DUE_BY = re.compile(
    r"\bby\s+(?:(?:mon|tue|wed|thu|fri|sat|sun)[a-z]*\s+)?"
    r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+"
    r"(\d{1,2}),?\s+(\d{4})",
    re.I,
)
_DUE_ISO = re.compile(r"\b[Dd]ue\s+(\d{4}-\d{2}-\d{2})\b")
_URL = re.compile(r"https?://[^\s<>\]]+")


class BoardError(Exception):
    pass


# why_owner has to name one of these blockers in a sentence. The phone shows the sentence.
_WHY_OWNER_RULES = (
    ("sign-in, 2FA, or passkey", re.compile(r"sign[\s-]?in|2fa|two-factor|passkey|google account|account owner", re.I)),
    ("payment or billing", re.compile(r"payment|billing|\bcard\b|\bspend\b", re.I)),
    ("legal or tax identity", re.compile(r"legal|tax|identity|songwriter|\bPRO\b|SoundExchange|\bMLC\b", re.I)),
    ("approval of creative, ad copy, or spend", re.compile(r"approv", re.I)),
    ("website go-live preview", re.compile(r"go-live|preview|deploy", re.I)),
    ("admin elevation, BIOS, or a physical step", re.compile(r"\badmin\b|BIOS|physical|elevat|\bUAC\b|\bSVM\b|reboot", re.I)),
)

AGENTS_BLURB = (
    "Not on the phone board. Agents work this from social/agent-queue.json. "
    "Leave these boxes unchecked."
)


def why_owner_error(text: str) -> str | None:
    cleaned = re.sub(r"\s+", " ", (text or "").strip())
    if len(cleaned) < 20:
        return "why_owner must name the specific blocker in a sentence"
    if not any(pattern.search(cleaned) for _label, pattern in _WHY_OWNER_RULES):
        return (
            "why_owner must name the blocker: sign-in/2FA/passkey, payment/billing, "
            "legal/tax identity, approval of creative/ad copy/spend, website go-live preview, "
            "or admin elevation/BIOS/physical step"
        )
    return None


def is_agent_task(task: dict) -> bool:
    if (task.get("owner") or "adam") == "agent":
        return True
    return (task.get("section") or "").strip().lower() == "agents"


def adam_visible(task: dict) -> bool:
    return not is_agent_task(task)


PRIORITIES = ("high", "medium", "low")
_PRIORITY_WEIGHT = {"high": 0, "medium": 3, "low": 7}


def priority_error(value: str | None) -> str | None:
    if value not in PRIORITIES:
        return "priority must be high, medium, or low"
    return None


def checked_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", (value or "")).strip()


def checked_error(value: str | None) -> str | None:
    """Open owner tasks must say when and how an agent confirmed the work is not already done."""
    text = checked_text(value)
    if len(text) < 40:
        return "checked must say when, how (API, browser, files, email, or logs), and what you saw"
    return None


def days_until(due: str | None, today) -> int | None:
    if not due:
        return None
    try:
        moment = datetime.strptime(due, "%Y-%m-%d").date()
    except ValueError:
        return None
    return (moment - today).days


def due_phrase(due: str | None, today) -> str:
    """Plain date line: Due today, Due in 3 days — Mon Nov 9, or No deadline."""
    days = days_until(due, today)
    if days is None:
        return "No deadline"
    moment = datetime.strptime(due, "%Y-%m-%d").date()
    when = f"{moment.strftime('%a')} {moment.strftime('%b')} {moment.day}"
    if days < 0:
        count = -days
        unit = "day" if count == 1 else "days"
        return f"Overdue by {count} {unit} — {when}"
    if days == 0:
        return "Due today"
    if days == 1:
        return f"Due tomorrow — {when}"
    return f"Due in {days} days — {when}"


def task_band(task: dict, today) -> str:
    """do_now, this_week, or later. High priority, overdue, and the next 2 days are Do now."""
    days = days_until(task.get("due"), today)
    if days is not None and days <= 2:
        return "do_now"
    if (task.get("priority") or "") == "high":
        return "do_now"
    if days is not None and days <= 7:
        return "this_week"
    return "later"


def urgency_key(task: dict, today) -> tuple:
    """Overdue first, then sooner dates plus priority. Lower sorts first."""
    days = days_until(task.get("due"), today)
    weight = _PRIORITY_WEIGHT.get(task.get("priority") or "", 3)
    if days is None:
        return (1, 1000 + weight, task.get("id") or "")
    if days < 0:
        return (0, days, weight, task.get("id") or "")
    return (1, days + weight, 0, task.get("id") or "")


def _note_by(note: dict) -> str:
    return str((note or {}).get("by") or "").strip().lower()


def latest_note_time(task: dict, who: str) -> str:
    best = ""
    for note in task.get("notes") or []:
        if _note_by(note) != who:
            continue
        stamp = str(note.get("time") or "")
        if stamp > best:
            best = stamp
    return best


TEAM_REPLY_AFTER = timedelta(hours=4)


def latest_note(task: dict, who: str | None = None) -> dict | None:
    best = None
    best_stamp = ""
    for note in task.get("notes") or []:
        if who and _note_by(note) != who:
            continue
        stamp = str(note.get("time") or "")
        if stamp >= best_stamp:
            best = note
            best_stamp = stamp
    return best


def needs_grace(task: dict) -> bool:
    """His note on an open owner task is waiting for an agent reply."""
    if is_agent_task(task):
        return False
    status = task.get("status") or ""
    if status in ("done", "on_hold", "noted"):
        return False
    if status == "blocked":
        return True
    if status != "open":
        return False
    owner_at = latest_note_time(task, "owner")
    if not owner_at:
        return False
    return owner_at > latest_note_time(task, "agent")


def show_fixed(task: dict) -> bool:
    """An agent replied after he wrote, and the task is back on his list."""
    if is_agent_task(task) or task.get("status") != "open" or needs_grace(task):
        return False
    if task.get("fixed_at"):
        return True
    owner_at = latest_note_time(task, "owner")
    agent_at = latest_note_time(task, "agent")
    return bool(owner_at and agent_at and agent_at > owner_at)


def with_the_team(task: dict) -> bool:
    """On the With the team tab: his unanswered note, or a task pulled off his list with a note."""
    status = task.get("status") or ""
    if status in ("done", "on_hold", "noted"):
        return False
    if needs_grace(task):
        return True
    return bool(is_agent_task(task) and task.get("held_from_owner"))


def team_own_work(task: dict) -> bool:
    """Agent queue items he never touched. They stay out of the With the team count."""
    status = task.get("status") or ""
    if status in ("done", "on_hold", "noted"):
        return False
    return bool(is_agent_task(task) and not with_the_team(task))


def unanswered_since(task: dict) -> str:
    """When his latest note started waiting. Empty once an agent note is newer."""
    owner_at = latest_note_time(task, "owner")
    agent_at = latest_note_time(task, "agent")
    if owner_at and owner_at > (agent_at or ""):
        return owner_at
    return ""


def reply_overdue(task: dict, now: datetime | None = None) -> bool:
    since = unanswered_since(task)
    if not since:
        return False
    try:
        moment = datetime.fromisoformat(since)
    except ValueError:
        return False
    current = now or datetime.now().astimezone()
    if moment.tzinfo is None and current.tzinfo is not None:
        moment = moment.replace(tzinfo=current.tzinfo)
    if current.tzinfo is None and moment.tzinfo is not None:
        current = current.replace(tzinfo=moment.tzinfo)
    return current - moment > TEAM_REPLY_AFTER


def clock_label(stamp: str) -> str:
    if not stamp:
        return ""
    try:
        moment = datetime.fromisoformat(stamp)
    except ValueError:
        return ""
    return moment.strftime("%I:%M %p").lstrip("0")


def waiting_phrase(task: dict) -> str:
    del task
    return "Grace is working on this"


def why_missing(task: dict) -> bool:
    """Open tasks on Adam's board with no reason. On hold and done are left alone."""
    if is_agent_task(task):
        return False
    if task.get("status") != "open":
        return False
    return not str(task.get("why_owner") or "").strip()


def _fill_owner(task: dict, section: str) -> bool:
    changed = False
    if not task.get("owner"):
        task["owner"] = "agent" if (section or "").strip().lower() == "agents" else "adam"
        changed = True
    if task.get("why_owner") is None or "why_owner" not in task:
        task["why_owner"] = ""
        changed = True
    return changed


def data_root() -> str:
    env = os.environ.get("GC_BOARD_ROOT")
    if env:
        return os.path.abspath(env)
    return os.path.join(REPO, "social")


def public_base() -> str:
    return os.environ.get("GC_BOARD_PUBLIC_BASE", PUBLIC_BASE_DEFAULT).rstrip("/")


def task_url(task_id: str) -> str:
    """Phone page for one task. Calendar events that belong to a task start with this, not the home page."""
    return f"{public_base()}/task/{task_id}"


def tasks_json_path() -> str:
    return os.path.join(data_root(), "tasks.json")


def tasks_md_path() -> str:
    return os.path.join(data_root(), "tasks.md")


def agent_queue_path() -> str:
    return os.path.join(data_root(), "agent-queue.json")


def events_path() -> str:
    return os.path.join(data_root(), "board-events.jsonl")


def task_files_root() -> str:
    return os.path.join(data_root(), "task-files")


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def today_mt():
    try:
        from zoneinfo import ZoneInfo

        return datetime.now(ZoneInfo("America/Denver")).date()
    except Exception:
        return datetime.now().astimezone().date()


def log_line(message: str) -> None:
    text = str(message).replace("\r", " ").replace("\n", " ")
    line = f"{now_iso()} {text}\n"
    path = os.path.join(data_root(), "board.log")
    with _LOG_LOCK:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            maybe_rotate(path, LOG_MAX)
            with open(path, "a", encoding="utf-8", newline="\n") as handle:
                handle.write(line)
        except OSError:
            pass


def maybe_rotate(path: str, limit: int) -> None:
    if os.path.isfile(path) and os.path.getsize(path) >= limit:
        os.replace(path, path + ".1")


class BoardLock:
    """Cross-process lock. Not reentrant on the same thread."""

    def __enter__(self):
        import msvcrt

        os.makedirs(data_root(), exist_ok=True)
        self._handle = open(os.path.join(data_root(), ".board.lock"), "a+b")
        deadline = time.time() + 30
        while True:
            try:
                self._handle.seek(0)
                msvcrt.locking(self._handle.fileno(), msvcrt.LK_NBLCK, 1)
                return self
            except OSError:
                if time.time() > deadline:
                    raise BoardError("board data is busy; try again")
                time.sleep(0.05)

    def __exit__(self, exc_type, exc, tb):
        import msvcrt

        try:
            self._handle.seek(0)
            msvcrt.locking(self._handle.fileno(), msvcrt.LK_UNLCK, 1)
        except OSError:
            pass
        self._handle.close()


def _atomic_bytes(path: str, data: bytes) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = f"{path}.{os.getpid()}.{threading.get_ident()}.tmp"
    try:
        with open(tmp, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        last_error = None
        for attempt in range(8):
            try:
                os.replace(tmp, path)
                return
            except PermissionError as exc:
                # Windows denies the replace while another reader, often the editor, has the file.
                last_error = exc
                time.sleep(0.15 * (attempt + 1))
        if last_error:
            raise last_error
    finally:
        if os.path.isfile(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass


def _fresh_doc() -> dict:
    return {"version": 1, "next_id": 1, "tasks": []}


def _load() -> dict:
    path = tasks_json_path()
    if not os.path.isfile(path):
        return _fresh_doc()
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise BoardError(f"tasks.json could not be read ({exc}); refusing to overwrite it") from exc
    if not isinstance(data, dict) or not isinstance(data.get("tasks"), list):
        raise BoardError("tasks.json is malformed; refusing to overwrite it")
    data.setdefault("version", 1)
    data.setdefault("next_id", 1)
    return data


def _save(doc: dict) -> None:
    payload = {
        "version": 1,
        "next_id": int(doc.get("next_id") or 1),
        "tasks": doc.get("tasks") or [],
    }
    raw = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
    _atomic_bytes(tasks_json_path(), raw)


def _read_md():
    path = tasks_md_path()
    if not os.path.isfile(path):
        return None, False
    try:
        raw = open(path, "rb").read()
    except OSError as exc:
        raise BoardError(f"tasks.md could not be read ({exc})") from exc
    bom = raw.startswith(b"\xef\xbb\xbf")
    body = raw[3:] if bom else raw
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise BoardError(f"tasks.md is not UTF-8 ({exc}); refusing to rewrite it") from exc
    return text, bom


def _write_md(text: str, bom: bool) -> None:
    raw = text.encode("utf-8")
    if bom:
        raw = b"\xef\xbb\xbf" + raw
    _atomic_bytes(tasks_md_path(), raw)


def split_ending(line: str) -> tuple[str, str]:
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    if line.endswith("\r"):
        return line[:-1], "\r"
    return line, ""


def split_lines(text: str | None) -> list[str]:
    if not text:
        return []
    parts = text.split("\n")
    lines = []
    for index, part in enumerate(parts):
        if index < len(parts) - 1:
            lines.append(part + "\n")
        elif part:
            lines.append(part)
    return lines


def analyze(line: str):
    core, ending = split_ending(line)
    match = _CHECK.match(core)
    if not match:
        return None
    body_match = _MARKER.match(match.group(4))
    body = body_match.group(1) if body_match else match.group(4)
    marker = body_match.group(2) if body_match else None
    return {
        "ending": ending,
        "checked": match.group(2).lower() == "x",
        "body": body,
        "marker": marker,
    }


def lines_are_safe(old_text: str, new_text: str) -> bool:
    """True when the new file only checks boxes, adds id markers, or inserts agent lines."""
    old_lines = split_lines(old_text)
    new_lines = split_lines(new_text)
    cursor = 0
    total = len(new_lines)
    for old in old_lines:
        matched = False
        while cursor < total:
            new = new_lines[cursor]
            cursor += 1
            if new == old or allowed_edit(old, new):
                matched = True
                break
            if is_agent_insert(new):
                continue
            return False
        if not matched:
            return False
    while cursor < total:
        if not is_agent_insert(new_lines[cursor]):
            return False
        cursor += 1
    return True


def allowed_edit(old: str, new: str) -> bool:
    before = analyze(old)
    after = analyze(new)
    if not before or not after:
        return False
    if before["ending"] != after["ending"]:
        return False
    if before["body"] != after["body"]:
        return False
    if before["checked"] and not after["checked"]:
        return False
    if before["marker"] and before["marker"] != after["marker"]:
        return False
    if before["marker"] is None and after["marker"] is None:
        return (not before["checked"]) and after["checked"]
    return True


def is_agent_insert(line: str) -> bool:
    info = analyze(line)
    if not info or info["checked"] or not info["marker"]:
        return False
    pattern = (
        r"^.+\. Due (?:\d{4}-\d{2}-\d{2}|none)\. Open: https?://\S+/task/"
        + re.escape(info["marker"])
        + r"$"
    )
    return re.match(pattern, info["body"]) is not None


def make_title(text: str, limit: int = 90) -> str:
    """First sentence, trimmed to `limit` characters.

    A leading fragment shorter than 24 characters (a date stamp such as
    "November 4.") is joined to the next sentence so the phone row is useful.
    """
    cleaned = _MARKER_PRESENT.sub("", text or "")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    sentences = []
    rest = cleaned
    title = ""
    while rest and len(sentences) < 3:
        match = re.search(r"[.!?]\s", rest)
        if match:
            sentences.append(rest[: match.start() + 1].strip())
            rest = rest[match.end() :].strip()
        else:
            sentences.append(rest.strip())
            rest = ""
        title = " ".join(part.strip() for part in sentences).strip()
        if len(title.rstrip(".")) >= 24:
            break
    if title.endswith(".") and not title.endswith("..."):
        title = title[:-1].rstrip()
    if len(title) <= limit:
        return title or "Task"
    budget = max(1, limit - 3)
    clipped = title[:budget]
    space = clipped.rfind(" ")
    if space >= 40:
        clipped = clipped[:space]
    clipped = clipped.rstrip(" .,:;")
    if not clipped:
        return "Task"
    return (clipped + "...")[:limit]


def parse_due(text: str) -> str | None:
    if not text:
        return None
    iso = _DUE_ISO.search(text)
    if iso:
        try:
            datetime.strptime(iso.group(1), "%Y-%m-%d")
        except ValueError:
            return None
        return iso.group(1)
    match = _DUE_BY.search(text)
    if not match:
        return None
    month = _MONTHS[match.group(1)[:3].lower()]
    day = int(match.group(2))
    year = int(match.group(3))
    try:
        return datetime(year, month, day).date().isoformat()
    except ValueError:
        return None


def extract_links(text: str) -> list[str]:
    found = []
    for raw in _URL.findall(text or ""):
        url = raw.rstrip(").,;\"'")
        if url and url not in found:
            found.append(url)
    return found


def _http_status(url: str) -> int:
    import urllib.error
    import urllib.request

    request = urllib.request.Request(url, headers={"User-Agent": "Gracechase-link-check"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return int(response.status)
    except urllib.error.HTTPError as exc:
        return int(exc.code)
    except Exception:
        return 0


def _collect_links(task: dict) -> list[str]:
    found = []
    for raw in list(task.get("links") or []) + extract_links(task.get("instructions") or ""):
        link = str(raw or "").strip()
        if link.startswith("http://") or link.startswith("https://"):
            if link not in found:
                found.append(link)
    for item in task.get("approval_items") or []:
        if not isinstance(item, dict):
            continue
        value = str(item.get("path_or_text") or "").strip()
        if (value.startswith("http://") or value.startswith("https://")) and value not in found:
            found.append(value)
    return found


def is_preview_task(task: dict) -> bool:
    pieces = [
        str(task.get("title") or ""),
        str(task.get("instructions") or ""),
        " ".join(str(link) for link in (task.get("links") or [])),
    ]
    for item in task.get("approval_items") or []:
        if isinstance(item, dict):
            pieces.append(str(item.get("path_or_text") or ""))
    blob = " ".join(pieces).lower()
    return "preview the website" in blob or ":8791" in blob


def needs_approval_items(task: dict) -> bool:
    if is_preview_task(task):
        return True
    title = str(task.get("title") or "").lower()
    return title.startswith("approve ") or title.startswith("is the ")


def _approval_file_ok(path: str) -> bool:
    if path and os.path.isfile(path):
        return True
    if path and not path.startswith(("http://", "https://")):
        return os.path.isfile(os.path.join(REPO, path))
    return False


def ready_error(task: dict) -> str | None:
    """Why an open owner task is not ready for Adam's list. None when it can be open.

    A website preview needs a port-8791 link that returns 200 and an Approve or Reject
    item. An approval task needs those items, and each image, video, or audio item has
    to be a file that exists. Other links that 404, or that do not connect, also hold
    the task on the agent queue. Set GC_BOARD_SKIP_LINK_CHECK=1 to skip the HTTP check.
    """
    if (task.get("owner") or "adam") != "adam":
        return None
    if task.get("status") not in (None, "open", ""):
        return None
    links = _collect_links(task)
    if needs_approval_items(task) and not task.get("approval_items"):
        return "this task needs an Approve or Reject item before it goes on Adam's list"
    if is_preview_task(task) and not any(":8791" in url for url in links):
        return "a website preview needs a preview link before it goes on Adam's list"
    for item in task.get("approval_items") or []:
        if not isinstance(item, dict):
            continue
        if item.get("kind") in ("image", "video", "audio") and not _approval_file_ok(str(item.get("path_or_text") or "")):
            label = str(item.get("path_or_text") or item.get("key") or "item")
            return f"approval file is missing: {label}"
    if os.environ.get("GC_BOARD_SKIP_LINK_CHECK") == "1":
        return None
    preview = is_preview_task(task)
    for url in links:
        status = _http_status(url)
        if preview or ":8791" in url:
            if status != 200:
                return f"not ready for Adam's list, link returned {status}: {url}"
        elif status in (0, 404):
            return f"not ready for Adam's list, link returned {status}: {url}"
    return None


def _bump_next(doc: dict, number: int) -> None:
    current = int(doc.get("next_id") or 1)
    if current < number:
        doc["next_id"] = number


def _alloc_id(doc: dict) -> str:
    number = int(doc.get("next_id") or 1)
    for task in doc["tasks"]:
        match = re.fullmatch(r"T(\d+)", str(task.get("id") or ""))
        if match:
            number = max(number, int(match.group(1)) + 1)
    doc["next_id"] = number + 1
    return f"T{number:03d}"


def _blank_task(task_id: str, title: str, **extra) -> dict:
    task = {
        "id": task_id,
        "title": title,
        "due": extra.get("due"),
        "status": extra.get("status", "open"),
        "section": extra.get("section") or "",
        "created": extra.get("created") or now_iso(),
        "completed_at": extra.get("completed_at"),
        "completed_by": extra.get("completed_by"),
        "instructions": extra.get("instructions") or "",
        "links": list(extra.get("links") or []),
        "approval_items": list(extra.get("approval_items") or []),
        "approvals": dict(extra.get("approvals") or {}),
        "notes": list(extra.get("notes") or []),
        "files": list(extra.get("files") or []),
        "source": extra.get("source") or "tasks.md",
        "md_id": extra.get("md_id") or task_id,
        "md_linked": bool(extra.get("md_linked", True)),
        "owner": extra.get("owner") or "adam",
        "why_owner": extra.get("why_owner") or "",
        "priority": extra.get("priority") or "",
        "checked": extra.get("checked") or "",
        "held_from_owner": bool(extra.get("held_from_owner")),
        "held_at": extra.get("held_at") or "",
    }
    return task


def _mark_done(task: dict, by: str) -> None:
    task["status"] = "done"
    task["completed_at"] = now_iso()
    task["completed_by"] = by


def _add_marker(line: str, task_id: str) -> str:
    core, ending = split_ending(line)
    if _MARKER_PRESENT.search(core):
        return line
    return f"{core} <!-- id:{task_id} -->{ending}"


def _check_line(line: str) -> str:
    core, ending = split_ending(line)
    match = re.match(r"^(\s*)- \[ \](.*)$", core)
    if not match:
        return line
    return f"{match.group(1)}- [x]{match.group(2)}{ending}"


def _now_insert_index(lines: list[str]) -> int | None:
    for index, line in enumerate(lines):
        core, _ending = split_ending(line)
        if core == "## Now":
            if index + 1 < len(lines) and split_ending(lines[index + 1])[0] == "":
                return index + 2
            return index + 1
    return None


def _agent_line(task: dict, ending: str) -> str:
    title = re.sub(r"\s+", " ", (task.get("title") or "Task")).strip().rstrip(".")
    title = title.replace("<!--", "")
    due = task.get("due") or "none"
    url = task_url(task["id"])
    return f"- [ ] {title}. Due {due}. Open: {url} <!-- id:{task['id']} -->{ending}"


def _dominant_ending(lines: list[str]) -> str:
    for line in lines:
        if line.endswith("\r\n"):
            return "\r\n"
    return "\n"


def _import_task(doc: dict, task_id: str, body: str, checked: bool, section: str) -> dict:
    stamp = now_iso()
    notes = []
    completed_at = None
    completed_by = None
    if checked:
        status = "done"
        completed_at = stamp
        completed_by = "owner (tasks.md)"
    elif body.startswith("Sackbuts Christmas"):
        status = "on_hold"
        notes = [{"time": stamp, "text": SACKBUTS_NOTE, "by": "migration"}]
    else:
        status = "open"
    task = _blank_task(
        task_id,
        make_title(body),
        due=parse_due(body),
        status=status,
        section=section,
        created=stamp,
        completed_at=completed_at,
        completed_by=completed_by,
        instructions=body,
        links=extract_links(body),
        notes=notes,
        source="tasks.md",
        md_id=task_id,
        md_linked=True,
        owner="agent" if (section or "").strip().lower() == "agents" else "adam",
        why_owner="",
    )
    doc["tasks"].append(task)
    match = re.fullmatch(r"T(\d+)", task_id)
    if match:
        _bump_next(doc, int(match.group(1)) + 1)
    return task


def _assign(task: dict, key: str, value) -> bool:
    if task.get(key) != value:
        task[key] = value
        return True
    return False


def _apply_checks_only(text: str, doc: dict) -> bool:
    """Mark json done where the owner already checked the box. Does not edit markdown."""
    by_id = {task["id"]: task for task in doc["tasks"]}
    changed = False
    fence = False
    for line in split_lines(text):
        core, _ending = split_ending(line)
        if core.strip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        info = analyze(line)
        if not info or not info["marker"] or not info["checked"]:
            continue
        task = by_id.get(info["marker"])
        if task and task.get("status") != "done":
            _mark_done(task, "owner (tasks.md)")
            changed = True
    return changed


def _compute(text: str | None, doc: dict) -> tuple[str | None, dict, bool, bool, dict]:
    stats = {"imported": 0, "checked": 0, "done_from_md": 0, "inserted": 0}
    if text is None:
        return None, doc, False, False, stats
    lines = split_lines(text)
    by_id = {task["id"]: task for task in doc["tasks"]}
    md_changed = False
    json_changed = False
    seen = set()
    section = ""
    fence = False
    for index, line in enumerate(lines):
        core, _ending = split_ending(line)
        if core.strip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        heading = re.match(r"^##\s+(.*?)\s*$", core)
        if heading:
            section = heading.group(1)
            continue
        info = analyze(line)
        if not info:
            continue
        if info["marker"]:
            seen.add(info["marker"])
            task = by_id.get(info["marker"])
            if task is None:
                task = _import_task(doc, info["marker"], info["body"], info["checked"], section)
                by_id[task["id"]] = task
                json_changed = True
                stats["imported"] += 1
            else:
                if _assign(task, "md_linked", True):
                    json_changed = True
                if info["checked"] and task.get("status") != "done":
                    _mark_done(task, "owner (tasks.md)")
                    json_changed = True
                    stats["done_from_md"] += 1
                elif task.get("status") == "done" and not info["checked"]:
                    updated = _check_line(line)
                    if updated != line:
                        lines[index] = updated
                        md_changed = True
                        stats["checked"] += 1
                if task.get("source") == "tasks.md":
                    if _assign(task, "instructions", info["body"]):
                        json_changed = True
                    if _assign(task, "title", make_title(info["body"])):
                        json_changed = True
                    if _assign(task, "links", extract_links(info["body"])):
                        json_changed = True
                    if _assign(task, "due", parse_due(info["body"])):
                        json_changed = True
                if section and _assign(task, "section", section):
                    json_changed = True
                if _fill_owner(task, section):
                    json_changed = True
            continue
        task_id = _alloc_id(doc)
        task = _import_task(doc, task_id, info["body"], info["checked"], section)
        by_id[task_id] = task
        lines[index] = _add_marker(line, task_id)
        seen.add(task_id)
        md_changed = True
        json_changed = True
        stats["imported"] += 1
    pending = [
        task
        for task in doc["tasks"]
        if task.get("source") == "agent"
        and not task.get("md_linked")
        and task["id"] not in seen
        and (task.get("owner") or "adam") != "agent"
    ]
    pending.sort(key=lambda task: task["id"])
    if pending:
        insert_at = _now_insert_index(lines)
        if insert_at is None:
            raise BoardError("tasks.md has no '## Now' section; not inserting a line")
        ending = _dominant_ending(lines)
        for task in pending:
            lines.insert(insert_at, _agent_line(task, ending))
            task["md_linked"] = True
            insert_at += 1
            stats["inserted"] += 1
            md_changed = True
            json_changed = True
    new_text = "".join(lines)
    if new_text == text:
        md_changed = False
    return new_text, doc, md_changed, json_changed, stats


def _sync_locked() -> dict:
    for _attempt in range(3):
        text, bom = _read_md()
        doc = _load()
        new_text, new_doc, md_changed, json_changed, stats = _compute(text, doc)
        text2, bom2 = _read_md()
        if text2 == text and bom2 == bom:
            break
    else:
        text, _bom = _read_md()
        doc = _load()
        if text is not None and _apply_checks_only(text, doc):
            _save(doc)
            log_line("tasks.md changed while syncing; updated checked tasks only")
            return {"imported": 0, "checked": 0, "done_from_md": 1, "inserted": 0, "md_written": False}
        log_line("tasks.md changed while syncing; skipped this pass")
        return {"imported": 0, "checked": 0, "done_from_md": 0, "inserted": 0, "md_written": False}
    if md_changed and text is not None and new_text is not None:
        if not lines_are_safe(text, new_text):
            raise BoardError("refusing to write tasks.md: the edit was not limited to single checklist lines")
        _write_md(new_text, bom)
        stats["md_written"] = True
    else:
        stats["md_written"] = False
    if json_changed:
        _save(new_doc)
        stats["json_written"] = True
    else:
        stats["json_written"] = False
    if any(stats.get(key) for key in ("imported", "checked", "done_from_md", "inserted")):
        log_line(
            "sync imported={imported} checked={checked} done_from_md={done_from_md} inserted={inserted}".format(
                **stats
            )
        )
    return stats


def sync() -> dict:
    with BoardLock():
        return _sync_locked()


def _must(doc: dict, task_id: str) -> dict:
    for task in doc["tasks"]:
        if task.get("id") == task_id:
            return task
    raise BoardError(f"no task {task_id}")


def list_tasks() -> list[dict]:
    with BoardLock():
        _sync_locked()
        return copy.deepcopy(_load()["tasks"])


def get_task(task_id: str) -> dict:
    with BoardLock():
        _sync_locked()
        return copy.deepcopy(_must(_load(), task_id))


def _clean_approval_items(approval_items: list[dict]) -> list[dict]:
    items = []
    seen_keys = set()
    for item in approval_items or []:
        if not isinstance(item, dict):
            raise BoardError("approval items must be objects")
        key = str(item.get("key") or "").strip()
        kind = str(item.get("kind") or "").strip()
        if not key or key in seen_keys:
            raise BoardError("each approval item needs a unique key")
        if kind not in ("image", "video", "audio", "text", "link"):
            raise BoardError("approval kind must be image, video, audio, text, or link")
        seen_keys.add(key)
        items.append(
            {
                "key": key,
                "kind": kind,
                "path_or_text": str(item.get("path_or_text") or ""),
                "caption": str(item.get("caption") or ""),
            }
        )
    return items


def _clean_links(links: list[str]) -> list[str]:
    cleaned = []
    for link in links or []:
        link = (link or "").strip()
        if link and link not in cleaned:
            cleaned.append(link)
    return cleaned


def _write_agent_queue(doc: dict) -> None:
    items = []
    for task in doc.get("tasks") or []:
        if (task.get("owner") or "") != "agent":
            continue
        if task.get("status") == "done":
            continue
        items.append(
            {
                "id": task.get("id"),
                "title": task.get("title") or "",
                "status": task.get("status") or "open",
                "due": task.get("due"),
                "section": task.get("section") or "Agents",
                "instructions": task.get("instructions") or "",
                "links": list(task.get("links") or []),
                "notes": list(task.get("notes") or []),
            }
        )
    payload = {"version": 1, "updated": now_iso(), "items": items}
    raw = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
    _atomic_bytes(agent_queue_path(), raw)


def _set_line_body(text: str, task_id: str, body: str) -> str:
    """Replace one checklist line's words. The box and the id comment stay."""
    body = re.sub(r"\s+", " ", body or "").strip().replace("<!--", "")
    lines = split_lines(text)
    for index, line in enumerate(lines):
        info = analyze(line)
        if not info or info["marker"] != task_id:
            continue
        mark = "x" if info["checked"] else " "
        ending = info["ending"] or "\n"
        lines[index] = f"- [{mark}] {body} <!-- id:{task_id} -->{ending}"
        break
    return "".join(lines)


def _retitle_agent_line(text: str, task: dict) -> str:
    lines = split_lines(text)
    ending = _dominant_ending(lines) or "\n"
    for index, line in enumerate(lines):
        info = analyze(line)
        if not info or info["marker"] != task.get("id"):
            continue
        if info["checked"]:
            break
        lines[index] = _agent_line(task, info["ending"] or ending)
        break
    return "".join(lines)


def _relocate_to_now(text: str, task_id: str) -> str:
    """Move one line under ## Now. Does not change its checkbox."""
    lines = split_lines(text)
    found = None
    kept = []
    for line in lines:
        info = analyze(line)
        if info and info["marker"] == task_id and found is None:
            found = line
            continue
        kept.append(line)
    if found is None:
        return text
    ending = _dominant_ending(kept) or "\n"
    if not found.endswith(("\n", "\r\n")):
        found = found + ending
    out = []
    inserted = False
    for line in kept:
        out.append(line)
        if not inserted and split_ending(line)[0] == "## Now":
            out.append(found)
            inserted = True
    if not inserted:
        out.append(found)
    return "".join(out)


def _relocate_to_agents(text: str, task_id: str) -> str:
    """Move one line under ## Agents. Does not change its checkbox."""
    lines = split_lines(text)
    found = None
    kept = []
    for line in lines:
        info = analyze(line)
        if info and info["marker"] == task_id and found is None:
            found = line
            continue
        kept.append(line)
    if found is None:
        return text
    ending = _dominant_ending(kept) or "\n"
    if not any(split_ending(line)[0] == "## Agents" for line in kept):
        if kept and not kept[-1].endswith(("\n", "\r\n")):
            kept[-1] = kept[-1] + ending
        if not (kept and split_ending(kept[-1])[0] == ""):
            kept.append(ending)
        kept.append(f"## Agents{ending}")
        kept.append(ending)
        kept.append(f"{AGENTS_BLURB}{ending}")
        kept.append(ending)
    if kept and not kept[-1].endswith(("\n", "\r\n")):
        kept[-1] = kept[-1] + ending
    if not found.endswith(("\n", "\r\n")):
        found = found + ending
    kept.append(found)
    return "".join(kept)


def add_task(
    title: str,
    due: str | None,
    instructions: str,
    links: list[str],
    approval_items: list[dict],
    owner: str = "adam",
    why_owner: str = "",
    priority: str = "",
    checked: str = "",
) -> dict:
    title = re.sub(r"\s+", " ", (title or "").strip())
    if not title:
        raise BoardError("title is required")
    owner = (owner or "adam").strip().lower()
    if owner not in ("adam", "agent"):
        raise BoardError("owner must be adam or agent")
    why = re.sub(r"\s+", " ", (why_owner or "").strip())
    if owner == "adam":
        error = why_owner_error(why)
        if error:
            raise BoardError(error)
        bad_priority = priority_error(priority)
        if bad_priority:
            raise BoardError(bad_priority)
        bad_checked = checked_error(checked)
        if bad_checked:
            raise BoardError(bad_checked)
        checked = checked_text(checked)
    else:
        why = ""
        if priority and priority_error(priority):
            raise BoardError(priority_error(priority) or "priority must be high, medium, or low")
        if priority_error(priority):
            priority = ""
    if due:
        try:
            datetime.strptime(due, "%Y-%m-%d")
        except ValueError as exc:
            raise BoardError("due must be YYYY-MM-DD") from exc
    cleaned_links = _clean_links(links)
    items = _clean_approval_items(approval_items)
    if owner == "adam":
        block = ready_error(
            {
                "owner": "adam",
                "status": "open",
                "title": title,
                "instructions": instructions or "",
                "links": cleaned_links,
                "approval_items": items,
            }
        )
        if block:
            raise BoardError(block)
    with BoardLock():
        _sync_locked()
        doc = _load()
        task_id = _alloc_id(doc)
        task = _blank_task(
            task_id,
            title,
            due=due,
            status="open",
            section="Agents" if owner == "agent" else "Now",
            instructions=instructions or "",
            links=cleaned_links,
            approval_items=items,
            source="agent",
            md_id=task_id,
            md_linked=owner == "agent",
            owner=owner,
            why_owner=why,
            priority=priority if owner == "adam" else (priority or ""),
            checked=checked if owner == "adam" else "",
        )
        doc["tasks"].append(task)
        _save(doc)
        _sync_locked()
        if owner == "agent":
            _write_agent_queue(_load())
        return copy.deepcopy(_must(_load(), task_id))


def revise_task(
    task_id: str,
    title: str | None = None,
    instructions: str | None = None,
    why_owner: str | None = None,
    priority: str | None = None,
    checked: str | None = None,
) -> dict:
    """Update an owner task. why_owner is required when the task does not have one yet."""
    why = None
    if why_owner is not None:
        why = re.sub(r"\s+", " ", why_owner).strip()
        error = why_owner_error(why)
        if error:
            raise BoardError(error)
    if priority is not None:
        bad_priority = priority_error(priority)
        if bad_priority:
            raise BoardError(bad_priority)
    cleaned_checked = None
    if checked is not None:
        bad_checked = checked_error(checked)
        if bad_checked:
            raise BoardError(bad_checked)
        cleaned_checked = checked_text(checked)
    with BoardLock():
        _sync_locked()
        doc = _load()
        task = _must(doc, task_id)
        if (task.get("owner") or "adam") == "agent":
            raise BoardError("this task is on the agent queue")
        if why is not None:
            task["owner"] = "adam"
            task["why_owner"] = why
        elif task.get("status") == "open" and not str(task.get("why_owner") or "").strip():
            raise BoardError("open owner task needs why_owner")
        if priority is not None:
            task["priority"] = priority
        elif priority_error(task.get("priority")):
            raise BoardError("owner task needs priority high, medium, or low")
        if cleaned_checked is not None:
            task["checked"] = cleaned_checked
        elif task.get("status") == "open" and checked_error(task.get("checked")):
            raise BoardError("open owner task needs checked: when, how, and what you saw")
        if title:
            task["title"] = re.sub(r"\s+", " ", title).strip()
        text, bom = _read_md()
        if instructions is not None and task.get("source") == "tasks.md":
            # Keep the numbered steps for the phone page. The checklist line stays
            # one short title so a checked box is never rewritten into a paragraph.
            task["instructions"] = instructions.strip()
            task["links"] = extract_links(instructions)
            found_due = parse_due(instructions)
            if found_due:
                task["due"] = found_due
            if not title:
                task["title"] = make_title(instructions)
            task["source"] = "agent"
            if text is not None:
                text = _retitle_agent_line(text, task)
        elif instructions is not None:
            task["instructions"] = instructions.strip()
            task["links"] = extract_links(instructions)
            if text is not None:
                text = _retitle_agent_line(text, task)
        elif title and text is not None and task.get("source") == "agent":
            text = _retitle_agent_line(text, task)
        block = ready_error(task)
        if block:
            raise BoardError(block)
        _save(doc)
        original, _original_bom = _read_md()
        if text is not None and text != original:
            _write_md(text, bom)
        return copy.deepcopy(_must(_load(), task_id))


def set_checked(task_id: str, checked: str) -> dict:
    """Record the check-first note. Works for owner tasks and agent-queue tasks."""
    bad = checked_error(checked)
    if bad:
        raise BoardError(bad)
    text = checked_text(checked)
    with BoardLock():
        _sync_locked()
        doc = _load()
        task = _must(doc, task_id)
        task["checked"] = text
        _save(doc)
        return copy.deepcopy(_must(_load(), task_id))


def move_to_agents(
    task_id: str,
    note: str,
    title: str | None = None,
    instructions: str | None = None,
    noted: bool = False,
) -> dict:
    """Take a task off Adam's phone list. The checkbox in tasks.md is not changed."""
    note = re.sub(r"\s+", " ", (note or "").strip())
    if not note:
        raise BoardError("say why this moved to the agent queue")
    with BoardLock():
        _sync_locked()
        doc = _load()
        task = _must(doc, task_id)
        if task.get("status") == "done":
            raise BoardError("finished tasks stay finished")
        if title:
            task["title"] = re.sub(r"\s+", " ", title).strip()
        if instructions is not None and task.get("source") != "tasks.md":
            task["instructions"] = instructions.strip()
        task["owner"] = "agent"
        task["why_owner"] = ""
        task["section"] = "Agents"
        task["held_from_owner"] = True
        task["held_at"] = now_iso()
        task["fixed_at"] = None
        if noted:
            task["status"] = "noted"
        task.setdefault("notes", []).append({"time": now_iso(), "text": note, "by": "agent"})
        text, bom = _read_md()
        if text is not None:
            if instructions is not None and task.get("source") == "tasks.md":
                one = re.sub(r"\s+", " ", instructions).strip()
                task["instructions"] = one
                task["title"] = make_title(one)
                task["links"] = extract_links(one)
                task["due"] = parse_due(one)
                text = _set_line_body(text, task_id, one)
            elif task.get("source") == "agent":
                text = _retitle_agent_line(text, task)
            text = _relocate_to_agents(text, task_id)
        _save(doc)
        if text is not None:
            _write_md(text, bom)
        _write_agent_queue(_load())
        return copy.deepcopy(_must(_load(), task_id))


def assign_to_adam(
    task_id: str,
    *,
    instructions: str,
    why_owner: str,
    priority: str,
    checked: str,
    approval_items: list[dict] | None = None,
    title: str | None = None,
    due: str | None = None,
) -> dict:
    """Put a task on Adam's list only after the ready gate passes. The checkbox is not changed."""
    why = re.sub(r"\s+", " ", (why_owner or "").strip())
    error = why_owner_error(why)
    if error:
        raise BoardError(error)
    bad_priority = priority_error(priority)
    if bad_priority:
        raise BoardError(bad_priority)
    bad_checked = checked_error(checked)
    if bad_checked:
        raise BoardError(bad_checked)
    if due:
        try:
            datetime.strptime(due, "%Y-%m-%d")
        except ValueError as exc:
            raise BoardError("due must be YYYY-MM-DD") from exc
    items = _clean_approval_items(approval_items or [])
    instructions = (instructions or "").strip()
    draft_title = re.sub(r"\s+", " ", (title or "")).strip() or make_title(instructions)
    block = ready_error(
        {
            "owner": "adam",
            "status": "open",
            "title": draft_title,
            "instructions": instructions,
            "links": extract_links(instructions),
            "approval_items": items,
        }
    )
    if block:
        raise BoardError(block)
    with BoardLock():
        _sync_locked()
        doc = _load()
        task = _must(doc, task_id)
        if task.get("status") == "done":
            raise BoardError("finished tasks stay finished")
        task["owner"] = "adam"
        task["section"] = "Now"
        task["status"] = "open"
        task["held_from_owner"] = False
        task["why_owner"] = why
        task["priority"] = priority
        task["checked"] = checked_text(checked)
        task["instructions"] = instructions
        task["links"] = extract_links(instructions)
        task["approval_items"] = items
        task["source"] = "agent"
        task["title"] = draft_title
        if due:
            task["due"] = due
        else:
            found = parse_due(instructions)
            if found:
                task["due"] = found
        text, bom = _read_md()
        if text is not None:
            text = _relocate_to_now(text, task_id)
            text = _retitle_agent_line(text, task)
            _write_md(text, bom)
        _save(doc)
        _write_agent_queue(_load())
        return copy.deepcopy(_must(_load(), task_id))


def rebuild_agent_queue() -> dict:
    with BoardLock():
        _sync_locked()
        doc = _load()
        _write_agent_queue(doc)
        return copy.deepcopy(_load_queue())


def _load_queue() -> dict:
    path = agent_queue_path()
    if not os.path.isfile(path):
        return {"version": 1, "updated": None, "items": []}
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise BoardError(f"agent-queue.json could not be read ({exc})") from exc
    if not isinstance(data, dict) or not isinstance(data.get("items"), list):
        raise BoardError("agent-queue.json is malformed")
    return data


def list_agent_queue() -> list[dict]:
    with BoardLock():
        if not os.path.isfile(agent_queue_path()):
            _sync_locked()
            _write_agent_queue(_load())
        return copy.deepcopy(_load_queue().get("items") or [])


def add_note(task_id: str, text: str, by: str = "owner", ping: bool = True) -> dict:
    text = (text or "").strip()
    if not text:
        raise BoardError("note is empty")
    if len(text) > 8000:
        text = text[:8000]
    with BoardLock():
        _sync_locked()
        doc = _load()
        task = _must(doc, task_id)
        who = (by or "owner").strip().lower() or "owner"
        waiting = needs_grace(task) or task.get("status") == "blocked"
        task.setdefault("notes", []).append({"time": now_iso(), "text": text, "by": who})
        if not is_agent_task(task) and who.startswith("owner") and task.get("status") in ("open", "blocked"):
            task["status"] = "blocked"
            task["fixed_at"] = None
        elif who.startswith("agent") and waiting and task.get("status") != "done":
            was_blocked = task.get("status") == "blocked"
            if was_blocked:
                task["status"] = "open"
            if task.get("status") == "open":
                task["fixed_at"] = now_iso()
            if was_blocked and task.get("approval_items"):
                _drop_rejected(task)
        _save(doc)
        snapshot = copy.deepcopy(task)
    if ping:
        notify("note", snapshot, note=text, by=by)
    return snapshot


def report_stuck(task_id: str, text: str, files: list[dict] | None = None) -> dict:
    """Adam tapped I'm stuck. Save his note, optional screenshot, and mark the task blocked."""
    text = (text or "").strip()
    if not text:
        raise BoardError("say what happened")
    if len(text) > 8000:
        text = text[:8000]
    stored = []
    with BoardLock():
        _sync_locked()
        doc = _load()
        task = _must(doc, task_id)
        if is_agent_task(task):
            raise BoardError("this task is on the agent queue")
        if task.get("status") == "done":
            raise BoardError("finished tasks stay finished")
        task["status"] = "blocked"
        task["fixed_at"] = None
        task.setdefault("notes", []).append({"time": now_iso(), "text": text, "by": "owner"})
        stamp = now_iso()
        for item in files or []:
            entry = {
                "path": item["path"],
                "name": item["name"],
                "size": int(item["size"]),
                "time": stamp,
            }
            task.setdefault("files", []).append(entry)
            stored.append(entry["path"])
        _save(doc)
        snapshot = copy.deepcopy(task)
    notify("stuck", snapshot, note=text, files=stored, by="owner")
    return snapshot


def reply_task(task_id: str, text: str) -> dict:
    """Agent fixed a stuck task. The note puts it back on his list."""
    return add_note(task_id, text, by="agent", ping=False)


def register_files(task_id: str, files: list[dict]) -> dict:
    if not files:
        raise BoardError("no files")
    with BoardLock():
        _sync_locked()
        doc = _load()
        task = _must(doc, task_id)
        stamp = now_iso()
        stored = []
        for item in files:
            entry = {
                "path": item["path"],
                "name": item["name"],
                "size": int(item["size"]),
                "time": stamp,
            }
            task.setdefault("files", []).append(entry)
            stored.append(entry["path"])
        _save(doc)
        snapshot = copy.deepcopy(task)
    notify("upload", snapshot, note=f"Uploaded {len(stored)} file(s).", files=stored)
    return snapshot


def complete_task(task_id: str, by: str = "owner (board)") -> dict:
    with BoardLock():
        _sync_locked()
        doc = _load()
        task = _must(doc, task_id)
        changed = task.get("status") != "done"
        if changed and task.get("workflow") == "make":
            raise BoardError("tap Ready to post when the file is in")
        if changed and is_review_task(task):
            counts = review_counts(task)
            if counts["answered"] < counts["total"] or counts["changes"]:
                raise BoardError("answer every section first")
        if changed:
            _mark_done(task, by)
            _save(doc)
            _sync_locked()
            task = _must(_load(), task_id)
        snapshot = copy.deepcopy(task)
    if changed:
        notify("complete", snapshot, note="Marked done.", by=by)
    return snapshot


def is_review_task(task: dict) -> bool:
    if task.get("workflow") == "make":
        return False
    return bool(task.get("approval_items"))


MAKE_STEPS = (
    "This is yours to make. The plan is approved. Nothing is generated unless you tap a help button.\n\n"
    "Where: on your phone or this PC, this page.\n\n"
    "1. Make the files described in the plan below.\n"
    "2. If you want starter clips, tap Generate starter clips. If you want a Premiere project, tap Make a Premiere project. "
    "A Premiere project for these batches is an organized folder plus an XML or EDL import. A .prproj is not built for them.\n"
    "3. Upload the finished file on this page, or type its path, then tap Ready to post.\n\n"
    "You should see the task leave your list after Ready to post. Agents then schedule it on the planned dates. Nothing posts before that."
)


HELP_TEXT = {
    "starter_clips": "He asked for starter clips of the assets in this plan. Cut or generate only those.",
    "premiere": (
        "He asked for a Premiere project. A .prproj is not generated for these batches. "
        "Build an organized bin folder plus an XML or EDL import, and say which on this task."
    ),
}


def review_counts(task: dict) -> dict:
    items = task.get("approval_items") or []
    decisions = task.get("approvals") or {}
    good = 0
    changes = 0
    for item in items:
        key = str(item.get("key") or "")
        choice = str((decisions.get(key) or {}).get("decision") or "")
        if choice == "approve":
            good += 1
        elif choice == "reject":
            changes += 1
    total = len(items)
    return {"total": total, "answered": good + changes, "good": good, "changes": changes}


def review_note_text(task: dict) -> str:
    lines = []
    decisions = task.get("approvals") or {}
    for item in task.get("approval_items") or []:
        key = str(item.get("key") or "")
        decision = decisions.get(key) or {}
        if str(decision.get("decision") or "") != "reject":
            continue
        caption = str(item.get("caption") or key).strip()
        comment = str(decision.get("comment") or "").strip()
        lines.append(f"{caption}: {comment}")
    return "\n".join(lines)


def _drop_rejected(task: dict) -> None:
    """A returned review asks again only for the sections that needed changes."""
    approvals = task.setdefault("approvals", {})
    for key in list(approvals):
        if str((approvals.get(key) or {}).get("decision") or "") == "reject":
            approvals.pop(key, None)


def decide(task_id: str, key: str, decision: str, comment: str = "") -> dict:
    decision = (decision or "").strip().lower()
    if decision not in ("approve", "reject"):
        raise BoardError("decision must be approve or reject")
    key = (key or "").strip()
    if not key:
        raise BoardError("approval key is required")
    comment = (comment or "").strip()
    if len(comment) > 2000:
        comment = comment[:2000]
    if decision == "reject" and not comment:
        raise BoardError("say what should change")
    with BoardLock():
        _sync_locked()
        doc = _load()
        task = _must(doc, task_id)
        if task.get("status") in ("done", "blocked") or is_agent_task(task):
            raise BoardError("this review is not waiting for an answer")
        known = [str(item.get("key")) for item in (task.get("approval_items") or [])]
        if known and key not in known:
            raise BoardError("unknown approval item")
        task.setdefault("approvals", {})[key] = {
            "decision": decision,
            "comment": comment,
            "time": now_iso(),
        }
        _save(doc)
        snapshot = copy.deepcopy(task)
    note = f"{decision} {key}."
    if comment:
        note = f"{note} {comment}"
    notify("approval", snapshot, note=note, approvals={key: snapshot["approvals"][key]})
    return snapshot


def submit_review(task_id: str) -> dict:
    """Approve all and finish, or send the change notes to the team. Nothing goes live on a send."""
    action = ""
    with BoardLock():
        _sync_locked()
        doc = _load()
        task = _must(doc, task_id)
        if not is_review_task(task):
            raise BoardError("this task has no sections")
        if task.get("status") == "done":
            raise BoardError("finished tasks stay finished")
        if is_agent_task(task) or task.get("status") == "blocked":
            raise BoardError("this review is not waiting for an answer")
        counts = review_counts(task)
        if counts["answered"] < counts["total"]:
            raise BoardError("answer every section first")
        if counts["changes"] == 0 and task.get("workflow") == "plan":
            title = re.sub(r"\s+", " ", task.get("title") or "").strip()
            if title.startswith("Plan: "):
                task["title"] = "Make: " + title[len("Plan: ") :]
            elif not title.startswith("Make:"):
                task["title"] = "Make: " + title
            task["workflow"] = "make"
            task["status"] = "open"
            existing = task.get("instructions") or ""
            if not existing.startswith("This is yours to make"):
                task["instructions"] = MAKE_STEPS + "\n\n" + existing
            text, bom = _read_md()
            if text is not None:
                _write_md(_retitle_agent_line(text, task), bom)
            _save(doc)
            snapshot = copy.deepcopy(task)
            action = "plan"
        elif counts["changes"] == 0:
            _mark_done(task, "owner (board)")
            _save(doc)
            _sync_locked()
            snapshot = copy.deepcopy(_must(_load(), task_id))
            action = "approved"
        else:
            text = review_note_text(task)
            if not text:
                raise BoardError("say what should change")
            task.setdefault("notes", []).append({"time": now_iso(), "text": text, "by": "owner"})
            task["status"] = "blocked"
            task["fixed_at"] = None
            _save(doc)
            snapshot = copy.deepcopy(task)
            action = "sent"
    if action == "approved":
        notify("complete", snapshot, note="Approved all. Agents publish it.", by="owner (board)")
    elif action == "plan":
        notify(
            "note",
            snapshot,
            note="Plan approved. This is now Make. Nothing is generated unless he taps a help button.",
            by="owner (board)",
        )
    else:
        notify("note", snapshot, note=review_note_text(snapshot), by="owner")
    snapshot["review_action"] = action
    return snapshot


def request_help(task_id: str, kind: str) -> dict:
    """Record a Make-task help tap. Does not take the task off his list."""
    kind = (kind or "").strip()
    if kind not in HELP_TEXT:
        raise BoardError("unknown help")
    with BoardLock():
        _sync_locked()
        doc = _load()
        task = _must(doc, task_id)
        if task.get("workflow") != "make" or (task.get("owner") or "") != "adam":
            raise BoardError("help is only on a Make task")
        if task.get("status") in ("done", "noted"):
            raise BoardError("this task is finished")
        task["help_request"] = kind
        task["help_at"] = now_iso()
        task["status"] = "open"
        _save(doc)
        snapshot = copy.deepcopy(task)
    notify("note", snapshot, note=HELP_TEXT[kind], by="owner (board)")
    return snapshot


def ready_to_post(task_id: str, path: str = "") -> dict:
    """He uploaded the file or named its path. That is approved creative."""
    path = re.sub(r"\s+", " ", (path or "").strip())
    if len(path) > 500:
        path = path[:500]
    with BoardLock():
        _sync_locked()
        doc = _load()
        task = _must(doc, task_id)
        if task.get("workflow") != "make":
            raise BoardError("Ready to post is only on a Make task")
        if task.get("status") == "done":
            return copy.deepcopy(task)
        if not (task.get("files") or []) and not path:
            raise BoardError("add the finished file or its path first")
        if path:
            task["asset_path"] = path
        task["asset_approved"] = True
        _mark_done(task, "owner (board)")
        _save(doc)
        _sync_locked()
        snapshot = copy.deepcopy(_must(_load(), task_id))
    notify(
        "complete",
        snapshot,
        note="Ready to post. Schedule the planned dates. This is approved creative.",
        by="owner (board)",
    )
    return snapshot


def display_path(abs_path: str) -> str:
    abs_path = os.path.abspath(abs_path)
    for base in (os.path.abspath(REPO), os.path.abspath(data_root())):
        try:
            if os.path.commonpath([os.path.normcase(abs_path), os.path.normcase(base)]) == os.path.normcase(base):
                return os.path.relpath(abs_path, base).replace("\\", "/")
        except ValueError:
            continue
    return abs_path.replace("\\", "/")


def safe_filename(name: str) -> str:
    name = os.path.basename((name or "").replace("\\", "/")).replace("\x00", "")
    name = re.sub(r"[^A-Za-z0-9._ -]+", "_", name).strip(" .")
    if not name or name in (".", ".."):
        name = "upload"
    stem, ext = os.path.splitext(name)
    reserved = {"CON", "PRN", "AUX", "NUL"}
    reserved.update({f"COM{i}" for i in range(1, 10)})
    reserved.update({f"LPT{i}" for i in range(1, 10)})
    if stem.upper() in reserved:
        stem = "_" + stem
    if len(stem) > 80:
        stem = stem[:80]
    if len(ext) > 12:
        ext = ext[:12]
    return stem + ext


def task_file_dir(task_id: str) -> str:
    if not re.fullmatch(r"T\d+", task_id or ""):
        raise BoardError("bad task id")
    return os.path.join(task_files_root(), task_id)


def resolve_upload(task_id: str, name: str) -> str | None:
    if not re.fullmatch(r"T\d+", task_id or ""):
        return None
    if not name or "/" in name or "\\" in name or name in (".", ".."):
        return None
    directory = os.path.abspath(task_file_dir(task_id))
    path = os.path.abspath(os.path.join(directory, name))
    try:
        if os.path.commonpath([os.path.normcase(path), os.path.normcase(directory)]) != os.path.normcase(directory):
            return None
    except ValueError:
        return None
    if not os.path.isfile(path):
        return None
    return path


def is_under(path: str, root: str) -> bool:
    path = os.path.normcase(os.path.abspath(path))
    root = os.path.normcase(os.path.abspath(root))
    if path == root:
        return False
    try:
        return os.path.commonpath([path, root]) == root
    except ValueError:
        return False


def resolve_media_path(raw: str) -> str | None:
    if not raw or "\x00" in raw:
        return None
    raw = raw.strip().strip('"')
    drive, rest = os.path.splitdrive(raw)
    if ":" in rest:
        return None
    if not os.path.isabs(raw):
        raw = os.path.join(REPO, raw.replace("/", os.sep))
    real = os.path.realpath(os.path.abspath(raw))
    _drive, real_rest = os.path.splitdrive(real)
    if ":" in real_rest:
        return None
    roots = [os.path.realpath(REPO), os.path.realpath(r"E:\Music")]
    if not any(is_under(real, root) for root in roots):
        return None
    if not os.path.isfile(real):
        return None
    return real


def _read_events() -> list:
    path = events_path()
    if not os.path.isfile(path):
        return []
    rows = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            try:
                item = json.loads(stripped)
            except json.JSONDecodeError:
                rows.append({"_raw": stripped})
                continue
            if isinstance(item, dict):
                rows.append(item)
            else:
                rows.append({"_raw": stripped})
    return rows


def _write_events(rows: list) -> None:
    chunks = []
    for row in rows:
        if "_raw" in row and len(row) == 1:
            chunks.append(row["_raw"])
        else:
            chunks.append(json.dumps(row, ensure_ascii=False))
    payload = ("\n".join(chunks) + ("\n" if chunks else "")).encode("utf-8")
    _atomic_bytes(events_path(), payload)


def _next_event_id(rows: list) -> str:
    number = 0
    for row in rows:
        match = re.fullmatch(r"E(\d+)", str(row.get("event_id") or ""))
        if match:
            number = max(number, int(match.group(1)))
    return f"E{number + 1:04d}"


def _append_event_locked(event: dict) -> None:
    path = events_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    line = json.dumps(event, ensure_ascii=False) + "\n"
    with open(path, "a", encoding="utf-8", newline="\n") as handle:
        handle.write(line)
        handle.flush()
        os.fsync(handle.fileno())


def _set_ping_locked(event_id: str, ok: bool, output: str) -> None:
    rows = _read_events()
    for row in rows:
        if row.get("event_id") == event_id:
            row["ping"] = {"ok": bool(ok), "output": output[:800]}
    _write_events(rows)


def redact(text: str) -> str:
    text = re.sub(r"(?i)(bearer\s+)\S+", r"\1[redacted]", text or "")
    text = re.sub(r"(?i)(key|token|password|secret)=([^\s&]+)", r"\1=[redacted]", text)
    return text


def build_message(event_type: str, task: dict, note: str, files: list[str] | None) -> str:
    files = files or []
    shown = ", ".join(files) if files else "none"
    note = re.sub(r"\s+", " ", (note or "")).strip()
    title = re.sub(r"\s+", " ", (task.get("title") or "")).strip()
    url = task_url(task["id"])

    def pack(note_text: str, file_text: str, title_text: str) -> str:
        return (
            f"BOARD {event_type}: {task['id']} {title_text}. "
            f"Notes: {note_text}. Files: {file_text}. Open {url}"
        )

    message = pack(note, shown, title)
    if len(message) <= 1500:
        return message
    keep_note = note
    while keep_note and len(pack(keep_note, shown, title)) > 1500:
        keep_note = keep_note[: max(0, len(keep_note) - 50)].rstrip()
        if len(keep_note) < 8:
            keep_note = ""
            break
        keep_note = keep_note + "..."
    message = pack(keep_note, shown, title)
    if len(message) > 1500:
        message = pack(keep_note, "truncated", title[:80])
    return message[:1500]


def _ping_worker(event_id: str, message: str) -> None:
    script = os.path.join(REPO, "tools", "ping-owner.ps1")
    run_kwargs = {}
    if sys.platform == "win32":
        # pythonw must not flash a console on the owner's screen.
        run_kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
    try:
        proc = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                script,
                "-Message",
                message,
            ],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO,
            **run_kwargs,
        )
        output = ((proc.stdout or "") + (proc.stderr or "")).strip()
        ok = proc.returncode == 0
    except subprocess.TimeoutExpired:
        ok = False
        output = "timeout"
    except Exception as exc:
        ok = False
        output = str(exc)
    try:
        with BoardLock():
            _set_ping_locked(event_id, ok, redact(output)[:800])
    except Exception as exc:
        log_line(f"could not record ping result {event_id}: {exc}")


def notify(
    event_type: str,
    task: dict,
    note: str = "",
    files: list[str] | None = None,
    approvals=None,
    by: str = "",
) -> str:
    message = build_message(event_type, task, note, files)
    with BoardLock():
        rows = _read_events()
        event_id = _next_event_id(rows)
        event = {
            "event_id": event_id,
            "time": now_iso(),
            "type": event_type,
            "task_id": task.get("id"),
            "title": task.get("title"),
            "note": note or "",
            "files": list(files or []),
            "approvals": approvals,
            "by": by or "",
            "ping": {"ok": None, "output": "pending"},
            "acked_by": None,
        }
        _append_event_locked(event)
        if os.environ.get("GC_BOARD_NO_PING") == "1":
            _set_ping_locked(event_id, False, "skipped (GC_BOARD_NO_PING=1)")
            return event_id
    threading.Thread(target=_ping_worker, args=(event_id, message), daemon=True).start()
    return event_id


def list_events(unacked_only: bool = False) -> list[dict]:
    with BoardLock():
        rows = [row for row in _read_events() if "event_id" in row]
    if unacked_only:
        rows = [row for row in rows if not row.get("acked_by")]
    return rows


def ack_event(event_id: str, by: str, action: str) -> dict:
    by = (by or "").strip()
    action = (action or "").strip()
    if not by or not action:
        raise BoardError("ack needs a name and an action")
    with BoardLock():
        rows = _read_events()
        found = None
        for row in rows:
            if row.get("event_id") == event_id:
                row["acked_by"] = by
                row["acked_at"] = now_iso()
                row["ack_action"] = action
                found = row
                break
        if found is None:
            raise BoardError(f"no event {event_id}")
        _write_events(rows)
        return copy.deepcopy(found)


def schedule_records(data, today=None, days: int = 21) -> list[dict]:
    today = today or today_mt()
    end = today + timedelta(days=days)
    rows = []
    for item in _extract_schedule(data):
        day = _schedule_day(item)
        if day is None or day < today or day >= end:
            continue
        approval = item.get("approval_needed", item.get("needs_approval"))
        rows.append(
            {
                "date": day.isoformat(),
                "platform": str(_pick(item, "platform", "network", "where") or ""),
                "title": str(_pick(item, "title", "name", "text", "caption") or ""),
                "status": str(_pick(item, "status", "state") or ""),
                "approval_needed": approval,
            }
        )
    rows.sort(key=lambda row: (row["date"], row["platform"], row["title"]))
    return rows


def load_schedule():
    path = os.path.join(REPO, "social", "schedule.json")
    if not os.path.isfile(path):
        return None, "missing"
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"malformed: {exc.__class__.__name__}"
    try:
        return schedule_records(data), None
    except Exception as exc:
        return None, f"malformed: {exc.__class__.__name__}"


def _pick(item: dict, *keys):
    for key in keys:
        value = item.get(key)
        if value not in (None, ""):
            return value
    return ""


def _extract_schedule(data) -> list[dict]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if not isinstance(data, dict):
        return []
    for key in ("items", "posts", "schedule", "events", "entries"):
        value = data.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    days = data.get("days")
    rows = []
    if isinstance(days, dict):
        for day, value in days.items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        row = dict(item)
                        row.setdefault("date", day)
                        rows.append(row)
            elif isinstance(value, dict):
                row = dict(value)
                row.setdefault("date", day)
                rows.append(row)
    return rows


def _schedule_day(item: dict):
    raw = _pick(item, "date", "day", "when", "on")
    if not raw:
        return None
    text = str(raw).strip()
    try:
        return datetime.strptime(text[:10], "%Y-%m-%d").date()
    except ValueError:
        return None
