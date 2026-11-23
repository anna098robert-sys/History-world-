# I Accidentally Stole the Mona Lisa!

History World episode 5 (6:42, 1920x1080, 24 fps): the red-cap doodle guy touches an old Louvre ticket dated
21 August 1911, lands in Paris on the day of the theft, sneaks into the Louvre disguised as a cleaner, catches the
painting from the fleeing thief, is mistaken for the thief, escapes through Paris (crashing into the same baguette cart
as the cold open), returns the painting to the police the same night, and comes home to find history rewritten.
Final twist: the ticket now reads NEXT DESTINATION: TITANIC, 1912.

| File | What it does |
|---|---|
| `script.md` | Narration, scene map against the 11-scene brief, scene notes, fact check, editing plan |
| `story.py` | Narration text (replace it with your own script to re-voice) |
| `scenes.py` | Paris 1911 streets, Louvre facade/Grand Gallery/Salon Carré/Daru staircase, police station, characters, all 28 shots |
| `egypt_lib.py`, `helpers.py`, `gfx.py` | Shared drawing library (hero, bedroom, effects) |
| `render.py`, `narrate.py`, `audio.py`, `subtitles.py` | Renderer, TTS, score + SFX mix, captions |
| `subtitles_en.srt` | English captions |
| `build.sh` | Builds everything end to end |

The rendered MP4 is not committed; run `./build.sh` to rebuild it.
