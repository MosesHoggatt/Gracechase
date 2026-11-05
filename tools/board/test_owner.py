"""Owner-task rules. Uses GC_BOARD_ROOT so the real checklist is not touched.

Run: py -3 tools/board/test_owner.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from datetime import timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

ROOT = tempfile.mkdtemp(prefix="gc-board-owner-")
os.environ["GC_BOARD_ROOT"] = ROOT
os.environ["GC_BOARD_NO_PING"] = "1"
os.environ["GC_BOARD_SKIP_LINK_CHECK"] = "1"

import board_core  # noqa: E402
import server  # noqa: E402


def fail(message: str) -> None:
    print("FAIL", message)
    raise SystemExit(1)


def main() -> None:
    md = os.path.join(ROOT, "tasks.md")
    with open(md, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(
            "# Moses\n\n## Now\n\n"
            "- [ ] Agents publish the reel. Not an owner task. <!-- id:T008 -->\n"
            "- [ ] Sackbuts Christmas: leave this on hold. <!-- id:T012 -->\n"
            "- [x] Already done by him. <!-- id:T019 -->\n"
        )
    board_core.sync()
    held = board_core.get_task("T012")
    if held.get("status") != "on_hold":
        fail(f"hold status {held.get('status')}")
    if board_core.why_missing(held):
        fail("on hold should not be flagged")

    try:
        board_core.add_task("No reason", None, "Do the thing.", [], [])
        fail("adam add without why_owner should have failed")
    except board_core.BoardError as exc:
        if "why_owner" not in str(exc):
            fail(f"unexpected error: {exc}")

    try:
        board_core.add_task("Vague", None, "Do it.", [], [], why_owner="because I said so today")
        fail("vague why_owner should have failed")
    except board_core.BoardError:
        pass

    owner = board_core.add_task(
        "Sign in once",
        "2026-11-09",
        "Click Allow.",
        ["https://console.cloud.google.com"],
        [],
        why_owner="Google sign-in: the consent Allow click has to be the account owner's.",
        priority="high",
        checked="2026-11-04 test fixture. Looked at the throwaway checklist. The step was not already done.",
    )
    if owner["owner"] != "adam" or not owner["why_owner"]:
        fail("owner task missing why_owner")
    text, _bom = board_core._read_md()
    if f"id:{owner['id']}" not in text.split("## Agents")[0]:
        fail("owner task was not inserted in Now")
    home = server.home_body(board_core.list_tasks(), False)
    if "Why you: Google sign-in" not in home:
        fail("home page did not show why_owner")
    if "Agents publish the reel" not in home:
        fail("imported open task should still be visible before it is moved")

    agent = board_core.add_task(
        "Check the song bar",
        None,
        "Look at the watch page. Do not start a title test yet.",
        [],
        [],
        owner="agent",
    )
    text, _bom = board_core._read_md()
    now, _, rest = text.partition("## Agents")
    if f"id:{agent['id']}" in now:
        fail("agent add landed in Now")
    home = server.home_body(board_core.list_tasks(), False)
    if "Check the song bar" in home:
        fail("agent task showed on the phone home page")
    queued = {item["id"] for item in board_core.list_agent_queue()}
    if agent["id"] not in queued:
        fail("agent add missing from the queue")

    before = [line for line in text.splitlines() if "id:T008" in line][0]
    if "[ ]" not in before or "[x]" in before:
        fail(f"fixture box changed before move: {before}")
    moved = board_core.move_to_agents("T008", "A scheduled task on this PC publishes it.")
    if moved["owner"] != "agent":
        fail("move did not set owner agent")
    text, _bom = board_core._read_md()
    after_lines = [line for line in text.splitlines() if "id:T008" in line]
    if len(after_lines) != 1:
        fail(f"expected one T008 line, got {after_lines}")
    if "[ ]" not in after_lines[0] or "[x]" in after_lines[0]:
        fail(f"checkbox changed: {after_lines[0]}")
    if text.find("id:T008") < text.find("## Agents"):
        fail("T008 is still above ## Agents")
    home = server.home_body(board_core.list_tasks(), False)
    if "Agents publish the reel" in home:
        fail("moved task still on the phone home page")
    if "T008" not in {item["id"] for item in board_core.list_agent_queue()}:
        fail("moved task missing from the queue")

    fresh = board_core.add_task(
        "Tuesday posts stay unsent",
        None,
        "No decision needed.",
        [],
        [],
        why_owner="Approval of new creative: placeholder so the noted move can run.",
        priority="low",
        checked="2026-11-04 test fixture. Looked at the throwaway checklist. The step was not already done.",
    )
    noted = board_core.move_to_agents(fresh["id"], "Informational. No decision needed.", noted=True)
    if noted["status"] != "noted":
        fail(f"noted status {noted.get('status')}")
    text, _bom = board_core._read_md()
    line = [row for row in text.splitlines() if f"id:{fresh['id']}" in row][0]
    if "[ ]" not in line or "[x]" in line:
        fail(f"noted move checked the box: {line}")

    missing = [task for task in board_core.list_tasks() if board_core.why_missing(task)]
    if not any(task["id"] == "T008" for task in []):
        pass
    # The reel was moved. The hold is not flagged. The done box is not flagged.
    # The owner task has why. No open adam task should be missing why.
    if missing:
        fail("unexpected missing why: " + ", ".join(task["id"] for task in missing))

    text, bom = board_core._read_md()
    text = text.replace(
        "## Now\n\n",
        "## Now\n\n- [ ] Old hidden-computer step in one line. <!-- id:T050 -->\n",
        1,
    )
    board_core._write_md(text, bom)
    board_core.sync()
    before = [line for line in board_core._read_md()[0].splitlines() if "id:T050" in line][0]
    if "[ ]" not in before or "[x]" in before:
        fail(f"fixture box was not open: {before}")
    revised = board_core.revise_task(
        "T050",
        title="Turn on the hidden computer feature",
        instructions="This turns on a Windows feature.\n\nOn this PC:\n\n1. Click Start.\n2. Click Run as administrator.\n\nYou should see Hyper-V is already enabled.\n\nThen tap Complete.\n",
        why_owner="Admin elevation: the test task stands in for an elevated PowerShell step.",
        priority="medium",
        checked="2026-11-04 test fixture. Looked at the throwaway checklist. The step was not already done.",
    )
    if "\n" not in revised["instructions"] or "Click Start." not in revised["instructions"]:
        fail("revise flattened the numbered steps")
    if revised["title"] != "Turn on the hidden computer feature":
        fail(f"title {revised['title']}")
    after = [line for line in board_core._read_md()[0].splitlines() if "id:T050" in line]
    if len(after) != 1 or "[ ]" not in after[0] or "[x]" in after[0]:
        fail(f"revise changed the checkbox: {after}")
    if "Click Start." in after[0]:
        fail("the checklist line kept the whole instruction")
    page = server.task_body(board_core.get_task("T050"), False)
    if "<ol" not in page or "Click Start." not in page:
        fail("numbered steps did not render")
    wrapped = server.layout("Task", page, "/task/T050", show_home=True).decode("utf-8")
    if 'class="home"' not in wrapped or ">Home</a>" not in wrapped:
        fail("task page is missing the Home button")
    if "All tasks" in wrapped or 'class="screenbar' in wrapped or ">Tasks</a>" in wrapped:
        fail("the old top bar or Tasks button is still on the page")
    home_page = server.layout("Home", server.home_body([], False), "/", show_home=False).decode("utf-8")
    if ">Home</a>" not in home_page or "Next 21 days" not in home_page:
        fail("the sidebar is missing Home or the schedule link")

    copy_task = board_core.add_task(
        "Approve the test lines",
        None,
        "Pick one.",
        [],
        [
            {"key": "opt-a", "kind": "text", "path_or_text": "Option A words", "caption": "T2 option A"},
            {"key": "opt-b", "kind": "text", "path_or_text": "Option B words", "caption": "T2 option B"},
            {"key": "headline", "kind": "text", "path_or_text": "Headline words", "caption": "Headline"},
        ],
        why_owner="Approval of new ad copy: this throwaway task checks that a decision stays saved.",
        priority="high",
        checked="2026-11-04 test fixture. Looked at the throwaway approvals. Nothing was approved yet.",
    )
    fresh = server.task_body(board_core.get_task(copy_task["id"]), False)
    if "0 of 3 answered" not in fresh or "Change your mind" in fresh:
        fail("new approval sections did not start undecided")
    if "Answer every section first (0 of 3 done)" not in fresh or ">Complete</button>" in fresh:
        fail("a new review did not show the disabled button")
    if ">Approve</button>" in fresh or ">Reject</button>" in fresh:
        fail("old Approve and Reject buttons are still on a section")
    board_core.decide(copy_task["id"], "opt-a", "approve", "")
    raw = json.loads(open(board_core.tasks_json_path(), encoding="utf-8").read())
    stored = [task for task in raw["tasks"] if task["id"] == copy_task["id"]][0]
    if stored["approvals"].get("opt-a", {}).get("decision") != "approve":
        fail("approve did not persist in tasks.json")
    shown = server.task_body(board_core.get_task(copy_task["id"]), "Saved: Looks good T2 option A")
    if "Saved: Looks good T2 option A" not in shown:
        fail("save banner missing")
    if "1 of 3 answered" not in shown:
        fail("progress line missing")
    if "Looks good" not in shown or "chosen" not in shown:
        fail("looks-good badge missing")
    if shown.count("Change your mind") != 1:
        fail("Change your mind should show only on the decided section")
    try:
        board_core.decide(copy_task["id"], "opt-b", "reject", "")
        fail("needs changes without a note should fail")
    except board_core.BoardError as exc:
        if "change" not in str(exc):
            fail(f"empty change note said {exc}")
    board_core.decide(copy_task["id"], "opt-b", "reject", "too long")
    shown = server.task_body(board_core.get_task(copy_task["id"]), False)
    if "Needs changes" not in shown or "declined" not in shown or "too long" not in shown:
        fail("needs-changes badge missing")
    if "2 of 3 answered" not in shown:
        fail("progress did not count the change note")
    chunk = shown.split("T2 option B")[1].split("Headline")[0]
    if ">Looks good</button>" in chunk.split("Change your mind")[0]:
        fail("Looks good still shows on a section that needs changes")
    board_core.decide(copy_task["id"], "opt-a", "reject", "make it shorter")
    raw = json.loads(open(board_core.tasks_json_path(), encoding="utf-8").read())
    stored = [task for task in raw["tasks"] if task["id"] == copy_task["id"]][0]
    if stored["approvals"]["opt-a"]["decision"] != "reject":
        fail("a changed decision did not replace the saved one")
    if stored["approvals"]["opt-b"]["decision"] != "reject":
        fail("the other decision was lost")

    review = board_core.add_task(
        "Review the three lines",
        "2026-11-06",
        "Look at each line.",
        [],
        [
            {"key": "one", "kind": "text", "path_or_text": "Line one", "caption": "Line one"},
            {"key": "two", "kind": "text", "path_or_text": "Line two", "caption": "Line two"},
            {"key": "three", "kind": "text", "path_or_text": "Line three", "caption": "Line three"},
        ],
        why_owner="Approval of new ad copy: this throwaway review checks the one button.",
        priority="high",
        checked="2026-11-04 test fixture. Looked at the three lines. None were answered.",
    )
    board_core.decide(review["id"], "one", "approve", "")
    board_core.decide(review["id"], "two", "reject", "Cut the second line.")
    waiting = server.home_body(board_core.list_tasks(), False, "mine")
    if "Review the three lines" not in waiting:
        fail("an unfinished review left My tasks")
    board_core.decide(review["id"], "three", "approve", "")
    page = server.task_body(board_core.get_task(review["id"]), False)
    if "Send my notes to the team" not in page or "the 1 section that needs changes" not in page:
        fail("a mixed review did not explain the send")
    sent = board_core.submit_review(review["id"])
    if sent.get("status") != "blocked" or sent.get("review_action") != "sent":
        fail("send did not hand the review to the team")
    mine = server.home_body(board_core.list_tasks(), False, "mine")
    team = server.home_body(board_core.list_tasks(), False, "team")
    if "Review the three lines" in mine or "Cut the second line." not in team:
        fail("a sent review stayed on My tasks")
    back = board_core.reply_task(review["id"], "The second line is shorter.")
    approvals = back.get("approvals") or {}
    if approvals.get("one", {}).get("decision") != "approve" or approvals.get("three", {}).get("decision") != "approve":
        fail("looks-good sections were not kept")
    if "two" in approvals:
        fail("the changed section still had an old answer")
    page = server.task_body(board_core.get_task(review["id"]), False)
    if ">Back from the team</span>" not in page or "Answer every section first (2 of 3 done)" not in page:
        fail("the returned review did not ask only for the changed section")
    if page.find("The second line is shorter.") > page.find("<h2>Approval</h2>"):
        fail("the fix was not shown at the top")
    final = board_core.add_task(
        "Review the last line",
        "2026-11-06",
        "Look at the line.",
        [],
        [{"key": "last", "kind": "text", "path_or_text": "Last line", "caption": "Last line"}],
        why_owner="Approval of new ad copy: this throwaway review checks approve all.",
        priority="low",
        checked="2026-11-04 test fixture. Looked at the last line. It was not approved yet.",
    )
    board_core.decide(final["id"], "last", "approve", "")
    page = server.task_body(board_core.get_task(final["id"]), False)
    if "Approve all — agents publish it" not in page:
        fail("an all-clear review did not offer publish")
    published = board_core.submit_review(final["id"])
    if published.get("status") != "done" or published.get("review_action") != "approved":
        fail("approve all did not finish the review")

    page = server.layout("Home", server.home_body([], False), "/", False).decode("utf-8")
    if "Agents: not allowed" not in page or ">1 hour</option>" not in page:
        fail("the screen line did not say not allowed")
    if "Until I turn it off" not in page:
        fail("the no-expiry option is missing")
    if ">Stop</button>" in page or "Hands-off:" in page or "On for 1h" in page or "screenbar" in page:
        fail("not-allowed page still shows Stop or the old bar")
    board_core.hands_off.set_host_allow(1, "test", by="test")
    board_core.hands_off.set_off("test", by="test")
    if not board_core.hands_off.host_screen_allowed():
        fail("a one-hour grant did not allow the screen")
    allowed = server.layout("Home", "<p>x</p>", "/", False).decode("utf-8")
    if "Agents: allowed until" not in allowed or ">Stop</button>" not in allowed:
        fail("allowed page did not show the status and Stop")
    board_core.hands_off.set_on(1, "test", by="test")
    if board_core.hands_off.host_screen_allowed():
        fail("hands-off on should count as not allowed")
    blocked = server.screen_control_html("/")
    if "Agents: not allowed" not in blocked or ">Stop</button>" in blocked:
        fail("hands-off on still looked allowed")
    board_core.hands_off.set_off("test", by="test")
    past = (board_core.hands_off.datetime.now().astimezone() - board_core.hands_off.timedelta(minutes=5)).isoformat(
        timespec="seconds"
    )
    board_core.hands_off._atomic_write(
        board_core.hands_off.host_screen_path(),
        {"allow": True, "until": past, "set_at": None, "set_by": "test", "reason": "expired"},
    )
    if board_core.hands_off.host_screen_allowed():
        fail("an expired grant was still allowed")
    if "Agents: not allowed" not in server.screen_control_html("/"):
        fail("expiry did not return to not allowed")
    board_core.hands_off.toggle("test", by="test")
    if board_core.hands_off.load_host().get("allow") is True:
        fail("Stop now granted the screen")
    if board_core.hands_off.host_screen_allowed():
        fail("Stop now left the screen allowed")
    board_core.hands_off.set_host_allow(None, "test", by="test")
    board_core.hands_off.set_off("test", by="test")
    if board_core.hands_off.load_host().get("until") not in (None, ""):
        fail("a no-expiry grant stored an end time")
    if not board_core.hands_off.host_screen_allowed():
        fail("a no-expiry grant was not allowed")
    if board_core.hands_off.plain_status_line() != "Agents can use your PC screen — on until you click Stop now":
        fail(board_core.hands_off.plain_status_line())
    open_ended = server.screen_control_html("/")
    if "Agents: allowed (no limit)" not in open_ended or ">Stop</button>" not in open_ended:
        fail("the no-expiry line did not show Stop")
    if "Until I turn it off" not in open_ended:
        fail("the no-expiry option disappeared while allowed")
    board_core.hands_off.stop_now("test", by="test")
    if board_core.hands_off.host_screen_allowed() or board_core.hands_off.load_host().get("allow") is True:
        fail("Stop now did not override a no-expiry grant")
    if "Agents: not allowed" not in server.screen_control_html("/"):
        fail("Stop now did not return the line to not allowed")

    try:
        board_core.add_task(
            "Missing priority",
            None,
            "Do the thing.",
            [],
            [],
            why_owner="Sign-in: this throwaway add has a reason and no priority.",
        )
        fail("add without priority should fail")
    except board_core.BoardError as exc:
        if "priority" not in str(exc):
            fail(f"add without priority said {exc}")

    today = board_core.today_mt()

    def iso(delta: int) -> str:
        return (today + timedelta(days=delta)).isoformat()

    ordered = [
        {"id": "T901", "title": "Late one", "due": iso(-2), "status": "open", "owner": "adam", "priority": "low", "why_owner": "Physical step: late."},
        {"id": "T902", "title": "Soon high", "due": iso(1), "status": "open", "owner": "adam", "priority": "high", "why_owner": "Sign-in: soon."},
        {"id": "T903", "title": "Week medium", "due": iso(5), "status": "open", "owner": "adam", "priority": "medium", "why_owner": "Payment: this week."},
        {"id": "T904", "title": "Optional later", "due": iso(20), "status": "open", "owner": "adam", "priority": "low", "why_owner": "Legal identity: later."},
        {"id": "T905", "title": "No date", "due": None, "status": "open", "owner": "adam", "priority": "medium", "why_owner": "BIOS: no date."},
        {"id": "T906", "title": "High later date", "due": iso(12), "status": "open", "owner": "adam", "priority": "high", "why_owner": "Ad copy: high but not this week."},
    ]
    page = server.home_body(ordered, False)
    if page.find("Late one") > page.find("Soon high") or page.find("Soon high") > page.find("High later date"):
        fail("Do now was not overdue, then soon, then later high")
    if page.find("Do now") > page.find("This week") or page.find("This week") > page.find("Later"):
        fail("groups were not Do now, This week, Later")
    if "Week medium" not in page.split("This week", 1)[-1].split("Later", 1)[0]:
        fail("a 5-day medium task was not in This week")
    if "Optional later" not in page.split("Later", 1)[-1] or "No date" not in page.split("Later", 1)[-1]:
        fail("later tasks were not in Later")
    if "Overdue by 2 days" not in page or "Due tomorrow" not in page or "Due in 5 days" not in page:
        fail(f"due labels missing: {page}")
    if "No deadline" not in page or 'class="pri high"' not in page or 'class="pri low"' not in page:
        fail("priority tag or no-deadline label missing")
    if board_core.due_phrase(today.isoformat(), today) != "Due today":
        fail("today label")
    phrase = board_core.due_phrase(iso(3), today)
    if not phrase.startswith("Due in 3 days — "):
        fail(phrase)

    try:
        board_core.add_task(
            "Missing check",
            None,
            "Do the thing.",
            [],
            [],
            why_owner="Sign-in: this throwaway add has a reason and a priority.",
            priority="low",
        )
        fail("add without checked should fail")
    except board_core.BoardError as exc:
        if "checked" not in str(exc):
            fail(f"add without checked said {exc}")

    stuck = board_core.add_task(
        "Open the signup page",
        iso(1),
        "Open the page.",
        [],
        [],
        why_owner="Sign-in: the throwaway stuck task needs the account owner.",
        priority="high",
        checked="2026-11-04 test fixture. HTTP check of the signup page. It was not already done.",
    )
    body = server.task_body(board_core.get_task(stuck["id"]), False)
    if "I'm stuck" not in body or "What happened?" not in body:
        fail("task page is missing I'm stuck")
    reported = board_core.report_stuck(stuck["id"], "The signup page showed a 404.")
    if reported.get("status") != "blocked":
        fail(f"stuck status {reported.get('status')}")
    mine = server.home_body(board_core.list_tasks(), False, "mine")
    team = server.home_body(board_core.list_tasks(), False, "team")
    if "My tasks" not in mine or "With the team (2)" not in mine:
        fail("home is missing the two tabs")
    if "Waiting on Grace" in mine or "Waiting on Grace" in team:
        fail("Waiting on Grace is still on the list")
    if "Open the signup page" in mine:
        fail("a noted task stayed on My tasks")
    if "Grace is working on this" not in team or "The signup page showed a 404." not in team:
        fail("With the team did not show his note")
    noted = board_core.add_task(
        "Sign the paper form",
        iso(1),
        "Sign it.",
        [],
        [],
        why_owner="Sign-in: the throwaway note task needs the account owner.",
        priority="low",
        checked="2026-11-04 files. The form was not signed. This is a fixture.",
    )
    board_core.add_note(noted["id"], "I can't find the button.", by="owner", ping=False)
    team = server.home_body(board_core.list_tasks(), False, "team")
    if "With the team (3)" not in team or "find the button" not in team:
        fail("a saved note did not move the task to With the team")
    import owner_inbox
    owner_inbox.main()
    inbox = open(owner_inbox.inbox_path(), encoding="utf-8").read()
    if inbox.count("The signup page showed a 404.") != 1:
        fail("owner inbox missed the stuck report")
    path = os.path.join(ROOT, "tasks.json")
    doc = json.loads(open(path, encoding="utf-8").read())
    for task in doc["tasks"]:
        if task["id"] != stuck["id"]:
            continue
        stamp = task["notes"][-1]["time"]
        moment = board_core.datetime.fromisoformat(stamp) - timedelta(hours=5)
        task["notes"][-1]["time"] = moment.isoformat(timespec="seconds")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(doc, handle)
    late = server.home_body(board_core.list_tasks(), False, "team")
    if "Overdue for a reply" not in late:
        fail("a 5-hour-old note was not overdue")
    owner_inbox.main()
    inbox = open(owner_inbox.inbox_path(), encoding="utf-8").read()
    if inbox.count("<!-- overdue " + stuck["id"]) != 1 or "Overdue for a reply" not in inbox:
        fail("owner inbox missed the overdue reply")
    owner_inbox.main()
    again = open(owner_inbox.inbox_path(), encoding="utf-8").read()
    if again.count("<!-- overdue " + stuck["id"]) != 1:
        fail("owner inbox wrote the overdue reply twice")
    reopened = board_core.reply_task(stuck["id"], "The link is corrected. Try the new steps.")
    if reopened.get("status") != "open" or not board_core.show_fixed(reopened):
        fail("reply did not return the task")
    mine = server.home_body(board_core.list_tasks(), False, "mine")
    team = server.home_body(board_core.list_tasks(), False, "team")
    if "Back from the team — see note" not in mine or "The link is corrected" not in mine:
        fail("the reply did not come back to My tasks")
    if "Open the signup page" in team:
        fail("a replied task stayed With the team")
    page = server.task_body(board_core.get_task(stuck["id"]), False)
    if "Back from the team — see note" not in page or "The link is corrected" not in page.split("Notes")[0]:
        fail("the task page did not show the reply at the top")
    pulled = board_core.add_task(
        "Hold the signup until tomorrow",
        iso(3),
        "Wait.",
        [],
        [],
        why_owner="Sign-in: this throwaway hold needs the account owner.",
        priority="low",
        checked="2026-11-04 files. Nothing was submitted. This is a fixture.",
    )
    board_core.move_to_agents(pulled["id"], "Holding this until the estimate is done.")
    solo = board_core.add_task(
        "Download the installer file",
        None,
        "Save the file.",
        [],
        [],
        owner="agent",
    )
    team = server.home_body(board_core.list_tasks(), False, "team")
    if "Hold the signup until tomorrow" not in team or "Holding this until the estimate is done." not in team:
        fail("a to-agent note did not show With the team")
    if "With the team (3)" not in team:
        fail(f"team count changed when an untouched task was added: {team[team.find('With the team'):team.find('With the team')+24]}")
    own_at = team.find("Team's own work")
    solo_at = team.find("Download the installer file")
    if own_at < 0 or solo_at < own_at:
        fail("untouched agent work was not kept in Team's own work")
    if solo["id"] and "Download the installer file" in team[:own_at]:
        fail("untouched agent work was listed in With the team")

    queued = board_core.add_task(
        "Preview the website: sample",
        iso(2),
        "Look later.",
        [],
        [],
        owner="agent",
    )
    try:
        board_core.assign_to_adam(
            queued["id"],
            instructions="Open http://192.168.1.59:8791/ and look.",
            why_owner="Website preview: only he can approve the pages before they are published.",
            priority="high",
            checked="2026-11-04 files. Fixture skipped the live HTTP check. No approval item yet.",
            approval_items=[],
        )
        fail("preview without approval items was assigned")
    except board_core.BoardError as exc:
        if "Approve" not in str(exc) and "approval" not in str(exc).lower():
            fail(f"ready gate said {exc}")
    if board_core.get_task(queued["id"]).get("owner") != "agent":
        fail("ready gate moved an unfinished preview onto Adam's list")
    assigned = board_core.assign_to_adam(
        queued["id"],
        instructions="Open http://192.168.1.59:8791/ and look at Latest releases.",
        why_owner="Website preview: only he can approve the pages before they are published.",
        priority="high",
        checked="2026-11-04 files. Fixture skipped the live HTTP check. The approval item is present.",
        approval_items=[
            {
                "key": "home",
                "kind": "link",
                "path_or_text": "http://192.168.1.59:8791/",
                "caption": "Latest releases",
            }
        ],
        due="2026-11-06",
    )
    if assigned.get("owner") != "adam" or not assigned.get("approval_items"):
        fail("ready preview did not move to Adam")
    if ":8791" not in " ".join(assigned.get("links") or []):
        fail("preview link was not stored")

    planned = board_core.add_task(
        "Plan fixture",
        None,
        "Old agent copy.",
        [],
        [],
        owner="agent",
    )
    planned = board_core.assign_to_adam(
        planned["id"],
        title="Plan: one clip",
        instructions="This is the plan for one clip. You approve the plan.\n\nWhere: this page.\n\n1. Tap Approve plan.\n\nYou should see Plan approved.",
        why_owner="Approval of new creative: only he can approve this plan before the file is made.",
        priority="high",
        checked="2026-11-04 files. Fixture. The clip file was not on disk.",
        due="2026-11-06",
        approval_items=[
            {"key": "clip", "kind": "text", "path_or_text": "Vertical clip, 15 seconds. Source: new footage needed.", "caption": "One clip"}
        ],
    )
    with board_core.BoardLock():
        doc = board_core._load()
        row = board_core._must(doc, planned["id"])
        row["workflow"] = "plan"
        row["approvals"] = {}
        board_core._save(doc)
    page = server.task_body(board_core.get_task(planned["id"]), False)
    if "Approve plan" not in page or "Needs changes" not in page:
        fail("plan task did not show Approve plan and Needs changes")
    if "Approve all" in page or ">Complete<" in page:
        fail("plan task still offered publish or Complete")
    board_core.decide(planned["id"], "clip", "approve")
    made = board_core.submit_review(planned["id"])
    if made.get("workflow") != "make" or made.get("status") != "open" or not str(made.get("title")).startswith("Make:"):
        fail(f"approving the plan did not become Make: {made.get('workflow')} {made.get('status')} {made.get('title')}")
    if board_core.with_the_team(made):
        fail("approving the plan moved it to With the team")
    make_page = server.task_body(board_core.get_task(planned["id"]), False)
    if "Generate starter clips" not in make_page or "Make a Premiere project" not in make_page or "Ready to post" not in make_page:
        fail("Make task is missing the help buttons or Ready to post")
    if "XML or EDL" not in make_page:
        fail("Make task did not say the Premiere project is an XML or EDL import")
    if ">Complete<" in make_page:
        fail("Make task still showed Complete")
    helped = board_core.request_help(planned["id"], "premiere")
    if helped.get("status") != "open" or board_core.needs_grace(helped):
        fail("help button took the Make task off his list")
    try:
        board_core.ready_to_post(planned["id"], "")
        fail("Ready to post worked with no file and no path")
    except board_core.BoardError:
        pass
    posted = board_core.ready_to_post(planned["id"], r"C:\finished\clip.mp4")
    if posted.get("status") != "done" or posted.get("asset_path") != r"C:\finished\clip.mp4" or not posted.get("asset_approved"):
        fail("Ready to post did not record the file as approved creative")

    print("ok", ROOT)


if __name__ == "__main__":
    main()
