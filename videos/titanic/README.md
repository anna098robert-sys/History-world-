# I Accidentally Boarded the Titanic! (Remotion project)

History World long-form episode (6:10, 1920×1080, 30 fps). The red-cap doodle guy buys a $5 time machine at a flea market,
lands on the Titanic on 14 April 1912, fails hilariously to warn anyone, meets Captain Smith, hunts for the missing
binoculars, and, when disaster strikes, helps passengers to the lifeboats. Back home he promises never to time-travel
again… and accidentally sets the machine to **Pompeii — AD 79**.

Everything is original: vector animation written in React/SVG, synthesised narration, music and sound effects.

## Render the video

```bash
npm install
npm run render        # -> out/i-accidentally-boarded-the-titanic.mp4
npm run studio        # live preview / scrubbing in the browser
```

All assets needed for rendering are committed (`public/vo/*.mp3`, `public/audio/bed.mp3`, `public/fonts`).
`remotion.config.ts` uses the system Chromium headless shell when it exists; otherwise Remotion downloads its own browser.

## Project layout

| Path | What it is |
|---|---|
| `src/Root.tsx` | The `Titanic` composition (duration comes from `src/timeline.json`) |
| `src/Video.tsx` | One `<Sequence>` per shot, crossfades / white flashes, narration audio, music + SFX bed, subtitles |
| `src/scenes.tsx` | All 33 shots, each synced to its narration sentences via `cue()` |
| `src/Hero.tsx` | The doodle hero (reference design) and the cast built on the same body (captain, waiter, passengers, …) |
| `src/bg.tsx`, `src/props.tsx` | Backgrounds (flea market, decks, Grand Staircase, bridge, crow's nest, open sea, …) and props (time machine, ship, iceberg, lifeboats) |
| `src/fx.tsx` | Camera, pop-up text, comic bursts, fact cards, vignette, sparkles |
| `src/Subtitles.tsx` | Synchronised English subtitles with the spoken word highlighted |
| `src/timeline.json` | Shot start times + sentence timings (generated) |
| `tools/story.py` | Narration script (946 words) |
| `tools/narrate.py` | Text-to-speech (Kokoro, Liam/Puck blend), one sentence at a time for exact timing |
| `tools/timeline.py` | Builds `src/timeline.json` |
| `tools/audio.py`, `tools/audio_lib.py` | Original synthesised score + sound effects, ducked under the voice |
| `tools/stills.mjs` | Review contact sheets per shot |
| `tools/build.sh` | Full rebuild (voice → timeline → audio → render) |
| `script.md` | Narration with timestamps per scene + fact check |
