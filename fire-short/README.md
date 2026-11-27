# I Witnessed the Great Fire of London! 🔥 (History World Short)

A Remotion project for a single vertical YouTube Short.

- 1080×1920, 9:16, 30 fps, **50.0 s**
- Final render: [`final/i-witnessed-the-great-fire-of-london.mp4`](final/i-witnessed-the-great-fire-of-london.mp4)

## Render

```bash
npm install
npm run render     # writes out/fire-short.mp4
npm run studio     # preview in the browser
```

## Structure

| Path | What it does |
|---|---|
| `src/timeline.json` | Scene timings, voice-over cues and SFX cues. Both the visuals and the audio scripts read it. |
| `src/components/Character.tsx` | The History World doodle guy with the red cap. Same component as the earlier Shorts, unchanged. |
| `src/components/Fire.tsx` | Animated flames (many rising "tongues" plus a turbulence warp), fire walls, embers, smoke |
| `src/components/London.tsx` | Jettied timber-framed houses, cobbled streets, Londoners in 1660s clothes, Farriner's bakery, Old St Paul's, ruins |
| `src/components/TimeMachine.tsx` | The time machine, its "POMPEII — AD 79" screen, and the portal |
| `src/scenes/` | The seven scripted scenes, each cut into 2–3 second shots |

## Historical notes

The facts shown on screen are the standard figures for the fire:

- **Start:** early on 2 September 1666, at Thomas Farriner's bakery on Pudding Lane.
- **Spread:** a strong east wind drove the fire west through tightly packed timber houses.
- **St Paul's:** Old St Paul's burned on 4 September. It is drawn with its square central tower (the spire fell after a lightning strike in 1561) and Inigo Jones's classical west portico.
- **End:** the fire was out by about 6 September. Around 13,200 houses and 87 parish churches were destroyed.

The narrator, the time machine and the Pompeii ending are fiction, framed as the character's comedy adventure.

## Audio (copyright-free)

- **Voice-over:** made with Kokoro, an open-weight TTS model (Apache-2.0). The narrator uses `am_puck`, the same History World voice as the earlier Shorts. The time machine uses `am_michael`, processed to sound robotic. To regenerate, run `python3 tools/generate_voice.py <folder with kokoro.onnx + voices.bin>`.
- **Music and sound effects:** synthesized from scratch (`python3 tools/generate_audio.py`). This covers the fire roar, crackle, crowd panic, church bells, timber crash, wind and portal, plus an original D-minor orchestral-style score. No samples or existing tracks are used.
