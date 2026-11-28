# I Accidentally Started a War! (History World Short)

A Remotion project for a single vertical YouTube Short. It has no subtitles, captions or watermark, and the story is told visually.

- 1080×1920, 9:16, 30 fps, **54.0 s**
- Final render: [`final/i-accidentally-started-a-war.mp4`](final/i-accidentally-started-a-war.mp4)

```bash
npm install
npm run render   # writes out/war-short.mp4
```

## Story beats (`src/timeline.json`)

| Time | Scene |
|---|---|
| 0–5 s | **Hook:** a burning battlefield behind him. He turns to camera, a crash zoom hits his face ("Uh-oh."), then a VHS rewind into the flashback. |
| 5–12 s | **Mission:** an official hands him two sealed scrolls. Picture bubbles explain them: blue seal → king, red seal → friend. "Got it!" He sprints through the city juggling the two scrolls. |
| 12–20 s | **Tension:** swords sharpened with sparks, generals arguing over a map, citizens slamming shutters, enemy campfires on the hill. |
| 20–30 s | **Mistake:** he hands the king the RED scroll. The seal cracks, revealing a rude doodle of the king with donkey ears. The king boils (steam!), slams the table and roars "WAR!" |
| 30–40 s | **Chaos:** hoplites charge through the streets, cavalry gallops, shields clash. He stands frozen, guilty, still holding the blue scroll. |
| 40–48 s | **Explanation:** soldiers close in. He holds up both scrolls and swaps them to show the mix-up ("I mixed up the letters!"), then gets blank stares, crickets and "Heh… heh…" |
| 48–54 s | **Ending:** close-up. He blushes, hides the scrolls behind his back and whistles. "…Oops." Then a dun-dun-DUN triple crash zoom. |

The letters carry no writing. The joke is told with pictures: an olive-branch/crown bubble, a smiley "friend" bubble, and the donkey-ear caricature.

## Historical setting

- **Setting:** a Classical Greek city with Doric stoas and temples, whitewashed houses with terracotta roofs, and a market with amphorae.
- **Soldiers:** hoplites with Corinthian helmets, bronze aspis shields, linen cuirasses and dory spears, plus cavalry.
- **Letters:** papyrus scrolls with wax seals.
- **Fiction:** the two city-states, the king and the letter mix-up are invented for comedy. They use generic shield devices (a trident and a star) rather than real city emblems, so the video doesn't imply that a real war started this way.

## Audio (copyright-free)

- **Voices:** a few short spoken lines, made with Kokoro (open-weight TTS, Apache-2.0). The hero uses `am_puck`, the History World voice. The king uses `am_onyx`, pitched down. To regenerate, run `python3 tools/generate_voice.py <folder with kokoro.onnx + voices.bin>`.
- **Sound effects and music:** synthesized from scratch with `python3 tools/generate_audio.py`. That covers battle, rewind, whetstone, wax-seal crack, table slam, steam whistle, gallop, crickets, whistle, the dun-dun-DUN sting, and an original lyre/reed/drum score.
