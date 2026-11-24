# I Accidentally Destroyed Troy! (Short)

History World Short (59.5 s, 1080x1920): the red-cap doodle guy takes a "free" wooden horse to Troy, hears it sneeze,
opens the hatch, and lets out a free army. Ends with a one-star review and a portal exit.

Files: `story.py` (narration), `scenes.py` (7 vertical shots), `render.py` (vertical renderer with burned-in animated
subtitles), `narrate.py`, `audio.py`, `subtitles_en.srt`, `script.md`. Build:

    python3 narrate.py kokoro-v1.0.onnx voices-v1.0.bin build/vo
    python3 audio.py build/vo build/mix.wav
    python3 render.py video build/vo build/video.mp4
    ffmpeg -i build/video.mp4 -i build/mix.wav -c:v copy -c:a aac -shortest troy-short.mp4
