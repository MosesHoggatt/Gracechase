"""Shared schedule, time, and safety helpers for the posting runner.

Nothing in this module sends a post. Network uploads check require_live().
"""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import winreg
from datetime import datetime, timedelta, timezone
from decimal import Decimal

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

NETWORK_POSTS = False
THUMB_MAX = 50 * 1024 * 1024
MISSED_AFTER = timedelta(hours=6)
MIN_SCHEDULE_LEAD = timedelta(minutes=15)
MAX_SCHEDULE_LEAD = timedelta(days=29)

PLATFORMS = {
    "youtube",
    "youtube_short",
    "youtube_community",
    "facebook",
    "facebook_reel",
    "instagram_feed",
    "instagram_reel",
    "instagram_story",
    "threads",
    "x",
    "tiktok",
    "pinterest",
    "spotify",
    "website",
    "ads_meta",
    "ads_google",
    "release",
    "deadline",
    "review",
}
TYPES = {
    "post",
    "short",
    "reel",
    "story",
    "community",
    "carousel",
    "ad",
    "release",
    "deadline",
    "review",
    "approval_batch",
}
STATUSES = {
    "planned",
    "needs_asset",
    "needs_approval",
    "ready",
    "scheduled_external",
    "posted",
    "skipped",
    "missed",
    "on_hold",
    "needs_check",
    "done",
    "waiting_on_asset",
}
ACTS = {"gracechase", "sackbuts"}
TERMINAL = {"posted", "skipped", "missed", "done", "scheduled_external", "on_hold"}
AUTOMATED = {
    "youtube",
    "youtube_short",
    "facebook",
    "facebook_reel",
    "instagram_feed",
    "instagram_reel",
    "instagram_story",
    "threads",
    "x",
    "tiktok",
}
SCHEDULABLE = {"youtube", "youtube_short", "facebook", "facebook_reel"}
LINK_IN_TEXT = {"facebook", "facebook_reel", "x", "threads", "youtube", "youtube_short"}
NEEDS_VIDEO = {"youtube", "youtube_short", "facebook_reel", "instagram_reel", "tiktok"}
MANUAL_REASON = {
    "youtube_community": "YouTube Community has no write in the Data API",
    "pinterest": "Pinterest has no posting API in this runner",
    "spotify": "Spotify for Artists is not posted from this runner",
    "ads_meta": "ads stay off; this runner never creates or pays for an ad",
    "ads_google": "ads stay off; this runner never creates or pays for an ad",
    "website": "deploy the site only after the owner approves the preview on the board",
    "release": "release reminder, not a social post",
    "deadline": "deadline reminder, not a social post",
    "review": "review reminder, not a social post",
}
REMIND_TYPES = {"ad", "release", "deadline", "review", "approval_batch"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm"}
PLACEHOLDER = "[YOUTUBE URL]"
SECRET_NAMES = (
    "YOUTUBE_CLIENT_ID",
    "YOUTUBE_CLIENT_SECRET",
    "YOUTUBE_REFRESH_TOKEN",
    "SACKBUTS_YOUTUBE_CLIENT_ID",
    "SACKBUTS_YOUTUBE_CLIENT_SECRET",
    "SACKBUTS_YOUTUBE_REFRESH_TOKEN",
    "META_PAGE_ID",
    "META_PAGE_ACCESS_TOKEN",
    "IG_USER_ID",
    "THREADS_APP_ID",
    "THREADS_APP_SECRET",
    "THREADS_USER_ID",
    "THREADS_ACCESS_TOKEN",
    "X_API_KEY",
    "X_API_SECRET",
    "X_ACCESS_TOKEN",
    "X_ACCESS_TOKEN_SECRET",
    "TIKTOK_CLIENT_KEY",
    "TIKTOK_CLIENT_SECRET",
    "TIKTOK_ACCESS_TOKEN",
)
USER_ENV = r"Environment"
URL_RE = re.compile(r"https?://[^\s]+")
HASHTAG_RE = re.compile(r"(?<!\w)#(\w+)", re.UNICODE)
TRAIL = ".,;:!?)]}>\"'"
_ZONE = None
_ZONE_FAILED = False


class PostingError(RuntimeError):
    pass


class PermanentError(PostingError):
    """A post that will not succeed until the schedule entry changes."""


class TransientError(PostingError):
    """A post that can be tried again on a later run."""


def require_live() -> None:
    if not NETWORK_POSTS:
        raise PostingError("refusing to send because this run is not live")


def redact(text: str, extra: tuple[str, ...] = ()) -> str:
    cleaned = text or ""
    values = [value for value in extra if value]
    for name in SECRET_NAMES:
        value = os.environ.get(name) or ""
        if len(value) >= 8:
            values.append(value)
    for value in sorted(set(values), key=len, reverse=True):
        cleaned = cleaned.replace(value, "[redacted]")
    cleaned = re.sub(r"(access_token=)[^&\s\"']+", r"\1[redacted]", cleaned, flags=re.I)
    cleaned = re.sub(r"(refresh_token=)[^&\s\"']+", r"\1[redacted]", cleaned, flags=re.I)
    cleaned = re.sub(r"(client_secret=)[^&\s\"']+", r"\1[redacted]", cleaned, flags=re.I)
    cleaned = re.sub(r"(upload_id=)[^&\s\"']+", r"\1[redacted]", cleaned, flags=re.I)
    cleaned = re.sub(
        r"https://www\.googleapis\.com/upload/\S+",
        "https://www.googleapis.com/upload/[redacted]",
        cleaned,
    )
    cleaned = re.sub(r"Bearer\s+\S+", "Bearer [redacted]", cleaned)
    cleaned = re.sub(r"\bOAuth\s+[A-Za-z0-9%._~+/=-]{8,}", "OAuth [redacted]", cleaned)
    return cleaned


def env_value(name: str) -> str:
    return (os.environ.get(name) or "").strip()


def load_user_env() -> None:
    """Copy Windows user variables into this process. Never prints a value."""
    if os.name != "nt":
        return
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, USER_ENV, 0, winreg.KEY_READ)
    except OSError:
        return
    with key:
        for name in SECRET_NAMES:
            if env_value(name):
                continue
            try:
                value, kind = winreg.QueryValueEx(key, name)
            except FileNotFoundError:
                continue
            if not isinstance(value, str):
                continue
            if kind == winreg.REG_EXPAND_SZ:
                value = os.path.expandvars(value)
            value = value.strip()
            if value:
                os.environ[name] = value


def paths() -> dict[str, str]:
    social = os.path.join(ROOT, "social")
    return {
        "schedule": os.environ.get("GC_SCHEDULE_PATH") or os.path.join(social, "schedule.json"),
        "enabled": os.environ.get("GC_ENABLED_PATH") or os.path.join(social, "posting-enabled.json"),
        "paused": os.environ.get("GC_PAUSED_PATH") or os.path.join(social, "posting-paused.json"),
        "limits": os.environ.get("GC_LIMITS_PATH") or os.path.join(social, "posting-limits.json"),
        "log": os.environ.get("GC_POST_LOG") or os.path.join(social, "post-log.jsonl"),
        "dry_log": os.environ.get("GC_DRY_LOG") or os.path.join(social, "post-log-dryrun.jsonl"),
        "receipts": os.environ.get("GC_RECEIPT_LOG") or os.path.join(social, "post-receipts.jsonl"),
        "lock": os.environ.get("GC_LOCK_PATH") or os.path.join(social, ".post-due.lock"),
    }


def read_flag(path: str, field: str) -> bool | None:
    """True or False for a boolean field. None when the file is missing."""
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8-sig") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or field not in data or not isinstance(data[field], bool):
        raise PostingError(f"{path} must contain a boolean {field}")
    return data[field]


def is_paused(path: str) -> bool:
    try:
        flag = read_flag(path, "paused")
    except (OSError, json.JSONDecodeError, PostingError) as exc:
        raise PostingError(f"pause file could not be read, so nothing will be sent: {exc}") from None
    return flag is True


def is_enabled(path: str) -> bool:
    try:
        flag = read_flag(path, "enabled")
    except (OSError, json.JSONDecodeError, PostingError):
        return False
    return flag is True


def nth_sunday(year: int, month: int, n: int) -> int:
    first = datetime(year, month, 1)
    delta = (6 - first.weekday()) % 7
    return 1 + delta + (n - 1) * 7


def denver_offset_fallback(moment: datetime) -> timedelta:
    """US Mountain Time. Second Sunday in March through first Sunday in November is UTC-6."""
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    utc = moment.astimezone(timezone.utc)
    start = datetime(utc.year, 3, nth_sunday(utc.year, 3, 2), 9, tzinfo=timezone.utc)
    end = datetime(utc.year, 11, nth_sunday(utc.year, 11, 1), 8, tzinfo=timezone.utc)
    if start <= utc < end:
        return timedelta(hours=-6)
    return timedelta(hours=-7)


def denver_zone():
    global _ZONE, _ZONE_FAILED
    if _ZONE_FAILED:
        return None
    if _ZONE is not None:
        return _ZONE
    try:
        from zoneinfo import ZoneInfo

        _ZONE = ZoneInfo("America/Denver")
        return _ZONE
    except Exception:
        _ZONE_FAILED = True
        return None


def denver_offset(moment: datetime) -> timedelta:
    zone = denver_zone()
    if zone is not None:
        if moment.tzinfo is None:
            moment = moment.replace(tzinfo=timezone.utc)
        offset = moment.astimezone(timezone.utc).astimezone(zone).utcoffset()
        if offset is not None:
            return offset
    return denver_offset_fallback(moment)


def parse_dt(value: str) -> datetime:
    text = (value or "").strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise ValueError("datetime needs a numeric offset")
    return parsed


def now() -> datetime:
    override = (os.environ.get("GC_NOW") or "").strip()
    if override:
        return parse_dt(override)
    return datetime.now(timezone.utc).astimezone(timezone(denver_offset(datetime.now(timezone.utc))))


def iso_denver(moment: datetime) -> str:
    offset = denver_offset(moment)
    return moment.astimezone(timezone(offset)).isoformat(timespec="seconds")


def month_key(moment: datetime) -> str:
    local = moment.astimezone(timezone(denver_offset(moment)))
    return f"{local.year:04d}-{local.month:02d}"


def money(value) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.001"))


def source(entry: dict) -> dict:
    value = entry.get("content_source") or {}
    return value if isinstance(value, dict) else {}


def is_remote(path: str) -> bool:
    return path.startswith("https://") or path.startswith("http://")


def resolve_path(path: str) -> str:
    if is_remote(path):
        return path
    if os.path.isabs(path):
        return path
    return os.path.normpath(os.path.join(ROOT, path))


def media_paths(entry: dict) -> list[str]:
    raw = source(entry).get("media") or []
    if isinstance(raw, str):
        raw = [raw]
    paths = []
    for item in raw:
        if item is None or item == "":
            continue
        paths.append(resolve_path(str(item)))
    return paths


def thumbnail_path(entry: dict) -> str | None:
    raw = source(entry).get("thumbnail")
    if not raw:
        return None
    return resolve_path(str(raw))


def file_size(path: str) -> int | None:
    if is_remote(path):
        return None
    try:
        return os.path.getsize(path)
    except OSError:
        return None


def file_exists(path: str) -> bool:
    if path.startswith("https://"):
        return True
    if path.startswith("http://"):
        return False
    return os.path.isfile(path)


def extension(path: str) -> str:
    if is_remote(path):
        import urllib.parse

        path = urllib.parse.urlparse(path).path
    return os.path.splitext(path)[1].lower()


def media_kind(path: str) -> str:
    ext = extension(path)
    if ext in VIDEO_EXT:
        return "video"
    if ext in IMAGE_EXT:
        return "image"
    return "file"


def final_text(entry: dict) -> str:
    caption = entry.get("caption") or ""
    if not isinstance(caption, str):
        caption = str(caption)
    link = str(source(entry).get("link") or "").strip()
    if link and PLACEHOLDER in caption:
        caption = caption.replace(PLACEHOLDER, link)
    platform = entry.get("platform")
    if link and platform in LINK_IN_TEXT and link not in caption:
        caption = caption.rstrip() + "\n\n" + link
    return caption


def x_length(text: str) -> int:
    """X length, counting each http(s) URL as 23 characters."""
    total = 0
    pos = 0
    for match in URL_RE.finditer(text):
        end = match.end()
        while end > match.start() and text[end - 1] in TRAIL:
            end -= 1
        total += match.start() - pos
        total += 23
        total += match.end() - end
        pos = match.end()
    total += len(text) - pos
    return total


def hashtags(text: str) -> list[str]:
    return HASHTAG_RE.findall(text)


def contains_link(text: str) -> bool:
    return URL_RE.search(text) is not None


def show_path(path: str) -> str:
    if any(ch.isspace() for ch in path):
        return '"' + path.replace('"', "'") + '"'
    return path


def describe_files(paths: list[str]) -> list[dict]:
    rows = []
    for path in paths:
        rows.append({"path": path, "bytes": file_size(path)})
    return rows


def load_json(path: str):
    with open(path, encoding="utf-8-sig") as handle:
        return json.load(handle)


def load_schedule(path: str):
    if not os.path.isfile(path):
        return None, "not found"
    try:
        data = load_json(path)
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON ({exc})"
    except OSError as exc:
        return None, str(exc)
    if not isinstance(data, dict):
        return None, "schedule must be a JSON object"
    return data, None


def atomic_write_json(path: str, data) -> None:
    directory = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".schedule-", suffix=".tmp", dir=directory)
    tmp_kept = tmp
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
        tmp_kept = ""
    finally:
        if tmp_kept:
            try:
                os.remove(tmp_kept)
            except OSError:
                pass


def patch_entry(path: str, entry_id: str, fields: dict) -> None:
    """Re-read the schedule and change one entry. Other entries stay as they are on disk."""
    data, err = load_schedule(path)
    if data is None:
        raise PostingError(f"could not update the schedule: {err}")
    entries = data.get("entries")
    if not isinstance(entries, list):
        raise PostingError("schedule entries is not a list")
    found = False
    for entry in entries:
        if isinstance(entry, dict) and entry.get("id") == entry_id:
            for key, value in fields.items():
                if key == "result" and isinstance(entry.get("result"), dict) and isinstance(value, dict):
                    merged = dict(entry["result"])
                    merged.update(value)
                    entry["result"] = merged
                else:
                    entry[key] = value
            found = True
            break
    if not found:
        raise PostingError(f"entry {entry_id} disappeared from the schedule before it could be updated")
    atomic_write_json(path, data)


def append_jsonl(path: str, record: dict) -> None:
    directory = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(directory, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
    with open(path, "a", encoding="utf-8", newline="\n") as handle:
        handle.write(line)
        handle.flush()
        os.fsync(handle.fileno())


def load_jsonl(path: str) -> list[dict]:
    if not os.path.isfile(path):
        return []
    rows = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            text = line.strip()
            if not text:
                continue
            try:
                row = json.loads(text)
            except json.JSONDecodeError:
                continue
            if isinstance(row, dict):
                rows.append(row)
    return rows


def configure_stdio() -> None:
    """Make print safe. pythonw.exe has no console, and sys.stdout is None there."""
    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w", encoding="utf-8", errors="replace")
    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w", encoding="utf-8", errors="replace")
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def approval_ok(entry: dict) -> tuple[bool, str]:
    if "approval_needed" not in entry:
        return False, "approval_needed is missing"
    if entry.get("approval_needed") is False:
        return True, ""
    if entry.get("approval_needed") is not True:
        return False, "approval_needed must be true or false"
    approved = entry.get("approved")
    if not isinstance(approved, dict):
        return False, "approval needed"
    if not str(approved.get("by") or "").strip() or not str(approved.get("date") or "").strip():
        return False, "approval needed"
    return True, ""


def dependency_block(entry: dict, by_id: dict) -> str:
    deps = entry.get("depends_on") or []
    if not isinstance(deps, list):
        return "depends_on must be a list"
    for dep in deps:
        other = by_id.get(dep)
        if not isinstance(other, dict):
            return f"missing dependency {dep}"
        if other.get("status") not in {"posted", "done", "skipped", "scheduled_external"}:
            return f"dependency {dep} is {other.get('status')}"
    return ""


def block_reason(entry: dict) -> str:
    """Why this entry must not be sent automatically. Empty when it may be sent."""
    platform = entry.get("platform")
    kind = entry.get("type")
    act = entry.get("act")
    if kind in REMIND_TYPES or platform in MANUAL_REASON:
        if platform in MANUAL_REASON:
            return MANUAL_REASON[platform]
        if kind == "ad":
            return "ads stay off; this runner never creates or pays for an ad"
        return MANUAL_REASON.get(kind, "not a social post")
    if act == "sackbuts" and platform in {
        "facebook",
        "facebook_reel",
        "instagram_feed",
        "instagram_reel",
        "instagram_story",
        "threads",
        "x",
        "tiktok",
    }:
        return "no Sackbuts account on this platform. A Gracechase cross-post uses act=gracechase"
    if platform == "tiktok" and not env_value("TIKTOK_ACCESS_TOKEN"):
        return (
            "TIKTOK_ACCESS_TOKEN is not set. Public TikTok posts are an agent browser job "
            "when the screen is allowed. The unaudited app can only publish a private post. "
            "Not an owner phone task."
        )
    if platform in {"youtube", "youtube_short"} and act == "sackbuts":
        names = (
            "SACKBUTS_YOUTUBE_CLIENT_ID",
            "SACKBUTS_YOUTUBE_CLIENT_SECRET",
            "SACKBUTS_YOUTUBE_REFRESH_TOKEN",
        )
        if not all(env_value(name) for name in names):
            return (
                "Sackbuts YouTube needs SACKBUTS_YOUTUBE_CLIENT_ID, "
                "SACKBUTS_YOUTUBE_CLIENT_SECRET, and SACKBUTS_YOUTUBE_REFRESH_TOKEN. "
                "The Gracechase token is not used"
            )
    if platform not in AUTOMATED:
        return "no posting API in this runner"
    return ""


def postable_reason(entry: dict, by_id: dict) -> str:
    """Empty when a ready entry may be sent. The reason is why it is held."""
    if entry.get("status") != "ready":
        return f"status is {entry.get('status')}"
    ok, why = approval_ok(entry)
    if not ok:
        return why
    text = final_text(entry).strip()
    if not text:
        return "caption is empty"
    problems = limit_problems(entry, ready_only=True)
    if problems:
        return problems[0]
    dep = dependency_block(entry, by_id)
    if dep:
        return dep
    paths = media_paths(entry)
    for path in paths:
        if not file_exists(path):
            return f"missing media {path}"
    platform = entry.get("platform")
    if platform in NEEDS_VIDEO and not any(media_kind(path) == "video" for path in paths):
        return "a video file is required"
    if platform == "instagram_feed" and not paths:
        return "an image file is required"
    if platform == "instagram_story" and not paths:
        return "a story image or video is required"
    if platform in {"youtube", "youtube_short"}:
        thumb = thumbnail_path(entry)
        if not thumb or not file_exists(thumb):
            return "a thumbnail file is required"
        if thumb and not is_remote(thumb):
            size = file_size(thumb)
            if size is not None and size > THUMB_MAX:
                return f"thumbnail is {size} bytes, over 50 MiB. It was not resized"
            if extension(thumb) not in {".jpg", ".jpeg", ".png"}:
                return "thumbnail must be jpeg or png. It was not converted"
    if platform == "threads" and any(media_kind(path) == "video" and not path.startswith("https://") for path in paths):
        public = str(source(entry).get("public_url") or "")
        if not public.startswith("https://"):
            return "Threads cannot upload a local video. Set content_source.public_url to https"
    return ""


def limit_problems(entry: dict, ready_only: bool = False) -> list[str]:
    platform = entry.get("platform")
    text = final_text(entry)
    title = entry.get("title") or ""
    if not isinstance(title, str):
        title = str(title)
    problems = []
    if platform in {"youtube", "youtube_short"}:
        if ready_only or title or entry.get("status") == "ready":
            if entry.get("status") == "ready" and not title.strip():
                problems.append("YouTube title is empty")
            if len(title) > 100:
                problems.append(f"YouTube title is {len(title)} characters. The limit is 100")
            if "\n" in title or "\r" in title:
                problems.append("YouTube title cannot contain a line break")
        if len(text) > 5000:
            problems.append(f"YouTube description is {len(text)} characters. The limit is 5000")
        tags = source(entry).get("tags") or []
        if isinstance(tags, str):
            tags = [part.strip() for part in tags.split(",") if part.strip()]
        if isinstance(tags, list) and tags:
            joined = ",".join(str(tag) for tag in tags)
            if len(joined) > 500:
                problems.append(f"YouTube tags are {len(joined)} characters. The limit is 500")
    if platform in {"instagram_feed", "instagram_reel", "instagram_story"} and text:
        if len(text) > 2200:
            problems.append(f"Instagram caption is {len(text)} characters. The limit is 2200")
        tags = hashtags(text)
        if len(tags) > 30:
            problems.append(f"Instagram caption has {len(tags)} hashtags. The limit is 30")
    if platform == "threads" and len(text) > 500:
        problems.append(f"Threads text is {len(text)} characters. The limit is 500")
    if platform == "tiktok" and len(text) > 2200:
        problems.append(f"TikTok caption is {len(text)} characters. The limit is 2200")
    if platform == "x" and text:
        length = x_length(text)
        if length > 280:
            problems.append(f"X text counts as {length}. The limit is 280, and each link counts as 23")
    return problems


def can_schedule(entry: dict) -> bool:
    return entry.get("platform") in SCHEDULABLE and not block_reason(entry)


def video_mime(path: str) -> str:
    return {
        ".mp4": "video/mp4",
        ".m4v": "video/mp4",
        ".mov": "video/quicktime",
        ".webm": "video/webm",
    }.get(extension(path), "video/mp4")


def image_mime(path: str) -> str:
    ext = extension(path)
    if ext in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if ext == ".png":
        return "image/png"
    raise PermanentError(f"image must be jpeg or png, not {ext or 'that type'}. The file was not converted")
