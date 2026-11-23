# How I Accidentally Did NOT Destroy the Great Wall of China

History World episode 2 (5:24, 1080p): the red-cap doodle guy touches a Ming brick, lands at Jinshanling in 1570,
fills the mortar with extra sticky rice, mistakes a beacon tower for a campfire, and accidentally saves the wall.

Built on the same code-generated pipeline as `../accidentally-changed-history/`: Kokoro TTS deep-voice narration,
pycairo animation, synthesised score and SFX (pentatonic Chinese theme, war drums, gong), English subtitles.

| File | What it does |
|---|---|
| `script.md` | Narration with timestamps, scene notes, hook strategy, fact check |
| `story.py` | Narration text, one entry per shot |
| `scenes.py` | Landscape, wall, beacons, characters (workers, soldiers, foreman, cook, raiders) and all 29 shots |
| `gfx.py`, `render.py`, `narrate.py`, `audio.py`, `subtitles.py` | Shared engine (renderer, TTS, mix) |
| `subtitles_en.srt` | English captions |
| `build.sh` | Builds everything end to end |

Extra requirement compared with episode 1: a CJK font (`fonts-noto-cjk`, "Noto Serif CJK SC") for the brick inscriptions.
The rendered MP4 is not committed (about 61 MB); run `./build.sh` to rebuild it.
