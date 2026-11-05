"""Dry-run tests for the posting runner. Live cases never have a file the APIs could accept."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import post_due
from posting import common, facebook, instagram, oauth1, threads, tiktok, x, youtube

PY = os.path.join(os.environ["LOCALAPPDATA"], "Programs", "Python", "Python311", "python.exe")
RUNNER = os.path.join(HERE, "post_due.py")
NOW = "2026-11-04T18:00:00-07:00"


def schedule(entries):
    return {"version": 1, "timezone": "America/Denver", "entries": entries}


def entry(entry_id, when, platform, **extra):
    body = {
        "id": entry_id,
        "datetime_mt": when,
        "platform": platform,
        "type": extra.pop("type", "post"),
        "act": extra.pop("act", "gracechase"),
        "title": extra.pop("title", "Hello"),
        "content_source": extra.pop(
            "content_source",
            {"inventory_id": None, "media": [], "thumbnail": None, "link": None},
        ),
        "caption": extra.pop("caption", "Hello from Gracechase"),
        "status": extra.pop("status", "ready"),
        "approval_needed": extra.pop("approval_needed", False),
        "approved": extra.pop("approved", None),
        "task_id": None,
        "depends_on": extra.pop("depends_on", []),
        "notes": "",
        "result": {"url": None, "post_id": None, "posted_at": None, "error": None},
    }
    body.update(extra)
    return body


class PureTests(unittest.TestCase):
    def test_denver_fallback_around_the_2026_changes(self):
        utc = timezone.utc
        self.assertEqual(common.denver_offset_fallback(datetime(2026, 11, 4, 18, tzinfo=utc)), timedelta(hours=-7))
        self.assertEqual(common.denver_offset_fallback(datetime(2026, 7, 15, 18, tzinfo=utc)), timedelta(hours=-6))
        self.assertEqual(common.denver_offset_fallback(datetime(2026, 11, 1, 7, 59, tzinfo=utc)), timedelta(hours=-6))
        self.assertEqual(common.denver_offset_fallback(datetime(2026, 11, 1, 8, tzinfo=utc)), timedelta(hours=-7))
        self.assertEqual(common.denver_offset_fallback(datetime(2026, 3, 8, 8, 59, tzinfo=utc)), timedelta(hours=-7))
        self.assertEqual(common.denver_offset_fallback(datetime(2026, 3, 8, 9, tzinfo=utc)), timedelta(hours=-6))

    def test_x_length_counts_a_link_as_23(self):
        url = "https://www.youtube.com/watch?v=Fh-bg9WbIFg"
        self.assertGreater(len(url), 23)
        self.assertEqual(common.x_length("see " + url), 4 + 23)
        self.assertEqual(common.x_length("hi"), 2)

    def test_final_text_keeps_instagram_caption_and_fills_a_placeholder(self):
        ig = entry("ig", NOW, "instagram_feed", caption="Link in bio.", content_source={"link": "https://www.youtube.com/watch?v=Fh-bg9WbIFg", "media": []})
        self.assertEqual(common.final_text(ig), "Link in bio.")
        tweet = entry("tw", NOW, "x", caption="Watch [YOUTUBE URL]", content_source={"link": "https://youtu.be/abc", "media": []})
        self.assertIn("https://youtu.be/abc", common.final_text(tweet))
        self.assertNotIn("[YOUTUBE URL]", common.final_text(tweet))

    def test_x_cap_boundary(self):
        self.assertFalse(x.would_exceed(common.money("9.800"), common.money("0.200"), common.money("10")))
        self.assertTrue(x.would_exceed(common.money("9.801"), common.money("0.200"), common.money("10")))
        linked = entry("a", NOW, "x", caption="https://gracechase.com")
        plain = entry("b", NOW, "x", caption="No address here")
        self.assertEqual(x.estimate_cost(linked), common.money("0.200"))
        self.assertEqual(x.estimate_cost(plain), common.money("0.015"))

    def test_month_spent_ignores_other_months_and_dry_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "log.jsonl")
            rows = [
                {"ts": "2026-11-04T12:00:00-07:00", "platform": "x", "action": "posted", "estimated_cost_usd": "1.500"},
                {"ts": "2026-10-04T12:00:00-06:00", "platform": "x", "action": "posted", "estimated_cost_usd": "9.000"},
                {"ts": "2026-11-04T12:00:00-07:00", "platform": "x", "action": "would_post", "estimated_cost_usd": "0.200"},
                {"ts": "2026-11-04T12:00:00-07:00", "platform": "facebook", "action": "posted", "estimated_cost_usd": "4.000"},
            ]
            with open(path, "w", encoding="utf-8") as handle:
                for row in rows:
                    handle.write(json.dumps(row) + "\n")
            moment = common.parse_dt("2026-11-04T18:00:00-07:00")
            self.assertEqual(x.month_spent(path, moment), common.money("1.500"))

    def test_oauth_rfc5849_signature(self):
        url = "http://photos.example.net/photos?file=vacation.jpg&size=original"
        header = oauth1.sign(
            "GET",
            url,
            None,
            "dpf43f3p2l4k3l03",
            "kd94hf93k423kf44",
            "nnch734d00sl2jdk",
            "pfkkdhi9sl3r4s00",
            nonce="kllo9940pd9333jh",
            timestamp="1191242096",
        )
        self.assertIn('oauth_signature="tR3%2BTy81lMeYAr%2FFid0kMTYa%2FWM%3D"', header)

    def test_youtube_metadata_declares_synthetic_and_not_for_kids(self):
        body = youtube.video_metadata({"title": "Song", "caption": "Words", "platform": "youtube", "content_source": {}}, None)
        self.assertIs(body["status"]["containsSyntheticMedia"], True)
        self.assertIs(body["status"]["selfDeclaredMadeForKids"], False)
        self.assertEqual(body["snippet"]["categoryId"], "10")
        self.assertEqual(body["status"]["privacyStatus"], "public")
        scheduled = youtube.video_metadata({"title": "Song", "caption": "Words", "platform": "youtube", "content_source": {}}, "2026-11-05T17:00:00-07:00")
        self.assertEqual(scheduled["status"]["privacyStatus"], "private")
        self.assertEqual(scheduled["status"]["publishAt"], "2026-11-05T17:00:00-07:00")

    def test_auth_and_rate_limits_stay_retryable(self):
        body = b'{"error":{"message":"no","code":10}}'
        for status in (401, 403, 429, 500, 503):
            with self.assertRaises(common.TransientError):
                x._raise_http(status, body)
            with self.assertRaises(common.TransientError):
                facebook._raise_graph(status, body)
        for status in (400, 404):
            with self.assertRaises(common.PermanentError):
                x._raise_http(status, body)
            with self.assertRaises(common.PermanentError):
                facebook._raise_graph(status, body)

    def test_attempt_without_a_receipt_blocks_until_ready_is_set_again(self):
        slot = {"success": None, "attempts": [{"kind": "attempt", "attempt_id": "a1"}]}
        ready = {"status": "ready", "result": {"error": None}}
        self.assertEqual(post_due.blocking_attempt(ready, slot), "a1")
        self.assertEqual(post_due.blocking_attempt({"status": "needs_check", "result": {}}, slot), "a1")
        cleared = {"status": "ready", "result": {"attempt_id": "a1"}}
        self.assertIsNone(post_due.blocking_attempt(cleared, slot))
        done = {"success": {"kind": "success", "post_id": "1", "status": "posted"}, "attempts": slot["attempts"]}
        self.assertIsNone(post_due.blocking_attempt(ready, done))
        self.assertIn("needs_check", common.STATUSES)

    def test_waiting_on_asset_is_skipped_not_failed(self):
        self.assertIn("waiting_on_asset", common.STATUSES)
        self.assertNotIn("waiting_on_asset", common.TERMINAL)
        folder = tempfile.mkdtemp()
        dry = os.path.join(folder, "dry.jsonl")
        due = entry(
            "2026-11-04-yt-short-waiting",
            "2026-11-04T17:00:00-07:00",
            "youtube_short",
            status="waiting_on_asset",
            task_id="T043",
            content_source={"inventory_id": None, "media": ["social/batches/missing.mp4"], "thumbnail": None, "link": None},
        )
        late = entry(
            "2026-11-03-yt-short-waiting",
            "2026-11-03T10:00:00-07:00",
            "youtube_short",
            status="waiting_on_asset",
            task_id="T043",
        )
        args = type("Args", (), {"schedule_ahead": None})()
        cfg = {
            "receipts": os.path.join(folder, "receipts.jsonl"),
            "log": os.path.join(folder, "log.jsonl"),
            "dry_log": dry,
            "schedule": os.path.join(folder, "schedule.json"),
        }
        code = post_due._process([due, late], args, cfg, False)
        self.assertEqual(code, 0)
        self.assertEqual(due["status"], "waiting_on_asset")
        self.assertEqual(late["status"], "waiting_on_asset")
        with open(dry, encoding="utf-8") as handle:
            text = handle.read()
        self.assertEqual(text.count("waiting on asset T043"), 2)
        self.assertNotIn("mark_missed", text)
        self.assertNotIn("FAIL", text)

    def test_unpublished_photo_is_explicitly_unpublished(self):
        fields = facebook.unpublished_photo_fields()
        self.assertEqual(fields["published"], "false")
        self.assertNotIn("true", fields.values())

    def test_sends_refuse_unless_the_run_is_live(self):
        common.NETWORK_POSTS = False
        calls = (
            lambda: youtube.upload_video({"platform": "youtube"}, None),
            lambda: youtube.set_thumbnail("token", "video", "thumb.jpg"),
            lambda: facebook.publish({}, None),
            lambda: facebook.unpublished_cdn_url("photo.jpg"),
            lambda: instagram.publish({}),
            lambda: threads.publish({"caption": "Hi", "content_source": {}}),
            lambda: x.publish({"caption": "Hi", "content_source": {}, "platform": "x"}),
            lambda: tiktok.publish({}),
        )
        for call in calls:
            with self.assertRaises(common.PostingError) as caught:
                call()
            self.assertIn("not live", str(caught.exception))

    def test_redact_removes_a_secret_and_an_upload_url(self):
        text = common.redact(
            "saw SUPERSECRETVALUE at https://www.googleapis.com/upload/youtube/v3/videos?upload_id=abc123&part=snippet",
            extra=("SUPERSECRETVALUE",),
        )
        self.assertNotIn("SUPERSECRETVALUE", text)
        self.assertNotIn("abc123", text)

    def test_patch_changes_only_one_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "schedule.json")
            common.atomic_write_json(
                path,
                schedule(
                    [
                        entry("keep", NOW, "threads", caption="leave this"),
                        entry("change", NOW, "threads", caption="old"),
                    ]
                ),
            )
            common.patch_entry(path, "change", {"status": "missed", "result": {"error": "late"}})
            data = common.load_json(path)
            rows = {item["id"]: item for item in data["entries"]}
            self.assertEqual(rows["keep"]["caption"], "leave this")
            self.assertEqual(rows["keep"]["status"], "ready")
            self.assertEqual(rows["change"]["status"], "missed")
            self.assertEqual(rows["change"]["caption"], "old")
            self.assertEqual(rows["change"]["result"]["error"], "late")


class RunnerTests(unittest.TestCase):
    def test_real_gate_files_were_not_created(self):
        # posting-enabled.json is the owner's switch and may exist. Tests must not create the pause file.
        self.assertFalse(os.path.exists(os.path.join(ROOT, "social", "posting-paused.json")))

    def test_already_scheduled_clips_are_not_sent(self):
        with tempfile.TemporaryDirectory() as tmp:
            video = os.path.join(tmp, "clip.mp4")
            image = os.path.join(tmp, "still.jpg")
            with open(video, "wb") as handle:
                handle.write(b"not a real video")
            with open(image, "wb") as handle:
                handle.write(b"not a real image")
            media = {"inventory_id": None, "media": [video], "thumbnail": image, "link": "https://www.youtube.com/watch?v=Fh-bg9WbIFg"}
            rows = [
                entry(
                    "2026-11-05-ig-reel-ain-adclip",
                    "2026-11-04T17:00:00-07:00",
                    "instagram_reel",
                    type="reel",
                    caption="Emmanuel is here.",
                    content_source=media,
                ),
                entry(
                    "2026-11-05-yt-short-ain-adclip",
                    "2026-11-04T10:00:00-07:00",
                    "youtube_short",
                    type="short",
                    title="All I Need",
                    caption="Emmanuel is here.",
                    content_source=media,
                ),
                entry(
                    "2026-11-05-fb-reel-ain-adclip",
                    "2026-11-04T17:00:00-07:00",
                    "facebook_reel",
                    type="reel",
                    caption="Emmanuel is here.",
                    content_source=media,
                ),
            ]
            paths = self._write_case(tmp, rows)
            before = open(paths["schedule"], "rb").read()
            result = self._run(paths)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(open(paths["schedule"], "rb").read(), before)
            ig = self._line(result.stdout, "id=2026-11-05-ig-reel-ain-adclip")
            self.assertIn("SKIP", ig)
            self.assertIn("Gracechase-IG-Reel-All-I-Need", ig)
            self.assertNotIn("would_post", ig)
            fb = self._line(result.stdout, "id=2026-11-05-fb-reel-ain-adclip")
            self.assertIn("SKIP", fb)
            self.assertIn("1150288730782473", fb)
            self.assertNotIn("would_post", fb)
            self.assertNotIn("id=2026-11-05-yt-short-ain-adclip", result.stdout)
            self.assertNotIn("mark_missed", result.stdout)

    def test_pythonw_style_missing_stdout_still_finishes(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._write_case(tmp, [entry("later", "2026-11-05T12:00:00-07:00", "threads", caption="Tomorrow.")])
            env = os.environ.copy()
            env.update({
                "GC_SCHEDULE_PATH": paths["schedule"],
                "GC_POST_LOG": paths["log"],
                "GC_DRY_LOG": paths["dry"],
                "GC_ENABLED_PATH": paths["enabled"],
                "GC_PAUSED_PATH": paths["paused"],
                "GC_LIMITS_PATH": paths["limits"],
                "GC_RECEIPT_LOG": paths["receipts"],
                "GC_LOCK_PATH": paths["lock"],
                "GC_NOW": NOW,
                "PYTHONUTF8": "1",
            })
            code = (
                "import sys\n"
                "sys.stdout = None\n"
                "sys.stderr = None\n"
                "import post_due\n"
                "raise SystemExit(post_due.main([]))\n"
            )
            result = subprocess.run(
                [PY, "-c", code],
                cwd=HERE,
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_dry_run_covers_due_future_missed_approval_and_manual(self):
        with tempfile.TemporaryDirectory() as tmp:
            video = os.path.join(tmp, "clip.mp4")
            image = os.path.join(tmp, "still.jpg")
            with open(video, "wb") as handle:
                handle.write(b"not a real video")
            with open(image, "wb") as handle:
                handle.write(b"not a real image")
            media = {"inventory_id": None, "media": [video], "thumbnail": image, "link": None}
            photo = {"inventory_id": None, "media": [image], "thumbnail": None, "link": None}
            rows = [
                entry("due-yt", "2026-11-04T17:00:00-07:00", "youtube", type="post", title="Hello Song", caption="A worship song.", content_source=media),
                entry("future-fb", "2026-11-05T12:00:00-07:00", "facebook", caption="Tomorrow."),
                entry("future-yt", "2026-11-05T12:30:00-07:00", "youtube", title="Tomorrow's song", caption="Tomorrow on YouTube.", content_source=media),
                entry("ig-later", "2026-11-05T14:00:00-07:00", "instagram_feed", caption="Later.", content_source=photo),
                entry("missed-yt", "2026-11-04T10:00:00-07:00", "youtube", title="Too late", caption="Too late.", content_source=media),
                entry("needs-ok", "2026-11-04T17:30:00-07:00", "instagram_feed", caption="Needs a yes.", approval_needed=True, content_source=photo),
                entry(
                    "approved-ig",
                    "2026-11-04T17:40:00-07:00",
                    "instagram_feed",
                    caption="Approved still.",
                    approval_needed=True,
                    approved={"by": "Moses", "date": "2026-11-04", "task_id": "t1"},
                    content_source=photo,
                ),
                entry("manual-pin", "2026-11-04T17:00:00-07:00", "pinterest", caption="Pin this."),
                entry("ads", "2026-11-04T17:00:00-07:00", "ads_meta", type="ad", caption="Do not buy this."),
                entry("not-ready", "2026-11-04T17:00:00-07:00", "threads", status="planned", caption="Not yet."),
                entry("x-plain", "2026-11-04T17:00:00-07:00", "x", caption="No address here"),
                entry("x-link", "2026-11-04T17:05:00-07:00", "x", caption="Watch the video https://www.youtube.com/watch?v=Fh-bg9WbIFg"),
                entry("tiktok-due", "2026-11-04T17:10:00-07:00", "tiktok", caption="A short clip."),
                entry("sackbuts-yt", "2026-11-04T17:15:00-07:00", "youtube", act="sackbuts", title="Sackbuts song", caption="For the Sackbuts.", content_source=media),
                entry("depends", "2026-11-04T17:20:00-07:00", "threads", caption="After the other one.", depends_on=["future-fb"]),
                entry("community", "2026-11-04T17:25:00-07:00", "youtube_community", type="community", caption="A community note."),
            ]
            paths = self._write_case(tmp, rows)
            with open(paths["log"], "w", encoding="utf-8") as handle:
                handle.write(json.dumps({
                    "ts": "2026-11-04T12:00:00-07:00",
                    "platform": "x",
                    "action": "posted",
                    "estimated_cost_usd": "9.900",
                }) + "\n")
                handle.write(json.dumps({
                    "ts": "2026-12-04T12:00:00-07:00",
                    "platform": "x",
                    "action": "posted",
                    "estimated_cost_usd": "5.000",
                }) + "\n")
            before = open(paths["schedule"], "rb").read()
            result = self._run(paths)
            after = open(paths["schedule"], "rb").read()
            self.assertEqual(before, after, result.stderr)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            out = result.stdout
            self.assertNotIn("access_token=", out)
            self.assertNotIn("Bearer ", out)
            self.assertNotRegex(out, r"client_secret=\S")
            due = self._line(out, "id=due-yt")
            self.assertIn("action=would_post", due)
            self.assertIn("platform=youtube", due)
            self.assertIn("upload/youtube/v3/videos", due)
            self.assertIn("caption_len=", due)
            self.assertIn("media=", due)
            self.assertIn("bytes=", due)
            self.assertIn("synthetic=true", due)
            self.assertIn("made_for_kids=false", due)
            self.assertIn("category=10", due)
            self.assertNotIn("id=future-fb", out)
            self.assertNotIn("id=future-yt", out)
            self.assertNotIn("id=ig-later", out)
            self.assertIn("action=mark_missed", self._line(out, "id=missed-yt"))
            self.assertIn("late_hours=8.0", self._line(out, "id=missed-yt"))
            self.assertIn("approval needed", self._line(out, "id=needs-ok"))
            approved = self._line(out, "id=approved-ig")
            self.assertIn("action=would_post", approved)
            self.assertIn("published=false", approved)
            self.assertIn("reason=Pinterest has no posting API", self._line(out, "id=manual-pin"))
            self.assertIn("ads stay off", self._line(out, "id=ads"))
            self.assertIn("status is planned", self._line(out, "id=not-ready"))
            plain = self._line(out, "id=x-plain")
            self.assertIn("action=would_post", plain)
            self.assertIn("estimated_cost_usd=0.015", plain)
            self.assertIn("month_total_usd=9.900", plain)
            refused = self._line(out, "id=x-link")
            self.assertIn("action=refuse", refused)
            self.assertIn("0.200", refused)
            self.assertIn("TIKTOK_ACCESS_TOKEN is not set", self._line(out, "id=tiktok-due"))
            self.assertIn("Gracechase token is not used", self._line(out, "id=sackbuts-yt"))
            self.assertNotIn("upload/youtube", self._line(out, "id=sackbuts-yt"))
            self.assertIn("dependency future-fb", self._line(out, "id=depends"))
            self.assertIn("no write", self._line(out, "id=community"))
            dry_log = open(paths["dry"], encoding="utf-8").read()
            self.assertIn("would_post", dry_log)
            self.assertIn("would_mark_missed", dry_log)
            self.assertEqual(open(paths["log"], encoding="utf-8").read().count("\n"), 2)
            self.assertFalse(os.path.exists(paths["enabled"]))

            ahead = self._run(paths, "--schedule-ahead", "24")
            self.assertEqual(ahead.returncode, 0, ahead.stdout + ahead.stderr)
            scheduled = self._line(ahead.stdout, "id=future-fb")
            self.assertIn("action=would_schedule", scheduled)
            self.assertIn("published=false", scheduled)
            self.assertIn("scheduled_publish_time=", scheduled)
            later_video = self._line(ahead.stdout, "id=future-yt")
            self.assertIn("action=would_schedule", later_video)
            self.assertIn("privacy=private", later_video)
            self.assertIn("publish_at=2026-11-05T12:30:00-07:00", later_video)
            self.assertIn("synthetic=true", later_video)
            waiting = self._line(ahead.stdout, "id=ig-later")
            self.assertIn("WAIT", waiting)
            self.assertIn("no future-publish", waiting)
            self.assertEqual(open(paths["schedule"], "rb").read(), before)

    def test_live_without_enable_or_while_paused_sends_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            video = os.path.join(tmp, "clip.mp4")
            image = os.path.join(tmp, "still.jpg")
            with open(video, "wb") as handle:
                handle.write(b"not a real video")
            with open(image, "wb") as handle:
                handle.write(b"not a real image")
            media = {"inventory_id": None, "media": [video], "thumbnail": image, "link": None}
            rows = [entry("due-yt", "2026-11-04T17:00:00-07:00", "youtube", title="Hello Song", caption="A worship song.", content_source=media)]
            paths = self._write_case(tmp, rows)
            before = open(paths["schedule"], "rb").read()
            disabled = self._run(paths, "--live")
            self.assertEqual(disabled.returncode, 2, disabled.stdout + disabled.stderr)
            self.assertIn("NOT ENABLED", disabled.stdout)
            self.assertEqual(open(paths["schedule"], "rb").read(), before)
            self.assertFalse(os.path.exists(paths["enabled"]))
            with open(paths["enabled"], "w", encoding="utf-8") as handle:
                json.dump({"enabled": True}, handle)
            with open(paths["paused"], "w", encoding="utf-8") as handle:
                json.dump({"paused": True}, handle)
            paused = self._run(paths, "--live")
            self.assertEqual(paused.returncode, 0, paused.stdout + paused.stderr)
            self.assertIn("PAUSED", paused.stdout)
            self.assertNotIn("POSTED", paused.stdout)
            self.assertNotIn("would_post", paused.stdout)
            self.assertEqual(open(paths["schedule"], "rb").read(), before)

    def test_live_marks_a_late_post_missed_and_lists_manual(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = os.path.join(tmp, "missing.mp4")
            rows = [
                entry(
                    "late-yt",
                    "2026-11-04T10:00:00-07:00",
                    "youtube",
                    title="Too late",
                    caption="Too late.",
                    content_source={"inventory_id": None, "media": [missing], "thumbnail": None, "link": None},
                ),
                entry("pin", "2026-11-04T17:00:00-07:00", "pinterest", caption="By hand."),
            ]
            paths = self._write_case(tmp, rows)
            with open(paths["enabled"], "w", encoding="utf-8") as handle:
                json.dump({"enabled": True}, handle)
            result = self._run(paths, "--live")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("access_token=", result.stdout)
            data = common.load_json(paths["schedule"])
            rows = {item["id"]: item for item in data["entries"]}
            self.assertEqual(rows["late-yt"]["status"], "missed")
            self.assertEqual(rows["pin"]["status"], "ready")
            self.assertIn("MISSED", result.stdout)
            self.assertIn("MANUAL", result.stdout)
            self.assertIn("id=pin", result.stdout)

    def test_schedule_ahead_stops_at_29_days(self):
        with tempfile.TemporaryDirectory() as tmp:
            rows = [
                entry("inside-fb", "2026-12-03T18:00:00-07:00", "facebook", caption="Inside the window."),
                entry("outside-fb", "2026-12-03T19:00:00-07:00", "facebook", caption="Past the window."),
            ]
            paths = self._write_case(tmp, rows)
            result = self._run(paths, "--schedule-ahead", "800")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("capped at 29 days", result.stdout)
            inside = self._line(result.stdout, "id=inside-fb")
            self.assertIn("action=would_schedule", inside)
            self.assertNotIn("id=outside-fb", result.stdout)
            self.assertFalse(os.path.exists(os.path.join(ROOT, "social", "posting-enabled.json")))

    def test_crash_between_attempt_and_receipt_is_not_retried(self):
        with tempfile.TemporaryDirectory() as tmp:
            rows = [entry("crash-th", "2026-11-04T17:00:00-07:00", "threads", caption="Hello from Gracechase")]
            paths = self._write_case(tmp, rows)
            with open(paths["enabled"], "w", encoding="utf-8") as handle:
                json.dump({"enabled": True}, handle)
            forbid = {"GC_FORBID_NETWORK": "1"}
            crashed = self._run(paths, "--live", extra_env={**forbid, "GC_CRASH_AFTER_ATTEMPT": "1"})
            self.assertEqual(crashed.returncode, 99, crashed.stdout + crashed.stderr)
            self.assertEqual(common.load_json(paths["schedule"])["entries"][0]["status"], "ready")
            receipts = common.load_jsonl(paths["receipts"])
            self.assertEqual(len(receipts), 1)
            self.assertEqual(receipts[0]["kind"], "attempt")
            self.assertEqual(receipts[0]["id"], "crash-th")
            self.assertEqual(receipts[0]["platform"], "threads")
            self.assertTrue(receipts[0].get("time"))
            self.assertTrue(receipts[0].get("attempt_id"))
            self.assertNotIn("post_id", receipts[0])

            again = self._run(paths, extra_env=forbid)
            self.assertEqual(again.returncode, 0, again.stdout + again.stderr)
            self.assertIn("CHECK id=crash-th", again.stdout)
            self.assertIn(post_due.CHECK_ERROR, again.stdout)
            self.assertNotIn("would_post", again.stdout)
            self.assertNotIn("POSTED", again.stdout)
            row = common.load_json(paths["schedule"])["entries"][0]
            self.assertEqual(row["status"], "needs_check")
            self.assertEqual(row["result"]["error"], post_due.CHECK_ERROR)
            self.assertEqual(row["result"]["attempt_id"], receipts[0]["attempt_id"])
            self.assertEqual(len(common.load_jsonl(paths["receipts"])), 1)

            listed = self._run(paths, extra_env=forbid)
            self.assertEqual(listed.returncode, 0, listed.stdout + listed.stderr)
            self.assertIn("CHECK id=crash-th", listed.stdout)
            self.assertEqual(common.load_json(paths["schedule"])["entries"][0]["status"], "needs_check")
            self.assertEqual(len(common.load_jsonl(paths["receipts"])), 1)
            checked = self._run(paths, "validate")
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

            data = common.load_json(paths["schedule"])
            data["entries"][0]["status"] = "ready"
            common.atomic_write_json(paths["schedule"], data)
            retry = self._run(paths, "--live", extra_env={**forbid, "GC_CRASH_AFTER_ATTEMPT": "1"})
            self.assertEqual(retry.returncode, 99, retry.stdout + retry.stderr)
            receipts = common.load_jsonl(paths["receipts"])
            self.assertEqual([item["kind"] for item in receipts], ["attempt", "attempt"])
            self.assertNotEqual(receipts[0]["attempt_id"], receipts[1]["attempt_id"])
            self.assertEqual(common.load_json(paths["schedule"])["entries"][0]["status"], "ready")

            followed = self._run(paths, extra_env=forbid)
            self.assertEqual(followed.returncode, 0, followed.stdout + followed.stderr)
            self.assertNotIn("would_post", followed.stdout)
            row = common.load_json(paths["schedule"])["entries"][0]
            self.assertEqual(row["status"], "needs_check")
            self.assertEqual(row["result"]["attempt_id"], receipts[1]["attempt_id"])
            self.assertEqual(len(common.load_jsonl(paths["receipts"])), 2)
            self.assertFalse(os.path.exists(os.path.join(ROOT, "social", "posting-enabled.json")))

    def test_validate_and_upcoming(self):
        with tempfile.TemporaryDirectory() as tmp:
            rows = [
                entry("same", NOW, "x", status="planned", caption="ok"),
                entry("same", NOW, "x", status="planned", caption="ok"),
                entry("long-x", NOW, "x", status="planned", caption="word " * 80),
                entry("tags", NOW, "instagram_feed", status="planned", caption=" ".join(f"#tag{i}" for i in range(31))),
                entry("title", NOW, "youtube", status="planned", title="T" * 101, caption="ok"),
                entry("soon", "2026-11-06T17:00:00-07:00", "threads", status="planned", caption="Next"),
                entry("gone", NOW, "youtube", status="ready", title="Missing file", caption="Missing.", content_source={"media": [os.path.join(tmp, "nope.mp4")], "thumbnail": None, "link": None}),
            ]
            paths = self._write_case(tmp, rows)
            checked = self._run(paths, "validate")
            self.assertEqual(checked.returncode, 1, checked.stdout)
            self.assertIn("duplicate id same", checked.stdout)
            self.assertIn("counts as", checked.stdout)
            self.assertIn("hashtags", checked.stdout)
            self.assertIn("100", checked.stdout)
            self.assertIn("missing media", checked.stdout)
            coming = self._run(paths, "upcoming", "--days", "7")
            self.assertEqual(coming.returncode, 0, coming.stdout + coming.stderr)
            self.assertIn("soon", coming.stdout)

    def _write_case(self, tmp, rows):
        paths = {
            "schedule": os.path.join(tmp, "schedule.json"),
            "log": os.path.join(tmp, "live.jsonl"),
            "dry": os.path.join(tmp, "dry.jsonl"),
            "enabled": os.path.join(tmp, "enabled.json"),
            "paused": os.path.join(tmp, "paused.json"),
            "limits": os.path.join(tmp, "limits.json"),
            "receipts": os.path.join(tmp, "receipts.jsonl"),
            "lock": os.path.join(tmp, "run.lock"),
        }
        common.atomic_write_json(paths["schedule"], schedule(rows))
        with open(paths["limits"], "w", encoding="utf-8") as handle:
            json.dump({"x_monthly_usd_cap": 10}, handle)
        return paths

    def _run(self, paths, *args, extra_env=None):
        env = os.environ.copy()
        env.update({
            "GC_SCHEDULE_PATH": paths["schedule"],
            "GC_POST_LOG": paths["log"],
            "GC_DRY_LOG": paths["dry"],
            "GC_ENABLED_PATH": paths["enabled"],
            "GC_PAUSED_PATH": paths["paused"],
            "GC_LIMITS_PATH": paths["limits"],
            "GC_RECEIPT_LOG": paths["receipts"],
            "GC_LOCK_PATH": paths["lock"],
            "GC_NOW": NOW,
            "PYTHONUTF8": "1",
        })
        env.pop("GC_CRASH_AFTER_ATTEMPT", None)
        env.pop("GC_FORBID_NETWORK", None)
        if extra_env:
            env.update(extra_env)
        return subprocess.run(
            [PY, RUNNER, *args],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )

    def _line(self, output, token):
        found = [line for line in output.splitlines() if token in line]
        self.assertEqual(len(found), 1, output)
        return found[0]


if __name__ == "__main__":
    unittest.main()
