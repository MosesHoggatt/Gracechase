"""Post schedule entries that are due.

Default mode is a dry run. It prints what would be sent and appends one line to the
dry-run log. It does not call a posting API. A dry run changes the schedule only to
set needs_check when an attempt has no success receipt.

A real post requires --live and social/posting-enabled.json containing {"enabled": true}.
social/posting-paused.json containing {"paused": true} stops the run before anything is sent.
"""

from __future__ import annotations

import argparse
import os
import secrets
import sys
from datetime import timedelta

TOOLS = os.path.dirname(os.path.abspath(__file__))
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

from posting import facebook, instagram, tiktok, youtube
from posting import common
from posting import threads as threads_api
from posting import x as x_api

MANUAL_REMINDER = timedelta(days=7)
CHECK_ERROR = "attempt without receipt; verify on the platform before retrying"
# Already handed to another scheduler. Never send these, and never mark them missed.
OWNED_OUTSIDE = {
    "2026-11-05-ig-reel-ain-adclip": (
        "Gracechase-IG-Reel-All-I-Need publishes this Reel. This runner does not."
    ),
    "2026-11-05-yt-short-ain-adclip": (
        "YouTube Short Ws_LanSqp3U is already scheduled. This runner does not upload it again."
    ),
    "2026-11-05-fb-reel-ain-adclip": (
        "Facebook Reel 1150288730782473 is already scheduled. This runner does not upload it again."
    ),
}


def _is_attempt(row: dict) -> bool:
    if row.get("kind") == "success":
        return False
    return row.get("kind") == "attempt" or bool(row.get("attempt_id"))


def _is_success(row: dict) -> bool:
    if _is_attempt(row):
        return False
    if row.get("kind") == "success":
        return True
    return bool(row.get("post_id") or row.get("status") in {"posted", "scheduled_external"})


def receipt_index(rows: list[dict]) -> dict:
    found: dict = {}
    for row in rows:
        ident = row.get("id")
        if not ident:
            continue
        slot = found.setdefault(ident, {"success": None, "attempts": []})
        if _is_success(row):
            slot["success"] = row
        elif _is_attempt(row):
            slot["attempts"].append(row)
    return found


def blocking_attempt(entry: dict, slot: dict | None) -> str | None:
    """Attempt id that must not be sent again. None when a send is allowed."""
    if not slot or slot.get("success") or not slot.get("attempts"):
        return None
    status = entry.get("status")
    if status not in {"ready", "needs_check"}:
        return None
    attempt_id = str(slot["attempts"][-1].get("attempt_id") or "")
    if not attempt_id:
        return "unknown"
    result = entry.get("result") if isinstance(entry.get("result"), dict) else {}
    if status == "ready" and str(result.get("attempt_id") or "") == attempt_id:
        return None
    return attempt_id


def _endpoint(entry: dict, scheduled: bool) -> str:
    platform = entry.get("platform")
    if platform in {"youtube", "youtube_short"}:
        return youtube.UPLOAD_ENDPOINT
    if platform in {"facebook", "facebook_reel"}:
        return facebook.endpoint(entry, scheduled)
    if str(platform).startswith("instagram"):
        return instagram.endpoint(entry)
    if platform == "threads":
        return threads_api.endpoint(entry)
    if platform == "x":
        return x_api.endpoint(entry)
    if platform == "tiktok":
        return tiktok.endpoint(entry)
    return ""


def _extras(entry: dict, publish_at: str | None, cost, spent) -> list[tuple[str, str]]:
    platform = entry.get("platform")
    items: list[tuple[str, str]] = []
    if platform in {"youtube", "youtube_short"}:
        items.append(("privacy", "private" if publish_at else _youtube_privacy(entry)))
        items.append(("synthetic", "true"))
        items.append(("made_for_kids", "false"))
        items.append(("category", "10"))
        if publish_at:
            items.append(("publish_at", publish_at))
        videos = [path for path in common.media_paths(entry) if common.media_kind(path) == "video"]
        facts = youtube.probe_video(videos[0]) if videos and not common.is_remote(videos[0]) else None
        if facts:
            items.append(("video", f"{facts['width']}x{facts['height']}"))
            items.append(("duration_s", f"{facts['duration']:.1f}"))
        elif platform == "youtube_short":
            items.append(("video", "unverified"))
    elif platform in {"facebook", "facebook_reel"}:
        if publish_at:
            when = common.parse_dt(publish_at)
            items.append(("published", "false"))
            items.append(("scheduled_publish_time", str(int(when.timestamp()))))
            if platform == "facebook_reel":
                items.append(("video_state", "SCHEDULED"))
        elif platform == "facebook_reel":
            items.append(("video_state", "PUBLISHED"))
        else:
            items.append(("published", "true"))
    elif platform == "x" and cost is not None:
        items.append(("estimated_cost_usd", format(cost, "f")))
        if spent is not None:
            items.append(("month_total_usd", format(spent, "f")))
    elif platform == "tiktok":
        items.append(("privacy", "SELF_ONLY"))
        items.append(("is_aigc", "true"))
    elif platform == "instagram_story":
        items.append(("story_caption", "not_sent"))
        items.append(("link_sticker", "not_available"))
    return items


def _youtube_privacy(entry: dict) -> str:
    requested = str(common.source(entry).get("privacy") or "").lower()
    if requested in {"public", "unlisted", "private"}:
        return requested
    return "public"


def _dry_line(entry: dict, endpoint: str, extras: list[tuple[str, str]], action: str) -> str:
    bits = [
        "DRY RUN",
        f"action={action}",
        f"id={entry.get('id')}",
        f"platform={entry.get('platform')}",
        f"endpoint={endpoint}",
        f"caption_len={len(common.final_text(entry))}",
    ]
    media = common.describe_files(common.media_paths(entry))
    if not media:
        bits.append("media=none")
    for item in media:
        bits.append("media=" + common.show_path(item["path"]))
        bits.append("bytes=" + ("unknown" if item["bytes"] is None else str(item["bytes"])))
    thumb = common.thumbnail_path(entry)
    if thumb:
        size = common.file_size(thumb)
        bits.append("thumbnail=" + common.show_path(thumb))
        bits.append("bytes=" + ("unknown" if size is None else str(size)))
    for key, value in extras:
        bits.append(f"{key}={value}")
    return " ".join(bits)


def _title(entry: dict) -> str:
    title = str(entry.get("title") or "").replace("\n", " ").strip()
    if len(title) > 80:
        return title[:77] + "..."
    return title


class RunLock:
    def __init__(self, path: str):
        self.path = path
        self.fd = None

    def __enter__(self):
        directory = os.path.dirname(os.path.abspath(self.path)) or "."
        os.makedirs(directory, exist_ok=True)
        for attempt in range(2):
            try:
                self.fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                os.write(self.fd, str(os.getpid()).encode("ascii"))
                return self
            except FileExistsError:
                if attempt == 0 and _steal_lock(self.path):
                    continue
                raise common.PostingError(f"another post_due run holds the lock ({os.path.basename(self.path)})")
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None
        try:
            os.remove(self.path)
        except OSError:
            pass
        return False


def _steal_lock(path: str) -> bool:
    try:
        age = __import__("time").time() - os.path.getmtime(path)
    except OSError:
        return True
    pid = 0
    try:
        with open(path, encoding="utf-8") as handle:
            pid = int((handle.read() or "0").strip() or "0")
    except (OSError, ValueError):
        pid = 0
    alive = False
    if pid > 0:
        try:
            os.kill(pid, 0)
            alive = True
        except OSError:
            alive = False
    if alive and age < 3 * 3600:
        return False
    try:
        os.remove(path)
    except OSError:
        return False
    return True


def _dep_state(entry: dict, by_id: dict) -> str:
    deps = entry.get("depends_on") or []
    if not isinstance(deps, list):
        return "missing"
    for dep in deps:
        other = by_id.get(dep)
        if not isinstance(other, dict):
            return "missing"
        status = other.get("status")
        if status in {"posted", "done", "skipped", "scheduled_external"}:
            continue
        if status in common.TERMINAL:
            return "blocked"
        return "later"
    return "ok"


def _dispatch(entry: dict, publish_at: str | None) -> dict:
    platform = entry.get("platform")
    if platform in {"youtube", "youtube_short"}:
        return youtube.upload_video(entry, publish_at)
    if platform in {"facebook", "facebook_reel"}:
        unix = int(common.parse_dt(publish_at).timestamp()) if publish_at else None
        return facebook.publish(entry, unix)
    if str(platform).startswith("instagram"):
        return instagram.publish(entry)
    if platform == "threads":
        return threads_api.publish(entry)
    if platform == "x":
        return x_api.publish(entry)
    if platform == "tiktok":
        return tiktok.publish(entry)
    raise common.PermanentError(f"{platform} has no posting adapter")


def run_posts(args) -> int:
    cfg = common.paths()
    try:
        paused = common.is_paused(cfg["paused"])
    except common.PostingError as exc:
        print(common.redact(str(exc)))
        return 2
    if paused:
        print(f"PAUSED {cfg['paused']}. Nothing sent.")
        return 0
    enabled = common.is_enabled(cfg["enabled"])
    if args.live and not enabled:
        print(
            "NOT ENABLED. "
            f"{cfg['enabled']} must contain {{\"enabled\": true}}. Nothing sent."
        )
        return 2
    live = bool(args.live) and enabled
    data, err = common.load_schedule(cfg["schedule"])
    if data is None:
        if err == "not found":
            print(f"No schedule at {cfg['schedule']}. Nothing due.")
            return 0
        print(f"Schedule not readable: {err}")
        return 1
    if data.get("version") != 1:
        print("Schedule version is not 1. Nothing sent.")
        return 1
    if data.get("timezone") not in (None, "America/Denver"):
        print("Schedule timezone must be America/Denver. Nothing sent.")
        return 1
    entries = data.get("entries")
    if not isinstance(entries, list):
        print("Schedule entries is not a list. Nothing sent.")
        return 1
    previous = common.NETWORK_POSTS
    try:
        if live:
            common.NETWORK_POSTS = True
        try:
            with RunLock(cfg["lock"]):
                return _process(entries, args, cfg, live)
        except common.PostingError as exc:
            print(common.redact(str(exc)))
            return 3
    finally:
        common.NETWORK_POSTS = previous


def _ahead_hours(value) -> float | None:
    """Hours of native scheduling. Never more than 29 days, the Meta window."""
    if value is None:
        return None
    hours = float(value)
    if hours < 0:
        hours = 0.0
    cap = common.MAX_SCHEDULE_LEAD.total_seconds() / 3600
    return min(hours, cap)


def _process(entries: list, args, cfg: dict, live: bool) -> int:
    moment = common.now()
    ahead = _ahead_hours(args.schedule_ahead)
    if args.schedule_ahead is not None and ahead is not None and float(args.schedule_ahead) > ahead:
        print(
            "schedule-ahead capped at 29 days. "
            "YouTube publishAt and Facebook scheduled_publish_time are not set further out than that."
        )
    by_id = {entry.get("id"): entry for entry in entries if isinstance(entry, dict) and entry.get("id")}
    receipts = receipt_index(common.load_jsonl(cfg["receipts"]))
    spent = x_api.month_spent(cfg["log"], moment)
    counts = {name: 0 for name in ("due", "scheduled", "missed", "manual", "skipped", "refused", "future", "errors", "check")}
    log_path = cfg["log"] if live else cfg["dry_log"]

    def emit(entry: dict, action: str, line: str, **fields) -> None:
        print(line)
        record = {
            "ts": common.iso_denver(moment),
            "mode": "live" if live else "dry_run",
            "id": entry.get("id"),
            "platform": entry.get("platform"),
            "act": entry.get("act"),
            "action": action,
            "caption_len": len(common.final_text(entry)),
        }
        record.update(fields)
        if record.get("error"):
            record["error"] = common.redact(str(record["error"]))[:500]
        common.append_jsonl(log_path, record)

    def miss(entry: dict, late_hours: float) -> None:
        counts["missed"] += 1
        if live:
            common.patch_entry(
                cfg["schedule"],
                entry["id"],
                {
                    "status": "missed",
                    "result": {
                        "url": None,
                        "post_id": None,
                        "posted_at": None,
                        "error": "more than 6 hours late; not posted",
                    },
                },
            )
            action = "missed"
            line = f"MISSED id={entry.get('id')} platform={entry.get('platform')} late_hours={late_hours:.1f}"
        else:
            action = "would_mark_missed"
            line = (
                f"DRY RUN action=mark_missed id={entry.get('id')} "
                f"platform={entry.get('platform')} late_hours={late_hours:.1f}"
            )
        entry["status"] = "missed"
        emit(entry, action, line, ok=True, reason="more than 6 hours late")

    def manual(entry: dict, reason: str) -> None:
        counts["manual"] += 1
        line = (
            f"MANUAL id={entry.get('id')} platform={entry.get('platform')} "
            f"datetime_mt={entry.get('datetime_mt')} title={_title(entry)} reason={reason}"
        )
        emit(entry, "manual", line, ok=True, reason=reason)

    def skip(entry: dict, reason: str) -> None:
        counts["skipped"] += 1
        line = f"SKIP id={entry.get('id')} platform={entry.get('platform')} reason={reason}"
        emit(entry, "skip", line, ok=True, reason=reason)

    def refuse(entry: dict, reason: str, cost) -> None:
        counts["refused"] += 1
        if live:
            counts["errors"] += 1
        if live:
            common.patch_entry(
                cfg["schedule"],
                entry["id"],
                {
                    "status": "on_hold",
                    "result": {"url": None, "post_id": None, "posted_at": None, "error": reason},
                },
            )
            entry["status"] = "on_hold"
            line = f"REFUSED id={entry.get('id')} platform=x reason={reason}"
            action = "refused"
        else:
            line = f"DRY RUN action=refuse id={entry.get('id')} platform=x reason={reason}"
            action = "would_refuse"
        emit(
            entry,
            action,
            line,
            ok=False,
            reason=reason,
            estimated_cost_usd=None if cost is None else format(cost, "f"),
            endpoint=x_api.endpoint(entry),
        )

    def send(entry: dict, publish_at: str | None) -> str:
        platform = entry.get("platform")
        scheduled = bool(publish_at)
        cost = None
        if platform == "x":
            try:
                cap = x_api.load_cap(cfg["limits"])
            except common.PermanentError as exc:
                refuse(entry, str(exc), x_api.estimate_cost(entry))
                return "refused"
            cost = x_api.estimate_cost(entry)
            if x_api.would_exceed(spent, cost, cap):
                refuse(
                    entry,
                    (
                        f"estimated {format(cost, 'f')} USD would bring {common.month_key(moment)} "
                        f"to {format(spent + cost, 'f')} USD. The cap is {format(cap, 'f')} USD"
                    ),
                    cost,
                )
                return "refused"
        endpoint = _endpoint(entry, scheduled)
        extras = _extras(entry, publish_at, cost, spent if platform == "x" else None)
        action_name = "would_schedule" if scheduled else "would_post"
        if not live:
            emit(
                entry,
                action_name,
                _dry_line(entry, endpoint, extras, action_name),
                ok=True,
                endpoint=endpoint,
                media=common.describe_files(common.media_paths(entry)),
                estimated_cost_usd=None if cost is None else format(cost, "f"),
                publish_at=publish_at,
            )
            if cost is not None:
                nonlocal_spent(cost)
            entry["status"] = "scheduled_external" if scheduled else "posted"
            counts["scheduled" if scheduled else "due"] += 1
            return action_name
        attempt_id = secrets.token_hex(8)
        common.append_jsonl(
            cfg["receipts"],
            {
                "kind": "attempt",
                "id": entry.get("id"),
                "platform": platform,
                "time": common.iso_denver(moment),
                "attempt_id": attempt_id,
            },
        )
        receipts.setdefault(entry.get("id"), {"success": None, "attempts": []})["attempts"].append(
            {"kind": "attempt", "id": entry.get("id"), "attempt_id": attempt_id}
        )
        if os.environ.get("GC_CRASH_AFTER_ATTEMPT") == "1":
            os._exit(99)
        try:
            result = _dispatch(entry, publish_at)
        except common.PostingError:
            mark_needs_check(entry, attempt_id)
            return "needs_check"
        status_name = "scheduled_external" if scheduled or result.get("scheduled") else "posted"
        posted_at = common.iso_denver(moment)
        result_body = {
            "url": result.get("url"),
            "post_id": result.get("post_id"),
            "posted_at": posted_at,
            "error": result.get("error"),
        }
        if result.get("thumbnail_error"):
            result_body["thumbnail_error"] = result["thumbnail_error"]
            result_body["thumbnail_attempts"] = 1
        if result.get("unpublished_photo_id"):
            result_body["unpublished_photo_id"] = result["unpublished_photo_id"]
        if cost is not None:
            result_body["estimated_cost_usd"] = format(cost, "f")
        success = {
            "kind": "success",
            "id": entry.get("id"),
            "platform": platform,
            "post_id": result.get("post_id"),
            "url": result.get("url"),
            "posted_at": posted_at,
            "status": status_name,
            "error": result_body.get("error"),
        }
        common.append_jsonl(cfg["receipts"], success)
        receipts.setdefault(entry.get("id"), {"success": None, "attempts": []})["success"] = success
        common.patch_entry(cfg["schedule"], entry["id"], {"status": status_name, "result": result_body})
        entry["status"] = status_name
        entry["result"] = result_body
        if cost is not None:
            nonlocal_spent(cost)
        counts["scheduled" if status_name == "scheduled_external" else "due"] += 1
        log_action = "scheduled" if status_name == "scheduled_external" else "posted"
        emit(
            entry,
            log_action,
            f"{log_action.upper()} id={entry.get('id')} platform={platform} url={result.get('url') or ''}",
            ok=True,
            endpoint=endpoint,
            estimated_cost_usd=None if cost is None else format(cost, "f"),
            publish_at=publish_at,
        )
        return log_action

    def nonlocal_spent(cost) -> None:
        nonlocal spent
        spent += cost

    def mark_needs_check(entry: dict, attempt_id: str) -> None:
        counts["check"] += 1
        result = entry.get("result") if isinstance(entry.get("result"), dict) else {}
        already = (
            entry.get("status") == "needs_check"
            and result.get("error") == CHECK_ERROR
            and result.get("attempt_id") == attempt_id
        )
        if not already:
            common.patch_entry(
                cfg["schedule"],
                entry["id"],
                {"status": "needs_check", "result": {"error": CHECK_ERROR, "attempt_id": attempt_id}},
            )
            merged = dict(result)
            merged["error"] = CHECK_ERROR
            merged["attempt_id"] = attempt_id
            entry["status"] = "needs_check"
            entry["result"] = merged
        emit(
            entry,
            "needs_check",
            f"CHECK id={entry.get('id')} platform={entry.get('platform')} attempt_id={attempt_id} error={CHECK_ERROR}",
            ok=False,
            reason=CHECK_ERROR,
            attempt_id=attempt_id,
        )

    def heal(entry: dict) -> bool:
        slot = receipts.get(entry.get("id")) or {}
        receipt = slot.get("success")
        if not receipt or entry.get("status") not in {"ready", "needs_check"}:
            return False
        status_name = receipt.get("status") or "posted"
        common.patch_entry(
            cfg["schedule"],
            entry["id"],
            {
                "status": status_name,
                "result": {
                    "url": receipt.get("url"),
                    "post_id": receipt.get("post_id"),
                    "posted_at": receipt.get("posted_at"),
                    "error": receipt.get("error"),
                },
            },
        )
        entry["status"] = status_name
        emit(entry, "receipt_applied", f"RECEIPT id={entry.get('id')} platform={entry.get('platform')} status={status_name}", ok=True)
        return True

    def consider(entry: dict) -> str:
        if not isinstance(entry, dict):
            return "ignore"
        if entry.get("status") in common.TERMINAL:
            return "ignore"
        owned = OWNED_OUTSIDE.get(entry.get("id"))
        if owned:
            try:
                when = common.parse_dt(str(entry.get("datetime_mt") or ""))
            except Exception as exc:
                skip(entry, f"datetime_mt {exc}")
                return "skip"
            if when > moment:
                counts["future"] += 1
                return "future"
            if moment - when <= common.MISSED_AFTER:
                skip(entry, owned)
                return "skip"
            return "ignore"
        if heal(entry):
            return "healed"
        attempt_id = blocking_attempt(entry, receipts.get(entry.get("id")))
        if attempt_id:
            mark_needs_check(entry, attempt_id)
            return "needs_check"
        try:
            when = common.parse_dt(str(entry.get("datetime_mt") or ""))
        except Exception as exc:
            skip(entry, f"datetime_mt {exc}")
            return "skip"
        late = moment - when
        status = entry.get("status")
        if status == "waiting_on_asset":
            in_window = ahead is not None and when > moment and (when - moment) <= timedelta(hours=ahead)
            if when > moment and not in_window:
                counts["future"] += 1
                return "future"
            task_id = str(entry.get("task_id") or "").strip()
            skip(entry, f"waiting on asset {task_id}".strip())
            return "skip"
        blocked = common.block_reason(entry)
        if late > common.MISSED_AFTER:
            if status == "ready" and not blocked:
                miss(entry, late.total_seconds() / 3600)
                return "missed"
            if status == "ready" and blocked and late <= MANUAL_REMINDER:
                manual(entry, blocked + ". Past the 6-hour auto-post window.")
                return "manual"
            return "ignore"
        in_window = ahead is not None and when > moment and (when - moment) <= timedelta(hours=ahead)
        due = when <= moment
        if not due and not in_window:
            counts["future"] += 1
            return "future"
        if not due:
            if blocked or not common.can_schedule(entry):
                if blocked:
                    manual(entry, blocked)
                else:
                    reason = "Instagram has no future-publish field" if str(entry.get("platform")).startswith("instagram") else "this platform is posted at the due time"
                    counts["skipped"] += 1
                    emit(
                        entry,
                        "wait",
                        f"WAIT id={entry.get('id')} platform={entry.get('platform')} until={entry.get('datetime_mt')} reason={reason}",
                        ok=True,
                        reason=reason,
                    )
                return "wait"
            if when - moment < common.MIN_SCHEDULE_LEAD:
                counts["future"] += 1
                return "soon"
            state = _dep_state(entry, by_id)
            if state == "later":
                return "wait_dep"
            if state != "ok":
                skip(entry, common.dependency_block(entry, by_id) or "dependency is not posted")
                return "skip"
            if status != "ready":
                skip(entry, f"status is {status}")
                return "skip"
            reason = common.postable_reason(entry, by_id)
            if reason:
                skip(entry, reason)
                return "skip"
            return send(entry, common.iso_denver(when))
        if status != "ready":
            skip(entry, f"status is {status}")
            return "skip"
        if blocked:
            manual(entry, blocked)
            return "manual"
        state = _dep_state(entry, by_id)
        if state == "later":
            return "wait_dep"
        if state != "ok":
            skip(entry, common.dependency_block(entry, by_id) or "dependency is not posted")
            return "skip"
        reason = common.postable_reason(entry, by_id)
        if reason:
            skip(entry, reason)
            return "skip"
        return send(entry, None)

    ordered = sorted(
        [entry for entry in entries if isinstance(entry, dict)],
        key=lambda entry: (str(entry.get("datetime_mt") or ""), str(entry.get("id") or "")),
    )
    pending = ordered
    for _ in range(len(pending) + 1):
        if not pending:
            break
        again = []
        moved = False
        for entry in pending:
            outcome = consider(entry)
            if outcome == "wait_dep":
                again.append(entry)
            else:
                moved = True
        if not moved:
            for entry in again:
                skip(entry, common.dependency_block(entry, by_id) or "dependency is not posted")
            break
        pending = again
    if live:
        _retry_thumbnails(entries, cfg, emit)
    print(
        "summary "
        + " ".join(
            f"{name}={counts[name]}"
            for name in ("due", "scheduled", "missed", "manual", "skipped", "refused", "future", "errors", "check")
        )
    )
    return 1 if live and counts["errors"] else 0


def _retry_thumbnails(entries: list, cfg: dict, emit) -> None:
    moment = common.now()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        if entry.get("platform") not in {"youtube", "youtube_short"}:
            continue
        if entry.get("status") != "posted":
            continue
        result = entry.get("result") or {}
        if not result.get("thumbnail_error") or not result.get("post_id"):
            continue
        attempts = int(result.get("thumbnail_attempts") or 0)
        if attempts >= 5:
            continue
        posted_at = result.get("posted_at")
        if posted_at:
            try:
                age = moment - common.parse_dt(str(posted_at))
            except ValueError:
                age = None
            if age is not None and age > timedelta(days=7):
                continue
        try:
            youtube.retry_thumbnail(entry)
        except common.PostingError as exc:
            message = common.redact(str(exc))[:500]
            common.patch_entry(
                cfg["schedule"],
                entry["id"],
                {"result": {"thumbnail_error": message, "thumbnail_attempts": attempts + 1, "error": "video is up; thumbnail failed: " + message}},
            )
            emit(entry, "thumbnail_error", f"THUMBNAIL id={entry.get('id')} error={message}", ok=False, error=message)
            continue
        common.patch_entry(
            cfg["schedule"],
            entry["id"],
            {"result": {"thumbnail_error": None, "thumbnail_attempts": attempts + 1, "error": None}},
        )
        emit(entry, "thumbnail_set", f"THUMBNAIL id={entry.get('id')} set", ok=True)


def validate_schedule(path: str) -> int:
    data, err = common.load_schedule(path)
    if data is None:
        print(f"FAIL {path}: {err}")
        return 1
    errors = []
    warnings = []
    if data.get("version") != 1:
        errors.append("version must be 1")
    if data.get("timezone") != "America/Denver":
        errors.append("timezone must be America/Denver")
    entries = data.get("entries")
    if not isinstance(entries, list):
        errors.append("entries must be a list")
        entries = []
    seen = set()
    by_id = {}
    labeled = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entry {index} is not an object")
            continue
        ident = entry.get("id")
        label = f"entry {ident}" if isinstance(ident, str) and ident else f"entry {index}"
        labeled.append((label, entry))
        if not isinstance(ident, str) or not ident:
            errors.append(f"{label} needs a string id")
        elif ident in seen:
            errors.append(f"duplicate id {ident}")
        else:
            seen.add(ident)
            by_id[ident] = entry
        if entry.get("platform") not in common.PLATFORMS:
            errors.append(f"{label} platform {entry.get('platform')!r} is not known")
        if "type" in entry and entry.get("type") not in common.TYPES:
            errors.append(f"{label} type {entry.get('type')!r} is not known")
        if entry.get("status") not in common.STATUSES:
            errors.append(f"{label} status {entry.get('status')!r} is not known")
        if "act" in entry and entry.get("act") not in common.ACTS:
            errors.append(f"{label} act {entry.get('act')!r} is not known")
        try:
            common.parse_dt(str(entry.get("datetime_mt") or ""))
        except Exception as exc:
            errors.append(f"{label} datetime_mt: {exc}")
        approved = entry.get("approved")
        if approved is not None and not isinstance(approved, dict):
            errors.append(f"{label} approved must be an object or null")
        if entry.get("status") != "ready":
            for problem in common.limit_problems(entry):
                errors.append(f"{label} {problem}")
            for media in common.media_paths(entry):
                if not common.file_exists(media):
                    warnings.append(f"{label} missing media {media}")
    for label, entry in labeled:
        if entry.get("status") != "ready":
            continue
        blocked = common.block_reason(entry)
        reason = common.postable_reason(entry, by_id)
        if blocked:
            warnings.append(f"{label} will be listed as manual. {blocked}")
        elif reason:
            errors.append(f"{label} {reason}")
        for dep in entry.get("depends_on") or []:
            if dep not in by_id:
                errors.append(f"{label} depends on missing id {dep}")
    for entry in entries:
        if not isinstance(entry, dict) or entry.get("status") == "ready":
            continue
        ident = entry.get("id")
        for dep in entry.get("depends_on") or []:
            if dep not in by_id:
                errors.append(f"entry {ident} depends on missing id {dep}")
    for warning in warnings:
        print(f"WARN {warning}")
    for error in errors:
        print(f"FAIL {error}")
    print(f"validate errors={len(errors)} warnings={len(warnings)} entries={len(entries)}")
    return 1 if errors else 0


def upcoming(path: str, days: float) -> int:
    data, err = common.load_schedule(path)
    if data is None:
        if err == "not found":
            print(f"No schedule at {path}.")
            return 0
        print(f"Schedule not readable: {err}")
        return 1
    moment = common.now()
    end = moment + timedelta(days=days)
    rows = []
    for entry in data.get("entries") or []:
        if not isinstance(entry, dict):
            continue
        try:
            when = common.parse_dt(str(entry.get("datetime_mt") or ""))
        except Exception:
            continue
        if moment <= when <= end:
            rows.append((when, entry))
    rows.sort(key=lambda item: item[0])
    if not rows:
        print(f"Nothing from {common.iso_denver(moment)} through the next {days:g} days.")
        return 0
    for _when, entry in rows:
        print(
            f"{entry.get('datetime_mt')}  {str(entry.get('status') or ''):<18}  "
            f"{str(entry.get('platform') or ''):<20}  {entry.get('id')}  {_title(entry)}"
        )
    print(f"upcoming={len(rows)}")
    return 0


def check_auth(include_x: bool) -> int:
    common.load_user_env()
    lines = [
        youtube.check_auth("gracechase"),
        youtube.check_auth("sackbuts"),
        facebook.check_auth(),
        instagram.check_auth(),
        threads_api.check_auth(),
        tiktok.check_auth(),
    ]
    if include_x:
        lines.append(x_api.check_auth())
    else:
        lines.append("x SKIP GET /2/users/me was not called. It can cost a small read fee. Pass --include-x to run it.")
    failed = False
    for line in lines:
        print(line)
        head = line.split(" ", 1)[0]
        if head in {"youtube", "facebook", "instagram", "threads"} and " FAIL" in line:
            failed = True
        if include_x and head == "x" and " FAIL" in line:
            failed = True
        if head == "tiktok" and " FAIL" in line and "no TIKTOK_ACCESS_TOKEN" not in line:
            failed = True
    return 1 if failed else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Post due Gracechase schedule entries. The default is a dry run.")
    parser.add_argument("--live", action="store_true", help="post for real. Also requires social/posting-enabled.json")
    parser.add_argument(
        "--schedule-ahead",
        nargs="?",
        const=24,
        type=float,
        default=None,
        metavar="HOURS",
        help="also upload YouTube and Facebook posts due within HOURS (default 24) using native scheduling",
    )
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("validate", help="check schedule.json")
    coming = sub.add_parser("upcoming", help="print entries in the next week")
    coming.add_argument("--days", type=float, default=7)
    auth = sub.add_parser("check-auth", help="read-only auth checks. Does not post.")
    auth.add_argument("--include-x", action="store_true", help="also call X GET /2/users/me, which may cost a small read fee")
    return parser


def main(argv: list[str] | None = None) -> int:
    common.configure_stdio()
    common.load_user_env()
    args = build_parser().parse_args(argv)
    cfg = common.paths()
    if args.command == "validate":
        return validate_schedule(cfg["schedule"])
    if args.command == "upcoming":
        return upcoming(cfg["schedule"], args.days)
    if args.command == "check-auth":
        return check_auth(bool(args.include_x))
    return run_posts(args)


if __name__ == "__main__":
    sys.exit(main())
