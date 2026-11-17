# A Very Sackbuts Christmas: the special

Written November 17, 2026, for Adam, and revised the same morning after his note on lip sync. Plan and script only. No image, clip, or audio was made, nothing was posted, and nothing under `E:\` changed.

One long YouTube video: the six album songs, with short host segments between them in one Sackbuts living-room set. The host segments are mostly on camera: the man who is talking is in his own close-up and lip-synced. A line is off camera only where that plays better: a reaction, an insert, a pickup, Bedgo asleep, or a quick cutaway. It is built from 16 stills that get reused, plus 22 lip-sync clips.

## 1. Plan

### Runtime

| Part | Length |
|---|---|
| Six songs, as their own lyric videos | 26:57 |
| Open, five song intros, and the close | about 2:15 |
| **Total** | **about 29 minutes** |

Song lengths are the wavs in `E:\Music\The Sackbuts\Songs\`. The song picture is each song's lyric video: the sequences in Adam's `A Very Sackbuts Christmas` Premiere project for five songs, and the finished Two Years Late mp4. The special adds only the set, the host segments, and the cut into each song.

### Song order

| # | Song | Length | Why it goes here |
|---|---|---|---|
| 1 | Nebo County Sleigh Ride | 4:16 | Bright, fast opener. It sets up Nebo, Dewey, and The Furnace not starting. |
| 2 | Stuck in a Stable on Christmas | 4:26 | The Furnace dies again, so the running joke gets bigger. It is also the first quiet turn, with Silent Night in the barn. |
| 3 | Eighteen Wheels and a Prayer | 4:55 | The biggest story, and Luther's turn as Firehose. It is the energy peak in the middle. |
| 4 | The Tinsel Comes and Goes | 4:44 | Slows down at Mama's house. Mama is alive at ninety, and the manger never moves. |
| 5 | Mama's Fruitcake | 4:54 | The tender one. It comes after Tinsel, so we meet Mama before we miss her. |
| 6 | Two Years Late and Right on Time | 3:41 | Ends on the one King they bow to and "Happy birthday, Friend," which leads into the close. |

### Segments

| Id | Where | Length | Lip-sync clips |
|---|---|---|---|
| A | Open, then into Sleigh Ride | about 28 s | LS01–LS05 |
| B | Into Stuck in a Stable | about 17 s | LS06–LS07 |
| C | Into Eighteen Wheels | about 16 s | LS08–LS10 |
| D | Into Tinsel | about 16 s | LS11–LS12 |
| E | Into Mama's Fruitcake | about 18 s | LS13–LS16 |
| F | Into Two Years Late | about 17 s | LS17–LS18 |
| G | Close | about 24 s | LS19–LS22 |

### Lip-sync budget

**22 lip-sync clips, covering 23 of the 31 spoken lines, with about 74 seconds of speech.**

**Padding.** Each clip gets 0.5 s of driving audio before the line and 1.0 s after. On the nine punchline clips, the after pad is 2.0 s instead. That keeps the speaker's face on screen while the joke lands, rather than cutting away.

**Billed time.** That comes to **116 billed seconds, about $19.10**, at about $0.165 per second for OmniHuman 1.5 at 1080p.

**Redo reserve.** Hold **34 more seconds, about $5.60**, for redoing up to about six clips that come back wrong. That brings the plan to **about 150 billed seconds, about $24.75**, which is the middle of Adam's $20–30.

**Hard stop: 181 billed seconds ($30).** Run `hedra.py estimate` before each batch and log the spend.

| Clip | Speaker | Line | Still | Speech | Billed |
|---|---|---|---|---|---|
| LS01 | Earl | A2 | CU-E | 4.5 s | 6.0 s |
| LS02 | Luther | A3 | CU-L | 3.0 s | 4.5 s |
| LS03 | Luther | A6 (punchline) | CU-L2 | 1.5 s | 4.0 s |
| LS04 | Earl | A7 | CU-E | 5.0 s | 6.5 s |
| LS05 | Luther | A8 (punchline) | CU-L | 2.0 s | 4.5 s |
| LS06 | Earl | B1 | CU-E2 | 3.5 s | 5.0 s |
| LS07 | Luther | B2 (punchline) | CU-L | 6.5 s | 9.0 s |
| LS08 | Earl | C2 | CU-E2 | 2.0 s | 3.5 s |
| LS09 | Luther | C3 (punchline) | CU-L2 | 1.0 s | 3.5 s |
| LS10 | Earl | C4 | CU-E | 4.0 s | 5.5 s |
| LS11 | Luther | D1 | CU-L2 | 2.5 s | 4.0 s |
| LS12 | Earl | D2 | CU-E2 | 3.5 s | 5.0 s |
| LS13 | Luther | E1 | CU-L2 | 2.0 s | 3.5 s |
| LS14 | Earl | E2 | CU-E2 | 2.0 s | 3.5 s |
| LS15 | Luther | E3 (punchline) | CU-L | 2.5 s | 5.0 s |
| LS16 | Earl | E4 (punchline) | CU-E | 4.5 s | 7.0 s |
| LS17 | Earl | F2 | CU-E | 4.0 s | 5.5 s |
| LS18 | Luther | F3 (punchline) | CU-L | 5.0 s | 7.5 s |
| LS19 | Earl | G2 | CU-E | 3.0 s | 4.5 s |
| LS20 | Luther | G3 (punchline) | CU-L | 3.0 s | 5.5 s |
| LS21 | Earl | G4 | CU-E | 3.0 s | 4.5 s |
| LS22 | Bedgo | G6a and G6c (punchline) | CU-B2 | 6.0 s | 8.5 s |
| **Total** | | | | **74.0 s** | **116.0 s** |

By speaker: Earl 11 clips, Luther 10, and Bedgo 1.

The eight NO-SYNC lines, and why each one plays better off camera:

| Line | Speaker | Why it is off camera |
|---|---|---|
| A5 | Earl | The joke is Bedgo asleep, so we stay on Bedgo. |
| A10 | Luther | The count-in plays over the band with instruments up. |
| C1 | Luther | His voice comes through the CB, over a shot of the radio. |
| D3 | Earl | The line is about the manger, so we look at the manger. |
| D4 | Luther | "Like Bedgo" lands on Bedgo asleep. |
| F1 | Luther | The joke is Earl wiping his eye, so it is a reaction shot. |
| G5 | Luther | We stay on Bedgo asleep, just before he wakes. |
| G6b | Earl | We hold on Bedgo through his wake-up so it lands in one shot. |

## 2. Script

Speaker names are for this script only. No one says them on screen unless the line does.

Shot codes are in section 3.

**Who is looking where**

- **CU-E and CU-L** are the front close-ups. Earl and Luther are talking to us, just beside the lens.
- **CU-E2 and CU-L2** are the second angles. They are turned toward each other, talking across.
- "Lips closed" means the Dream Machine prompt for that clip says his lips stay closed.

**Standing rules for every segment**

- **Each segment after a song** opens on a 1-second W01 beat, with the instruments back on their stands, before the first close-up.
- **Bedgo** is asleep in the recliner for every talking line until G. His eyes are closed, he never moves on his own, and he snores (sound effect) only where marked. When a song starts, he is still asleep with the bass in his arms.
- **And Friend** appears only in W02F, before songs 3 and 6 and at the start of the close. He is always small and soft, deep in the dim archway at the back, in a plain dark coat, with no readable face. He has no glow, no halo, and no light on him. Nobody points at him or explains him. When he comes up, the boys smile and change the subject.
- **Instruments** stay on their stands whenever anyone is talking. Each song lead-in is a quick run of pickups: Earl's guitar (P01), Luther's fiddle (P02), and Luther leaning the bass into sleeping Bedgo's arms (P03). Then comes the ready wide (W02 or W02F), and the song starts.

### A. Open, into Nebo County Sleigh Ride (about 28 s)

| # | Speaker | Line | Sync | Shot | Background |
|---|---|---|---|---|---|
| A1 | — | Fire crackle, tree lights. The logo goes on here in the edit. | — | W01, slow push in, 3 s | Bedgo asleep |
| A2 | EARL | "Evenin', and Merry Christmas from Nebo County, Tennessee. We're the Sackbuts." | **LIP-SYNC (LS01)** | CU-E | — |
| A3 | LUTHER | "I'm Luther. That there's Earl. And that's Bedgo." | **LIP-SYNC (LS02)** | CU-L | — |
| A4 | — | Snore. | — | CU-B1, 1.5 s | asleep |
| A5 | EARL | "He's been like that since Thanksgiving." | NO-SYNC | CU-B1, held | asleep |
| A6 | LUTHER | "...And Friend." He glances back over his shoulder toward the back of the room. | **LIP-SYNC (LS03)** | CU-L2 | — |
| A7 | EARL | "Anyhow. First one's about a horse that won't move unless you quote him Scripture." He starts with a small smile. | **LIP-SYNC (LS04)** | CU-E | — |
| A8 | LUTHER | "Bedgo knows the short one." | **LIP-SYNC (LS05)** | CU-L | — |
| A9 | — | Pickups. Luther leans the bass into Bedgo, who hugs it without waking. | — | P01, P02, P03, 3 s | asleep |
| A10 | LUTHER | "One, two..." The song starts. | NO-SYNC | W02 | asleep on the bass |

"The short one" is "Jesus wept." It is the line that gets Dewey moving in the song, so this only sets it up and does not spoil it.

### B. Into Stuck in a Stable on Christmas (about 17 s)

| # | Speaker | Line | Sync | Shot | Background |
|---|---|---|---|---|---|
| B0 | — | Back on the set. | — | W01, 1 s | asleep |
| B1 | EARL | "Dewey's twenty-six, and he still runs better than The Furnace." | **LIP-SYNC (LS06)** | CU-E2 | — |
| B2 | LUTHER | "One Christmas Eve The Furnace quit, and we slept in a barn with a cow, a donkey, and Bedgo. Hard to tell which one was snorin'." | **LIP-SYNC (LS07)** | CU-L | — |
| B3 | — | Snore. | — | CU-B1, 1.5 s | asleep |
| B4 | — | Pickups, then the song. | — | P01, P03, W02 | asleep on the bass |

### C. Into Eighteen Wheels and a Prayer (about 16 s)

| # | Speaker | Line | Sync | Shot | Background |
|---|---|---|---|---|---|
| C0 | — | Back on the set. | — | W01, 1 s | asleep |
| C1 | LUTHER | "Breaker one-nine, this here's Firehose. Come on." It is filtered to sound like it is coming through the CB. | NO-SYNC | I02, CB radio | — |
| C2 | EARL | "Luther. We're on television." | **LIP-SYNC (LS08)** | CU-E2 | — |
| C3 | LUTHER | "Old habit." He sheepishly sets the mic down, out of frame. | **LIP-SYNC (LS09)** | CU-L2 | — |
| C4 | EARL | "This next one's forty truckers, one blizzard, and a baby that would not wait." | **LIP-SYNC (LS10)** | CU-E | — |
| C5 | — | Pickups, then the song. | — | P01, P02, P03, W02F | **And Friend** in the archway, first time. Asleep on the bass. |

### D. Into The Tinsel Comes and Goes (about 16 s)

| # | Speaker | Line | Sync | Shot | Background |
|---|---|---|---|---|---|
| D0 | — | Back on the set. | — | W01, 1 s | asleep |
| D1 | LUTHER | "Earl, tell 'em about your mama's Christmas trees." | **LIP-SYNC (LS11)** | CU-L2 | — |
| D2 | EARL | "Silver, green, white, and one she made in ceramics class." | **LIP-SYNC (LS12)** | CU-E2 | — |
| D3 | EARL | "But that little dollar manger never moved. Not one inch." | NO-SYNC | I03, the manger | — |
| D4 | LUTHER | "Like Bedgo." | NO-SYNC | CU-B1 | asleep |
| D5 | — | Pickups, then the song. | — | P01, P02, P03, W02 | asleep on the bass |

### E. Into Mama's Fruitcake (about 18 s)

The joke lands on the fruitcake. Earl's last line is the turn into the song.

| # | Speaker | Line | Sync | Shot | Background |
|---|---|---|---|---|---|
| E0 | — | Back on the set. | — | W01, 1 s | asleep |
| E1 | LUTHER | "Earl. Is that your mama's fruitcake?" | **LIP-SYNC (LS13)** | CU-L2 | — |
| E1b | — | Silent cutaway to the fruitcake. | — | I01, 1 s | — |
| E2 | EARL | "Same recipe since fifty-six." | **LIP-SYNC (LS14)** | CU-E2 | — |
| E3 | LUTHER | "I've put out grease fires that were friendlier." | **LIP-SYNC (LS15)** | CU-L | — |
| E4 | EARL | "Worst fruitcake in Tennessee. And I'd give anything for one more slice." | **LIP-SYNC (LS16)** | CU-E | — |
| E5 | — | Only Earl picks up, with no count-in, and the song starts soft. | — | P01, W02 | asleep on the bass |

### F. Into Two Years Late and Right on Time (about 17 s)

| # | Speaker | Line | Sync | Shot | Background |
|---|---|---|---|---|---|
| F0 | — | Back on the set. | — | W01, 1 s | asleep |
| F1 | LUTHER | "Somebody hand Earl a hankie." | NO-SYNC | CU-E. Earl wipes one eye with a knuckle, lips closed | — |
| F2 | EARL | "Last one tonight. Three wise men, three camels, and a whole lot of wrong turns." | **LIP-SYNC (LS17)** | CU-E | — |
| F3 | LUTHER | "Took them wise men two years to get there. Bedgo'd still be asleep on the camel." | **LIP-SYNC (LS18)** | CU-L | — |
| F4 | — | Pickups, then the song. | — | P02, P03, W02F | **And Friend** in the archway. Asleep on the bass. |

### G. Close (about 24 s)

Two Years Late ends on "Happy birthday, Friend." Cut straight to W02F, which is the second time he is in the archway.

| # | Speaker | Line | Sync | Shot | Background |
|---|---|---|---|---|---|
| G1 | — | Soft applause (sound effect). | — | W02F, 2 s | **And Friend** in the archway. Asleep on the bass. |
| G2 | EARL | "Y'all are welcome to clap. We just don't bow." | **LIP-SYNC (LS19)** | CU-E | — |
| G3 | LUTHER | "Thank you kindly, but we're gonna have to go with no." | **LIP-SYNC (LS20)** | CU-L | — |
| G4 | EARL | "From all of us in Nebo County, Merry Christmas." | **LIP-SYNC (LS21)** | CU-E | — |
| G5 | LUTHER | "And Bedgo slept through the whole thing." | NO-SYNC | CU-B1 | asleep |
| G6a | BEDGO | "...Did I miss it?" One eye cracks open, then both. | **LIP-SYNC (LS22)** | CU-B2 | — |
| G6b | EARL | "The whole show, Bedgo." He is off screen, in the gap inside the same clip. Bedgo's lips are closed for it. | NO-SYNC | CU-B2, same clip | — |
| G6c | BEDGO | "Naw." He glances back over his shoulder toward the archway behind him and smiles a little. "Didn't miss a thing." | **LIP-SYNC (LS22)** | CU-B2, same clip | — |
| G7 | — | Fire and tree lights only. The archway is empty. Fade to black, then the end card. | — | SET01, 3 s | nobody |

"And Bedgo slept through the whole thing" is the last line of Eighteen Wheels, so G5 is a callback. When Bedgo says "Didn't miss a thing," the archway he glances at is empty. Leave that unexplained.

## 3. Shot list

There are 16 stills. Compared with the first draft, the two from-behind stills (SET02 and B01) are gone, and a second close-up angle for each talker (CU-E2 and CU-L2) is added.

Every still is Firefly Gemini Flash at 16:9, run with the repo's Firefly tooling only after Adam approves this plan. Each still is graded before it is used.

Make them in this order, because later stills use earlier approved ones as image 1:

1. SET01
2. W01
3. W02
4. W02F
5. CU-E, CU-E2, CU-L, CU-L2, and CU-B1
6. CU-B2
7. P01, P02, and P03
8. I01, I02, and I03

| Still | Used for |
|---|---|
| SET01 | Empty set: image 1 for the wides, and the last shot |
| W01 | Talking wide: the open, the 1-second beats after each song, and image 1 for the close-ups and pickups |
| W02 | Ready-to-play wide, before songs 1, 2, 4, and 5 |
| W02F | Ready-to-play wide with And Friend, before songs 3 and 6 and the close |
| CU-E | Earl, front, talking to us: 7 clips, plus F1's reaction |
| CU-E2 | Earl, second angle, talking to Luther: 4 clips |
| CU-L | Luther, front, talking to us: 6 clips |
| CU-L2 | Luther, second angle, talking to Earl: 4 clips |
| CU-B1 | Bedgo asleep: A4, A5, B3, D4, and G5 |
| CU-B2 | Bedgo awake: LS22 |
| P01, P02, P03 | Instrument pickups |
| I01, I02, I03 | Fruitcake, CB radio, and manger inserts |

Reference paths:

| Short name | File |
|---|---|
| Shady Full | `E:\Music\The Sackbuts\Art\The Guys\Earl Shady Pruitt\Shady Full.png` |
| Shady Full 2 (guitar) | `E:\Music\The Sackbuts\Art\The Guys\Earl Shady Pruitt\Shady Full 2.png` |
| Shady (face) | `E:\Music\The Sackbuts\Art\The Guys\Earl Shady Pruitt\Shady.png` |
| Mesh Full | `E:\Music\The Sackbuts\Art\The Guys\Luther Mesh McCall\Mesh Full.png` |
| Mesh Full 2 (fiddle) | `E:\Music\The Sackbuts\Art\The Guys\Luther Mesh McCall\Mesh Full 2.png` |
| Mesh (face) | `E:\Music\The Sackbuts\Art\The Guys\Luther Mesh McCall\Mesh.png` |
| Bedgo Full | `E:\Music\The Sackbuts\Art\The Guys\Abner Bedgo Dobbins\Bedgo Full.png` |
| Bedgo Full 2 (upright bass) | `E:\Music\The Sackbuts\Art\The Guys\Abner Bedgo Dobbins\Bedgo Full 2.png` |
| Bedgo (face) | `E:\Music\The Sackbuts\Art\The Guys\Abner Bedgo Dobbins\Bedgo.png` |
| Fruitcake (approved prop) | `E:\Music\The Sackbuts\Art\Additional Characters\Mama's fruitcake - reference.png` |
| Nativity (approved prop) | `E:\Music\The Sackbuts\Art\Additional Characters\The five-and-dime nativity - reference.png` |

And Friend never gets a reference image (`lyricvideo/SACKBUTS_CHARACTER_RULES.md`, rule 5). He is the only person described in words.

Every prompt with people ends with this tail, and the per-shot prompts below say "Tail" in its place:

> Everyone wears exactly the clothes from his or her own reference image. Each person looks exactly like his or her own reference image; keep everyone in the place described and do not swap anyone's position or role. One single seamless photograph, not a collage, split screen or grid of the reference images. Warm 1970s Kodachrome film photograph, slight grain, cinematic 16:9 widescreen, no text or lettering anywhere.

### (a) Set reference

**SET01: the empty set, front camera.** Refs: none. This is an empty plate, so the room is described in words.

```
A cozy 1970s country television Christmas special set, built like a small-town Tennessee living room at night. Warm knotty-pine paneled walls, with a garland of big old-fashioned colored bulbs along the top. On the back wall, left of center, a full Christmas tree with big colored bulbs, silver icicle tinsel and a few bubble lights. Right of center on the back wall, a wide open archway with no door, leading into a dim, unlit hallway. Far right on the back wall, a window with snow outside and one small white church steeple far off in the blue night. Along the back of the set, left to right: a ladder-back wooden chair with a small side table holding an old CB radio base station and its hand microphone; an old wooden church pew with a folded patchwork quilt over its back; a sagging plaid recliner. In front of the pew, a low wooden coffee table with a round red fruitcake tin, a dark fruitcake on a plate, and a small plastic nativity set. On floor stands: an acoustic guitar on a guitar stand beside the pew, a fiddle and bow on a small stand beside the chair, and an upright bass on its stand beside the recliner. A braided rag rug. The camera stands at the front of the set, centered, about twelve feet back from the coffee table, at seated eye height, level, normal lens, aimed at the pew. The front wall with the fireplace is behind the camera, out of frame. Warm lamplight from a floor lamp at frame left, firelight from behind the camera, the tree glowing. No people anywhere in frame. Nobody in the archway. One single seamless photograph. Warm 1970s Kodachrome film photograph, slight grain, cinematic 16:9 widescreen, no text or lettering anywhere.
```

### (b) Wides with the band

**W01: talking wide, instruments on stands.** Refs:

1. SET01
2. Shady Full
3. Mesh Full
4. Bedgo Full
5. Shady (face)
6. Mesh (face)

```
Image 1 sets the camera and the room. Keep its camera position, height, lens, framing, lighting, and every piece of furniture, decoration and instrument exactly. The man in image 3 sits on the ladder-back chair at left, leaning forward with his elbows on his knees. The man in image 2 sits in the middle of the church pew, relaxed, hands folded. The man in image 4 is slumped asleep in the plaid recliner at right, head tipped to one side against the wing of the chair, eyes closed, mouth closed, arms folded. Nobody holds an instrument: the guitar, the fiddle and the upright bass stay on their stands. The archway behind them is empty. The two awake men look toward someone just left of the camera, not into the lens, lips closed. Shallow depth of field: the three men sharp, the tree and archway softer. Image 5 is a close-up of the face of the man in image 2. Image 6 is a close-up of the face of the man in image 3. Tail.
```

**W02: ready-to-play wide.** Refs:

1. SET01
2. Shady Full 2
3. Mesh Full 2
4. Bedgo Full 2
5. Shady (face)
6. Mesh (face)

```
Image 1 sets the camera and the room. Keep its camera position, height, lens, framing, lighting, and every piece of furniture and decoration exactly. The man in image 3 sits forward on the ladder-back chair at left with the fiddle from image 3 tucked under his chin and the bow lifted, ready to play. The man in image 2 sits in the middle of the church pew with the guitar from image 2 on his knee, his hand ready over the strings. The man in image 4 is asleep in the plaid recliner at right with the upright bass from image 4 leaning against him, both arms wrapped around its neck, cheek resting on it, eyes closed, mouth closed. The three instrument stands beside them are empty. The archway behind them is empty. The two awake men look toward someone just left of the camera, not into the lens, lips closed. Shallow depth of field: the three men sharp, the tree and archway softer. Image 5 is a close-up of the face of the man in image 2. Image 6 is a close-up of the face of the man in image 3. Tail.
```

**W02F: the ready wide with And Friend.** It is made from the approved W02. Refs:

1. W02, approved
2. Shady Full 2
3. Mesh Full 2
4. Bedgo Full 2

```
Image 1 is the frame to keep. Keep its camera, framing, lighting, and every person, instrument and object exactly where and how they are in image 1. The man on the pew is the man in image 2, the man on the ladder-back chair is the man in image 3, and the man asleep in the recliner holding the upright bass is the man in image 4. The only change: deep in the dim archway behind them, a fourth man stands quietly, small and soft in the shadow, in a plain dark coat. His face is not readable. He has no glow, no halo, and no light on him. He does not look at the camera. Tail.
```

### (c) Close-ups for the people who talk

Each close-up is made from the approved W01, used as image 1, per `lyricvideo/PROCESS.md` section 4.3. Nobody else is in frame, so OmniHuman cannot give a second face lips.

If Firefly keeps W01's wide camera, crop W01 for the review copy. If that crop is too soft, make an empty close plate of that seat from the new camera first, then put the man in.

The two angles for each talker differ in camera side and eyeline:

- The front close-up talks to us.
- The second angle is turned toward the other man.

**CU-E: Earl, front.** Refs:

1. W01, approved
2. Shady (face)
3. Shady Full

```
Image 1 is the scene. Show the exact same moment from a second camera at seated eye height in front of the pew: a close-up from mid-chest up of the man sitting in the middle of the church pew in image 1, who is the man in image 2. Image 2 is only his face; take nothing else from image 2. Image 3 is only his clothes; take nothing else from image 3. Keep his pose, the warm lamplight, and the Christmas tree glowing soft behind his shoulder. He looks toward someone just beside the camera, not into the lens, relaxed, lips closed. Nobody else is in frame. Tail.
```

**CU-E2: Earl, second angle, turned toward Luther.** Refs:

1. W01, approved
2. Shady (face)
3. Shady Full

```
Image 1 is the scene. Show the exact same moment from a third camera set to the left of the pew at seated eye height, angled across at him: a three-quarter close-up from mid-chest up of the man sitting in the middle of the church pew in image 1, who is the man in image 2. Image 2 is only his face; take nothing else from image 2. Image 3 is only his clothes; take nothing else from image 3. He is turned toward someone just left of the camera, not into the lens, lips closed. Behind him, soft and out of focus: the knotty-pine back wall, the dim empty archway, and the snowy window. Warm lamplight on the side of his face. Nobody else is in frame. Tail.
```

**CU-L: Luther, front.** Refs:

1. W01, approved
2. Mesh (face)
3. Mesh Full

```
Image 1 is the scene. Show the exact same moment from a second camera at seated eye height in front of the ladder-back chair: a close-up from mid-chest up of the man sitting on the ladder-back chair in image 1, who is the man in image 2. Image 2 is only his face; take nothing else from image 2. Image 3 is only his clothes; take nothing else from image 3. He leans forward a little, elbows on his knees. The old CB radio on the side table sits soft at the edge of the frame, and the knotty-pine wall is behind him. He looks toward someone just beside the camera, not into the lens, lips closed. Nobody else is in frame. Tail.
```

**CU-L2: Luther, second angle, turned toward Earl.** Refs:

1. W01, approved
2. Mesh (face)
3. Mesh Full

```
Image 1 is the scene. Show the exact same moment from a third camera set to the right of the ladder-back chair at seated eye height, angled across at him: a three-quarter close-up from mid-chest up of the man sitting on the ladder-back chair in image 1, who is the man in image 2. Image 2 is only his face; take nothing else from image 2. Image 3 is only his clothes; take nothing else from image 3. He sits back in the chair, turned toward someone just right of the camera, not into the lens, lips closed. Behind him, soft and out of focus: the big colored bulbs of the Christmas tree and the knotty-pine wall. Nobody else is in frame. Tail.
```

**CU-B1: Bedgo asleep.** Refs:

1. W01, approved
2. Bedgo (face)
3. Bedgo Full

```
Image 1 is the scene. Show the exact same moment from a second camera at seated eye height in front of the recliner: a close-up from mid-chest up of the man asleep in the plaid recliner in image 1, who is the man in image 2. Image 2 is only his face; take nothing else from image 2. Image 3 is only his clothes; take nothing else from image 3. He is deeply asleep, head tipped against the wing of the chair, eyes closed, mouth closed, arms folded. Behind him, the dim archway is soft and empty. Nobody else is in frame. Tail.
```

**CU-B2: Bedgo awake.** It is made from the approved CU-B1. Refs:

1. CU-B1, approved
2. Bedgo (face)

```
Image 1 is the frame to keep: the same camera, framing, light, chair and clothes, and the same dim, empty archway behind him. The man in image 1 is the man in image 2; take only his face from image 2. The only change: he has just woken up. His eyes are open and heavy-lidded, his head is lifted a little off the chair, and he looks off toward the left of the frame, not into the lens, lips closed. Nobody else is in frame. Tail.
```

### (d) Instrument pickups

There are no faces talking in these, so none of them needs lip sync.

**P01: Earl's guitar pickup.** Refs:

1. W01, approved
2. Shady Full 2

```
Image 1 is the scene. Show the exact same moment from a second camera, low and close beside the pew at frame left, framed from the shoulders down. The man sitting on the pew in image 1, who is the man in image 2, has just lifted the guitar from image 2 off its stand and settled it on his knee, his right hand resting over the strings and his left hand on the neck. His face is above the top of the frame. The empty guitar stand is beside his boot. Warm lamplight. Tail.
```

**P02: Luther's fiddle pickup.** Refs:

1. W01, approved
2. Mesh Full 2
3. Mesh (face)

```
Image 1 is the scene. Show the exact same moment from a second camera at seated eye height in front of the ladder-back chair: a medium close shot of the man on the chair in image 1, who is the man in image 2, who has just tucked the fiddle from image 2 under his chin and lifted the bow, eyes down on the strings, lips closed. The empty fiddle stand is beside his chair. Image 3 is a close-up of the face of the man in image 2. Nobody else is in frame. Tail.
```

**P03: the bass goes to sleeping Bedgo.** Refs:

1. W01, approved
2. Bedgo Full 2
3. Mesh Full
4. Bedgo (face)

The still shows the moment just after the handoff.

```
Image 1 is the scene. Show the exact same moment from a second camera at seated eye height in front of the recliner: a medium shot of the man asleep in the plaid recliner in image 1, who is the man in image 2. The upright bass from image 2 now leans against him, and in his sleep his arms have wrapped around its neck, cheek resting on it, eyes closed, mouth closed. At the left edge of the frame, only the arm and hand of the man in image 3 show, from the shoulder down, his face out of frame, just letting go of the neck of the bass. Image 4 is a close-up of the face of the man in image 2. Tail.
```

### Inserts

**I01: the fruitcake.** Refs:

1. Fruitcake

If the reference's camera is not a close tabletop angle, crop W01's coffee table instead.

```
A close tabletop shot of the fruitcake in image 1, on a plate on a low wooden coffee table, with a round red fruitcake tin beside it. The fruitcake looks exactly like image 1. Behind it, soft and out of focus: knotty-pine paneling and the big colored bulbs of a Christmas tree. Warm lamplight. No people and no hands. One single seamless photograph. Warm 1970s Kodachrome film photograph, slight grain, cinematic 16:9 widescreen, no text or lettering anywhere.
```

**I02: the CB radio.** Refs: none.

```
A close shot of an old 1970s CB radio base station on a small wooden side table, its coiled cord and hand microphone resting in front of it, the dial lit a warm amber. Behind it, soft and out of focus: knotty-pine paneling and the big colored bulbs of a Christmas tree. Warm lamplight. No people and no hands. One single seamless photograph. Warm 1970s Kodachrome film photograph, slight grain, cinematic 16:9 widescreen, no text or lettering anywhere, no numbers on the dial.
```

**I03: the manger.** Refs:

1. Nativity

```
A close tabletop shot of the nativity set in image 1 on a low wooden coffee table, the baby in the manger at the center. The nativity looks exactly like image 1. A round red fruitcake tin sits soft at the edge of the frame. Behind it, soft and out of focus: knotty-pine paneling and the big colored bulbs of a Christmas tree. Warm lamplight on the manger. No people and no hands. One single seamless photograph. Warm 1970s Kodachrome film photograph, slight grain, cinematic 16:9 widescreen, no text or lettering anywhere.
```

### Motion for the shots that are not lip-synced

These get motion in Dream Machine, one clip each, extended once only where a shot plays longer than about 5.3 seconds:

- SET01
- W01, W02, and W02F
- CU-B1
- CU-E, for F1's reaction only
- P01, P02, and P03
- I01, I02, and I03

Every motion prompt says real time, normal speed, small natural movement, and the fire flickering and the tree lights twinkling. It never tells the background to hold still.

Every prompt with a face says his lips stay closed. If Dream Machine moves a closed mouth anyway, push in on the still in the edit instead.

| Shot | Motion |
|---|---|
| CU-B1 | His eyes stay closed and his chest rises and falls. If he wakes, use the still with a slow push in the edit. |
| CU-E, for F1 | He wipes one eye with a knuckle and gives a small embarrassed smile. |
| W02F | And Friend stays still and soft. Nobody turns toward him. |

## 4. Voice and lip sync

### Voices: MiniMax TTS

Every spoken line is made with **MiniMax text-to-speech** on our MiniMax API. **Adam trains each character's voice himself**, one voice each for Earl, Luther, and Bedgo. Fill in each voice ID here when he has it:

| Character | Voice ID | Starting settings | Read |
|---|---|---|---|
| Earl | ____ | speed 0.95 | Warm, gravelly baritone with a heavy Southern twang. Plain and unhurried; he hosts. Sincere on E4: no wink, and the joke stops before "one more slice." |
| Luther | ____ | speed 1.08 | The fast talker. Quicker and a little higher than Earl, with a grin in the voice. |
| Bedgo | ____ | speed 0.85 | Low, sleepy, deadpan bass, almost a mumble. Never a laugh or a big reaction. |

The character reads come from `band/bible.md`, plus Tinsel's spoken-line direction for Bedgo. The speeds are only a first try. Adam's ear decides.

And Friend has no voice and no lines.

**Format.** WAV, 44.1 kHz, mono, one file per line, saved in `lyricvideo/sackbuts/christmas-special/audio/voice/`.

**Text.** The text sent to MiniMax is the script line exactly. If MiniMax misreads a word, change the spelling in the text sent to MiniMax only, keep the script as written, and note the change beside that file.

**Who generates them.** Once the three voice IDs exist, an agent generates all 31 files. Adam listens and approves them before any lip sync runs.

| Line | Character | Text | File | Sync |
|---|---|---|---|---|
| A2 | Earl | Evenin', and Merry Christmas from Nebo County, Tennessee. We're the Sackbuts. | `A2_earl.wav` | LS01 |
| A3 | Luther | I'm Luther. That there's Earl. And that's Bedgo. | `A3_luther.wav` | LS02 |
| A5 | Earl | He's been like that since Thanksgiving. | `A5_earl.wav` | NO-SYNC |
| A6 | Luther | ...And Friend. | `A6_luther.wav` | LS03 |
| A7 | Earl | Anyhow. First one's about a horse that won't move unless you quote him Scripture. | `A7_earl.wav` | LS04 |
| A8 | Luther | Bedgo knows the short one. | `A8_luther.wav` | LS05 |
| A10 | Luther | One, two... | `A10_luther.wav` | NO-SYNC |
| B1 | Earl | Dewey's twenty-six, and he still runs better than The Furnace. | `B1_earl.wav` | LS06 |
| B2 | Luther | One Christmas Eve The Furnace quit, and we slept in a barn with a cow, a donkey, and Bedgo. Hard to tell which one was snorin'. | `B2_luther.wav` | LS07 |
| C1 | Luther | Breaker one-nine, this here's Firehose. Come on. | `C1_luther.wav` | NO-SYNC. CB filter goes on in the edit. |
| C2 | Earl | Luther. We're on television. | `C2_earl.wav` | LS08 |
| C3 | Luther | Old habit. | `C3_luther.wav` | LS09 |
| C4 | Earl | This next one's forty truckers, one blizzard, and a baby that would not wait. | `C4_earl.wav` | LS10 |
| D1 | Luther | Earl, tell 'em about your mama's Christmas trees. | `D1_luther.wav` | LS11 |
| D2 | Earl | Silver, green, white, and one she made in ceramics class. | `D2_earl.wav` | LS12 |
| D3 | Earl | But that little dollar manger never moved. Not one inch. | `D3_earl.wav` | NO-SYNC |
| D4 | Luther | Like Bedgo. | `D4_luther.wav` | NO-SYNC |
| E1 | Luther | Earl. Is that your mama's fruitcake? | `E1_luther.wav` | LS13 |
| E2 | Earl | Same recipe since fifty-six. | `E2_earl.wav` | LS14 |
| E3 | Luther | I've put out grease fires that were friendlier. | `E3_luther.wav` | LS15 |
| E4 | Earl | Worst fruitcake in Tennessee. And I'd give anything for one more slice. | `E4_earl.wav` | LS16 |
| F1 | Luther | Somebody hand Earl a hankie. | `F1_luther.wav` | NO-SYNC |
| F2 | Earl | Last one tonight. Three wise men, three camels, and a whole lot of wrong turns. | `F2_earl.wav` | LS17 |
| F3 | Luther | Took them wise men two years to get there. Bedgo'd still be asleep on the camel. | `F3_luther.wav` | LS18 |
| G2 | Earl | Y'all are welcome to clap. We just don't bow. | `G2_earl.wav` | LS19 |
| G3 | Luther | Thank you kindly, but we're gonna have to go with no. | `G3_luther.wav` | LS20 |
| G4 | Earl | From all of us in Nebo County, Merry Christmas. | `G4_earl.wav` | LS21 |
| G5 | Luther | And Bedgo slept through the whole thing. | `G5_luther.wav` | NO-SYNC |
| G6a | Bedgo | ...Did I miss it? | `G6a_bedgo.wav` | LS22 |
| G6b | Earl | The whole show, Bedgo. | `G6b_earl.wav` | NO-SYNC. It sits in the gap inside LS22. |
| G6c | Bedgo | Naw. Didn't miss a thing. | `G6c_bedgo.wav` | LS22 |

That is 31 files: 14 for Earl, 15 for Luther, and 2 for Bedgo.

The snore and the applause are sound effects from the library, not text-to-speech.

### Lip-sync method

This is the same as I Still Care About Your Christmas, from `lyricvideo/songs/i-still-care/run_lipsync.py` and `lyricvideo/PROCESS.md` section 4.5.

- **Model and size:** OmniHuman 1.5 through Hedra, 1080p, solo close-ups only.
- **Driving audio:** built from the approved voice file, saved in `lyricvideo/sackbuts/christmas-special/lipsync/in/LSnn.wav`. Each one starts 0.5 s before the line and ends 1.0 s after it, or 2.0 s after on the punchline clips. It gets `highshelf=f=3000:g=5` for consonants. Record `pad_in` so the edit skips the lead-in.
- **LS22:** the driving audio is `G6a_bedgo.wav`, then silence the exact length of `G6b_earl.wav`, then `G6c_bedgo.wav`. Earl's line goes on the edit audio only.
- **Cost:** each run is paid, so it stays with the main agent. Run `hedra.py estimate` first, check the wallet with `hedra.py balance`, and log the spend against the 150-second plan and the 181-second hard stop.
- **Stalls:** a job stuck at 90% for more than 10 minutes gets killed and resubmitted.
- **Redos:** these come out of the 34-second reserve, worst clip first.

Base prompt for all 22 clips:

> Footage of a man talking on the set of a cozy 1970s country Christmas television special, real time, normal speed. The camera holds the same close framing the whole time, with only a slight natural handheld sway; it does not zoom or push in. He keeps the same face, hair, and clothes from the first frame to the last. His lips match his voice and close fully between phrases. He never looks into the lens. The fire flickers warm light across the knotty-pine wall, and the Christmas tree lights twinkle softly behind him.

What each still adds to the base prompt:

| Still | Add |
|---|---|
| CU-E and CU-L | He talks to someone just beside the camera. |
| CU-E2 and CU-L2 | He talks across to the man sitting beside him, off screen. |
| Punchline clips | After the last word he holds a small grin, or for E4 a quiet look down, until the clip ends. |

What each clip adds:

| Clip | Add |
|---|---|
| LS03 | He glances back over his shoulder toward the back of the room. |
| LS04 | He starts with a small smile before "Anyhow." |
| LS09 | Sheepish. |
| LS16 | Quiet and sincere. His eyes drop on "one more slice." |
| LS22 | Heavy-lidded. His lips stay closed in the pause between his two lines. On the last line he glances back over his shoulder toward the room behind him and smiles slightly. |

## Before anything is made

1. Adam approves this plan.
2. Adam trains the three MiniMax voices.
3. An agent generates the 31 voice files, and Adam approves them.
4. The stills are made and graded, then the motion, then the 22 lip-sync clips.
5. The five song lyric videos need to be finished in his Premiere project first. The special's edit is a new sequence, and his project is not written to.
