# I Accidentally Woke Up a Mummy! 💀 (History World Short)

A Remotion project for a single vertical YouTube Short.

- 1080×1920, 9:16, 30 fps, **39.5 s**
- Final render: [`final/i-accidentally-woke-up-a-mummy.mp4`](final/i-accidentally-woke-up-a-mummy.mp4)

## Render

```bash
npm install
npm run render     # writes out/mummy-short.mp4
npm run studio     # preview and scrub in the browser
```

## Structure

| Path | What it does |
|---|---|
| `src/timeline.json` | The one source of truth for scene timings, voice-over cues and SFX cues. Both the visuals and the audio scripts read it. |
| `src/components/Character.tsx` | The History World doodle guy: round white head, dot eyes, red cap. Every scene uses this one component. |
| `src/components/Mummy.tsx` | The mummy, with glowing eyes, poses, talking and "needs the bathroom" wiggle |
| `src/components/Environment.tsx` | Hieroglyph corridors (side view and head-on), torches, golden door, tomb chamber, sarcophagus |
| `src/components/Effects.tsx` | Camera (zoom, pan, shake), smoke, dust, speed lines, flashes, comic bursts |
| `src/components/Subtitles.tsx` | Big captions synced to the narration, with the current word highlighted |
| `src/scenes/Scene1…6*.tsx` | The six scripted scenes, each cut into 2–3 second shots |
| `public/audio/` | Voice-over, sound effects and music (already generated) |

## Audio (all copyright-free)

- **Voice-over:** made with [Kokoro](https://github.com/thewh1teagle/kokoro-onnx), an open-weight TTS model (Apache-2.0), voice `am_puck` (energetic American male).
  To regenerate: `pip install kokoro-onnx soundfile`, download `kokoro-v1.0.onnx` and `voices-v1.0.bin` from the model-files-v1.0 release, then run `python3 tools/generate_voice.py <folder-with-model-files>`.
- **Music and SFX:** synthesized from scratch with numpy (`python3 tools/generate_audio.py`). They use no samples or existing tracks. The music ducks under the narration automatically.
- **Font:** Luckiest Guy (open license, via @fontsource), bundled in `public/fonts`.
