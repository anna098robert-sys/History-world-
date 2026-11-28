# I Witnessed the Last Day of Pompeii! (YouTube Short, Remotion)

45 s, 1080×1920, 30 fps. The red-cap doodle guy walks through Pompeii on an ordinary day in 79 AD. Then Vesuvius
erupts, ash buries the city, and almost 2,000 years later archaeologists uncover it again.

```bash
npm install
cd tools && STORY=short_story SPEED=1.0 GAP=0.24 python3 narrate.py <kokoro.onnx> <voices.bin> ../public/vo && cd ..
python3 tools/timeline.py   # scene timing (7 scenes, 45 s) -> src/timeline.json
python3 tools/audio.py      # original score + volcano SFX -> public/audio/bed.mp3
npm run render              # -> out/i-witnessed-the-last-day-of-pompeii.mp4 (-14 LUFS)
node tools/stills.mjs out/stills   # review contact sheets
```

| Path | What it is |
|---|---|
| `src/scenes.tsx` | The 7 scenes plus Pompeii assets: Vesuvius, the eruption column, falling ash, Roman houses and shops, stepping-stone street, Romans, archaeologists |
| `src/Video.tsx` | Sequences, narration, music bed, large synced subtitles |
| `src/Hero.tsx`, `src/fx.tsx`, `src/lib.ts`, ... | Shared with the other episodes (same hero design) |
| `tools/short_story.py` | Narration (exact lines from the brief) |
| `subtitles_en.srt` | English captions |

Historical notes: the eruption of Vesuvius is traditionally dated to 79 AD, and Pompeii was buried under metres of
ash and pumice. Systematic excavations began in 1748 and continue today. No victims are shown. Voice, music and SFX
are all synthesised.
