# I Witnessed the Fall of the Berlin Wall! (YouTube Short, Remotion)

45.4 s, 1080×1920, 30 fps. The red-cap doodle guy arrives in Berlin on 9 November 1989 and witnesses the crowds,
the opening of the border, the hammers on the Wall and families reunited, until his time machine starts flashing again.

```bash
npm install
npm run render     # -> out/berlin-wall-short.mp4 (loudness-normalised)
npm run studio     # live preview
```

| Path | What it is |
|---|---|
| `src/scenes.tsx` | The 7 scenes + Berlin assets (Wall, skyline with TV tower and Brandenburg Gate, checkpoint, Trabant, 1989 Berliners, border guard) |
| `src/Video.tsx` | Sequences, narration, music bed, large synced subtitles |
| `src/Hero.tsx`, `src/fx.tsx`, `src/props.tsx`, `src/bg.tsx`, `src/lib.ts` | Shared with the Titanic project (same hero design) |
| `src/timeline.json` | Scene timing (`tools/timeline.py`) |
| `tools/short_story.py` | Narration (exact lines from the brief) |
| `tools/narrate.py`, `tools/audio.py`, `tools/audio_lib.py` | Voice, original music + SFX |
| `subtitles_en.srt` | English captions |

Facts shown: the Wall stood from 13 August 1961 to 9 November 1989 (28 years); the first crossing to open that night
was Bornholmer Straße; people chipped pieces off the Wall with hammers and chisels in the following days.
The families and the hero are fictional; their division and reunion stand in for the many real ones.
