# Gracechase playbook

The operating system for every agent posting Gracechase and The Sackbuts. Read it, then `learnings.md`, before starting any work. Strategy and reasons are in `strategy.md`. The standing work loop is `delegation.md`. The calendar is `schedule.json`, with a readable copy in `post-schedule.md`.

Times are Mountain Time (America/Denver, MST, UTC-7, until March 14, 2027).

## 1. Before you start

1. Read this file, `learnings.md`, and the entries due in the next 7 days in `schedule.json`.
2. Read the board: open tasks, and unacknowledged events from `python tools/board/tasks_cli.py events --unacked`. A note from the owner is an instruction. Act on it, then `ack` it with what you did.
3. Check hands-off: `python tools/hands_off.py status`. Exit code 10 means hands off. Then don't use the screen, keyboard, mouse, or a visible browser, and don't run heavy GPU or CPU work (renders, Topaz, Firefly or Dream Machine drivers, whisper, 4K encodes). API calls, light file edits, and planning are fine.
4. Check PAUSE: if `social/posting-paused.json` says paused, publish nothing.
5. Never print or write secrets. Never modify `E:\`. Never click Cancel, Delete, Get Credits, billing, or account controls.

## 2. What needs approval

| Action | Approval? |
|---|---|
| Posting a published video, or a link to one, on any platform | No |
| Posting an approved file as it is (a clip, image, or thumbnail in an Approved folder, or one marked approved on the board or in a campaign file) | No |
| Writing a caption for one of those posts, following the voice guide | No |
| Text-only posts: a lyric line, a credit, a poll, a "new video" note | No |
| A Community post or Story built from approved media | No |
| Re-posting to a new platform, or reusing an approved clip on another day | No |
| Any new image: a lyric card, quote card, carousel slide, crop or reframe, banner, Canvas still, Pinterest pin | Yes, in a batch |
| Any new edit: a clip cut from a video, a vertical reframe, a compilation, a full-album video, a lyric video | Yes, in a batch |
| Any new thumbnail, Shorts included | Yes |
| All ad copy, and every ad creative not already approved | Yes |
| Spending money: ads, paid APIs past their caps, Hedra | Within the $300 test plan only after copy approval, and the owner publishes the ad unless ads access is given. Anything past $300, or any budget raise, is an ask. |
| Website changes | Owner preview on the board before deploy |
| Changing a title, thumbnail, or test on a live promoted video | Yes. A hand edit stops a running A/B test. |
| Sackbuts Christmas album work | On hold until the end of the week of Nov 2 |

Once something is approved, mark it in `schedule.json` (`approved` set) and in the inventory. From then on it posts freely.

## 3. Cadence per platform

Starting targets. The Monday review adjusts them, and changes go in `learnings.md`. Check YouTube Studio > Analytics > Audience > "When your viewers are on YouTube" once a month and move the times to match.

| Platform | Per week | Best times (MT) | What goes out |
|---|---|---|---|
| YouTube long video | 1 when an approved asset exists | Thu 5:00pm, or Sun 9:00am for worship | New video, compilation, full album, lyric video |
| YouTube Shorts | 5 (Mon to Fri) | 4:00pm | Clip from an approved batch. Related video = its long video. Custom thumbnail. |
| YouTube Community | 3 (Mon, Wed, Sat) | 11:00am | Poll, lyric image, "new Short / new video" note |
| Facebook Reels | 4 (Mon, Tue, Thu, Sat) | 6:30pm | Same clips as the Shorts, a day later |
| Facebook Page post | 2 (Wed link post, Sun worship) | Wed 6:30pm, Sun 8:30am | YouTube link or approved image plus caption |
| Instagram Reels | 4 (Mon, Wed, Fri, Sun) | 6:30pm, Sun 9:00am | Clips |
| Instagram feed or carousel | 2 (Tue, Sat) | 12:00pm | Approved cover, approved lyric-card carousel |
| Instagram Stories | Daily | 8:00am | Link sticker to that day's video. The API cannot add a link sticker, so that one is done by hand, or the Story goes out without the sticker. |
| Threads | 7 | 7:30am | Lyric line, short note, sometimes an image |
| TikTok | 5 (Mon to Fri) | 7:00pm | Same clips. The owner posts from the phone, as below. |
| X | 3 (Tue, Thu, Sat) | 12:00pm | Clip or link. About $0.20 each from prepaid credit, $10 a month cap. |
| Pinterest | 5, once the account exists | 8:00pm | Approved covers and cards, each pin linking to YouTube |
| Spotify, Apple, Amazon, Pandora | Profile check monthly. Artist Pick per campaign. | | |
| Website | Per release, preview first | | |

Spacing rules:

- One song per post.
- The same clip doesn't run on the same platform twice within 14 days.
- Space out reuse of a clip across platforms, Shorts first.
- On a day a new long video goes up, that platform's other posts point to it.
- Sundays lean on worship songs.
- From November 15 to December 25, about 70% of posts are Christmas songs.
- After December 26, Christmas stops except for one handoff post.

## 4. Turning existing content into many posts

Work from `social/content-inventory.json`. For each song, pick in this order:

1. **Proven long videos first.** Let My Heart Find Christmas, To Hear the Angels Sing, the All I Need live video, then the rest by views.
2. **Clip batch.** Adam makes these. The plan says the moments: the hook, the chorus, the bridge, a striking shot. Vertical 1080x1920, 15 to 45 seconds. Song title on screen in the first second. Lyric captions burned in, using the lyric-video font. A custom 1080x1920 thumbnail. Any named face uses that person's face file (`asset-quality.mdc`). No auto-picked frames. Output, once he makes it, goes to `social/batches/<batch-id>/`.
3. **Lyric cards.** 2 to 4 lines on an approved image or an approved video still. 1080x1350 for Instagram and Facebook, 1000x1500 for Pinterest. He makes the card. The plan names the line and the source image.
4. **Carousels.** 5 to 7 slides: a lyric that unfolds line by line, or "the story behind the song." He makes them. The plan lists the slides.
5. **Quote and text posts.** A lyric line, or one true detail about the song, for Threads, X, and Community. No approval.
6. **Credits and making-of.** "Written by Rebekah. Sung and produced with Suno. Pictures with Firefly. Cut by Adam," plus one detail of how it was made. Use approved stills or the published video. No approval unless a new image is made.
7. **Polls.** On Community and Instagram Stories: "Which Christmas Window song next?" or "Pick the line." No approval.
8. **Sunday worship.** One worship song every Sunday morning across Facebook, Instagram, Threads, and Community.
9. **Long-watch videos.** A full album and an hour of Christmas worship (`strategy.md`). These are new edits. He makes them from the plan.
10. **Spotify Canvas.** A silent 9:16 loop per Christmas song, from the briefs in `social/canvas/BRIEFS.md`. He makes the loop. Do not generate the stills unless he asks for that Canvas.

The quality bar is `.cursor/rules/asset-quality.mdc` and `shot-direction.mdc`. No auto-picked frames, no stretched images, no text-only thumbnails. Agents do not generate the asset. The plan task asks him, and the schedule entry stays `waiting_on_asset`.

## 5. Plan, then he makes it

Adam creates the social and video assets (November 4, 2026, 6:45pm). One plan task per batch is enough. Each asset on that task is a plan item.

- The plan says what it is (type, length or size, aspect ratio), the song and the source file or "new footage needed", the hook and the on-screen text, where and when it posts, and why.
- **Approve plan** on every item, then the bottom **Approve plan**, turns the task into **Make**. It stays on his list. Nothing is generated.
- **Needs changes** sends his notes to the team. Nothing is made.
- On Make, **Generate starter clips** and **Make a Premiere project** run only if he taps them. The Premiere handoff is an organized folder plus an XML or EDL import. Say which. Do not claim a .prproj for these batches.
- **Ready to post** means the file is approved creative. Set the linked `waiting_on_asset` entries to `ready` for their planned dates.
- If the file is not in by the post date, those posts stay `waiting_on_asset` and the runner skips them. Do not swap in something else. Text posts, links, and already-approved files keep running.

## 6. Posting workflow per platform

The runner is `tools/post_due.py`. Docs are in `tools/README-posting.md`. It reads `schedule.json`, posts entries that are `ready` and due, writes the result back, and logs to `social/post-log.jsonl`. It runs live only when `social/posting-enabled.json` says enabled, and never while `posting-paused.json` says paused. Status `waiting_on_asset` is skipped. It is not a failure, and it is not posted.

- Dry run: `python tools/post_due.py`
- Check the schedule: `python tools/post_due.py validate`
- See what's coming: `python tools/post_due.py upcoming --days 7`
- Check sign-ins: `python tools/post_due.py check-auth`

| Platform | How it posts | Notes |
|---|---|---|
| YouTube long and Shorts | API, `videos.insert`. Native `publishAt`, so upload ahead as Private, scheduled. | Thumbnail at full quality, never shrunk under 50 MB. Altered or synthetic content set to yes. Made for kids: no. The Short's related video is set in Studio (browser, so hands-off rules apply). Pin the comment and set the end screen in Studio. |
| YouTube Community | Studio only, no API | Browser task when hands-off is off, or a board task |
| Facebook | Graph API with the Page token. Native scheduling. | Text, link, photo, video, Reel |
| Instagram | `tools/ig_post.py` on the Graph API. There is no future-publish field. A scheduled task on this PC runs at the due time. The upload may start a few minutes early. `media_publish` waits until the due time and never runs earlier. | Never an owner task. Never publish early to "schedule" it. Reels and carousel videos upload from a local file (`rupload.facebook.com`, `upload_type=resumable`). A feed image uses a public https `image_url`. |
| Threads | `tools/threads_post.py` | Images and video need a public https URL |
| X | API, OAuth 1.0a | Costs prepaid credit. One post per moment. |
| TikTok | Owner, from the phone, until the API audit passes | Each week a board task carries the 5 files and captions, with download and copy buttons. Mark `manual` in `schedule.json`. |
| Pinterest | Manual, until an account and API access exist | |
| Spotify, Apple, Amazon, Pandora | Owner or a browser task | Artist Pick, Canvas, bio: approval first |
| Website | `tools/site-preview.ps1`, then an owner preview task at http://192.168.1.59:8791/, then deploy per `site-access.md` | Never deploy before approval |
| Meta ads | The owner publishes in Ads Manager, unless he grants ads access | Copy and creative approved on the board |
| Google Ads (YouTube in-feed) | Owner account | Copy approved on the board |

Every post:

- Uses the voice guide, the credit line, and AI disclosure.
- Uses one link, the YouTube video, with the stores in the description.
- Gets its result URL recorded in `schedule.json`.
- Gets a reply to its comments within 24 hours. Use the AI reply in `all-i-need-campaign.md` when someone asks.

## 7. Ad test framework

1. **Hypothesis.** One line: "A clip of song X, shown to people interested in Christian Christmas music, will bring engaged YouTube viewers for $0.70 or less per click."
2. **Copy and creative.** Approved on the board. `social/ad-copy.md` holds every version and its approval state.
3. **Setup.**
   - Objective: Traffic, optimized for link clicks.
   - Audience: United States, 18 and up, Christian music, Gospel, and Christmas music interests.
   - No Advantage+ audience expansion and no lookalike, unless that is the thing being tested.
   - Placements: Feeds, Reels, and Stories. No Audience Network.
   - Creative enhancements off.
   - Destination: the YouTube video.
4. **Budget.** A fixed lifetime amount over 7 days. Never edit or raise it mid-test.
5. **Day-3 check.** Stop if the cost per click is over $1.50, if there are fewer than 15 external views, or if the comments are mostly "is this AI?" and views haven't moved.
6. **Readout.** The day after the end: the numbers against the pass bar, plus a `learnings.md` line, plus a board note.
7. **Scale.** Only after a pass, only inside the $300, and with the same creative and audience. Anything more is an owner ask.
8. **Ledger.** `social/ad-ledger.md` records every dollar: test, dates, budget, actual spend, result.

## 8. Website

- On each release, update `src/data/catalog.js`, the release hero, and the landing page.
- Run `tools/site-preview.ps1`, then add a board task for the owner to preview at http://192.168.1.59:8791/.
- Deploy only after he completes that task with an approval.
- Don't send ads to the homepage. Never link to the placeholder blog.

## 9. Owner tasks

Add an owner task only when an agent cannot do it. Check an API, a scheduled task on this PC, the posting runner, the Hyper-V VM browser, and a cloud agent first. Owner tasks are only for his sign-in, 2FA, or passkey; payments or spend above an approved limit; approval of new creative or ad copy; a website go-live preview; or a step only a person can physically do. The task must say why only he can do it, in `why_owner`. See `.cursor/rules/no-stall.mdc`.

### Check first

Before assigning any account, link, sign-up, or setting, confirm it is not already done. Use the YouTube Data API for channel info, Meta Graph, Google Ads if it is reachable, and Gmail for confirmation emails. If none of those can see it, a read-only look in the browser counts while the screen is allowed. If it is already done, mark it done and do not assign it. If it is partly done, the task asks only for the missing step. If a check is impossible without him, the task says "We couldn't check this because…" and the first step is for him to confirm whether it is already done.

Every open owner task stores that check in `checked`: when, how (API, browser, files, email, or logs), and what was seen. `add --owner adam` and `revise` refuse to save an open owner task without `--checked`, `--why-owner`, and `--priority`. `lint` lists any open owner task still missing it. Verify every link in the instructions before assigning the task.

### Ready gate

Do not move a task onto his list until the thing he is approving exists. `python tools/board/tasks_cli.py to-owner` runs the same check as `add` and `revise`. A website preview stays on the agent queue until each `http://192.168.1.59:8791/` page returns 200 and the task has an Approve or Reject item per page. An approval task stays there until each image, video, or audio file is on the task. A link that 404s, or does not connect, also keeps it there. Clips built only from already-approved songs, videos, and images are marked approved and posted. New images, new edits, new thumbnails, and ad copy still wait for him, and only after the files exist. Public TikTok posts are posted by an agent (API, or the PC browser when the screen is allowed). They are not a phone task. The unaudited TikTok app can only publish a private post.

A calendar event tied to a board task starts its description with `http://192.168.1.59:8790/task/<ID>`. Never link only the main list at `http://192.168.1.59:8790/`.

- Each task gets a clear title, a due date, numbered steps, links, and what happens after.
- Add his task with `python tools/board/tasks_cli.py add --owner adam --why-owner "..." --priority high --checked "..."`. The CLI rejects it if `why_owner` does not name the blocker, or if priority or checked is missing. Agent work is `add --owner agent`, which writes `social/agent-queue.json` and stays off his phone.
- Then ping once (`ping-owner.mdc`).
- Bundle approvals: one batch task is better than ten single ones.

## 10. Lessons learned (standing)

Lessons from earlier work. New ones go in `learnings.md`. Once a lesson holds up for a few weeks, move it here.

- An Instagram API call publishes immediately, and a container expires in 24 hours. Instagram scheduling is a scheduled task on this PC that publishes at the due time. It is never an owner task, and it is never an early publish.
- The YouTube Data API cannot pin a comment, set an end screen, start an A/B test, or post to Community. Those are Studio tasks.
- A hand edit of a title or thumbnail stops a running A/B test. Leave promoted videos alone during tests.
- Title tests wait until the YouTube Music song bar is on the watch page, and every variant keeps the exact released song title.
- A Testing-mode Google OAuth refresh token dies after 7 days. Publishing the Gracechase posts app to Production is agent work when a signed-in browser or gcloud session is already on this PC. The owner's only step is the Google consent click if the refresh token has to be issued again, and that task's `why_owner` has to say so. If you see `invalid_grant`, refresh from the existing token first. Do not hand him the branding form.
- Stills of named characters without their face file in `refs` don't look like them (the STH01 to STH03 Short thumbnails). Always attach the face file.
- Thumbnails upload at full quality from the PC (50 MB limit). Never recompress.
- The X API charges per post, more for posts with links. Keep X to 3 a week.
- The Meta Page token can't read billing or run ads. The owner publishes ads unless he grants ads access.
- Interstreet claims on our own uploads are expected. Allowlist, then turn Watch Page ads on. Never dispute.
- Lyric videos alone stayed in the hundreds of views. Story videos of a specific song traveled. Spend creative effort on clips of the proven videos first.
- A missed post is not caught up later. Mark it `missed` and move on.
