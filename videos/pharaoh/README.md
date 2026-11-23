# I Accidentally Became a Pharaoh!

History World episode 4 (6:08, 1920x1080, 24 fps): the red-cap doodle guy presses the red button on a golden box from
under his bed, lands in Ancient Egypt, is mistaken for a pharaoh, builds a slide on a pyramid, crashes into a chariot,
and turns his slide idea into irrigation channels that save the farms from a Nile flood.

Same code-generated pipeline as the other episodes, with a young energetic American narrator (Kokoro TTS, Liam/Puck blend).

| File | What it does |
|---|---|
| `script.md` | Narration with timestamps, scene notes mapped to the 12-scene brief, fact check |
| `story.py` | Narration text, one entry per shot |
| `scenes.py` | Bedroom, golden box, portal, Giza, palace, slide, chariot, Nile, channels, classroom; all 27 shots |
| `helpers.py` | Camera, horse, fire and VHS helpers shared with earlier episodes |
| `gfx.py`, `render.py`, `narrate.py`, `audio.py`, `subtitles.py` | Engine (character, renderer, TTS, score + SFX mix) |
| `subtitles_en.srt` | English captions |
| `build.sh` | Builds everything end to end |

The rendered MP4 is not committed; run `./build.sh` to rebuild it.
