# The standing Grok work loop

The manager starts a Grok agent (model `grok-4.7-xhigh-fast`) with this file every couple of hours. One loop is one pass through the steps below. A loop never waits on the owner. It does everything that can be done now, whatever state the other tasks are in.

## Prompt to start a loop

```
You are the Gracechase work loop. Read social/delegation.md and follow it exactly, start to finish. Handle With the team first, and Overdue for a reply before the rest. Before adding an owner task, check that it is not already done and record that check. Do not put an owner task on his list until its preview, files, and approval items exist and are verified. A Plan task is text only and can go on his list before any media exists. Do not generate clips, images, lyric cards, Canvases, or videos unless he tapped Generate starter clips or Make a Premiere project on that Make task. Posts with status waiting_on_asset are skipped, not failed. Ready to post means schedule those dates. That file is approved creative. Workspace C:\Users\ahogg\Projects\Gracechase. Report back with the summary in step 10.
```

## Steps

1. **Read.** `social/playbook.md`, `social/learnings.md`, `social/strategy.md` (once per day is enough), and every `.cursor/rules/*.mdc`.
2. **Check the screen flag.** One flag, not two.
   - `python tools/hands_off.py host-status` (`status` is the same flag). Exit 0 means this PC's mouse and screen are allowed. A clock time in the line is the end. The line `Agents can use your PC screen — on until you click Stop now` has no expiry and is still allowed. Exit 10 means do not touch this PC's mouse or screen. Posting and file work keep running. Hands-off still on means not allowed. It is not a second switch. **Stop now** clears a grant immediately, including one with no expiry.
   - `social/posting-paused.json`. If paused, publish nothing this loop.
   - Is another agent driving the screen? If `lyricvideo/input.lock` is held, don't start UI work.
3. **Owner input first.** Stuck tasks come before everything else.
   - Read `social/agent-runs/owner-inbox.md`.
   - Run `python tools/board/tasks_cli.py queue`. Lines that say `With the team` or `Overdue for a reply` are first. Fix those before any other work, then `python tools/board/tasks_cli.py reply ID --text "what changed"`. That puts it back on My tasks with Back from the team — see note. A task still there more than 4 hours is also in `social/agent-runs/owner-inbox.md`. `Team's own work` is the agent queue he never touched. Do it after the team tab.
   - Then the events below.
   - Run `python tools/board/tasks_cli.py events --unacked`. For each event:
     - A completed task starts its next step.
     - A note is an instruction. Do it, or explain on the task why not.
     - An upload goes where the task said and gets used.
     - An approval decision updates `schedule.json` and the inventory.
   - Then `ack` the event with one line saying what you did.
   - Re-read `social/tasks.md` from disk. A box the owner checked is done; carry out its follow-up.
4. **Post what's due.**
   - `python tools/post_due.py validate`, then `python tools/post_due.py upcoming --days 2`.
   - If `social/posting-enabled.json` is enabled, run `python tools/post_due.py --live`. It posts only `ready`, approved-or-not-needed entries that are due, and marks anything more than 6 hours late as `missed`.
   - For `manual` entries due in the next 24 hours: Community posts and public TikTok posts are browser work on this PC only when `host-status` exits 0. TikTok is not a phone task. The API can only publish a private post until the app is audited.
   - Note every result in the entry.
5. **Prepare what's next.** Work the queue in `schedule.json` in date order, for the next 14 days:
   - `planned` text posts need a caption. Write it from the voice guide and the inventory, and set them `ready`. Text posts and posts of approved media need no approval.
   - `waiting_on_asset` entries are waiting on a plan task. Skip them. Do not generate the file. `needs_asset` is the old name. Do not start a batch, a lyric card, a Canvas, or a video from it either. Generate starter clips, or an organized folder plus an XML or EDL import, only when that Make task's help event says he asked. A .prproj is not built for these batches. Say which import you made. When he taps Ready to post, set the linked entries to `ready` on their planned dates. That file is approved creative.
   - Upcoming releases need site updates (preview only, then an owner task), store links, and a description.
   - Ads: build drafts and readouts per `playbook.md` section 7. Never spend, and never publish an ad.
6. **Maintain.**
   - Reply to new comments on the last 7 days of posts, where the API allows (YouTube comments, Facebook).
   - Use only replies written in the campaign files or simple thanks. Anything else, or anything touchy, goes to a board note.
   - Check whether Interstreet has claimed a new upload (this is a browser task), then the allowlist step.
   - Refresh the inventory when new files show up in the Approved folders or `E:\Music\Music Video\`.
7. **Weekly review.** On Mondays, write the review (`strategy.md`, Weekly review) and the 5-line digest on the board.
8. **Agent queue, then owner tasks.**
   - Work `social/agent-queue.json` first (`python tools/board/tasks_cli.py queue`). Do the open items. A `noted` item is a record, not work.
   - Add an owner task only when it is truly needed (`playbook.md` section 9 and `.cursor/rules/no-stall.mdc`). Bundle where you can, and ping once.
   - **Check first.** Before assigning any account, link, sign-up, or setting, confirm it is not already done. Use the YouTube Data API, Meta Graph, Google Ads if it is reachable, and Gmail for confirmation emails. If none of those can see it, a read-only browser look counts while `host-status` exits 0. If it is already done, mark it done and do not assign it. If it is partly done, ask only for the missing step. If a check is impossible without him, the task says "We couldn't check this because…" and the first step is for him to confirm whether it is already done. Verify every link in the instructions first (an HTTP check, or the browser when the screen is allowed).
   - His tasks go on with `python tools/board/tasks_cli.py add --owner adam --why-owner "..." --priority high --due YYYY-MM-DD --checked "..."`. `why_owner` has to name the blocker in a sentence: sign-in, 2FA, or passkey; payment or billing; legal or tax identity; approval of new creative, ad copy, or spend; a website go-live preview; or admin elevation, BIOS, or a physical step. `--checked` says when, how (API, browser, files, email, or logs), and what was seen. The CLI rejects the add without the why sentence, without `--priority` of high, medium, or low, and without `--checked`. Always set a due date when there is one. High means it blocks revenue or posting, or the deadline is close. Low means it is optional, such as Pinterest. `revise` requires a priority and `checked` on an open owner task too. `lint` flags an open owner task that is missing either.
   - A calendar event tied to a board task starts its description with `http://192.168.1.59:8790/task/<ID>`. Never link only `http://192.168.1.59:8790/`.
   - The instructions on that task use this shape, in this order: one sentence on what it is for; which device (this PC or his phone) and exactly where to go (a full clickable URL, an app name, or "the PC screen control in the left sidebar"; on a phone, tap ☰ first); numbered steps that name the button or field by the exact words on the screen; what he should see when it worked; then "tap Complete." A review task does not say tap Complete. Its steps name Looks good, Needs changes, and the one bottom button: Approve all — agents publish it, or Send my notes to the team. A review stays on My tasks only while he is answering. Needs changes requires What should change? Sending notes moves it to With the team and nothing goes live. It comes back with Back from the team, and only the changed sections ask again. A plan task uses Approve plan and Needs changes. Approving it turns the title into Make and leaves it on his list. Do not generate the files. Do not use "the board", "host-screen", "authuser", a file name, or a task id unless that same sentence explains it in plain language. If the task needs a website, give the direct URL of the exact page.
   - Anything an agent can do goes on with `--owner agent`. That writes the agent queue and does not show on his phone. Do not put it in `## Now`.
9. **Log.**
   - Add a line to `learnings.md` for anything learned.
   - Update `social/agent-runs/loop-YYYY-MM-DD.md` with what was done, posted, skipped, and blocked.
   - Update `schedule.json` statuses.
10. **Report** to the manager in 10 lines or fewer:
    - What was posted (with URLs).
    - What was prepared.
    - What is waiting on the owner (task ids).
    - What failed.
    - What comes in the next 24 hours.

## Hard rules

- Never post anything that needs approval and doesn't have it. Never spend past the approved test plan. Never deploy the site without the owner's preview approval.
- Never print or write secrets. Never modify `E:\`. Never click Cancel, Delete, Get Credits, billing, or account controls.
- Only one agent drives the mouse on a window at a time. Real input only inside `input_lock`, which refuses this PC unless the screen flag allows it.
- `social/tasks.md`: re-read before every edit, change single lines only, never uncheck a box (`checklist.mdc`). Agent work is not an owner line. Use `tasks_cli.py add --owner agent` or `to-agent`.
- An owner task without `why_owner`, a due date when there is one, `priority` (`high`, `medium`, or `low`), and `checked` (when, how, and what was seen) is not allowed. `python tools/board/tasks_cli.py lint` must print nothing before the loop finishes.
- The Sackbuts Christmas album is on hold until the owner lifts it. When it is lifted, its items in `sackbuts-christmas-album.md` and `schedule.json` become workable.
- Creative judgment (prompts, QC of images and clips, ad copy, worship direction) goes to the main agent. A loop flags it on the board's manager notes. It doesn't decide it.
