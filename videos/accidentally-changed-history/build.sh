#!/usr/bin/env bash
# Build "I Accidentally Changed History" end to end.
# Needs: python3 with kokoro-onnx soundfile numpy scipy pycairo; ffmpeg (with rubberband);
# fonts "Luckiest Guy" and "Patrick Hand" installed; Kokoro model files (kokoro-v1.0.onnx, voices-v1.0.bin).
set -euo pipefail
MODEL=${MODEL:-kokoro-v1.0.onnx}
VOICES=${VOICES:-voices-v1.0.bin}
OUT=${OUT:-build}
mkdir -p "$OUT"
python3 narrate.py "$MODEL" "$VOICES" "$OUT/vo"            # deep-voice narration + sentence timing
python3 audio.py "$OUT/vo" "$OUT/mix.wav"                  # score + SFX + voice mix
python3 render.py video "$OUT/vo" "$OUT/video_silent.mp4"  # 1080p24 animation
python3 subtitles.py "$OUT/vo" "$OUT/subtitles_en.srt"
ffmpeg -y -loglevel error -i "$OUT/video_silent.mp4" -i "$OUT/mix.wav" -c:v copy -c:a aac -b:a 192k \
  -shortest -movflags +faststart "$OUT/i-accidentally-changed-history.mp4"
echo "done: $OUT/i-accidentally-changed-history.mp4"
