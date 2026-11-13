# A Very Sackbuts Christmas — album cover prompt

Written November 12, 2026. Status: prompt only. Nothing was generated, uploaded, posted, or spent. Nothing under `E:\` was changed.

For Adam to paste into Firefly himself, with the Gemini Flash (Nano Banana) model, the same model that made the band photo.

## The scene

Christmas night in Nebo County. The three of them stand full length in the snow-dusted gravel churchyard, deadpan, instruments at rest. The Furnace is parked behind them with a string of big colored bulbs on its roof rack and a crooked wreath on its grille. The little white church glows on the hill behind. The night sky across the top stays open and dark for the logo, and the album title is painted along the bottom.

No camels, no fruitcake, no broken-down van, no CB radio. Nothing from a single song sits in the middle. The prompt describes each man by his clothes and his instrument rather than his name, so the model does not try to letter the names. Earl is the middle man, Luther is on the left, and Bedgo is on the right.

## Prompt

```
A square album cover for a country Christmas record, painted as a warm, slightly worn illustration: rich visible brushwork, a palette of deep night blue and warm gold, softly faded color, scuffed corners and worn edges like an old, well-loved record sleeve, fine paper grain. The mood is dry and funny, and quietly reverent.

It is Christmas night in the hills of rural Tennessee. Three middle-aged country musicians stand side by side, full length, on the snow-dusted gravel of a small churchyard. In the middle stands a burly man with a salt-and-pepper beard, a straw cowboy hat, and a red plaid pearl-snap western shirt, an acoustic guitar hanging on its strap in front of him, both hands resting on it. On the left stands a wiry man with a gray handlebar mustache, wearing tan firefighter turnout pants with reflective bands and red suspenders over a gray thermal shirt, a fiddle tucked under one arm and the bow in his other hand. On the right stands a tall, lanky man in faded denim overalls over a flannel shirt and a sagging knit cap, eyelids heavy, half asleep, leaning on the neck of an upright bass. All three face the camera with flat, deadpan expressions. Nobody smiles.

Behind them on the right, parked at an angle, is their rusty 1979 Ford Econoline van, dented, two-tone cream and faded brown, with a string of big old-fashioned colored bulbs looped along its roof rack and a lopsided pine wreath wired to the grille. Up a low hill behind them on the left stands one small white wooden country church with a plain steeple and a simple cross, every window glowing warm amber, a wreath on its door. The top of the steeple stays below the empty band of sky at the top of the cover. Far back near the church steps, a fourth man stands alone, small and soft, in a plain dark coat, his face not readable. Dark rolling hills run behind the church.

The camera stands in the churchyard about fifteen feet in front of the three men, at waist height, level, aimed at the man in the middle, with a normal lens. The three men are sharp. The van is a little softer. The church, the fourth man, and the hills are soft and loosely painted. Cold blue moonlight comes from high on the left, behind the church, and rims their hats and shoulders. The moon itself is out of frame. A warm light from low at the front left, outside the frame, lights their faces and the fronts of their instruments. The bulbs on the van throw small red, green, and gold glints on their hat brims and instruments.

The top fifth of the square is open night sky, deep navy fading to near black, empty across its full width: only faint pinprick stars, no moon, no bright star, no steeple, no branches, and no hat reaching into it. No snow is falling.

The bottom sixth of the square is a dark, nearly black band across the full width, like the worn dark lower edge of an old record sleeve. The snowy ground stays above that band, under their boots, with a little clear space between their boots and the band, and no snow runs into it. Centered on one line inside that dark band, in cream, slightly distressed, condensed serif capitals, large enough to read from across a room, is the title "A VERY SACKBUTS CHRISTMAS". No boot, bumper, or instrument touches the band or the letters. That title is the only text in the image. No other words, no logo, no wordmark, no letters on signs, no church sign, no letters or license plate on the van, no song titles, no signature.
```

Only if Firefly has no square choice and he is on Widescreen, add this line to the end of the prompt:

```
The canvas is wider than the cover. Keep the whole cover inside a centered square: the three men, the van, the church, the empty dark band across the top, and the full title line. Outside that square, the left and right sides are only empty dark night sky over dark empty hills and plain snowy ground, with no people, no van, no lights, and no letters.
```

## Notes

**Aspect.** The repo's Firefly driver (`lyricvideo/firefly/ff_batch.py`) only clicks Widescreen (16:9) or 9:16, so it is not the tool for this. Adam pastes this himself. In the Firefly window, open Aspect ratio and choose Square (1:1) if it is in the menu. If the menu has no square, choose Widescreen (16:9), paste the extra line above, and crop the centered square afterward (Photoshop Crop tool, ratio 1:1, centered). Reject any widescreen result where the title or a man runs outside the centered square.

**Size.** The two single covers on disk are 4096×4096. Upscale the chosen still to that size after he approves it, then add the logo, so the logo stays sharp.

**Logo.** Yes, add `E:\Music\The Sackbuts\Art\Sackbuts Logo.png` across the dark band at the top center after the picture is chosen. It does the same job it does on the two single covers: the band name across the top, the title along the bottom. Two Years Late puts it top center on open sky, the same place as here. Do not ask Firefly for a second wordmark. The prompt never names the band or asks for its logo. The title "A VERY SACKBUTS CHRISTMAS" stays painted into the picture because it is the album name, the same way each single paints its song title in the bottom line.

**Check each candidate.** Read the title letter by letter, because SACKBUTS is an unusual word and models sometimes garble it. Make sure nothing else is lettered: the van's sides and bumper, the church, and the sky should all be free of text. The top band should be dark and empty, with no hat brims, steeple, or bright star in it. The fourth man should stay small, soft, and ordinary. Reject him if he glows, has a halo, or is in a spotlight.

**References.** Generate this cover with no reference. The faces will be new each time. There is no face file for Earl, Luther, or Bedgo under `E:\Music\Art\The Group\`. If he later wants the faces from the band photo, do it in two steps. First, make an empty plate: run this same prompt with the three men, the fourth man, and the instruments taken out, and the words "No people anywhere in frame" added. Attach that empty plate as image 1. Image 1 must be empty of people, or Firefly locks their pose and camera from it. Then attach `E:\Music\The Sackbuts\Art\Firefly_Gemini Flash_Three middle-aged Southern country musicians standing in front of a rusty 1979 Ford E 745805.png` as image 2, and add to the prompt: "Image 2 is only the faces of the three men; take nothing else from image 2." Never make the band photo image 1. It brings its own camera, its own poses, and its own van. A photo reference can also pull the painting toward a photograph. If that happens, keep the version made without a reference.

**Status.** Prompt only. No image was generated in this task.
