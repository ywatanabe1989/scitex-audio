---
name: scitex-audio
description: Text-to-speech, audio playback, and notification sounds with multiple backends (LuxTTS, ElevenLabs, gTTS, pyttsx3). Use when generating speech, playing audio alerts, or providing auditory feedback.
allowed-tools: mcp__scitex__audio_*
---

# Text-to-Speech with scitex-audio

## Quick Start

```python
from scitex_audio import speak

speak("Hello, experiment complete!")
speak("Results ready", backend="luxtts", speed=1.5)
speak("Saved audio", output_path="alert.mp3", play=False)
```

## Available Backends

| Backend | Quality | Offline | Default Speed | Notes |
|---------|---------|---------|---------------|-------|
| `elevenlabs` | Highest | No | x1.2 | Paid API key required |
| `luxtts` | High | Yes | x2.0 | Open-source, voice cloning, 48kHz |
| `gtts` | Medium | No | x1.5 | Free, Google TTS |
| `pyttsx3` | Basic | Yes | native | System TTS (espeak) |

Fallback order: elevenlabs -> luxtts -> gtts -> pyttsx3

## Smart Routing

- `SCITEX_AUDIO_MODE=auto` (default): local if audio sink available, relay if suspended
- `SCITEX_AUDIO_MODE=local`: force local playback
- `SCITEX_AUDIO_MODE=remote`: force relay server
- `SCITEX_AUDIO_RELAY_URL`: relay server URL for remote playback

## Common Workflows

### "Speak text aloud"

```python
speak("Analysis complete", speed=1.5)
speak("High quality", backend="elevenlabs", speed=1.2)
speak("Offline mode", backend="luxtts", num_threads=8)
```

### "Save audio file"

```python
speak("Recording", output_path="/tmp/alert.mp3", play=False, save=True)
```

## CLI Commands

```bash
scitex-audio speak "Hello world"
scitex-audio speak "Fast" --backend luxtts --speed 2.0

# MCP server
scitex-audio mcp start
scitex-audio mcp doctor
scitex-audio mcp install
scitex-audio mcp list-tools

# Skills
scitex-audio skills list
scitex-audio skills get SKILL
```

## MCP Tools (for AI agents)

| Tool | Purpose |
|------|---------|
| `audio_speak` | Speak text with smart routing and backend selection |
| `audio_speak_relay` | Speak via relay server |
