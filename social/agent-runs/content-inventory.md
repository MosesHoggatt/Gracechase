# Content inventory run

Generated 2026-11-04T15:28:47-07:00.

## What this run did

- Read the social plan, preferences, catalog, All I Need campaign, Sackbuts notes, post schedule, and canvas briefs.
- Grepped lyricvideo/PLAN.md for approved plates and finals. Did not load the whole 120 KB file.
- YouTube token result: worked.
- Listed both channels' uploads, statistics, and playlist membership through the Data API. fileDetails did not return video streams. Width and height on YouTube rows come from the attached local file when one exists.
- Walked E:\Music\Music Video for finished exports, AD CLIP files, and thumbnails. ffprobe metadata only. No transcode and no scene detection.
- Walked both Approved folders, character face pngs, album masters, the Christmas Window lyric sheet, lyricvideo/lyrics.txt, the Your Majesty caption file, and Sackbuts lyrics in Lyrics.txt plus sackbuts.zip.
- Listed The Sackbuts folder. Christmas album items are marked on_hold. The public Two Years Late video is marked published.
- Did not edit social/agent-runs/open-work.md, social/tasks.md, or any campaign file. Did not write under E:\. Did not post, schedule, or spend.

## Counts

- Songs 89, videos 18, clips 2, images 155, posts 7.

## Could not read or did not open

- YouTube fileDetails returned no videoStreams for the Gracechase uploads. Width and height on those rows come from the matching local file when one is attached.
- No width or height for these uploads. fileDetails was empty and no local master was attached: Is Your Heart Snowed in This Christmas?; Gracechase - Even Better Christmas - New Christmas Album.
- Did not open Premiere projects, PSD pixels, or audio waveforms. PSD files that were listed got width and height from the header only.
- Did not inventory unreleased Songs folders (A Kingdom Apart and the rest) track by track. They are outside the website catalog.
- Did not copy full lyrics into the inventory. Quote lines are two short lines per song that has a lyric source.
- Old Albums\Album - Points of Light and Album - EP - Christmas Party were not added as current releases. Christmas Party looks like an earlier cover set, not the website catalog.

## Next steps

- If the token line says invalid_grant, Moses re-authorizes YouTube. The client id and secret stay. This run does not start that flow.
- The strategist can fill the calendar from the top 15 and the song table. Christmas songs with lyrics and no video are lyric-card posts, not video posts.
- Do not schedule I Still Care until a finished cut exists. Do not post STH thumbnails or character face files.
- Confirm vertical thumbnail.png before using it on the Short.
- Leave Sackbuts Christmas on hold. Two Years Late can be linked later; it is already public.
- Instagram Reel for All I Need still needs a person in the Instagram app. This inventory did not schedule it.

