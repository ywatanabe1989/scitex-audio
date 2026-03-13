# SciTeX Audio (<code>scitex-audio</code>)

<p align="center">
  <a href="https://scitex.ai">
    <img src="docs/scitex-logo-blue-cropped.png" alt="SciTeX" width="400">
  </a>
</p>

<p align="center"><b>Text-to-Speech with multiple backends for scientific workflows</b></p>

<p align="center">
  <a href="https://badge.fury.io/py/scitex-audio"><img src="https://badge.fury.io/py/scitex-audio.svg" alt="PyPI version"></a>
  <a href="https://scitex-audio.readthedocs.io/"><img src="https://readthedocs.org/projects/scitex-audio/badge/?version=latest" alt="Documentation"></a>
  <a href="https://github.com/ywatanabe1989/scitex-audio/actions/workflows/test.yml"><img src="https://github.com/ywatanabe1989/scitex-audio/actions/workflows/test.yml/badge.svg" alt="Tests"></a>
  <a href="https://www.gnu.org/licenses/agpl-3.0"><img src="https://img.shields.io/badge/License-AGPL--3.0-blue.svg" alt="License: AGPL-3.0"></a>
</p>

<p align="center">
  <a href="https://scitex-audio.readthedocs.io/">Full Documentation</a> · <code>pip install scitex-audio</code>
</p>

---

## Problem

Scientific workflows increasingly use AI agents that run on remote servers or headless environments. These agents need to communicate results audibly — for experiment completion notifications, error alerts, or accessibility — but have no direct access to audio hardware.

## Solution

SciTeX Audio provides a **unified TTS interface** with automatic backend fallback and smart local/remote routing. It works on local machines, remote servers (via relay), and WSL environments with automatic audio path detection.

| Backend | Quality | Cost | Internet | Offline | Default Speed |
|---------|---------|------|----------|---------|---------------|
| **ElevenLabs** | High | Paid | Required | No | 1.2x |
| **LuxTTS** | High | Free | First download | Yes | 2.0x |
| **Google TTS** | Good | Free | Required | No | 1.5x |
| **System TTS** | Basic | Free | No | Yes | 150 wpm |

<p align="center"><sub><b>Table 1.</b> Supported TTS backends. The fallback order (elevenlabs → luxtts → gtts → pyttsx3) ensures the best available quality is always used.</sub></p>

## Installation

Requires Python >= 3.10.

```bash
pip install scitex-audio
```

Install with specific backends:

```bash
pip install scitex-audio[gtts]         # Google TTS
pip install scitex-audio[pyttsx3]      # System TTS (+ apt install espeak-ng)
pip install scitex-audio[elevenlabs]   # ElevenLabs
pip install scitex-audio[luxtts]       # LuxTTS (voice cloning, offline)
pip install scitex-audio[all]          # Everything
```

## Quick Start

```python
from scitex_audio import speak, available_backends

# Check what's available
print(available_backends())  # e.g., ['gtts', 'pyttsx3']

# Speak with auto-selected backend
speak("Hello from SciTeX Audio!")

# Choose a specific backend
speak("Bonjour", backend="gtts", voice="fr")

# Save without playing
speak("Save this", output_path="output.mp3", play=False)
```

## Three Interfaces

<details>
<summary><strong>Python API</strong></summary>

<br>

```python
import scitex_audio

scitex_audio.speak("Hello!")                         # auto backend
scitex_audio.speak("Fast", backend="gtts", speed=1.5)
scitex_audio.available_backends()                    # list backends
scitex_audio.check_wsl_audio()                       # WSL audio status
scitex_audio.generate_bytes("As bytes")              # raw MP3 bytes
scitex_audio.stop_speech()                           # kill playback

tts = scitex_audio.get_tts("gtts")                   # get engine
tts.speak("With engine", voice="fr")
```

> **[Full API reference](https://scitex-audio.readthedocs.io/)**

</details>

<details>
<summary><strong>CLI Commands</strong></summary>

<br>

```bash
scitex-audio --help-recursive             # Show all commands
scitex-audio speak "Hello world"          # Speak text
scitex-audio speak "Bonjour" -b gtts -v fr
scitex-audio backends                     # List backends
scitex-audio check                        # Audio status (WSL)
scitex-audio stop                         # Stop playback
scitex-audio relay --port 31293           # Start relay server
scitex-audio list-python-apis             # List Python API tree
scitex-audio mcp list-tools               # List MCP tools
```

> **[Full CLI reference](https://scitex-audio.readthedocs.io/)**

</details>

<details>
<summary><strong>MCP Server — for AI Agents</strong></summary>

<br>

AI agents can speak through the MCP protocol for notifications and accessibility.

| Tool | Description |
|------|-------------|
| `audio_speak` | Convert text to speech with backend fallback |
| `list_backends` | List available TTS backends and status |
| `check_audio_status` | Check WSL audio connectivity |
| `announce_context` | Announce current directory and git branch |

<sub><b>Table 2.</b> Four MCP tools available for AI-assisted audio. All tools accept JSON parameters and return JSON results.</sub>

```bash
scitex-audio mcp start
```

> **[Full MCP specification](https://scitex-audio.readthedocs.io/)**

</details>

## Remote Audio Relay

When agents run on remote servers (NAS, cloud, HPC), they have no speakers. The **relay server** solves this: the local machine (with speakers) runs a lightweight HTTP server, and the remote agent sends speech requests over an SSH tunnel.

### Architecture

```
Remote Server (NAS/Cloud)          Local Machine (has speakers)
┌─────────────────────┐            ┌──────────────────────┐
│ AI Agent            │            │ Relay Server         │
│   speak("Hello")    │            │   scitex-audio relay │
│     ↓               │            │     ↓                │
│ POST /speak ────────┼── SSH ─────┼→ TTS engine          │
│   (port 31293)      │  tunnel    │     ↓                │
│                     │            │   🔊 Speakers        │
└─────────────────────┘            └──────────────────────┘
```

### Setup

**Step 1: Start relay on local machine (has speakers)**

```bash
scitex-audio relay --port 31293
```

**Step 2: SSH tunnel from local to remote**

Add to your `~/.ssh/config`:

```ssh-config
Host my-server
  HostName 192.168.0.69
  User myuser
  RemoteForward 31293 127.0.0.1:31293   # Audio relay
```

Then connect: `ssh my-server`. The tunnel maps remote port 31293 back to your local relay.

**Step 3: Configure remote environment**

On the remote server, set:

```bash
export SCITEX_AUDIO_MODE=remote
export SCITEX_AUDIO_RELAY_PORT=31293
# URL is auto-detected from the tunnel (localhost:31293)
```

Now `speak("Hello")` on the remote server plays audio on your local speakers.

### Relay Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/speak` | POST | Play TTS (`{"text": "...", "backend": "gtts"}`) |
| `/health` | GET | Health check (returns `{"status": "ok"}`) |
| `/list_backends` | GET | List available backends |

### Auto-Start Relay (Shell Profile)

```bash
# ~/.bashrc or ~/.bash_profile (local machine with speakers)
_start_audio_relay() {
    local port="${SCITEX_AUDIO_RELAY_PORT:-31293}"
    # Skip if already running
    curl -sf "http://localhost:$port/health" >/dev/null 2>&1 && return
    # Start in background
    scitex-audio relay --port "$port" --force &>/dev/null &
    disown
}
_start_audio_relay
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SCITEX_AUDIO_MODE` | `auto` | Audio mode: `local`, `remote`, or `auto` |
| `SCITEX_AUDIO_RELAY_URL` | *(auto)* | Full relay URL (e.g., `http://localhost:31293`) |
| `SCITEX_AUDIO_RELAY_HOST` | *(none)* | Relay host (combined with port to build URL) |
| `SCITEX_AUDIO_RELAY_PORT` | `31293` | Relay server port |
| `SCITEX_AUDIO_HOST` | `0.0.0.0` | Relay server bind host |
| `SCITEX_AUDIO_ELEVENLABS_API_KEY` | *(none)* | ElevenLabs API key |
| `SCITEX_DIR` | `~/.scitex` | Base directory for audio cache files |
| `SCITEX_CLOUD` | *(none)* | Set to `true` for browser relay mode (OSC escape) |

<p align="center"><sub><b>Table 3.</b> Environment variables. Port 31293 encodes "sa-i-te-ku-su" (サイテクス) in Japanese phone keypad mapping.</sub></p>

### Mode Resolution

- **`auto`** (default): Checks local audio availability. If suspended/unavailable and relay URL detected, routes to relay. Otherwise uses local.
- **`local`**: Always use local TTS engine and speakers.
- **`remote`**: Always send speech to relay server. Fails if relay unreachable.

## Part of SciTeX

SciTeX Audio is part of [**SciTeX**](https://scitex.ai). When used inside the orchestrator package `scitex`, audio integrates with the session system for automatic experiment notifications:

```python
import scitex

@scitex.session
def main(CONFIG=scitex.INJECTED):
    data = scitex.io.load("input.csv")
    result = process(data)
    scitex.io.save(result, "output.csv")
    scitex.audio.speak("Experiment complete")  # notify via TTS
    return 0
```

The SciTeX ecosystem follows the Four Freedoms for researchers:

>Four Freedoms for Research
>
>0. The freedom to **run** your research anywhere — your machine, your terms.
>1. The freedom to **study** how every step works — from raw data to final manuscript.
>2. The freedom to **redistribute** your workflows, not just your papers.
>3. The freedom to **modify** any module and share improvements with the community.
>
>AGPL-3.0 — because research infrastructure deserves the same freedoms as the software it runs on.

---

<p align="center">
  <a href="https://scitex.ai" target="_blank"><img src="docs/scitex-icon-navy-inverted.png" alt="SciTeX" width="40"/></a>
</p>

<!-- EOF -->
