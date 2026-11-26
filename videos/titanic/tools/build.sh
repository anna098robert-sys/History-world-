#!/usr/bin/env bash
# Full rebuild: narration -> timeline -> music/SFX bed -> MP3 assets -> Remotion render.
# Needs: node 18+, python3 with kokoro-onnx soundfile numpy scipy, ffmpeg,
#        Kokoro model files (kokoro-v1.0.onnx, voices-v1.0.bin).
# If you only want to re-render the video, skip all of this and run:  npm install && npm run render
set -euo pipefail
cd "$(dirname "$0")/.."
MODEL=${MODEL:-kokoro-v1.0.onnx}
VOICES=${VOICES:-voices-v1.0.bin}
(cd tools && SPEED=0.86 python3 narrate.py "$MODEL" "$VOICES" ../public/vo) && rm -f public/vo/*_raw.wav
python3 tools/timeline.py
python3 tools/audio.py
python3 tools/to_mp3.py
npm run render
