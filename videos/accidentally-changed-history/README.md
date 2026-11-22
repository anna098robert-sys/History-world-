# I Accidentally Changed History

An animated History World episode (5:53, 1080p): the red-cap doodle guy touches a museum pocket watch and
"accidentally" causes the Leaning Tower of Pisa, Newton's apple and Fleming's penicillin.

Everything is generated from code: narration (Kokoro TTS, deep male voice), vector animation (pycairo),
synthesised music and sound effects (numpy/scipy), muxed with ffmpeg.

| File | What it does |
|---|---|
| `script.md` | Full narration with timestamps, scene notes and a fact check |
| `story.py` | Narration text, one entry per shot |
| `narrate.py` | Text to speech, pitch and EQ, sentence timing (`timing.json`) |
| `gfx.py` | Drawing primitives, the doodle characters, props |
| `scenes.py` | Backgrounds and all 30 animated shots |
| `render.py` | Timeline, transitions, parallel rendering to H.264 (`stills` mode for contact sheets) |
| `audio.py` | Score per era, sound effects, ducking, final mix |
| `subtitles.py` / `subtitles_en.srt` | English captions |
| `build.sh` | Runs everything end to end |

The rendered MP4 is not committed (about 76 MB). Run `./build.sh` to rebuild it.
