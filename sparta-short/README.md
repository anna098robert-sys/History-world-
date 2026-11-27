# Peloponnesian War: Caught in the Middle (History World)

A 12-second animated scene for a YouTube Short. It has no text, no subtitles and no voice-over.

- 1080×1920, 9:16, 30 fps
- Final render: [`final/peloponnesian-war-caught-in-the-middle.mp4`](final/peloponnesian-war-caught-in-the-middle.mp4)

```bash
npm install
npm run render   # writes out/sparta-short.mp4
```

## Beats (`src/timeline.json`)

| Time | Action |
|---|---|
| 0–2 s | Medium shot. The doodle guy smiles between two glaring phalanxes. Banners wave and spears are beaten on shields. |
| 2 s | War cry. The armies shake their spears and he flinches. |
| 3.3 s | Spears lower and both phalanxes start marching in step. The camera begins its push-in. |
| 3.8 s / 4.9 s | He looks left, then right. |
| 6.0 s | His eyes widen and his cap pops up. |
| 6.4–8.6 s | He slowly raises his hands in panic. |
| 9–12 s | Close-up. He trembles as spear points close in from both sides, then gulps. |

## Historical details

- **Date:** the Peloponnesian War began in 431 BC.
- **Spartans:** red cloaks and the lambda (Λ) shield device.
- **Athenians:** owl-of-Athena shield devices.
- **Equipment:** Corinthian helmets with horsehair crests, round bronze aspis shields, linen cuirasses, greaves and dory spears.
- **Music:** the melody imitates an aulos. Spartan phalanxes were known for advancing in step to aulos players.

Artistic license, for the comedy:
- **Banners:** hoplite armies didn't really carry waving flags. They're included because the brief asked for them.
- **Head-on clash:** the war's first year was mostly a Spartan invasion of Attica while the Athenians stayed behind their walls.

## Audio

All sound is synthesized from scratch with `python3 tools/generate_audio.py`. That covers wind, shield clangs, the massed war cry, marching footsteps, a heartbeat and a gulp, plus an original aulos-and-drum score. No samples or existing music are used.

The character is the shared History World doodle guy, with the same model as the earlier Shorts. The only difference is that his panicked eyebrows now tilt in a worried shape.
