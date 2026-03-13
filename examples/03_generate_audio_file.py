#!/usr/bin/env python3
"""Generate audio files without playback.

Demonstrates:
- Generating audio bytes
- Saving to file without playing
- Using generate_bytes() for programmatic access
"""

import os

from scitex_audio import available_backends, generate_bytes, speak

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "03_generate_audio_file_out")
os.makedirs(OUTPUT_DIR, exist_ok=True)

backends = available_backends()
if not backends:
    print("No TTS backends available.")
else:
    # Save to file without playing
    output_path = os.path.join(OUTPUT_DIR, "greeting.mp3")
    result = speak(
        "This audio was saved to a file.",
        output_path=output_path,
        play=False,
    )
    print(f"Saved audio to: {output_path}")

    # Generate raw bytes (useful for streaming/HTTP responses)
    audio_bytes = generate_bytes("Hello as bytes")
    print(f"Generated {len(audio_bytes)} bytes of audio")

    # Save bytes manually
    bytes_path = os.path.join(OUTPUT_DIR, "bytes_output.mp3")
    with open(bytes_path, "wb") as f:
        f.write(audio_bytes)
    print(f"Saved bytes to: {bytes_path}")
