# A Very Sackbuts Christmas: the special

Written November 17, 2026, for Adam, and revised three times that day:

- **Morning:** more lip sync.
- **Evening:** a fuller open and close, and the instruments picked up only once.
- **Voices:** Luther moved to ElevenLabs.

Plan and script only. No image, clip, or audio was made in this pass, and nothing was posted.

One long YouTube video: the six album songs, with short host segments between them in one Sackbuts living-room set. The host segments are mostly on camera: the man who is talking is in his own close-up and lip-synced. A line is off camera only where that plays better: a reaction, an insert, a pickup, Bedgo asleep, or a quick cutaway. It is built from 19 stills in use and 28 lip-sync clips.

**How the tags work.** Lines and clips added in the evening pass are tagged **NEW**, and lines whose words changed are tagged **CHANGED**. Untagged lines keep their ids and their recorded files.

## 1. Plan

### Runtime

| Part | Length |
|---|---|
| Six songs, as their own lyric videos | 26:57 |
| Open (about 56 s), five song intros (about 71 s), and the close (about 45 s) | about 2:52 |
| **Total** | **about 30 minutes** |

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

| Id | Where | Host time | Lip-sync clips |
|---|---|---|---|
| A | Open, the one instrument pickup, then Sleigh Ride | about 56 s | LS01–LS05, LS23–LS26 |
| B | Into Stuck in a Stable | about 15 s | LS06–LS07 |
| C | Into Eighteen Wheels | about 13 s | LS08–LS10 |
| D | Into Tinsel | about 13 s | LS11–LS12 |
| E | Into Mama's Fruitcake | about 16 s | LS13–LS16 |
| F | Into Two Years Late | about 15 s | LS17–LS18 |
| G | Close | about 45 s | LS19–LS22, LS27–LS28 |

### Lip-sync budget

No lip sync has been run yet, so the whole budget is still open.

**The plan: 28 lip-sync clips, covering 33 of the 45 spoken lines, with about 110 seconds of speech.**

**Padding.** Each clip gets 0.5 s of driving audio before the line and 1.0 s after. On the eleven punchline clips, the after pad is 1.5 s, so the face holds while the joke lands. That was 2.0 s in the morning version, and the shorter pad keeps a real redo reserve under $30.

**Billed time.** That comes to **157 billed seconds, about $25.95**, at about $0.165 per second for OmniHuman 1.5 at 1080p.

**Redo reserve.** About **24 seconds, about $4**, covers redoing about four clips.

**Hard stop: 181 billed seconds ($30).** Run `hedra.py estimate` before each batch and log the spend.

| Clip | Speaker | Lines | Still | Speech | Billed | Status |
|---|---|---|---|---|---|---|
| LS01 | Earl | A2 + A2b | CU-E | 8.4 s | 9.9 s | CHANGED: adds A2b |
| LS02 | Luther | A2c + A3 | CU-L | 4.4 s | 5.9 s | CHANGED: adds A2c |
| LS03 | Luther | A6 (punchline) | CU-L2 | 1.5 s | 3.5 s | |
| LS23 | Earl | A6a | CU-E2 | 3.0 s | 4.5 s | NEW |
| LS24 | Luther | A6b + [A6c, Earl off screen] + A6d (punchline) | CU-L2 | 3.0 s | 5.0 s | NEW |
| LS25 | Earl | A6e | CU-E | 4.5 s | 6.0 s | NEW |
| LS26 | Luther | A6f (punchline) | CU-L | 4.0 s | 6.0 s | NEW |
| LS04 | Earl | A7 | CU-E | 6.0 s | 7.5 s | CHANGED: new words |
| LS05 | Luther | A8 (punchline) | CU-L | 2.0 s | 4.0 s | |
| LS06 | Earl | B1 | CU-E2 | 3.5 s | 5.0 s | |
| LS07 | Luther | B2 (punchline) | CU-L | 6.5 s | 8.5 s | |
| LS08 | Earl | C2 | CU-E2 | 2.0 s | 3.5 s | |
| LS09 | Luther | C3 (punchline) | CU-L2 | 1.0 s | 3.0 s | |
| LS10 | Earl | C4 | CU-E | 4.0 s | 5.5 s | |
| LS11 | Luther | D1 | CU-L2 | 2.5 s | 4.0 s | |
| LS12 | Earl | D2 | CU-E2 | 3.5 s | 5.0 s | |
| LS13 | Luther | E1 | CU-L2 | 2.0 s | 3.5 s | |
| LS14 | Earl | E2 | CU-E2 | 2.0 s | 3.5 s | |
| LS15 | Luther | E3 (punchline) | CU-L | 2.5 s | 4.5 s | |
| LS16 | Earl | E4 (punchline) | CU-E | 4.5 s | 6.5 s | |
| LS17 | Earl | F2 | CU-E | 4.0 s | 5.5 s | |
| LS18 | Luther | F3 (punchline) | CU-L | 5.0 s | 7.0 s | |
| LS19 | Earl | G2 | CU-E | 3.0 s | 4.5 s | |
| LS20 | Luther | G3 (punchline) | CU-L | 3.0 s | 5.0 s | |
| LS27 | Earl | G3b | CU-E | 4.5 s | 6.0 s | NEW |
| LS28 | Luther | G3c | CU-L | 5.5 s | 7.0 s | NEW |
| LS21 | Earl | G3d + G4 | CU-E | 7.9 s | 9.4 s | CHANGED: adds G3d |
| LS22 | Bedgo | G6a + [G6b, Earl off screen] + G6c (punchline) | **CU-B2H** | 6.0 s | 8.0 s | CHANGED: new still, with the bass |
| **Total** | | | | **about 110 s** | **157.2 s** | |

**By speaker:** Earl 14 clips, Luther 13, and Bedgo 1.

**By still:** CU-E 9, CU-E2 5, CU-L 8, CU-L2 5, and CU-B2H 1.

The twelve NO-SYNC lines, and why each one plays better off camera:

| Line | Speaker | Why it is off camera |
|---|---|---|
| A5 | Earl | The joke is Bedgo asleep, so we stay on Bedgo. |
| A5b | Luther (NEW) | Still on Bedgo asleep, finishing that joke. |
| A6c | Earl (NEW) | Luther's two-word comeback around it is the joke, so we hold on Luther. |
| A9a | Luther (NEW) | It plays over his own fiddle pickup. |
| A9b | Earl (NEW) | The punchline is Bedgo grabbing the bass in his sleep, so we watch Bedgo. |
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

- **Instruments are picked up once**, at the end of the open, right before Nebo County Sleigh Ride: Earl's guitar (P01), Luther's fiddle (P02), then Bedgo (P03 to P03E). From then on, the band holds their instruments for the rest of the show.
  - Earl's and Luther's close-ups are framed from the chest up, so the guitar and fiddle resting on their knees sit below the frame. The same four close-up stills work before and after the pickup.
  - Bedgo's close-ups show his arms, so after the pickup he uses CU-B1H and CU-B2H, which have the bass in his arms.
- **Each segment after a song** opens on a 1-second W02 beat (instruments in hand) and ends on W02 or W02F into the next song.
- **Bedgo** is asleep for every talking line until G6. His eyes are closed, he never moves on his own except to grab the bass in A9, and he snores (sound effect) only where marked.
- **And Friend** is never explained, never named on screen beyond "...And Friend," and never turned toward by anyone.
  - He appears only in W01F (once, in the open, right after "...And Friend") and W02F (before songs 3 and 6, and at the start and end of the close).
  - He is always small and soft, deep in the dim archway at the back, in a plain dark coat, with no readable face. He has no glow, no halo, and no light on him.
  - When he comes up, the boys smile and change the subject.

### A. Open, the one pickup, into Nebo County Sleigh Ride (about 56 s)

| # | Speaker | Line | Sync | Shot | Time | Background |
|---|---|---|---|---|---|---|
| A1 | — | Fire crackle, tree lights. The logo goes on here in the edit. | — | W01, slow push in | 3 s | Bedgo asleep, instruments on their stands |
| A2 | EARL | "Evenin', and Merry Christmas from Nebo County, Tennessee. We're the Sackbuts." | **LIP-SYNC (LS01)** | CU-E | 4.5 s | — |
| A2b **NEW** | EARL | "Welcome to A Very Sackbuts Christmas. Come on in and get warm." | **LIP-SYNC (LS01)** | CU-E, same clip | 3.5 s | — |
| A2c **NEW** | LUTHER | "Wipe your feet." | **LIP-SYNC (LS02)** | CU-L | 1 s | — |
| A3 | LUTHER | "I'm Luther. That there's Earl. And that's Bedgo." | **LIP-SYNC (LS02)** | CU-L, same clip | 3 s | — |
| A4 | — | Snore. | — | CU-B1 | 1.5 s | asleep |
| A5 | EARL | "He's been like that since Thanksgiving." | NO-SYNC | CU-B1, held | 2 s | asleep |
| A5b **NEW** | LUTHER | "Second helpin' of dressing. Never came back." | NO-SYNC | CU-B1, held | 2.5 s | asleep |
| A6 | LUTHER | "...And Friend." He glances back over his shoulder toward the back of the room. | **LIP-SYNC (LS03)** | CU-L2 | 1.5 s | — |
| A6x **NEW** | — | Silent cutaway: the room, and in the dim archway at the back, a small soft figure. No push in, no music sting. | — | **W01F** | 1.5 s | **And Friend** in the archway. Bedgo asleep. |
| A6a **NEW** | EARL | "Anyhow. Tonight we're gonna do what we do best." He smiles and changes the subject. | **LIP-SYNC (LS23)** | CU-E2 | 3 s | — |
| A6b **NEW** | LUTHER | "Eat?" | **LIP-SYNC (LS24)** | CU-L2 | 0.7 s | — |
| A6c **NEW** | EARL | "Tell stories." He is off screen, in the gap inside the same clip, and Luther's lips are closed for it. | NO-SYNC | CU-L2, same clip | 1 s | — |
| A6d **NEW** | LUTHER | "Then eat." | **LIP-SYNC (LS24)** | CU-L2, same clip | 0.8 s | — |
| A6e **NEW** | EARL | "We picked out a few of our favorite Christmas stories, and every one of 'em's a song." | **LIP-SYNC (LS25)** | CU-E | 4.5 s | — |
| A6f **NEW** | LUTHER | "Some happened to Earl, some happened to me, and one happened to a horse." | **LIP-SYNC (LS26)** | CU-L | 4 s | — |
| A7 **CHANGED** | EARL | "First one's about Granddaddy's old sleigh and a horse named Dewey, who won't move unless you quote him Scripture." | **LIP-SYNC (LS04)** | CU-E | 6 s | — |
| A8 | LUTHER | "Bedgo knows the short one." | **LIP-SYNC (LS05)** | CU-L | 2 s | — |
| A9 | — | Earl lifts his guitar off its stand. | — | P01 | 1.5 s | — |
| A9a **NEW** | LUTHER | "Somebody wake Bedgo up." He says it as he tucks the fiddle under his chin. | NO-SYNC | P02 | 1.5 s | — |
| A9b **NEW** | EARL | "Don't need to." Bedgo, eyes closed, reaches over in his sleep, lifts the bass off its stand, and hugs it. | NO-SYNC | P03 → P03E, one Dream Machine clip | 3 s | asleep, now holding the bass |
| A10 | LUTHER | "One, two..." The song starts. | NO-SYNC | W02 | 1.5 s | asleep on the bass |

A7 used to be "Anyhow. First one's about a horse that won't move unless you quote him Scripture." "Anyhow" moved to A6a, where it changes the subject from And Friend.

"The short one" is "Jesus wept." It is the line that gets Dewey moving in the song, so this only sets it up and does not spoil it.

### B. Into Stuck in a Stable on Christmas (about 15 s)

| # | Speaker | Line | Sync | Shot | Background |
|---|---|---|---|---|---|
| B0 | — | Back on the set, instruments in hand. | — | W02, 1 s | asleep on the bass |
| B1 | EARL | "Dewey's twenty-six, and he still runs better than The Furnace." | **LIP-SYNC (LS06)** | CU-E2 | — |
| B2 | LUTHER | "One Christmas Eve The Furnace quit, and we slept in a barn with a cow, a donkey, and Bedgo. Hard to tell which one was snorin'." | **LIP-SYNC (LS07)** | CU-L | — |
| B3 | — | Snore. | — | **CU-B1H**, 1.5 s | asleep on the bass |
| B4 | — | The song starts. | — | W02 | asleep on the bass |

### C. Into Eighteen Wheels and a Prayer (about 13 s)

| # | Speaker | Line | Sync | Shot | Background |
|---|---|---|---|---|---|
| C0 | — | Back on the set. | — | W02, 1 s | asleep on the bass |
| C1 | LUTHER | "Breaker one-nine, this here's Firehose. Come on." It is filtered to sound like it is coming through the CB. | NO-SYNC | I02, CB radio | — |
| C2 | EARL | "Luther. We're on television." | **LIP-SYNC (LS08)** | CU-E2 | — |
| C3 | LUTHER | "Old habit." He sheepishly sets the mic down, out of frame. | **LIP-SYNC (LS09)** | CU-L2 | — |
| C4 | EARL | "This next one's forty truckers, one blizzard, and a baby that would not wait." | **LIP-SYNC (LS10)** | CU-E | — |
| C5 | — | The song starts. | — | W02F | **And Friend** in the archway. Asleep on the bass. |

### D. Into The Tinsel Comes and Goes (about 13 s)

| # | Speaker | Line | Sync | Shot | Background |
|---|---|---|---|---|---|
| D0 | — | Back on the set. | — | W02, 1 s | asleep on the bass |
| D1 | LUTHER | "Earl, tell 'em about your mama's Christmas trees." | **LIP-SYNC (LS11)** | CU-L2 | — |
| D2 | EARL | "Silver, green, white, and one she made in ceramics class." | **LIP-SYNC (LS12)** | CU-E2 | — |
| D3 | EARL | "But that little dollar manger never moved. Not one inch." | NO-SYNC | I03, the manger | — |
| D4 | LUTHER | "Like Bedgo." | NO-SYNC | **CU-B1H** | asleep on the bass |
| D5 | — | The song starts. | — | W02 | asleep on the bass |

### E. Into Mama's Fruitcake (about 16 s)

The joke lands on the fruitcake. Earl's last line is the turn into the song.

| # | Speaker | Line | Sync | Shot | Background |
|---|---|---|---|---|---|
| E0 | — | Back on the set. | — | W02, 1 s | asleep on the bass |
| E1 | LUTHER | "Earl. Is that your mama's fruitcake?" | **LIP-SYNC (LS13)** | CU-L2 | — |
| E1b | — | Silent cutaway to the fruitcake. | — | I01, 1 s | — |
| E2 | EARL | "Same recipe since fifty-six." | **LIP-SYNC (LS14)** | CU-E2 | — |
| E3 | LUTHER | "I've put out grease fires that were friendlier." | **LIP-SYNC (LS15)** | CU-L | — |
| E4 | EARL | "Worst fruitcake in Tennessee. And I'd give anything for one more slice." | **LIP-SYNC (LS16)** | CU-E | — |
| E5 | — | No count-in. Earl starts the first chord soft and the song begins. | — | W02 | asleep on the bass |

### F. Into Two Years Late and Right on Time (about 15 s)

| # | Speaker | Line | Sync | Shot | Background |
|---|---|---|---|---|---|
| F0 | — | Back on the set. | — | W02, 1 s | asleep on the bass |
| F1 | LUTHER | "Somebody hand Earl a hankie." | NO-SYNC | CU-E. Earl wipes one eye with a knuckle, lips closed | — |
| F2 | EARL | "Last one tonight. Three wise men, three camels, and a whole lot of wrong turns." | **LIP-SYNC (LS17)** | CU-E | — |
| F3 | LUTHER | "Took them wise men two years to get there. Bedgo'd still be asleep on the camel." | **LIP-SYNC (LS18)** | CU-L | — |
| F4 | — | The song starts. | — | W02F | **And Friend** in the archway. Asleep on the bass. |

### G. Close (about 45 s)

Two Years Late ends on its spoken line: "Folks know the Sackbuts don't bow... but there's one King we'll kneel for. Happy birthday, Friend." Cut straight to W02F, with And Friend in the archway.

| # | Speaker | Line | Sync | Shot | Time | Background |
|---|---|---|---|---|---|---|
| G1 | — | Soft applause (sound effect). | — | W02F | 2 s | **And Friend** in the archway. Asleep on the bass. |
| G2 | EARL | "Y'all are welcome to clap. We just don't bow." | **LIP-SYNC (LS19)** | CU-E | 3 s | — |
| G3 | LUTHER | "Thank you kindly, but we're gonna have to go with no." | **LIP-SYNC (LS20)** | CU-L | 3.5 s | — |
| G3b **NEW** | EARL | "There's only one King the Sackbuts bow to, and He started out in a feed trough." | **LIP-SYNC (LS27)** | CU-E | 5 s | — |
| G3c **NEW** | LUTHER | "So wherever you spend Christmas, a farmhouse, a truck stop, or a barn, He's already been there." | **LIP-SYNC (LS28)** | CU-L | 6 s | — |
| G3x **NEW** | — | Silent cutaway to the manger. | — | I03 | 2 s | — |
| G3d **NEW** | EARL | "Hug your mama, call your people, and save somebody a slice of fruitcake." | **LIP-SYNC (LS21)** | CU-E | 4.5 s | — |
| G4 | EARL | "From all of us in Nebo County, Merry Christmas." | **LIP-SYNC (LS21)** | CU-E, same clip | 3 s | — |
| G5 | LUTHER | "And Bedgo slept through the whole thing." | NO-SYNC | **CU-B1H** | 2 s | asleep on the bass |
| G6a | BEDGO | "...Did I miss it?" One eye cracks open, then both. | **LIP-SYNC (LS22)** | **CU-B2H** | 7 s for the whole of G6 | — |
| G6b | EARL | "The whole show, Bedgo." He is off screen, in the gap inside the same clip. Bedgo's lips are closed for it. | NO-SYNC | CU-B2H, same clip | | — |
| G6c | BEDGO | "Naw." He glances back over his shoulder toward the archway behind him and smiles a little. "Didn't miss a thing." Then he settles his cheek back on the bass and closes his eyes. | **LIP-SYNC (LS22)** | CU-B2H, same clip | | — |
| G7 | — | Cut to the wide. Bedgo is asleep on the bass again, and in the archway, small and soft, And Friend. Hold, then fade. | — | W02F | 3 s | **And Friend** in the archway |
| G8 | — | Fire and tree lights only, then the end card. | — | SET01 | 3 s | nobody |

**Callbacks in the close**

- G3b ties to Two Years Late's "one King we'll kneel for" and to the barn in Stuck in a Stable.
- G3c names the farmhouse, the truck stop, and the barn from the album's songs.
- G5 is the last line of Eighteen Wheels.
- Bedgo's glance in G6c is toward the archway, and the cut to W02F shows the figure there. Leave that unexplained.

## 3. Shot list

**19 stills are in use.**

- 16 were already made and are approved in `gen/shots_status.json`.
- Four new stills are needed: W01F, P03E, CU-B1H, and CU-B2H.
- P03 is being redone.
- CU-B2 (Bedgo awake, no bass) is retired, because Bedgo holds the bass by the time he wakes.

Every still is Firefly Gemini Flash at 16:9, run with the repo's Firefly tooling. Each still is graded before it is used. Make the new ones in this order, because later stills use earlier approved ones as image 1:

1. W01F
2. P03 (redo)
3. P03E
4. CU-B1H
5. CU-B2H

| Still | Status | Used for |
|---|---|---|
| SET01 | done | The last shot |
| W01 | done | The open (A1), and image 1 for the close-ups, P01, P02, and W01F |
| **W01F** | **NEW** | The open's And Friend cutaway (A6x) |
| W02 | done | The beat after each song, and into songs 1, 2, 4, and 5 |
| W02F | done | Into songs 3 and 6, and the close (G1 and G7) |
| CU-E | done | Earl, front, talking to us: 9 clips, plus F1's reaction |
| CU-E2 | done | Earl, second angle, talking to Luther: 5 clips |
| CU-L | done | Luther, front, talking to us: 8 clips |
| CU-L2 | done | Luther, second angle, talking to Earl: 5 clips |
| CU-B1 | done | Bedgo asleep before the pickup: A4, A5, and A5b |
| **CU-B1H** | **NEW** | Bedgo asleep holding the bass: B3, D4, and G5 |
| **CU-B2H** | **NEW** | Bedgo awake holding the bass: LS22 |
| CU-B2 | retired | — |
| P01, P02 | done | The one pickup in A9 and A9a |
| **P03** | **REDO** | Start frame of Bedgo's pickup, A9b |
| **P03E** | **NEW** | End frame of Bedgo's pickup, A9b |
| I01, I02, I03 | done | Fruitcake, CB radio, and manger |

The prompts for the 16 done stills are unchanged from the morning version of this plan. The approved files and clips are listed in `gen/shots_status.json`.

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

### New and redone stills

**W01F (NEW): the talking wide with And Friend.** It is made from the approved W01, the same way W02F was made from W02. Refs:

1. W01, approved (`W01_v10`)
2. Shady Full
3. Mesh Full
4. Bedgo Full

```
Image 1 is the frame to keep. Keep its camera, framing, lighting, and every person, instrument and object exactly where and how they are in image 1; the guitar, the fiddle and the upright bass stay on their stands. The man on the pew is the man in image 2, the man on the ladder-back chair is the man in image 3, and the man asleep in the recliner is the man in image 4. The only change: deep in the dim archway behind them, a fourth man stands quietly, small and soft in the shadow, in a plain dark coat. His face is not readable. He has no glow, no halo, and no light on him. He does not look at the camera. Tail.
```

**P03 (REDO): Bedgo asleep, the bass on its stand beside him.** This is the start frame of his pickup. Refs:

1. CU-B1, approved
2. Bedgo Full
3. Bedgo (face)

The candidate `gen/review/P03_v4.jpg` already matches this description: asleep, arms folded, the bass on its stand at his right. If Adam approves it, it is P03, and only P03E needs making. The bass is described in words, and the bass-holding reference is not used, so Firefly does not put it in his arms.

```
Image 1 sets the camera and the room. Show the same moment from a slightly wider camera at seated eye height in front of the recliner: a medium shot of the man asleep in the plaid recliner in image 1, who is the man in image 2. He is deeply asleep, head tipped against the wing of the chair, eyes closed, mouth closed, arms folded. Right beside the recliner, within arm's reach, an upright bass stands upright on its floor stand; nobody is touching it. Behind him, the dim archway is soft and empty, and the warm floor lamp glows. Image 3 is a close-up of the face of the man in image 2. Nobody else is in frame. Tail.
```

**P03E (NEW): Bedgo still asleep, now holding the bass.** This is the end frame of his pickup. Refs:

1. P03, approved
2. Bedgo Full 2
3. Bedgo (face)

```
Image 1 is the frame to keep: the same camera, framing, light, recliner, lamp and archway. The man in image 1 is the man in image 2 and the man in image 3. The only change: still fast asleep, he has pulled the upright bass from image 2 off its stand and into his arms. Both arms are wrapped around its neck, his cheek rests against it, and his eyes and mouth are closed. The floor stand beside the recliner is now empty. Nobody else is in frame. Tail.
```

Dream Machine makes one clip with P03 as the start frame and P03E as the end frame:

> Real time, normal speed. Still asleep with his eyes closed the whole time, he reaches over, lifts the upright bass off its stand and pulls it into a hug, then settles. The lamp glows warm, and the room is softly lit by firelight. His eyes never open.

Using both frames keeps him asleep from start to end.

**CU-B1H (NEW): Bedgo asleep, holding the bass.** It is the after-pickup version of CU-B1. Refs:

1. W02, approved (`W02_v12`)
2. Bedgo (face)
3. Bedgo Full 2

```
Image 1 is the scene. Show the exact same moment from a second camera at seated eye height in front of the recliner: a close-up from mid-chest up of the man asleep in the plaid recliner holding the upright bass in image 1, who is the man in image 2. Image 2 is only his face; take nothing else from image 2. Image 3 is his clothes and the upright bass. The neck of the bass rises past his shoulder, both arms are wrapped around it, his cheek rests against it, and his eyes and mouth are closed. Behind him, the dim archway is soft and empty. Nobody else is in frame. Tail.
```

**CU-B2H (NEW): Bedgo awake, holding the bass.** It is used only for LS22. Refs:

1. CU-B1H, approved
2. Bedgo (face)

```
Image 1 is the frame to keep: the same camera, framing, light, chair, clothes and upright bass, and the same dim, empty archway behind him. The man in image 1 is the man in image 2; take only his face from image 2. The only change: he has just woken up. His eyes are open and heavy-lidded, his head is lifted a little off the neck of the bass, his arms are still around it, and he looks off toward the left of the frame, not into the lens, lips closed. Nobody else is in frame. Tail.
```

### Motion for the shots that are not lip-synced

These get motion in Dream Machine:

- **Already made:** SET01, W01, W02, W02F, CU-B1, CU-E for F1, P01, P02, I01, I02, and I03.
- **New:** W01F and CU-B1H, one clip each.
- **New:** the P03 to P03E pickup, one clip with a start frame and an end frame.

Every motion prompt says real time, normal speed, small natural movement, and the fire flickering and the tree lights twinkling. It never tells the background to hold still.

Every prompt with a face says his lips stay closed. If Dream Machine moves a closed mouth anyway, push in on the still in the edit instead.

| Shot | Motion |
|---|---|
| W01F | And Friend stays still and soft. Nobody turns toward him. Bedgo stays asleep. |
| CU-B1H | His eyes stay closed and his chest rises and falls against the bass. If he wakes, use the still with a slow push in the edit. |

## 4. Voice and lip sync

### Voices

| Character | Engine | Voice | Starting settings | Read |
|---|---|---|---|---|
| Earl | MiniMax text-to-speech | `moss_audio_a0a41263-e2c3-11f1-92f1-163db804a819`, trained by Adam | speed 0.95 | Warm, gravelly baritone with a heavy Southern twang. Plain and unhurried; he hosts. Sincere on E4 and G3b–G4: no wink. |
| Luther | **ElevenLabs**, recorded by Adam | Adam's ElevenLabs Luther voice | Adam's settings | The fast talker. Quicker and a little higher than Earl, with a grin in the voice. Quieter and warm on G3c. |
| Bedgo | MiniMax text-to-speech | `ttv-voice-2026111804244026-bYLxVfDI`, trained by Adam | speed 0.85 | Low, sleepy, deadpan bass, almost a mumble. Never a laugh or a big reaction. |

Luther's earlier MiniMax voice (`ttv-voice-2026111804215526-BK2ErWcB`) is retired. His lines are ElevenLabs only.

The character reads come from `band/bible.md`, plus Tinsel's spoken-line direction for Bedgo. And Friend has no voice and no lines.

**Where the takes go**

- Earl and Bedgo, from MiniMax: `E:\Music\The Sackbuts\Music Video\Christmas Special\audio\`.
- Luther, from ElevenLabs: `E:\Music\The Sackbuts\Music Video\Christmas Special\audio\elevenlabs\`, as an mp3 and a wav.

**Format.** WAV, 44.1 kHz, mono, one file per line.

**Text.** The text sent to the voice engine is the script line exactly. If the engine misreads a word, change the spelling in the text sent to the engine only, keep the script as written, and note the change beside that file.

**Filenames.** Unchanged lines keep their ids and files. A NEW line gets a new id with a letter suffix (`A2b_earl.wav`). A CHANGED line keeps its id and gets `_v2`, so the old take is not overwritten.

### New and changed lines to record

These are 15 files: 7 for Luther in ElevenLabs, 8 for Earl in MiniMax, and none for Bedgo.

**Luther: Adam records these in ElevenLabs (7 NEW)**

| Line | Text | File | Use |
|---|---|---|---|
| A2c | Wipe your feet. | `A2c_luther.wav` | LS02, before A3 |
| A5b | Second helpin' of dressing. Never came back. | `A5b_luther.wav` | NO-SYNC, over Bedgo |
| A6b | Eat? | `A6b_luther.wav` | LS24 |
| A6d | Then eat. | `A6d_luther.wav` | LS24 |
| A6f | Some happened to Earl, some happened to me, and one happened to a horse. | `A6f_luther.wav` | LS26 |
| A9a | Somebody wake Bedgo up. | `A9a_luther.wav` | NO-SYNC, over P02 |
| G3c | So wherever you spend Christmas, a farmhouse, a truck stop, or a barn, He's already been there. | `G3c_luther.wav` | LS28 |

**Earl: generate these in MiniMax (7 NEW and 1 CHANGED)**

| Line | Text | File | Use |
|---|---|---|---|
| A2b (NEW) | Welcome to A Very Sackbuts Christmas. Come on in and get warm. | `A2b_earl.wav` | LS01, after A2 |
| A6a (NEW) | Anyhow. Tonight we're gonna do what we do best. | `A6a_earl.wav` | LS23 |
| A6c (NEW) | Tell stories. | `A6c_earl.wav` | NO-SYNC, in the gap inside LS24 |
| A6e (NEW) | We picked out a few of our favorite Christmas stories, and every one of 'em's a song. | `A6e_earl.wav` | LS25 |
| A7 (CHANGED) | First one's about Granddaddy's old sleigh and a horse named Dewey, who won't move unless you quote him Scripture. | `A7_earl_v2.wav`, replacing `A7_earl.wav` | LS04 |
| A9b (NEW) | Don't need to. | `A9b_earl.wav` | NO-SYNC, over P03 to P03E |
| G3b (NEW) | There's only one King the Sackbuts bow to, and He started out in a feed trough. | `G3b_earl.wav` | LS27 |
| G3d (NEW) | Hug your mama, call your people, and save somebody a slice of fruitcake. | `G3d_earl.wav` | LS21, before G4 |

**Bedgo:** no new or changed lines.

### Every line and its file

That is 45 lines: 21 for Earl, 22 for Luther, and 2 for Bedgo.

| Line | Character | Text | File | Sync | Status |
|---|---|---|---|---|---|
| A2 | Earl | Evenin', and Merry Christmas from Nebo County, Tennessee. We're the Sackbuts. | `A2_earl.wav` | LS01 | |
| A2b | Earl | Welcome to A Very Sackbuts Christmas. Come on in and get warm. | `A2b_earl.wav` | LS01 | NEW |
| A2c | Luther | Wipe your feet. | `A2c_luther.wav` | LS02 | NEW |
| A3 | Luther | I'm Luther. That there's Earl. And that's Bedgo. | `A3_luther.wav` | LS02 | |
| A5 | Earl | He's been like that since Thanksgiving. | `A5_earl.wav` | NO-SYNC | |
| A5b | Luther | Second helpin' of dressing. Never came back. | `A5b_luther.wav` | NO-SYNC | NEW |
| A6 | Luther | ...And Friend. | `A6_luther.wav` | LS03 | |
| A6a | Earl | Anyhow. Tonight we're gonna do what we do best. | `A6a_earl.wav` | LS23 | NEW |
| A6b | Luther | Eat? | `A6b_luther.wav` | LS24 | NEW |
| A6c | Earl | Tell stories. | `A6c_earl.wav` | NO-SYNC, in LS24's gap | NEW |
| A6d | Luther | Then eat. | `A6d_luther.wav` | LS24 | NEW |
| A6e | Earl | We picked out a few of our favorite Christmas stories, and every one of 'em's a song. | `A6e_earl.wav` | LS25 | NEW |
| A6f | Luther | Some happened to Earl, some happened to me, and one happened to a horse. | `A6f_luther.wav` | LS26 | NEW |
| A7 | Earl | First one's about Granddaddy's old sleigh and a horse named Dewey, who won't move unless you quote him Scripture. | `A7_earl_v2.wav` | LS04 | CHANGED |
| A8 | Luther | Bedgo knows the short one. | `A8_luther.wav` | LS05 | |
| A9a | Luther | Somebody wake Bedgo up. | `A9a_luther.wav` | NO-SYNC | NEW |
| A9b | Earl | Don't need to. | `A9b_earl.wav` | NO-SYNC | NEW |
| A10 | Luther | One, two... | `A10_luther.wav` | NO-SYNC | |
| B1 | Earl | Dewey's twenty-six, and he still runs better than The Furnace. | `B1_earl.wav` | LS06 | |
| B2 | Luther | One Christmas Eve The Furnace quit, and we slept in a barn with a cow, a donkey, and Bedgo. Hard to tell which one was snorin'. | `B2_luther.wav` | LS07 | |
| C1 | Luther | Breaker one-nine, this here's Firehose. Come on. | `C1_luther.wav` | NO-SYNC. The CB filter goes on in the edit. | |
| C2 | Earl | Luther. We're on television. | `C2_earl.wav` | LS08 | |
| C3 | Luther | Old habit. | `C3_luther.wav` | LS09 | |
| C4 | Earl | This next one's forty truckers, one blizzard, and a baby that would not wait. | `C4_earl.wav` | LS10 | |
| D1 | Luther | Earl, tell 'em about your mama's Christmas trees. | `D1_luther.wav` | LS11 | |
| D2 | Earl | Silver, green, white, and one she made in ceramics class. | `D2_earl.wav` | LS12 | |
| D3 | Earl | But that little dollar manger never moved. Not one inch. | `D3_earl.wav` | NO-SYNC | |
| D4 | Luther | Like Bedgo. | `D4_luther.wav` | NO-SYNC | |
| E1 | Luther | Earl. Is that your mama's fruitcake? | `E1_luther.wav` | LS13 | |
| E2 | Earl | Same recipe since fifty-six. | `E2_earl.wav` | LS14 | |
| E3 | Luther | I've put out grease fires that were friendlier. | `E3_luther.wav` | LS15 | |
| E4 | Earl | Worst fruitcake in Tennessee. And I'd give anything for one more slice. | `E4_earl.wav` | LS16 | |
| F1 | Luther | Somebody hand Earl a hankie. | `F1_luther.wav` | NO-SYNC | |
| F2 | Earl | Last one tonight. Three wise men, three camels, and a whole lot of wrong turns. | `F2_earl.wav` | LS17 | |
| F3 | Luther | Took them wise men two years to get there. Bedgo'd still be asleep on the camel. | `F3_luther.wav` | LS18 | |
| G2 | Earl | Y'all are welcome to clap. We just don't bow. | `G2_earl.wav` | LS19 | |
| G3 | Luther | Thank you kindly, but we're gonna have to go with no. | `G3_luther.wav` | LS20 | |
| G3b | Earl | There's only one King the Sackbuts bow to, and He started out in a feed trough. | `G3b_earl.wav` | LS27 | NEW |
| G3c | Luther | So wherever you spend Christmas, a farmhouse, a truck stop, or a barn, He's already been there. | `G3c_luther.wav` | LS28 | NEW |
| G3d | Earl | Hug your mama, call your people, and save somebody a slice of fruitcake. | `G3d_earl.wav` | LS21 | NEW |
| G4 | Earl | From all of us in Nebo County, Merry Christmas. | `G4_earl.wav` | LS21 | |
| G5 | Luther | And Bedgo slept through the whole thing. | `G5_luther.wav` | NO-SYNC | |
| G6a | Bedgo | ...Did I miss it? | `G6a_bedgo.wav` | LS22 | |
| G6b | Earl | The whole show, Bedgo. | `G6b_earl.wav` | NO-SYNC, in LS22's gap | |
| G6c | Bedgo | Naw. Didn't miss a thing. | `G6c_bedgo.wav` | LS22 | |

The snore and the applause are sound effects from the library, not text-to-speech.

### Lip-sync method

This is the same as I Still Care About Your Christmas, from `lyricvideo/songs/i-still-care/run_lipsync.py` and `lyricvideo/PROCESS.md` section 4.5.

- **Model and size:** OmniHuman 1.5 through Hedra, 1080p, solo close-ups only.
- **Driving audio:** built from the approved voice files, saved in `lyricvideo/sackbuts/christmas-special/lipsync/in/LSnn.wav`.
  - It starts 0.5 s before the first word and ends 1.0 s after the last, or 1.5 s after on the punchline clips.
  - It gets `highshelf=f=3000:g=5` for consonants.
  - Record `pad_in` so the edit skips the lead-in.
- **Clips that join two files from the same speaker** (LS01, LS02, and LS21): put the two files end to end with 0.4 s of silence between them.
- **Clips with the other man in the gap:**
  - LS24 is `A6b_luther.wav`, then silence the exact length of `A6c_earl.wav`, then `A6d_luther.wav`.
  - LS22 is `G6a_bedgo.wav`, then silence the exact length of `G6b_earl.wav`, then `G6c_bedgo.wav`.
  - The off-screen man's line goes on the edit audio only.
- **Cost:** each run is paid, so it stays with the main agent. Run `hedra.py estimate` first, check the wallet with `hedra.py balance`, and log the spend against the 157-second plan and the 181-second hard stop.
- **Stalls:** a job stuck at 90% for more than 10 minutes gets killed and resubmitted.
- **Redos:** these come out of the roughly 24-second reserve, worst clip first.

Base prompt for all 28 clips:

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
| LS23 | He starts with a small smile, changing the subject. |
| LS24 | Deadpan. His lips stay closed in the pause between his two words. |
| LS09 | Sheepish. |
| LS16 | Quiet and sincere. His eyes drop on "one more slice." |
| LS27 and LS28 | Quiet and warm, no grin. |
| LS22 | Heavy-lidded, his arms around the upright bass. His lips stay closed in the pause between his two lines. On the last line he glances back over his shoulder toward the room behind him and smiles slightly. Then he lays his cheek back on the bass and closes his eyes. |

## What this changes downstream

1. **Voice files:** record or generate the 15 files listed above. Adam approves them before any lip sync runs.
2. **Stills:** make W01F, P03 (or approve `P03_v4`), P03E, CU-B1H, and CU-B2H. Then make the three new Dream Machine clips.
3. **The special's edit** (`gen/special.py` and the special's Premiere sequence) needs these changes:
   - The longer open and close.
   - The pickups removed from segments B through F.
   - The 1-second post-song beats moved from W01 to W02.
   - The new Bedgo stills.
   - Adam's own project is not written to.
4. **Lip sync** runs after all of that, starting with `hedra.py estimate`.
