#!/usr/bin/env python3
"""Basic text-to-speech example.

Demonstrates the simplest usage of scitex-audio:
- Auto-selects the best available backend
- Speaks text with default settings
"""

from scitex_audio import available_backends, speak

# List what's available
backends = available_backends()
print(f"Available backends: {backends}")

if not backends:
    print("No TTS backends installed. Install one:")
    print("  pip install pyttsx3   # + apt install espeak-ng")
    print("  pip install gTTS      # requires internet")
else:
    # Speak with auto-selected backend
    result = speak("Hello from SciTeX Audio!", play=True)
    print(f"Backend used: {result.get('backend')}")
    print(f"Audio played: {result.get('played')}")
