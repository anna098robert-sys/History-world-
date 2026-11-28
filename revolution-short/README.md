# I Saved a Man Who Was Supposed to Die! (History World Short)

A Remotion project for a single vertical YouTube Short. It has no subtitles, no on-screen text and no watermark.

- 1080×1920, 9:16, 30 fps, **58.5 s**
- Final render: [`final/i-saved-a-man-who-was-supposed-to-die.mp4`](final/i-saved-a-man-who-was-supposed-to-die.mp4)

```bash
npm install
npm run render   # writes out/revolution-short.mp4
```

## Story beats (`src/timeline.json`)

| Time | Scene |
|---|---|
| 0–5 s | **Hook:** a lantern-lit prison corridor. A prisoner's arm reaches through the bars ("Help me…"), giant shadows swell on the walls, and he turns to camera for a crash zoom. The lantern gusts out. |
| 5–13 s | **Prison:** he walks the stone corridor past iron doors and candles, peeks into a grille, and a rat makes him jump. Then he tiptoes down a long vaulted corridor. |
| 13–22 s | **The prisoner:** a young man shakes the bars and begs ("They'll take me at dawn!"). Two-shot, then a tearful close-up with the scaffold silhouetted through the cell window, then the hero's sympathetic close-up. A dawn bell rings. |
| 22–32 s | **Decision:** he looks left and right, pulls out the iron key (glint, "Shhh!"), and the key turns in the lock in an extreme close-up. The bars swing open and the prisoner bolts into the dark. |
| 32–43 s | **Reveal:** a sunrise flash to a Paris square with tricolours and a crowd. He spots a wanted poster: a crash zoom to the prisoner's face, then to his own horrified face ("Uh-oh."). |
| 43–53 s | **Consequences:** the escaped man, now cloaked, melts into the crowd. National Guardsmen search the streets while he hides behind a bread stall. |
| 53–58.5 s | **Twist:** alone in a dark attic with the key, a poster slides under the door, and it shows *his* face. He looks at camera ("…What have I done?"), the candle goes out, fade to black. |

The posters have no writing, only a portrait, a coin purse for the reward and a red wax seal.

## Character

The hero is the shared History World doodle guy, with the same head, face, proportions and red baseball cap. In this video he wears a 1790s outfit in every scene: a short navy *carmagnole* jacket with red lapels and brass buttons, a white cravat, a sash, and cream striped trousers. It's an `outfit="revolution"` option added to `Character.tsx`, applied everywhere through the `Hero` wrapper.

## Historical setting

- **Setting:** the Paris of the Revolution (c. 1793–94).
- **Prison:** vaulted stone, iron doors and straw floors.
- **Streets:** mansard-roofed houses with shutters and iron balconies, tricolour flags, and a bread stall.
- **People:** sans-culottes in red liberty caps with cockades, and National Guardsmen in blue coats and bicornes carrying muskets.
- **Scaffold:** the guillotine appears only as a distant silhouette, never in use.
- **Fiction:** the prisoner and the story are invented. No real person is depicted.

## Audio (copyright-free)

- **Voices:** short lines made with Kokoro (open-weight TTS, Apache-2.0). The hero uses `am_puck`. The prisoner uses `am_liam`, with whispers and stone-hall echo added. To regenerate, run `python3 tools/generate_voice.py <folder with kokoro.onnx + voices.bin>`.
- **Sound effects and music:** synthesized from scratch with `python3 tools/generate_audio.py`. That covers chains, dripping water, stone footsteps, the rat squeak, rattling bars, the dawn bell, key and lock, crowd, rooster, military drums, boots, paper and candle puff, plus an original harpsichord, strings and drums score.
