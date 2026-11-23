# How I Accidentally Ruined Napoleon's Coronation

History World episode 3 (5:35, 1080p): the red-cap doodle guy touches a golden leaf from Napoleon's laurel wreath, lands in
Paris on 2 December 1804, breaks two leaves off the wreath, gets the coach lost, trips Josephine's train and sneezes the crown
into Napoleon's hands.

Same code-generated pipeline as the other episodes: Kokoro TTS deep-voice narration, pycairo animation, synthesised score
(imperial march, cathedral organ and bells) and SFX, English subtitles.

| File | What it does |
|---|---|
| `script.md` | Narration with timestamps, scene notes, hook strategy, fact check |
| `story.py` | Narration text, one entry per shot |
| `scenes.py` | Paris, Notre-Dame, the coach, David's painting, characters (Napoleon, Josephine, Pius VII, David, Biennais, grenadiers, sisters) and all 29 shots |
| `gfx.py`, `render.py`, `narrate.py`, `audio.py`, `subtitles.py` | Shared engine |
| `subtitles_en.srt` | English captions |
| `build.sh` | Builds everything end to end |

The rendered MP4 is not committed; run `./build.sh` to rebuild it.
