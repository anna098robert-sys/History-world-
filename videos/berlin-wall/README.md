# I Witnessed the Fall of the Berlin Wall! (long-form, Remotion)

About 6:16, 1920×1080, 30 fps, English narration with burned-in subtitles. The red-cap doodle guy's $5 time machine
misfires to Berlin in 1961. He sees the Wall go up, years of life beside it (Kennedy, Tunnel 57, the balloon escape,
the memorial, Reagan), then Leipzig, Schabowski's press conference, the opening at Bornholmer Strasse, the party at
the Brandenburg Gate, the Mauerspechte, and reunification. He comes home with a piece of the Wall.

```bash
npm install
STORY=story SPEED=0.88 python3 tools/narrate.py <kokoro.onnx> <voices.bin> public/vo   # voice (Kokoro TTS)
python3 tools/timeline.py   # -> src/timeline.json (+ mp3 narration)
python3 tools/audio.py      # -> public/audio/bed.mp3 (original music + SFX, ducked)
npm run render              # -> out/i-witnessed-the-fall-of-the-berlin-wall.mp4 (loudness -14 LUFS)
node tools/stills.mjs out/stills [shot ...]   # review contact sheets
```

| Path | What it is |
|---|---|
| `src/scenes.tsx` | 27 narrated shots plus the title and end card |
| `src/berlin.tsx` | Berlin set pieces and cast: Wall, barbed wire, watchtower, Brandenburg Gate, Trabant, Berliners, guards, official, candles |
| `src/Video.tsx`, `src/Subtitles.tsx` | Sequences, narration, music bed, synced subtitles |
| `src/Hero.tsx`, `src/fx.tsx`, `src/props.tsx`, `src/bg.tsx`, `src/lib.ts` | Shared with the earlier episodes (same hero design) |
| `tools/story.py` | Narration (916 words) |
| `script.md` | Script and fact check |
| `subtitles_en.srt` | English captions |

Voice (Kokoro TTS), music and sound effects are all synthesised. No samples or copyrighted material are used.
