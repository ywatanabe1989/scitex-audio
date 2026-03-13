#!/usr/bin/env python3
"""Backend selection and voice configuration example.

Demonstrates:
- Listing available backends
- Selecting a specific backend
- Configuring voice/language
- Speed control
"""

from scitex_audio import FALLBACK_ORDER, available_backends, get_tts

# Show fallback order and availability
print("TTS Backend Fallback Order:")
backends = available_backends()
for b in FALLBACK_ORDER:
    status = "available" if b in backends else "not installed"
    print(f"  {b}: {status}")

# Use a specific backend if available
if "gtts" in backends:
    tts = get_tts("gtts")
    voices = tts.get_voices()
    print(f"\nGoogle TTS languages: {len(voices)} available")
    for v in voices[:5]:
        print(f"  {v['name']} ({v['id']})")

    # Speak in a specific language
    result = tts.speak("Bonjour le monde", voice="fr", play=True)
    print(f"\nSpoke in French: played={result.get('played')}")
