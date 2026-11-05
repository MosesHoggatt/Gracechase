# Learnings

A running log. Every agent reads this before starting work and adds to it when it finishes something worth remembering. Never rewrite or remove another agent's lines. Add one line at the top of the Log, in this form:

`YYYY-MM-DD | who | what we tried | result (numbers if any) | what to do next time`

Longer notes go in the Notes section below the Log. Lessons that hold up for a few weeks move to `playbook.md` section 10.

## Log

- 2026-11-04 | agent | Adam makes social and video assets himself, from 6:45pm | Plan tasks T043–T049 and T052 are on his list. Posts that need those files are waiting_on_asset and the runner skips them. Ready posts of existing approved files still auto-post. Agents do not generate a clip, card, Canvas, or video unless he taps that help button | Write the plan first. Generate starter clips or a folder plus XML or EDL only after he asks. Ready to post is the approval.
- 2026-11-04 | agent | Fixed Adam's three T050 preview rejections and rebuilt port 8791 | Latest releases uses the live-single cover and a Watch link that opens YouTube in a new tab, with the player on the page. /all-i-need and /album/christmas-window use the same chosen-app button. Headless check passed. Nothing deployed | The path /all-i-need was a separate fixed Apple Music page. Remove that file so the preview serves the site. Keep the live single cover off the Christmas Window art.
- 2026-11-04 | agent | Sent T050, preview the website, to Adam before the preview existed | Port 8791 was down. The task had no preview link and no Approve items. He did not know what to do | Ready gate: a preview stays on the agent queue until each page at http://192.168.1.59:8791/ returns 200 and the task has an Approve item per page. Do not deploy. The preview is that address, /all-i-need, and /album/christmas-window.
- 2026-11-04 | agent | Assigned T034, open a Google Ads account and link YouTube, without checking | The signup URL 404'd. Adam already had the account, and @Gracechase was linked on Mar 17, 2026. The note sat on his list because ping is not configured | Check first: API, email, or a read-only browser look. If it is already done, mark it done and do not assign it. Verify every instruction link before assigning. A guessed URL that 404s is not his to discover.
- 2026-11-04 | agent | Traced why T035 and other tasks were on Adam's board with no why-only-Adam | no-stall.mdc (3:27pm) is a Cursor rule only. tasks_cli add had no why_owner check. The 3:38pm board import kept every unchecked line, including T008. social/board-specs/add_nov4_tasks.py at 3:47pm added T031-T038. playbook.md called OAuth publish an owner step | Owner adam now requires why_owner. Agent work goes to social/agent-queue.json and stays off the phone.
- 2026-11-04 | agent | Dry-ran the posting runner for eight days, then turned auto-posting on | 11 posts would send (Threads 6, Facebook 2, Instagram 2, X 1). Held 3 stories that used the Even Better Christmas cover and 3 captions that repeated the 90,000-people line. The Nov 5 Reel, Short, and Facebook Reel stay with their own schedules | Story images have to match the song and be 9:16. Do not reuse that 90,000 sentence. Register the runner with pythonw so the 15-minute task does not take the screen.
- 2026-11-04 | strategist (Opus) | Delegated the content inventory to Grok without an explicit no-git line | Grok created branch `cursor/content-inventory-b50b`, committed, pushed, and left the workspace on that branch | Every Grok prompt says: no git commit, push, checkout, or branch. Check `git branch --show-current` after each subagent finishes.
- 2026-11-04 | strategist (Opus) | QC of Grok's first-week captions | Five posts in three days reused the same Let My Heart Find Christmas line and the "90,000 people" sentence | Vary the song and the line across platforms on the same day and on consecutive days. One lyric line per song per platform per week.
- 2026-11-04 | strategist (Opus) | Two agents wrote `learnings.md` and `social/hands-off.json` at the same time with different formats | One overwrote the other's log, and the hands-off file had two opposite meanings | Append single lines only. One meaning per file (see the hands-off rule).
- 2026-11-04 | strategist (Opus) | Set up the operating system: strategy, playbook, board, schedule, runner | Not run live yet | The first Monday review (Nov 9) checks whether the cadence in `playbook.md` actually got published, and what each platform returned.
- 2026-11-04 | Moses | Short thumbnails STH01 to STH03 were made without face refs | Mercy was recognizable, Justice was not, and none were used | Always attach the face file for a named character.
- 2026-11-03 | team | Tried to schedule an Instagram Reel through the API | Instagram has no future-publish field, so a call publishes now | Instagram posts at the due time from the runner or a scheduled job.
- 2026-11-04 | agent | Hand the All I Need Instagram Reel to Adam because the Graph API has no future-publish time | Dry-run against @_gracechase_ passed and created nothing. Task Gracechase-IG-Reel-All-I-Need uploads at 4:50pm Mountain on Nov 5 and publishes at 5:00pm | Instagram scheduling is a scheduled runner job on the PC at the due time, never an owner task.

## Notes

### 2026-11-04 — Owner tasks had no why-only-Adam

`no-stall.mdc` was on disk at 3:27pm. Nothing in `tools/board` read it. `add_task` inserted every new task as an unchecked line at the top of `## Now`, and the phone listed every open task. There was no `owner` field and no `why_owner`.

The board agent wrote `social/agent-runs/task-board.md` at 3:38pm. It imported every checkbox. It saw that T008 said it was not an owner task and left the line open because the box was unchecked. It added T030 with no why field. The next id was T031.

At 3:47pm `social/board-specs/add_nov4_tasks.py` called `tasks_cli.py add` eight times and created T031–T038. T035 tells Adam to publish the OAuth app and re-authorize. It never names a blocker only he can clear. `social/playbook.md` called that publish an owner step, which disagreed with no-stall. T034 is the only task in that batch that says "Only you can do this," and that sentence was prose, not a field the CLI could reject.

`add --owner adam` now refuses a task without `why_owner`. Agent work is `add --owner agent`, stored in `social/agent-queue.json`, and hidden on the phone. `to-agent` moves a line under `## Agents` and does not change the checkbox.

### 2026-11-04 — Browser work takes the host mouse

Firefly and Dream Machine are not API clients and they are not Playwright. `lyricvideo/firefly/ff_batch.py` and `lyricvideo/dm/dm_batch.py` drive the logged-in Chrome window with Windows UI Automation (`uiautomation`, `SetCursorPos`, `mouse_event`). They take `input_lock` so they do not fight each other, and that lock is on this PC. TikTok and Threads posting in `tools/` use HTTP APIs and do not touch the screen. There was no remote-debugging or `connect_over_cdp` path in the repo.

UI Automation only works in the interactive desktop session. `Invoke-Command -VMName` (PowerShell Direct) runs in a different session, so a host-side click script cannot drive Chrome inside a VM, and running the old scripts on the host moves Adam's mouse. The worker therefore runs a small logon agent (`tools/vm/guest-agent.py`) that starts those same scripts on the VM desktop. New signed-in sites (Studio, Meta, Instagram, TikTok, DistroKid) should use Chrome in the VM with remote debugging and Playwright `connect_over_cdp` from the host. Playwright is not installed here yet.

The host screen is refused unless `social/host-screen.json` exists and `allow` is boolean true (and `until`, if set, is still in the future) and the hands-off switch is off. A missing file means the mouse stays free. The VM wins when its agent answers, even if that file allows the host.

### 2026-11-04 — This PC can host the VM, after SVM and a guest license

Windows 11 Pro, build 26200, Gigabyte B550 VISION D-P, Ryzen 9 5950X, 128 GB RAM. `C:` has about 511 GB free. `E:` is the music disk (about 3.7 TB). `F:` is a second data disk and is not shared. Hyper-V is not enabled: `HypervisorPresent` is false. The CPU has second-level address translation. `VirtualizationFirmwareEnabled` is false, so AMD SVM is off in the firmware until Adam turns it on. The setup script does not reboot and does not change the BIOS.

The Pro license on the physical PC does not license a VM. Microsoft's old prebuilt Windows 11 development VHDX is not on https://developer.microsoft.com/en-us/windows/downloads/virtual-machines/ anymore (that URL now leads to general developer tools). The legal choices are the x64 ISO from https://www.microsoft.com/software-download/windows11 (choose Pro in setup, and use a separate Pro key; do not run the Installation Assistant) or the 90-day Enterprise evaluation at https://www.microsoft.com/en-us/evalcenter/evaluate-windows-11-enterprise. The evaluation shuts down every hour after 90 days. Home is the wrong edition because Enhanced Session needs the guest Remote Desktop stack.

Hyper-V has no shared-folder device. The host shares the repo, `E:\`, and `C:\Gracechase\vm-share` over SMB on the Default Switch only. Mapping those as `R:`, `E:`, and `S:` inside the guest keeps the paths the batch scripts already use. The debug port and the agent port stay on that NAT switch, with the guest firewall limited to the local subnet, because the Chrome debug port has no password.

Checked without elevation. Nothing that needs an administrator was run, and the PC was not rebooted.
