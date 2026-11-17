# A Very Sackbuts Christmas: the special

Written November 17, 2026, for Adam. Plan and script only. No image, clip, or audio was made, nothing was posted, and nothing under `E:\` changed.

One long YouTube video: the six album songs, with short host segments between them in one Sackbuts living-room set. It is built from 16 stills that get reused, plus 5 lip-sync clips.

## 1. Plan

### Runtime

| Part | Length |
|---|---|
| Six songs, as their own lyric videos | 26:57 |
| Open, five song intros, and the close | about 2:05 |
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
| A | Open, then into Sleigh Ride | about 25 s | LS1 Earl |
| B | Into Stuck in a Stable | about 15 s | LS2 Luther |
| C | Into Eighteen Wheels | about 14 s | none |
| D | Into Tinsel | about 15 s | none |
| E | Into Mama's Fruitcake | about 16 s | LS3 Earl |
| F | Into Two Years Late | about 15 s | LS4 Luther |
| G | Close | about 24 s | LS5 Bedgo |

### Lip-sync budget

**5 lip-sync clips, about 26.5 seconds of speech.** Each clip gets 0.5 s of driving audio before and 1.0 s after, so about **34 seconds** is billed. OmniHuman 1.5 at 1080p is about $0.165 per second, so the estimate is **about $5.60**. Run `hedra.py estimate` first. Every other line is NO-SYNC.

| Clip | Speaker | Segment | Speech | Padded |
|---|---|---|---|---|
| LS1 | Earl | A | 4.5 s | 6.0 s |
| LS2 | Luther | B | 6.5 s | 8.0 s |
| LS3 | Earl | E | 4.5 s | 6.0 s |
| LS4 | Luther | F | 5.0 s | 6.5 s |
| LS5 | Bedgo | G | 6.0 s | 7.5 s |
| **Total** | | | **26.5 s** | **34.0 s** |

How the other lines keep mouths out of the picture:

- **From behind** (B01): the three backs facing the fire.
- **The listener**: one man talks off screen while we watch the other one, with his lips closed.
- **Inserts**: the fruitcake, the CB radio, and the manger.
- **Hands**: the instrument pickups.
- **Bedgo asleep**: anyone can talk over him.
- **The wides**: a voice over W01 or W02 only on a short line, where the faces are small.

## 2. Script

Speaker names are for this script only. No one says them on screen unless the line does.

Shot codes are in section 3. "Lips closed" means the Dream Machine prompt for that clip says his lips stay closed.

**Standing rules for every segment**

- **Bedgo** is asleep in the recliner for every talking line until G. His eyes are closed, he never moves on his own, and he snores (sound effect) only where marked. When a song starts, he is still asleep with the bass in his arms.
- **And Friend** appears only in W02F, before songs 3 and 6 and at the start of the close. He is always small and soft, deep in the dim archway at the back, in a plain dark coat, with no readable face. He has no glow, no halo, and no light on him. Nobody points at him or explains him. When he comes up, the boys smile and change the subject.
- **Instruments** stay on their stands whenever anyone is talking. Each song lead-in is a quick run of pickups: Earl's guitar (P01), Luther's fiddle (P02), and Luther leaning the bass into sleeping Bedgo's arms (P03). Then comes the ready wide (W02 or W02F), and the song starts. After each song we cut back to W01, with the instruments on their stands again.

### A. Open, into Nebo County Sleigh Ride (about 25 s)

| # | Speaker | Line | Sync | Shot | Background |
|---|---|---|---|---|---|
| A1 | — | Fire crackle, tree lights. The logo goes on here in the edit. | — | W01, slow push in, 3 s | Bedgo asleep |
| A2 | EARL | "Evenin', and Merry Christmas from Nebo County, Tennessee. We're the Sackbuts." | **LIP-SYNC (LS1)** | CU-E | — |
| A3 | LUTHER | "I'm Luther. That there's Earl. And that's Bedgo." | NO-SYNC | B01, from behind | Bedgo's head tipped over the recliner |
| A4 | — | Snore. | — | CU-B1, 1.5 s | asleep |
| A5 | EARL | "He's been like that since Thanksgiving." | NO-SYNC | CU-B1, held | asleep |
| A6 | LUTHER | "...And Friend." | NO-SYNC | CU-E. Earl smiles a little, glances toward the back of the room, lips closed | — |
| A7 | EARL | "Anyhow." | NO-SYNC | W01 | — |
| A8 | EARL | "First one's about a horse that won't move unless you quote him Scripture." | NO-SYNC | P01, guitar pickup | — |
| A9 | LUTHER | "Bedgo knows the short one." | NO-SYNC | P02, fiddle pickup | — |
| A10 | — | Luther leans the bass into Bedgo. Bedgo hugs it without waking. | — | P03, 2 s | asleep |
| A11 | LUTHER | "One, two..." The song starts. | NO-SYNC | W02 | asleep on the bass |

"The short one" is "Jesus wept." It is the line that gets Dewey moving in the song, so this only sets it up and does not spoil it.

### B. Into Stuck in a Stable on Christmas (about 15 s)

| # | Speaker | Line | Sync | Shot | Background |
|---|---|---|---|---|---|
| B1 | EARL | "Dewey's twenty-six, and he still runs better than The Furnace." | NO-SYNC | B01 | asleep |
| B2 | LUTHER | "One Christmas Eve The Furnace quit, and we slept in a barn with a cow, a donkey, and Bedgo. Hard to tell which one was snorin'." | **LIP-SYNC (LS2)** | CU-L | — |
| B3 | — | Snore. | — | CU-B1, 1.5 s | asleep |
| B4 | — | Pickups, then the song. | — | P01, P03, W02 | asleep on the bass |

### C. Into Eighteen Wheels and a Prayer (about 14 s)

| # | Speaker | Line | Sync | Shot | Background |
|---|---|---|---|---|---|
| C1 | LUTHER | "Breaker one-nine, this here's Firehose. Come on." It is filtered to sound like it is coming through the CB. | NO-SYNC | I02, CB radio | — |
| C2 | EARL | "Luther. We're on television." | NO-SYNC | B01 | asleep |
| C3 | LUTHER | "Old habit." | NO-SYNC | B01, continued | asleep |
| C4 | EARL | "This next one's forty truckers, one blizzard, and a baby that would not wait." | NO-SYNC | P01 | — |
| C5 | — | Pickups, then the song. | — | P02, P03, W02F | **And Friend** in the archway, first time. Asleep on the bass. |

### D. Into The Tinsel Comes and Goes (about 15 s)

| # | Speaker | Line | Sync | Shot | Background |
|---|---|---|---|---|---|
| D1 | LUTHER | "Earl, tell 'em about your mama's Christmas trees." | NO-SYNC | W01 | asleep |
| D2 | EARL | "Silver, green, white, and one she made in ceramics class." | NO-SYNC | I03, the manger | — |
| D3 | EARL | "But that little dollar manger never moved. Not one inch." | NO-SYNC | CU-L. Luther listens and nods, lips closed | — |
| D4 | LUTHER | "Like Bedgo." | NO-SYNC | CU-B1 | asleep |
| D5 | — | Pickups, then the song. | — | P01, P02, P03, W02 | asleep on the bass |

### E. Into Mama's Fruitcake (about 16 s)

The joke lands on the fruitcake. Earl's line is the turn, so it gets a lip-sync clip.

| # | Speaker | Line | Sync | Shot | Background |
|---|---|---|---|---|---|
| E1 | LUTHER | "Earl. Is that your mama's fruitcake?" | NO-SYNC | I01, fruitcake | — |
| E2 | EARL | "Same recipe since fifty-six." | NO-SYNC | CU-L. Luther eyes it warily, lips closed | — |
| E3 | LUTHER | "I've put out grease fires that were friendlier." | NO-SYNC | B01 | asleep |
| E4 | EARL | "Worst fruitcake in Tennessee. And I'd give anything for one more slice." | **LIP-SYNC (LS3)** | CU-E | — |
| E5 | — | Only Earl picks up, with no count-in, and the song starts soft. | — | P01, W02 | asleep on the bass |

### F. Into Two Years Late and Right on Time (about 15 s)

| # | Speaker | Line | Sync | Shot | Background |
|---|---|---|---|---|---|
| F1 | LUTHER | "Somebody hand Earl a hankie." | NO-SYNC | CU-E. Earl wipes one eye with a knuckle, lips closed | — |
| F2 | EARL | "Last one tonight. Three wise men, three camels, and a whole lot of wrong turns." | NO-SYNC | B01 | asleep |
| F3 | LUTHER | "Took them wise men two years to get there. Bedgo'd still be asleep on the camel." | **LIP-SYNC (LS4)** | CU-L | — |
| F4 | — | Pickups, then the song. | — | P02, P03, W02F | **And Friend** in the archway. Asleep on the bass. |

### G. Close (about 24 s)

Two Years Late ends on "Happy birthday, Friend." Cut straight to W02F, which is the second time he is in the archway.

| # | Speaker | Line | Sync | Shot | Background |
|---|---|---|---|---|---|
| G1 | — | Soft applause (sound effect). | — | W02F, 2 s | **And Friend** in the archway. Asleep on the bass. |
| G2 | EARL | "Y'all are welcome to clap. We just don't bow." | NO-SYNC | B01 | asleep |
| G3 | LUTHER | "Thank you kindly, but we're gonna have to go with no." | NO-SYNC | B01, continued | asleep |
| G4 | EARL | "From all of us in Nebo County, Merry Christmas." | NO-SYNC | I03, the manger | — |
| G5 | LUTHER | "And Bedgo slept through the whole thing." | NO-SYNC | CU-B1 | asleep |
| G6 | BEDGO | "...Did I miss it?" | **LIP-SYNC (LS5)** | CU-B2. One eye cracks open, then both. | — |
| G6 | EARL | "The whole show, Bedgo." He is off screen, in the gap inside the same clip. Bedgo's lips are closed for it. | NO-SYNC | CU-B2, same clip | — |
| G6 | BEDGO | "Naw." He glances back over his shoulder toward the archway behind him and smiles a little. "Didn't miss a thing." | **LIP-SYNC (LS5)** | CU-B2, same clip | — |
| G7 | — | Fire and tree lights only. The archway is empty. Fade to black, then the end card. | — | SET01, 3 s | nobody |

"And Bedgo slept through the whole thing" is the last line of Eighteen Wheels, so G5 is a callback. When Bedgo says "Didn't miss a thing," the archway he glances at is empty. Leave that unexplained.

## 3. Shot list

There are 16 stills. Every still is Firefly Gemini Flash at 16:9, run with the repo's Firefly tooling only after Adam approves this plan. Each still is graded before it is used.

Make them in this order, because later stills use earlier approved ones as image 1:

1. SET01
2. SET02
3. W01
4. W02
5. W02F
6. B01
7. CU-E, CU-L, and CU-B1
8. CU-B2
9. P01, P02, and P03
10. I01, I02, and I03

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

### (a) Set references

**SET01: the empty set, front camera.** Refs: none. This is an empty plate, so the room is described in words.

```
A cozy 1970s country television Christmas special set, built like a small-town Tennessee living room at night. Warm knotty-pine paneled walls, with a garland of big old-fashioned colored bulbs along the top. On the back wall, left of center, a full Christmas tree with big colored bulbs, silver icicle tinsel and a few bubble lights. Right of center on the back wall, a wide open archway with no door, leading into a dim, unlit hallway. Far right on the back wall, a window with snow outside and one small white church steeple far off in the blue night. Along the back of the set, left to right: a ladder-back wooden chair with a small side table holding an old CB radio base station and its hand microphone; an old wooden church pew with a folded patchwork quilt over its back; a sagging plaid recliner. In front of the pew, a low wooden coffee table with a round red fruitcake tin, a dark fruitcake on a plate, and a small plastic nativity set. On floor stands: an acoustic guitar on a guitar stand beside the pew, a fiddle and bow on a small stand beside the chair, and an upright bass on its stand beside the recliner. A braided rag rug. The camera stands at the front of the set, centered, about twelve feet back from the coffee table, at seated eye height, level, normal lens, aimed at the pew. The front wall with the fireplace is behind the camera, out of frame. Warm lamplight from a floor lamp at frame left, firelight from behind the camera, the tree glowing. No people anywhere in frame. Nobody in the archway. One single seamless photograph. Warm 1970s Kodachrome film photograph, slight grain, cinematic 16:9 widescreen, no text or lettering anywhere.
```

**SET02: the empty set, reverse camera from behind the seats.** Refs: none. No kept still has this camera yet, so the room is described in the same words.

```
The same cozy 1970s country television Christmas special set, a small-town Tennessee living room at night with warm knotty-pine paneled walls and a garland of big old-fashioned colored bulbs along the top. The camera stands at the back of the set, just in front of a dim open archway, at seated eye height, level, normal lens, aimed at the front wall. In the foreground, seen from behind: a ladder-back wooden chair at left with a small side table holding an old CB radio, an old wooden church pew in the middle with a folded patchwork quilt over its back, and a sagging plaid recliner at right, all empty. An acoustic guitar, a fiddle and an upright bass stand on floor stands beside them. Just past the seats, a low wooden coffee table with a round red fruitcake tin. Beyond it, the front wall: a fieldstone fireplace with a crackling fire, four plain red stockings hanging from the mantel, pine garland with big colored bulbs on the mantel, and a red fire extinguisher on the floor beside the hearth. The firelight is the main light, warm on the backs of the seats. No people anywhere in frame. One single seamless photograph. Warm 1970s Kodachrome film photograph, slight grain, cinematic 16:9 widescreen, no text or lettering anywhere.
```

The fourth stocking is set dressing. Never point at it.

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

**W02: ready-to-play wide.** It is used before every song. Refs:

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

**B01: from behind the seats, faces hidden.** It carries most of the NO-SYNC lines. Refs:

1. SET02
2. Shady Full
3. Mesh Full
4. Bedgo Full

```
Image 1 sets the camera and the room. Keep its camera position, height, lens, framing, firelight, and every piece of furniture and decoration exactly. The three men are seen from behind, facing the fireplace. The man in image 3 sits on the ladder-back chair at left, the back of his head and his shoulders toward the camera, turned a little toward the pew. The man in image 2 sits in the middle of the church pew with his back to the camera. The man in image 4 is slumped asleep in the plaid recliner at right; only the top of his head shows above the chair back, tipped to one side. None of their faces are visible. Firelight rims their heads and shoulders. Nobody holds an instrument; the instruments stay on their stands. Tail.
```

### (c) Close-ups for the people who talk

Each close-up is made from the approved W01, used as image 1, per `lyricvideo/PROCESS.md` section 4.3. Nobody else is in frame, so OmniHuman cannot give a second face lips.

If Firefly keeps W01's wide camera, crop W01 for the review copy. If that crop is too soft, make an empty close plate of that seat from the new camera first, then put the man in.

**CU-E: Earl.** It is used for LS1 and LS3, and for two listener moments with his lips closed. Refs:

1. W01, approved
2. Shady (face)
3. Shady Full

```
Image 1 is the scene. Show the exact same moment from a second camera at seated eye height in front of the pew: a close-up from mid-chest up of the man sitting in the middle of the church pew in image 1, who is the man in image 2. Image 2 is only his face; take nothing else from image 2. Image 3 is only his clothes; take nothing else from image 3. Keep his pose, the warm lamplight, and the Christmas tree glowing soft behind his shoulder. He looks toward someone just left of the camera, not into the lens, relaxed, lips closed. Nobody else is in frame. Tail.
```

**CU-L: Luther.** It is used for LS2 and LS4, and for two listener moments. Refs:

1. W01, approved
2. Mesh (face)
3. Mesh Full

```
Image 1 is the scene. Show the exact same moment from a second camera at seated eye height in front of the ladder-back chair: a close-up from mid-chest up of the man sitting on the ladder-back chair in image 1, who is the man in image 2. Image 2 is only his face; take nothing else from image 2. Image 3 is only his clothes; take nothing else from image 3. He leans forward a little, elbows on his knees. The old CB radio on the side table sits soft at the edge of the frame, and the knotty-pine wall is behind him. He looks toward someone just right of the camera, not into the lens, lips closed. Nobody else is in frame. Tail.
```

**CU-B1: Bedgo asleep.** It is used under NO-SYNC lines throughout. Refs:

1. W01, approved
2. Bedgo (face)
3. Bedgo Full

```
Image 1 is the scene. Show the exact same moment from a second camera at seated eye height in front of the recliner: a close-up from mid-chest up of the man asleep in the plaid recliner in image 1, who is the man in image 2. Image 2 is only his face; take nothing else from image 2. Image 3 is only his clothes; take nothing else from image 3. He is deeply asleep, head tipped against the wing of the chair, eyes closed, mouth closed, arms folded. Behind him, the dim archway is soft and empty. Nobody else is in frame. Tail.
```

**CU-B2: Bedgo awake.** It is used only for LS5 and is made from the approved CU-B1. Refs:

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

These have no people and make cheap cover for NO-SYNC lines.

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

### Motion for the NO-SYNC shots

The NO-SYNC shots get motion in Dream Machine, one clip each, extended once only where it plays longer than about 5.3 seconds. B01 and W01 need the extend. Nothing else does.

Every motion prompt says real time, normal speed, small natural movement, and the fire flickering and the tree lights twinkling. It never tells the background to hold still.

Every prompt with a face says his lips stay closed. If Dream Machine moves a closed mouth anyway, push in on the still in the edit instead.

| Shot | Motion |
|---|---|
| CU-B1 | His eyes stay closed and his chest rises and falls. If he wakes, use the still with a slow push in the edit. |
| CU-E, as listener | A small smile, a glance toward the back of the room. For F1, one knuckle to the eye. |
| CU-L, as listener | A slow nod. For E2, a wary sideways look. |
| W02F | And Friend stays still and soft. Nobody turns toward him. |

## 4. Voice and lip sync

### Where the voices come from

The repo has no tool for the band's speaking voices. Before any lip sync, each line needs a dry recording: one wav per line, 48 kHz, named by line id (for example `A2_earl.wav`). How those get made is Adam's call. The lines must sound like the singers on the songs.

### The characters

**Earl** (`band/bible.md`)

- Warm, gravelly baritone with a heavy Southern twang.
- Plain and unhurried. He hosts.
- Sincere on LS3: no wink, and the joke stops before "one more slice."
- He speaks in A2, A5, A7, A8, B1, C2, C4, D2, D3, E2, E4, F2, G2, G4, and G6.

**Luther** (`band/bible.md`)

- The fast talker, who handles the banter.
- Quicker and a little higher than Earl, with a grin in the voice.
- C1 is the CB voice: same reading, run through a radio filter in the edit.
- He speaks in A3, A6, A9, A11, B2, C1, C3, D1, D4, E1, E3, F1, F3, G3, and G5.

**Bedgo** (`band/bible.md`, and Tinsel's spoken-line direction)

- Low, sleepy, deadpan bass, almost a mumble.
- He speaks only in G6. That is two short lines, and the second is the wise one.
- Never give him a laugh or a big reaction.

**And Friend** has no voice and no lines.

### Lip-sync method

This is the same as I Still Care About Your Christmas, from `lyricvideo/songs/i-still-care/run_lipsync.py` and `lyricvideo/PROCESS.md` section 4.5.

- **Model and size:** OmniHuman 1.5 through Hedra, 1080p, solo close-ups only.
- **Driving audio:** that line's dry voice from 0.5 s before to 1.0 s after, with `highshelf=f=3000:g=5` for consonants. Record `pad_in` so the edit skips the lead-in.
- **LS5:** the driving audio is Bedgo's two lines, with silence the length of Earl's line between them. Earl's line goes on the edit audio only.
- **Cost:** each run is paid, so it stays with the main agent. Run `hedra.py estimate` first, check the wallet with `hedra.py balance`, and log the spend.
- **Stalls:** a job stuck at 90% for more than 10 minutes gets killed and resubmitted.

Base prompt for all five clips:

> Footage of a man talking on the set of a cozy 1970s country Christmas television special, real time, normal speed. The camera holds the same close framing the whole time, with only a slight natural handheld sway; it does not zoom or push in. He keeps the same face, hair, and clothes from the first frame to the last. His lips match his voice and close fully between phrases. He talks to someone just beside the camera and never looks into the lens. The fire flickers warm light across the knotty-pine wall, and the Christmas tree lights twinkle softly behind him.

What each clip adds to the base prompt:

| Clip | Add |
|---|---|
| LS1 | Earl, friendly, welcoming. |
| LS2 | Luther, quick, enjoying his own joke, leaning forward on his elbows. |
| LS3 | Earl, quiet and sincere. His eyes drop for a moment on "one more slice." |
| LS4 | Luther, deadpan, a small grin at the end. |
| LS5 | Bedgo, heavy-lidded. His lips stay closed in the pause between his two lines. On the last line he glances back over his shoulder toward the room behind him and smiles slightly. |

## Before anything is made

- Adam approves this plan.
- Then the stills are made and graded, then the motion, then the five lip-sync clips. All of this happens only after he records or approves the voice lines.
- The five song lyric videos need to be finished in his Premiere project first. The special's edit is a new sequence, and his project is not written to.
